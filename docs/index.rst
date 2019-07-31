=======
cwf2neo
=======

cwf2neo is a Python library used to download, parse and import
the `NICE Cybersecurity Workforce Framework`_ into a Neo4j_ graphing database,
which can be used to run complex queries against.

.. note::

    cwf2neo requires a Neo4j database.
    See `Neo4j Getting Started`_ to install one or `Neo4j Docker`_ to simply use a Docker container.

***************
Getting Started
***************

.. code-block:: bash

    pip install --user cwf2neo

.. code-block:: python

    import logging
    from cwf2neo import CWF

    # Set logging level for more verbose output
    logging.basicConfig(level=logging.INFO)

    # Get an instance of the CWF object used to interact with the Neo4j database
    cwf = CWF()

    # Import the NIST/NICE data into Neo4j
    cwf.initialize()

.. code-block:: bash

    $ python3
    Python 3.7.1 (default, Nov 28 2018, 11:51:47)
    [Clang 10.0.0 (clang-1000.11.45.5)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import logging
    >>> from cwf2neo import CWF
    >>> cwf = CWF()
    >>> logging.basicConfig(level=logging.INFO)
    >>> cwf.initialize()
    INFO:cwf2neo.cwf2neo:Configuring Neo4j connection
    INFO:cwf2neo.cwf2neo:Downloading data sources
    INFO:cwf2neo.cwf2neo:Downloading https://www.nist.gov/file/448306
    INFO:cwf2neo.cwf2neo:Downloading https://www.nist.gov/document/supplementnicespecialtyareasandworkroleksasandtasksxlsx
    INFO:cwf2neo.cwf2neo:Downloading https://www.nist.gov/document/niceframeworkksatocompetencymappingxlsx
    INFO:cwf2neo.cwf2neo:Importing NIST Cybersecurity Framework
    Importing NIST Cybersecurity Framework  |████████████████████████████████| 100% (504/504) [0:00:12]
    INFO:cwf2neo.cwf2neo:Done importing NIST Cybersecurity Framework
    INFO:cwf2neo.cwf2neo:Adding NICE CWF Categories
    Adding NICE CWF Categories  |████████████████████████████████| 100% (7/7) [0:00:00]
    INFO:cwf2neo.cwf2neo:Done Adding NICE CWF Categories
    INFO:cwf2neo.cwf2neo:Importing NICE CWF Specialty Areas and Workroles
    Importing NICE CWF Specialty Areas and Workroles  |████████████████████████████████| 100% (52/52) [0:00:08]
    INFO:cwf2neo.cwf2neo:Done Importing NICE CWF Specialty Areas and Workroles
    INFO:cwf2neo.cwf2neo:Parsing NICE CWF KSATs
    Parsing NICE CWF KSATs 4586
    INFO:cwf2neo.cwf2neo:Done Parsing NICE CWF KSATs
    INFO:cwf2neo.cwf2neo:Importing NICE Competencies
    Importing NICE Competencies  |████████████████████████████████| 100% (3269/3269) [0:02:35]
    INFO:cwf2neo.cwf2neo:Done Importing NICE Competencies
    INFO:cwf2neo.cwf2neo:Creating database index for KSATs
    INFO:cwf2neo.cwf2neo:KSAT Index already exists
    INFO:cwf2neo.cwf2neo:Done Creating database index for KSATs
    >>>

    # The NICE CWF is ready to use in your Neo4j database!

See :ref:`Cypher Query Language Examples` to get started using the database.

.. _NICE Cybersecurity Workforce Framework: https://www.nist.gov/itl/applied-cybersecurity/nice/resources/nice-cybersecurity-workforce-framework
.. _Neo4j: https://neo4j.com/
.. _Neo4j Getting Started: https://neo4j.com/developer/get-started/
.. _Neo4j Docker: https://hub.docker.com/_/neo4j
