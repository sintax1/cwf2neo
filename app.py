#!/usr/bin/env python

# import logging
from cwf2neo import CWF
import logging

# Set logging level for more verbose output
logging.basicConfig(level=logging.INFO)

# Get an instance of the CWF object used to interact with the Neo4j database
cwf = CWF(neo4j_host='neo4j', neo4j_user='neo4j', neo4j_pass='password', neo4j_port=7687)

# Import the NIST/NICE data into Neo4j
cwf.initialize()
