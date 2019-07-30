import os
import shutil
import tempfile

import pytest
from cwf2neo import CWF
from cwf2neo.utils import file_download, list2dict, parse_ksats


def test_file_download():
    """Ensure the function used to download files produces files on disk
     as expected
    """
    cwf = CWF()

    temp_dir = tempfile.mkdtemp()
    cwf = cwf.config['data_sources']['NICE']['cwf'].get()

    file_download(cwf['source_url'], temp_dir, cwf['local_filename'])

    assert os.path.exists(os.path.join(temp_dir, cwf['local_filename'])) == 1

    shutil.rmtree(temp_dir)


def test_list2dict():
    """Ensure a list of lists is properly converted to a list of dicts
    """

    list_in = [
        ['header1', 'header2', 'header3'],
        ['data1', 'data2', 'data3'],
        ['data4', 'data5', 'data6']
    ]
    dict_compare = [
        {'header1': 'data1', 'header2': 'data2', 'header3': 'data3'},
        {'header1': 'data4', 'header2': 'data5', 'header3': 'data6'}
    ]
    dict_out = list2dict(list_in)

    assert dict_out == dict_compare


def test_parse_ksats():
    """Ensure all KSATs are parsed from a text string
    """

    text_in = "abc K0012 X1234 S1234 aB12 A9876 K123 .?#T9999"
    list_compare = ['K0012', 'S1234', 'A9876', 'T9999']
    list_out = parse_ksats(text_in)

    assert list_out == list_compare


def test_parse_ksats_exception():
    """Ensure Exception is raised when no KSATs are found
    """

    with pytest.raises(Exception, match=r".*No KSATs found.*"):
        text_in = "abc X1234 aB12 K123 .?#"
        parse_ksats(text_in)
