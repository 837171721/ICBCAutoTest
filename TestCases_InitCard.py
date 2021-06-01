# coding=utf-8
'''
Created on 2018.07.16 @author: FJQ
Created on 2018.08.18 @author: YS

'''
import re
import GenCertGroup
import win32api, win32con
import operator
from GlobalConfigure import levels,log_level,str_title,str_srcPin

from logTest import SysClass, LoggerClass
conf = LoggerClass(loglevel=levels.get(log_level), logger="TestCases_InitCard.py")
logger = conf.getlogger()

# 错误信息列表
ver_Err = '''初始化失败:未知错误。返回码:-411 ukey version error!'''
no_key_Err = '''初始化失败:未知错误。返回码:-102 There is no key!'''
many_key_Err = '''初始化失败:未知错误。返回码:-104 There is more than one key!'''
#pressC_Err = '''初始化失败:未知错误。返回码:-100 User cancel!'''
time_out_Err = '''初始化失败:未知错误。返回码:-105 Time out!'''
lock_Err = '''初始化失败:未知错误。返回码:-221 Pin Locked!'''
cancel_Err = '''初始化失败:未知错误。返回码:-100 User cancel!'''
right_Info = '''初始化成功'''

def test_GetInitCard(ctrlObj, TestingRange, AdminKeyInfo):
    # 调用流程
    testCtrl = InitCardCases(ctrlObj, AdminKeyInfo)  # 建立类对象，打开控件测试页

    if '00' != AdminKeyInfo[1]:
        testResult = testCtrl.testCtrl.get_InitCard(str_title, str_srcPin, str_srcPin)
        testResult = re.sub(re.compile('\s+'), ' ', testResult)
        if operator.eq(ver_Err, testResult):
            logger.warning("接口不支持，请选择国密旧体系盾或非国密盾进行!")
            return
    testInitCardGroup(testCtrl, TestingRange)  # 测试用例集，根据测试范围定义测试强度


def testInitCardGroup(ctrlElemObj, testRange):
    # 测试用例集
    if 0 == testRange:  # 详细测试
        #testResult = ctrlElemObj.positiveCase()  # 5、按OK键成功

        testResult = ctrlElemObj.positiveCase_formatKey()  # 11、初始化的key

        testResult = ctrlElemObj.operationCase_pressC()  # 6、按C键失败

        testResult = ctrlElemObj.operationCase_timeout()  # 7、不按键15min超时

        testResult = ctrlElemObj.operationCase_outKey()  # 9、拔出key

        #ctrlElemObj.negativeCase_Keyboard()  # 4、按键等待时，按下键盘的Esc、空格、回车键
        #ctrlElemObj.positiveCase_again()  # 10、插key，进行初始化
        #ctrlElemObj.positiveCase_changeAll()#12、已修改密码、修改名称、有证书的U盾
        #ctrlElemObj.positiveCase_operation()  # 14、拔出多余U盾，只留1支在位

    elif 1 == testRange:  # 验证测试
        a=0
        testResult = ctrlElemObj.positiveCase()  #其他接口已调用，可以注释

    elif 2 == testRange:  # 无key测试
        testResult = ctrlElemObj.negativeCase_noKey()

    elif 3 == testRange:  # 多key测试
        testResult = ctrlElemObj.negativeCase_manyKey()

    elif 4 == testRange:  # 多key测试
        testResult = ctrlElemObj.positiveCase()  #其他接口已调用，可以注释
        
        testResult = ctrlElemObj.operationCase_pressC()  # 6、按C键失败

class InitCardCases():
    def __init__(self, testCtrl, AdminKeyInfo):
        self.testCtrl = testCtrl  # 控件测试页
        self.AdminKeyAlgId = AdminKeyInfo  # 保护密钥信息
        self.CertRequest = GenCertGroup.GenCertClass(self.testCtrl, AdminKeyInfo)  # 创建证书申请对象

    def positiveCase(self):
        # 用例描述：插入1支U盾，点击初始化Key，插入1支U盾，U盾按键确认后，初始化成功；
        caseTitle = "用例——插入1支U盾，点击初始化Key，U盾按键确认后，初始化成功"
        caseResult = None
        e = None
        initResult = self.CertRequest.init_key(str_srcPin,str_srcPin)
        if initResult[0]:
            caseResult = "pass"
        else:
            caseResult = "fail"

        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult

    def negativeCase_noKey(self):
        # 用例描述：未插入U盾，点击初始化Key，期望返回“初始化失败:未知错误。返回码:-102 There is no key!”
        caseTitle = "用例——未插入U盾，点击初始化Key，期望返回“初始化失败:未知错误。返回码:-102 There is no key!”"
        caseResult = None

        e = None
        testResult = self.testCtrl.get_InitCard(str_title, str_srcPin, str_srcPin)
        testResult = re.sub(re.compile('\s+'), ' ', testResult)
        if operator.eq(no_key_Err, testResult):
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
        # 用例描述：弹出初始化按键提示框时，先不对Key执行操作，按下键盘的Esc、空格、回车键，按键提示框不会被异常关闭;然后再按下Key的C键，期望：返回“初始化失败:未知错误。返回码:-100 User cancel!”错误提示；
        caseTitle = "用例——初始化等待按键状态，按下键盘Esc/空格/回车键或U盾上下翻页键,应无反应,U盾保持等待按键状态！按下U盾取消键,期望：返回“初始化失败:未知错误。返回码:-100 User cancel!”错误提示；"
        caseResult = None
        e = None
        win32api.MessageBox(0, "确认初始化等待按键状态,按下键盘Esc/空格/回车键或U盾上下翻页键,应无反应,U盾保持等待按键状态！按下U盾取消键,取消操作”错误提示", "提示框",win32con.MB_OK)

        testResult = self.testCtrl.get_InitCard(str_title, str_srcPin, str_srcPin)
        testResult = re.sub(re.compile('\s+'), ' ', testResult)
        if operator.eq(cancel_Err, testResult):
            caseResult = "pass"
        else:
            caseResult = "fail"
            e = "实测返回：" + "“" + testResult + "”"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult

    def operationCase_timeout(self):
        # 用例描述：弹出初始化按键提示框时，不对Key执行操作，等待15Min，期望返回“初始化失败:未知错误。返回码:-105 Time out!”
        caseTitle = "用例——弹出初始化按键提示框时，不对Key执行操作，等待15Min，返回“初始化失败:未知错误。返回码:-105 Time out!”"
        caseResult = None
        e = None
        win32api.MessageBox(0, "确认初始化等待按键状态,请不要按键，等待15Min", "提示框", win32con.MB_OK)
        testResult = self.testCtrl.get_InitCard(str_title, str_srcPin, str_srcPin)
        testResult = re.sub(re.compile('\s+'), ' ', testResult)
        if operator.eq(time_out_Err, testResult):
            caseResult = "pass"
        else:
            caseResult = "fail"
            e = "实测返回：" + "“" + testResult + "”"
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
        win32api.MessageBox(0, "确认初始化等待按键状态,请拔出key", "提示框", win32con.MB_OK)
        testResult = self.testCtrl.get_InitCard(str_title, str_srcPin, str_srcPin)
        testResult = re.sub(re.compile('\s+'), ' ', testResult)
        if operator.eq(cancel_Err, testResult):
            caseResult = "pass"
        else:
            caseResult = "fail"
            e = "实测返回：" + "“" + testResult + "”"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult

    def positiveCase_formatKey(self):
        # 用例描述：插入1支初始化U盾，点击初始化Key，期望初始化成功
        caseTitle = "用例——插入1支初始化U盾，点击初始化Key，期望初始化成功"
        caseResult = None
        e = None
        InitCardResult = self.CertRequest.init_key(str_srcPin, str_srcPin)
        if InitCardResult[0]:
            testResult = self.testCtrl.get_InitCard(str_title, str_srcPin, str_srcPin)
            testResult = re.sub(re.compile('\s+'), ' ', testResult)
            if operator.eq(right_Info, testResult):
                caseResult = "pass"
            else:
                caseResult = "fail"
                e = "实测返回：" + "“" + testResult + "”"
        else:
            caseResult = "fail"
            e = "初始化失败，结束用例执行"

        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult

    def negativeCase_manyKey(self):
        # 用例描述：插入多个同款U盾，插入多个同款U盾，点击初始化Key，期望返回“初始化失败:未知错误。返回码:-104 There is more than one key!”错误提示
        caseTitle = "用例——插入多个同款U盾，插入多个同款U盾，点击初始化Key，期望返回“初始化失败:未知错误。返回码:-104 There is more than one key!”错误提示"
        caseResult = None
        e = None
        testResult = self.testCtrl.get_InitCard(str_title, str_srcPin, str_srcPin)
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

'''
def positiveCase_oneKey(self):
    # 用例描述：插入1支U盾，点击初始化Key，期望：1、弹出密码输入框，输入正确密码，提示“初始化U盾，请按键确认”；2、Key上显示“请确认”；
    caseTitle = "用例——插入1支U盾，点击初始化Key，期望：1、弹出密码输入框，输入正确密码，提示“初始化U盾，请按键确认”；2、Key上显示“请确认”；"
    caseResult = None
    e = None
    # self.testCtrl.browser.find_element_by_id("InitCard").click()
    self.testCtrl.get_InitCard(str_title, str_srcPin, str_srcPin)
    im = ImageGrab.grab()
    im.save('D:\\IcbcAutoTest\\outport\\初始化按键确认信息.jpeg')
    win32api.MessageBox(0, "请查看U盾信息是否为“请确认”！", "提示框", win32con.MB_OK)
'''

'''
def operationCase_pressOKtimeout(self):
    # 用例描述：弹出初始化按键提示框时，长按键15Min，直至超时，期望返回“初始化失败:未知错误。返回码:-105 Time out!”
    caseTitle = "用例——弹出初始化按键提示框时，长按键15Min，直至超时，期望返回“初始化失败:未知错误。返回码:-105 Time out!”"
    caseResult = None
    e = None

    if 0 == TestingType:
        win32api.MessageBox(0, "请按下OK键，等待超时时间15Min。", "提示框", win32con.MB_OK)

    testResult = self.testCtrl.get_InitCard(str_title, str_srcPin, str_srcPin)
    testResult = re.sub(re.compile('\s+'), ' ', testResult)
    if operator.eq(overtime_Err, testResult):
        caseResult = "pass"
    else:
        caseResult = "fail"
        e = "实测返回：" + "“" + re.sub(re.compile('\s+'), ' ', testResult) + "”"
    if e == None:
        logger.critical("%s || %s ",caseResult,caseTitle)
    else:
        logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
    return caseResult
'''

'''
    def positiveCase_changeAll(self):
        # 用例描述：插入1支已修改密码、修改名称、有证书的U盾，点击初始化Key，期望初始化成功
        caseTitle = "用例——插入1支已修改密码、修改名称、有证书的U盾，点击初始化Key，期望初始化成功"
        caseResult = None
        e = None

        if 0 == TestingType:
            win32api.MessageBox(0, "请插入key。", "提示框", win32con.MB_OK)
        # 修改密码
        self.testCtrl.get_ChangePin(gf.str_changeTitle, str_srcPin, gf.str_defaultPin, gf.str_verifyPin)
        # 修改名称

        # 有证书
        certResult = self.CertRequest.genCert_with_RSA1024_Mix()
        # 初始化
        testResult = self.testCtrl.get_InitCard(str_title, str_srcPin, str_srcPin)
        testResult = re.sub(re.compile('\s+'), ' ', testResult)
        if right_Info == testResult:
            caseResult = "pass"
        else:
            caseResult = "fail"
            e = "实测返回：" + "“" + re.sub(re.compile('\s+'), ' ', testResult) + "”"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult
'''

'''
def positiveCase_again(self):
    # 用例描述：再插入Key，重新初始化，期望初始化成功
    caseTitle = "用例——再插入Key，重新初始化，期望初始化成功"
    caseResult = None
    e = None
    if 0 == TestingType:
        win32api.MessageBox(0, "请插入key。", "提示框", win32con.MB_OK)

    testResult = self.testCtrl.get_InitCard(str_title, str_srcPin, str_srcPin)
    testResult = re.sub(re.compile('\s+'), ' ', testResult)
    if right_Info == testResult:
        caseResult = "pass"
    else:
        caseResult = "fail"
        e = "实测返回：" + "“" + re.sub(re.compile('\s+'), ' ', testResult) + "”"
    if e == None:
        logger.critical("%s || %s ",caseResult,caseTitle)
    else:
        logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
    return caseResult
'''

'''
def negativeCase_Keyboard(self):
    # 用例描述：弹出初始化按键提示框时，不对Key执行操作，按下键盘的Esc、空格、回车键，按键提示框不会被异常关闭
    caseTitle = "用例——弹出初始化按键提示框时，不对Key执行操作，按下键盘的Esc、空格、回车键，按键提示框不会被异常关闭"
    caseResult = None
    e = None

    if 0 == TestingType:
        win32api.MessageBox(0, "初始化按键等待时，请先按下键盘的Esc、空格、回车键！", "提示框", win32con.MB_OK)

    testResult = self.testCtrl.get_InitCard(str_title, str_srcPin, str_srcPin)
    if testResult.count("成功"):
        return "pass"
    else:
        return "fail"
'''

'''
    def negativeCase_newAndminKey(self):
        # 用例描述：插入新体系的国密U盾，点击初始化Key，期望返回：初始化失败:未知错误。返回码:-411 ukey version error!
        caseTitle = "用例——插入更新体系的国密U盾，点击初始化Key，期望返回：初始化失败:未知错误。返回码:-411 ukey version error!"
        caseResult = None
        e = None

        testResult = self.testCtrl.get_InitCard(str_title, str_srcPin, str_srcPin)
        testResult = re.sub(re.compile('\s+'), ' ', testResult)
        if Newsys_Err == testResult:
            caseResult = "pass"
        else:
            caseResult = "fail"
            e = "实测返回：" + "“" + re.sub(re.compile('\s+'), ' ', testResult) + "”"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult
'''

'''
    def negativeCase_operation(self):
        # 用例描述：插入多个同款U盾，拔出多余U盾，只留1支在位，点击初始化Key，期望初始化成功
        caseTitle = "用例——插入多个同款U盾，拔出多余U盾，只留1支在位，点击初始化Key，期望初始化成功"
        caseResult = None
        e = None

        testResult = self.testCtrl.get_InitCard(str_title, str_srcPin, str_srcPin)
        testResult = re.sub(re.compile('\s+'), ' ', testResult)
        if right_Info == testResult:
            caseResult = "pass"
        else:
            caseResult = "fail"
            e = "实测返回：" + "“" + re.sub(re.compile('\s+'), ' ', testResult) + "”"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult
'''
