from setuptools import setup

setup(
    name='cwf2neo',
    version='0.15.0',
    packages=['cwf2neo'],
    package_dir={'cwf2neo': 'cwf2neo'},
    package_data={'cwf2neo': ['cwf2neo/config_default.yaml']},
    include_package_data=True,
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
