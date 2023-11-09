import string
import random
import pytest
import yaml
from Seminar2.checkers import checkout

with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture(autouse=True, scope='module')
def make_folder():
    return checkout('mkdir -p {} {} {} {}'.format(data['folder_in'], data['folder_out'], data['folder_ext'],
                                                  data['folder_ext2']), '')


@pytest.fixture(autouse=True, scope='class')
def make_files():
    list_off_files = []
    for i in range(data['count']):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if checkout(
                'cd {};  dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock'.format(data['folder_in'], filename,
                                                                                        data['bs']), ''):
            list_off_files.append(filename)
    return list_off_files


@pytest.fixture(autouse=True, scope='module')
def clear_folder():
    return checkout('rm -rf {}/* {}/* {}/* {}/*'.format(data['folder_in'], data['folder_out'], data['folder_ext'],
                                                        data['folder_ext2']), '')


@pytest.fixture(autouse=True, scope='module')
def make_bad_arx():
    checkout('cd {}; 7z a{}/bad_arx'.format(data['folder_in'], data['folder_out']), 'Everything is Ok')
    checkout('truncate -s 1 {}/bad_arx.7z'.format( data['folder_out']), '')