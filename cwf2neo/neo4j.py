import logging

from py2neo import Graph

log = logging.getLogger(__name__)


class Neo4j(object):

    def __init__(self, **kwargs):
        self.graph = Graph(**kwargs)
