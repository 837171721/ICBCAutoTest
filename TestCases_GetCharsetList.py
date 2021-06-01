#coding=utf-8
'''
Created on 2018.04.09 @author: SYX
'''
import re
import operator
import GenCertGroup
from GlobalConfigure import levels, log_level,str_srcPin

from logTest import SysClass, LoggerClass
conf  = LoggerClass(loglevel=levels.get(log_level), logger="TestCases_GetCharsetList.py")
logger=conf.getlogger()

#错误信息列表
no_key_Err="获取字符集失败:未知错误。返回码:-102 There is no key!"
many_key_Err="获取字符集失败:未知错误。返回码:-104 There is more than one key!"
right_info='''UTF-8||GBK||GB18030'''

def test_GetCharsetList(ctrlObj,TestingRange,AdminKeyInfo):
    #调用流程
    testCtrl=GetCharsetListCases(ctrlObj,AdminKeyInfo)  #建立类对象，打开控件测试页 
    testGetCharsetListGroup(testCtrl,TestingRange)   #测试用例集，根据测试范围定义测试强度

def testGetCharsetListGroup(ctrlObj,testRange):
    #测试用例集
    if 0 == testRange:  #详细测试
        testResult = ctrlObj.positiveCase_noCert()

        testResult = ctrlObj.negativeCase_noKey()

    elif 1 == testRange: #验证测试
        testResult = ctrlObj.positiveCase()
        
    elif 2 == testRange: #无key测试
        testResult = ctrlObj.negativeCase_noKey()
        
    elif 3 == testRange: #多key测试
        testResult = ctrlObj.negativeCase_manyKey()
        
    elif 4 == testRange:
        testResult = ctrlObj.positiveCase()
        
class GetCharsetListCases():
    def __init__(self,testCtrl,AdminKeyInfo):
        self.testCtrl=testCtrl   #控件测试页
        self.AdminKeyAlgId=AdminKeyInfo  #保护密钥信息
        self.CertRequest=GenCertGroup.GenCertClass(self.testCtrl,AdminKeyInfo)   #创建证书申请对象
    
    def positiveCase(self):
        #用例描述：插入1支U盾，点击获取支持的字符集,返回支持的字符集“UTF-8||GBK||GB18030”
        caseTitle="用例——插入1支U盾，点击获取支持的字符集，期望返回支持的字符集"
        caseResult = None
        e = None       
        CharsetListResult=self.testCtrl.get_CharsetList()
        if right_info in CharsetListResult:
            logger.warning("响应字符集为%s:",CharsetListResult)
            caseResult="pass"
        else:
            caseResult="fail"
            e="实测返回："+"“"+re.sub(re.compile('\s+'),' ',CharsetListResult)+"”"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult 
            
    def negativeCase_noKey(self):
        #用例描述：未插入U盾，点击获取支持的字符集,返回“获取字符集失败:未知错误。返回码:-102 There is no key!”错误提示
        caseTitle="用例——未插入U盾，点击获取支持的字符集"
        caseResult = None
        e = None
        
        caseResult=self.testCtrl.get_CharsetList()
        caseResult=re.sub(re.compile('\s+'),' ',caseResult)
        if operator.eq(caseResult,no_key_Err):
            #logger.warning("响应字符集为%s:",caseResult)
            caseResult="pass"
        else:
            caseResult="fail"
            e="实测返回："+"“"+caseResult+"”"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult    

    def positiveCase_noCert(self):
        #用例描述：插入1支已格式化的U盾，点击获取支持的字符集,返回支持的字符集“UTF-8||GBK||GB18030”
        caseTitle="用例——插入1支已格式化的U盾，点击获取支持的字符集"
        caseResult = None
        e = None       
        
        initResult=self.CertRequest.init_key(str_srcPin,str_srcPin)
        if initResult[0]:
            caseResult=self.testCtrl.get_CharsetList()
            #caseResult=re.sub(re.compile('\s+'),' ',caseResult)
            if right_info in caseResult:
                #logger.warning("获取字符集为:",caseResult)
                caseResult="pass"
            else:
                caseResult="fail"
                e="实测返回："+"“"+re.sub(re.compile('\s+'),' ',caseResult)+"”"
        else:
            caseResult = "fail"
            e = "初始化失败，结束用例执行"

        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult    

    def positiveCase_oneCert(self):
        #用例描述：插入1支非格式化的U盾，点击获取支持的字符集,返回支持的字符集“UTF-8||GBK||GB18030”
        caseTitle="用例——插入1支非格式化的U盾，点击获取支持的字符集"
        caseResult = None
        e = None         
        certResult=self.CertRequest.genCert_with_RSA1024_Mix()
        if certResult[1]:
            caseResult=self.testCtrl.get_CharsetList()
            #caseResult=re.sub(re.compile('\s+'),' ',caseResult)
            if right_info in caseResult:
                #logger.warning("获取字符集为:",caseResult)
                caseResult="pass"
            else:
                caseResult="fail"
                e="实测返回："+"“"+re.sub(re.compile('\s+'),' ',caseResult)+"”"
        else:
            caseResult = "fail"
            e = "下证失败，结束用例执行"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult    

    def negativeCase_manyKey(self):
        #用例描述：插入多支同款U盾，点击获取支持的字符集，返回“获取字符集失败:未知错误。返回码:-104 There is more than one key!”错误提示
        caseTitle="用例——插入多支同款U盾，点击获取支持的字符集"
        caseResult = None
        e = None   

        caseResult=self.testCtrl.get_CharsetList()
        caseResult=re.sub(re.compile('\s+'),' ',caseResult)
        if operator.eq(caseResult,many_key_Err):
            #logger.warning("获取字符集为:",caseResult)
            caseResult="pass"
        else:
            caseResult="fail"
            e="实测返回："+"“"+caseResult+"”"

        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult           
        
#########################
#开始测试
#########################  
