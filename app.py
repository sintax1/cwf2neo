#!/usr/bin/env python

# import logging
from cwf2neo import CWF
import logging

# Set logging level for more verbose output
logging.basicConfig(level=logging.INFO)

# Get an instance of the CWF object used to interact with the Neo4j database
cwf = CWF()

# Set the neo4j hostname to connect to
cwf.config['neo4j']['host'] = 'neo4j'

# Import the NIST/NICE data into Neo4j
cwf.initialize()
