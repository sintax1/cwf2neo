import logging

from cwf2neo import CWF

logging.basicConfig(format='%(asctime)s %(levelname)s\t%(message)s',
                    level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

# Get an instance of the CWF object used to interact with Neo4j database
cwf = CWF()

# Import the NIST/NICE data into Neo4j
cwf.initialize()
