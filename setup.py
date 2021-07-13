from pathlib import Path

from setuptools import setup

readme = Path(__file__).parent.joinpath('README.md')
if readme.exists():
    with readme.open() as f:
        long_description = f.read()
else:
    long_description = '-'

setup(
    name='cwf2neo',
    version='0.74.0',
    packages=['cwf2neo'],
    include_package_data=True,
    license='Apache License 2.0',
    description='cwf2neo is a Python library use to download, parse and import'
    ' the NICE Cybersecurity Workforce Framework into a Neo4j graphing'
    ' database, which can be used to run complex queries against.',
    author_email='ckoroscil@circadence.com',
    install_requires=[
        'confuse',
        'progress',
        'py2neo',
        'xlrd==1.2.0'
    ]
)
