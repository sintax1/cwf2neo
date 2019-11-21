
def test_config_parse():
    """Test yaml configuration
    """
    from cwf2neo import CWF
    cwf = CWF()

    assert cwf.config['data_sources']['NIST']['cf']['source_url'].get() == \
        "https://www.nist.gov/file/448306"
