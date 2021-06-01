#coding=utf-8
'''
Created on 2018.08.01
@author: FJQ
'''

import re         #引入正在表达式
import operator
import GenCertGroup 
from logTest import SysClass, LoggerClass
from GlobalConfigure import levels,log_level
from GlobalConfigure import CertListInfoMap
#from TestLog import LogConfig
conf  = LoggerClass(loglevel=levels.get(log_level), logger="TestCases_GetBase64Random.py")
logger=conf.getlogger()

#错误信息列表
no_key_Err="随机数获取失败:未知错误。返回码:-102 There is no key!"
many_key_Err="随机数获取失败:未知错误。返回码:-104 There is more than one key!"

def test_GetBase64Random(ctrlObj,TestingRange,AdminKeyInfo):
    testCtrl=GetBase64RandomCases(ctrlObj,AdminKeyInfo)  #建立类对象，打开控件测试页 
    testGetBase64RandomCase(testCtrl,TestingRange)   #测试用例集，根据测试范围定义测试强度
    
def testGetBase64RandomCase(ctrlObj,testRange):
    #测试用例集
    if 0 == testRange:  #详细测试
        testResult = ctrlObj.positiveCase()

        testResult = ctrlObj.negativeCase_noKey()#1、未插入U盾，点击获取随机数

        testResult = ctrlObj.negativeCase_manyKeyVerify()#3、插入多只key
        
        #testResult = ctrlObj.positiveCase_operation()#7、插入多支同款U盾，拔出多余U盾，只留1支在位

    elif 1 == testRange: #验证测试
        testResult = ctrlObj.positiveCase()

    elif 2 == testRange: #无key测试
        testResult = ctrlObj.negativeCase_noKey()
        
    elif 3 == testRange: #多key测试
        testResult = ctrlObj.negativeCase_manyKey()
        
    elif 4 == testRange: #U盾在位
        testResult = ctrlObj.positiveCase()
        
    else:
        a=0
        
class GetBase64RandomCases():
    def __init__(self,testCtrl,AdminKeyInfo):
        self.testCtrl=testCtrl   #控件测试页
        self.AdminKeyAlgId=AdminKeyInfo  #保护密钥信息
        
    #用例描述：插入1支U盾，点击获取随机数
    def positiveCase(self):
        caseTitle  = "用例——插入1支U盾，点击获取随机数"  
        caseResult = None
        e=None

        testResult=self.testCtrl.get_Base64Random()
        
        if testResult.count("随机数获取成功，结果为："):
            caseResult="pass"
        else:
            caseResult="fail"
            e="实测返回："+"“"+re.sub(re.compile('\s+'),' ',testResult)+"”"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult
        
    def negativeCase_noKey(self):
        # 用例描述：未插入U盾，点击获取随机数,返回“随机数获取失败:未知错误。返回码:-102 There is no key!”错误提示
        caseTitle  = "用例——未插入U盾，点击获取随机数,返回“随机数获取失败:未知错误。返回码:-102 There is no key!”错误提示"
        caseResult = None
        e=None

        testResult=self.testCtrl.get_Base64Random()
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
        # 用例描述：插入多支同款U盾，点击获取随机数,返回“随机数获取失败:未知错误。返回码:-104 There is more than one key!
        caseTitle  = "用例——插入多支同款U盾，点击获取随机数,返回“随机数获取失败:未知错误。返回码:-104 There is more than one key!"
        caseResult = None
        e=None
        testResult=self.testCtrl.get_Base64Random()
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
    