#coding=utf-8
'''
Created on 2018.04.01 @author: SYX
Created on 2018.07.18 @author: YS
'''
import re
import GenCertGroup
from GlobalConfigure import DriverVer,str_srcPin,levels, log_level

from logTest import SysClass, LoggerClass
conf  = LoggerClass(loglevel=levels.get(log_level), logger="TestCases_GetDriverVer.py")
logger=conf.getlogger()

def test_GetDriverVer(ctrlObj,TestingRange,AdminKeyInfo):
    #调用流程
    testCtrl=GetDriverVerCases(ctrlObj,AdminKeyInfo)  #建立类对象，打开控件测试页 
    testGetDriverVerGroup(testCtrl,TestingRange)   #测试用例集，根据测试范围定义测试强度
  
def testGetDriverVerGroup(ctrlElemObj,testRange):
    #测试用例集
    if 0 == testRange:  #详细测试        
        testResult=ctrlElemObj.positiveCase_formatKey()

        testResult=ctrlElemObj.positiveCase_oneCert()

        #testResult=ctrlElemObj.positiveCase_noKey()

        #testResult=ctrlElemObj.positiveCase_manyKey()
    
        #testResult=ctrlElemObj.positiveCase_operation()

                          
    elif 1 == testRange: #验证测试
        testResult=ctrlElemObj.positiveCase()
       
    elif 2 == testRange:
        testResult = ctrlElemObj.positiveCase_noKey()

    elif 3 == testRange:
        testResult = ctrlElemObj.positiveCase_manyKey()
        
    elif 4 == testRange:
        testResult=ctrlElemObj.positiveCase()
       
class GetDriverVerCases():
    def __init__(self,testCtrl,AdminKeyInfo):
        self.testCtrl=testCtrl   #控件测试页
        self.AdminKeyAlgId=AdminKeyInfo  #保护密钥信息
        self.CertRequest=GenCertGroup.GenCertClass(self.testCtrl,AdminKeyInfo)   #创建证书申请对象
           
    def positiveCase(self):
        #用例描述：插入1支U盾，点击获取驱动版本号，返回当前安装驱动版本号：Driver版本号x.x.x.x
        caseTitle="用例——插入1支U盾，点击获取驱动版本号，返回当前安装驱动版本号：Driver版本号x.x.x.x"
        caseResult = None
        e = None      
        testResult=self.testCtrl.get_DriverVer()
        testResult=re.sub(re.compile('\s+'),' ',testResult)
        if DriverVer in testResult:
            #logger.warning("响应驱动版本号为:%s",testResult)
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
        #用例描述：插入1支无证书U盾，点击获取驱动版本号，返回当前安装驱动版本号：Driver版本号x.x.x.x
        caseTitle="用例——插入无证书的U盾，点击获取驱动版本号，返回当前安装驱动版本号：Driver版本号x.x.x.x"
        caseResult = None
        e = None
        initResult=self.CertRequest.init_key(str_srcPin,str_srcPin)
        if initResult[0]:
            testResult=self.testCtrl.get_DriverVer()
            testResult=re.sub(re.compile('\s+'),' ',testResult)
            if DriverVer in testResult:
                #logger.warning("响应驱动版本号为:%s",testResult)
                caseResult="pass"
            else:
                caseResult="fail"
                e="实测返回："+"“"+testResult+"”"
        else:
            caseResult="fail"
            e="初始化操作失败，结束用例执行！"
            
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult
    
    def positiveCase_oneCert(self):
        #用例描述：插入1支有1张证书U盾，点击获取驱动版本号，返回当前安装驱动版本号：Driver版本号x.x.x.x
        caseTitle="用例——插入1支有1张证书U盾，点击获取驱动版本号，返回当前安装驱动版本号：Driver版本号x.x.x.x"
        caseResult=None
        e=None

        certResult=self.CertRequest.genCert_with_RSA1024_Mix(False)
        if certResult[1]:             
            testResult=self.testCtrl.get_DriverVer()
            testResult=re.sub(re.compile('\s+'),' ',testResult)
            if DriverVer in testResult:
                #logger.warning("响应驱动版本号为:%s",testResult)
                caseResult="pass"
            else:
                caseResult="fail"
                e="实测返回："+"“"+testResult+"”"
        else:
            caseResult="fail"
            e="证书下载失败，结束用例执行！"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult
    
    def positiveCase_noKey(self):
        #用例描述：未插入U盾，点击获取驱动版本号，返回当前安装驱动版本号：Driver版本号x.x.x.x
        caseTitle="用例——未插入U盾，点击获取驱动版本号，返回当前安装驱动版本号：Driver版本号x.x.x.x"
        caseResult=None
        e=None
        
        testResult=self.testCtrl.get_DriverVer()
        testResult=re.sub(re.compile('\s+'),' ',testResult)        
        if DriverVer in testResult:
            #logger.warning("响应驱动版本号为:%s",testResult)
            caseResult="pass"
        else:
            caseResult="fail"
            e="实测返回："+"“"+testResult+"”"
            
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult
        
    def positiveCase_manyKey(self):
        #用例描述：插入多支同款U盾，点击获取驱动版本号，返回当前安装驱动版本号：Driver版本号x.x.x.x”
        caseTitle="用例——插入多支同款U盾，点击获取驱动版本号，返回当前安装驱动版本号：Driver版本号x.x.x.x"
        caseResult=None
        e=None
        
        testResult=self.testCtrl.get_DriverVer()
        testResult=re.sub(re.compile('\s+'),' ',testResult)        
        if DriverVer in testResult:
            #logger.warning("响应驱动版本号为:%s",testResult)
            caseResult="pass"
        else:
            caseResult="fail"
            e="实测返回："+"“"+testResult+"”"
            
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult
    
    def positiveCase_operation(self):
        #用例描述：插入多支同款U盾，拔出多余U盾，只留1支在位，点击获取驱动版本号，返回当前安装驱动版本号：Driver版本号x.x.x.x
        caseTitle="用例——插入多支同款U盾，拔出多余U盾，只留1支在位，点击获取驱动版本号，返回当前安装驱动版本号：Driver版本号x.x.x.x"
        caseResult=None
        e=None
        
        testResult=self.testCtrl.get_DriverVer()
        testResult=re.sub(re.compile('\s+'),' ',testResult)        
        if DriverVer in testResult:
            logger.warning("响应驱动版本号为:%s",testResult)
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
   