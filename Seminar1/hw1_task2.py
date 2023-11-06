'''
Доработать функцию из предыдущего задания таким образом, чтобы у неё появился дополнительный режим работы,
в котором вывод разбивается на слова с удалением всех знаков пунктуации (их можно взять из списка string.punctuation
модуля string). В этом режиме должно проверяться наличие слова в выводе
'''

import subprocess
import string


def check_text(cmd, words):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    temp = result.stdout
    for p in string.punctuation:
        if p in temp:
            temp = temp.replace(p, ' ')
    if result.returncode == 0:
        if words in temp:
            return True
        else:
            return False
    return f'wrong command{cmd}'


if __name__ == '__main__':
    print(check_text('ls /home/user', 'snap'))
    print(check_text('rm --help', 'fooo'))
    print(check_text('cat /etc/os-release', 'LIKE'))
