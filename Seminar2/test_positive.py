import subprocess
import pytest
import srting

folder_in = '/home/user/Test7z/tst'
folder_out = '/home/user/Test7z/out'
folder_ext = '/home/user/Test7z/folder1'
folder_ext2 = '/home/user/Test7z/folder2'


@pytest.fixture()
def make_folders():
    # функция для создания директорий, ищем пустую строку просто.
    return checkout('mkdir {} {} {} {}'.format(folder_in, folder_out, folder_ext, folder_ext2), '')


@pytest.fixture()
def clear_folders():
    # функция для очистки  директорий, ищем пустую строку просто.
    return checkout('rm -rf {}/* {}/* {}/* {}/*'.format(folder_in, folder_out, folder_ext, folder_ext2), '')


@pytest.fixture()
def make_files():
    # создаем список
    list_of_file = []
    for i in range(5):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if checkout('cd {}; dd if=/dev/urandom of ={} bs=1M count=1 if flag=fullblock'.format(folder_in, filename), ''):
            list_of_file.append(filename)
    return list_of_file


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not checkout('cd {}; mk dir {}'.format(folder_in, subfoldername), '')
        return None, None
    if not checkout('cd {}; dd if=/dev/urandom of ={} bs=1M count=1 if flag=fullblock'.format(folder_in, subfoldername,
                                                                                              testfilename), ''):
        return subfoldername, None
    else:
        return subfoldername, testfilename



def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if text in result.stdout and result.returncode == 0:
        return True
    else:
        return False


# ДЗ_2. Добавила функцию для сохранения вывода команды(в данном случае хэша)
def hash_func(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    hash_file = result.stdout
    return hash_file


def test_step1(make_folders, clear_folders, make_files):
    result1 = checkout('cd {}; 7z a {}/arx2'.format(folder_in, folder_out), 'Everything is Ok')
    result2 = checkout('cd {}; ls'.format(folder_out), 'arx2.7z')
    assert result1 and result2, 'test1 Fail'


# ДЗ_2. Тест для сравнения полученных хэшей
def test1_hash():
    result1 = hash_func('cd {}; crc32 arx2.7z'.format(folder_out)).upper()
    result2 = hash_func('cd {}; 7z h arx2.7z'.format(folder_out))
    assert result1 in result2, 'test1_hash Fail'


def test_step2(make_files):
    res=[]
    res.append(checkout('cd {}; 7z a {}/arx2'.format(folder_in, folder_out), 'Everything is Ok'))
    res.append(checkout('cd {}; 7z e arx2.7z -o{} -y'.format(folder_out, folder_ext), 'Everything is Ok'))
    for item in make_files:
        res.append(checkout('ls {}'.format(folder_ext), item))
    assert all(res), 'test2 Fail'


# ДЗ_2
def test_step3(clear_folders, make_files, make_subfolder):
    res =[]
    res.append(checkout('cd {}; 7z a {}/arx'.format(folder_in, folder_out), 'Everything is Ok'))
    res.append(checkout('cd {}; 7z x arx.7z -o{} -y'.format(folder_out, folder_ext2), 'Everything is Ok'))
    for item in make_files:
        res.append(checkout('ls {}'.format(folder_ext2)))
    result2 = checkout('cd {}; ls'.format(folder_ext2), 'qwe')
    result3 = checkout('cd {}; ls'.format(folder_ext2), 'rty')
    assert result1 and result2 and result3, 'test3 Fail'


def test_step4():
    assert checkout('cd {}; 7z t arx2.7z'.format(folder_out), 'Everything is Ok'), 'te4 Fail'


def test_step5():
    assert checkout('cd {}; 7z u {}/arx2.7z'.format(folder_in, folder_out), 'Everything is Ok'), 'test5 Fail'


# ДЗ_2
def test_step6(clear_folders, make_files):
    # assert checkout('cd {}; 7z l arx2.7z'.format(out), '2 files'), 'test5 Fail'
    res=[]
    res.append(checkout('cd {}; 7z a {}/arx2'.format(folder_in, folder_out), 'Everything is Ok'))
    for item in make_files:
        res.append(checkout('cd {}; 7z l arx2.7z'.format(folder_out), item))
    assert all(res), 'test6 Fail'


def test_step7():
    assert checkout('cd {}; 7z d arx2.7z'.format(folder_out), 'Everything is Ok'), 'test7 Fail'
