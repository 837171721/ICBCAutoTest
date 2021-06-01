#coding=utf-8
'''
Created on 2018.10.15 @author: SYX
'''

import re         #引入正在表达式
import operator
from GlobalConfigure import levels,log_level,str_title,str_srcPin,CertListInfoMap,AmdinKey_3DES,AmdinKey_AES_new,AmdinKey_SM4
import win32api, win32con
import GenCertGroup

from logTest import SysClass, LoggerClass,main_url,testUrl_Manage
conf  = LoggerClass(loglevel=levels.get(log_level), logger="TestCases_InitCardDefaultPin.py")
logger=conf.getlogger()

#错误信息列表
right_info="写入证书成功"
cancel_Err=  "初始化失败:未知错误。返回码:-100 User cancel!"
ver_Err = "初始化失败:未知错误。返回码:-411 ukey version error!"
no_key_Err="初始化失败:未知错误。返回码:-102 There is no key!"
para_Err="初始化失败:-300 Failed!"

def test_ImportEncCert(ctrlObj,TestingRange,AdminKeyInfo):
    testCtrl=ImportEncCertCases(ctrlObj,AdminKeyInfo)  #建立类对象，打开控件测试页   
    if False == AdminKeyInfo[0]:
        logger.warning("接口不支持，请选择蓝牙盾进行!")
        return
    tesImportEncCertCase(testCtrl,TestingRange)   #测试用例集，根据测试范围定义测试强度    
    
def tesImportEncCertCase(ImportEncCertCtrl,testRange):
    #测试用例集
    if 0 == testRange:  #详细测试
        testResult = ImportEncCertCtrl.positiveCase()
        
        testResult = ImportEncCertCtrl.operationCase_pressC()  
        
    elif 1 == testRange: #验证测试
        testResult = ImportEncCertCtrl.positiveCase()
                
    elif 2 == testRange: #无key测试
        testResult = ImportEncCertCtrl.negativeCase_noKey()
        
    elif 3 == testRange: #多key测试
        a=0
        
    elif 4 == testRange: #U盾在位
        testResult = ImportEncCertCtrl.positiveCase()
        
        testResult = ImportEncCertCtrl.operationCase_pressC()  
        
    else:
        a=0
       
class ImportEncCertCases():
    def __init__(self,testCtrl,AdminKeyInfo):
        self.testCtrl=testCtrl   #控件测试页
        self.AdminKeyAlgId=AdminKeyInfo  #保护密钥信息
        if '00' == self.AdminKeyAlgId[1]:
            self.AdminKey = AmdinKey_3DES
        if '01' == self.AdminKeyAlgId[1]:
            self.AdminKey = AmdinKey_AES_new
        if '02' == self.AdminKeyAlgId[1]:
            self.AdminKey = AmdinKey_SM4
        self.CertRequest=GenCertGroup.GenCertClass(self.testCtrl,AdminKeyInfo)  

    def positiveCase(self):
        #用例描述：插入1支U盾，点击初始化，返回初始化成功
        caseTitle  = "用例——插入1支U盾，点击写入签名和加密证书，返回写入成功"
        caseResult = None
        e=None
        InitResult=self.CertRequest.init_key(str_srcPin,str_srcPin)   
        #InitResult=[True,'12345678'] 
        if InitResult[0]:                
            ImportEncCertInfo=self.testCtrl.setImportEncCertInfo(CertListInfoMap["SM2256_Sig2_c"], str_title, InitResult[1], self.AdminKeyAlgId[1], self.AdminKey)
            if '00' == self.AdminKeyAlgId[1]:
                ImportEncCertResult=self.testCtrl.GMWritePKCS7Enc(ImportEncCertInfo[0],ImportEncCertInfo[1])
            else:
                ImportEncCertResult=self.testCtrl.GMWritePKCS7Enc(ImportEncCertInfo[0],ImportEncCertInfo[1],ImportEncCertInfo[2])
            if operator.eq(ImportEncCertResult,right_info):
                caseResult="pass"                        
            else:
                caseResult="fail"
                e="实测返回："+"“"+re.sub(re.compile('\s+'),' ',ImportEncCertResult)+"”"
        else:
            caseResult="fail"
            e="初始化失败,结束用例执行"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult
    
        