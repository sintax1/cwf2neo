===========
config.yaml
===========

Configuration file used to define Neo4j connection parameters and
NIST/NICE data sources.


neo4j configuration
===================

.. code-block:: yaml

    neo4j:
      host: localhost
      user: neo4j
      pass: password
      port: 7687

host
""""
Hostname used to connect to a Neo4j database

user
""""
Username used to login to a Neo4j database

pass
""""
Password used to login to a Neo4j database

port
""""
Port used to connect to the Neo4j Connector (Default: Bolt)


data_sources configuration
==========================

.. code-block:: yaml

    data_sources:
      NIST:
        cf:
          source_url: https://www.nist.gov/file/448306
          local_filename: 2018-04-16_framework_v1.1_core1.xlsx
      NICE:
        cwf:
          source_url: https://www.nist.gov/document/supplementnicespecialtyareasandworkroleksasandtasksxlsx
          local_filename: supplement_nice_specialty_areas_and_work_role_ksas_and_tasks.xlsx
        competencies:
          source_url: https://www.nist.gov/document/niceframeworkksatocompetencymappingxlsx
          local_filename: nice_framework_ksa_to_competency_mapping.xlsx

NIST.cf
"""""""
NIST Cybersecurity Framework data source configuration

NICE.cwf
""""""""
NICE Cybersecurity Workforce Framework data source configuration

NICE.competencies
"""""""""""""""""
NIST Cybersecurity Framework Competencies data source configuration

source_url
""""""""""
URL of the data source

local_filename
""""""""""""""
filename used to store the reference document locally
