import os
import re
import urllib
import urllib.request


def file_download(source_url, local_dir, local_filename):
    urllib.request.urlretrieve(
        source_url, os.path.join(local_dir, local_filename))


def list2dict(list_in):
    return [dict(zip(list_in[0], c)) for c in list_in[1:]]


def parse_ksats(data_input):
    ksats = re.findall(
        r"((?:K|S|A|T)[0-9]{4})", data_input, re.IGNORECASE | re.MULTILINE)
    if not ksats:
        raise Exception("No KSATs found: %s" % data_input)
    return list(ksats)


def ksat_id_to_type(ksat_id):

    ksat_types_map = {
        'K': 'Knowledge',
        'S': 'Skill',
        'A': 'Ability',
        'T': 'Task'
    }

    ksat_prefix = ksat_id[0].upper()

    if ksat_prefix not in ksat_types_map.keys():
        raise Exception(
            "'{}' is not a valid KSAT ID".format(ksat_id))

    return ksat_types_map[ksat_prefix]
