# coding=utf-8
'''
Created on 2021.6.1

@author: wsk

'''
from os import name
import unittest
import time
from unittest import result
from unittest import runner
from logger import *
from icbc_management_tools import *
from win_operaton import *
from HTMLTestRunner import HTMLTestRunner
from Configuration import *

install_path_64 = 'E:\SVN-自动化脚本\ICBC\Import\驱动安装包\V2.5.0.11\ICBC_MW&WDC_UShield2_Install.exe'


class TestCaseInstall(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.test = IcbcManagementTools()
        self.logtest = loggerClass(
            logger_name='TestCaseInstall.py', logger_level='INFO')
        self.logger = self.logtest.getlogger()

    def test_install(self):
        '''安装管理工具'''
        result = self.test.install(INSTALL_PATH)
        self.logger.info('测试用例：安装管理工具 || ' + str(result))
        assert result == True, '安装失败'

    def test_install_same(self):
        '''安装相同版本管理工具'''
        result = self.test.install(INSTALL_PATH)
        if result == '同版本覆盖安装':
            result = True
        self.logger.info('测试用例：安装相同版本管理工具 || ' + str(result))
        assert result == True, '安装失败'

    def test_install_old(self):
        '''安装低版本管理工具'''
        result = self.test.install(INSTALL_PATH_OLD)
        self.logger.info('测试用例：安装相同版本管理工具 || ' + str(result))
        assert result == '低版本无法覆盖高版本', '安装失败'

    def test_install_start_menu(self):
        '''查看开始菜单文件'''
        file_list = es_win_get_filelist(START_PATH)
        result = 'False'
        if file_list.sort() == START_FILE.sort():
            result = 'True'
        self.logger.info('测试用例：查看开始菜单文件 || ' + result +
                         '——实际输出：' + str(file_list))
        assert result == 'True', '开始菜单显示异常'

    def test_install_desktop_lnk(self):
        '''查看桌面是否生成快捷方式'''
        result = es_win_file_exits(DESKTOP_PATH, DESKTOP_FILE)
        self.logger.info('测试用例：安装完成后是否生成桌面快捷方式 || ' + str(result))
        assert result == True, '未找到快捷方式'

    def test_install_path(self):
        '''查看安装目录下文件列表是否正确'''
        install_list = es_win_get_filelist(FILE_PATH)
        result = False
        if install_list.sort() == FILE_LIST.sort():
            result = True
        self.logger.info('测试用例：安装完成查看安装目录内容是否完成 || ' +
                         str(result) + '——实际输出' + str(install_list))
        assert result == True

    def test_install_dll(self):
        '''查看dll文件是否存在'''
        result = es_win_file_exits(DLL_PATH, DLL_FILE)
        self.logger.info('测试用例：安装完成后是否释放dll文件 || ' + str(result))
        assert result == True, '文件不符'

    def test_uninstall(self):
        '''卸载管理工具'''
        result = self.test.uninstall(UNINSTALL_PATH)
        self.logger.info('测试用例：卸载管理工具 || ' + str(result))
        assert result == True, '卸载失败'

    def test_uninstall_path(self):
        '''卸载管理工具后查看安装目录下的文件是否被清除'''
        self.test.uninstall(UNINSTALL_PATH)
        result = es_win_file_notexits(UNINSTALL_FILE_PATH, UNINSTALL_FILE)
        self.logger.info('测试用例：卸载完成后安装目录内容下的文件是否被清除 || ' + str(result))
        assert result == True

    def test_uninstall_dll(self):
        '''卸载管理工具后查看dll文件是否被清除'''
        self.test.uninstall(UNINSTALL_PATH)
        result = es_win_file_notexits(UNINSTALL_FILE_PATH, UNINSTALL_FILE)
        self.logger.info('测试用例：卸载完成后安装目录内容下的文件是否被清除 || ' +
                         str(result))
        assert result == True

    def test_uninstall_desk_lnk(self):
        '''卸载完成后，查看桌面快捷方式是否清除'''
        self.test.uninstall(UNINSTALL_PATH)
        result = es_win_file_notexits(DESKTOP_PATH, DESKTOP_FILE)
        self.logger.info('测试用例：卸载完成后是否生成桌面快捷方式 || ' + str(result))
        assert result == True, '快捷方式未删除'

    def test_uninstall_start_menu(self):
        '''卸载管理工具后，查看开始菜单文件是否被删除'''
        self.test.uninstall(UNINSTALL_PATH)
        result = es_win_file_notexits(UNINSTALL_START_PATH, UNINSTALL_FILE)
        self.logger.info('测试用例：卸载完成后是否删除开始菜单文件 || ' + str(result))
        assert result == True, '开始菜单文件未删除'

    @classmethod
    def tearDownClass(self):
        self.test.install(INSTALL_PATH)


if __name__ == '__main__':
    # if os.path.exists(OPEN_PATH):
    #     prepare = IcbcManagementTools()
    #     prepare.uninstall(UNINSTALL_PATH)
    test = unittest.TestSuite()
    test.addTest(TestCaseInstall('test_install'))
    # test.addTest(TestCaseInstall('test_install_same'))
    # test.addTest(TestCaseInstall('test_install_old'))
    # test.addTest(TestCaseInstall('test_install_start_menu'))
    # test.addTest(TestCaseInstall('test_install_desktop_lnk'))
    test.addTest(TestCaseInstall('test_install_path'))
    # test.addTest(TestCaseInstall('test_install_dll'))
    # test.addTest(TestCaseInstall('test_uninstall'))
    # test.addTest(TestCaseInstall('test_uninstall_path'))
    # test.addTest(TestCaseInstall('test_uninstall_dll'))
    # test.addTest(TestCaseInstall('test_uninstall_desk_lnk'))
    # test.addTest(TestCaseInstall('test_uninstall_start_menu'))


    now = time.strftime('%Y-%m-%d %H_%M_%S')
    filename = HTMLREPORT_PATH + now + 'result.html'
    file_result = open(filename, 'wb')
    runner = HTMLTestRunner(
        stream=file_result, title=u'测试报告', description=u'测试情况')
    runner.run(test)
    file_result.close()
