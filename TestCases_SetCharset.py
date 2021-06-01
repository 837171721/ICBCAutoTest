# coding=utf-8
'''
Created on 2018.03.27 @author: FJQ
Created on 2018.08.18 @author: YS
'''
import re  # 引入正在表达式
import GenCertGroup
import operator
from GlobalConfigure import levels,log_level,str_srcPin
from logTest import SysClass, LoggerClass
conf = LoggerClass(loglevel=levels.get(log_level), logger="TestCases_SetCharset.py")
logger = conf.getlogger()

# 错误信息列表
no_key_Err = '''设置字符集失败:未知错误。返回码:-102 There is no key!'''
param_Err = '''设置字符集失败:未知错误。返回码:-304 Failed Param!'''
many_key_Err = '''设置字符集失败:未知错误。返回码:-104 There is more than one key!'''
right_Info = "成功"


def test_SetCharset(ctrlObj, TestingRange, AdminKeyInfo):
    testCtrl = SetCharsetCases(ctrlObj, AdminKeyInfo)  # 建立类对象，打开控件测试页
    testSetCharsetGroup(testCtrl, TestingRange)  # 测试用例集，根据测试范围定义测试强度

def testSetCharsetGroup(ctrlObj, testRange):
    # 测试用例集
    if 0 == testRange:  # 详细测试
        testResult = ctrlObj.positiveCase_formatKey()  # 插入1支格式化U盾，字符集输入UTF-8

        testResult = ctrlObj.positiveCase_oneCert()  # 插入1支非格式化U盾，字符集输入UTF-8

        testResult = ctrlObj.nagativeCase_errParaChoice()  # 插入1支非格式化U盾，字符集输入test

    elif 1 == testRange:  # 验证测试
        testResult = ctrlObj.positiveCase()

    elif 2 == testRange:  # 无key测试
        testResult = ctrlObj.negativeCase_noKey()

    elif 3 == testRange:  # 多key测试
        testResult = ctrlObj.negativeCase_manyKey()  # 插入多只U盾，字符集输入UTF-8

    elif 4 == testRange:  # 多key测试
        testResult = ctrlObj.positiveCase()


class SetCharsetCases():
    def __init__(self, testCtrl, AdminKeyInfo):
        self.testCtrl = testCtrl  # 控件测试页
        self.AdminKeyAlgId = AdminKeyInfo  # 保护密钥信息
        self.CertRequest = GenCertGroup.GenCertClass(self.testCtrl, AdminKeyInfo)  # 创建证书申请对象

    def positiveCase(self):
        caseTitle = "用例——插入1支U盾，遍历正确的参数，点击设置字符集，期望返回成功"
        caseResult = None
        e = None
        charSetLists = ['UTF-8', 'GBK', 'GB18030']
        logger.critical("beginning... || %s ",caseTitle)
        for charSet in charSetLists:
            charSetResult = self.testCtrl.SetCharset(charSet)
            charSetResult = re.sub(re.compile('\s+'), ' ', charSetResult)
            if operator.eq(right_Info, charSetResult):
                caseResult = "pass"
                logger.critical("%s || %s ", caseResult, charSet)
            else:
                caseResult = "fail"
                logger.critical("%s || %s || %s", caseResult, charSet, charSetResult)
        logger.critical("end. || %s ", caseTitle)
        return caseResult

    def negativeCase_noKey(self):
        # 第一条用例
        caseTitle = "用例——未插入U盾，不输入字符集参数，点击设置即将签名的明文字符集,返回设置字符集失败:未知错误。返回码:-304 Failed Param!"
        caseResult = None
        e = None
        charSet = ''
        testResult = self.testCtrl.SetCharset(charSet)
        testResult = re.sub(re.compile('\s+'), ' ', testResult)
        if operator.eq(param_Err, testResult):
            caseResult = "pass"
        else:
            caseResult = "fail"
            e = "实测返回：" + "“" + testResult + "”"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult

    def positiveCase_formatKey(self):
        caseTitle = "用例——插入1支已格式化的U盾，字符集参数输入UTF-8/GBK/GB18030，点击设置即将签名的明文字符集，返回成功"
        caseResult = None
        e = None
        charSetLists = ['UTF-8', 'GBK', 'GB18030']

        logger.critical("beginning... || %s ", caseTitle)
        initResult=self.CertRequest.init_key(str_srcPin,str_srcPin)
        if initResult[0]:
            for charSet in charSetLists:
                charSetResult = self.testCtrl.SetCharset(charSet)
                charSetResult = re.sub(re.compile('\s+'), ' ', charSetResult)
                if operator.eq(right_Info, charSetResult):
                    caseResult = "pass"
                    logger.critical("%s || %s ", caseResult, charSet)
                else:
                    caseResult = "fail"
                    logger.critical("%s || %s || %s", caseResult, charSet, charSetResult)
        else:
            caseResult = "fail"
            e = "初始化失败,结束用例执行"
            logger.critical("%s || %s ", caseResult,e)

        logger.critical("end. || %s ", caseTitle)
        return caseResult

    def positiveCase_oneCert(self):
        caseTitle = "用例——插入1支非格式化的U盾，字符集参数输入UTF-8/GBK/GB18030，点击设置即将签名的明文字符集，返回成功"
        caseResult = None
        e = None
        charSetLists = ['UTF-8', 'GBK', 'GB18030']

        logger.critical("beginning... || %s ", caseTitle)
        certResult=self.CertRequest.genCert_with_RSA1024_Mix()
        if certResult[0]:
            for charSet in charSetLists:
                charSetResult = self.testCtrl.SetCharset(charSet)
                charSetResult = re.sub(re.compile('\s+'), ' ', charSetResult)
                if operator.eq(right_Info, charSetResult):
                    caseResult = "pass"
                    logger.critical("%s || %s ", caseResult, charSet)
                else:
                    caseResult = "fail"
                    logger.critical("%s || %s || %s", caseResult, charSet, charSetResult)
        else:
            caseResult = "fail"
            e = "证书下载失败，结束用例执行"
            logger.critical("%s || %s ", caseResult,e)

        logger.critical("end. || %s ", caseTitle)
        return caseResult

    def nagativeCase_errParaChoice(self):
        # 第五条用例
        caseTitle = "用例——插入1支U盾，字符集参数输入test，点击设置即将签名的明文字符集，返回设置字符集失败:未知错误。返回码:-304 Failed Param!"
        caseResult = None
        e = None
        charSet = 'test'
        testResult = self.testCtrl.SetCharset(charSet)
        testResult = re.sub(re.compile('\s+'), ' ', testResult)
        if operator.eq(param_Err, testResult):
            caseResult = "pass"
        else:
            caseResult = "fail"
            e = "实测返回：" + "“" + testResult + "”"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult

    def negativeCase_manyKey(self):
        caseTitle = "用例——插入多只U盾，字符集参数输入UTF-8/GBK/GB18030，点击设置即将签名的明文字符集，返回失败-104"
        caseResult = None
        e = None
        charSetLists = ['UTF-8', 'GBK', 'GB18030']
        logger.critical("beginning... || %s ", caseTitle)
        for charSet in charSetLists:
            charSetResult = self.testCtrl.SetCharset(charSet)
            charSetResult = re.sub(re.compile('\s+'), ' ', charSetResult)
            if operator.eq(many_key_Err, charSetResult):
                caseResult = "pass"
                logger.critical("%s || %s ", caseResult, charSet)
            else:
                caseResult = "fail"
                logger.critical("%s || %s || %s", caseResult, charSet, charSetResult)

        logger.critical("end. || %s ", caseTitle)
        return caseResult
    