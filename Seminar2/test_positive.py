import subprocess
import pytest

tst = '/home/user/tst'
out = '/home/user/out'
folder1 = '/home/user/folder1'

def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if text in result.stdout and result.returncode == 0:
        return True
    else:
        return False


# обновляет и создает архив, если нет
def test_step1():
    result1 = checkout('cd {}; 7z a {}/arx2'.format(tst, out), 'Everything is Ok')
    result2 = checkout('cd {}; ls'.format(out), 'arx2.7z')
    assert result1 and result2, 'test1 Fail'


@pytest.mark.run_this
def test_step2():
    result1 = checkout('cd {}; 7z e arx2.7z -o{} -y'.format(out, folder1), 'Everything is Ok')
    result2 = checkout('cd {}; ls '.format(folder1), 'qwe')
    result3 = checkout('cd {}; ls '.format(folder1), 'rty')
    assert result1 and result2 and result3, 'test2 Fail'


def test_step3():
    assert checkout('cd {}; 7z t arx2.7z'.format(out), 'Everything is Ok'), 'test3 Fail'


# обновляет архив
def test_step4():
    assert checkout('cd {}; 7z u {}arx2'.format(tst,out), 'Everything is Ok'), 'test4 Fail'


def test_step5():
    assert checkout('cd {}; 7z d arx2.7z'.format(out), 'Everything is Ok'), 'test5 Fail'
