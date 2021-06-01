#coding=utf-8
'''
Created on 2018.07.15 @author:  lzy
Created on 2018.08.13 @author:  syx
Created on 2018.08.18 @author:  ys
'''
import re
import string
import random
import operator
import GenCertGroup
from GlobalConfigure import levels,log_level

from logTest import LoggerClass
conf  = LoggerClass(loglevel=levels.get(log_level), logger="TestCases_GMWritePKCS7.py")
logger=conf.getlogger()

Para_Err = '写入证书失败:未知错误。返回码:-304 Failed Param!' 
many_key_Err = '写入证书失败:未知错误。返回码:-104 There is more than one key!'
no_key_Err='''写入证书失败:未知错误。返回码:-102 There is no key!'''

def test_GetGMWritePKCS7(ctrlObj,TestingRange,AdminKeyInfo):
    testCtrl=GetGMWritePKCS7Cases(ctrlObj,AdminKeyInfo)  #建立类对象，打开控件测试页 
    testGMWritePKCS7Group(testCtrl,TestingRange)   #测试用例集，根据测试范围定义测试强度

def testGMWritePKCS7Group(ctrlElemObj,testRange):
    #测试用例集
    if 0 == testRange:  #详细测试
        #正确性测试在其他用例文档中已包含
        a=0
        #testResult = ctrlElemObj.positiveCase()

        #testResult = ctrlElemObj.negativeCase_noKey_voidParaChoice()

        #testResult = ctrlElemObj.negativeCase_noKey_errParaChoice()

        #testResult = ctrlElemObj.negativeCase_noKeyFormattedInfo()

        #testResult = ctrlElemObj.negativeCase_ManyKey()

        #testResult = ctrlElemObj.negativeCase_ManyToOneKey()
           
    elif 1 == testRange: #验证测试
        testResult = ctrlElemObj.positiveCase()
                
    elif 2 == testRange: #无key测试
        testResult = ctrlElemObj.negativeCase_noKey_voidParaChoice()

        testResult = ctrlElemObj.negativeCase_noKey_errParaChoice()

        testResult = ctrlElemObj.negativeCase_noKey_validParaChoice()
        
    elif 3 == testRange: #多key测试
        testResult = ctrlElemObj.negativeCase_manyKey()
        
    elif 4 == testRange: #多key测试
        testResult = ctrlElemObj.positiveCase()
       
class GetGMWritePKCS7Cases():
    def __init__(self,testCtrl,AdminKeyInfo):
        self.testCtrl=testCtrl   #控件测试页
        self.AdminKeyAlgId=AdminKeyInfo  #保护密钥信息
        self.CertRequest=GenCertGroup.GenCertClass(self.testCtrl,AdminKeyInfo)   #创建证书申请对象
    
    def positiveCase(self):
        #插入1支U盾，输入请求信息：（申请RSA2048-sha1-混用）        
        caseTitle =  "用例——插入1支U盾，申请RSA1024—sha1-混用证书，期望成功！"
        caseResult = None
        e = None        
        certResult = self.CertRequest.genCert_with_RSA1024_Mix()
        if certResult[1]:
            caseResult = "pass"
        else:
            caseResult = "fail"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult

    def negativeCase_noKey_voidParaChoice(self):
        caseTitle = "用例——未插入U盾，不输入证书信息，点击写入证书; 期望返回：“写入证书失败:未知错误。返回码:-304 Failed Param!"
        e = None
        caseResult = None

        testResult = self.testCtrl.GMWritePKCS7()
        testResult = re.sub(re.compile('\s+'),' ',testResult) 
        if operator.eq(Para_Err, testResult): 
            caseResult = "pass"
        else:
            caseResult = "fail" 
            e =" 实测返回："+"“"+testResult+"”"       
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult

    def negativeCase_noKey_errParaChoice(self):
        caseTitle = "用例——未插入U盾，随意输入证书响应信息，点击写入证书 ;期望返回:写入证书失败:未知错误。返回码:-102 There is no key! "
        e = None
        caseResult = None
        p7CertData= ''.join(random.sample(string.ascii_letters + string.digits, 50))
        testResult=self.testCtrl.GMWritePKCS7(p7CertData)
        testResult = re.sub(re.compile('\s+'),' ',testResult) 
        if operator.eq(no_key_Err, testResult): 
            caseResult = "pass"
        else:
            caseResult = "fail" 
            e =" 实测返回："+"“"+testResult+"”"
            
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult      
             
    def negativeCase_noKey_validParaChoice(self):
        caseTitle = "用例——未插入U盾，输入合法PKCS07证书响应信息，点击写入证书 ;期望返回:写入证书失败:未知错误。返回码:-102 There is no key! "
        e = None
        caseResult = None

        base64P10="MIIFHzCCBIigAwIBAgIEESIzRDANBgkqhkiG9w0BAQUFADBEMRgwFgYDVQQDDA9NeU9wZW5TU0xSb290Q0ExCzAJBgNVBAYMAkNOMRswGQYDVQQKDBLljY7kuK3np5HmioDlpKflraYwHhcNMTgwODE5MDMyMTMwWhcNMjAwODE4MDMyMTMwWjCCA0QxFDASBgNVBAMMC1Rlc3RSU0ExMDI0MRswGQYDVQQKDBJyc2FwZXJjYTEzOS5jb20uY24xggMNMIIDCQYDVQQLDIIDAE1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdTCBnzANBgkqhkiG9w0BAQEFAAOBjQAwgYkCgYEAhuW6hmL3hVGMMW/B4lX4B1+u2HIS4tot8olSvSdf54s90LnEmDTXemWI8CUtWxit/x/9UUHayerEHGHWzVfDfziMu+di36lNljJVJOklndbsrRFvh/X1ys+/D7flCcfTr33VYAik6ujSasWqI3dRr3XhJlaWCv6M8Eabm65fDtsCAwEAAaMcMBowCwYDVR0PBAQDAgTwMAsGA1UdDgQEBAISNDANBgkqhkiG9w0BAQUFAAOBgQB06XpwSvPgkvm2z3xBPE0BjyzR6V6rSMnovUIqSlHlBlqM7fUq2JIE3aGLO9b1jl7RCpYwnwcr2pZMA3zzZnGifsa+PhDm3JRm5/2arbj/wxdzN7HEsuzvbjkrcRvbVNiMDNBBWaBSa8XwyPOqOfOZnhdys4kDAEgPyDXLXHm0DA=="

        #self.testCtrl.P102P7(base64P10)
        testResult = self.testCtrl.GMWritePKCS7(base64P10)
        testResult = re.sub(re.compile('\s+'),' ',testResult)
        if operator.eq(no_key_Err, testResult):
            caseResult = "pass"
        else:
            caseResult = "fail"
            e =" 实测返回："+"“"+testResult+"”"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult

    def negativeCase_manyKey(self):
        caseTitle = "用例——插入多支同款U盾,写入证书,期望返回：写入证书失败:未知错误。返回码:-104 There is more than one key!"
        caseResult = None
        e = None

        base64P10 = "MIIFHzCCBIigAwIBAgIEESIzRDANBgkqhkiG9w0BAQUFADBEMRgwFgYDVQQDDA9NeU9wZW5TU0xSb290Q0ExCzAJBgNVBAYMAkNOMRswGQYDVQQKDBLljY7kuK3np5HmioDlpKflraYwHhcNMTgwODE5MDMyMTMwWhcNMjAwODE4MDMyMTMwWjCCA0QxFDASBgNVBAMMC1Rlc3RSU0ExMDI0MRswGQYDVQQKDBJyc2FwZXJjYTEzOS5jb20uY24xggMNMIIDCQYDVQQLDIIDAE1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdU1pbmlDYU91TWluaUNhT3VNaW5pQ2FPdTCBnzANBgkqhkiG9w0BAQEFAAOBjQAwgYkCgYEAhuW6hmL3hVGMMW/B4lX4B1+u2HIS4tot8olSvSdf54s90LnEmDTXemWI8CUtWxit/x/9UUHayerEHGHWzVfDfziMu+di36lNljJVJOklndbsrRFvh/X1ys+/D7flCcfTr33VYAik6ujSasWqI3dRr3XhJlaWCv6M8Eabm65fDtsCAwEAAaMcMBowCwYDVR0PBAQDAgTwMAsGA1UdDgQEBAISNDANBgkqhkiG9w0BAQUFAAOBgQB06XpwSvPgkvm2z3xBPE0BjyzR6V6rSMnovUIqSlHlBlqM7fUq2JIE3aGLO9b1jl7RCpYwnwcr2pZMA3zzZnGifsa+PhDm3JRm5/2arbj/wxdzN7HEsuzvbjkrcRvbVNiMDNBBWaBSa8XwyPOqOfOZnhdys4kDAEgPyDXLXHm0DA=="

        # self.testCtrl.P102P7(base64P10)
        testResult = self.testCtrl.GMWritePKCS7(base64P10)
        testResult = re.sub(re.compile('\s+'),' ',testResult)
        if operator.eq(many_key_Err, testResult): 
            caseResult =  "pass"
        else:
            caseResult =  "fail"
            e =" 实测返回："+"“"+testResult+"”"

        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult              
    '''          
    def negativeCase_operation(self):
         # 用例描述：插入多支同款U盾，插入多个同款U盾，拔出多余U盾，只留1支在位，写入证书成功   期望返回：写入证书成功；
         caseTitle =  "用例——插入多个同款U盾，拔出多余U盾，只留1支在位，写入证书   期望返回：写入证书成功"
         caseResult = None
         e = None

         result = self.testCtrl.get_InitCard(str_title,str_srcPin,str_srcPin)
         if  None != result and "" != result and result == init_str:
             base64P10=self.testCtrl.GMCreatePKCS10(CertListInfoMap["RSA2048_Mixed_sha512"],'输入密码',str_srcPin)
             if "" != base64P10 and None != base64P10:
                 self.testCtrl.P102P7(base64P10)
                 testResult = self.testCtrl.GMWritePKCS7()
                 caseResult = "pass"
             else:
                 caseResult =  "fail"
                 e =" 实测返回："+"“"+base64P10+"”"
         else:
             caseResult = "fail"
             if result == None:
                 e =" 实测返回：None "
             else:
                 e =" 实测返回："+"“"+result+"”"
         if e == None:
             logger.critical("%s || %s ",caseResult,caseTitle)
         else:
             logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
         return caseResult
    '''
#########################
#开始测试
#########################
   