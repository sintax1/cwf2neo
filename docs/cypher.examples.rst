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

Show all KSATs for the 'Cyber Defense Analyst' Workrole
=======================================================
.. code-block:: cypher

    MATCH (w:NICEWorkrole {title:'Cyber Defense Analyst'})--(k:KSAT)
    RETURN DISTINCT k.id, k.description ORDER BY k.id, k.description

Show all Workroles related to Knowledge K0019
=============================================

.. code-block:: cypher

    MATCH (k:Knowledge {id:'K0019'})--(w:NICEWorkrole)
    RETURN DISTINCT w.title

Show the common KSATs across all 52 Workroles
=============================================

.. code-block:: cypher

    MATCH (w:NICEWorkrole)-[r]-(k:KSAT)
    WITH k, COUNT(r) AS rels
    WHERE rels = 52
    RETURN DISTINCT k.id, k.description

Show all KSAs and Workroles related to the 'Policy Management' Competency
=========================================================================

.. code-block:: cypher

    MATCH (c:NICECompetency {name:"Policy Management"})--(k:KSAT)
    MATCH (k)--(w:NICEWorkrole)
    WITH c, k, COLLECT(w.title) AS Workroles
    RETURN DISTINCT c.name, c.description, k.id, k.description, Workroles

Show all Workroles and Competencies related to a list of KSATs
==============================================================

.. note::

    This query is ideal for aligning an organization's curriculum to
    NICE Workroles and Competencies once the curriculum has been mapped to KSATs.

.. code-block:: cypher

    MATCH (k:KSAT)--(w:NICEWorkrole)
    WHERE k.id IN ["K0101", "K0102", "S0039", "A0055", "T0023"]
    OPTIONAL MATCH (k)--(c:NICECompetency)
    WITH k, c, COLLECT(DISTINCT w.title) AS Workroles
    RETURN DISTINCT k.id, k.description, c.id, c.name, c.description, Workroles

Use `full-text search`_ to find KSATs related to a given task description
=========================================================================

.. code-block:: cypher

    CALL db.index.fulltext.queryNodes('ksat_index', 'important techniques for protecting your Linux Unix systems from external attacks')
    YIELD node, score
    WITH *
    WHERE score > 0.2
    RETURN node.id, node.description, score

Show All Workroles related to NIST Recover Function
===================================================

.. note::

    These relationaships are based on `NIST SP 800-181`_, Table 8 - Crosswalk of NICE Framework
    Workforce Categories to Cybersecurity Framework.

.. code-block:: cypher

    MATCH (n:NISTFunction {title:"RECOVER"})--(nc:NICECategory)--(ns:NICESpecialtyArea)--(w:NICEWorkrole)
    RETURN n.title AS `NIST Function`, nc.title AS `NICE Category`, ns.title AS `NICE Specialty Area`, w.title AS `Workrole`, w.description AS `Workrole Description`

.. _cypher: https://neo4j.com/developer/cypher-query-language/
.. _`Neo4j Browser`: https://neo4j.com/developer/guide-neo4j-browser/
.. _`Neo4j Driver/API`: https://neo4j.com/docs/
.. _`full-text search`: https://neo4j.com/docs/cypher-manual/3.5/schema/index/#schema-index-fulltext-search
.. _NIST SP 800-181: https://www.nist.gov/itl/applied-cybersecurity/nice/resources/nice-cybersecurity-workforce-framework
