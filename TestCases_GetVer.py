
#coding=utf-8
'''
Created on 2018.03.27 @author: lzy
Created on 2018.07.26 @author: ys
Created on 2018.08.09 @author: syx
Created on 2018.08.18 @author: ys
'''
import re
import GenCertGroup
from GlobalConfigure import levels,log_level,str_srcPin,CtrlVer

from logTest import SysClass, LoggerClass
conf  = LoggerClass(loglevel=levels.get(log_level), logger="TestCases_GetVer.py")
logger=conf.getlogger()

def test_GetVer(ctrlObj,TestingRange,AdminKeyInfo):
    #调用流程
    testCtrl=getGetVerCases(ctrlObj,AdminKeyInfo)  #建立类对象，打开控件测试页 
    testGetVerGroup(testCtrl,TestingRange)   #测试用例集，根据测试范围定义测试强度

def testGetVerGroup(ctrlElemObj,testRange):
    #测试用例集
    if 0 == testRange:  #详细测试        
        testResult = ctrlElemObj.positiveCase_formatKey()  #插入一支格式化的U盾，点击控件版本号

        testResult = ctrlElemObj.positiveCase_oneCert()    #插入一支有证书的U盾，点击控件版本号

        #testResult= ctrlElemObj.positiveCase_noKey()      #未插入U盾，点击控件版本号

        #testResult = ctrlElemObj.positiveCase_ManyKey()    #插入多支U盾，点击控件版本号

    elif 1 == testRange: #验证测试
        testResult = ctrlElemObj.positiveCase()
                
    elif 2 == testRange: #无key测试
        testResult = ctrlElemObj.positiveCase_noKey()
        
    elif 3 == testRange: #多key测试
        testResult = ctrlElemObj.positiveCase_manyKey()
        
    elif 4 == testRange: #多key测试
        testResult = ctrlElemObj.positiveCase()
       
class getGetVerCases():
    def __init__(self,testCtrl,AdminKeyInfo):
        self.testCtrl=testCtrl   #控件测试页
        self.AdminKeyAlgId=AdminKeyInfo  #保护密钥信息
        self.CertRequest=GenCertGroup.GenCertClass(self.testCtrl,AdminKeyInfo)   #创建证书申请对象
      
    def positiveCase(self):
        #用例描述：插入1支U盾,点击获取控件版本号; 返回当前控件版本信息：版本号:x.x.x.x
        caseTitle="用例——插入1支U盾,点击获取控件版本号; 返回当前控件版本信息：版本号:x.x.x.x"
        caseResult=None
        e=None
        
        testResult=self.testCtrl.get_Ver()
        if CtrlVer in testResult:
            #logger.warning("响应控件版本号为:%s",testResult)
            caseResult="pass"
        else:
            caseResult="fail"
            e="实测返回："+"“"+re.sub(re.compile('\s+'),' ',testResult)+"”"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult

    def positiveCase_oneCert(self):
        # 用例描述：插入1支只有1张证书的U盾，点击获取控件版本号; 返回当前控件版本信息：版本号:x.x.x.x
        caseTitle = "用例——插入1支只有1张证书的U盾 ，点击获取控件版本号; 返回当前控件版本信息：版本号:x.x.x.x"
        caseResult = None
        e = None

        certResult = self.CertRequest.genCert_with_RSA2048_Mix()
        if certResult[1]:
            testResult = self.testCtrl.get_Ver()
            if CtrlVer in testResult:
                # logger.warning("响应控件版本号为:%s",testResult)
                caseResult = "pass"
            else:
                caseResult = "fail"
                e = "实测返回：" + "“" + re.sub(re.compile('\s+'), ' ', testResult) + "”"
        else:
            caseResult = "fail"
            e = "下证失败,结束用例执行"

        if e == None:
            logger.critical("%s || %s ", caseResult, caseTitle)
        else:
            logger.critical("%s || %s || %s ", caseResult, caseTitle, e)
        return caseResult

    def positiveCase_noKey(self):
        #用例描述：未插入U盾，点击获取控件版本号; 返回当前控件版本信息：版本号:x.x.x.x       
        caseTitle="用例——未插入U盾，点击获取控件版本号; 返回当前控件版本信息：版本号:x.x.x.x"
        caseResult=None
        e=None
        testResult=self.testCtrl.get_Ver()
        if CtrlVer in testResult:
            #logger.warning("响应控件版本号为:%s",testResult)
            caseResult="pass"
        else:
            caseResult="fail"
            e="实测返回："+"“"+re.sub(re.compile('\s+'),' ',testResult)+"”"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult
                
    def positiveCase_formatKey(self):
        #用例描述：插入1支格式化的U盾，点击获取控件版本号; 返回当前控件版本信息：版本号:x.x.x.x
        caseTitle="用例——插入1支格式化的U盾，点击获取控件版本号; 返回当前控件版本信息：版本号:x.x.x.x"
        caseResult=None
        e=None  
        flag=self.CertRequest.init_key(str_srcPin,str_srcPin)        
        if flag:
            testResult=self.testCtrl.get_Ver()
            if CtrlVer in testResult:
                #logger.warning("响应控件版本号为:%s",testResult)
                caseResult="pass"
            else:
                caseResult="fail"
                e="实测返回："+"“"+re.sub(re.compile('\s+'),' ',testResult)+"”"
        else:
            caseResult="fail"
            e="初始化失败,结束用例执行"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult
     
    def positiveCase_manyKey(self):    
        #用例描述：插入多支同款U盾，点击获取控件版本号  ;返回返回当前控件版本信息：版本号:x.x.x.x
        caseTitle="用例——插入多支同款U盾，点击获取控件版本号；返回当前控件版本信息：版本号:x.x.x.x"
        caseResult=None
        e=None
        testResult=self.testCtrl.get_Ver()
        if CtrlVer in testResult:
            #logger.warning("响应控件版本号为:%s",testResult)
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

 
    
    
    
    