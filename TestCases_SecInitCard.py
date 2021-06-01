# coding=utf-8
'''
Created on 2018.08.01 @author: SYX
Created on 2018.08.18 @author: YS
'''

import re  # 引入正在表达式
import random
import string
import operator
import win32api
import win32con
import GenCertGroup
from GlobalConfigure import levels,log_level,str_srcPin,CardNum,testUrl_GM_User,str_changeTitle

from logTest import SysClass, LoggerClass
conf = LoggerClass(loglevel=levels.get(log_level), logger="TestCases_SecInitCard.py")
logger = conf.getlogger()

# 错误信息列表
right_info = "安全初始化成功"
param_Err = '''安全初始化失败:未知错误。返回码:-304 Failed Param!'''
decoding_Err = '''安全初始化失败:未知错误。返回码:-401 Base64 decoding failed!'''
cancel_Err = '''安全初始化失败:未知错误。返回码:-100 User cancel!'''
time_out_Err = '''安全初始化失败:未知错误。返回码:-105 Time out!'''
no_key_Err="初始化失败:未知错误。返回码:-102 There is no key!"
many_key_Err = '''安全初始化失败:未知错误。返回码:-104 There is more than one key!'''
unknown_Err = '''安全初始化失败:未知错误。返回码:-300 unKnown error!'''
lock_Err = '''修改口令失败:未知错误。返回码:-221 Pin Locked!'''

str_errPin='12121212'
str_newPin='1A1A1A1A'
initData="FkwVXp3I9vYVYfXYzg4H+HUXEwovNgNgFB400ab8Zg=="

def test_SecInitCard(ctrlObj, TestingRange, AdminKeyInfo):
    testCtrl = SecInitCardCases(ctrlObj, AdminKeyInfo)  # 建立类对象，打开控件测试页
    if AdminKeyInfo[1]=='00':
        testResult = testCtrl.testCtrl.get_SecInitCard(AdminKeyInfo,CardNum,initData,False)
        testResult = re.sub(re.compile('\s+'), ' ', testResult)
        if operator.eq(unknown_Err, testResult):
            logger.warning("接口不支持，请选择国密新体系盾进行!")
            return      
    testSecInitCardCase(testCtrl, TestingRange)  # 测试用例集，根据测试范围定义测试强度

def testSecInitCardCase(SecInitCardCtrl, testRange):
    # 测试用例集
    if 0 == testRange:  # 详细测试
        #testResult = SecInitCardCtrl.positiveCase()

        testResult = SecInitCardCtrl.negativeCase_oneKey_voidParaChoice()

        testResult = SecInitCardCtrl.negativeCase_oneKey_errParaChoice()

        testResult = SecInitCardCtrl.operationCase_pressC()

        testResult = SecInitCardCtrl.operationCase_timeout()

        testResult = SecInitCardCtrl.operationCase_outKey()  # 10、拔出key

        testResult = SecInitCardCtrl.operationCase_pinLock()

    elif 1 == testRange:  # 验证测试
        testResult = SecInitCardCtrl.positiveCase()

    elif 2 == testRange:  # 无key测试
        testResult = SecInitCardCtrl.negativeCase_noKey_voidParaChoice()
        
        testResult = SecInitCardCtrl.negativeCase_noKey_errParaChoice()

    elif 3 == testRange:  # 多key测试
        testResult = SecInitCardCtrl.negativeCase_manyKey()
        
    elif 4 == testRange: #U盾在位
        testResult = SecInitCardCtrl.positiveCase()

    else:
        a = 0

class SecInitCardCases():
    def __init__(self, testCtrl, AdminKeyInfo):
        self.testCtrl = testCtrl  # 控件测试页
        self.AdminKeyAlgId = AdminKeyInfo  # 保护密钥信息
        self.CertRequest = GenCertGroup.GenCertClass(self.testCtrl, AdminKeyInfo)  # 创建证书申请对象

    def positiveCase(self):
        # 用例描述：插入1支初始化的U盾，输入正确的InitData参数后，点击安全初始化期望返回:1.弹出按键提示框，提示用户初始化U盾，请按键确认。2.按下U盾的OK返回“安全初始化成功”提示
        caseTitle = "用例——插入1支U盾，输入正确的InitData参数后，点击安全初始化,期望返回成功"
        caseResult = None
        e = None
        initResult=self.CertRequest.init_key(str_srcPin, str_srcPin)
        if initResult[0]:
            caseResult = "pass"
        else:
            caseResult = "fail"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult

    def negativeCase_noKey_voidParaChoice(self):
        # 用例描述：未插入U盾，InitData参数栏不输入后，点击安全初始化。期望返回“安全初始化失败:未知错误。返回码:-304Failed Param!”；
        caseTitle = "用例——未插入U盾,InitData参数栏不输入后,安全初始化期望返回“安全初始化失败:未知错误。返回码:-304 Failed Param!或-102 There is no key!(实测返回)”"
        caseResult = None
        e = None
        testResult = self.testCtrl.get_SecInitCard(self.AdminKeyAlgId[1], CardNum, None, False)
        testResult = re.sub(re.compile('\s+'), ' ', testResult)
        if operator.eq(param_Err, testResult) or operator.eq(no_key_Err, testResult):  #-102是实际测试返回结果，-304是测试大纲中结果
            caseResult = "pass"
        else:
            caseResult = "fail"
            e = "实测返回：" + "“" + testResult + "”"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult

    def negativeCase_noKey_errParaChoice(self):
        # 用例描述：未插入U盾，InitData参数栏任意输入，点击安全初始化。期望返回“安全初始化失败:未知错误。返回码:-401 Base64 decoding failed!”
        caseTitle = "用例——未插入U盾,InitData参数栏任意输入,安全初始化期望返回“安全初始化失败:未知错误。返回码:-401 Base64 decoding failed! 或-102 There is no key!(实测返回)”"
        caseResult = None
        e = None
        
        initDataLen = random.randint(0,50)
        initDataRandom=''.join(random.sample(string.ascii_letters + string.digits,initDataLen)).replace(" ","")

        testResult = self.testCtrl.get_SecInitCard(self.AdminKeyAlgId[1], CardNum, initDataRandom, False)
        testResult = re.sub(re.compile('\s+'), ' ', testResult)
        if operator.eq(decoding_Err, testResult) or operator.eq(no_key_Err, testResult):  #-102是实际测试返回结果，-401是测试大纲中结果
            caseResult = "pass"
        else:
            caseResult = "fail"
            e = "实测返回：" + "“" + testResult + "”"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult

    def negativeCase_oneKey_voidParaChoice(self):
        # 用例描述：插入1支U盾，InitData参数栏不输入后，点击安全初始化。期望返回“安全初始化失败:未知错误。返回码:-304 Failed Param!”
        caseTitle = "用例——插入1支U盾,，InitData参数栏不输入数据,安全初始化期望返回“安全初始化失败:未知错误。返回码:-304 Failed Param!”"
        caseResult = None
        e = None
        testResult = self.testCtrl.get_SecInitCard(self.AdminKeyAlgId[1], CardNum, None,False)
        testResult = re.sub(re.compile('\s+'), ' ', testResult)
        if operator.eq(param_Err, testResult):
            caseResult = "pass"
        else:
            caseResult = "fail"
            e = "实测返回：" + "“" + testResult + "”"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult

    def negativeCase_oneKey_errParaChoice(self):
        # 用例描述：插入1支U盾，InitData参数栏任意输入后，点击安全初始化,期望返回“安全初始化失败:未知错误。返回码:-401Base64 decoding failed!”
        caseTitle = "用例——插入1支U盾，InitData参数栏任意输入后，点击安全初始化,期望返回“安全初始化失败:未知错误。返回码:-401Base64 decoding failed!”"
        caseResult = None
        e = None
        
        initDataLen = random.randint(0,100)
        initDataRandom=''.join(random.sample(string.ascii_letters + string.digits,initDataLen)).replace(" ","")
        
        testResult = self.testCtrl.get_SecInitCard(self.AdminKeyAlgId[1], CardNum, initDataRandom, False)
        testResult = re.sub(re.compile('\s+'), ' ', testResult)
        if operator.eq(decoding_Err, testResult):
            caseResult = "pass"
        else:
            caseResult = "fail"
            e = "实测返回：" + "“" + testResult + "”"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult

    def operationCase_pressC(self):
        # 用例描述：用例——弹出按键提示框，先不对Key执行操作，按下键盘的Esc、空格、回车键，按键提示框不会被异常关闭，然后按U盾上下翻页键,初始化按键提示框不消失，Key上无乱码；最后按下U盾C键，期望返回“安全初始化失败:未知错误。返回码:-100User cancel!”"
        caseTitle = "用例——初始化等待按键状态，按下键盘Esc/空格/回车键或U盾上下翻页键,应无反应,U盾保持等待按键状态！按下U盾取消键,期望：返回“初始化失败:未知错误。返回码:-100 User cancel!”错误提示；"
        caseResult = None
        e = None
        win32api.MessageBox(0, "确认初始化等待按键状态,按下键盘Esc/空格/回车键或U盾上下翻页键,应无反应,U盾保持等待按键状态！按下U盾取消键,取消操作”错误提示", "提示框",win32con.MB_OK)
        initResult=self.CertRequest.init_key(str_srcPin, str_srcPin)
        if not initResult[0]:
            textAreaResultSecInitCard = self.testCtrl.browser.find_element_by_id("ResultCustInitCardSec")
            testResult=textAreaResultSecInitCard.get_attribute('value')
            testResult = re.sub(re.compile('\s+'), ' ', testResult)
            if operator.eq(cancel_Err, testResult):
                caseResult = "pass"
            else:
                caseResult = "fail"
                e = "实测返回：" + "“" + testResult + "”"
        else:
            caseResult = "fail"
            e = "初始化结果与实际不符"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle) 
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult

    def operationCase_timeout(self):
        # 用例描述：弹出按键提示框，不操作U盾，等待超时时间15Min,期望返回"安全初始化失败:未知错误。返回码:-105 Time out!"
        caseTitle = "用例——确认初始化等待按键状态,不操作U盾，等待超时时间15Min,安全初始化失败: 未知错误。返回码: -105 Time out!"
        caseResult = None
        e = None
        win32api.MessageBox(0, "确认初始化等待按键状态,不要按键，等待15Min", "提示框", win32con.MB_OK)
        initResult = self.CertRequest.init_key(str_srcPin, str_srcPin)
        if not initResult[0]:
            textAreaResultSecInitCard = self.testCtrl.browser.find_element_by_id("ResultCustInitCardSec")
            testResult = textAreaResultSecInitCard.get_attribute('value')
            testResult = re.sub(re.compile('\s+'), ' ', testResult)
            if operator.eq(time_out_Err, testResult):
                caseResult = "pass"
            else:
                caseResult = "fail"
                e = "实测返回：" + "“" + re.sub(re.compile('\s+'), ' ', testResult) + "”"
        else:
            caseResult = "fail"
            e = "初始化结果与实际不符"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult
    
    def operationCase_outKey(self):
        # 用例描述：弹出初始化按键提示框时，直接拔Key，期望返回“初始化失败:未知错误。返回码:-100 User cancel!”错误提示；
        caseTitle = "用例——弹出初始化按键提示框时，直接拔Key，期望返回“初始化失败:未知错误。返回码:-100 User cancel!”错误提示；"
        caseResult = None
        e = None
        win32api.MessageBox(0, "确认初始化等待按键状态,拔出U盾", "提示框", win32con.MB_OK)

        initResult = self.CertRequest.init_key(str_srcPin, str_srcPin)
        if not initResult[0]:
            textAreaResultSecInitCard = self.testCtrl.browser.find_element_by_id("ResultCustInitCardSec")
            testResult = textAreaResultSecInitCard.get_attribute('value')
            testResult = re.sub(re.compile('\s+'), ' ', testResult)
            if operator.eq(time_out_Err, testResult):
                caseResult = "pass"
            else:
                caseResult = "fail"
                e = "实测返回：" + "“" + re.sub(re.compile('\s+'), ' ', testResult) + "”"
        else:
            caseResult = "fail"
            e = "初始化结果与实际不符"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult

    def operationCase_pinLock(self):
        # 用例描述：插入1支被锁死的U盾，输入正确InitData参数后，点击安全初始化
        caseTitle = "用例——插入1支被锁死的U盾，输入正确InitData参数后，点击安全初始化"
        caseResult = None
        e = None

        cur_url = self.testCtrl.browser.current_url
        # 修改密码
        if operator.eq(-1, cur_url.find(testUrl_GM_User)):
            self.testCtrl.browser.get(testUrl_GM_User)
        changePinResult=''
        while not operator.eq(lock_Err, changePinResult) :
            changePinResult=self.testCtrl.get_ChangePin(str_changeTitle,str_errPin,str_newPin,str_newPin)
            changePinResult=re.sub(re.compile('\s+'),' ',changePinResult)
            if operator.eq(lock_Err, changePinResult):
                self.testCtrl.browser.get(cur_url)
                break
        # 初始化
        testResult = self.CertRequest.init_key(str_srcPin, str_srcPin)
        if testResult[0]:
            caseResult = "pass"
        else:
            caseResult = "fail"
            e = "实测返回：" + "“" + testResult + "”"

        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult

    def negativeCase_manyKey(self):
        # 用例描述：插入多支同款U盾，输入相应Key转换的InitData数据，进行安全初始化
        caseTitle = "用例——插入多支同款U盾，输入相应Key转换的InitData数据，进行安全初始化,期望返回“安全初始化失败:未知错误。返回码:-104 There is more than one key!”"
        caseResult = None
        e = None
        #InitData="FkwVXp3I9vYVYfXYzg4H+HUXEwovNgNgFB400ab8Zg=="
        
        testResult = self.testCtrl.get_SecInitCard(self.AdminKeyAlgId, CardNum,initData,False)
        testResult = re.sub(re.compile('\s+'), ' ', testResult)
        if operator.eq(many_key_Err, testResult):
            caseResult = "pass"
        else:
            caseResult = "fail"
            e = "实测返回：" + "“" + testResult + "”"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult

    def negativeCase_operation(self):
        #用例描述：插入多支同款U盾，拔出多余U盾，只留1支在位，点击保护密钥更新
        caseTitle="用例——插入多支同款U盾，拔出多余U盾，只留1支在位，点击保护密钥更新"
        caseResult = None
        e=None        
        testResult=self.CertRequest.init_key(str_srcPin,str_srcPin)
        #testResult=re.sub(re.compile('\s+'),' ',testResult[0])
        if True == testResult[0]:
            caseResult="pass"                     
        else:
            caseResult="fail"
            e="实测返回："+"“"+testResult+"”"
        if e==None:
            logger.critical("%s || %s ",caseTitle,caseResult)
        else:
            logger.critical("%s || %s || %s ",caseTitle,caseResult,e)
        return caseResult     

