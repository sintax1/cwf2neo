import logging
import os
import re
import shutil
import tempfile

import confuse
import xlrd
from cwf2neo.graph_objects import (KSAT, NICECategory, NICECompetency,
                                   NICECompetencyGroup, NICESpecialtyArea,
                                   NICEWorkrole, NISTCategory, NISTFunction,
                                   NISTReference, NISTSubCategory)
from cwf2neo.neo4j import Neo4j
from cwf2neo.utils import (file_download, list2dict,
                           parse_ksats, ksat_id_to_type)
from progress.bar import IncrementalBar
from progress.counter import Counter

log = logging.getLogger(__name__)

# Static list of NICE CWF Categories since we don't have an easy to parse
# source
NICE_Categories = [
    {
        'id': 'SP',
        'title': 'Securely Provision',
        'description': 'Conceptualizes, designs, procures, and/or builds '
        'secure information technology (IT) systems, with responsibility '
        'for aspects of system and/or network development.'
    },
    {
        'id': 'OM',
        'title': 'Operate and Maintain',
        'description': 'Provides the support, administration, and maintenance '
        'necessary to ensure effective and efficient information technology '
        '(IT) system performance and security'
    },
    {
        'id': 'OV',
        'title': 'Oversee and Govern',
        'description': 'Provides leadership, management, direction, or '
        'development and advocacy so the organization may effectively '
        'conduct cybersecurity work.'
    },
    {
        'id': 'PR',
        'title': 'Protect and Defend',
        'description': 'Identifies, analyzes, and mitigates threats to '
        'internal information technology (IT) systems and/or networks.'
    },
    {
        'id': 'AN',
        'title': 'Analyze',
        'description': 'Performs highly-specialized review and evaluation of '
        'incoming cybersecurity information to determine its usefulness for '
        'intelligence.'
    },
    {
        'id': 'CO',
        'title': 'Collect and Operate',
        'description': 'Provides specialized denial and deception operations '
        'and collection of cybersecurity information that may be used to '
        'develop intelligence.'
    },
    {
        'id': 'IN',
        'title': 'Investigate',
        'description': 'Investigates cybersecurity events or crimes related '
        'to information technology (IT) systems, networks, and digital '
        'evidence.'
    }
]

# NICE CWF Category to NIST Function map
NICE_Category_map = {
    'SP': ['ID', 'PR'],
    'OM': ['PR', 'DE'],
    'OV': ['ID', 'PR', 'DE', 'RC'],
    'PR': ['PR', 'DE', 'RS'],
    'AN': ['ID', 'DE', 'RS'],
    'CO': ['DE', 'PR', 'RS'],
    'IN': ['DE', 'RS', 'RC']
}


class CWF(object):
    """Main class used to parse the NICE cybersecurity Workforce Framework (CWF)
    data sources and store in a Neo4j graphing database.
    """

    def __init__(
        self, neo4j_host='localhost', neo4j_user='neo4j',
            neo4j_pass='password', neo4j_port=7687):
        """Constructor for initial setup

        :param neo4j_host: Neo4j server hostname, defaults to 'localhost'
        :type neo4j_host: str, optional
        :param neo4j_user: Neo4j login username, defaults to 'neo4j'
        :type neo4j_user: str, optional
        :param neo4j_pass: Neo4j login password, defaults to 'password'
        :type neo4j_pass: str, optional
        :param neo4j_port: Neo4j port to connect to, defaults to 7687
        :type neo4j_port: int, optional
        """
        self.temp_dir = self.__create_temp_directory()
        self.db = None
        self.config = confuse.LazyConfig('cwf2neo', __name__)
        self.neo4j_host = os.getenv('NEO4J_HOST', neo4j_host)
        self.neo4j_user = os.getenv('NEO4J_USER', neo4j_user)
        self.neo4j_pass = os.getenv('NEO4J_PASS', neo4j_pass)
        self.neo4j_port = os.getenv('NEO4J_BOLT_PORT', neo4j_port)
        self.neo4j_secure = os.getenv('NEO4J_SECURE', 'False').lower() in ('true', '1')

    def __del__(self):
        """Destructor for cleanup
        """

        self.__cleanup_temp_directory()

    def __create_temp_directory(self):
        """Private function used to create a temporary directory

        :return: absolute path to the temporary directory
        :rtype: str
        """

        self.temp_dir = tempfile.mkdtemp()
        log.info("Using temp directory: %s", self.temp_dir)
        return self.temp_dir

    def __cleanup_temp_directory(self):
        """Private function used to recursively remove the temporary directory
        """

        log.info("Cleaning up. Removing temp directory: %s", self.temp_dir)
        shutil.rmtree(self.temp_dir)

    def __download_source(self, source):
        """Private function used to recursively download data sources
         and store them in the temporary directory

        :param source: dict containing ('source_url', 'local_filename'),
         or dict of dicts.
        :type source: dict
        """

        if isinstance(source, dict):
            if set(['source_url', 'local_filename']).issubset(source.keys()):
                # Valid source, download the file
                log.info("Downloading {}".format(source['source_url']))
                file_download(
                    source['source_url'],
                    self.temp_dir,
                    source['local_filename'])
            else:
                # Not a valid source yet, use recursion to find the next
                # valid source
                for next_source in source.items():
                    self.__download_source(next_source[1])

    def initialize(self):
        """Initialize the NICE CWF Neo4j Database
        """

        # Setup Neo4j Connection
        self.setup_neo4j_connection()

        # Download the official sources of data from NIST/NICE
        self.download_data_sources()

        # Import the Cybersecurity Framework
        self.import_NIST_Cybersecurity_Framework()

        # Import the Cybersecurity Workforce Framework
        self.import_NICE_CWF()

        # Import the KSA Competencies
        self.import_NICE_Competencies()

        # Create an index for fulltext searches across all KSATs
        self.create_db_KSAT_index()

    def setup_neo4j_connection(self):
        """Configure the Neo4j connection and store an instance in the class
        """

        log.info('Configuring Neo4j connection')

        self.db = Neo4j(
            host=self.neo4j_host,
            port=self.neo4j_port,
            auth=(
                self.neo4j_user,
                self.neo4j_pass),
            secure=self.neo4j_secure
        )

    def get_temp_directory(self):
        """Get the current temp directory in use

        :return: Absolute path to the current temporary directory in use
        :rtype: str
        """

        return self.temp_dir

    def download_data_sources(self):
        """Download all the data sources listed in config.yaml
        """

        log.info('Downloading data sources')

        for data_source in self.config['data_sources'].get():
            self.__download_source(
                self.config['data_sources'][data_source].get())

    def import_NIST_Cybersecurity_Framework(self):
        """Import the NIST Cybersecurity Framework into the neo4j database
        """

        nist_function_nodes = []
        nist_category_nodes = []
        nist_subcategory_nodes = []
        nist_reference_nodes = []
        nist_category_relationships = []
        nist_subcategory_relationships = []
        nist_reference_node_relationships = []

        log.info("Importing NIST Cybersecurity Framework")

        workbook_name = \
            self.config['data_sources']['NIST']['cf']['local_filename'].get()
        workbook = xlrd.open_workbook(
            filename=os.path.join(self.temp_dir, workbook_name))

        sheet = workbook.sheet_by_name('Sheet1')

        mapped_data = list2dict(sheet._cell_values[sheet._first_full_rowx:])

        bar = IncrementalBar(
            'Importing NIST Cybersecurity Framework ',
            max=len(mapped_data),
            suffix='%(percent)d%% (%(index)d/%(max)d) [%(elapsed_td)s]')

        graph = self.db.graph

        for data in mapped_data:

            if data['Function']:
                nist_function_node = NISTFunction()
                m = re.match(r"([A-Z]+) \(([A-Z][A-Z])\)", data['Function'])
                nist_function_node.title = m[1]
                nist_function_node.id = m[2]

                # Create the node if it doesn't exist
                nist_function_nodes.append(nist_function_node)

            if data['Category']:
                m = re.match(
                    r"([a-zA-Z, ]+) \(([\S.]+)\):[ \n]?(.*)",
                    data['Category'])

                nist_category_node = NISTCategory()
                nist_category_node.title = m[1]
                nist_category_node.id = m[2]
                nist_category_node.description = m[3]

                # Create the node if it doesn't exist
                nist_category_nodes.append(nist_category_node)

                # add the category to function relationship
                nist_category_relationships.append((nist_category_node, 'NIST_FUNCTION', nist_function_node))

            if data['Subcategory']:
                m = re.match(
                    r"([A-Z][A-Z].[A-Z][A-Z]-[0-9]+): (.*)",
                    data['Subcategory'])

                nist_subcategory_node = NISTSubCategory()
                nist_subcategory_node.id = m[1]
                nist_subcategory_node.description = m[2]

                # Create the node if it doesn't exist
                nist_subcategory_nodes.append(nist_subcategory_node)

                # add the category to subcategory relationship
                nist_subcategory_relationships.append((nist_subcategory_node, 'NIST_CATEGORY', nist_category_node))

            if data['Informative References']:
                nist_reference_node = NISTReference()

                # Remove non-ascii characters
                ref = data['Informative References']
                ref = ref.encode("ascii", errors="ignore").decode()

                nist_reference_node.reference = ref.strip()

                # Create the node if it doesn't exist
                nist_reference_nodes.append(nist_reference_node)

                # add the reference to subcategory relationship
                nist_reference_node_relationships.append((nist_reference_node, 'NIST_SUBCATEGORY', nist_subcategory_node))

            bar.next()

        bar.finish()

        self.db.add_nodes(nist_function_nodes)
        self.db.add_nodes(nist_category_nodes)
        self.db.add_nodes(nist_subcategory_nodes)
        self.db.add_nodes(nist_reference_nodes)
        self.db.add_relationships(nist_category_relationships)
        self.db.add_relationships(nist_subcategory_relationships)
        self.db.add_relationships(nist_reference_node_relationships)

        log.info("Done importing NIST Cybersecurity Framework")

    def import_NICE_Workroles(self, workbook):
        """Import the NICE CWF workroles

        :param workbook: NICE CWF spreadsheet represented as a python class
        :type workbook: class 'xlrd.book.Book'
        """

        log.info("Importing NICE CWF Specialty Areas and Workroles")

        toc_sheet = workbook.sheet_by_name('Table of Contents')
        rows = list2dict(toc_sheet._cell_values[toc_sheet._first_full_rowx:])

        number_of_categories = 7

        specialty_area_nodes = []
        workrole_nodes = []
        category_relationships = []
        specialty_area_relationships = []

        bar = IncrementalBar(
            'Importing NICE CWF Specialty Areas and Workroles ',
            max=len(rows) - number_of_categories,
            suffix='%(percent)d%% (%(index)d/%(max)d) [%(elapsed_td)s]')

        for data in rows:
            if data['NICE Specialty Area']:
                m = re.search(
                    r"([a-zA-Z &,/-]+) \(([A-Z]{3})\)",
                    data['NICE Specialty Area'])
                if not m:
                    continue
                specialty_area_node = NICESpecialtyArea()
                specialty_area_node.id = m[2]
                specialty_area_node.title = m[1]

                if data['NICE Specialty Area Description']:
                    specialty_area_node.description = \
                        data['NICE Specialty Area Description']

                # create the node if it doesn't exist
                specialty_area_nodes.append(specialty_area_node)

            if data['Work Role']:
                workrole_node = NICEWorkrole()
                workrole_node.title = data['Work Role'].strip()

                log.debug("Adding {}".format(workrole_node.title))

                if data['Work Role ID']:
                    m = re.search(
                        r"([A-Z]{2})-[A-Z]{3}-[0-9]{3}",
                        data['Work Role ID'])
                    workrole_node.id = m[0]

                    # add the specialty area to nice category relationship
                    nice_category_node = NICECategory()
                    nice_category_node.id = m[1]

                    category_relationships.append((specialty_area_node, 'NICE_SPECIALTY_AREA', nice_category_node))

                if data['Work Role Description']:
                    workrole_node.description = data['Work Role Description']

                if data['OPM Code (Fed Use)']:
                    workrole_node.opm_code = data['OPM Code (Fed Use)']

                # create the node if it doesn't exist
                workrole_nodes.append(workrole_node)

                # add the workrole to specialty area relationship
                specialty_area_relationships.append((workrole_node, 'NICE_SPECIALTY_AREA', specialty_area_node))

            bar.next()

        bar.finish()

        self.db.add_nodes(specialty_area_nodes)
        self.db.add_nodes(workrole_nodes)
        self.db.add_relationships(category_relationships)
        self.db.add_relationships(specialty_area_relationships)

        log.info("Done Importing NICE CWF Specialty Areas and Workroles")

    def import_NICE_KSAT(self, workbook):
        """Import the NICE KSATs and their relationships with Workroles

        :param workbook: NICE CWF spreadsheet represented as a python class
        :type workbook: class 'xlrd.book.Book'
        """

        log.info("Parsing NICE CWF KSATs")
        bar = Counter(
            'Parsing NICE CWF KSATs ',
            suffix='%(percent)d%% (%(index)d/%(max)d) [%(elapsed_td)s]')

        all_sheets = workbook.sheets()

        knowledge_nodes = []
        skill_nodes = []
        ability_nodes = []
        task_nodes = []
        workrole_relationships = []

        for sheet in all_sheets:
            if not re.match(r"[A-Z]+-[A-Z]+-[0-9]+", sheet.name):
                continue

            workrole_id = re.match(
                r"([A-Z]{2}-[A-Z]{3}-[0-9]{3})",
                sheet.name)[1]

            for row in sheet._cell_values:
                # capture and store the KSAT unless it's a header row
                try:
                    ksat = parse_ksats(row[0])[0]
                except Exception:
                    # Ignore header rows that don't contain KSATs
                    continue

                ksat_type = ksat_id_to_type(ksat)
                ksat_node = KSAT()
                ksat_node.id = ksat
                ksat_node.description = row[1]
                ksat_node.type = ksat_type
                ksat_node.__node__.add_label(ksat_type)

                # create the node if it doesn't exist
                if ksat_type == "Knowledge":
                    knowledge_nodes.append(ksat_node)
                elif ksat_type == "Skill":
                    skill_nodes.append(ksat_node)
                elif ksat_type == "Ability":
                    ability_nodes.append(ksat_node)
                elif ksat_type == "Task":
                    task_nodes.append(ksat_node)

                workrole_node = NICEWorkrole()
                workrole_node.id = workrole_id

                workrole_relationships.append((ksat_node, 'NICE_WORKROLE', workrole_node))

                bar.next()

        bar.finish()

        self.db.add_nodes(knowledge_nodes)
        self.db.add_nodes(skill_nodes)
        self.db.add_nodes(ability_nodes)
        self.db.add_nodes(task_nodes)
        self.db.add_relationships(workrole_relationships)

        log.info("Done Parsing NICE CWF KSATs")

    def import_NICE_CWF(self):
        """Import the NICE Cybersecurity Workforce Framework into the neo4j database
        """

        self.add_NICE_Categories()

        workbook_name = os.path.basename(
            self.config['data_sources']['NICE']['cwf']['local_filename'].get())
        workbook = xlrd.open_workbook(
            filename=os.path.join(self.temp_dir, workbook_name))

        # Parse the Workroles from the NICE CWF spreadsheet table of contents
        self.import_NICE_Workroles(workbook)

        # Parse all work role KSAT sheets
        self.import_NICE_KSAT(workbook)

    def import_NICE_Competencies(self):
        """Read the NICE CWF Competencies from the pivot table and
        import into the neo4j database
        """

        NICE_ref = self.config['data_sources']['NICE']
        workbook_name = NICE_ref['competencies']['local_filename'].get()
        sheet_name = 'KSAs mapped to Competency'

        workbook = xlrd.open_workbook(
            filename=os.path.join(self.temp_dir, workbook_name))
        sheet = workbook.sheet_by_name(sheet_name)

        rows = list2dict(sheet._cell_values[sheet._first_full_rowx:])

        competencygroup_nodes = []
        competency_nodes = []
        ksat_nodes = []
        competencygroup_relationships = []
        competency_relationships = []

        log.info("Importing NICE Competencies")
        bar = IncrementalBar(
            'Importing NICE Competencies ',
            max=len(rows),
            suffix='%(percent)d%% (%(index)d/%(max)d) [%(elapsed_td)s]')

        for row in rows:
            try:
                ksats = parse_ksats(row['KSA ID'])
            except Exception as err:
                log.error("YY %s" % err)

            for ksat in ksats:
                # Get the db node matching the ksat id
                ksat_node = KSAT()
                ksat_node.id = ksat

                # Add the Competency Group
                competencygroup_node = NICECompetencyGroup()
                # Competency Group ID removed in 30 June 2020 update
                # competencygroup_node.id = row['Competency Group ID']
                # Competency Group changed to Competency Grouping in 30 June 2020 update
                competencygroup_node.name = row['Competency Grouping']

                competencygroup_nodes.append(competencygroup_node)

                # Add the Competency
                competency_node = NICECompetency()
                competency_node.id = row['Competency ID']
                competency_node.name = row['Competency']

                competency_nodes.append(competency_node)

                #competency_node.nice_competency_group.add(competencygroup_node)
                competencygroup_relationships.append((competency_node, 'NICE_COMPETENCY_GROUP', competencygroup_node))

                # Add the KSA to Competency relationship
                competency_relationships.append((ksat_node, 'NICE_COMPETENCY', competency_node))

                ksat_nodes.append(ksat_node)
            bar.next()

        self.db.add_nodes(competencygroup_nodes)
        self.db.add_nodes(competency_nodes)
        self.db.add_nodes(ksat_nodes)
        self.db.add_relationships(competencygroup_relationships)
        self.db.add_relationships(competency_relationships)

        # Import the competency definitions
        self.__import_NICE_Competency_descriptions()

        bar.finish()
        log.info("Done Importing NICE Competencies")

    def __import_NICE_Competency_descriptions(self):
        """Read the NICE CWF Competency descriptions from the pivot table and
        import into the neo4j database
        """

        NICE_ref = self.config['data_sources']['NICE']
        workbook_name = NICE_ref['competencies']['local_filename'].get()
        sheet_name = 'Competency Descriptions'

        workbook = xlrd.open_workbook(
            filename=os.path.join(self.temp_dir, workbook_name))
        sheet = workbook.sheet_by_name(sheet_name)

        rows = list2dict(sheet._cell_values[sheet._first_full_rowx:])

        # start the graph transaction
        tx = self.db.graph.begin()

        for row in rows:

            # Cypher query to update the Competency description
            statement = """MATCH (n:NICECompetency)
                        WHERE n.id = $n
                        SET n.description = $d"""

            # Add to the transaction
            tx.run(statement, n=row['Competency ID'], d=row['Description'])

        # Commit the transactions to the databse
        tx.commit()

    def create_db_KSAT_index(self):
        """Create a fulltext search index for KSATs
        """
        graph = self.db.graph

        log.info("Creating database index for KSATs")
        try:
            graph.run(
                r'CALL db.index.fulltext.createNodeIndex('
                r'"ksat_index",'
                r'["Knowledge", "Skill", "Ability", "Task"],'
                r'["id", "description"])')
        except Exception as err:
            if err.code == 'Neo.ClientError.Procedure.ProcedureCallFailed':
                log.info('KSAT Index already exists')
            else:
                raise err

        log.info("Done Creating database index for KSATs")

    def add_NICE_Categories(self):
        """Add the NICE CWF Categories to the neo4j database. Currently this is done
        using a static list within this package since there is no easy to parse
        document with all the necessary information.
        """

        log.info("Adding NICE CWF Categories")
        bar = IncrementalBar(
            'Adding NICE CWF Categories ',
            max=len(NICE_Categories),
            suffix='%(percent)d%% (%(index)d/%(max)d) [%(elapsed_td)s]')

        category_nodes = []
        category_relationships = []

        for category in NICE_Categories:
            category_node = NICECategory()
            category_node.id = category['id']
            category_node.title = category['title']
            category_node.description = category['description']

            for nist_function in NICE_Category_map[category['id']]:
                nist_function_node = NISTFunction()
                nist_function_node.id = nist_function
                category_relationships.append((category_node, 'NIST_Function', nist_function_node))
            
            category_nodes.append(category_node)

            bar.next()

        bar.finish()

        self.db.add_nodes(category_nodes)
        self.db.add_relationships(category_relationships)

        log.info("Done Adding NICE CWF Categories")
