#coding=utf-8
'''
Created on 2018.06.23 @author: SYX
'''
import re
import operator
import GenCertGroup
from GlobalConfigure import levels,log_level,str_srcPin,CertListInfoMap

from logTest import SysClass, LoggerClass
conf  = LoggerClass(loglevel=levels.get(log_level), logger="TestCases_GetPubKeyNum.py")
logger=conf.getlogger()
 
#错误信息列表
no_key_Err='''获取公钥个数失败:未知错误。返回码:-102 There is no key!'''
many_key_Err='''获取公钥个数失败:未知错误。返回码:-104 There is more than one key!'''

def test_GetPubKeyNum(ctrlObj,TestingRange,AdminKeyInfo):
    #调用流程
    testCtrl=GetPubKeyNumCases(ctrlObj,AdminKeyInfo)  #建立类对象，打开控件测试页 
    testGetPubKeyNumGroup(testCtrl,TestingRange)   #测试用例集，根据测试范围定义测试强度

def testGetPubKeyNumGroup(ctrlElemObj,testRange):
    #测试用例集
    if 0 == testRange:  #详细测试
        testResult = ctrlElemObj.positiveCase_formatKey()

        testResult = ctrlElemObj.positiveCase_oneCert()

        testResult = ctrlElemObj.positiveCase_tempkeypair()

        testResult = ctrlElemObj.positiveCase_manyCertAndmanyKeyPair()

        #testResult = ctrlElemObj.negativeCase_noKey()
        #testResult = ctrlElemObj.negativeCase_manyKey()
        #testResult = ctrlElemObj.negativeCase_operation()
                         
    elif 1 == testRange: #验证测试
        testResult = ctrlElemObj.positiveCase()
                
    elif 2 == testRange: #无key测试
        testResult = ctrlElemObj.negativeCase_noKey()
        
    elif 3 == testRange: #多key测试
        testResult = ctrlElemObj.negativeCase_manyKey()
        
    elif 4 == testRange: #多key测试
        testResult = ctrlElemObj.positiveCase_formatKey()
        
        testResult = ctrlElemObj.positiveCase()
       
class GetPubKeyNumCases():
    def __init__(self,testCtrl,AdminKeyInfo):
        self.testCtrl=testCtrl   #控件测试页
        self.AdminKeyAlgId=AdminKeyInfo  #保护密钥信息
        self.CertRequest=GenCertGroup.GenCertClass(self.testCtrl,AdminKeyInfo)   #创建证书申请对象
          
    def positiveCase(self):
        #用例描述：U盾中只有1张证书，点击获取公钥个数，期望返回1
        caseTitle="用例——U盾中只有1张证书，点击获取公钥个数，期望返回1"
        caseResult = None
        e = None
        certResult=self.CertRequest.genCert_with_RSA1024_Mix()
        if certResult[1]:
            testResult=self.testCtrl.get_PubKeyNum()
            if "1" == testResult:
                #logger.warning("获取公钥个数为%s:",testResult)
                caseResult="pass"
            else:
                caseResult="fail"
                e="实测返回："+"“"+testResult+"”"
        else:
            caseResult="fail"
            e="下载证书失败,结束用例执行"

        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult

    def positiveCase_oneCert(self):
        #用例描述：U盾中只有1张证书，点击获取公钥个数，期望返回1
        caseTitle="用例——U盾中只有1张证书，点击获取公钥个数，期望返回1"
        caseResult = None
        e = None
        certResult=self.CertRequest.genCert_with_RSA1024_Mix()
        if certResult[1]:
            testResult=self.testCtrl.get_PubKeyNum()
            if "1" == testResult:
                #logger.warning("获取公钥个数为%s:",testResult)
                caseResult="pass"
            else:
                caseResult="fail"
                e="实测返回："+"“"+testResult+"”"
        else:
            caseResult="fail"
            e="下载证书失败,结束用例执行"

        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult

    def positiveCase_tempkeypair(self):
        #用例描述：U盾中只有1对临时密钥对，点击获取公钥个数，期望返回1
        caseTitle="用例——U盾中只有1对临时密钥对，点击获取公钥个数，期望返回1"
        caseResult = None
        e = None
        keypairResult=self.CertRequest.genKeyPair(CertListInfoMap["RSA1024_Mixed"], str_srcPin,True) 
        if keypairResult[1]:
            testResult=self.testCtrl.get_PubKeyNum()
            if "1" == testResult:
                #logger.warning("获取公钥个数为%s:",testResult)
                caseResult="pass"
            else:
                caseResult="fail"
                e="实测返回："+"“"+testResult+"”"
        else:
            caseResult="fail"
            e="下载证书失败,结束用例执行"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult

    def positiveCase_formatKey(self):
        #用例描述：插入初始化的U盾，点击获取公钥个数，期望返回0
        caseTitle="用例——插入初始化的U盾，点击获取公钥个数，期望返回0"
        caseResult = None
        e = None
        initResult=self.CertRequest.init_key(str_srcPin,str_srcPin)
        if initResult[0]:
            testResult=self.testCtrl.get_PubKeyNum()
            if "0" == testResult:
                #logger.warning("获取公钥个数为%s:",testResult)
                caseResult="pass"
            else:
                caseResult="fail"
                e="实测返回："+"“"+testResult+"”"
        else:
            caseResult="fail"
            e="初始化失败,结束用例执行"

        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult

    def positiveCase_manyCertAndmanyKeyPair(self):
        #用例描述：U盾中有m张证书，n个密钥对，点击获取公钥个数，期望返回m+n
        caseTitle="用例——U盾中有2张证书，2个密钥对，点击获取公钥个数，期望返回4"
        caseResult = None
        e = None
        certResult=self.CertRequest.genCert_with_rsa1024M_and_rsa1024M()
        keypairResult=self.CertRequest.genKeyPair(CertListInfoMap["RSA2048_C(p)_and_RSA2048_M"], certResult[2]) 
        if certResult[1] and keypairResult[1]: 
            testResult=self.testCtrl.get_PubKeyNum()
            if "4" == testResult:
                #logger.warning("获取公钥个数为%s:",testResult)
                caseResult="pass"
            else:
                caseResult="fail"
                e="实测返回："+"“"+testResult+"”"
        else:
            caseResult="fail"
            e="证书下载失败，结束用例执行"

        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult

    def negativeCase_noKey(self):
        #用例描述：未插入U盾，点击获取公钥个数，返回“获取公钥个数失败:未知错误。返回码:-102 There is no key!”
        caseTitle="用例——未插入U盾，点击获取公钥个数,返回“获取公钥个数失败:未知错误。返回码:-102 There is no key!”"
        caseResult = None
        e = None
        testResult=self.testCtrl.get_PubKeyNum()
        testResult=re.sub(re.compile('\s+'),' ',testResult)
        if operator.eq(no_key_Err,testResult):
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
        #用例描述：插入多支同款U盾，点击获取公钥个数，期望返回“获取公钥个数失败:未知错误。返回码:-104 There is more than one key!”
        caseTitle="用例——插入多支同款U盾，点击获取公钥个数，期望返回“获取公钥个数失败:未知错误。返回码:-104 There is more than one key!”"
        caseResult = None
        e = None
        testResult=self.testCtrl.get_PubKeyNum()
        testResult=re.sub(re.compile('\s+'),' ',testResult)
        if operator.eq(many_key_Err,testResult):
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
        #用例描述：插入多支同款U盾，拔出多余U盾，只留1支在位，点击获取公钥个数，期望返回公钥个数
        caseTitle="用例——插入多支同款U盾，拔出多余U盾，只留1支在位，点击获取公钥个数，期望返回公钥个数"
        caseResult = None
        e = None
        #if 0 == TestingType:
            #win32api.MessageBox(0, "插入多支同款U盾，拔出多余U盾，只留1支在位！", "提示框",win32con.MB_OK)
        testResult=self.testCtrl.get_PubKeyNum()
        testResult=re.sub(re.compile('\s+'),' ',testResult)
        if "2" == testResult:
            #logger.warning("获取公钥个数为%s:",testResult)
            caseResult="pass"
        else:
            caseResult="fail"
            e="实测返回："+"“"+testResult+"”"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult
    
#########################
#开始测试
#########################
    
   