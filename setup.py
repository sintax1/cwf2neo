from setuptools import setup

setup(
    name='cwf2neo',
    version='0.16.0',
    packages=['cwf2neo'],
    include_package_data=True,
    license='Apache License 2.0',
    description='cwf2neo is a Python library use to download, '
    'parse and import the NICE Cybersecurity Workforce Framework '
    'into a Neo4j graphing database.',
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
