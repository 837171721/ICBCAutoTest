#coding=utf-8
'''
Created on 2018.07.23 @author: SYX
'''

import re         #引入正在表达式
import operator
from  GlobalConfigure import levels,log_level
import win32api, win32con

from logTest import SysClass, LoggerClass,main_url,testUrl_Manage
conf  = LoggerClass(loglevel=levels.get(log_level), logger="TestCases_InitCardDefaultPin.py")
logger=conf.getlogger()

#错误信息列表
right_info="初始化成功"
cancel_Err=  "初始化失败:未知错误。返回码:-100 User cancel!"
ver_Err = "初始化失败:未知错误。返回码:-411 ukey version error!"
no_key_Err="初始化失败:未知错误。返回码:-102 There is no key!"
para_Err="初始化失败:-300 Failed!"

def test_InitCardDefaultPin(ctrlObj,TestingRange,AdminKeyInfo):
    testCtrl=InitCardDefaultPinCases(ctrlObj,AdminKeyInfo)  #建立类对象，打开控件测试页 
    
    if '00' != AdminKeyInfo[1]:
        testResult = testCtrl.testCtrl.initCardDefaultPin()
        testResult = re.sub(re.compile('\s+'), ' ', testResult)
        if operator.eq(ver_Err, testResult) or (operator.eq(main_url, testUrl_Manage)and operator.eq(para_Err, testResult)):
            logger.warning("接口不支持，请选择国密旧体系盾或非国密盾进行!")
            return
    testInitCardDefaultPinCase(testCtrl,TestingRange)   #测试用例集，根据测试范围定义测试强度    
    
def testInitCardDefaultPinCase(InitCardCtrl,testRange):
    #测试用例集
    if 0 == testRange:  #详细测试
        testResult = InitCardCtrl.positiveCase()
        
        testResult = InitCardCtrl.operationCase_pressC()  
        
    elif 1 == testRange: #验证测试
        testResult = InitCardCtrl.positiveCase()
                
    elif 2 == testRange: #无key测试
        testResult = InitCardCtrl.negativeCase_noKey()
        
    elif 3 == testRange: #多key测试
        a=0
        
    elif 4 == testRange: #U盾在位
        testResult = InitCardCtrl.positiveCase()
        
        testResult = InitCardCtrl.operationCase_pressC()  
        
    else:
        a=0
       
class InitCardDefaultPinCases():
    def __init__(self,testCtrl,AdminKeyInfo):
        self.testCtrl=testCtrl   #控件测试页
        self.AdminKeyAlgId=AdminKeyInfo  #保护密钥信息

    def positiveCase(self):
        #用例描述：插入1支U盾，点击初始化，返回初始化成功
        caseTitle  = "用例——插入1支U盾，点击初始化，返回初始化成功"
        caseResult = None
        e=None
        testResult=self.testCtrl.initCardDefaultPin()
        testResult=re.sub(re.compile('\s+'),' ',testResult)
        if operator.eq(right_info, testResult):
            caseResult = "pass"
        else:
            caseResult="fail"
            e="实测返回："+"“"+testResult+"”"
        if e==None:
            caseResult="pass"
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult
        
    def operationCase_pressC(self):
        #用例描述：插入1支U盾，点击保初始化，按“C键”，返回初始化失败:未知错误。返回码:-100 User cancel!
        caseTitle  = "用例——插入1支U盾,初始化等待按键状态，按取消键，返回“初始化失败:未知错误。返回码:-100 User cancel!”"
        caseResult = None
        e=None
        win32api.MessageBox(0, "确认初始化等待按键状态,按下U盾取消键", "提示框",win32con.MB_OK)
        testResult=self.testCtrl.initCardDefaultPin()
        testResult=re.sub(re.compile('\s+'),' ',testResult)
        if operator.eq(cancel_Err, testResult):
            caseResult = "pass"
        else:
            caseResult="fail"
            e="实测返回："+"“"+testResult+"”"
        if e==None:
            caseResult="pass"
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult
        
    def negativeCase_noKey(self):
        #用例描述：未插入U盾，点击初始化，返回初始化失败:未知错误。返回码:-102 There is no key!
        caseTitle  = "用例——未插入U盾,点击初始化,返回“初始化失败:未知错误。返回码:-102 There is no key!”"
        caseResult = None
        e=None
        testResult=self.testCtrl.initCardDefaultPin()
        testResult=re.sub(re.compile('\s+'),' ',testResult)
        if operator.eq(no_key_Err, testResult):
            caseResult = "pass"
        else:
            caseResult="fail"
            e="实测返回："+"“"+testResult+"”"
        if e==None:
            caseResult="pass"
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult
    
        
              
        
        