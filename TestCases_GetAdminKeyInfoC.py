#coding=utf-8
'''
Created on 2018.07.06 @author: SYX
'''

import re         #引入正在表达式
import operator
import GenCertGroup
from  GlobalConfigure import levels,log_level,str_srcPin

from logTest import SysClass, LoggerClass
conf  = LoggerClass(loglevel=levels.get(log_level), logger="TestCases_GetAdminKeyInfoC.py")
logger=conf.getlogger()

#错误信息列表
no_key_Err=  "获取保护密钥信息失败:未知错误。返回码:-102 There is no key!"
many_key_Err="获取保护密钥信息失败:未知错误。返回码:-104 There is more than one key!"

def test_GetAdminKeyInfo(ctrlObj,TestingRange,AdminKeyInfo):
    testCtrl=GetAdminKeyInfoCases(ctrlObj,AdminKeyInfo)  #建立类对象，打开控件测试页 
    testGetAdminKeyInfoGroup(testCtrl,TestingRange)   #测试用例集，根据测试范围定义测试强度
    
def testGetAdminKeyInfoGroup(AdminKeyInfoCtrl,testRange):
    #测试用例集
    if 0 == testRange:  #详细测试
        testResult = AdminKeyInfoCtrl.positiveCase()

        #testResult = AdminKeyInfoCtrl.nagativeCase_noKey()

        #testResult = AdminKeyInfoCtrl.nagativeCase_manyKey()
    
        #testResult =AdminKeyInfoCtrl.nagativeCase_operation()

    elif 1 == testRange: #验证测试W
        testResult = AdminKeyInfoCtrl.positiveCase()

    elif 2 == testRange: #无key测试
        testResult = AdminKeyInfoCtrl.negativeCase_noKey()
        
    elif 3 == testRange: #多key测试
        testResult = AdminKeyInfoCtrl.negativeCase_manyKey()
        
    elif 4 == testRange: #多key测试
        testResult = AdminKeyInfoCtrl.positiveCase_formatKey()
       
class GetAdminKeyInfoCases():
    def __init__(self,testCtrl,AdminKeyInfo):
        self.testCtrl=testCtrl   #控件测试页
        self.AdminKeyAlgId=AdminKeyInfo  #保护密钥信息
        self.CertRequest=GenCertGroup.GenCertClass(self.testCtrl,AdminKeyInfo)   #创建证书申请对象
     
    def positiveCase(self):
        #用例描述：插入1支U盾，点击获取保护密钥信息，期望返回U盾的保护密钥信息
        caseTitle  = "用例——插入1支U盾，点击获取保护密钥信息，期望返回U盾的保护密钥信息（非国密盾返回空，国密旧体系返回2字节，国密新体系返回完整信息）"
        caseResult = None
        e=None

        testResult = self.testCtrl.get_AdminKeyInfoC()
        if None != testResult and '' != testResult:
            if testResult[2:4] == self.AdminKeyAlgId[1]:
                caseResult = "pass"
            else:
                caseResult = "fail"
        elif None == testResult or '' == testResult:
            if not self.AdminKeyAlgId[0]:
                caseResult = "pass"
            else:
                caseResult = "fail"
        else:
            caseResult = "fail"
            e = "实测返回：" + "“" + testResult + "”"

        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult

    def positiveCase_formatKey(self):
        #用例描述：插入1支U盾，点击获取保护密钥信息，期望返回U盾的保护密钥信息
        caseTitle  = "用例——插入1支U盾，点击获取保护密钥信息，期望返回U盾的保护密钥信息（非国密盾返回空，国密旧体系返回2字节，国密新体系返回完整信息）"
        caseResult = None
        e=None
        initResult=self.CertRequest.init_key(str_srcPin,str_srcPin)
        if initResult[0]:
            testResult = self.testCtrl.get_AdminKeyInfoC()
            if None != testResult and '' != testResult:
                if testResult[2:4] == self.AdminKeyAlgId[1]:
                    caseResult = "pass"
                else:
                    caseResult = "fail"
            elif None == testResult or '' == testResult:
                if not self.AdminKeyAlgId[0]:
                    caseResult = "pass"
                else:
                    caseResult = "fail"
            else:
                caseResult = "fail"
                e = "实测返回：" + "“" + testResult + "”"
        else:
            caseResult = "fail"
            e = "初始化失败，结束用例执行"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult

    def negativeCase_noKey(self):
        #用例描述：未插入U盾，点击获取保护密钥信息，期望返回获取介质号失败:未知错误。返回码:-102 There is no key!
        caseTitle  = "用例——未插入U盾，点击获取保护密钥信息，期望返回获取介质号失败:未知错误。返回码:-102 There is no key!"
        caseResult = None
        e=None
  
        testResult=self.testCtrl.get_AdminKeyInfoC()
        testResult=re.sub(re.compile('\s+'),' ',testResult)
        if  operator.eq(no_key_Err,testResult):
            caseResult="pass"
        else:
            caseResult="fail"
            if testResult == None:
                testResult="None"
            e="实测返回："+"“"+testResult+"”"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult               
    
    def negativeCase_manyKey(self):
        #用例描述：插入多支同款U盾，点击获取保护密钥信息，期望返回获取介质号失败:未知错误。返回码:-104 There is more than one key!!
        caseTitle="用例——插入多支同款U盾，点击获取保护密钥信息，期望返回获取介质号失败:未知错误。返回码:-104 There is more than one key"
        caseResult = None
        e=None  
        testResult=self.testCtrl.get_AdminKeyInfoC()
        testResult=re.sub(re.compile('\s+'),' ',testResult)
        if True == operator.eq(many_key_Err,testResult):
            caseResult="pass"                        
        else:
            caseResult="fail"
            if testResult == None:
                testResult="None"
            e="实测返回："+"“"+testResult+"”"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult    

#########################
#开始测试
#########################
