import os
import logging

from py2neo import Graph
from py2neo.bulk import merge_nodes, merge_relationships
from py2neo.errors import *
from itertools import islice

log = logging.getLogger(__name__)


class Neo4j(object):

    def __init__(self, **kwargs):
        log.info("Neo4j connection settings: {}".format(kwargs))
        self.graph = Graph(**kwargs)

    def add_nodes(self, nodes):
        data = []

        log.info("Sending bulk nodes to the database")

        for node in nodes:
            data.append(dict(node.__node__))
        
        if data:
            merge_key = tuple([list(nodes[0].__node__._labels)[0]] + list(nodes[0].__node__.keys()))
            self.__merge_nodes(data, merge_key, labels=nodes[0].__node__._labels)
    
    def __merge_nodes(self, data, merge_key=('pk'), labels=None):
        stream = iter(data)
        batch_size = 1000

        while True:
            batch = list(islice(stream, batch_size))
            if batch:
                merge_nodes(self.graph.auto(), batch, merge_key, labels)
            else:
                break

    def add_relationships(self, relationships):
        data = []

        for relationship in relationships:
            relationship_details = relationship[3] if len(relationship) == 4 else {}

            data.append((tuple(relationship[0].__node__.values()), relationship_details, tuple(relationship[2].__node__.values())))

        if data:
            start_node_key = [list(relationships[0][0].__node__._labels)[0],] + list(relationships[0][0].__node__.keys())
            end_node_key = [list(relationships[0][2].__node__._labels)[0],] + list(relationships[0][2].__node__.keys())

            self.__merge_relationships(data, relationships[0][1], tuple(start_node_key), tuple(end_node_key))

    def __merge_relationships(self, data, merge_key, start_node_key, end_node_key):
        stream = iter(data)
        batch_size = 1000

        log.info("Sending bulk relationships to the database")

        while True:
            batch = list(islice(stream, batch_size))
            if batch:
                merge_relationships(
                    self.graph.auto(),
                    batch,
                    merge_key,
                    start_node_key=start_node_key,
                    end_node_key=end_node_key
                )
            else:
                break

        