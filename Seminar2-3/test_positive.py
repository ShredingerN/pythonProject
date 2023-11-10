import subprocess
import yaml
from checkers import hash_func
from checkers import checkout

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestPositive:
    def test_step1(self):
        result1 = checkout('cd {}; 7z a {}/arx2'.format(data['folder_in'], data['folder_out']), 'Everything is Ok')
        result2 = checkout('cd {}; ls'.format(data['folder_out']), 'arx2.7z')
        assert result1 and result2, 'test1 Fail'

    # ДЗ. Тест для сравнения полученных хэшей
    def test1_hash(self):
        result1 = hash_func('cd {}; crc32 arx2.7z'.format(data['folder_out'])).upper()
        result2 = hash_func('cd {}; 7z h arx2.7z'.format(data['folder_out']))
        assert result1 in result2, 'test1_hash Fail'

    # def  test1_hash(self, clear_folders, make_files):
    #     # test8
    #     res = []
    #     for i in make_files:
    #         res.append(checkout("cd {}; 7z h {}".format(data["folder_in"], i), "Everything is Ok"))
    #         hash = hash_func("cd {}; crc32 {}".format(data["folder_in"], i)).upper()
    #         res.append(checkout("cd {}; 7z h {}".format(data["folder_in"], i), hash))
    #     assert all(res), " test1_hash"

    def test_step2(self, make_files):
        result1 = checkout('cd {}; 7z e arx2.7z -o{} -y'.format(data['folder_out'], data['folder_ext']),
                           'Everything is Ok')
        result2 = checkout('cd {}; ls'.format(data['folder_ext']), make_files[0])
        assert result1 and result2, 'test2 Fail'

    # def test_step2(self, clear_folders, make_files):
    #     # test2
    #     res = []
    #     res.append(checkout("cd {}; 7z a {}/arx".format(data["folder_in"], data["folder_out"]), "Everything is Ok"))
    #     res.append(
    #         checkout("cd {}; 7z e arx.7z -o{} -y".format(data["folder_out"], data["folder_ext"]), "Everything is Ok"))
    #     for item in make_files:
    #         res.append(checkout("ls {}".format(data["folder_ext"]), item))
    #     assert all(res)

    # ДЗ
    def test_step3(self):
        result1 = checkout('cd {}; 7z x arx2.7z -o{} -y'.format(data['folder_out'], data['folder_ext2']), 'Everything is Ok')
        result2 = checkout('cd {}; ls'.format(data['folder_ext2']), 'qwe')
        result3 = checkout('cd {}; ls'.format(data['folder_ext2']), 'rty')
        assert result1 and result2 and result3, 'test3 Fail'

    # def test_step3(self, clear_folders, make_files, make_subfolder):
    #     res = []
    #     res.append(checkout("cd {}; 7z a {}/arx -t{}".format(data["folder_in"], data["folder_out"], data["type"]), "Everything is Ok"))
    #     res.append(checkout("cd {}; 7z x arx.{} -o{} -y".format(data["folder_out"], data["type"], data["folder_ext2"]), "Everything is Ok"))
    #     for i in make_files:
    #         res.append(checkout("ls {}".format(data["folder_ext2"]), i))
    #     res.append(checkout("ls {}".format(data["folder_ext2"]), make_subfolder[0]))
    #     res.append(checkout("ls {}/{}".format(data["folder_ext2"], make_subfolder[0]), make_subfolder[1]))
    #     assert all(res), "test3 FAIL"

    def test_step4(self):
        assert checkout('cd {}; 7z t arx2.7z'.format(data['folder_out']), 'Everything is Ok'), 'te4 Fail'

    def test_step5(self):
        assert checkout('cd {}; 7z u {}/arx2.7z'.format(['folder_in'], data['folder_out']),
                        'Everything is Ok'), 'test5 Fail'

    # ДЗ
    def test_step6(self):
        result1 = checkout('cd {}; 7z l arx2.7z'.format(data['folder_out']), 'qwe')
        result2 = checkout('cd {}; 7z l arx2.7z'.format(data['folder_out']), 'rty')
        assert result1 and result2, 'test6 Fail'

    # def test_step6(self, clear_folders, make_files):
    #     # test5
    #     res = []
    #     res.append(checkout("cd {}; 7z a {}/arx".format(data["folder_in"], data["folder_out"]), "Everything is Ok"))
    #     for i in make_files:
    #         res.append(checkout("cd {}; 7z l arx.7z".format(data["folder_out"], data["folder_ext"]), i))
    #     assert all(res), "test6 FAIL"


    def test_step7(self):
        assert checkout('cd {}; 7z d arx2.7z'.format(data['folder_out']), 'Everything is Ok'), 'test7 Fail'
