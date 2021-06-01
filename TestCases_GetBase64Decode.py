#coding=utf-8
'''
Created on 2018.08.21 @author: SYX
'''

import re         #引入正在表达式
import operator
from  GlobalConfigure import *

from logTest import SysClass, LoggerClass
conf  = LoggerClass(loglevel=levels.get(log_level), logger="TestCases_GetBase64Decode.py")
logger=conf.getlogger()

#错误信息列表
param_Err=  "操作失败:未知错误。返回码:-401 Base64 decoding failed!"

def test_GetBase64Decode(ctrlObj,TestingRange,AdminKeyInfo):
    testCtrl=GetBase64DecodeCases(ctrlObj,AdminKeyInfo)  #建立类对象，打开控件测试页 
    testGetBase64DecodeGroup(testCtrl,TestingRange)   #测试用例集，根据测试范围定义测试强度    
    
def testGetBase64DecodeGroup(GetBase64DecodeCtrl,testRange):
    #测试用例集
    if 0 == testRange:  #详细测试
        testResult = GetBase64DecodeCtrl.positiveCase()
        
    elif 1 == testRange: #验证测试
        testResult = GetBase64DecodeCtrl.positiveCase()
                
    elif 2 == testRange: #无key测试
        testResult = GetBase64DecodeCtrl.negativeCase_noKey_voidParaChoice()
        
    elif 3 == testRange: #多key测试
        a=0
        
    elif 4 == testRange: #U盾在位
        testResult = GetBase64DecodeCtrl.positiveCase()
        
    else:
        a=0
       
class GetBase64DecodeCases():
    def __init__(self,testCtrl,AdminKeyInfo):
        self.testCtrl=testCtrl   #控件测试页
        self.AdminKeyAlgId=AdminKeyInfo  #保护密钥信息

    def positiveCase(self):
        #用例描述：输入数据，正常返回
        caseTitle  = "用例——输入数据，正常返回"
        caseResult = None
        e=None
        str_Base64Data =self.testCtrl.get_ServerRandom()
        testResult=self.testCtrl.get_Base64Decode(str_Base64Data)
        if len(testResult)>0:
            caseResult="pass"
        else:
            caseResult="fail"
            e="实测返回："+"“"+re.sub(re.compile('\s+'),' ',testResult)+"”"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult
        
    def negativeCase_noKey_voidParaChoice(self):
        # 用例描述：BASE64解密，不输入数据,U盾不在位,返回“操作失败:未知错误。返回码:-401 Base64 decoding failed!”错误提示
        caseTitle  = "用例——BASE64解密，不输入数据,U盾不在位,返回“操作失败:未知错误。返回码:-401 Base64 decoding failed!”错误提示"
        caseResult = None
        e=None

        testResult=self.testCtrl.get_Base64Decode('')
        testResult=re.sub(re.compile('\s+'),' ',testResult)
        if operator.eq(testResult,param_Err):
            caseResult="pass"
        else:
            caseResult="fail"
            e="实测返回："+"“"+testResult+"”"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult
    
        
        
        
        
        