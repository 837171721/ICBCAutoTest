#coding=utf-8
'''
Created on 2018.03.21  @author: SYX
Created on 2018.08.10 @author:YS
'''
import re
import operator
import GenCertGroup
from GlobalConfigure import str_srcPin,levels, log_level

from logTest import SysClass, LoggerClass
conf  = LoggerClass(loglevel=levels.get(log_level), logger="TestCases_GetCertDN.py")
logger=conf.getlogger()

#错误信息列表
no_key_Err='''获取证书DN失败:未知错误。返回码:-102 There is no key!'''
many_key_Err='''获取证书DN失败:未知错误。返回码:-104 There is more than one key!'''

def test_GetCertDN(ctrlObj,TestingRange,AdminKeyInfo):
    #调用流程
    testCtrl=GetCertDNCases(ctrlObj,AdminKeyInfo)  #建立类对象，打开控件测试页 
    testGetCertDNGroup(testCtrl,TestingRange)   #测试用例集，根据测试范围定义测试强度
  
def testGetCertDNGroup(CertDNCtrl,testRange):
    #测试用例集
    if 0 == testRange:  #详细测试
        testResult=CertDNCtrl.positiveCase_noCert()

        testResult = CertDNCtrl.positiveCase_oneCert()

        testResult=CertDNCtrl.positiveCase_manyCert()
        
        #testResult=CertDNCtrl.negativeCase_noKey()
        #testResult=CertDNCtrl.negativeCase_manyKey()            
        #testResult=CertDNCtrl.negativeCase_operation()
                   
    elif 1 == testRange: #验证测试
        testResult=CertDNCtrl.positiveCase()  #其他接口已涉及，可以注释
        
    elif 2 == testRange:
        testResult = CertDNCtrl.negativeCase_noKey()
          
    elif 3 == testRange:       
        testResult = CertDNCtrl.negativeCase_manyKey() 
               
    elif 4 == testRange:   
        testResult = CertDNCtrl.positiveCase_noCert()
        
        testResult=CertDNCtrl.positiveCase()  #其他接口已涉及，可以注释
       
class GetCertDNCases():
    def __init__(self,testCtrl,AdminKeyInfo):
        self.testCtrl=testCtrl   #控件测试页
        self.AdminKeyAlgId=AdminKeyInfo  #保护密钥信息
        self.CertRequest=GenCertGroup.GenCertClass(self.testCtrl,AdminKeyInfo)   #创建证书申请对象

    def positiveCase(self):
        #用例描述：插入1支有1张证书U盾，点击获取证书DN，期望返回DN字符串信息
        caseTitle="用例——插入1支有1张证书的U盾，点击获取证书DN，期望返回DN字符串信息"
        caseResult = None
        e = None

        certResult=self.CertRequest.genCert_with_RSA1024_Mix()
        if certResult[1]:
            #logger.warning("响应证书DN为:%s",certResult[0])
            caseResult="pass"
        else:
            caseResult="fail"
            e="下证失败，结束用例执行！"
            
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult
              
    def positiveCase_noCert(self):
        #用例描述：插入1支无证书U盾，点击获取证书DN，期望返回空字符串
        caseTitle="用例——插入1支无证书的U盾，点击获取证书DN，期望返回空字符串"
        caseResult = None
        e = None

        initResult=self.CertRequest.init_key(str_srcPin,str_srcPin)
        if initResult[0]:
            testResult=self.testCtrl.get_GMCertDN()
            testResult=re.sub(re.compile('\s+'),' ',testResult)
            if None == testResult or '' == testResult:
                #logger.warning("响应证书DN为:%s",testResult)
                caseResult="pass"
            else:
                caseResult="fail"
                e="实测返回："+"“"+testResult+"”"
        else:
            caseResult="fail"
            e="初始化失败，结束用例执行！"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult

    def positiveCase_oneCert(self):
        #用例描述：插入1支无证书U盾，点击获取证书DN，期望返回空字符串
        caseTitle="用例——插入1支无证书的U盾，点击获取证书DN，期望返回空字符串"
        caseResult = None
        e = None
        certResult=self.CertRequest.genCert_with_RSA2048_Comm_P()
        if  certResult[1]:
            #logger.warning("响应证书DN为:%s", certResult[0])
            caseResult = "pass"
        else:
            caseResult = "fail"
            e = "下证失败，结束用例执行！"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult

    def positiveCase_manyCert(self):
        #用例描述：插入1支有多张证书U盾，点击获取证书DN，期望返回多张证书的DN字符串信息，以||分隔
        caseTitle="用例——插入1支有多张证书的U盾，点击获取证书DN，期望返回多张证书的DN字符串信息，以||分隔"
        caseResult = None
        e = None

        certResult=self.CertRequest.genCert_with_rsa1024Cp_and_rsa2048M()
        if  certResult[1]:       
            #logger.warning("响应证书DN为:%s",certResult[0])
            caseResult="pass"
        else:
            caseResult="fail"
            e="下证失败，结束用例执行！"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult

    def negativeCase_noKey(self):
        #用例描述：未插入U盾，点击获取证书DN，期望返回“获取证书DN失败:未知错误。返回码:-102 There is no key!”
        caseTitle="用例——未插入U盾，点击获取证书DN，期望返回“获取证书DN失败:未知错误。返回码:-102 There is no key!”"
        caseResult = None
        e = None

        certDNResult=self.testCtrl.get_GMCertDN()
        certDNResult=re.sub(re.compile('\s+'),' ',certDNResult)
        if operator.eq(no_key_Err,certDNResult):
            #logger.warning("响应证书DN为:%s",certDNResult)
            caseResult="pass"
        else:
            caseResult="fail"
            e = "实测返回：" + "“" + re.sub(re.compile('\s+'), ' ', certDNResult) + "”"
        
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult

    def negativeCase_manyKey(self):
        #用例描述：插入多支同款U盾，点击获取证书DN，期望返回“获取证书DN失败:未知错误。返回码:-104 There is more than one key!”
        caseTitle="用例——插入多支同款U盾，点击获取证书DN，期望返回“获取证书DN失败:未知错误。返回码:-104 There is more than one key!”"
        caseResult = None
        e = None

        certDNResult=self.testCtrl.get_GMCertDN()
        certDNResult=re.sub(re.compile('\s+'),' ',certDNResult)
        if operator.eq(many_key_Err, certDNResult):
            #logger.warning("响应证书DN为:%s",certDNResult)
            caseResult = "pass"
        else:
            caseResult = "fail"
            e = "实测返回：" + "“" + re.sub(re.compile('\s+'), ' ', certDNResult) + "”"
        
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult

    def negativeCase_operation(self):
        #用例描述：插入多支同款U盾，拔出多余U盾，只留1支在位，点击获取证书DN，期望返回证书DN字符串信息
        caseTitle="用例——插入多支同款U盾，拔出多余U盾，只留1支在位，点击获取证书DN，期望返回证书DN字符串信息"
        caseResult = None
        e = None

        certDNResult=self.testCtrl.get_GMCertDN()
        certDNResult=re.sub(re.compile('\s+'),' ',certDNResult)
        if False == operator.eq(many_key_Err, certDNResult) and  False == operator.eq(no_key_Err, certDNResult):
            #logger.warning("响应证书DN为:%s",caseResult)
            caseResult = "pass"
        else:
            caseResult = "fail"
            e = "实测返回：" + "“" + re.sub(re.compile('\s+'), ' ', certDNResult) + "”"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult

#########################
#开始测试
#########################
