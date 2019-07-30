=============
Usage Example
=============

.. code-block:: python

    import logging

    from cwf2neo import CWF

    logging.basicConfig(format='%(asctime)s %(levelname)s\t%(message)s',
                        level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

    # Get an instance of the CWF object used to interact with Neo4j database
    cwf = CWF()

    # Import the NIST/NICE data into Neo4j
    cwf.initialize()

.. code-block::

    $ python3
    Python 3.7.1 (default, Nov 28 2018, 11:51:47)
    [Clang 10.0.0 (clang-1000.11.45.5)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from cwf2neo import CWF
    >>> cwf = CWF()
    >>> cwf.initialize()
    Importing NIST Cybersecurity Framework  |████████████████████████████████| 100% (504/504) [0:00:13]
    Adding NICE CWF Categories  |████████████████████████████████| 100% (7/7) [0:00:00]
    Importing NICE CWF Specialty Areas and Workroles  |████████████████████████████████| 100% (52/52) [0:00:09]
    Parsing NICE CWF KSATs 4586
    Importing NICE Competencies  |████████████████████████████████| 100% (3269/3269) [0:02:37]
    >>>
