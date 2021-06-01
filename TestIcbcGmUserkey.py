#coding=utf-8
'''
Created on 2017.12.15

@author: ys

'''
import re
import string
import time
#import uuid
import os
import traceback
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
#import autoit
import unittest
import win32api 
import win32con
import win32gui
import operator
import random
from ctypes import *
import pyautogui as pag
from LocalConvertTool import *
from GlobalConfigure import *
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from GlobalConfigure import Str_IEServerDrive,CardNum, levels, AuxTool
#from LocalConvertTool import open_window, ToolConvert
#from PinCheckClass import CheckPasswordClass
from pymouse import PyMouse
from pykeyboard import PyKeyboard

from logTest import SysClass, LoggerClass
conf  = LoggerClass(loglevel=levels.get("info"), logger="TestIcbcGmUserkey.py")
logger=conf.getlogger()
             
class TestIcbcGmUser:
    def __init__(self, url, type = None):
        self.isActiveXLoaded = False
        self.url = url
        IEDriverServer  = Str_IEServerDrive       
        os.environ["webdriver.ie.driver"] = IEDriverServer 
        DesiredCapabilities.INTERNETEXPLORER["ignoreProtectedModeSettings"] = True
        self.browser = webdriver.Ie(IEDriverServer)
        self.m = PyMouse()
        self.k = PyKeyboard()
      
    def open(self):
        if None != self.browser and None != self.url:
            self.browser.get(self.url)
            self.browser.maximize_window()
            #self._load_ActiveX()
            #self._load_ActiveX_New('明华澳汉控件测试', 'DirectUIHWND1')
            
    def get_MediaId(self):
        ''''' 
                 获取介质号 
        ''''' 
        try:
            #global MediaId       
            #定位鼠标位置，确保鼠标焦点定位在对话框上
            self.mouseFocus_locate()
            #初始化
            textAreaResultGetMediaID = self.browser.find_element_by_id("ResultGetMediaID")           
            textAreaResultGetMediaID.clear()
            #测试开始
            btnGetMediaID = self.browser.find_element_by_id("GetMediaIDC")
            btnGetMediaID.click()
            WebDriverWait(self.browser, 5).until(lambda x: 0 <= len(x.find_element_by_id("ResultGetMediaID").get_attribute('value')))
            MediaId=textAreaResultGetMediaID.get_attribute('value')
            # print("介质号：" + MediaId)
            return MediaId
        except Exception as e:
            logger.error("Exception- %s ",str(e))
            return 
    
    def get_GMCertDN(self):
        ''''' 
                        获取证书DN值
        ''''' 
        try:
            #定位鼠标位置，确保鼠标焦点定位在对话框上
            self.mouseFocus_locate()
            #初始化
            textAreaResultGetGMCertDN = self.browser.find_element_by_id("ResultGetCertDN")
            textAreaResultGetGMCertDN.clear()
            #测试开始
            btnGetGMCertDN = self.browser.find_element_by_id("GetCertDNC")
            btnGetGMCertDN.click()
            WebDriverWait(self.browser, 5).until(lambda x: 0 <= len(x.find_element_by_id("ResultGetCertDN").get_attribute('value')))
            # print('证书DN' + textAreaResultGetGMCertDN.get_attribute('value'))
            return textAreaResultGetGMCertDN.get_attribute('value')
        except Exception as e:
            logger.error("Exception- %s ",str(e))
            #pass
            return

    def get_PubKey(self,ReadType='AllPubKey'):
        ''''' 
                        获取公钥明文
        ''''' 
        '''
        ReadType:获取类型，"AllPubKey"/"CertPubKey"/"NoCertPubKey"
        '''
        try:
            #定位鼠标位置，确保鼠标焦点定位在对话框上
            self.mouseFocus_locate()
            #初始化
            textAreaResultGetPubKey = self.browser.find_element_by_id("ResultGMGetPublicKey")
            textAreaResultGetPubKey.clear()
            #测试开始
            if operator.eq(testUrl_GM_User,main_url):
                if None != ReadType and '' != ReadType:            
                    s1 = Select(self.browser.find_element_by_id('ReadType')) 
                    s1.select_by_value(ReadType)
                else: 
                    self.browser.find_element_by_xpath("/html/body/table/tbody/tr/td[1]/p[4]/a").click() #通过左边的按钮进行清空下拉框内容                   
            btnGetPubKey = self.browser.find_element_by_id("GetPublicKey")
            btnGetPubKey.click()
            WebDriverWait(self.browser, 5).until(lambda x: 0 <= len(x.find_element_by_id("ResultGMGetPublicKey").get_attribute('value')))
            # print(textAreaResultGetPubKey.get_attribute('value'))
            return textAreaResultGetPubKey.get_attribute('value')
        except Exception as e:
            logger.error("Exception- %s ",str(e))
            return

    def get_PubKeyC(self):
        ''''' 
                        读取原保护密钥的加密公钥
        ''''' 
        try:
            #定位鼠标位置，确保鼠标焦点定位在对话框上
            self.mouseFocus_locate()
            #初始化
            textAreaResultGetPublicKeyC = self.browser.find_element_by_id("ResultGetPublicKeyC")
            textAreaResultGetPublicKeyC.clear()
            #测试开始
            btnGetPublicKey = self.browser.find_element_by_id("GetPublicKeyC")
            btnGetPublicKey.click()
            WebDriverWait(self.browser, 5).until(lambda x: 0 <= len(x.find_element_by_id("ResultGetPublicKeyC").get_attribute('value')))
            print(textAreaResultGetPublicKeyC.get_attribute('value'))
            return textAreaResultGetPublicKeyC.get_attribute('value')
        except Exception as e:
            logger.error("Exception- %s ",str(e))
            #pass
            return
        
    def get_GMPubKeyC(self,KeyType='02', DNorID=None,SerRand=None,ToolSerRand=False):
        ''''' 
                            读取新保护密钥的加密公钥
        '''''
        '''
        KeyType: 获取类型，02-签名  ， 01-下证 或  空； 
        DNorID:证书DN或公钥DN   
        SerRand:服务端随机数
        ToolSerRand:通过工具获取随机数,True或False
        '''
        try:
            #定位鼠标位置，确保鼠标焦点定位在对话框上
            self.mouseFocus_locate()
            #初始化
            textAreaResultGMGetPubKeyC = self.browser.find_element_by_id("ResultGMGetPublicKeyC")
            textAreaResultGMGetPubKeyC.clear()                            
            textAreaResultDNorID = self.browser.find_element_by_id("DNorID")
            textAreaResultDNorID.clear() 
            textAreaResultBase64SerRand=self.browser.find_element_by_id("Base64SerRand")
            textAreaResultBase64SerRand.clear()
            #参数判断    
            if None != KeyType and '' != KeyType:                       
                #获取类型
                s1 = Select(self.browser.find_element_by_id('KeyType')) 
                s1.select_by_value(KeyType) 
            else:
                self.browser.find_element_by_xpath("/html/body/table/tbody/tr/td[1]/p[6]/a").click() #通过左边的按钮进行清空下拉框内容                   
            if None != DNorID and '' != DNorID:
                #证书DN或公钥ID
                textAreaResultDNorID.click() 
                content='document.getElementById("DNorID").value = "%s"' % DNorID             
                self.browser.execute_script(content)
            if True == ToolSerRand:
                self.get_ServerRandom()
            else:                
                if None != SerRand and '' != SerRand: 
                    textAreaResultBase64SerRand.click() 
                    content='document.getElementById("Base64SerRand").value = "%s"' % SerRand             
                    self.browser.execute_script(content) 

            #测试开始                                       
            btnGMGetPubKeyC = self.browser.find_element_by_id("GMGetPublicKeyC")
            btnGMGetPubKeyC.click()                     
            WebDriverWait(self.browser, 5).until(lambda x: 0 <= len(x.find_element_by_id("ResultGMGetPublicKeyC").get_attribute('value')))
            return textAreaResultGMGetPubKeyC.get_attribute('value')
        except Exception as e:
            logger.error("Exception- %s ",str(e))
        return

    def get_Ver(self):
        ''''' 
                        获取控件版本号
        '''''
        try:
            #定位鼠标位置，确保鼠标焦点定位在对话框上
            self.mouseFocus_locate()
            #初始化
            textAreaResultGetVer = self.browser.find_element_by_id("ResultGetVersion")
            textAreaResultGetVer.clear()
            #测试开始
            btnGetVer = self.browser.find_element_by_id("GetVersion")
            btnGetVer.click()
            WebDriverWait(self.browser, 5).until(lambda x: 0 <= len(x.find_element_by_id("ResultGetVersion").get_attribute('value')))
            return textAreaResultGetVer.get_attribute('value')
        except Exception as e:
            logger.error("Exception- %s ",str(e))
        return

    def get_DriverVer(self):
        ''''' 
                        获取驱动版本号
        '''''        
        try:
            #定位鼠标位置，确保鼠标焦点定位在对话框上
            self.mouseFocus_locate()
            #初始化
            textAreaResultGetDriverVer = self.browser.find_element_by_id("ResultGetDriverVersion")
            textAreaResultGetDriverVer.clear()
            #测试开始
            btnGetDriverVer = self.browser.find_element_by_id("GetDviverVersionC")
            btnGetDriverVer.click()
            WebDriverWait(self.browser, 5).until(lambda x: 0 <= len(x.find_element_by_id("ResultGetDriverVersion").get_attribute('value')))
            return textAreaResultGetDriverVer.get_attribute('value')
        except Exception as e:
            logger.error("Exception- %s ",str(e))
        return

    def get_GMDelTempKey(self,str_CertDn=None,str_PubkeyDn=None,str_tipTitle=str_verifyTitle):
        ''''' 
                        删除临时密钥对
        '''''         
        try:
            #定位鼠标位置，确保鼠标焦点定位在对话框上
            self.mouseFocus_locate()
            #初始化
            textAreaResultCertDn = self.browser.find_element_by_id('CertDn')
            textAreaResultCertDn.clear()
            textAreaResultPubKeyID = self.browser.find_element_by_id('PublicKeyId')
            textAreaResultPubKeyID.clear() 
            textAreaResultGMDelTempKey = self.browser.find_element_by_id("ResultGMDelTempKey")
            textAreaResultGMDelTempKey.clear()
            #参数判断           
            if None != str_CertDn and '' != str_CertDn: 
                #证书DN或公钥ID
                textAreaResultCertDn.click() 
                content='document.getElementById("CertDn").value = "%s"' % str_CertDn             
                self.browser.execute_script(content)
            if None != str_PubkeyDn and '' != str_PubkeyDn:
                textAreaResultCertDn.click() 
                content='document.getElementById("PublicKeyId").value = "%s"' % str_PubkeyDn             
                self.browser.execute_script(content)  
            #测试开始
            btnGMDelTempKeyC = self.browser.find_element_by_id("GMDelTempKeyC")
            btnGMDelTempKeyC.click()
            time.sleep(0.5)
            #用户提示
            if 2 <= GL.TestingRange and GL.TestingRange <= 3:
                WebDriverWait(self.browser, 5).until(lambda x: 0 < len(x.find_element_by_id("ResultGMDelTempKey").get_attribute('value')))
                return textAreaResultGMDelTempKey.get_attribute('value')
            
            else:
                while self.find_subWindow(str_tipTitle):
                    logger.warning('等待U盾按键操作...')
                    time.sleep(1)
                
            WebDriverWait(self.browser, 5).until(lambda x: 0 <= len(x.find_element_by_id("ResultGMDelTempKey").get_attribute('value')))
            return textAreaResultGMDelTempKey.get_attribute('value')
        except Exception as e:
            tempExcept=re.sub(re.compile('\s+'), ' ', str(e))
            str_excep1_one='''Alert Text: Message: Modal dialog present '''
            if operator.eq(tempExcept,str_excep1_one):
                return textAreaResultGMDelTempKey.get_attribute('value')
            else:
                logger.error("Exception- %s ",str(e))
                return
    
    def get_CharsetList(self):
        ''''' 
                        获取支持的字符集
        '''''         
        try:
            #定位鼠标位置，确保鼠标焦点定位在对话框上
            self.mouseFocus_locate()
            #初始化
            textAreaResultGetCharsetList = self.browser.find_element_by_id("ResultGetCharsetList")
            textAreaResultGetCharsetList.clear()
            #测试开始
            btnGetDriverVer = self.browser.find_element_by_id("GetCharsetListC")
            btnGetDriverVer.click()
            
            WebDriverWait(self.browser, 5).until(lambda x: 0 <= len(x.find_element_by_id("ResultGetCharsetList").get_attribute('value')))
            return textAreaResultGetCharsetList.get_attribute('value')
        except Exception as e:
            logger.error("Exception- %s ",str(e))            
        return

    def SetCharset(self,charSet='UTF-8'):
        ''''' 
                        设置即将签名的明文字符集
        '''''           
        try:
            #定位鼠标位置，确保鼠标焦点定位在对话框上
            self.mouseFocus_locate()
            #初始化  
            textAreaResultSetCharset = self.browser.find_element_by_id("ResultSetCharset")
            textAreaResultSetCharset.clear()
            textszCharset = self.browser.find_element_by_id('szCharset')
            textszCharset.clear()
            if None != charSet or '' !=charSet:
                textszCharset.send_keys(charSet)
            else:
                textszCharset.clear()
            #测试开始          
            btnSetCharsetC = self.browser.find_element_by_id("SetCharsetC")
            btnSetCharsetC.click()            
            WebDriverWait(self.browser, 5).until(lambda x: 0 <= len(x.find_element_by_id("ResultSetCharset").get_attribute('value')))
            return textAreaResultSetCharset.get_attribute('value')
        except Exception as e:
            logger.error("Exception- %s ",str(e))
            return

    def get_LanguageList(self):
        ''''' 
                        获取U盾提示语
        '''''          
        try:
            #定位鼠标位置，确保鼠标焦点定位在对话框上
            self.mouseFocus_locate()
            #初始化  
            textAreaResultGetKeyMsg = self.browser.find_element_by_id("ResultGetKeyMsg")
            textAreaResultGetKeyMsg.clear()
            #测试开始
            btnGetLanguageListC = self.browser.find_element_by_id("GetLanguageListC")
            btnGetLanguageListC.click()
            
            WebDriverWait(self.browser, 5).until(lambda x: 0 <= len(x.find_element_by_id("ResultGetKeyMsg").get_attribute('value')))
            return textAreaResultGetKeyMsg.get_attribute('value')
        except Exception as e:
            logger.error("Exception- %s ",str(e))
        return

    def set_LanguageList(self,langtype='zh_CN'):
        ''''' 
                        设置U盾提示语
        '''''           
        try:
            #定位鼠标位置，确保鼠标焦点定位在对话框上
            self.mouseFocus_locate()
            #初始化
            self.browser.find_element_by_xpath("/html/body/table/tbody/tr/td[1]/p[15]/a").click()
            textAreaResultSetLanguageList = self.browser.find_element_by_id("ResultSetLanguageList")
            #textAreaResultSetLanguageList.clear()
            textszLanguage = self.browser.find_element_by_id('szLanguage')
            textszLanguage.clear()
            #测试开始
            if None != langtype or '' != langtype:
                textszLanguage.send_keys(langtype)
            else:
                textszLanguage.clear()                       
            btnSetLanguageListC = self.browser.find_element_by_id("SetLanguageListC")
            btnSetLanguageListC.click()

            WebDriverWait(self.browser, 5).until(lambda x: 0 < len(x.find_element_by_id("ResultSetLanguageList").get_attribute('value')))
            return textAreaResultSetLanguageList.get_attribute('value')
        except Exception as e:            
            tempExcept=re.sub(re.compile('\s+'), ' ', str(e))
            str_excep1_one="Alert Text: Message: Modal dialog present "
            str_excep2_one="Message:,No,alert,is,active,"
            if operator.eq(tempExcept,str_excep1_one):
                #logger.warning("===%s",tempExcept)
                try:
                    alertResult=EC.alert_is_present()(self.browser)      
                    if alertResult: 
                        alertResult.accept()             
                        time.sleep(0.5)
                except Exception as ex:
                    '''
                    tempExcept=re.sub(re.compile('\s+'), ',', str(ex))
                    #logger.warning("%s",tempExcept)                    
                    if not operator.eq(str_excep2_one,tempExcept):
                        logger.warning("&&& %s",tempExcept)                        
                        #return textAreaResultSetLanguageList.get_attribute('value')
                    else:
                        #logger.warning("--- %s",tempExcept)
                        logger.error("Exception- %s ",tempExcept)
                    '''
                    return textAreaResultSetLanguageList.get_attribute('value')
            else:
                #logger.warning("%s", tempExcept)
                logger.error("Exception- %s ",str(e))
                return
            

    def set_WarningMsg(self,ScreenWarningMsg='screen warning'):
        ''''' 
                        设置PC屏幕警告语
        '''''          
        try:
            #定位鼠标位置，确保鼠标焦点定位在对话框上
            self.mouseFocus_locate()
            #初始化  
            textAreaResultSetWarningMsg = self.browser.find_element_by_id("ResultSetWarningMsg")
            textAreaResultSetWarningMsg.clear()
            textWarningMsg = self.browser.find_element_by_id('WarningMsg')
            textWarningMsg.clear()
            #测试开始
            if None != ScreenWarningMsg:
                textWarningMsg.send_keys(ScreenWarningMsg)
            else:
                textWarningMsg.clear()                          
            btnSetWarningMsgC = self.browser.find_element_by_id("SetWarningMsgC")
            btnSetWarningMsgC.click()
            WebDriverWait(self.browser, 5).until(lambda x: 0 <= len(x.find_element_by_id("ResultSetWarningMsg").get_attribute('value')))
            return textAreaResultSetWarningMsg.get_attribute('value')
        except Exception as e:
            logger.error("Exception- %s ",str(e))
        return

    def get_CspInfoC(self,str_MediaId):
        ''''' 
                    获取CSP信息
        '''''         
        try:
            #定位鼠标位置，确保鼠标焦点定位在对话框上
            self.mouseFocus_locate()
            #初始化
            
            textMediaID = self.browser.find_element_by_id('szMediaID')
            textMediaID.clear()
            
            textAreaResultGetCspInfo = self.browser.find_element_by_id("ResultGetCspInfo")
            textAreaResultGetCspInfo.clear()
            #参数判断
            if None != str_MediaId and '' != str_MediaId:
                textMediaID.click()
                #textMediaID.send_keys(str_MediaId)
                content='document.getElementById("szMediaID").value = "%s"' % str_MediaId             
                self.browser.execute_script(content)               
                time.sleep(0.01)            
            #测试开始
            btnGetCspInfo = self.browser.find_element_by_id("GetCspInfo")
            btnGetCspInfo.click()
            WebDriverWait(self.browser, 5).until(lambda x: 0 <= len(x.find_element_by_id("ResultGetCspInfo").get_attribute('value')))
            return textAreaResultGetCspInfo.get_attribute('value')
        except Exception as e:
            logger.error("Exception- %s ",str(e))
        return

    def get_PubKeyNum(self):
        ''''' 
                        获取公钥个数
        '''''        
        try:
            #定位鼠标位置，确保鼠标焦点定位在对话框上
            self.mouseFocus_locate()
            #初始化  
            textAreaResultGetPubKeyNum = self.browser.find_element_by_id("ResultGetPubKeyNum")
            textAreaResultGetPubKeyNum.clear()
            #测试开始
            btnGetPubKeyNum = self.browser.find_element_by_id("GetPubKeyNum")
            btnGetPubKeyNum.click()
            WebDriverWait(self.browser, 5).until(lambda x: 0 <= len(x.find_element_by_id("ResultGetPubKeyNum").get_attribute('value')))
            return textAreaResultGetPubKeyNum.get_attribute('value')
        except Exception as e:
            logger.error("Exception- %s ",str(e))
        return

    def RegisterCertC(self):
        ''''' 
                        注册证书
        '''''          
        try:
            #定位鼠标位置，确保鼠标焦点定位在对话框上
            self.mouseFocus_locate()
            #初始化            
            textAreaResultRegisterCert = self.browser.find_element_by_id("ResultRegisterCert")
            textAreaResultRegisterCert.clear()
            #测试开始
            btnRegisterCert = self.browser.find_element_by_id("RegisterCert")
            btnRegisterCert.click()
            WebDriverWait(self.browser, 5).until(lambda x: 0 <= len(x.find_element_by_id("ResultRegisterCert").get_attribute('value')))
            return textAreaResultRegisterCert.get_attribute('value')
        except Exception as e:
            logger.error("Exception- %s ",str(e))
        return

    def UnRegisterCertC(self):
        ''''' 
                        注销证书
        '''''         
        try:
            #定位鼠标位置，确保鼠标焦点定位在对话框上
            self.mouseFocus_locate()
            #初始化
            textAreaResultUnRegisterCert = self.browser.find_element_by_id("ResultUnRegisterCert")
            textAreaResultUnRegisterCert.clear()
            #测试开始
            btnUnRegisterCert = self.browser.find_element_by_id("UnRegisterCert")
            btnUnRegisterCert.click()
            WebDriverWait(self.browser, 5).until(lambda x: 0 <= len(x.find_element_by_id("ResultUnRegisterCert").get_attribute('value')))
            return textAreaResultUnRegisterCert.get_attribute('value')
        except Exception as e:
            logger.error("Exception- %s ",str(e))
        return

    def get_AdminKeyInfoC(self):
        ''''' 
                        获取保护密钥信息
        '''''         
        try:
            #定位鼠标位置，确保鼠标焦点定位在对话框上
            self.mouseFocus_locate()
            #初始化
            textAreaResultGMGetAdminKeyInfo = self.browser.find_element_by_id("ResultGMGetAdminKeyInfo")
            textAreaResultGMGetAdminKeyInfo.clear()
            #测试开始
            btnGetAdminKeyInfo = self.browser.find_element_by_id("GetAdminKeyInfo")
            btnGetAdminKeyInfo.click()
            WebDriverWait(self.browser, 5).until(lambda x: 0 <= len(x.find_element_by_id("ResultGMGetAdminKeyInfo").get_attribute('value')))
            return textAreaResultGMGetAdminKeyInfo.get_attribute('value')
        except Exception as e:
            logger.error("Exception- %s ",str(e))
            return
           
    def get_InitCard(self,str_title,str_initPin,str_verifyPin,inputBtnType=0,simpleBtnType=0,str_tipTitle=str_verifyTitle):
        ''''' 
        初始化Key
        '''''  
        '''
        inputBtnType: 输入密码框上0表示确认，1表示取消，2表示关闭“x”,默认是0
        simpleBtnType:弱密码框上0表示确认，1表示取消，2表示关闭“x”，默认是0
        ''' 
        try:
            #定位鼠标位置，确保鼠标焦点定位在对话框上
            self.mouseFocus_locate()
            #初始化变量
            textAreaResultInitCard = self.browser.find_element_by_id("ResultCustInitCard")
            textAreaResultInitCard.clear()
            btnInitCard = self.browser.find_element_by_id("InitCard")
            btnInitCard.click()
            time.sleep(1)
            #测试开始
            if 2 <= GL.TestingRange and GL.TestingRange <= 3:
                WebDriverWait(self.browser, 5).until(lambda x: 0 < len(x.find_element_by_id("ResultCustInitCard").get_attribute('value')))
                return textAreaResultInitCard.get_attribute('value')
            
            elif self.find_subWindow(str_title):
                #输入指定密码
                dlg_hWnd=self.find_subWindow(str_title)
                #self.mouseFocus_locate()
                #pag.click()
                                  
                #rect=RECT()
                #ctypes.windll.user32.GetWindowRect(dlg_hWnd, ctypes.byref(rect)) #获取对话框相对屏幕的坐标位置
                #pag.click(rect.left+20, rect.top+20)
                   
                self.inputPinFunc(2,str_initPin,str_verifyPin)

                if len(str_initPin)<6 or len(str_verifyPin) <6:
                    logger.warning('密码长度过短,无法继续操作!核对以上现象后,关闭密码输入框以结束本次流程')
                    self.DlgBtnClick(dlg_hWnd,2)
                    WebDriverWait(self.browser, 5).until(lambda x: 0 < len(x.find_element_by_id("ResultCustInitCard").get_attribute('value')))                                                           
                    return textAreaResultInitCard.get_attribute('value') 
                #确认键
                time.sleep(0.2)
                contiMark=self.DlgBtnClick(dlg_hWnd,inputBtnType)
                if contiMark:       #仅按确认键流程后才有剩余判断框流程   
                    #用户提示  
                    resp_title= str_tipTitle       #窗口名称
                    while operator.eq(str_tipTitle,resp_title):
                        resp_title=''                        
                        dlg_tip_hWnd=self.find_subWindow(str_tipTitle)
                        resp_title = win32gui.GetWindowText(dlg_tip_hWnd)
                        dlg_tip_hWnd = win32gui.FindWindow(None,resp_title)
                        if not  win32gui.IsWindowVisible(dlg_tip_hWnd):
                            break                        
                        if operator.eq(str_tipTitle,resp_title):#确认对话框已弹出
                            #第1步：先判断新pin与确认pin是否一致：一致，继续；否则重新输入新Pin和校验Pin    
                            #第2步：再判断新pin是否为弱密码:
                            #第3步：信息核对框等待按键确认
                            if operator.eq(str_initPin,str_verifyPin):  #修改pin与确认pin一致
                                #判断弹框中有无按钮
                                btn= win32gui.FindWindowEx(dlg_tip_hWnd, None, 'Button', None) 
                                if btn>0:
                                    #判断是否为弱密码
                                    simplePin=self.PasswordRulesOfICBC(str_initPin)
                                    if 0 == simplePin: 
                                        #弱密码
                                        rect = RECT()
                                        ctypes.windll.user32.GetWindowRect(dlg_tip_hWnd,ctypes.byref(rect))  # 获取对话框相对屏幕的坐标位置
                                        pag.moveTo(rect.left + 20, rect.top + 20)
                                        if not self.DlgBtnClick(dlg_hWnd,simpleBtnType):  
                                            #关闭弱密码框，回到输入密码框重新输入新旧密码
                                            time.sleep(0.5)
                                            logger.warning('关闭弱密码框，回到输入密码框，要求重新输入新密码和校验密码.核对现象后，关闭输入密码框以结束本次流程')
                                            self.DlgBtnClick(dlg_hWnd,2) #关闭输入密码框，已结束本次操作
                                        else:
                                            logger.warning('等待U盾按键操作...')
                                            time.sleep(1)
                                    else:
                                        #弹出信息核对框
                                        logger.warning('等待U盾按键操作...')
                                        time.sleep(1)
                                else:
                                    #弹出信息核对框
                                    logger.warning('等待U盾按键操作...')  
                                    time.sleep(1)   
                            else:#新pin与确认pin不一致
                                dlg_tip_hWnd=self.find_subWindow(str_tipTitle)
                                rect = RECT()
                                ctypes.windll.user32.GetWindowRect(dlg_tip_hWnd,ctypes.byref(rect))  # 获取对话框相对屏幕的坐标位置
                                pag.moveTo(rect.left + 20, rect.top + 20)
                                pag.typewrite(['enter'])#弹框中仅有确认按钮,点击确认后回到密码输入框等待输入新密码及验证密码                                    
                                time.sleep(0.5)
                                logger.warning('关闭新pin与确认pin不一致提示框，回到输入密码框，要求重新输入新密码和校验密码.核对现象后，关闭输入密码框以结束本次流程')
                                self.DlgBtnClick(dlg_hWnd,2)  #关闭输入密码框，已结束本次操作
                
            else:
                logger.error("InitCard Exception:not found the window" + str_title)
            WebDriverWait(self.browser, 5).until(lambda x: 0 < len(x.find_element_by_id("ResultCustInitCard").get_attribute('value')))
            return textAreaResultInitCard.get_attribute('value')                             
        except Exception as e:
            tempExcept = re.sub(re.compile('\s+'), ' ', str(e))
            str_excep1_one = '''Alert Text: Message: Modal dialog present '''
            if operator.eq(tempExcept, str_excep1_one):
                return textAreaResultInitCard.get_attribute('value')
            else:
                logger.error("Exception- %s ", str(e))
                return
     
    def get_ChangePin(self,str_title,oldPinStr,newPinStr,verifyPinStr,inputBtnType=0,simpleBtnType=0,str_tipTitle=str_verifyTitle):
        ''''' 
                    修改PIN
        '''''  
        '''
        inputBtnType: 输入密码框上0表示确认，1表示取消，2表示关闭“x”,默认是0
        simpleBtnType:弱密码框上0表示确认，1表示取消，2表示关闭“x”，默认是0
        '''
        try:
            #定位鼠标位置，确保鼠标焦点定位在对话框上
            self.mouseFocus_locate()
            #初始化变量
            textAreaResultChangePin = self.browser.find_element_by_id("ResultChangePin")
            textAreaResultChangePin.clear()            
            btnChangePinC = self.browser.find_element_by_id("ChangePinC")
            btnChangePinC.click()
            time.sleep(1)
            #测试开始
            if 2 <= GL.TestingRange and GL.TestingRange <= 3:
                WebDriverWait(self.browser, 5).until(lambda x: 0 < len(x.find_element_by_id("ResultChangePin").get_attribute('value')))
                return textAreaResultChangePin.get_attribute('value')
                                 
            elif self.find_subWindow(str_title):    
                #输入指定密码
                dlg_hWnd=self.find_subWindow(str_title)
#                 self.mouseFocus_locate()
#                 pag.click()
#                                    
#                 rect=RECT()
#                 ctypes.windll.user32.GetWindowRect(dlg_hWnd, ctypes.byref(rect)) #获取对话框相对屏幕的坐标位置
#                 pag.click(rect.left+20, rect.top+20)   
                           
                self.inputPinFunc(3,oldPinStr,newPinStr,verifyPinStr)
                if len(oldPinStr)<6 or len(newPinStr) <6 or len(verifyPinStr)<6:
                    logger.warning('密码长度过短,无法继续操作!核对以上现象后,关闭密码输入框以结束本次流程')
                    self.DlgBtnClick(dlg_hWnd,2)
                    WebDriverWait(self.browser, 5).until(lambda x: 0 <= len(x.find_element_by_id("ResultChangePin").get_attribute('value')))                                                           
                    return textAreaResultChangePin.get_attribute('value')                           
                #确认键，修改PIN码
                time.sleep(0.2)
                contiMark=self.DlgBtnClick(dlg_hWnd,inputBtnType)                
                if contiMark:       #仅按确认键流程后才有剩余判断框流程
                    #用户提示 
                    resp_title= str_tipTitle       #窗口名称
                    while operator.eq(str_tipTitle,resp_title):
                        resp_title=''
                        dlg_tip_hWnd=self.find_subWindow(str_tipTitle)
                        resp_title = win32gui.GetWindowText(dlg_tip_hWnd)
                        dlg_tip_hWnd = win32gui.FindWindow(None,resp_title)
                        if not  win32gui.IsWindowVisible(dlg_tip_hWnd):
                            break  
                        if operator.eq(str_tipTitle,resp_title):#确认对话框已弹出
                            #第1步：先判断修改pin与校验pin是否一致：一致，继续；否则重新输入新Pin和校验Pin
                            #第2步：再判断新旧密码是否一致:不一致,继续；否则重新输入新Pin和校验Pin
                            #第3步：再判断修改pin是否为弱密码:
                            #第3步：再判断原密码是否正确
                            #第4步：信息核对框等待按键确认
                            if operator.eq(newPinStr,verifyPinStr):  #修改pin与校验pin一致
                                if False == operator.eq(newPinStr,oldPinStr): #新旧密码不一致
                                    #判断弹框中有无按钮
                                    btn= win32gui.FindWindowEx(dlg_tip_hWnd, None, 'Button', None) 
                                    if btn>0:
                                        #判断是否为弱密码
                                        simplePin=self.PasswordRulesOfICBC(newPinStr)
                                        if 0 == simplePin: 
                                            #弱密码
                                            rect=RECT()
                                            ctypes.windll.user32.GetWindowRect(dlg_tip_hWnd, ctypes.byref(rect)) #获取对话框相对屏幕的坐标位置
                                            pag.moveTo(rect.left+20, rect.top+20)                               
                                            if not self.DlgBtnClick(dlg_tip_hWnd,simpleBtnType):  
                                                #关闭弱密码框，回到输入密码框重新输入新旧密码
                                                time.sleep(0.5)
                                                logger.warning('关闭弱密码框，回到输入密码框，要求重新输入新密码和校验密码.核对现象后，关闭输入密码框以结束本次流程')
                                                self.DlgBtnClick(dlg_hWnd,2) #关闭输入密码框，已结束本次操作
                                            else:
                                                logger.warning('等待U盾按键操作...')
                                        if operator.eq(oldPinStr,str_srcPin):  
                                            #原密码正确，弹出信息核对框
                                            logger.warning('等待U盾按键操作...')
                                        else:
                                            #原密码不正确
                                            rect=RECT()
                                            ctypes.windll.user32.GetWindowRect(dlg_tip_hWnd, ctypes.byref(rect)) #获取对话框相对屏幕的坐标位置
                                            pag.moveTo(rect.left+20, rect.top+20)
                                            #dlg1_tip_hWnd = self.find_subWindow(str_tipTitle)
                                            dlg1_tip_hWnd = win32gui.FindWindow(None,str_tipTitle)                        
                                            ErrPinBtn= win32gui.FindWindowEx(dlg1_tip_hWnd, None, 'Button', None)
                                            if ErrPinBtn >0: 
                                                #关闭错误密码框，回到输入密码框重新输入新旧密码
                                                time.sleep(0.5)
                                                logger.warning('关闭错误密码框，结束本次流程')
                                                self.DlgBtnClick(dlg1_tip_hWnd,0)#关闭输入密码框，已结束本次操                                                
                                            else:
                                                logger.warning('错误密码剩余2/1次，等待U盾按键操作...')
                                    else:
                                        #弹出信息核对框
                                        logger.warning('等待U盾按键操作...')
                                                                                       
                                else: #新旧密码一致
                                    dlg_tip_hWnd=self.find_subWindow(str_tipTitle)
                                    rect = RECT()
                                    ctypes.windll.user32.GetWindowRect(dlg_tip_hWnd,ctypes.byref(rect))  # 获取对话框相对屏幕的坐标位置
                                    pag.moveTo(rect.left + 20, rect.top + 20)                              
                                    pag.typewrite(['enter']) #弹框中仅有确认按钮,点击确认后回到密码输入框等待输入新密码及验证密码
                                    #pag.press('enter') #弹框中仅有确认按钮,点击确认后回到密码输入框等待输入新密码及验证密码
                                    time.sleep(0.5)
                                    logger.warning('关闭新旧密码一致提示框，回到输入密码框，要求重新输入新密码和校验密码.核对现象后，关闭输入密码框以结束本次流程')
                                    self.DlgBtnClick(dlg_hWnd,2)#关闭输入密码框，已结束本次操作            
                            else:#新pin与校验pin不一致
                                dlg_tip_hWnd=self.find_subWindow(str_tipTitle)
                                rect = RECT()
                                ctypes.windll.user32.GetWindowRect(dlg_tip_hWnd,ctypes.byref(rect))  # 获取对话框相对屏幕的坐标位置
                                pag.moveTo(rect.left + 20, rect.top + 20)                              
                                pag.typewrite(['enter'])
                                #pag.press('enter') #弹框中仅有确认按钮,点击确认后回到密码输入框等待输入新密码及验证密码                                    
                                time.sleep(0.5)
                                logger.warning('关闭新pin与校验pin不一致提示框，回到输入密码框，要求重新输入新密码和校验密码.核对现象后，关闭输入密码框以结束本次流程')
                                self.DlgBtnClick(dlg_hWnd,2)  #关闭输入密码框，已结束本次操作
                                #self.inputPinFunc(2,newPinStr,verifyPinStr,'')                                             
            elif self.find_subWindow(str_tipTitle):
                    logger.warning('Pin Locked!')
                    dlg_hWnd=self.find_subWindow(str_tipTitle)
                    self.DlgBtnClick(dlg_hWnd,2)   
            else:
                logger.error("ChangePin Exception:not found the window" + str_title)
            
            #获取IE页面返回码
            WebDriverWait(self.browser, 5).until(lambda x: 0 < len(x.find_element_by_id("ResultChangePin").get_attribute('value')))                                                           
            return textAreaResultChangePin.get_attribute('value')    
        except Exception as e:
            tempExcept = re.sub(re.compile('\s+'), ' ', str(e))
            str_excep1_one = '''Alert Text: Message: Modal dialog present '''
            if operator.eq(tempExcept, str_excep1_one):
                return textAreaResultChangePin.get_attribute('value')
            else:
                logger.error("Exception- %s ", str(e))
                return
        return 
        
    def GMCreatePKCS10(self, DN_info, str_title, str_verifyPin,inputBtnType=0,ErrBtnType=0,str_tipTitle=str_verifyTitle):     #是否弹出密码认证框  isBombBox  True:弹出
        '''''
                    生成P10包
        '''''
        '''
        inputBtnType: 输入密码框上0表示确认，1表示取消，2表示关闭“x”,默认是0
        ErrBtnType:错误密码框上0表示确认，1表示取消，2表示关闭“x”，默认是0
        ''' 
        try:
            #global textAreaResultGMCreatePKCS10
            #定位鼠标位置，确保鼠标焦点定位在对话框上
            self.mouseFocus_locate()
            #初始化变量
            textAreaResultGMCreatePKCS10 = self.browser.find_element_by_id("ResultGMCreatePKCS10")
            textAreaResultGMCreatePKCS10.clear()
            textReqinfo = self.browser.find_element_by_id("GenData")
            textReqinfo.clear()
            #测试开始
            if None != DN_info or '' != DN_info:
                textReqinfo.click() 
                content='document.getElementById("GenData").value = "%s"' % DN_info             
                self.browser.execute_script(content)  
                             
            btnGMCreatePKCS10C = self.browser.find_element_by_id("GMCreatePKCS10C")
            btnGMCreatePKCS10C.click()
            time.sleep(1)
            
            if 2 <= GL.TestingRange and GL.TestingRange <= 3:
                WebDriverWait(self.browser, 5).until(lambda x: 0 < len(x.find_element_by_id("ResultGMCreatePKCS10").get_attribute('value')))
                return textAreaResultGMCreatePKCS10.get_attribute('value')
            
            elif self.find_subWindow(str_title):                #输入指定密码                
                dlg_hWnd=self.find_subWindow(str_title)                
#                 self.mouseFocus_locate()
#                 pag.click()
#                 
#                 rect=RECT()
#                 ctypes.windll.user32.GetWindowRect(dlg_hWnd, ctypes.byref(rect)) #获取对话框相对屏幕的坐标位置
#                 pag.click(rect.left+20, rect.top+20)
                                
                self.inputPinFunc(1,str_verifyPin)
                if len(str_verifyPin) <6:
                    logger.warning('密码长度过短,无法继续操作!核对以上现象后,关闭密码输入框以结束本次流程')
                    self.DlgBtnClick(dlg_hWnd,2)
                    WebDriverWait(self.browser, 5).until(lambda x: 0 < len(x.find_element_by_id("ResultGMCreatePKCS10").get_attribute('value')))
                    return textAreaResultGMCreatePKCS10.get_attribute('value')  
                #确认键
                contiMark=self.DlgBtnClick(dlg_hWnd,inputBtnType)
                if contiMark:       #仅按确认键流程后才有剩余判断框流程   
                    #用户提示  
                    resp_title= str_tipTitle       #窗口名称
                    while operator.eq(str_tipTitle,resp_title):
                        resp_title=''
                        dlg_tip_hWnd = self.find_subWindow(str_tipTitle)
                        resp_title = win32gui.GetWindowText(dlg_tip_hWnd)
                        if not  win32gui.IsWindowVisible(dlg_tip_hWnd):
                            break 
                        if operator.eq(str_tipTitle,resp_title):#确认对话框已弹出
                            #第1步：先判断pin是否正确：正确，继续；否则错误提示框    
                            #第2步：错误提示框点击<是>，重新输入Pin，否则结束本次操作:
                            #第3步：等待生成P10                            
                            #判断弹框中有无按钮
                            dlg_tip_hWnd=win32gui.FindWindow(None, resp_title)
                            btn= win32gui.FindWindowEx(dlg_tip_hWnd, None, 'Button', None) 
                            if btn>0:
                                #错误提示框 
                                rect=RECT()
                                ctypes.windll.user32.GetWindowRect(dlg_tip_hWnd, ctypes.byref(rect)) #获取对话框相对屏幕的坐标位置
                                pag.moveTo(rect.left+20, rect.top+20)
                                self.DlgBtnClick(dlg_tip_hWnd,ErrBtnType)
                                if  0 ==ErrBtnType and True == self.find_subWindow(str_title, resp_title,1):            
                                    #dlg_hWnd=win32gui.FindWindow(None,str_title)
                                    dlg_hWnd=self.find_subWindow(str_title)
                                    self.DlgBtnClick(dlg_hWnd,2)  #结束本次操作 
                            else:
                                logger.warning('密码剩余2/1次,等待U盾按键操作  或 生成P10进行中...')   
                                time.sleep(1)                             
            
            elif self.find_subWindow(str_tipTitle):               
                    logger.warning('Pin Locked!')
                    dlg_hWnd=self.find_subWindow(str_tipTitle)
                    self.DlgBtnClick(dlg_hWnd,2)
                    WebDriverWait(self.browser, 5).until(lambda x: 0 < len(x.find_element_by_id("ResultGMCreatePKCS10").get_attribute('value')))
                    return textAreaResultGMCreatePKCS10.get_attribute('value')

            else:
                logger.error("Exception:not found the window" + str_title)
            #获取IE页面返回码
            WebDriverWait(self.browser, 5).until(lambda x: 0 < len(x.find_element_by_id("ResultGMCreatePKCS10").get_attribute('value')))
            return textAreaResultGMCreatePKCS10.get_attribute('value')   
        except Exception as e:
            tempExcept = re.sub(re.compile('\s+'), ' ', str(e))
            str_excep1_one = '''Alert Text: Message: Modal dialog present '''
            if operator.eq(tempExcept, str_excep1_one):
                return textAreaResultGMCreatePKCS10.get_attribute('value')
            else:
                logger.error("Exception- %s ", str(e))
                return

    def P102P7(self,base64P10=''):
        '''''
        P10转P7
        '''''
        try:
            #定位鼠标位置，确保鼠标焦点定位在对话框上
            self.mouseFocus_locate()
            textAreaResultGMCreatePKCS10 = self.browser.find_element_by_id("ResultGMCreatePKCS10")
            p10_vlaue = textAreaResultGMCreatePKCS10.get_attribute('value')
            if p10_vlaue != "":
                textAreaResultGMCreatePKCS10.send_keys(Keys.CONTROL,'a') #选择文档
                textAreaResultGMCreatePKCS10.send_keys(Keys.CONTROL,'c') #复制
                time.sleep(0.1)
                ToolHwnd=open_window(AuxTool)
                rect=RECT()
                ctypes.windll.user32.GetWindowRect(ToolHwnd, ctypes.byref(rect)) #获取对话框相对屏幕的坐标位置
                testView=ToolConvert(ToolHwnd, rect)
                testView.FuncP102P7()     #调用P10->P7
                '''      
                os.startfile(AuxTool)
                #运行录制的autoIT脚本
                os.system(AutoItExe)
                time.sleep(2)
                '''                
                #关闭p10转p7工具
                os.system('taskkill /F /IM IcbcOcxAuxTool_rls.exe')
                #获取IE页面返回码
                WebDriverWait(self.browser, 10).until(lambda x: 0 <= len(x.find_element_by_id("ResultGMCreatePKCS10").get_attribute('value')))
                
                textCertInfo = self.browser.find_element_by_id('CertData')
                textCertInfo.clear()
                textCertInfo.send_keys(Keys.CONTROL,'v') #粘贴
                return True
        except Exception as e:
            logger.error("P102P7 Exception- %s ",str(e))
        return False

    def GMWritePKCS7(self, p7CertData=None):  # type=0 证书信息不随意输入):
        '''''
                    写入证书
        '''''
        try:
            #定位鼠标位置，确保鼠标焦点定位在对话框上
            self.mouseFocus_locate()
            #初始化
            textAreaResultGMWritePKCS7 = self.browser.find_element_by_id("ResultGMWritePKCS7")
            textAreaResultGMWritePKCS7.clear()
            if None != p7CertData and '' != p7CertData:
                Certinfo = p7CertData
                content='document.getElementById("CertData").value = "%s"' % Certinfo             
                self.browser.execute_script(content)      
            #测试开始
            btnGMWritePKCS7C = self.browser.find_element_by_id("GMWritePKCS7C")
            btnGMWritePKCS7C.click()
            #获取IE页面返回码
            WebDriverWait(self.browser, 5).until(lambda x: 0 <= len(x.find_element_by_id("ResultGMWritePKCS7").get_attribute('value')))
            return textAreaResultGMWritePKCS7.get_attribute('value')  
              
        except Exception as e:
            logger.error("GMWritePKCS7 Exception- %s ",str(e))
        return False
    
    def get_DispSign(self,str_certDn ,str_hashId,str_xmlData,str_DispData,str_Pin,inputBtnType=0,ErrBtnType=0, str_title=str_title,str_tipTitle=str_verifyTitle,str_signTitle=str_signTitle):
        '''''
                        显示签名测试
        '''''
        '''
        inputBtnType: 输入密码框上0表示确认，1表示取消，2表示关闭“x”,默认是0
        ErrBtnType:错误密码框上0表示确认，1表示取消，2表示关闭“x”，默认是0
        ''' 
        try: 
            #定位鼠标位置，确保鼠标焦点定位在对话框上
            self.mouseFocus_locate()
            #初始化
            textSignerDN = self.browser.find_element_by_id('SignerDN')
            textSignerDN.clear()
            textHashName = self.browser.find_element_by_id('HashName')
            textHashName.clear()
            textXmlMsg = self.browser.find_element_by_id('XmlMsg')
            textXmlMsg.clear()            
            textKeyMsg = self.browser.find_element_by_id('KeyMsg')
            textKeyMsg.clear() 
            textResultTestGMUsbKeySign = self.browser.find_element_by_id('ResultTestGMUsbKeySign')
            textResultTestGMUsbKeySign.clear()                                   
            #证书DN
            if None != str_certDn:
                textSignerDN.click()
                #textSignerDN.send_keys(str_certDn)
                content='document.getElementById("SignerDN").value = "%s"' % str_certDn             
                self.browser.execute_script(content)
                time.sleep(0.01) 
            #hashID
            if None != str_hashId:
                textHashName.click()
                #textHashName.send_keys(str_hashId)
                content='document.getElementById("HashName").value = "%s"' % str_hashId 
                self.browser.execute_script(content)
                time.sleep(0.01)                        
            #xml报文
            if None != str_xmlData:            
                textXmlMsg.click()
                #textXmlMsg.send_keys(str_xmlData)
                str_xmlData=re.sub(re.compile('"+'),'\\"',str_xmlData)
                content='document.getElementById("XmlMsg").value = "%s"' % str_xmlData 
                self.browser.execute_script(content)
                time.sleep(0.01)
            #KEY显数据
            if None != str_DispData:  
                textKeyMsg.click()
                str_DispData=re.sub(re.compile('\n+'),'\\\\n',str_DispData)
                content='document.getElementById("KeyMsg").value = "%s"' % str_DispData 
                self.browser.execute_script(content)                     
                time.sleep(0.01)             
            #签名
            btnGMSign = self.browser.find_element_by_id('GMSign')
            ActionChains(self.browser).drag_and_drop(textKeyMsg, btnGMSign).perform() #鼠标拖拽，保证目标按钮处于可见视野范围内
            btnGMSign.click()
            time.sleep(1) 
                                          
            #输入PIN码
            if 2 <= GL.TestingRange and GL.TestingRange <= 3:
                WebDriverWait(self.browser, 5).until(lambda x: 0 < len(x.find_element_by_id("ResultTestGMUsbKeySign").get_attribute('value')))
                return textResultTestGMUsbKeySign.get_attribute('value')
                     
            elif self.find_subWindow(str_title):                                    
                #输入指定密码          
                dlg_hWnd=self.find_subWindow(str_title)
#                 self.mouseFocus_locate()
#                 pag.click()
#                    
#                 rect=RECT()
#                 ctypes.windll.user32.GetWindowRect(dlg_hWnd, ctypes.byref(rect)) #获取对话框相对屏幕的坐标位置
#                 pag.click(rect.left+20, rect.top+20)                                
                self.inputPinFunc(1,str_Pin)
                if len(str_Pin) <6:
                    logger.warning('密码长度过短,无法继续操作!核对以上现象后,关闭密码输入框以结束本次流程')
                    self.DlgBtnClick(dlg_hWnd,2)
                    WebDriverWait(self.browser, 5).until(lambda x: 0 < len(x.find_element_by_id("ResultTestGMUsbKeySign").get_attribute('value')))
                    return textResultTestGMUsbKeySign.get_attribute('value')  
                #确认键
                time.sleep(0.2)
                contiMark=self.DlgBtnClick(dlg_hWnd,inputBtnType)
                if contiMark:       #仅按确认键流程后才有剩余判断框流程   
                    #第1步：先判断pin是否正确：正确，继续；否则错误提示框    
                    #第2步：错误提示框点击<是>，重新输入Pin，否则结束本次操作:
                    #第3步：签名                            
                    #判断弹框中有无按钮       
                    resp_title= str_signTitle     #窗口名称                    
                    while operator.eq(str_signTitle,resp_title) or operator.eq(str_tipTitle,resp_title):
                        resp_title=''
                        dlg_tip_hWnd = self.find_subWindow(str_signTitle)  
                        if not dlg_tip_hWnd>0:
                            dlg_tip_hWnd = self.find_subWindow(str_tipTitle)
                            if not dlg_tip_hWnd>0:
                                #未弹框情况
                                break
                        resp_title = win32gui.GetWindowText(dlg_tip_hWnd)
                        dlg_tip_hWnd=win32gui.FindWindow(None, resp_title)                                              
                        btn= win32gui.FindWindowEx(dlg_tip_hWnd, None, 'Button', None) 
                        if btn>0:
                            #错误提示框 
                            rect=RECT()
                            ctypes.windll.user32.GetWindowRect(dlg_tip_hWnd, ctypes.byref(rect)) #获取对话框相对屏幕的坐标位置
                            pag.moveTo(rect.left+20, rect.top+20)
                            self.DlgBtnClick(dlg_tip_hWnd,ErrBtnType)
                            if  0 ==ErrBtnType and self.find_subWindow(str_title):            
                                dlg_hWnd=self.find_subWindow(str_title)
                                self.DlgBtnClick(dlg_hWnd,2)  #结束本次操作 
                        else:
                            logger.warning('密码剩余2/1次,等待U盾按键操作  或 签名进行中...')
                            time.sleep(1)
            
            elif self.find_subWindow(str_tipTitle):                
                logger.warning('Pin Locked!')
                dlg_hWnd=self.find_subWindow(str_tipTitle)
                self.DlgBtnClick(dlg_hWnd,2)            
            else:
                logger.error("DispSign:not found the UI about Pin")                                         
            #获取IE页面返回码
            WebDriverWait(self.browser, 5).until(lambda x: 0 < len(x.find_element_by_id("ResultTestGMUsbKeySign").get_attribute('value')))
            return textResultTestGMUsbKeySign.get_attribute('value')
        except Exception as e:
            tempExcept = re.sub(re.compile('\s+'), ' ', str(e))
            str_excep1_one = '''Alert Text: Message: Modal dialog present '''
            if operator.eq(tempExcept, str_excep1_one):
                return textResultTestGMUsbKeySign.get_attribute('value')
            else:
                logger.error("DispSign Exception- %s ", str(e))
                return
    
    def get_FileSign(self,str_certDn,str_hashId,str_xmlData,str_DispData,str_batpath,str_p7path,str_Pin,inputBtnType=0,ErrBtnType=0, str_title=str_title,str_tipTitle=str_verifyTitle):                      
        '''''
                        文件签名测试
        '''''
        '''
        inputBtnType: 输入密码框上0表示确认，1表示取消，2表示关闭“x”,默认是0
        ErrBtnType:错误密码框上0表示确认，1表示取消，2表示关闭“x”，默认是0
        ''' 
        try: 
            #定位鼠标位置，确保鼠标焦点定位在对话框上
            self.mouseFocus_locate()
            #初始化
            textSignerDN = self.browser.find_element_by_id('SignerDN')
            textSignerDN.clear()
            textHashName = self.browser.find_element_by_id('HashName')
            textHashName.clear()
            textXmlMsg = self.browser.find_element_by_id('XmlMsg')
            textXmlMsg.clear()            
            textKeyMsg = self.browser.find_element_by_id('KeyMsg')
            textKeyMsg.clear() 
            textBatFileMsg = self.browser.find_element_by_id('NewVal')
            textBatFileMsg.clear()
            textP7FileMsg = self.browser.find_element_by_id('FileP7')
            textP7FileMsg.clear()                         
            textResultTestGMUsbKeySign = self.browser.find_element_by_id('ResultTestGMUsbKeySign')
            textResultTestGMUsbKeySign.clear()                                   
            #证书DN
            if None != str_certDn and '' != str_certDn:
                textSignerDN.click()
                #textSignerDN.send_keys(str_certDn)
                content='document.getElementById("SignerDN").value = "%s"' % str_certDn             
                self.browser.execute_script(content)
                time.sleep(0.01) 
            #hashID
            if None != str_hashId  and '' != str_hashId:
                textHashName.click()
                content='document.getElementById("HashName").value = "%s"' % str_hashId 
                self.browser.execute_script(content)
                time.sleep(0.01)                        
            #xml报文
            if None != str_xmlData  and '' != str_xmlData:            
                textXmlMsg.click()
                str_xmlData=re.sub(re.compile('"+'),'\\"',str_xmlData)
                content='document.getElementById("XmlMsg").value = "%s"' % str_xmlData 
                self.browser.execute_script(content)
                time.sleep(0.01)
            #KEY显数据
            if None != str_DispData and '' != str_DispData:  
                textKeyMsg.click()
                str_DispData=re.sub(re.compile('\n+'),'\\\\n',str_DispData)
                content='document.getElementById("KeyMsg").value = "%s"' % str_DispData 
                self.browser.execute_script(content)                     
                time.sleep(0.01) 
            #批量文件路径
            if '' != str_batpath and None != str_batpath: 
                textBatFileMsg.click()
                str=re.sub(re.compile('\\\+'),'\\"',str_batpath)
                str_batpath=re.sub(re.compile('"+'),'\\\\',str)  
                content='document.getElementById("NewVal").value = "%s"' % str_batpath 
                self.browser.execute_script(content)                     
                time.sleep(0.01)
            #P7文件路径
            if '' != str_p7path and None != str_p7path: 
                textP7FileMsg.click()
                str=re.sub(re.compile('\\\+'),'\\"',str_p7path)
                str_p7path=re.sub(re.compile('"+'),'\\\\',str) 
                content='document.getElementById("FileP7").value = "%s"' % str_p7path 
                self.browser.execute_script(content)                     
                time.sleep(0.01)                       
            #签名
            btnGMFileSign = self.browser.find_element_by_id('GMSignFile')
            ActionChains(self.browser).drag_and_drop(textP7FileMsg, btnGMFileSign).perform() #鼠标拖拽，保证目标按钮处于可见视野范围内
            btnGMFileSign.click()  
            time.sleep(1)   
                                      
            #输入PIN码
            if 2 <= GL.TestingRange and GL.TestingRange <= 3:
                WebDriverWait(self.browser, 5).until(lambda x: 0 < len(x.find_element_by_id("ResultTestGMUsbKeySign").get_attribute('value')))
                return textResultTestGMUsbKeySign.get_attribute('value')
                     
            elif self.find_subWindow(str_title):                                                      
                #输入指定密码
                dlg_hWnd=self.find_subWindow(str_title)
#                 self.mouseFocus_locate()
#                 pag.click()
#                 
#                 rect=RECT()
#                 ctypes.windll.user32.GetWindowRect(dlg_hWnd, ctypes.byref(rect)) #获取对话框相对屏幕的坐标位置
#                 pag.click(rect.left+20, rect.top+20)  
             
                self.inputPinFunc(1,str_Pin)                
                if len(str_Pin) <6:
                    logger.warning('密码长度过短,无法继续操作!核对以上现象后,关闭密码输入框以结束本次流程')
                    self.DlgBtnClick(dlg_hWnd,2)
                    WebDriverWait(self.browser, 5).until(lambda x: 0 < len(x.find_element_by_id("ResultTestGMUsbKeySign").get_attribute('value')))
                    return textResultTestGMUsbKeySign.get_attribute('value')
                #确认键
                time.sleep(0.2)
                contiMark=self.DlgBtnClick(dlg_hWnd,inputBtnType)
                if contiMark:       #仅按确认键流程后才有剩余判断框流程   
                    #第1步：先判断pin是否正确：正确，继续；否则错误提示框    
                    #第2步：错误提示框点击<是>，重新输入Pin，否则结束本次操作:
                    #第3步：签名                            
                    #判断弹框中有无按钮       
                    resp_title= str_signTitle     #窗口名称                    
                    while operator.eq(str_signTitle,resp_title) or operator.eq(str_tipTitle,resp_title):
                        resp_title=''
                        dlg_tip_hWnd = self.find_subWindow(str_signTitle)
                        if not dlg_tip_hWnd>0:
                            dlg_tip_hWnd = self.find_subWindow(str_tipTitle) 
                            if not dlg_tip_hWnd>0:
                                #未弹框情况
                                break
                        resp_title = win32gui.GetWindowText(dlg_tip_hWnd)  
                        dlg_tip_hWnd=win32gui.FindWindow(None, resp_title)                  
                        btn= win32gui.FindWindowEx(dlg_tip_hWnd, None, 'Button', None) 
                        if btn>0:
                            #错误提示框 
                            rect=RECT()
                            ctypes.windll.user32.GetWindowRect(dlg_tip_hWnd, ctypes.byref(rect)) #获取对话框相对屏幕的坐标位置
                            pag.moveTo(rect.left+20, rect.top+20)
                            self.DlgBtnClick(dlg_tip_hWnd,ErrBtnType)
                            if  0 ==ErrBtnType and self.find_subWindow(str_title):            
                                dlg_hWnd=win32gui.FindWindow(None,str_title)
                                self.DlgBtnClick(dlg_hWnd,2)  #结束本次操作 
                        else:
                            logger.warning('密码剩余2/1次,等待U盾按键操作  或 签名进行中...')
                            time.sleep(1)
            elif self.find_subWindow(str_tipTitle):
                #Pin Locked!情况
                logger.warning('Pin Locked!')
                dlg_hWnd=self.find_subWindow(str_tipTitle)
                self.DlgBtnClick(dlg_hWnd,2)
            else:
                logger.error("FileSign Exception:not found the window" + str_title)                                         
            #获取IE页面返回码                         
            WebDriverWait(self.browser, 5).until(lambda x: 0 < len(x.find_element_by_id("ResultTestGMUsbKeySign").get_attribute('value')))
            return textResultTestGMUsbKeySign.get_attribute('value')
        except Exception as e:
            tempExcept = re.sub(re.compile('\s+'), ' ', str(e))
            str_excep1_one = '''Alert Text: Message: Modal dialog present '''
            if operator.eq(tempExcept, str_excep1_one):
                return textResultTestGMUsbKeySign.get_attribute('value')
            else:
                logger.error("FileSign Exception- %s ", str(e))
                return
    def setImportEncCertInfo(self, DN_info, str_title, str_verifyPin, AdminKeyID, str_AdminKey):
        '''''
                        使用转换工具获取导入加密证书信息
        '''''
        try:
            #定位鼠标位置，确保鼠标焦点定位在对话框上
            self.mouseFocus_locate()
            #获取P10信息
            base64P10=self.GMCreatePKCS10(DN_info,str_title,str_verifyPin)
            if '00' == AdminKeyID:   
                #国密旧体系
                #初始化  
                textAreaGMGetTemKey = self.browser.find_element_by_id("ResultGMGetTemKey")
                textAreaGMGetTemKey.clear() 
                btnGMGetTemKey = self.browser.find_element_by_id("GMGetTemKey")
                btnGMGetTemKey.click()
                time.sleep(1)
                inputBtnType=0
                ErrBtnType=0
                if 2 <= GL.TestingRange and GL.TestingRange <= 3:
                    WebDriverWait(self.browser, 5).until(lambda x: 0 < len(x.find_element_by_id("ResultGMGetTemKey").get_attribute('value')))
                    return textAreaGMGetTemKey.get_attribute('value')
                
                elif self.find_subWindow(str_title):                #输入指定密码                
                    dlg_hWnd=self.find_subWindow(str_title)                
    #                 self.mouseFocus_locate()
    #                 pag.click()
    #                 
    #                 rect=RECT()
    #                 ctypes.windll.user32.GetWindowRect(dlg_hWnd, ctypes.byref(rect)) #获取对话框相对屏幕的坐标位置
    #                 pag.click(rect.left+20, rect.top+20)
                                    
                    self.inputPinFunc(1,str_verifyPin)
                    if len(str_verifyPin) <6:
                        logger.warning('密码长度过短,无法继续操作!核对以上现象后,关闭密码输入框以结束本次流程')
                        self.DlgBtnClick(dlg_hWnd,2)
                        WebDriverWait(self.browser, 5).until(lambda x: 0 < len(x.find_element_by_id("ResultGMGetTemKey").get_attribute('value')))
                        return textAreaGMGetTemKey.get_attribute('value')  
                    #确认键
                    contiMark=self.DlgBtnClick(dlg_hWnd,inputBtnType)
                    if contiMark:       #仅按确认键流程后才有剩余判断框流程   
                        #用户提示  
                        resp_title= str_title       #窗口名称
                        while operator.eq(str_title,resp_title):
                            resp_title=''
                            dlg_tip_hWnd = self.find_subWindow(str_title)
                            resp_title = win32gui.GetWindowText(dlg_tip_hWnd)
                            if not  win32gui.IsWindowVisible(dlg_tip_hWnd):
                                break 
                            if operator.eq(str_title,resp_title):#确认对话框已弹出
                                #第1步：先判断pin是否正确：正确，继续；否则错误提示框    
                                #第2步：错误提示框点击<是>，重新输入Pin，否则结束本次操作:
                                #第3步：等待生成P10                            
                                #判断弹框中有无按钮
                                dlg_tip_hWnd=win32gui.FindWindow(None, resp_title)
                                btn= win32gui.FindWindowEx(dlg_tip_hWnd, None, 'Button', None) 
                                if btn>0:
                                    #错误提示框 
                                    rect=RECT()
                                    ctypes.windll.user32.GetWindowRect(dlg_tip_hWnd, ctypes.byref(rect)) #获取对话框相对屏幕的坐标位置
                                    pag.moveTo(rect.left+20, rect.top+20)
                                    self.DlgBtnClick(dlg_tip_hWnd,ErrBtnType)
                                    if  0 ==ErrBtnType and True == self.find_subWindow(str_title, resp_title,1):            
                                        #dlg_hWnd=win32gui.FindWindow(None,str_title)
                                        dlg_hWnd=self.find_subWindow(str_title)
                                        self.DlgBtnClick(dlg_hWnd,2)  #结束本次操作 
                                else:
                                    logger.warning('密码剩余2/1次,等待U盾按键操作  或 生成P10进行中...')   
                                    time.sleep(1)                             
                
                elif self.find_subWindow(str_title):               
                        logger.warning('Pin Locked!')
                        dlg_hWnd=self.find_subWindow(str_title)
                        self.DlgBtnClick(dlg_hWnd,2)
                        WebDriverWait(self.browser, 5).until(lambda x: 0 < len(x.find_element_by_id("ResultGMGetTemKey").get_attribute('value')))
                        return textAreaGMGetTemKey.get_attribute('value')
    
                else:
                    logger.error("Exception:not found the window" + str_title)    
                WebDriverWait(self.browser, 5).until(lambda x: 0 <= len(x.find_element_by_id("ResultGMGetTemKey").get_attribute('value')))
                TemKeyorRand_value = textAreaGMGetTemKey.get_attribute('value')
            else:
                #国密新体系
                textAreaResultGMBankEncGetRand = self.browser.find_element_by_id("ResultGMBankEncGetRand")
                textAreaResultGMBankEncGetRand.clear() 
                btnGMGetTemKey = self.browser.find_element_by_id("GMBankEncGetRand")
                btnGMGetTemKey.click()
                time.sleep(1)
                inputBtnType=0
                ErrBtnType=0
                if 2 <= GL.TestingRange and GL.TestingRange <= 3:
                    WebDriverWait(self.browser, 5).until(lambda x: 0 < len(x.find_element_by_id("ResultGMBankEncGetRand").get_attribute('value')))
                    return textAreaResultGMBankEncGetRand.get_attribute('value')
                
                elif self.find_subWindow(str_title):                #输入指定密码                
                    dlg_hWnd=self.find_subWindow(str_title)                
    #                 self.mouseFocus_locate()
    #                 pag.click()
    #                 
    #                 rect=RECT()
    #                 ctypes.windll.user32.GetWindowRect(dlg_hWnd, ctypes.byref(rect)) #获取对话框相对屏幕的坐标位置
    #                 pag.click(rect.left+20, rect.top+20)
                                    
                    self.inputPinFunc(1,str_verifyPin)
                    if len(str_verifyPin) <6:
                        logger.warning('密码长度过短,无法继续操作!核对以上现象后,关闭密码输入框以结束本次流程')
                        self.DlgBtnClick(dlg_hWnd,2)
                        WebDriverWait(self.browser, 5).until(lambda x: 0 < len(x.find_element_by_id("ResultGMBankEncGetRand").get_attribute('value')))
                        return textAreaResultGMBankEncGetRand.get_attribute('value')  
                    #确认键
                    contiMark=self.DlgBtnClick(dlg_hWnd,inputBtnType)
                    if contiMark:       #仅按确认键流程后才有剩余判断框流程   
                        #用户提示  
                        resp_title= str_title       #窗口名称
                        while operator.eq(str_title,resp_title):
                            resp_title=''
                            dlg_tip_hWnd = self.find_subWindow(str_title)
                            resp_title = win32gui.GetWindowText(dlg_tip_hWnd)
                            if not  win32gui.IsWindowVisible(dlg_tip_hWnd):
                                break 
                            if operator.eq(str_title,resp_title):#确认对话框已弹出
                                #第1步：先判断pin是否正确：正确，继续；否则错误提示框    
                                #第2步：错误提示框点击<是>，重新输入Pin，否则结束本次操作:
                                #第3步：等待生成P10                            
                                #判断弹框中有无按钮
                                dlg_tip_hWnd=win32gui.FindWindow(None, resp_title)
                                btn= win32gui.FindWindowEx(dlg_tip_hWnd, None, 'Button', None) 
                                if btn>0:
                                    #错误提示框 
                                    rect=RECT()
                                    ctypes.windll.user32.GetWindowRect(dlg_tip_hWnd, ctypes.byref(rect)) #获取对话框相对屏幕的坐标位置
                                    pag.moveTo(rect.left+20, rect.top+20)
                                    self.DlgBtnClick(dlg_tip_hWnd,ErrBtnType)
                                    if  0 ==ErrBtnType and True == self.find_subWindow(str_title, resp_title,1):            
                                        #dlg_hWnd=win32gui.FindWindow(None,str_title)
                                        dlg_hWnd=self.find_subWindow(str_title)
                                        self.DlgBtnClick(dlg_hWnd,2)  #结束本次操作 
                                else:
                                    logger.warning('密码剩余2/1次,等待U盾按键操作  或 生成P10进行中...')   
                                    time.sleep(1)                             
                
                elif self.find_subWindow(str_title):               
                        logger.warning('Pin Locked!')
                        dlg_hWnd=self.find_subWindow(str_title)
                        self.DlgBtnClick(dlg_hWnd,2)
                        WebDriverWait(self.browser, 5).until(lambda x: 0 < len(x.find_element_by_id("ResultGMBankEncGetRand").get_attribute('value')))
                        return textAreaResultGMBankEncGetRand.get_attribute('value')
    
                else:
                    logger.error("Exception:not found the window" + str_title)    
                WebDriverWait(self.browser, 5).until(lambda x: 0 <= len(x.find_element_by_id("ResultGMBankEncGetRand").get_attribute('value')))
                TemKeyorRand_value = textAreaResultGMBankEncGetRand.get_attribute('value')
            #定位鼠标位置，确保鼠标焦点定位在对话框上
            ToolHwnd=open_window(AuxTool)
            rect=RECT()
            ctypes.windll.user32.GetWindowRect(ToolHwnd, ctypes.byref(rect)) #获取对话框相对屏幕的坐标位置
            testView=ToolConvert(ToolHwnd, rect)
            testView.FuncsetImportEncCertInfo(base64P10, AdminKeyID, str_AdminKey, TemKeyorRand_value)
            #关闭p10转p7工具
            os.system('taskkill /F /IM IcbcOcxAuxTool_rls.exe')
            
            textCertData = self.browser.find_element_by_id('CertData')
            textCertData.clear()
            textCertData.send_keys(Keys.CONTROL,'v') #粘贴
            #P7信息分割
            str_textAll=textCertData.get_attribute('value')
            str_list=str_textAll.split()
            return str_list
        except Exception as e:
            logger.error("setImportEncCertInfo- %s ",str(e))
        return False
    def GMWritePKCS7Enc(self, p7CertData, EncData, ServerRand=None):  
        '''''
                        导入加密证书
        '''''
        try:
            #定位鼠标位置，确保鼠标焦点定位在对话框上
            self.mouseFocus_locate()
            #初始化
            textAreaResultGMWritePKCS7 = self.browser.find_element_by_id("ResultGMWritePKCS7")
            textAreaResultGMWritePKCS7.clear()
            textAreaCertData = self.browser.find_element_by_id("CertData")
            textAreaCertData.clear()
            textAreaEncData = self.browser.find_element_by_id("EncData")
            textAreaEncData.clear()
            textAreaServerRand = self.browser.find_element_by_id("ServerRand")
            textAreaServerRand.clear()
            #证书信息
            if None != p7CertData and '' != p7CertData:
                Certinfo = p7CertData
                content='document.getElementById("CertData").value = "%s"' % Certinfo             
                self.browser.execute_script(content) 
            #加密信息
            if None != EncData and '' != EncData:
                EncDatainfo = EncData
                content='document.getElementById("EncData").value = "%s"' % EncDatainfo             
                self.browser.execute_script(content)
            #随机数
            if None != ServerRand and '' != ServerRand:
                Randinfo = ServerRand
                content='document.getElementById("ServerRand").value = "%s"' % Randinfo             
                self.browser.execute_script(content)     
            #测试开始
            btnGMWritePKCS7Enc = self.browser.find_element_by_id("GMWritePKCS7Enc")
            btnGMWritePKCS7Enc.click()
            #获取IE页面返回码
            WebDriverWait(self.browser, 5).until(lambda x: 0 <= len(x.find_element_by_id("ResultGMWritePKCS7").get_attribute('value')))
            return textAreaResultGMWritePKCS7.get_attribute('value')  
              
        except Exception as e:
            logger.error("GMWritePKCS7Enc Exception- %s ",str(e))
        return False
          
    def setAdminKey(self,oldAdminKey,newAdminKey,olgAlgId,newAlgId,counts): 
        '''''
                        使用转换工具设置保护密钥
        '''''
        '''
                    参数说明: 
            oldAdminKey:旧保护密钥值
            newAdminKey:新保护密钥值
            olgAlgId:旧保护密钥算法Id
            newAlgId:新保护密钥算法Id
            counts:更新序号，仅在新体系更新时有效
        '''
        try:
            #定位鼠标位置，确保鼠标焦点定位在对话框上
            ToolHwnd=open_window(AuxTool)
            logger.warning("ToolHwnd=%s", ToolHwnd)
            rect=RECT()
            ctypes.windll.user32.GetWindowRect(ToolHwnd, ctypes.byref(rect)) #获取对话框相对屏幕的坐标位置
            testView=ToolConvert(ToolHwnd, rect)
            newAdminKey=testView.FuncSetAdminKey(oldAdminKey,newAdminKey,olgAlgId,newAlgId,counts)     #调用设置保护密钥
            #关闭p10转p7工具
            os.system('taskkill /F /IM IcbcOcxAuxTool_rls.exe')
            
            textNewAdminKey = self.browser.find_element_by_id('NewAdminKey')
            textNewAdminKey.send_keys(Keys.CONTROL,'v') #粘贴
            return True
        except Exception as e:
            logger.error("setAmdinKey Exception- %s ",str(e))
        return False

    def GMSetNewAmdinKeyC(self,oldAdminKey,newAdminKey,olgAlgId,newAlgId,counts='00',str_newAdminKey=None,str_toolMark=True):  #1:通过setAmdinKey传参； 0：不输入字符
        '''''
                        管理员控件页保护密钥更新
        '''''
        try:
            #定位鼠标位置，确保鼠标焦点定位在对话框上
            self.mouseFocus_locate()
            #初始化
            textAreaResultGMSetNewAmdinKeyC = self.browser.find_element_by_id("ResultSetAdminKey")
            textAreaResultGMSetNewAmdinKeyC.clear()
            textNewAdminKey = self.browser.find_element_by_id('NewAdminKey')
            textNewAdminKey.clear()
            #输入新保护密钥
            if None != str_newAdminKey and '' != str_newAdminKey:
                content='document.getElementById("NewAdminKey").value = "%s"' % str_newAdminKey 
                self.browser.execute_script(content)   
            else:
                if str_toolMark:
                    self.setAdminKey(oldAdminKey,newAdminKey,olgAlgId,newAlgId,counts)
            #测试开始    
            btnGMSetNewAmdinKeyC = self.browser.find_element_by_id("GMSetNewAmdinKey")
            btnGMSetNewAmdinKeyC.click()
            #获取IE页面返回码
            WebDriverWait(self.browser, 5).until(lambda x: 0 <= len(x.find_element_by_id("ResultSetAdminKey").get_attribute('value')))
            return textAreaResultGMSetNewAmdinKeyC.get_attribute('value')              
        except Exception as e:
            logger.error("GMSetNewAmdinKeyC Exception- %s ",str(e))
        return False 
          
    def get_Base64Random(self):
        '''
                   管理员控件获取Base64编码的随机数
        '''        
        try:
            #定位鼠标位置，确保鼠标焦点定位在对话框上
            self.mouseFocus_locate()
            #初始化
            textAreaResultGetUsbkeyRom = self.browser.find_element_by_id("ResultGetUsbkeyRom")           
            textAreaResultGetUsbkeyRom.clear()
            #测试开始
            btnGetUsbkeyRom = self.browser.find_element_by_id("GetUsbkeyRom")
            btnGetUsbkeyRom.click()
            WebDriverWait(self.browser, 5).until(lambda x: 0 <= len(x.find_element_by_id("ResultGetUsbkeyRom").get_attribute('value')))
            strBase64Random=textAreaResultGetUsbkeyRom.get_attribute('value')
            return strBase64Random
        except Exception as e:
            logger.error("Exception- %s ",str(e))
            pass
        return False
  
    def setSecInitData(self,strMediaId,strBase64Random,strAdminKey,strAdminAlgId):
        '''
                    获取安全初始化数据——中间件工具获取               
        '''
        '''
                    参数说明：
            AdminKeyInfo:保护密钥信息数组，元素1表示U盾类型：国密盾-1，非国密盾-0
                                                                                                元素2表示保护密钥算法：00-3DES,01-AES,02-SM4
            main_url:主流程控件测试页面，本接口应指国密管理员控件页
            main_win_title: 主流程控件测试页面标题，本接口应指国密管理员控件页面
            minor_url：辅助测试页面，用以获取中间过程  ，本接口应指国密用户控件页   
            minor_win_title: 辅助测试页面标题，本接口应指国密用户控件页                                                                                            
        '''
        try:
            '''
            if False == AdminKeyInfo[0] or '00' == AdminKeyInfo[1]:
                logger.warning('请选择国密新体系盾进行！') 
                return 
            '''
            #定位鼠标位置，确保鼠标焦点定位在对话框上
            self.mouseFocus_locate()          
            ToolHwnd=open_window(AuxTool)
            rect=RECT()
            ctypes.windll.user32.GetWindowRect(ToolHwnd, ctypes.byref(rect)) #获取对话框相对屏幕的坐标位置
            testView=ToolConvert(ToolHwnd, rect)
            testView.FuncSecInitCard(strMediaId,strAdminKey,strBase64Random,strAdminAlgId)   #调用P10->P7              
                      
            #关闭p10转p7工具
            os.system('taskkill /F /IM IcbcOcxAuxTool_rls.exe')
            time.sleep(0.5)            
            #获取IE页面返回码
            #WebDriverWait(self.browser, 5).until(lambda x: 0 <= len(x.find_element_by_id("ResultGMCreatePKCS10").get_attribute('value')))
            textInitData = self.browser.find_element_by_id("Order")
            textInitData.clear()
            textInitData.click()
            textInitData.send_keys(Keys.CONTROL,'v') #粘贴                        
        except Exception as e:
            logger.error("SecInitData Exception- %s ",str(e))
        return False
        
    def get_SecInitCard(self,AdminKeyInfo, str_MediaID=CardNum, str_initData=None,str_toolMark=True,str_tipTitle=str_verifyTitle):
        '''
                   管理员控件安全初始化
        '''
        '''
                参数说明：str_initData：初始化数据
                str_toolMark：是否调用中间件工具获取初始化数据，此时要求str_initData为空
                AdminKeyInfo:保护密钥信息数组，表示保护密钥算法：00-3DES,01-AES,02-SM4
                str_MediaID:介质号 
        '''
        try:
            #定位鼠标位置，确保鼠标焦点定位在对话框上
            self.mouseFocus_locate()
          
            #初始化变量
            textInitData = self.browser.find_element_by_id("Order")
            textInitData.clear()               
            #测试开始    
            if None == str_initData or '' ==str_initData:
                if str_toolMark:
                    strBase64Random=self.get_Base64Random()                                    
                    strAdminKey=AmdinKey_AES_new
                    strAdminAlgId='AES'
                    if '02' == AdminKeyInfo:
                        strAdminKey=AmdinKey_SM4
                        strAdminAlgId='SM4'                    
                    self.setSecInitData(str_MediaID,strBase64Random,strAdminKey,strAdminAlgId)
            else: 
                textInitData.send_keys(str_initData)
                
            textAreaResultSecInitCard = self.browser.find_element_by_id("ResultCustInitCardSec")
            textAreaResultSecInitCard.clear()
            btnSecInitCard = self.browser.find_element_by_id("CustInitCardSec")
            btnSecInitCard.click()
            time.sleep(1)
            
            if 2 <= GL.TestingRange and GL.TestingRange <= 3:
                WebDriverWait(self.browser, 5).until(lambda x: 0 < len(x.find_element_by_id("ResultCustInitCardSec").get_attribute('value')))
                return textAreaResultSecInitCard.get_attribute('value')
            
            else:   
                while self.find_subWindow(str_tipTitle):
                    logger.warning('等待U盾按键操作...')
                    time.sleep(1)

            WebDriverWait(self.browser, 5).until(lambda x: 0 <= len(x.find_element_by_id("ResultCustInitCardSec").get_attribute('value')))
            #textAreaResultSecInitCard = self.browser.find_element_by_id("ResultCustInitCardSec")
            return textAreaResultSecInitCard.get_attribute('value')                             
        except Exception as e:
            logger.error("Exception- %s ",str(e))
            return
    
    def verifySignAfter(self,p7SignedData=None,p7SignedFile=None):
        '''
                   管理员控件事后延签
        '''
        '''
                    参数说明：p7SignedData：P7签名数据包
                p7SignedFile：P7签名文件
        '''
        try:
            #定位鼠标位置，确保鼠标焦点定位在对话框上
            self.mouseFocus_locate()
         
            #初始化变量
            textResultSignVerify = self.browser.find_element_by_id("ResultSignVerify")
            textResultSignVerify.clear()
            textp7SignedData = self.browser.find_element_by_id("SignedP7")
            textp7SignedData.clear()
            textp7SignedFile = self.browser.find_element_by_id("SignedP7File")
            textp7SignedFile.clear()                      
                          
            #测试开始    
            if None != p7SignedData and '' !=p7SignedData:
                textp7SignedData.click()
                content='document.getElementById("SignedP7").value = "%s"' % p7SignedData 
                self.browser.execute_script(content)
                time.sleep(0.01) 
            if None != p7SignedFile and '' !=p7SignedFile: 
                textp7SignedFile.click()
                content='document.getElementById("SignedP7File").value = "%s"' % p7SignedFile 
                self.browser.execute_script(content)
                
            btnSignVerData = self.browser.find_element_by_id("SignVerify")
            btnSignVerData.click() 
            
            WebDriverWait(self.browser, 5).until(lambda x: 0 < len(x.find_element_by_id("ResultSignVerify").get_attribute('value')))                         
            #SignedVerifyResult=textResultSignVerify.get_attribute('value')  
            return textResultSignVerify.get_attribute('value')                            
        except Exception as e:
            logger.error("Exception- %s ",str(e))
        return
    
    def get_XmlMsg(self):
        '''
                   管理员控件获取XML信息
        '''        
        try:
            #定位鼠标位置，确保鼠标焦点定位在对话框上
            self.mouseFocus_locate()
            #初始化
            textAreaResultGetXmlMsg = self.browser.find_element_by_id("ResultGetXmlMsg")
            textAreaResultGetXmlMsg.clear()

            #测试开始
            btnGetXmlMsg = self.browser.find_element_by_id("GetXmlMsg")
            btnGetXmlMsg.click()
            
            WebDriverWait(self.browser, 5).until(lambda x: 0 <= len(x.find_element_by_id("ResultGetUsbkeyRom").get_attribute('value')))              
            return textAreaResultGetXmlMsg.get_attribute('value')
        except Exception as e:
            logger.error("Exception- %s ",str(e))
            pass
        return 
          
    def get_KeyDispMsg(self):
        '''
                   管理员控件获取屏显信息
        '''        
        try:
            #定位鼠标位置，确保鼠标焦点定位在对话框上
            self.mouseFocus_locate()
            #初始化
            textAreaResultGetKeyMsg  = self.browser.find_element_by_id("ResultGetKeyMsg")
            textAreaResultGetKeyMsg.clear()

            #测试开始
            btnGetKeyMsg = self.browser.find_element_by_id("GetKeyMsg")
            btnGetKeyMsg.click()
            
            WebDriverWait(self.browser, 5).until(lambda x: 0 <= len(x.find_element_by_id("ResultGetUsbkeyRom").get_attribute('value')))              
            return textAreaResultGetKeyMsg.get_attribute('value')
        except Exception as e:
            logger.error("Exception- %s ",str(e))
            pass
        return
       
    def get_Base64Decode(self,Base64Encode=None):
        '''
                   管理员控件Base64解密
        '''        
        try:
            #定位鼠标位置，确保鼠标焦点定位在对话框上
            self.mouseFocus_locate()
            #初始化
            textAreaBase64EncodeData=self.browser.find_element_by_id("Base64SerRand")
            textAreaResultBase64Decode  = self.browser.find_element_by_id("ResultBase64Decode")
            textAreaResultBase64Decode.clear()
            
            if None != Base64Encode and '' != Base64Encode:
                textAreaBase64EncodeData.click()
                content='document.getElementById("Base64SerRand").value = "%s"' % Base64Encode 
                self.browser.execute_script(content)
            else:
                textAreaBase64EncodeData.clear()
                

            #测试开始
            btnBase64Decode = self.browser.find_element_by_id("Base64Decode")
            btnBase64Decode.click()
            
            WebDriverWait(self.browser, 5).until(lambda x: 0 <= len(x.find_element_by_id("ResultBase64Decode").get_attribute('value')))              
            return textAreaResultBase64Decode.get_attribute('value')
        except Exception as e:
            logger.error("Exception- %s ",str(e))
            pass
        return
    
    def initCardDefaultPin(self,str_tipTitle=str_verifyTitle):
        '''
                   管理员控件初始化为默认PIN码
        '''        
        try:
            #定位鼠标位置，确保鼠标焦点定位在对话框上
            self.mouseFocus_locate()
            #初始化
            textAreaResultCustInitCard = self.browser.find_element_by_id("ResultCustInitCard")
            textAreaResultCustInitCard.clear()
                        
            btnCustInitCard = self.browser.find_element_by_id("CustInitCard")
            btnCustInitCard.click() 
            time.sleep(1)
            
            if 2 <= GL.TestingRange and GL.TestingRange <= 3:
                WebDriverWait(self.browser, 5).until(lambda x: 0 < len(x.find_element_by_id("ResultCustInitCard").get_attribute('value')))
                return textAreaResultCustInitCard.get_attribute('value')
            
            else:    
                while self.find_subWindow(str_tipTitle):
                    logger.warning('等待U盾按键操作...') 
                    time.sleep(1)
                 
            WebDriverWait(self.browser, 5).until(lambda x: 0 < len(x.find_element_by_id("ResultCustInitCard").get_attribute('value')))                         
            return textAreaResultCustInitCard.get_attribute('value')                             
        except Exception as e:
            logger.error("Exception- %s ",str(e))
        return       

    def printCodeEnvelope(self,str_tipTitle=str_verifyTitle):
        '''
                   管理员控件打印密码信封
        '''        
        try:
            #定位鼠标位置，确保鼠标焦点定位在对话框上
            self.mouseFocus_locate()
            #初始化
            textAreaResultPrtRandomPIN = self.browser.find_element_by_id("ResultPrtRandomPIN")
            textAreaResultPrtRandomPIN.clear()
                        
            btnCustInitCard = self.browser.find_element_by_id("PrtRandomPIN")
            btnCustInitCard.click() 
                           
            resp_title= ''
            while True == self.find_subWindow(str_tipTitle, resp_title):
                logger.warning('等待U盾按键操作...') 
                 
            WebDriverWait(self.browser, 5).until(lambda x: 0 <= len(x.find_element_by_id("ResultPrtRandomPIN").get_attribute('value')))                         
            return textAreaResultPrtRandomPIN.get_attribute('value')                             
        except Exception as e:
            logger.error("Exception- %s ",str(e))
        return
              
    def get_ServerRandom(self):
        try:
            ToolHwnd=open_window(AuxTool)
            rect=RECT()
            ctypes.windll.user32.GetWindowRect(ToolHwnd, ctypes.byref(rect)) #获取对话框相对屏幕的坐标位置
            testView=ToolConvert(ToolHwnd, rect)
            testView.FuncGetBase64EncodeRandom()     #获取Base64随机数              
            #关闭p10转p7工具
            os.system('taskkill /F /IM IcbcOcxAuxTool_rls.exe')
            
            #获取IE页面返回码
            WebDriverWait(self.browser, 5).until(lambda x: 0 <= len(x.find_element_by_id("Base64SerRand").get_attribute('value')))
    
            textAreaResultBase64SerRand=self.browser.find_element_by_id("Base64SerRand")
            textAreaResultBase64SerRand.clear()
            textAreaResultBase64SerRand.click()
            textAreaResultBase64SerRand.send_keys(Keys.CONTROL,'v') #粘贴
            return textAreaResultBase64SerRand.get_attribute('value')
        except Exception as e:
            logger.error("get_ServerRandom Exception- %s ",str(e))
            return

        
    def get_UkeyType(self):
        '''
                    判断U盾类型：非国密盾False,国密盾True 并返回保护密钥算法ID和序号
        '''
        flag=False
        AdminAlgID=None
        AdminCount=None
        AdminKeyInfo=self.get_AdminKeyInfoC()
        if None !=AdminKeyInfo and '' !=AdminKeyInfo:
            AdminAlgID=AdminKeyInfo[2:4]
            AdminCount=AdminKeyInfo[0:2]
            flag=True
        else:
            AdminAlgID='00'    #非国密盾保护密钥算法默认为3DES——方便兼容性处理
            AdminCount='00'
        return flag,AdminAlgID,AdminCount
    
    def PasswordRulesOfICBC(self,pwd):
        pwd_len=len(pwd)
        if (pwd_len >= 6 and pwd_len<=30): #密码长度满足6~30位
            if (pwd_len < 8): #密码长度在6~8位
                logger.warning("简单密码！当前密码长度不足8位:%d",pwd)
                return 0
            elif (pwd_len >=8 and pwd_len <=10):
                if True == len(re.findall(r'(?=567890|098765)', pwd)):
                    logger.warning("简单密码！存在超过6个的连续字符：%s",pwd)
                    return 0
                elif True == self.checkContinousSymbol(pwd,5):
                    logger.warning("简单密码！存在超过6个的连续字符：%s", pwd)
                    return 0
                else:
                    logger.warning('合法字符！%s',pwd) 
                    return 1 
            else :   
                logger.warning("强密码！当前密码长度超过10位：%d",pwd_len)
                return 1                
        elif(pwd_len < 6):
            logger.warning("密码长度不符！当前密码长度不足6位：%d",pwd_len)
            return 2
        else:
            subpwd=pwd[0:30]
            logger.warning("密码超长截断！当前密码长度位：%d,截取后密码长度:%d" %(pwd_len,len(subpwd)))  #多变量输出效果
            return 2

    def checkContinousSymbol(self,pwd,cLen): #连续字符判断
        AscList=self.char2ASC(pwd) #字符转换为ASCII码
        tmp=[]
        tmp.clear()
        for  i in range(0,len(pwd)-1):
            tmp.append(AscList[i+1]-AscList[i])
        strstr=''
        strstr=''.join(i.__str__() for i in tmp)  #数组转字符串
        same_continue_one=len(re.findall(r'(?=11111|00000|-1-1-1-1-1)', strstr)) #字符串中是否存在5个连续相同的1值

        if same_continue_one>=1:
            #连续字符超过6个  /递增字符超过6个  /递减字符超过6个
            return True
        else:
            return False

    def char2ASC(self,pwd): #字符转换为ASCII码
        tmp=[]
        tmp.clear()
        for i in range(0,len(pwd)):
            tmp.append(ord(pwd[i]))
        return tmp

    def close(self):
        if None != self.browser:
            self.browser.quit()
            
    def _load_ActiveX(self):
        if False == self.isActiveXLoaded :
            logger.warning('_load_ActiveX')
            title = '明华澳汉控件测试 '
            #ret = os.system("E:\work\宸ヨ\鎺т欢\Python\exe\ClickInstallActivx.exe %s" % (str(title)))
            ret = os.popen("E:\work\工行\控件\Python\exe\ClickInstallActivx.exe %s" % (str(title)))
            #print('ret=' + str(ret))
            time.sleep(5)
            if 0 == ret :
                self.isActiveXLoaded = True
    ''' 
    def _load_ActiveX_New(self, title, control):
        try:
            if False == self.isActiveXLoaded :
                window = autoit.win_get_process(title)
                autoit.win_activate(title)
                autoit.win_wait(title, 10)
                autoit.win_set_on_top(title)                
                time.sleep(1)            

                # 鍙兘瀛樺湪澶氫釜锛屽皾璇曢亶鍘�
                for index in range(0, 3) : 
                    autoit.control_focus('[CLASS:IEFrame]', control) 
                    time.sleep(1)  
                    autoit.control_send('[CLASS:IEFrame]', control, '!A')                
                time.sleep(3)                                           
        except Exception as e:
            logger.error("Exception:" + str(e))
       
    def _wait_for_native_exe_show(self, title, timeout = 10):
        try:
            #window = autoit.win_get_process(title)
            #print('win_get_process window=' + str(window))
            logger.warning('_wait_for_native_exe_show')
            
            ret = autoit.win_wait(title, timeout)
            logger.warning('win_wait ret=' + str(ret))
            
            logger.warning('win_get_state ret=' + str(autoit.win_get_state(title)))
            if 1 == ret:
                return True
        except Exception as e:
            logger.warning("_wait_for_native_exe_show Exception:" + str(e))
        return False
    
    def _is_native_exe_exist(self, title):
        try:
            ret = autoit.win_get_state(title)
            return 0 != (1 & ret)
        except Exception as e:
            logger.error("_is_native_exe_exist Exception:" + str(e))
        return False      
    '''
    def find_subWindow_old(self,str_title,resp_title,timeout=5):
        try:
            timesleep = 0
            while(False == operator.eq(str_title,resp_title) and (timesleep <= timeout)) :  #等待子窗口弹出，最长等待10s
                dlg_hWnd = win32gui.FindWindow(None,str_title)            
                resp_title = win32gui.GetWindowText(dlg_hWnd)
                time.sleep(1) 
                timesleep = timesleep + 1
            if True == operator.eq(str_title,resp_title): #找到窗口 
                return True
            else:
                return False
        except Exception as e:
            #logger.error('find_subWindow Exception:',+ str(e))
            return  
    
    def get_hwnds_for_Windows (self,titleName):
        def callback (h, hwnds):
            if win32gui.IsWindowVisible (h) and win32gui.IsWindowEnabled (h):
                if titleName == win32gui.GetWindowText(h):
                    hwnds.append (h)
                    return True
        hwnds = []
        win32gui.EnumWindows (callback, hwnds)
        return hwnds    
         
    def find_subWindow(self,titleName,timeout=5):        
        destHwnd=0
        hwnds=[]
        tCounts=0
        while [] == hwnds and tCounts < timeout:
            hwnds = self.get_hwnds_for_Windows(titleName)  
            if [] != hwnds:    
                for h in hwnds:
                    win32gui.SetForegroundWindow(h)
                    pag.click() #防止鼠标焦点乱跑，定位在当前对话框上                    
                    destHwnd=h
                    break
            else:
                time.sleep(0.5)
                hwnds=[]
            tCounts+=1         
        return destHwnd     
     
    def open_tabWindow(self,destUrl,destWinTitle):
        tempUrl="https://www.baidu.com"
        tempWinTitle="百度一下，你就知道"
        cur_title=''
        js='window.open("%s");'%tempUrl
        self.browser.execute_script(js)
        all_handles=self.browser.window_handles
        for handle in all_handles:
            cur_url=self.browser.current_url
            if -1 == cur_url.find(tempUrl):  #找到指定窗口Tab
                self.browser.switch_to_window(handle)   
            if -1 !=self.browser.current_url.find(tempUrl):
                self.browser.get(destUrl)
                cur_title=self.browser.title
                break
        if operator.eq(destWinTitle,cur_title):
            return True
        else:
            return False
                         
    def close_tabWindow(self,destUrl,destWinTitle,srcUrl):
        all_handles=self.browser.window_handles
        countHwnds=len(all_handles)
        if countHwnds>1:
            for handle in all_handles:
                if True==operator.eq(destWinTitle,self.browser.title):  #未找到指定窗口Tab
                    self.browser.close()
                    break
                else:
                    self.browser.switch_to_window(handle)
                
        if (countHwnds-1)==len(self.browser.window_handles):     
            return True
        else:
            return False
                
    def switch_tabWindow(self,destUrl,destWinTitle):
        cur_title=''
        all_handles=self.browser.window_handles
        for handle in all_handles:
            cur_url=self.browser.current_url
            if -1 == cur_url.find(destUrl):  #未找到指定窗口Tab
                self.browser.switch_to_window(handle)
            if True==operator.eq(destWinTitle,self.browser.title):
                cur_title=self.browser.title
                break
        if operator.eq(destWinTitle,cur_title):
            return True
        else:
            return False
              
    def mouseFocus_locate(self):
        try:
            #定位鼠标位置，确保鼠标焦点定位在对话框上
            screenX,screenY=pag.size() #获取屏幕分辨率
            MousePos_X=screenX/2
            MousePos_Y=screenY/3 
            pag.moveTo(MousePos_X, MousePos_Y)
        except Exception as e:
            logger.error('mouseFocus_locate Exception:',+ str(e))
        return 
       
    def DlgBtnClick(self,hWnd,btn_type=0):
        if btn_type <0 and btn_type >2:
            pag.alert("parameter error:",btn_type)
            return False
        if 0 == btn_type:
            pag.typewrite(['enter'])
            #pag.press('enter')
            return True
        elif 1 == btn_type: 
            pag.typewrite(['esc'])            
            #pag.press('esc')
            return False 
        elif 2 == btn_type:
            win32gui.PostMessage(hWnd, win32con.WM_CLOSE, 0, 0)
            return False
        
    def inputPinFunc(self,input_Count=3,str_pin_1='',str_pin_2='',str_pin_3=''):
        '''
        input_Count:需要输入的密码次数，如修改密码需要输入3次密码，初始化需要输入2次密码，校验密码需要输入1次密码
                   =3  ——修改密码流程 
                   =2  ——初始化流程
                   =1  ——校验密码流程
                   =其他 ——参数错误
        str_pin_1:原密码
        str_pin_2:新密码/空
        str_pin_3:校验密码/空
        '''
        try:
            if  3 == input_Count:
                #原密码
                curX, curY=pag.position()            
                pag.click(curX+1, curY)
                pag.typewrite(str_pin_1)           
                #切换光标
                pag.typewrite(['tab'])
                #pag.press('tab')
                #time.sleep(0.1)
                #新密码
                curX, curY=pag.position()  #获取当前光标所在位置               
                pag.click(curX, curY)
                pag.typewrite(str_pin_2) 
                
                #切换光标
                pag.typewrite(['tab'])
                #pag.press('tab')
                #time.sleep(0.1)
                #确认密码
                curX, curY=pag.position()  #获取当前光标所在位置               
                pag.click(curX, curY) 
                pag.typewrite(str_pin_3)
                
            elif 2 == input_Count:
                #新密码
                curX, curY=pag.position()  #获取当前光标所在位置               
                pag.click(curX, curY)
                print("Test")
                print(curX, curY) 
                print("Test")
                pag.typewrite(str_pin_1)
                #切换光标
                pag.typewrite(['tab'])
                #pag.press('tab')
                #time.sleep(0.1)
                #确认密码
                curX, curY=pag.position()  #获取当前光标所在位置               
                pag.click(curX, curY) 
                pag.typewrite(str_pin_2)
            elif 1 == input_Count:
                #确认密码
                curX, curY=pag.position()  #获取当前光标所在位置               
                pag.click(curX, curY) 
                pag.typewrite(str_pin_1)
            else:
                logger.error('parameter error:')
                return 
        except Exception as e:
            logger.error('inputPinFunc Exception:',+ str(e))
        return    
    
    def diable_mouse(self):
        try:
            user32 = windll.LoadLibrary('user32.dll')
            user32.BlockInput(True)  
            return True                            
        except Exception as e:
            logger.error('diable_mouse Exception:',+ str(e))
        return False
        
    def enable_mouse(self):
        try:
            if True ==self.diable_mouse(self):
                user32 = windll.LoadLibrary('user32.dll')
                user32.BlockInput(False)  
                return True                            
        except Exception as e:
            logger.error('enable_mouse Exception:',+ str(e))
        return False        

'''''
 start run
'''''
 
if __name__ == '__main__':   
    #==============开始测试===================# 
    driver = TestIcbcGmUser('file:///'+testUrl_GM_User)
    driver.open()
    # result = driver.get_InitCard("输入密码","12345678","12345678")
    # result = driver.get_MediaId()
    DN = driver.get_GMCertDN()
    # result = driver.get_PubKey()
    # result = driver.get_PubKeyC()
    SerRand = 'txCtsLn0DQ1lmOssE4du'
    result = driver.get_GMPubKeyC('02', DN, SerRand)
    time.sleep(5)
    driver.close()
    #result=driver.get_ChangePin('修改U盾密码', str_srcPin, '12345678', '12345678')
    # result=driver.P102P7()
    #result=driver.get_InitCard(str_title, str_srcPin, str_srcPin)
    #print(result)   
    #result=driver.get_InitCard(str_title, str_srcPin, str_srcPin)
    #result=driver.get_ChangePin(str_changeTitle, str_srcPin, '12345678', '12345678')
    '''
    driver = TestIcbcGmUser(testUrl_GM_Manage)
    driver.open()   
    result=driver.get_SecInitCard(None, True)
    print(result)
    result=driver.get_Base64Random()
    print(result)    
    '''
    '''
    curUrl=testUrl_GM_User
    curWinTitle="明华澳汉控件测试"
    destUrl=testUrl_GM_Manage
    destUrlTitle="明华澳汉管理员控件测试"
    
    driver = TestIcbcGmUser(curUrl)
    driver.open() 
       
    tempUrl="https://www.baidu.com"
    tempWinTitle="百度一下，你就知道"
    cur_title=''
    js='window.open("%s");'%tempUrl
    driver.browser.execute_script(js)
    all_handles=driver.browser.window_handles
    for handle in all_handles:
        cur_url=driver.browser.current_url
        if -1 == cur_url.find(tempUrl):  #找到指定窗口Tab
            driver.browser.switch_to_window(handle)   
        if -1 !=driver.browser.current_url.find(tempUrl):
            driver.browser.get(destUrl)
            result=driver.get_Base64Random()
            cur_title=driver.browser.title
            driver.browser.close()
            driver.browser.switch_to_window(all_handles[0])
            break
    all_handles=driver.browser.window_handles
    result=driver.get_MediaId()
    #test.browser.get('https://www.baidu.com') # 在当前浏览器中访问百度      
    #test = TestIcbcGmUser(testUrl_GM_User)
    #test.open()
    #print(testUrl_GM_Manage)
    #str_xmlData=re.sub(re.compile('\\\\+'),'//',testUrl_GM_Manage)
    #print(str_xmlData)
    #js1='window.open("%s");'%str_xmlData
    #js='window.open("F://SVN//IcbcAutoTest//Import//IE//Test_GM_Icbc_Manage_64.htm");'
    #print(js)    
    #print(js1)
    #test1.browser.execute_script(js)
    #test = TestIcbcGmUser(testUrl_GM_Manage)
    #test.open()
    '''
    #接口测试
    '''
    result=test.get_InitCard(str_title, str_srcPin, str_srcPin)
    
    MediaId=test.get_MediaId()
    
    CertDN=test.get_GMCertDN()
    
    PubKey=test.get_PubKey()
    
    PubKey=test.get_PubKey(None)  
    PubKey=test.get_PubKey('')         
    PubKey=test.get_PubKey('AllPubKey')    
    PubKey=test.get_PubKey('CertPubKey')         
    PubKey=test.get_PubKey('NoCertPubKey') 
    
    PubKeyC=test.get_PubKeyC()
    
    GMPubKeyC = test.get_GMPubKeyC()
    GMPubKeyC = test.get_GMPubKeyC('','','')    
    GMPubKeyC = test.get_GMPubKeyC('02')
    GMPubKeyC = test.get_GMPubKeyC('01')    
    CertDnLen=random.randint(0,60)
    CertDnRandom=''.join(random.sample(string.ascii_letters + string.digits,CertDnLen)).replace(" ","")
    serverRandom=''.join(random.sample('abcdefg&#%^*f012*9',16)).replace(" ","")  
    GMPubKeyC = test.get_GMPubKeyC('02',CertDnRandom,serverRandom)
    PubId=random.randint(10,100)
    #CertDnRandom=''.join(random.sample(string.ascii_letters + string.digits,CertDnLen)).replace(" ","")
    serverRandom=''.join(random.sample('abcdefg&#%^*f012*9',16)).replace(" ","")  
    GMPubKeyC = test.get_GMPubKeyC('02',PubId,serverRandom)    
    Ver=test.get_Ver() 
    DriverVer=test.get_DriverVer() 
    test.get_GMDelTempKey()
          
    test.close()
    '''
