# coding=utf-8
'''
Created on 2018.03.27 @author: FJQ
Created on 2018.08.18 @author: YS
'''
import re  # 引入正在表达式
import random
import GenCertGroup
import operator
from GlobalConfigure import levels,log_level,str_srcPin,languageType
from logTest import SysClass, LoggerClass
conf = LoggerClass(loglevel=levels.get(log_level), logger="TestCases_SetLanguageList.py")
logger = conf.getlogger()

# 错误信息列表
no_key_Err = '''设置提示语言失败:未知错误。返回码:-102 There is no key!'''
param_Err = '''设置提示语言失败:未知错误。返回码:-304 Failed Param!'''
many_key_Err = '''设置提示语言失败:未知错误。返回码:-104 There is more than one key!'''
right_Info = '''成功'''


def test_SetLanguageList(ctrlObj, TestingRange, AdminKeyInfo):
    testCtrl = SetLanguageListCases(ctrlObj, AdminKeyInfo)  # 建立类对象，打开控件测试页
    testSetLanguageListGroup(testCtrl, TestingRange)  # 测试用例集，根据测试范围定义测试强度


def testSetLanguageListGroup(ctrlObj, testRange):
    # 测试用例集
    if 0 == testRange:  # 详细测试
        testResult = ctrlObj.nagativeCase_errParaChoice()  # 插入1支U盾，输入任意参数，点击设置U盾提示语
        
        testResult = ctrlObj.positiveCase_formatKey()  # 插入1支格式化U盾，输入zh_CN，点击设置U盾提示语
        
        testResult = ctrlObj.positiveCase_oneCert()  # 插入1支非格式化U盾，输入zh_CN，点击设置U盾提示语
        
    elif 1 == testRange:  # 验证测试
        testResult = ctrlObj.positiveCase()

    elif 2 == testRange:  # 无key测试
        testResult = ctrlObj.negativeCase_noKey_voidParaChoice()  # 未插入U盾，不输入参数，点击设置U盾提示语

        testResult = ctrlObj.negativeCase_noKey_errParaChoice()  # 未插入U盾，输入任意参数，点击设置U盾提示语

        testResult = ctrlObj.negativeCase_noKey()  # 未插入U盾，输入zh_CN，点击设置U盾提示语

    elif 3 == testRange:  # 多key测试
        testResult = ctrlObj.negativeCase_manyKey()

    elif 4 == testRange:  # 多key测试
        testResult = ctrlObj.positiveCase()

class SetLanguageListCases():
    def __init__(self, testCtrl, AdminKeyInfo):
        self.testCtrl = testCtrl  # 控件测试页
        self.AdminKeyAlgId = AdminKeyInfo  # 保护密钥信息
        self.CertRequest = GenCertGroup.GenCertClass(self.testCtrl, AdminKeyInfo)  # 创建证书申请对象
        if languageType == 0:
            self.sysLang =  'zh_CN'  # 系统语言
        elif languageType == 1:
            self.sysLang =  'zh_TW'  # 系统语言
        elif languageType == 2:
            self.sysLang =  'en_US'  # 系统语言

    def positiveCase(self):
        # 第一条用例
        caseTitle = "用例——插入1只U盾，遍历正确参数，点击设置U盾提示语，提示设置成功，为方便后续测试，最终会将U盾提示语设恢复为系统语言"
        caseResult = None
        e = None
        LangLists = ['zh_CN','en_US', 'zh_TW' ,self.sysLang]
        #LangLists = ['zh_CN']
        logger.critical("beginning... || %s ",caseTitle)
        for langtype in LangLists:
            setLangResult = self.testCtrl.set_LanguageList(langtype)
            textAreaResultSetLanguageList = self.testCtrl.browser.find_element_by_id("ResultSetLanguageList")
            setLangResult=textAreaResultSetLanguageList.get_attribute('value')
            setLangResult = re.sub(re.compile('\s+'), ' ', setLangResult)
            if operator.eq(right_Info, setLangResult):
                caseResult = "pass"
                logger.critical("%s || %s ", caseResult, langtype)
            else:
                caseResult = "fail"
                logger.critical("%s || %s || %s", caseResult, langtype, setLangResult)

        logger.critical("end. || %s ", caseTitle)
        return caseResult

    def negativeCase_noKey_voidParaChoice(self):
        # 第二条用例
        caseTitle = "用例——未插入U盾，不输入参数，点击设置U盾提示语，设置提示语言失败:未知错误。返回码:-304 Failed Param!”错误提示"
        caseResult = None
        e = None

        langtype = ''
        testResult = self.testCtrl.set_LanguageList(langtype)
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

    def negativeCase_noKey_errParaChoice(self):
        caseTitle = "用例——未插入U盾，输入任意参数，点击设置U盾提示语，设置提示语言失败:未知错误。返回码:-102 There is no key!”错误提示"
        caseResult = None
        e = None

        langtype = random.choice(['1234', 'ABC', 'A1$'])
        testResult = self.testCtrl.set_LanguageList(langtype)
        testResult = re.sub(re.compile('\s+'), ' ', testResult)
        if operator.eq(no_key_Err, testResult):
            caseResult = "pass"
        else:
            caseResult = "fail"
            e = "实测返回：" + "“" + testResult + "”"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult

    def negativeCase_noKey(self):
        caseTitle = "用例——未插入U盾，输入en_US/zh_TW/zh_CN，点击设置U盾提示语，设置提示语言失败:未知错误。返回码:-102 There is no key!”错误提示"
        caseResult = None
        e = None

        LangLists = ['en_US', 'zh_TW', 'zh_CN']
        logger.critical("beginning... || %s ",caseTitle)
        for langtype in LangLists:
            setLangResult = self.testCtrl.set_LanguageList(langtype)
            setLangResult = re.sub(re.compile('\s+'), ' ', setLangResult)
            if operator.eq(no_key_Err, setLangResult):
                caseResult = "pass"
                logger.critical("%s || %s ", caseResult, langtype)
            else:
                caseResult = "fail"
                logger.critical("%s || %s || %s", caseResult, langtype, setLangResult)

        logger.critical("end. || %s ", caseTitle)
        return caseResult

    def nagativeCase_errParaChoice(self):
        # 第三条用例
        caseTitle = "用例——插入1支U盾，输入任意字符到提示语参数栏，点击设置U盾提示语，设置提示语言失败:未知错误。返回码:-304 Failed Param!"
        caseResult = None
        e = None
        langtype = random.choice(['1234', 'ICBC', 'A1$'])
        testResult = self.testCtrl.set_LanguageList(langtype)
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

        logger.critical("end. || %s ", caseTitle)
        return caseResult

    def positiveCase_formatKey(self):
        # 第五条用例
        caseTitle = "用例——插入1支已格式化U盾，输入en_US/zh_TW/zh_CN，点击设置U盾提示语，设置成功"
        caseResult = None
        e = None

        LangLists = ['en_US', 'zh_TW', 'zh_CN',self.sysLang]
        logger.critical("beginning... || %s ",caseTitle)
        
        initResult = self.CertRequest.init_key(str_srcPin, str_srcPin)
        if initResult[0]:
            for langtype in LangLists:
                setLangResult = self.testCtrl.set_LanguageList(langtype)
                setLangResult = re.sub(re.compile('\s+'), ' ', setLangResult)
                if operator.eq(right_Info, setLangResult):
                    caseResult = "pass"
                    logger.critical("%s || %s ", caseResult, langtype)
                else:
                    caseResult = "fail"
                    logger.critical("%s || %s || %s", caseResult, langtype, setLangResult)
        else:
            caseResult = "fail"
            e = "初始化失败,结束用例执行"
            logger.critical("%s || %s ", caseResult,e)

        logger.critical("end. || %s ", caseTitle)
        return caseResult

    def positiveCase_oneCert(self):
        # 第五条用例
        caseTitle = "用例——插入1支非格式化U盾，输入en_US/zh_TW/zh_CN，点击设置U盾提示语，设置成功"
        caseResult = None
        e = None

        LangLists = ['en_US', 'zh_TW', 'zh_CN',self.sysLang]

        logger.critical("beginning... || %s ",caseTitle)
        certResult = self.CertRequest.genCert_with_RSA1024_Mix()
        if certResult[0]:
            for langtype in LangLists:
                setLangResult = self.testCtrl.set_LanguageList(langtype)
                setLangResult = re.sub(re.compile('\s+'), ' ', setLangResult)
                if operator.eq(right_Info, setLangResult):
                    caseResult = "pass"
                    logger.critical("%s || %s ", caseResult, langtype)
                else:
                    caseResult = "fail"
                    logger.critical("%s || %s || %s", caseResult, langtype, setLangResult)
        else:
            caseResult = "fail"
            e = "证书下载失败,结束用例执行"
            logger.critical("%s || %s ", caseResult,e)

        logger.critical("end. || %s ", caseTitle)
        return caseResult

    def negativeCase_manyKey(self):
        # 第六条用例
        caseTitle = "用例——插入多只U盾，输入en_US/zh_TW/zh_CN，点击设置U盾提示语,设置提示语言失败:未知错误。返回码:-104 There is more than one key!"
        caseResult = None
        e = None
        LangLists = ['en_US', 'zh_TW', 'zh_CN']

        logger.critical("beginning... || %s ",caseTitle)
        for langtype in LangLists:
            setLangResult = self.testCtrl.set_LanguageList(langtype)
            setLangResult = re.sub(re.compile('\s+'), ' ', setLangResult)
            if operator.eq(many_key_Err, setLangResult):
                caseResult = "pass"
                logger.critical("%s || %s ", caseResult, langtype)
            else:
                caseResult = "fail"
                logger.critical("%s || %s || %s", caseResult, langtype, setLangResult)

        logger.critical("end. || %s ", caseTitle)
        return caseResult
