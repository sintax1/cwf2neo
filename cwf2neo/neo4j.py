import os
import logging

from py2neo import Graph

log = logging.getLogger(__name__)


class Neo4j(object):

    def __init__(self, **kwargs):
        if 'NEO4J_HOSTNAME' in os.environ.keys():
            log.info("Setting Neo4j Hostname to: {}".format(
                os.environ['NEO4J_HOSTNAME']))
            kwargs['host'] = os.environ['NEO4J_HOSTNAME']
        if 'NEO4J_AUTH' in os.environ.keys():
            kwargs['auth'] = os.environ['NEO4J_AUTH'].split("/")
        self.graph = Graph(**kwargs)
