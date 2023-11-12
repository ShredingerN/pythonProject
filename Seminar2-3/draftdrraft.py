import string
import random
import pytest
import yaml
from datetime import datetime
from checkers import checkout
from checkers import hash_func


with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def make_folder():
    return checkout('mkdir {} {} {} {}'.format(data['folder_in'], data['folder_out'], data['folder_ext'],
                                               data['folder_ext2']), '')


@pytest.fixture()
def clear_folder():
    return checkout('rm -rf {}/* {}/* {}/* {}/*'.format(data['folder_in'], data['folder_out'], data['folder_ext'],
                                                        data['folder_ext2']), '')


@pytest.fixture()
def make_files():
    list_off_files = []
    for i in range(data['count']):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if checkout(
                'cd {};  dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock'.format(data['folder_in'], filename,
                                                                                        data['bs']), ''):
            list_off_files.append(filename)
    return list_off_files


# @pytest.fixture()
# def make_bad_arx():
#     checkout('cd {}; 7z a{}/bad_arx'.format(data['folder_in'], data['folder_out']), 'Everything is Ok')
#     checkout('truncate -s 1 {}/bad_arx.7z'.format(data['folder_out']), '')

@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not checkout('cd {}; mkdir {}'.format(data['folder_in'], subfoldername), ''):
        return None, None
    if not checkout(
            'cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock'.format(data['folder_in'], subfoldername,
                                                                                      testfilename), ''):
        return subfoldername, None
    else:
        return subfoldername, testfilename


@pytest.fixture(autouse=True)
def print_time():
    print('Start: {}'.format(datetime.now().strftime('%H:%M:%S.%f')))
    yield
    print('Finish: {}'.format(datetime.now().strftime('%H:%M:%S.%f')))

class TestPositive:
    def test_step1(self, make_folder, clear_folder, make_files):
        result1 = checkout('cd {}; 7z a {}/arx2'.format(data['folder_in'], data['folder_out']), 'Everything is Ok')
        result2 = checkout('cd {}; ls'.format(data['folder_out']), 'arx2.7z')
        assert result1 and result2, 'test1 Fail'

    # ДЗ. Тест для сравнения полученных хэшей
    def test1_hash(self):
        result1 = hash_func('cd {}; crc32 arx2.7z'.format(data['folder_out'])).upper()
        result2 = hash_func('cd {}; 7z h arx2.7z'.format(data['folder_out']))
        assert result1 in result2, 'test1_hash Fail'

    # def test1_hash(self, clear_folders, make_files):
    #     # test8
    #     res = []
    #     for i in make_files:
    #         res.append(checkout("cd {}; 7z h {}".format(data["folder_in"], i), "Everything is Ok"))
    #         hash = hash_func("cd {}; crc32 {}".format(data["folder_in"], i)).upper()
    #         res.append(checkout("cd {}; 7z h {}".format(data["folder_in"], i), hash))
    #     assert all(res), " test1_hash"

    def test_step2(self, make_files):
        res = []
        res.append(checkout('cd {}; 7z a {}/arx2'.format(data['folder_in'], data['folder_out']), 'Everything is Ok'))
        res.append(checkout('cd {}; 7z e arx2.7z -o{} -y'.format(data['folder_out'], data['folder_ext']),
                            'Everything is Ok'))
        for i in make_files:
            res.append(checkout('ls {}'.format(data['folder_ext']), i))
        assert all(res), 'test2 Fail'

    def test_step3(self):
        assert checkout('cd {}; 7z t arx2.7z'.format(data['folder_out']), 'Everything is Ok'), 'test3 Fail'

    def test_step4(self):
        assert checkout('cd {}; 7z u {}/arx2.7z'.format(['folder_in'], data['folder_out']),
                        'Everything is Ok'), 'test4 Fail'

    def test_step5(self, clear_folder, make_files):
        # test5
        res = []
        res.append(checkout("cd {}; 7z a {}/arx2".format(data["folder_in"], data["folder_out"]), "Everything is Ok"))
        for i in make_files:
            res.append(checkout("cd {}; 7z l arx2.7z".format(data["folder_out"], data["folder_ext"]), i))
        assert all(res), "test5 FAIL"

    def test_step6(self,clear_folder, make_files, make_subfolder):
        # test6
        res = []
        res.append(checkout('cd {}; 7z a {}/arx2'.format(data['folder_in'], data['folder_out']),
                            'Everything is Ok'))
        res.append(checkout('cd {}; 7z x arx2.7x -o{} -y'.format(data['folder_out'], data['folder_ext2']),
                            'Everything is Ok'))
        for i in make_files:
            res.append(checkout('ls {}'.format(data['folder_ext2']), i))
            res.append(checkout('ls {}'.format(data['folder_ext2']), make_subfolder[0]))
            res.append(checkout('ls {}/{}'.format(data['folder_ext2'], make_subfolder[0]), make_subfolder[1]))
        assert all(res), 'test6 FAIL'

    def test_step7(self):
        assert checkout('cd {}; 7z d arx2.7z'.format(data['folder_out']), 'Everything is Ok')



1+0 записей получено
1+0 записей отправлено
1048576 байт (1,0 MB, 1,0 MiB) скопирован, 0,00635244 s, 165 MB/s
1+0 записей получено
1+0 записей отправлено
1048576 байт (1,0 MB, 1,0 MiB) скопирован, 0,00676664 s, 155 MB/s
1+0 записей получено
1+0 записей отправлено
1048576 байт (1,0 MB, 1,0 MiB) скопирован, 0,00572775 s, 183 MB/s
1+0 записей получено
1+0 записей отправлено
1048576 байт (1,0 MB, 1,0 MiB) скопирован, 0,0105262 s, 99,6 MB/s
1+0 записей получено
1+0 записей отправлено
1048576 байт (1,0 MB, 1,0 MiB) скопирован, 0,00810547 s, 129 MB/s
1+0 записей получено
1+0 записей отправлено
1048576 байт (1,0 MB, 1,0 MiB) скопирован, 0,00594097 s, 176 MB/s
FAILED                        [ 87%]
ERROR: No more files
arx2.7x



System ERROR:
Неизвестная ошибка -2147024872
ls: невозможно получить доступ к '/home/user/Test7z/folder2/N4JMJ': Нет такого файла или каталога

test_positive.py:54 (TestPositive.test_step6)
self = <test_positive.TestPositive object at 0x7f265e2d8d60>
clear_folder = True, make_files = ['RWRLM', 'TL8GR', 'FBDVD', 'VKABV', '0R6XD']
make_subfolder = ('N4JMJ', 'FVIAR')

    def test_step6(self,clear_folder, make_files, make_subfolder):
        # test6
        res = []
        res.append(checkout('cd {}; 7z a {}/arx2'.format(data['folder_in'], data['folder_out']),
                            'Everything is Ok'))
        res.append(checkout('cd {}; 7z x arx2.7x -o{} -y'.format(data['folder_out'], data['folder_ext2']),
                            'Everything is Ok'))
        for i in make_files:
            res.append(checkout('ls {}'.format(data['folder_ext2']), i))
        res.append(checkout('ls {}'.format(data['folder_ext2']), make_subfolder[0]))
        res.append(checkout('ls {}/{}'.format(data['folder_ext2'], make_subfolder[0]), make_subfolder[1]))
>       assert all(res), 'test6 FAIL'
E       AssertionError: test6 FAIL
E       assert False
E        +  where False = all([True, False, False, False, False, False, ...])

test_positive.py:66: AssertionError