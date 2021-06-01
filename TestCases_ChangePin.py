#coding=utf-8
'''
Created on 2018.04.08 @author: SYX
Created on 2018.08.08 @author: FJQ
'''
import re
import time
import operator
import win32api,win32con
import GenCertGroup
from GlobalConfigure import levels,log_level,str_changeTitle,str_verifyTitle,str_srcPin,str_defaultPin,str_verifyPin

from logTest import SysClass, LoggerClass
conf  = LoggerClass(loglevel=levels.get(log_level), logger="TestCases_ChangePin.py")
logger=conf.getlogger()
 
#错误信息列表
right_Info='''修改口令成功'''
no_key_Err='''修改口令失败:未知错误。返回码:-102 There is no key!'''
many_key_Err='''修改口令失败:未知错误。返回码:-104 There is more than one key!'''
overtime_Err='''修改口令失败:未知错误。返回码:-105 Time out!'''
lock_Err='''修改口令失败:未知错误。返回码:-221 Pin Locked!'''
cancel_Err='''修改口令失败:未知错误。返回码:-100 User cancel!'''
oldPin_Err='''修改口令失败:未知错误。返回码:-205 PIN Error!'''

str_errPin='12121212'
str_simplePin='111111'
str_newPin='1A1A1A1A'

def test_GetChangePin(ctrlObj,TestingRange,AdminKeyInfo):
    testCtrl=ChangePinCases(ctrlObj,AdminKeyInfo)  #建立类对象，打开控件测试页 
    testChangePinGroup(testCtrl,TestingRange)   #测试用例集，根据测试范围定义测试强度

def testChangePinGroup(ctrlElemObj,testRange):
    #测试用例集
    if 0 == testRange:  #详细测试
        testResult = ctrlElemObj.positiveCase_formatKey()
 
        testResult = ctrlElemObj.positiveCase_simplePin()
 
        testResult = ctrlElemObj.positiveCase_sepecialPin()
 
        testResult = ctrlElemObj.operationCase_pressC()
 
        testResult = ctrlElemObj.operationCase_timeout()
 
        testResult = ctrlElemObj.operationCase_PinUI_PressC()
 
        testResult = ctrlElemObj.operationCase_simpleUI_PressC()
 
        testResult = ctrlElemObj.operationCase_pinRestore()
         
        testResult = ctrlElemObj.negativeCase_pinLock()
 
        testResult = ctrlElemObj.negativeCase_newPinNoMatch()
 
        testResult = ctrlElemObj.negativeCase_errOldPin()
 
        testResult = ctrlElemObj.negativeCase_shortPinLength()
 
        testResult = ctrlElemObj.negativeCase_longPinLength()
         
    elif 1 == testRange: #验证测试
        testResult = ctrlElemObj.positiveCase()
                
    elif 2 == testRange: #无key测试
        testResult = ctrlElemObj.negativeCase_noKey()
        
    elif 3 == testRange: #多key测试
        testResult = ctrlElemObj.negativeCase_manyKey()
        
    elif 4 == testRange: #多key测试
        testResult = ctrlElemObj.positiveCase()
        
        testResult = ctrlElemObj.negativeCase_errOldPin()
        
        testResult = ctrlElemObj.operationCase_PinUI_PressC()
        
        testResult = ctrlElemObj.operationCase_pressC()
       
class ChangePinCases():
    def __init__(self,testCtrl,AdminKeyInfo):
        self.testCtrl=testCtrl   #控件测试页
        self.AdminKeyAlgId=AdminKeyInfo  #保护密钥信息
        self.CertRequest=GenCertGroup.GenCertClass(self.testCtrl,AdminKeyInfo)   #创建证书申请对象

    def positiveCase(self):
        #用例描述：插入1支U盾，点击修改口令，返回“修改口令成功”
        caseTitle  = "用例——插入1支U盾，点击修改口令，返回“修改口令成功”"  
        caseResult=None
        e=None

        InitResult=self.CertRequest.init_key(str_srcPin,str_srcPin)    
        if InitResult[0]:                
            changePinResult=self.testCtrl.get_ChangePin(str_changeTitle,InitResult[1],str_newPin,str_newPin)
            if operator.eq(changePinResult,right_Info):
                caseResult="pass"                        
            else:
                caseResult="fail"
                e="实测返回："+"“"+re.sub(re.compile('\s+'),' ',changePinResult)+"”"
        else:
            caseResult="fail"
            e="初始化失败,结束用例执行"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult
               
    def positiveCase_formatKey(self):
        #用例描述：插入1支已格式化的U盾，点击修改口令，返回“修改口令成功”
        caseTitle  = "用例——插入1支已格式化的U盾，点击修改口令，返回“修改口令成功”"  
        caseResult=None
        e=None
        win32api.MessageBox(0, "确认修改密码等待按键状态,按下U盾确认键", "提示框", win32con.MB_OK)

        initResult=self.CertRequest.init_key(str_srcPin,str_srcPin)
        if initResult[0]:
            changePinResult=self.testCtrl.get_ChangePin(str_changeTitle,initResult[1],str_newPin,str_newPin)
            if operator.eq(changePinResult,right_Info):
                caseResult="pass"                        
            else:
                caseResult="fail"
                e="实测返回："+"“"+re.sub(re.compile('\s+'),' ',changePinResult)+"”"
        else:
            caseResult="fail"
            e="初始化失败,结束用例执行"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult

    def positiveCase_simplePin(self):
        #用例描述：新密码及确认新密码输入连续简单的字符后，确定,弹出密码位数过低提示框，选择是,密码修改成功
        caseTitle  = "用例——新密码及确认新密码为弱密码，期望修改密码成功"  
        caseResult=None
        e=None
        win32api.MessageBox(0, "确认修改密码等待按键状态,按下U盾确认键", "提示框", win32con.MB_OK)

        InitResult=self.CertRequest.init_key(str_srcPin,str_srcPin)    
        if InitResult[0]:                      
            changePinResult=self.testCtrl.get_ChangePin(str_changeTitle,InitResult[1],str_simplePin,str_simplePin)
            if operator.eq(changePinResult,right_Info):
                caseResult="pass"                        
            else:
                caseResult="fail"
                e="实测返回："+"“"+re.sub(re.compile('\s+'),' ',changePinResult)+"”"
        else:
            caseResult="fail"
            e="初始化失败,结束用例执行"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult

    def positiveCase_sepecialPin(self):
        #用例描述：空格作为密码输入,修改口令成功
        caseTitle  = "用例——空格或特殊字符作为密码输入,修改口令成功"  
        caseResult=None
        e=None

        win32api.MessageBox(0, "确认修改密码等待按键状态,按下U盾确认键", "提示框", win32con.MB_OK)

        InitResult=self.CertRequest.init_key(str_srcPin,str_srcPin)    
        if InitResult[0]:          
            changePinResult=self.testCtrl.get_ChangePin(str_changeTitle,InitResult[1],' $@#% &*',' $@#% &*')
            if operator.eq(changePinResult,right_Info):
                caseResult="pass"                        
            else:
                caseResult="fail"
                e="实测返回："+"“"+re.sub(re.compile('\s+'),' ',changePinResult)+"”"
        else:
            caseResult="fail"
            e="初始化失败,结束用例执行"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult
        
    def operationCase_pressC(self):
        #用例描述：弹出修改密码按键提示框时，按下Key的C键,返回“修改口令失败:未知错误。返回码:-100 User cancel!”错误提示
        caseTitle  = "用例——修改密码等待按键状态,按下键盘Esc/空格/回车键或U盾上下翻页键,应无反应,U盾保持等待按键状态！按下U盾取消键,返回“修改口令失败:未知错误。返回码:-100 User cancel!”错误提示"  
        caseResult=None
        e=None
        win32api.MessageBox(0, "确认修改密码等待按键状态,按下键盘Esc/空格/回车键或U盾上下翻页键,应无反应,U盾保持等待按键状态！按下U盾取消键，取消操作！", "提示框", win32con.MB_OK)

        InitResult=self.CertRequest.init_key(str_srcPin,str_srcPin)
        if InitResult[0]:
            time.sleep(0.2)
            changePinResult=self.testCtrl.get_ChangePin(str_changeTitle,InitResult[1],str_newPin,str_newPin)
            changePinResult=re.sub(re.compile('\s+'),' ',changePinResult)
            if operator.eq(changePinResult,cancel_Err):
                caseResult="pass"                        
            else:
                caseResult="fail"
                e="实测返回："+"“"+changePinResult+"”"
        else:
            caseResult="fail"
            e="初始化失败,结束用例执行"    
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult
    
    def operationCase_timeout(self):
        #用例描述：弹出修改密码按键提示框时，不操作Key，等待15Min,返回“修改口令失败:未知错误。返回码:-105  Time out!”
        caseTitle  = "用例——弹出修改密码按键提示框时，不操作Key，等待15Min,期望返回-105  Time out!"  
        caseResult=None
        e=None
        win32api.MessageBox(0, "修改密码等待按键状态时，不操作Key，等待15Min", "提示框", win32con.MB_OK)

        InitResult=self.CertRequest.init_key(str_srcPin,str_srcPin)    
        if InitResult[0]:
            changePinResult=self.testCtrl.get_ChangePin(str_changeTitle,InitResult[1],str_newPin,str_newPin)
            changePinResult=re.sub(re.compile('\s+'),' ',changePinResult)
            if operator.eq(changePinResult,overtime_Err):
                caseResult="pass"                        
            else:
                caseResult="fail"
                e="实测返回："+"“"+changePinResult+"”"
        else:
            caseResult="fail"
            e="初始化失败,结束用例执行"    
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult
    
    def operationCase_PinUI_PressC(self):
        #用例描述：CSP弹出修改U盾密码对话框时，点击取消,返回“修改口令失败:未知错误。返回码:-100 User cancel!”错误提示
        caseTitle  = "用例——CSP弹出修改U盾密码对话框时，点击UI弹框上的取消，期望返回-100 User cancel!"  
        caseResult=None
        e=None  
        InitResult=self.CertRequest.init_key(str_srcPin,str_srcPin)    
        if InitResult[0]:     
            changePinResult=self.testCtrl.get_ChangePin(str_changeTitle,InitResult[1],str_newPin,str_newPin,1,0,str_verifyTitle)
            changePinResult=re.sub(re.compile('\s+'),' ',changePinResult)
            if operator.eq(changePinResult,cancel_Err):             
                caseResult="pass"                        
            else:
                caseResult="fail"
                e="实测返回："+"“"+changePinResult+"”"
        else:
            caseResult="fail"
            e="初始化失败,结束用例执行"    
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult
       
    def operationCase_simpleUI_PressC(self):
        #用例描述：弹出密码位数过低提示框，选择否,返回密码输入界面，要求重新输入新密码及新密码确认
        caseTitle  = "用例——弹出密码位数过低提示框，选择否,请确认返回密码输入界面等待重新输入，为方便测试关闭UI框结束本次操作"  
        caseResult=None
        e=None 
        InitResult=self.CertRequest.init_key(str_srcPin,str_srcPin)    
        if InitResult[0]:     
            changePinResult=self.testCtrl.get_ChangePin(str_changeTitle,InitResult[1],str_simplePin,str_simplePin,0,1,str_verifyTitle)
            changePinResult=re.sub(re.compile('\s+'),' ',changePinResult)
            if operator.eq(changePinResult,cancel_Err): 
                caseResult="pass"                        
            else:
                caseResult="fail"
                e="实测返回："+"“"+changePinResult+"”"
        else:
            caseResult="fail"
            e="初始化失败,结束用例执行"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult
    
    def negativeCase_newPinNoMatch(self):
        #用例描述：新密码和确认密码不一致,弹出用户提示“两次输入的新密码不一致，请重新输入！
        caseTitle  = "用例——新密码和确认密码不一致，弹出输入密码不一致错误提示框，为方便测试关闭UI框结束本次操作"  
        caseResult=None
        e=None
        InitResult=self.CertRequest.init_key(str_srcPin,str_srcPin)    
        if InitResult[0]:     
            changePinResult=self.testCtrl.get_ChangePin(str_changeTitle,InitResult[1],str_newPin,str_errPin)
            changePinResult=re.sub(re.compile('\s+'),' ',changePinResult)
            if operator.eq(changePinResult,cancel_Err): 
                caseResult="pass"                       
            else:
                caseResult="fail"
                e="实测返回："+"“"+changePinResult+"”"
        else:
            caseResult="fail"
            e="初始化失败,结束用例执行"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult
    
    def negativeCase_errOldPin(self):
        #用例描述：旧密码输入错误，输入符合要求的新密码,返回“修改口令失败:未知错误。返回码:-205 PIN Error!”错误提示
        caseTitle  = "用例——错误原密码，返回:-205 PIN Error!"  
        caseResult=None
        e=None
        InitResult=self.CertRequest.init_key(str_srcPin,str_srcPin)    
        if InitResult[0]:     
            changePinResult=self.testCtrl.get_ChangePin(str_changeTitle,str_errPin,str_newPin,str_newPin)
            changePinResult=re.sub(re.compile('\s+'),' ',changePinResult)
            if operator.eq(changePinResult,oldPin_Err):
                caseResult="pass"                        
            else:
                caseResult="fail"
                e="实测返回："+"“"+changePinResult+"”"
        else:
            caseResult="fail"
            e="初始化失败,结束用例执行"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult
    
    def negativeCase_pinLock(self):
        #用例描述：连续输入错误密码至锁死
        caseTitle  = "用例——连续输入错误密码至锁死"  
        caseResult=None
        e=None
        win32api.MessageBox(0, "确认修改密码等待按键状态,按下U盾确认键", "提示框", win32con.MB_OK)

        InitResult=self.CertRequest.init_key(str_srcPin,str_srcPin)    
        if InitResult[0]:  
            count=0
            changePinResult=''
            while count < 7 :   
                changePinResult=self.testCtrl.get_ChangePin(str_changeTitle,str_errPin,str_newPin,str_newPin)
                count += 1
            changePinResult=re.sub(re.compile('\s+'),' ',changePinResult) 
            if operator.eq(changePinResult,lock_Err):
                caseResult="pass"                        
            else:
                caseResult="fail"
                e="实测返回："+"“"+changePinResult+"”"
        else:
            caseResult="fail"
            e="初始化失败,结束用例执行"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult  
    
    def operationCase_pinRestore(self):
        #用例描述：连续5次输入错误密码，最后1次输入正确密码,修改口令成功，密码重试次数恢复为6次
        caseTitle  = "用例——连续5次输入错误密码，最后1次输入正确密码，密码重试次数恢复为6次"  
        caseResult=None
        e=None
        win32api.MessageBox(0, "确认修改密码等待按键状态,按下U盾确认键", "提示框", win32con.MB_OK)

        InitResult=self.CertRequest.init_key(str_srcPin,str_srcPin)    
        if InitResult[0]:  
            count=0
            changePinResult=''
            while count < 5 :            
                changePinResult=self.testCtrl.get_ChangePin(str_changeTitle,str_errPin,str_newPin,str_newPin)
                count += 1               
            changePinResult=self.testCtrl.get_ChangePin(str_changeTitle,InitResult[1],str_newPin,str_newPin)
            if operator.eq(changePinResult,right_Info): 
                changePinResult=self.testCtrl.get_ChangePin(str_changeTitle,str_errPin,str_newPin,str_newPin)            
                changePinResult=re.sub(re.compile('\s+'),' ',changePinResult)
                if operator.eq(changePinResult,oldPin_Err):
                    caseResult="pass"
                else:
                    caseResult="fail"
                    e="实测返回："+"“"+changePinResult+"”"
        else:
            caseResult="fail"
            e="初始化失败,结束用例执行"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult
    
    def negativeCase_shortPinLength(self):
        #用例描述：密码边界测试（6-30字符）：输入少于6字符的密码,输入多余30字符的密码
        caseTitle  = "用例——密码边界测试（6-30字符）：输入少于6字符的密码,无法修改密码。为方便测试关闭UI框结束本次操作"  
        caseResult=None
        e=None
        InitResult=self.CertRequest.init_key(str_srcPin,str_srcPin)
        if InitResult[0]:           
            #输入少于6字符的密码
            changePinResult=self.testCtrl.get_ChangePin(str_changeTitle,InitResult[1],'11111','11111')
            changePinResult=re.sub(re.compile('\s+'),' ',changePinResult)
            if operator.eq(changePinResult,cancel_Err): 
                caseResult="pass"                        
            else:
                caseResult="fail"
                e="实测返回："+"“"+changePinResult+"”"
        else:
            caseResult="fail"
            e="初始化失败,结束用例执行"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult

    def negativeCase_longPinLength(self):
        #用例描述：密码边界测试（6-30字符）：输入多余30字符的密码
        caseTitle  = "用例——密码边界测试（6-30字符）：输入多余30字符的密码,密码框仅截取前30个字符，修改密码成功"  
        caseResult=None
        e=None
        InitResult=self.CertRequest.init_key(str_srcPin,str_srcPin)
        if InitResult[0]:                     
            #输入多余30字符的密码
            longPin='1234567890123456789012345678901'
            longPin1='123456789012345678901234567890'
            changePinResult=self.testCtrl.get_ChangePin(str_changeTitle,InitResult[1],longPin,longPin)
            if operator.eq(changePinResult,right_Info): 
                changePinResult=self.testCtrl.get_ChangePin(str_changeTitle,longPin1,str_defaultPin,str_verifyPin)
                changePinResult=re.sub(re.compile('\s+'), ' ', changePinResult)
                if operator.eq(changePinResult,right_Info): 
                    caseResult="pass"                        
                else:
                    caseResult="fail"
                    e="实测返回："+"“"+changePinResult+"”"
        else:
            caseResult="fail"
            e="初始化失败,结束用例执行"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult

    def negativeCase_noKey(self):
        #用例描述：未插入U盾，点击修改口令，返回“修改口令失败:未知错误。返回码:-102 There is no key!”错误提示
        caseTitle  = "用例——未插入U盾,点击修改口令,返回“修改口令失败:未知错误。返回码:-102 There is no key!”错误提示"
        caseResult=None
        e=None
        testResult=self.testCtrl.get_ChangePin(str_changeTitle,str_srcPin,str_defaultPin,str_verifyPin)
        testResult=re.sub(re.compile('\s+'),' ',testResult)
        if operator.eq(no_key_Err,testResult):
            caseResult="pass"                        
        else:
            caseResult="fail"
            e="实测返回："+"“"+testResult+"”"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult
        
    def negativeCase_manyKey(self):
        #用例描述：插入多个同款U盾，点击修改口令，返回“修改口令失败:未知错误。返回码:-104 There is more than one key!”错误提示
        caseTitle  = "用例——插入多个同款U盾"  
        caseResult=None
        e=None
      
        testResult=self.testCtrl.get_ChangePin(str_changeTitle,str_srcPin,str_defaultPin,str_verifyPin)
        testResult=re.sub(re.compile('\s+'),' ',testResult)
        if operator.eq(many_key_Err,testResult):
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
    def negativeCase_operation(self):
        #用例描述：插入多个同款U盾，拔出多余U盾，只留1支在位，点击修改口令，修改口令成功”
        caseTitle  = "用例——插入多个同款U盾，拔出多余U盾，只留1支在位"  
        e=None      
        self.testCtrl.get_InitCard(str_title,str_srcPin,str_srcPin)
        testResult=self.testCtrl.get_ChangePin(str_changeTitle,str_srcPin,str_defaultPin,str_verifyPin)
        testResult=re.sub(re.compile('\s+'),' ',testResult)
        if right_Info == testResult:
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
#########################
#开始测试
#########################
    
