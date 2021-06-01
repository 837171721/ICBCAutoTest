#coding=utf-8
'''
Created on 2018.03.27 @author: FJQ
'''
import re
import operator
import GenCertGroup
from GlobalConfigure import levels, log_level,str_srcPin

from logTest import SysClass, LoggerClass
conf  = LoggerClass(loglevel=levels.get(log_level), logger="TestCases_GetLanguageList.py")
logger=conf.getlogger()
#错误信息列表
no_key_Err='''获取提示语言失败:未知错误。返回码:-102 There is no key!'''
many_key_Err='''获取提示语言失败:未知错误。返回码:-104 There is more than one key!'''
right_Info='''zh_CN||en_US||zh_TW'''

def test_GetLanguageList(ctrlObj,TestingRange,AdminKeyInfo):
    testCtrl=GetLanguageListCases(ctrlObj,AdminKeyInfo)  #建立类对象，打开控件测试页 
    testGetLanguageListGroup(testCtrl,TestingRange)   #测试用例集，根据测试范围定义测试强度
    
def testGetLanguageListGroup(ctrlObj,testRange):
    #测试用例集
    if 0 == testRange:  #详细测试
        #testResult = ctrlObj.negativeCase_nokey()#未插入U盾，点击获取U盾提示语

        testResult = ctrlObj.positiveCase_formatKey()#插入1支格式化U盾，点击获取U盾提示语

        testResult = ctrlObj.positiveCase_oneCert()#插入1支非格式化U盾，点击获取U盾提示语

        #testResult = ctrlObj.negativeCase_manyKey()#插入多只U盾，点击获取U盾提示语

        #testResult = ctrlObj.positiveCase_operation()#插入多只，拔出多余key，留一只，点击获取U盾提示语
        
    elif 1 == testRange: #验证测试
        testResult = ctrlObj.positiveCase()
        
    elif 2 == testRange:
        testResult = ctrlObj.negativeCase_noKey()
          
    elif 3 == testRange:
        testResult = ctrlObj.negativeCase_manyKey()  
             
    elif 4 == testRange:
        testResult = ctrlObj.positiveCase()  
        
class GetLanguageListCases():
    def __init__(self,testCtrl,AdminKeyInfo):
        self.testCtrl=testCtrl   #控件测试页
        self.AdminKeyAlgId=AdminKeyInfo  #保护密钥信息
        self.CertRequest=GenCertGroup.GenCertClass(self.testCtrl,AdminKeyInfo)   #创建证书申请对象

    def positiveCase(self):
        #用例描述：插入1支U盾，点击获取U盾提示语，返回支持的字符集“UTF-8||GBK||GB18030”"
        caseTitle  = "用例——插入1支U盾，点击获取U盾提示语，返回支持的字符集“UTF-8||GBK||GB18030”"
        caseResult = None
        e=None
        testResult=self.testCtrl.get_LanguageList()
        testResult=re.sub(re.compile('\s+'),' ',testResult)
        if right_Info in testResult:
            caseResult="pass"                        
        else:
            caseResult="fail"
            e="实测返回："+"“"+testResult+"”"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult  
        
    def positiveCase_formatKey(self):
        caseTitle  = "用例——插入1支已格式化U盾，点击获取U盾提示语，返回支持的字符集“UTF-8||GBK||GB18030”"
        caseResult = None
        e=None
        initResult=self.CertRequest.init_key(str_srcPin,str_srcPin)
        if  initResult[0]:
            testResult=self.testCtrl.get_LanguageList()
            testResult=re.sub(re.compile('\s+'),' ',testResult)
            if right_Info in testResult:
                caseResult="pass"                        
            else:
                caseResult="fail"
                e="实测返回："+"“"+testResult+"”"
        else:
            caseResult="fail"
            e="初始化操作失败，结束用例执行!"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult    
        
    def positiveCase_oneCert(self):
        caseTitle  = "用例——插入1支非格式化U盾，点击获取U盾提示语，返回支持的字符集“UTF-8||GBK||GB18030”"
        caseResult = None
        e=None

        certResult=self.CertRequest.genCert_with_RSA1024_Sign_P()
        if certResult[1]:
            testResult=self.testCtrl.get_LanguageList()
            testResult=re.sub(re.compile('\s+'),' ',testResult)
            if right_Info in testResult:
                caseResult="pass"                        
            else:
                caseResult="fail"
                e="实测返回："+"“"+testResult+"”"
        else:
            caseResult="fail"
            e="下证失败，结束用例执行!"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult 
     
    def negativeCase_noKey(self):
        #用例描述：未插入U盾，点击获取U盾提示语，获取提示语言失败:未知错误。返回码:-102 There is no key!
        caseTitle  = "用例——未插入U盾，点击获取U盾提示语，获取提示语言失败:未知错误。返回码:-102 There is no key!"
        caseResult = None
        e=None
        testResult=self.testCtrl.get_LanguageList()
        testResult=re.sub(re.compile('\s+'),' ',testResult)
        if operator.eq(testResult,no_key_Err):
            caseResult="pass"                        
        else:
            caseResult="fail"
            e="实测返回："+"“"+testResult+"”"

        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult
            
    def negativeCase_manyKey(self):
        #用例描述：插入多个同款U盾，点击获取U盾提示语,返回获取提示语言失败:未知错误。返回码:-104 There is more than one key!"
        caseTitle  = "用例——插入多个同款U盾，点击获取U盾提示语,返回获取提示语言失败:未知错误。返回码:-104 There is more than one key!"
        caseResult = None
        e=None
        
        testResult=self.testCtrl.get_LanguageList()
        testResult=re.sub(re.compile('\s+'),' ',testResult)
        if operator.eq(testResult,many_key_Err):
            caseResult="pass"                        
        else:
            caseResult="fail"
            e="实测返回："+"“"+testResult+"”"

        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult
        
    def negativeCase_operation(self):
        
        #第四条用例
        caseTitle  = "用例——插入多个同款U盾，拔出多余U盾，只留1支在位，点击获取U盾提示语,返回U盾支持的语言列表"
        caseResult = None
        e=None
        
        testResult=self.testCtrl.get_LanguageList()
        testResult=re.sub(re.compile('\s+'),' ',testResult)
        if right_Info == testResult:
            caseResult="pass"                        
        else:
            caseResult="fail"
            e="实测返回："+"“"+re.sub(re.compile('\s+'),' ',testResult)+"”"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult
        
#########################
#开始测试
#########################
