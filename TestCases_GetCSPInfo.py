# coding=utf-8
'''
Created on 2018.08.09 @author: ys

'''
import re
import random
import operator
from GlobalConfigure import CSPVer,DriverVer,levels, log_level,CardNum

from logTest import SysClass, LoggerClass
conf = LoggerClass(loglevel=levels.get(log_level), logger="TestCases_GetCSPInfo.py")
logger = conf.getlogger()

no_key_Err = '''获取CSP信息失败:未知错误。返回码:-102 There is no key!'''
many_key_Err='''获取CSP信息失败:未知错误。返回码:-104 There is more than one key!'''
param_Err= '''获取CSP信息失败:未知错误。返回码:-304 Failed Param!'''

def test_GetCSPInfo(ctrlObj,TestingRange):
    #调用流程
    testCtrl=GetCSPInfoCases(ctrlObj)  #建立类对象，打开控件测试页 
    testGetCSPInfoGroup(testCtrl,TestingRange)   #测试用例集，根据测试范围定义测试强度

def testGetCSPInfoGroup(ctrlElemObj, testRange):
    if 0 == testRange:
        caseResult = ctrlElemObj.positiveCase_oneKey_validParaChoice()

        caseResult = ctrlElemObj.nagetiveCase_oneKey_errParaChoice()

        #caseResult = ctrlElemObj.nagetiveCase_manyKey()

        #caseResult = ctrlElemObj.nagetiveCase_operation()

    elif 1 == testRange:
        caseResult = ctrlElemObj.postiveCase()

    elif 2 == testRange:
        caseResult = ctrlElemObj.nagetiveCase_noKey_voidParaChoice()

        caseResult = ctrlElemObj.nagetiveCase_noKey_errParaChoice()
    
    elif 3 == testRange:
        caseResult = ctrlElemObj.nagetiveCase_manyKey()
        
    elif 4 == testRange:
        caseResult = ctrlElemObj.postiveCase()


class GetCSPInfoCases():
    def __init__(self, testCtrl):
        self.testCtrl=testCtrl   #控件测试页
       
    def postiveCase(self):
        #用例描述：插入1支U盾，点击获取CSP信息，返回M&W CSP for ICBC V5||x.x.x.x
        caseTitle = "用例——插入1支U盾，点击获取CSP信息，返回M&W CSP for ICBC V5||x.x.x.x"
        caseResult=None
        e = None        
        strMediaID = self.testCtrl.get_MediaId()
        if CardNum == strMediaID or (strMediaID.isdigit() and 10 == len(strMediaID)):
            testResult = self.testCtrl.get_CspInfoC(strMediaID)
            if (CSPVer in testResult) and (DriverVer in testResult) and testResult.count("||"):
                #logger.warning("响应CSP信息为%s:",testResult)
                caseResult = "pass"
            else:
                caseResult = "fail"
                e = "实测返回：" + "“" + re.sub(re.compile('\s+'), ' ', testResult) + "”"
        else:
            caseResult = "fail"
            e = "获取介质号失败，结束用例执行"
            
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult

    def positiveCase_oneKey_validParaChoice(self):
        #用例描述：插入1支U盾，输入正确MediaID（读取介质号），点击获取CSP信息返回M&W CSP for ICBC V5||x.x.x.x
        caseTitle= "用例——插入1支U盾，输入正确MediaID（读取介质号），点击获取CSP信息返回M&W CSP for ICBC V5||x.x.x.x"
        e= None
        strMediaID = self.testCtrl.get_MediaId()
        if CardNum == strMediaID or (strMediaID.isdigit() and 10 == len(strMediaID)):
            testResult = self.testCtrl.get_CspInfoC(strMediaID)
            if (CSPVer in testResult) and (DriverVer in testResult) and testResult.count("||"):
                #logger.warning("响应CSP信息为%s:",testResult)
                caseResult = "pass"
            else:
                caseResult = "fail"
                e = "实测返回：" + "“" + re.sub(re.compile('\s+'), ' ', testResult) + "”"
        else:
            caseResult = "fail"
            e = "获取介质号失败，结束用例执行"
            
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult
    
    def nagetiveCase_oneKey_errParaChoice(self):
        #用例描述：插入U盾，任意输入MediaID，点击获取CSP信息,获取CSP信息失败:未知错误。返回码:-304 Failed Param!
        caseTitle = "插入U盾，任意输入MediaID，点击获取CSP信息,获取CSP信息失败:未知错误。返回码:-304 Failed Param!"
        e = None
        strMediaID=str(random.randint(0,6990000000))
        testResult = self.testCtrl.get_CspInfoC(strMediaID)
        testResult=re.sub(re.compile('\s+'), ' ', testResult)
        if operator.eq(testResult,param_Err):
            #logger.warning("响应CSP信息为%s:",testResult)
            caseResult = "pass"
        else:
            caseResult = "fail"
            e = "实测返回："  + "“" + testResult + "”"
        
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult

    def nagetiveCase_noKey_voidParaChoice(self):
        #用例描述：未插入U盾，不输入MediaID，点击获取CSP信息,期望返回“获取CSP信息失败:未知错误。返回码:-304 Failed Param!       
        caseTitle="未插入U盾，不输入MediaID，点击获取CSP信息,期望返回“获取CSP信息失败:未知错误。返回码:-304 Failed Param!"
        caseResult=None
        e = None
        
        testResult=self.testCtrl.get_CspInfoC(None)
        testResult=re.sub(re.compile('\s+'), ' ', testResult)
        if operator.eq(testResult,param_Err):
            caseResult = "pass"
        else:
            caseResult = "fail"
            e = "实测返回：" + "“" + testResult + "”"
        
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult

    def nagetiveCase_noKey_errParaChoice(self):
        #用例描述：未插入U盾，任意输入MediaID，点击获取CSP信息 获取CSP信息失败:未知错误。返回码:-102 There is no key
        caseTitle = "未插入U盾，任意输入MediaID，点击获取CSP信息 获取CSP信息失败:未知错误。返回码:-102 There is no key"
        caseResult=None       
        e = None
        
        strMediaID=str(random.randint(0,6990000000))
        testResult = self.testCtrl.get_CspInfoC(strMediaID)
        testResult=re.sub(re.compile('\s+'), ' ', testResult)        
        if operator.eq(testResult,no_key_Err):
            caseResult = "pass"
        else:
            caseResult = "fail"
            e = "实测返回：" + "“" +  testResult + "”"
        
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult
    
    def nagetiveCase_manyKey(self):
        #用例描述：插入多支同款U盾，输入MediaID，点击获取CSP信息返回“获取CSP信息失败:未知错误。返回码:-104 There is more than one key!
        caseTitle="插入多支同款U盾，输入MediaID，点击获取CSP信息返回“获取CSP信息失败:未知错误。返回码:-104 There is more than one key!"
        caseResult=None 
        e= None
        strMediaID=str(random.randint(0,6990000000))
        testResult = self.testCtrl.get_CspInfoC(strMediaID)
        testResult=re.sub(re.compile('\s+'), ' ', testResult)
        if operator.eq(testResult,many_key_Err):
            caseResult = "pass"
        else:
            caseResult = "fail"
            e = "实测返回：" + "“" + testResult + "”"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult

    def nagetiveCase_operation(self):
        #用例描述：插入多支同款U盾，拔出多余U盾，只留1支在位，点击获取CSP信息 返回M&W CSP for ICBC V5||x.x.x.x
        caseTitle="插入多支同款U盾，拔出多余U盾，只留1支在位，点击获取CSP信息 返回M&W CSP for ICBC V5||x.x.x.x"
        e = None
        strMediaID = re.findall('(-?[\d]+)', self.testCtrl.get_MediaId())
        if (no_key_Err != strMediaID) and (many_key_Err != strMediaID):
            caseResult = self.testCtrl.get_CspInfoC(strMediaID)
        if None != (re.match(CSPVer, caseResult).span()):
            caseResult = "pass"
        else:
            caseResult = "fail"
            e = "实测返回：" + "“" + re.sub(re.compile('\s+'), ' ', caseResult) + "”"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult

