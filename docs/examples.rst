******************************
Cypher Query Language Examples
******************************

Some example cypher_ queries to help get started using the
NIST/NICE data in Neo4j.

.. code-block:: cypher

    MATCH (w:NICEWorkrole {title:'Cyber Defense Analyst'})--(k:KSAT)
    OPTIONAL MATCH (k)-[*..2]-(c:Content)
    RETURN DISTINCT k.id, k.description, COLLECT(c.name) AS Content ORDER BY k.id, k.description

.. _cypher: https://neo4j.com/developer/cypher-query-language/
