#coding=utf-8
'''
Created on 2018.03.27 @author: FJQ
Created on 2018.08.18 @author: YS
'''
import re  # 引入正在表达式
import operator
import GenCertGroup
from GlobalConfigure import levels,log_level,str_srcPin,CertListInfoMap

from logTest import SysClass,LoggerClass
conf  = LoggerClass(loglevel=levels.get(log_level), logger="TestCases_UnRegisterCertC.py")
logger=conf.getlogger()

#错误信息列表
no_key_Err="注销证书失败:未知错误。返回码:-102 There is no key!"
no_cert_Err="注销证书失败:未知错误。返回码:-318 There is no certificate!"
many_key_Err="注销证书失败:未知错误。返回码:-104 There is more than one key!"
right_Info_one="1"
right_Info_two="2"


def test_GetUnResgisterCertC(ctrlObj,TestingRange,AdminKeyInfo):
    testCtrl=GetUnResgisterCertCCases(ctrlObj,AdminKeyInfo)  #建立类对象，打开控件测试页 
    testUnResgisterCertCGroup(testCtrl,TestingRange)   #测试用例集，根据测试范围定义测试强度

def testUnResgisterCertCGroup(ctrlElemObj,testRange):
    #测试用例集
    if 0 == testRange:  #详细测试
        testResult = ctrlElemObj.positiveCase_oneCert()#插入1只1张证书的key，注册证书后注销证书

        testResult = ctrlElemObj.positiveCase_manyCertAndmanyTempKeyPair()#插入1只2张证书、2个密钥对的key，点击注销证书

        testResult = ctrlElemObj.negativeCase_formatKey()#插入一只格式化key，点击注销证书

        testResult = ctrlElemObj.negativeCase_tempKeyPair()#插入1只1对临时密钥对的key，点击注销证书

        testResult = ctrlElemObj.negativeCase_unRegisterCertRepeated()#反复注销证书

        #testResult = ctrlElemObj.positiveCase_deleteandregistered()# 无法实现，删除IE证书池中已经注册的证书，再注销证书

    elif 1 == testRange: #验证测试
        testResult = ctrlElemObj.positiveCase()

    elif 2 == testRange:  # 无key测试
        testResult = ctrlElemObj.negativeCase_noKey()

    elif 3 == testRange:  # 多key测试
        testResult = ctrlElemObj.negativeCase_manyKey()

    elif 4 == testRange:  # 多key测试
        testResult = ctrlElemObj.positiveCase()
        
class GetUnResgisterCertCCases():
    def __init__(self,testCtrl,AdminKeyInfo):
        self.testCtrl=testCtrl   #控件测试页
        self.AdminKeyAlgId=AdminKeyInfo  #保护密钥信息
        self.CertRequest=GenCertGroup.GenCertClass(self.testCtrl,AdminKeyInfo)   #创建证书申请对象
                
    def positiveCase(self):
        #插入一只有1张证书的U盾，点击注销证书，期望返回1
        caseTitle  = "插入一只有1张证书的U盾，注册证书后注销证书，期望均返回1"
        caseResult = None
        e=None
        logger.critical("beginning... || %s ", caseTitle)
        certResult=self.CertRequest.genCert_with_RSA1024_Mix()
        if certResult[1]:            
            testResult=self.testCtrl.RegisterCertC()
            testResult=re.sub(re.compile('\s+'), ' ', testResult)
            if right_Info_one == testResult:
                caseResult = "pass"
                logger.critical("%s || 注册证书 || %s ", caseResult,testResult)
                testResult=self.testCtrl.UnRegisterCertC()
                testResult = re.sub(re.compile('\s+'), ' ', testResult)
                if right_Info_one == testResult:
                    logger.critical("%s || 注销证书 || %s ", caseResult,testResult)
                else:
                    caseResult = "fail"
                    logger.critical("%s || 注销证书 || 实际返回：%s ", caseResult,testResult)
            else:
                caseResult="fail"
                logger.critical("%s || 注册证书 || 实际返回：%s ", caseResult, testResult)
        else:
            caseResult = "fail"
            e = "证书下载失败,结束用例执行"
            logger.critical("%s || %s ", caseResult, e)

        logger.critical("end. || %s ", caseTitle)
        return caseResult

    def negativeCase_noKey(self):
        #用例描述：未插入U盾，点击注销证书:未知错误。返回码:注销证书失败:未知错误。返回码:-102 There is no key!
        caseTitle  = "用例——未插入U盾，点击注销证书:未知错误。返回码:注销证书失败:未知错误。返回码:-102 There is no key!"
        caseResult = None
        e=None

        testResult=self.testCtrl.UnRegisterCertC()
        testResult=re.sub(re.compile('\s+'),' ',testResult)
        if operator.eq(no_key_Err, testResult):
            caseResult="pass"
        else:
            caseResult="fail"
            e="实测返回："+"“"+testResult+"”"
            
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult
                
    def negativeCase_formatKey(self):
        #用例描述：插入初始化的U盾，点击注销证书，期望返回:注销证书失败:未知错误。返回码:-318 There is no certificate!
        caseTitle  = "用例——插入初始化的U盾，点击注销证书，期望返回:注注销证书失败:未知错误。返回码:-318 There is no certificate!"
        caseResult = None
        e=None
        initResult=self.CertRequest.init_key(str_srcPin,str_srcPin)
        if initResult[0]:
            testResult=self.testCtrl.UnRegisterCertC()
            testResult=re.sub(re.compile('\s+'),' ',testResult)
            if operator.eq(no_cert_Err, testResult):
                caseResult="pass"
            else:
                caseResult="fail"
                e="实测返回："+"“"+testResult+"”"
        else:
            caseResult = "fail"
            e = "初始化失败，结束用例执行"

        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult

    def positiveCase_oneCert(self):
        #用例描述：只有1张证书的U盾，注册证书后注销证书，期望均返回1
        caseTitle = "插入一只有1张证书的U盾，注册证书后注销证书，期望均返回1"
        caseResult = None
        e = None
        logger.critical("beginning... || %s ", caseTitle)
        certResult = self.CertRequest.genCert_with_RSA1024_Mix()
        if certResult[1]:
            testResult = self.testCtrl.RegisterCertC()
            testResult = re.sub(re.compile('\s+'), ' ', testResult)
            if right_Info_one == testResult:
                caseResult = "pass"
                logger.critical("%s || 注册证书 || %s ", caseResult, testResult)
                testResult = self.testCtrl.UnRegisterCertC()
                testResult = re.sub(re.compile('\s+'), ' ', testResult)
                if right_Info_one == testResult:
                    logger.critical("%s || 注销证书 || %s ", caseResult, testResult)
                else:
                    caseResult = "fail"
                    logger.critical("%s || 注销证书 || 实际返回：%s ", caseResult, testResult)
            else:
                caseResult = "fail"
                logger.critical("%s || 注册证书 || 实际返回：%s ", caseResult, testResult)
        else:
            caseResult = "fail"
            e = "证书下载失败,结束用例执行"
            logger.critical("%s || %s ", caseResult, e)

        logger.critical("end. || %s ", caseTitle)
        return caseResult

    def negativeCase_tempKeyPair(self):
        #用例描述：插入一只有1对临时密钥对，点击注销证书   ，期望返回：注销证书失败:未知错误。返回码:-318 There is no certificate!
        caseTitle  = "用例——插入一只有1对临时密钥对，点击注册证书   ，期望返回：注册证书失败:未知错误。返回码:-318 There is no certificate!"
        caseResult = None
        e=None

        tempKeyPair = self.CertRequest.genKeyPair(CertListInfoMap["RSA1024_Mixed"], str_srcPin,True)
        if tempKeyPair[1]:
            testResult=self.testCtrl.UnRegisterCertC()
            testResult=re.sub(re.compile('\s+'),' ',testResult)
            if operator.eq(no_cert_Err, testResult):
                caseResult="pass"
            else:
                caseResult="fail"
                e="实测返回："+"“"+testResult+"”"

        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult

    def positiveCase_manyCertAndmanyTempKeyPair(self):
        # 用例描述：插入一只有2张证书，2个密钥对，点击注销证书，期望返回2
        caseTitle  = "用例——插入一只有2张证书，2个密钥对，点击注册和注销证书，期望返回均为2"
        caseResult = None
        e=None

        logger.critical("beginning... || %s ", caseTitle)
        certResult = self.CertRequest.genCert_with_rsa1024M_and_rsa2048M()
        tempKeyPair=self.CertRequest.genKeyPair(CertListInfoMap["RSA1024_M_and_RSA2048_M"],certResult[2])
        if certResult[1] and tempKeyPair[1]:
            testResult = self.testCtrl.RegisterCertC()
            testResult = re.sub(re.compile('\s+'), ' ', testResult)
            if right_Info_two == testResult:
                caseResult = "pass"
                logger.critical("%s || 注册证书 || %s ", caseResult, testResult)
                testResult = self.testCtrl.UnRegisterCertC()
                testResult = re.sub(re.compile('\s+'), ' ', testResult)
                if right_Info_two == testResult:
                    logger.critical("%s || 注销证书 || %s ", caseResult, testResult)
                else:
                    caseResult = "fail"
                    logger.critical("%s || 注销证书 || 实际返回：%s ", caseResult, testResult)
            else:
                caseResult = "fail"
                logger.critical("%s || 注册证书 || 实际返回：%s ", caseResult, testResult)
        else:
            caseResult = "fail"
            e = "生成密钥对或证书下载失败,结束用例执行"
            logger.critical("%s || %s ", caseResult, e)
        logger.critical("end. || %s ", caseTitle)
        return caseResult

    def negativeCase_unRegisterCertRepeated(self):
        #用例描述：插入一只有1张证书的U盾，反复注销证书，期望返回注销证书失败:未知错误。返回码:-318 There is no certificate!
        caseTitle  = "用例——插入一只有1张证书的U盾，反复注销证书，期望返回：注销证书失败:未知错误。返回码:-318 There is no certificate!"
        caseResult = None
        e=None

        certResult=self.CertRequest.genCert_with_RSA1024_Comm_C()
        if certResult[1]:
            #反复注销
            testResult = self.testCtrl.RegisterCertC()
            testResult = re.sub(re.compile('\s+'), ' ', testResult)
            if right_Info_one== testResult:
                self.testCtrl.browser.find_element_by_id("UnRegisterCert").click()

                testResult=self.testCtrl.UnRegisterCertC()
                testResult=re.sub(re.compile('\s+'),' ',testResult)
                if operator.eq(no_cert_Err, testResult):
                    caseResult="pass"
                else:
                    caseResult="fail"
                    e="实测返回："+"“"+testResult+"”"
            else:
                caseResult = "fail"
                e="证书注册失败"
        else:
            caseResult = "fail"
            e = "证书下载失败,结束用例执行"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult

    def negativeCase_manyKey(self):
        #用例描述：插入多支同款U盾，点击注销证书，期望返回“注销证书失败:未知错误。返回码:-104 There is more than one key!”
        caseTitle  = "用例——插入多支同款U盾，点击注销证书，期望返回“注销证书失败:未知错误。返回码:-104 There is more than one key!"
        caseResult = None
        e=None
        
        testResult=self.testCtrl.UnRegisterCertC()
        testResult=re.sub(re.compile('\s+'),' ',testResult)
        if operator.eq(many_key_Err, testResult):
            caseResult="pass"
        else:
            caseResult="fail"
            e="实测返回："+"“"+re.sub(re.compile('\s+'),' ',testResult)+"”"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult

'''
    #用例描述：插入多支同款U盾，拔出多余U盾，只留1支在位，点击注销证书，期望返回正确结果
    def positiveCase_operation(self):
        #第十三条用例
        caseTitle  = "用例——插入多支同款U盾，拔出多余U盾，只留1支在位，点击注销证书，期望返回正确结果"
        caseResult = None
        e=None
         
        GenCertGroup.GenCertClass(self.testCtrl).genCert_with_RSA1024_Mix()
        
        testResult=self.testCtrl.UnRegisterCertC()
        #testResult=re.sub(re.compile('\s+'),' ',testResult)
        if right_Info_one == testResult:
            caseResult="pass"
        else:
            caseResult="fail"
            e="实测返回："+"“"+testResult+"”"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult
'''