import os
import logging

from py2neo import Graph

log = logging.getLogger(__name__)


class Neo4j(object):

    def __init__(self, **kwargs):
        log.debug("Neo4j connection settings: {}".format(kwargs))
        self.graph = Graph(**kwargs)
