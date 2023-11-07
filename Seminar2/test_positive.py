import subprocess

tst = '/home/user/Test7z/tst'
out = '/home/user/Test7z/out'
folder1 = '/home/user/Test7z/folder1'
folder2 = '/home/user/Test7z/folder2'


def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if text in result.stdout and result.returncode == 0:
        return True
    else:
        return False


# ДЗ. Добавила функцию для сохранения вывода команды(в данном случае хэша)
def hash_func(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    hash_file = result.stdout
    return hash_file


def test_step1():
    result1 = checkout('cd {}; 7z a {}/arx2'.format(tst, out), 'Everything is Ok')
    result2 = checkout('cd {}; ls'.format(out), 'arx2.7z')
    assert result1 and result2, 'test1 Fail'


# ДЗ. Тест для сравнения полученных хэшей
def test1_hash():
    result1 = hash_func('cd {}; crc32 arx2.7z'.format(out)).upper()
    result2 = hash_func('cd {}; 7z h arx2.7z'.format(out))
    assert result1 in result2, 'test1_hash Fail'


def test_step2():
    result1 = checkout('cd {}; 7z e arx2.7z -o{} -y'.format(out, folder1), 'Everything is Ok')
    result2 = checkout('cd {}; ls'.format(folder1), 'qwe')
    result3 = checkout('cd {}; ls'.format(folder1), 'rty')
    assert result1 and result2 and result3, 'test2 Fail'


# ДЗ
def test_step3():
    result1 = checkout('cd {}; 7z x arx2.7z -o{} -y'.format(out, folder2), 'Everything is Ok')
    result2 = checkout('cd {}; ls'.format(folder2), 'qwe')
    result3 = checkout('cd {}; ls'.format(folder2), 'rty')
    assert result1 and result2 and result3, 'test3 Fail'


def test_step4():
    assert checkout('cd {}; 7z t arx2.7z'.format(out), 'Everything is Ok'), 'te4 Fail'


def test_step5():
    assert checkout('cd {}; 7z u {}/arx2.7z'.format(tst, out), 'Everything is Ok'), 'test5 Fail'


# ДЗ
def test_step6():
    # assert checkout('cd {}; 7z l arx2.7z'.format(out), '2 files'), 'test5 Fail'
    result1 = checkout('cd {}; 7z l arx2.7z'.format(out), 'qwe')
    result2 = checkout('cd {}; 7z l arx2.7z'.format(out), 'rty')
    assert result1 and result2, 'test6 Fail'


def test_step7():
    assert checkout('cd {}; 7z d arx2.7z'.format(out), 'Everything is Ok'), 'test7 Fail'
