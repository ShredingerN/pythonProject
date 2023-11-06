'''
Написать функцию на Python, которой передаются в качестве параметров команда и текст.
Функция должна возвращать True, если команда успешно выполнена и текст найден в её выводе и False в противном случае.
Передаваться должна только одна строка, разбиение вывода использовать не нужно.
'''

import subprocess


def check_text(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if result.returncode == 0 and text in result.stdout:
        return True
    else:
        return False


if __name__ == '__main__':
    print(check_text('ls /home/user', 'Страница справки по GNU'))
    print(check_text('rm --help', 'Страница справки по GNU'))
    print(check_text('cat /etc/os-release', 'Страница'))
