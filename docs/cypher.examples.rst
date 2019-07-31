==============================
Cypher Query Language Examples
==============================

Some example cypher_ queries to help get started using the
NIST/NICE data in Neo4j after successfully importing the data
using this (*cwf2neo*) python library.

.. note::

    Executing Cypher queries will require you to connect to Neo4j using the built-in `Neo4j Browser`_ (If installed locally: `http://localhost:7474/browser/ <http://localhost:7474/browser/>`_) or your favorite `Neo4j Driver/API`_ tool.

    For example,

    .. image:: _static/images/neo4j_screenshot.png
        :width: 400
        :alt: Neo4j Screenshot
        :align: center

----

Show All KSATs for the 'Cyber Defense Analyst' Workrole
=======================================================
.. code-block:: cypher

    MATCH (w:NICEWorkrole {title:'Cyber Defense Analyst'})--(k:KSAT)
    RETURN DISTINCT k.id, k.description ORDER BY k.id, k.description

Show All Workroles related to Knowledge K0019
=============================================
.. code-block:: cypher

    MATCH (k:Knowledge {id:'K0019'})--(w:NICEWorkrole)
    RETURN DISTINCT w.title

Show All KSATs relevant for for all 52 Workroles
================================================
.. code-block:: cypher

    MATCH (w:NICEWorkrole)-[r]-(k:KSAT)
    WITH k, COUNT(r) AS rels
    WHERE rels = 52
    RETURN DISTINCT k.id, k.description

.. _cypher: https://neo4j.com/developer/cypher-query-language/
.. _`Neo4j Browser`: https://neo4j.com/developer/guide-neo4j-browser/
.. _`Neo4j Driver/API`: https://neo4j.com/docs/
