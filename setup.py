from setuptools import setup

setup(
    name='cwf2neo',
    version='0.13.0',
    packages=['cwf2neo'],
    data_files=[
        'cwf2neo/config_default.yaml'
    ],
    license='Apache License 2.0',
    description='cwf2neo is a Python library use to download, '
    'parse and import the NICE Cybersecurity Workforce Framework '
    'into a Neo4J graphing database.',
    author_email='ckoroscil@circadence.com',
    install_requires=[
        'confuse',
        'progress',
        'py2neo',
        'xlrd',
        'bumpversion',
        'twine'
    ]
)
