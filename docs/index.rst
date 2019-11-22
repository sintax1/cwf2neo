=======
cwf2neo
=======

cwf2neo is a Python library used to download, parse and import
the `NICE Cybersecurity Workforce Framework`_ into a Neo4j_ graph database,
which can be used to run complex queries against.

.. note::

    cwf2neo requires a Neo4j database running and accessible.
    See `Neo4j Getting Started`_ to install one or `Neo4j Docker`_ to simply run a Neo4j Docker container.

***************
Getting Started
***************

This Python library has been published to PyPI for easy installation using pip.

.. code-block:: bash

    # Download and install cwf2neo package from PyPI
    pip install --user cwf2neo

.. code-block:: python

    import logging
    from cwf2neo import CWF

    # Set logging level for more verbose output
    logging.basicConfig(level=logging.INFO)

    # Get an instance of the CWF object used to interact with the Neo4j database
    cwf = CWF(neo4j_host='localhost', neo4j_user='neo4j', neo4j_pass='password', neo4j_port=7687)

    # Import the NIST/NICE data into Neo4j
    cwf.initialize()


Example Output:

.. code-block:: bash

    $ python3
    Python 3.7.1 (default, Nov 28 2018, 11:51:47)
    [Clang 10.0.0 (clang-1000.11.45.5)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import logging
    >>> from cwf2neo import CWF
    >>> cwf = CWF(neo4j_host='localhost', neo4j_user='neo4j', neo4j_pass='password', neo4j_port=7687)
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


******
Docker
******

A handy Docker configuration is also provided to make it even easier
to get started.

.. note::

    Requires Docker with docker-compose installed.

-----------------------------
Bring your own Neo4j database
-----------------------------

If you want to use your own Neo4j database, simply clone the cwf2neo repo,
edit the .env file, and start the cwf2neo parser.

.. code-block:: bash

    $ git clone https://github.com/sintax1/cwf2neo

    Cloning into 'cwf2neo'...
    remote: Enumerating objects: 230, done.
    remote: Counting objects: 100% (230/230), done.
    remote: Compressing objects: 100% (143/143), done.
    remote: Total 485 (delta 140), reused 161 (delta 81), pack-reused 255
    Receiving objects: 100% (485/485), 2.61 MiB | 2.45 MiB/s, done.
    Resolving deltas: 100% (293/293), done.

    $ cd cwf2neo/

    $ vim .env

    NEO4J_HOST=neo4j       # The hostname/IP of your Neo4j database
    NEO4J_HTTP_PORT=7474   # The port for Neo4j's http service
    NEO4J_BOLT_PORT=7687   # The port for Neo4j's bolt service
    NEO4J_USER=neo4j       # Neo4j username
    NEO4J_PASS=mypass      # NEo4j password

    $docker-compose up cwf2neo

    Starting cwf2neo_cwf2neo_1 ... done
    Attaching to cwf2neo_cwf2neo_1
    cwf2neo_1  | wait-for-it.sh: waiting 15 seconds for neo4j:7474
    cwf2neo_1  | wait-for-it.sh: neo4j:7474 is available after 7 seconds
    cwf2neo_1  | INFO:cwf2neo.cwf2neo:Using temp directory: /tmp/tmpsf1pa8jz
    cwf2neo_1  | INFO:cwf2neo.cwf2neo:Configuring Neo4j connection
    cwf2neo_1  | INFO:cwf2neo.cwf2neo:Downloading data sources
    cwf2neo_1  | INFO:cwf2neo.cwf2neo:Downloading https://www.nist.gov/file/448306
    cwf2neo_1  | INFO:cwf2neo.cwf2neo:Downloading https://www.nist.gov/document/supplementnicespecialtyareasandworkroleksasandtasksxlsx
    cwf2neo_1  | INFO:cwf2neo.cwf2neo:Downloading https://www.nist.gov/document/niceframeworkksatocompetencymappingxlsx
    cwf2neo_1  | INFO:cwf2neo.cwf2neo:Importing NIST Cybersecurity Framework
    cwf2neo_1  | INFO:cwf2neo.cwf2neo:Done importing NIST Cybersecurity Framework
    cwf2neo_1  | INFO:cwf2neo.cwf2neo:Adding NICE CWF Categories
    cwf2neo_1  | INFO:cwf2neo.cwf2neo:Done Adding NICE CWF Categories
    cwf2neo_1  | INFO:cwf2neo.cwf2neo:Importing NICE CWF Specialty Areas and Workroles
    cwf2neo_1  | INFO:cwf2neo.cwf2neo:Done Importing NICE CWF Specialty Areas and Workroles
    cwf2neo_1  | INFO:cwf2neo.cwf2neo:Parsing NICE CWF KSATs
    cwf2neo_1  | INFO:cwf2neo.cwf2neo:Done Parsing NICE CWF KSATs
    cwf2neo_1  | INFO:cwf2neo.cwf2neo:Importing NICE Competencies
    cwf2neo_1  | INFO:cwf2neo.cwf2neo:Done Importing NICE Competencies
    cwf2neo_1  | INFO:cwf2neo.cwf2neo:Creating database index for KSATs
    cwf2neo_1  | INFO:cwf2neo.cwf2neo:KSAT Index already exists
    cwf2neo_1  | INFO:cwf2neo.cwf2neo:Done Creating database index for KSATs
    cwf2neo_1  | INFO:cwf2neo.cwf2neo:Cleaning up. Removing temp directory: /tmp/tmpsf1pa8jz
    cwf2neo_cwf2neo_1 exited with code 0


-----------------------
Neo4j database included
-----------------------

The following steps will also start up a Neo4j database for you.

.. code-block:: bash

    $ git clone https://github.com/sintax1/cwf2neo

    Cloning into 'cwf2neo'...
    remote: Enumerating objects: 230, done.
    remote: Counting objects: 100% (230/230), done.
    remote: Compressing objects: 100% (143/143), done.
    remote: Total 485 (delta 140), reused 161 (delta 81), pack-reused 255
    Receiving objects: 100% (485/485), 2.61 MiB | 2.45 MiB/s, done.
    Resolving deltas: 100% (293/293), done.

    $ cd cwf2neo/

    $ vim .env

    NEO4J_HOST=neo4j       # The hostname/IP of your Neo4j database
    NEO4J_HTTP_PORT=7474   # The port for Neo4j's http service
    NEO4J_BOLT_PORT=7687   # The port for Neo4j's bolt service
    NEO4J_USER=neo4j       # Neo4j username
    NEO4J_PASS=mypass      # NEo4j password

    $ docker-compose up

    Starting cwf2neo_cwf2neo_1 ... done
    Starting cwf2neo_neo4j_1   ... done
    Attaching to cwf2neo_cwf2neo_1, cwf2neo_neo4j_1
    cwf2neo_1  | wait-for-it.sh: waiting 15 seconds for neo4j:7474
    neo4j_1    | Active database: graph.db
    neo4j_1    | Directories in use:
    neo4j_1    |   home:         /var/lib/neo4j
    neo4j_1    |   config:       /var/lib/neo4j/conf
    neo4j_1    |   logs:         /logs
    neo4j_1    |   plugins:      /var/lib/neo4j/plugins
    neo4j_1    |   import:       /var/lib/neo4j/import
    neo4j_1    |   data:         /var/lib/neo4j/data
    neo4j_1    |   certificates: /var/lib/neo4j/certificates
    neo4j_1    |   run:          /var/lib/neo4j/run
    neo4j_1    | Starting Neo4j.
    neo4j_1    | 2019-11-22 15:21:40.294+0000 INFO  ======== Neo4j 3.5.12 ========
    neo4j_1    | 2019-11-22 15:21:40.319+0000 INFO  Starting...
    neo4j_1    | 2019-11-22 15:21:45.554+0000 INFO  Bolt enabled on 0.0.0.0:7687.
    neo4j_1    | 2019-11-22 15:21:48.954+0000 INFO  Started.
    neo4j_1    | 2019-11-22 15:21:51.033+0000 INFO  Remote interface available at http://localhost:7474/
    cwf2neo_1  | wait-for-it.sh: timeout occurred after waiting 15 seconds for neo4j:7474
    cwf2neo_1  | INFO:cwf2neo.cwf2neo:Using temp directory: /tmp/tmpsf1pa8jz
    cwf2neo_1  | INFO:cwf2neo.cwf2neo:Configuring Neo4j connection
    cwf2neo_1  | INFO:cwf2neo.cwf2neo:Downloading data sources
    cwf2neo_1  | INFO:cwf2neo.cwf2neo:Downloading https://www.nist.gov/file/448306
    cwf2neo_1  | INFO:cwf2neo.cwf2neo:Downloading https://www.nist.gov/document/supplementnicespecialtyareasandworkroleksasandtasksxlsx
    cwf2neo_1  | INFO:cwf2neo.cwf2neo:Downloading https://www.nist.gov/document/niceframeworkksatocompetencymappingxlsx
    cwf2neo_1  | INFO:cwf2neo.cwf2neo:Importing NIST Cybersecurity Framework
    cwf2neo_1  | INFO:cwf2neo.cwf2neo:Done importing NIST Cybersecurity Framework
    cwf2neo_1  | INFO:cwf2neo.cwf2neo:Adding NICE CWF Categories
    cwf2neo_1  | INFO:cwf2neo.cwf2neo:Done Adding NICE CWF Categories
    cwf2neo_1  | INFO:cwf2neo.cwf2neo:Importing NICE CWF Specialty Areas and Workroles
    cwf2neo_1  | INFO:cwf2neo.cwf2neo:Done Importing NICE CWF Specialty Areas and Workroles
    cwf2neo_1  | INFO:cwf2neo.cwf2neo:Parsing NICE CWF KSATs
    cwf2neo_1  | INFO:cwf2neo.cwf2neo:Done Parsing NICE CWF KSATs
    cwf2neo_1  | INFO:cwf2neo.cwf2neo:Importing NICE Competencies
    cwf2neo_1  | INFO:cwf2neo.cwf2neo:Done Importing NICE Competencies
    cwf2neo_1  | INFO:cwf2neo.cwf2neo:Creating database index for KSATs
    cwf2neo_1  | INFO:cwf2neo.cwf2neo:KSAT Index already exists
    cwf2neo_1  | INFO:cwf2neo.cwf2neo:Done Creating database index for KSATs
    cwf2neo_1  | INFO:cwf2neo.cwf2neo:Cleaning up. Removing temp directory: /tmp/tmpsf1pa8jz
    cwf2neo_cwf2neo_1 exited with code 0

    # Connect to http://localhost:7474/browser/ using a web browser to access Neo4j.

   
Congratulations! The NICE CWf is ready for access in your Neo4j database.
See :ref:`Cypher Query Language Examples` to get started using the database.

.. _NICE Cybersecurity Workforce Framework: https://www.nist.gov/itl/applied-cybersecurity/nice/resources/nice-cybersecurity-workforce-framework
.. _Neo4j: https://neo4j.com/
.. _Neo4j Getting Started: https://neo4j.com/developer/get-started/
.. _Neo4j Docker: https://hub.docker.com/_/neo4j
