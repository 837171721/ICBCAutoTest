#coding=utf-8
'''
Created on 2018.03.18 @author: ys
'''
import re         #引入正在表达式
import operator
from  GlobalConfigure import levels,log_level

from logTest import SysClass, LoggerClass,CardNum
conf  = LoggerClass(loglevel=levels.get(log_level), logger="TestCases_GetMediaID.py")
logger=conf.getlogger()

#错误信息列表
no_key_Err=  "获取介质号失败:未知错误。返回码:-102 There is no key!"
many_key_Err="获取介质号失败:未知错误。返回码:-104 There is more than one key!"

def test_GetMediaId(ctrlObj,TestingRange):
    testCtrl=GetMediaIdCases(ctrlObj)  #建立类对象，打开控件测试页 
    testGetMediaIdGroup(testCtrl,TestingRange)   #测试用例集，根据测试范围定义测试强度
    
def testGetMediaIdGroup(MediaIdCtrl,testRange):
    #测试用例集
    if 0 == testRange:  #详细测试
        MediaIdCtrl.positiveCase()
        #MediaIdCtrl.nagativeCase_noKey()
        #MediaIdCtrl.nagativeCase_manyKey()    
        #MediaIdCtrl.nagativeCase_operation()
        
    elif 1 == testRange: #验证测试
        MediaIdCtrl.positiveCase()
                   
    elif 2 == testRange: #无key测试
        MediaIdCtrl.negativeCase_noKey()
        
    elif 3 == testRange: #多key测试
        MediaIdCtrl.negativeCase_manyKey()
        
    elif 4 == testRange: #基础测试
        MediaIdCtrl.positiveCase()
       
class GetMediaIdCases():
    def __init__(self,testCtrl):
        self.testCtrl=testCtrl   #控件测试页 
    
    def positiveCase(self):
        #用例描述：插入1支U盾，点击获取介质号，期望返回U盾序列号
        caseTitle  = "用例——插入1支U盾，点击获取介质号，期望返回U盾序列号"  
        caseResult = None
        e=None
        MediaIdResult=self.testCtrl.get_MediaId()
        if CardNum == MediaIdResult or (MediaIdResult.isdigit() and 10 == len(MediaIdResult)):
            caseResult="pass"                        
        else:
            caseResult="fail"
            e="实测返回："+"“"+re.sub(re.compile('\s+'),' ',MediaIdResult)+"”"

        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult
   
    def negativeCase_noKey(self):
        #用例描述：未插入U盾，点击获取介质号，期望返回获取介质号失败:未知错误。返回码:-102 There is no key!
        caseTitle  = "用例——未插入U盾，点击获取介质号，期望返回获取介质号失败:未知错误。返回码:-102 There is no key!"
        caseResult = None
        e=None

        MediaIdResult=self.testCtrl.get_MediaId()
        MediaIdResult=re.sub(re.compile('\s+'),' ',MediaIdResult)
        if operator.eq(no_key_Err,MediaIdResult):
            caseResult="pass"
        else:
            caseResult="fail"
            e="实测返回："+"“"+MediaIdResult+"”"

        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult            
    
    def negativeCase_manyKey(self):
        #用例描述：插入多支同款U盾，点击获取介质号，期望返回获取介质号失败:未知错误。返回码:-104 There is more than one key!!
        caseTitle="用例——插入多支同款U盾，点击获取介质号，期望返回获取介质号失败:未知错误。返回码:-104 There is more than one key"
        caseResult = None
        e=None
        MediaIdResult=self.testCtrl.get_MediaId()
        MediaIdResult=re.sub(re.compile('\s+'),' ',MediaIdResult)
        if operator.eq(many_key_Err,MediaIdResult):
            caseResult="pass"                        
        else:
            caseResult="fail"
            e="实测返回："+"“"+MediaIdResult+"”"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult

    def negativeCase_operation(self):
        #用例描述：插入多支同款U盾，拔出多余U盾，只留1支在位，点击获取介质号,期望返回U盾序列号
        caseTitle="用例——插入多支同款U盾，拔出多余U盾，只留1支在位，点击获取介质号,期望返回U盾序列号"
        caseResult = None
        e=None       
        #if 0 == TestingType:    
            #win32api.MessageBox(0, "请确认已接入多支同款U盾，并拔出多余U盾，只留一支测试U盾在位", "提示框",win32con.MB_OK)  
        MediaIdResult=self.testCtrl.get_MediaId()
        if CardNum == MediaIdResult or (MediaIdResult.isdigit() and 10 == len(MediaIdResult)):
            caseResult="pass" 
        else:
            caseResult="fail"                        
            e="实测返回："+"“"+MediaIdResult+"”"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult        

#########################
#开始测试
#########################
