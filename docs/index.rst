=======
cwf2neo
=======

cwf2neo is a Python library use to download, parse and import
the `NICE Cybersecurity Workforce Framework`_ into a Neo4j_ graphing database.

***************
Getting Started
***************

.. code-block:: bash

    pip install --user cwf2neo

.. code-block:: python

    from cwf2neo import CWF

    # Get an instance of the CWF object used to interact with the Neo4j database
    cwf = CWF()

    # Import the NIST/NICE data into Neo4j
    cwf.initialize()

    # The NICE CWF is ready to use in your Neo4j database!

.. _NICE Cybersecurity Workforce Framework: https://www.nist.gov/itl/applied-cybersecurity/nice/resources/nice-cybersecurity-workforce-framework
.. _Neo4j: https://neo4j.com/
