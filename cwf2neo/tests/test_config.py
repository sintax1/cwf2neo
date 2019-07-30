
def test_config_parse():
    """Test yaml configuration
    """
    from cwf2neo import CWF
    cwf = CWF()

    assert cwf.config['neo4j']['host'].get() == "localhost"
