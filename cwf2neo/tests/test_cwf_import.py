import os


def test_cwf_init():
    from cwf2neo import CWF

    cwf = CWF()

    cwf.setup_neo4j_connection()

    assert cwf.db.graph.database.name


def test_download_sources():
    from cwf2neo import CWF

    cwf = CWF()

    NICE_sources = cwf.config['data_sources']['NICE'].get()

    cwf.download_data_sources()

    file_to_check = os.path.join(
        cwf.temp_dir, NICE_sources['cwf']['local_filename'])
    file_to_check2 = os.path.join(
        cwf.temp_dir, NICE_sources['competencies']['local_filename'])

    assert os.path.exists(file_to_check) == 1 and \
        os.path.exists(file_to_check2) == 1
