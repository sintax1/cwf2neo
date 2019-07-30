import logging

import pytest
from neobolt.addressing import AddressError
from neobolt.exceptions import AuthError, ServiceUnavailable

log = logging.getLogger(__name__)


def test_db_connection():
    """Test the Neo4j connection
    """

    from cwf2neo.neo4j import Neo4j

    db = Neo4j()

    assert db.graph.database.name


def test_db_connection_bad_auth():
    """Ensure an Exception is raised when unable to authenticate to Neo4j
    """
    with pytest.raises(
            AttributeError,
            match=r".*'NoneType' object has no attribute 'split'.*") as err:

        with pytest.raises(
                AuthError,
                match=r".*authentication failure.*") as err2:

            from cwf2neo.neo4j import Neo4j

            db = Neo4j(auth=('baduser', 'badpass'))

            db.graph.database.name

        assert err2.type is AuthError

    assert err.type is AttributeError


def test_db_connection_bad_port():
    """Ensure an exception is raised when unable to connect to Neo4j service
    """

    with pytest.raises(ServiceUnavailable, match=r".*Connection refused.*"):

        from cwf2neo.neo4j import Neo4j

        db = Neo4j(port=1234)

        db.graph.database.name


def test_db_connection_bad_host():
    """Ensure an Exception is raised if a hostname is unable to be resolved
    """

    with pytest.raises(AddressError, match=r"Cannot resolve address .*"):

        from cwf2neo.neo4j import Neo4j

        db = Neo4j(host="invalidneo4jhostname")

        db.graph.database.name
