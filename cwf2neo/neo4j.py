from py2neo import Graph


class Neo4j(object):

    def __init__(self, **kwargs):
        self.graph = Graph(**kwargs)
