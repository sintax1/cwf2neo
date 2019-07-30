
def test_config_parse():
    """Test yaml configuration
    """
    from cwf2neo import config

    print(config.__dict__)

    assert config['neo4j']['host'].get() == "localhost"
