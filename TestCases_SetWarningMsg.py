# coding=utf-8
'''
Created on 2018.03.27 @author: FJQ
Created on 2018.08.16 @author: SYX
Created on 2018.08.18 @author: YS
'''
import re
import random
import string
import operator
import GenCertGroup
from GlobalConfigure import levels,log_level,str_srcPin

from logTest import SysClass, LoggerClass
conf = LoggerClass(loglevel=levels.get(log_level), logger="TestCases_SetWarningMsg.py")
logger = conf.getlogger()

# 错误信息列表
no_key_Err = '''设置提示语言失败:未知错误。返回码:-102 There is no key!'''
many_key_Err = '''设置提示语言失败:未知错误。返回码:-104 There is more than one key!'''
right_Info = '''成功'''


def test_SetWarningMsg(ctrlObj, TestingRange, AdminKeyInfo):
    testCtrl = setWarningMsgCases(ctrlObj, AdminKeyInfo)  # 建立类对象，打开控件测试页
    testSetWarningMsgGroup(testCtrl, TestingRange)  # 测试用例集，根据测试范围定义测试强度


def testSetWarningMsgGroup(ctrlObj, testRange):
    # 测试用例集
    if 0 == testRange:  # 详细测试    
        testResult = ctrlObj.positiveCase_formatKey()  # 插入1支格式化U盾，输入任意参数，点击设置PC屏幕警告语
        
        testResult = ctrlObj.positiveCase_oneCert()  # 插入1支非格式化U盾，输入任意参数，点击设置PC屏幕警告语
        
        testResult = ctrlObj.positiveCase_voidParaChoice()  # 插入1支U盾，不参数，点击设置PC屏幕警告语

    elif 1 == testRange:  # 验证测试
        testResult = ctrlObj.positiveCase()

    elif 2 == testRange:  # 无key测试
        testResult = ctrlObj.negativeCase_noKey_voidParaChoice()
        
        testResult = ctrlObj.negativeCase_noKey_errParaChoice()
        
    elif 3 == testRange:  # 多key测试
        testResult = ctrlObj.negativeCase_manyKey()

    elif 4 == testRange:  # 多key测试
        testResult = ctrlObj.positiveCase()


class setWarningMsgCases():
    def __init__(self, testCtrl, AdminKeyInfo):
        self.testCtrl = testCtrl  # 控件测试页
        self.AdminKeyAlgId = AdminKeyInfo  # 保护密钥信息
        self.CertRequest = GenCertGroup.GenCertClass(self.testCtrl, AdminKeyInfo)  # 创建证书申请对象

    def positiveCase(self):
        caseTitle = "用例——插入1支U盾，设置屏幕警告语为screen warning，返回成功"
        caseResult = None
        e = None
        
        ScreenWarningMsg = 'screen warning'
        testResult = self.testCtrl.set_WarningMsg(ScreenWarningMsg)
        testResult = re.sub(re.compile('\s+'), ' ', testResult)
        if operator.eq(right_Info, testResult):
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
        caseTitle = "用例——未插入U盾，输入任意参数，点击设置PC屏幕警告语。返回码:-102 There is no key!"
        caseResult = None
        e = None

        ScreenMsgLen = random.randint(0,20)
        ScreenMsg=''.join(random.sample(string.ascii_letters + string.digits,ScreenMsgLen)).replace(" ","")

        testResult = self.testCtrl.set_WarningMsg(ScreenMsg)
        testResult = re.sub(re.compile('\s+'), ' ', testResult)
        if operator.eq(no_key_Err, testResult):
            caseResult = "pass"
        else:
            caseResult = "fail"
            e = "实测返回：" + "“" +testResult+ "”"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult

    def negativeCase_noKey_voidParaChoice(self):
        caseTitle = "用例——未插入U盾，不输入参数，点击设置PC屏幕警告语。返回码:-102 There is no key!"
        caseResult = None
        e = None
        ScreenWarningMsg = ''
        testResult = self.testCtrl.set_WarningMsg(ScreenWarningMsg)
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

    def positiveCase_formatKey(self):
        caseTitle = "用例——插入1支格式化，设置屏幕警告语为screen warning，返回成功"
        caseResult = None
        e = None
        initResult=self.CertRequest.init_key(str_srcPin,str_srcPin)
        if initResult[0]:
            ScreenWarningMsg = 'screen warning'
            testResult = self.testCtrl.set_WarningMsg(ScreenWarningMsg)
            testResult=re.sub(re.compile('\s+'),' ',testResult)
            if operator.eq(right_Info, testResult):
                caseResult = "pass"
            else:
                caseResult = "fail"
                e = "实测返回：" + "“" + testResult + "”"
        else:
            caseResult="fail"
            e = "初始化失败,结束用例执行"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult

    def positiveCase_oneCert(self):
        caseTitle = "用例——插入1支非格式化，设置屏幕警告语为screen warning，返回成功"
        caseResult = None
        e = None
        certResult=self.CertRequest.genCert_with_RSA1024_Mix()
        if certResult[1]:            
            ScreenWarningMsg = 'screen warning'
            testResult = self.testCtrl.set_WarningMsg(ScreenWarningMsg)
            testResult=re.sub(re.compile('\s+'),' ',testResult)
            if operator.eq(right_Info, testResult):
                caseResult = "pass"
            else:
                caseResult = "fail"
                e = "实测返回：" + "“" + testResult + "”"
        else:
            caseResult="fail"
            e = "下证下载失败，结束用例执行"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult

    def positiveCase_voidParaChoice(self):
        caseTitle = "用例——插入1支K，设置屏幕警告语为空，返回成功"
        caseResult = None
        e = None
        testResult = self.testCtrl.set_WarningMsg('')
        testResult=re.sub(re.compile('\s+'),' ',testResult)
        if operator.eq(right_Info, testResult):
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
        caseTitle = "用例——插入多个同款U盾，设置屏幕警告语，返回“设置提示语言失败:未知错误。返回码:-104 There is more than one key!"
        caseResult = None
        e = None
        ScreenWarningMsg = 'screen warning'
        testResult = self.testCtrl.set_WarningMsg(ScreenWarningMsg)
        testResult = re.sub(re.compile('\s+'), ' ', testResult)
        if operator.eq(many_key_Err, testResult):
            caseResult = "pass"
        else:
            caseResult = "fail"
            e = "实测返回：" + "“" + testResult + "”"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult

    def positiveCase_operation(self):
        #第四条用例
        caseTitle  = "用例——插入多个同款U盾，拔出多余U盾，只留1支在位，设置屏幕警告语，返回成功提示"
        caseResult = None
        e=None
        #if 0 == GlobalConfigure.TestingType:
            #win32api.MessageBox(0, "请确认未接入任何设备", "提示框",win32con.MB_OK)
        
        ScreenWarningMsg='screen warning'
        testResult=self.testCtrl.set_WarningMsg(ScreenWarningMsg)
        #testResult=re.sub(re.compile('\s+'),' ',testResult)
        if right_Info == testResult:
            caseResult="pass"
        else:
            caseResult="fail"
            e="实测返回："+"“"+testResult+"”"
        if e==None:
            logger.critical("%s || %s ",caseTitle,caseResult)
        else:
            logger.critical("%s || %s || %s ",caseTitle,caseResult,e)
        return caseResult

