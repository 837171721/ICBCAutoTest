#coding=utf-8
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
from HTMLTestRunner import HTMLTestRunner

install_path_64 = r'E:\工行\测试对象\PC\驱动\V2.5.0.11\ICBC_MW&WDC_UShield2_Install.exe'


class TestCaseInstall(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.test = IcbcManagementTools()
        self.logtest = loggerClass(
            logger_name='TestCaseInstall.py', logger_level='INFO')
        self.logger = self.logtest.getlogger()

    def test_install(self):
        '''安装管理工具'''
        result = self.test.install(install_path_64)
        self.logger.info('测试用例：安装管理工具 || ' + str(result))
        assert result == True, '安装失败'

    @classmethod
    def tearDownClass(self):
        self.test.install()


if __name__ == '__main__':
    test = unittest.TestSuite()
    test.addTest(TestCaseInstall('test_install'))

    now = time.strftime('%Y-%m-%d %H_%M_%S')
    filename = 'result.html'
    file_result = open(filename, 'wb')
    runner = HTMLTestRunner(
        stream=file_result, title=u'测试报告', description=u'测试情况')
    runner.run(test)
    file_result.close()
    # test = TestCaseInstall()
    # test.test_install()
