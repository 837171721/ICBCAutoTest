#coding=utf-8
'''
Created on 2018.04.01 @author: SYX
Created on 2018.07.20 @author: YS
Created on 2018.08.10 @author: syx
Created on 2018.08.18 @author: ys
'''
import re
import string
import random
import operator
import win32api,win32con
import GenCertGroup
from GlobalConfigure import levels,log_level,str_title,str_srcPin,CertListInfoMap

from logTest import SysClass, LoggerClass
conf  = LoggerClass(loglevel=levels.get(log_level), logger="TestCases_GMDelTempKey.py")
logger=conf.getlogger()
 
#错误信息列表
no_key_Err='''删除指定证书和临时密钥对失败:未知错误。返回码:-102 There is no key!'''
many_key_Err='''删除指定证书和临时密钥对失败:未知错误。返回码:-104 There is more than one key!'''
voidPara_Err='''删除指定证书和临时密钥对失败:未知错误。返回码:-304 Failed Param!'''
err_key_Err='''删除指定证书和临时密钥对失败:未知错误。返回码:-411 ukey version error!'''
correct_Info='''删除指定证书和临时密钥对成功！'''
cancel_Err='''删除指定证书和临时密钥对失败:未知错误。返回码:-100 User cancel!'''
overtime_Err='''删除指定证书和临时密钥对失败:未知错误。返回码:-105 Time out!'''
no_cert_Err='''删除指定证书和临时密钥对失败:未知错误。返回码:-405 no matching cert!'''
inpdoc_Err='''删除指定证书和临时密钥对失败:未知错误。返回码:-321 DN data error!'''

def test_GetDelTempKey(ctrlObj,TestingRange,AdminKeyInfo):
    #调用流程
    testCtrl=GMDelTempKeyCases(ctrlObj,AdminKeyInfo)  #建立类对象，打开控件测试页 
    testGMDelTempKeyGroup(testCtrl,TestingRange)   #测试用例集，根据测试范围定义测试强度

def testGMDelTempKeyGroup(ctrlElemObj,testRange):
    #测试用例集
    if 0 == testRange:  #详细测试
        testResult = ctrlElemObj.negativeCase_formatKey_voidParaChoice()
        
        testResult = ctrlElemObj.negativeCase_formatKey_randParaChoice()
        
        testResult = ctrlElemObj.negativeCase_formatKey_validParaChoice()
        
        #testResult = ctrlElemObj.negativeCase_oldAdminKey_validParaChoice()  #用例更改，支持非国密盾
        
        testResult = ctrlElemObj.positiveCase_oneCert_validParaChoice()
        
        testResult = ctrlElemObj.operationCase_pressC()
        
        testResult = ctrlElemObj.operationCase_timeout()
        
        testResult = ctrlElemObj.operationCase_outKey()
        
        testResult = ctrlElemObj.negativeCase_oneCert_errParaChoice()
        
        testResult = ctrlElemObj.positiveCase_onePubKey_validParaChoice()
        
        testResult = ctrlElemObj.positiveCase_manyCertAndmanyPubKey()

        # testResult = ctrlElemObj.negativeCase_noKey_voidParaChoice()

        # testResult = ctrlElemObj.negativeCase_noKey_randParaChoice()
        
        #testResult = ctrlElemObj.negativeCase_manyKey()   
        
        #testResult = ctrlElemObj.negativeCase_operation()       
         
    elif 1 == testRange: #验证测试
        testResult = ctrlElemObj.positiveCase()
                
    elif 2 == testRange: #无key测试
        testResult = ctrlElemObj.negativeCase_noKey_voidParaChoice()

        testResult = ctrlElemObj.negativeCase_noKey_randParaChoice()
        
    elif 3 == testRange: #多key测试
        testResult = ctrlElemObj.negativeCase_manyKey()   
 
    elif 4 == testRange: #多key测试
        testResult = ctrlElemObj.negativeCase_formatKey_validParaChoice()
        
        testResult = ctrlElemObj.positiveCase()
       
class GMDelTempKeyCases():
    def __init__(self,testCtrl,AdminKeyInfo):
        self.testCtrl=testCtrl   #控件测试页
        self.AdminKeyAlgId=AdminKeyInfo  #保护密钥信息
        self.CertRequest=GenCertGroup.GenCertClass(self.testCtrl,AdminKeyInfo)   #创建证书申请对象
 
    def positiveCase(self):
        #用例描述：插入1支有1张证书、1对临时密钥对的U盾；输入正确的参数，点击删除临时公私钥,返回“删除指定证书和临时密钥对成功！”提示
        caseTitle="用例——插入1支有1张证书、1对临时密钥对的U盾；输入正确的参数，点击删除临时公私钥,返回“删除指定证书和临时密钥对成功！”"
        caseResult = None
        e = None        
        certResult=self.CertRequest.genCert_with_RSA1024_Mix()
        keypairResult=self.CertRequest.genKeyPair(CertListInfoMap["RSA1024_Mixed"], certResult[2])            
        if certResult[1] and keypairResult[1]:
            delTempKeyResult=self.testCtrl.get_GMDelTempKey(certResult[0][0],keypairResult[0][0])
            delTempKeyResult=re.sub(re.compile('\s+'),' ',delTempKeyResult)
            if operator.eq(correct_Info, delTempKeyResult): 
                caseResult="pass"
            else:
                caseResult="fail"
                e = "实测返回：" + "“" +delTempKeyResult+ "”"
        else:
            caseResult="fail"
            e = "下证失败,结束用例执行" 
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult
       
    def negativeCase_noKey_voidParaChoice(self):
        #用例描述：未插入U盾，不输入证书DN与公钥ID参数，点击删除临时公私钥，返回“删除指定证书和临时密钥对失败:未知错误。返回码:-304 Failed Param!”错误提示信息
        caseTitle="用例——未插入U盾，不输入证书DN与公钥ID参数，点击删除临时公私钥，返回“删除指定证书和临时密钥对失败:未知错误。返回码:-304 Failed Param!”错误提示信息"
        caseResult = None
        e = None
        delCertDN=''
        delPubKeyID=''
        delTempKeyResult=self.testCtrl.get_GMDelTempKey(delCertDN,delPubKeyID)
        delTempKeyResult=re.sub(re.compile('\s+'),' ',delTempKeyResult)
        if operator.eq(voidPara_Err,delTempKeyResult):
            caseResult="pass"
        else:
            caseResult="fail"
            e = "实测返回：" + "“" + delTempKeyResult+ "”"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult

    def negativeCase_noKey_randParaChoice(self):
        #用例描述：未插入U盾，证书DN与公钥ID参数任意输入，点击删除临时公私钥，返回“删除指定证书和临时密钥对失败:未知错误。返回码:-102 There is no key!”错误提示信息
        caseTitle="用例——未插入U盾，证书DN与公钥ID参数任意输入，点击删除临时公私钥，返回“删除指定证书和临时密钥对失败:未知错误。返回码:-102 There is no key!”错误提示信息"
        caseResult = None
        e = None        
        certDnLen = random.randint(0,60)
        certDnRandom=''.join(random.sample(string.ascii_letters + string.digits,certDnLen)).replace(" ","")
        delPubKeyID=''.join(random.sample('0123456789',2)).replace(" ","")  
        delTempKeyResult=self.testCtrl.get_GMDelTempKey(certDnRandom,delPubKeyID)
        delTempKeyResult=re.sub(re.compile('\s+'),' ',delTempKeyResult)
        if operator.eq(no_key_Err,delTempKeyResult):
            caseResult="pass"
        else:
            caseResult="fail"
            e = "实测返回：" + "“" + delTempKeyResult+ "”" 
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult
    
    def negativeCase_formatKey_voidParaChoice(self):
        #用例描述：插入1支格式化的U盾，不输入证书DN与公钥ID参数，点击删除临时公私钥,返回删除指定证书和临时密钥对失败:未知错误。返回码:-304 Failed Param!
        caseTitle="用例——插入1支格式化的U盾，不输入/任意输入证书DN与公钥ID参数，点击删除临时公私钥,返回删除指定证书和临时密钥对失败:未知错误。返回码:-304 Failed Param!"
        caseResult=None
        e=None
        initResult=self.CertRequest.init_key(str_srcPin,str_srcPin)
        if initResult[0]: 
            delCertDN=''
            delPubKeyID='' 
            delTempKeyResult=self.testCtrl.get_GMDelTempKey(delCertDN,delPubKeyID)
            delTempKeyResult=re.sub(re.compile('\s+'),' ',delTempKeyResult)
            if operator.eq(voidPara_Err,delTempKeyResult):
                caseResult="pass"
            else:
                caseResult="fail"
                e = "实测返回：" + "“" + delTempKeyResult+ "”"  
        else:
            caseResult="fail"
            e = "初始化失败，结束用例执行"         
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult

    def negativeCase_formatKey_randParaChoice(self):
        #用例描述：插入1支格式化的U盾，任意输入证书DN与公钥ID参数，点击删除临时公私钥,返回删除指定证书和临时密钥对失败:未知错误。返回码:-304 Failed Param!
        caseTitle="用例——插入1支格式化的U盾，不输入/任意输入证书DN与公钥ID参数，点击删除临时公私钥,返回删除指定证书和临时密钥对失败:未知错误。返回码:-304 Failed Param!"
        caseResult=None
        e=None
        initResult=self.CertRequest.init_key(str_srcPin,str_srcPin)
        if initResult[0]: 
            certDnLen = random.randint(0,60)
            certDnRandom=''.join(random.sample(string.ascii_letters + string.digits,certDnLen)).replace(" ","")
            delPubKeyID=''.join(random.sample('0123456789',2)).replace(" ","")  
            delTempKeyResult=self.testCtrl.get_GMDelTempKey(certDnRandom,delPubKeyID)
            delTempKeyResult=re.sub(re.compile('\s+'),' ',delTempKeyResult)
            if operator.eq(inpdoc_Err,delTempKeyResult):
                caseResult="pass"
            else:
                caseResult="fail"
                e = "实测返回：" + "“" + delTempKeyResult+ "”"   
        else:
            caseResult="fail"
            e = "初始化失败，结束用例执行"              
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult

    def negativeCase_formatKey_validParaChoice(self):
        #用例描述：插入1支格式化的U盾，输入有效证书DN与公钥ID参数，点击删除临时公私钥,返回删除指定证书和临时密钥对失败:未知错误。返回码:-304 Failed Param!
        caseTitle="用例——插入1支格式化的U盾，输入有效证书DN与公钥ID参数，点击删除临时公私钥,返回删除指定证书和临时密钥对失败:未知错误。返回码:-405 no matching cert!"
        caseResult=None
        e=None
        initResult=self.CertRequest.init_key(str_srcPin,str_srcPin)
        if initResult[0]: 
            certDnRandom="CN="
            delPubKeyID=None 
            delTempKeyResult=self.testCtrl.get_GMDelTempKey(certDnRandom,delPubKeyID)
            delTempKeyResult=re.sub(re.compile('\s+'),' ',delTempKeyResult)
            if operator.eq(no_cert_Err,delTempKeyResult):
                caseResult="pass"
            else:
                caseResult="fail"
                e = "实测返回：" + "“" + delTempKeyResult+ "”"   
        else:
            caseResult="fail"
            e = "初始化失败，结束用例执行"              
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult

    def negativeCase_oldAdminKey_validParaChoice(self):
        #用例描述：插入工行旧盾，输入正确的证书DN/公钥ID参数，点击删除临时公私钥，返回删除指定证书和临时密钥对失败:未知错误。返回码:-411 ukey version error!
        caseTitle="用例——插入工行旧盾，输入正确的证书DN/公钥ID参数，点击删除临时公私钥，返回删除指定证书和临时密钥对失败:未知错误。返回码:-411 ukey version error!"
        caseResult=None
        e=None
        win32api.MessageBox(0, "请确认已插入一支测试非国密U盾！", "提示框",win32con.MB_OK)
        certResult=self.CertRequest.genCert_with_RSA1024_Mix()
        keypairResult=self.CertRequest.genKeyPair(CertListInfoMap["RSA1024_Mixed"], certResult[2])          
        if certResult[1] and keypairResult[1]:
            delTempKeyResult=self.testCtrl.get_GMDelTempKey(certResult[0][0],keypairResult[0][0])
            delTempKeyResult=re.sub(re.compile('\s+'),' ',delTempKeyResult)
            if operator.eq(err_key_Err, delTempKeyResult): 
                logger.info("响应信息为:%s",delTempKeyResult)
                caseResult="pass"
            else:
                caseResult="fail"
                e = "实测返回：" + "“" + delTempKeyResult+ "”"
        else:
            caseResult="fail"
            e = "下证失败，结束用例执行"        
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult
        
    def positiveCase_oneCert_validParaChoice(self):
        #用例描述：插入1支有1张证书U盾，点击删除临时公私钥，按下U盾OK键，删除成功IE返回“删除指定证书和临时密钥对成功！”提示
        caseTitle="用例——插入1支有1张证书U盾，点击删除临时公私钥，按下U盾OK键，删除成功IE返回“删除指定证书和临时密钥对成功！”提示"
        caseResult=None
        e=None
        certResult=self.CertRequest.genCert_with_RSA1024_Mix()
        if certResult[1]:            
            delTempKeyResult=self.testCtrl.get_GMDelTempKey(certResult[0][0])
            delTempKeyResult=re.sub(re.compile('\s+'),' ',delTempKeyResult)
            if operator.eq(correct_Info, delTempKeyResult): 
                caseResult="pass"
            else:
                caseResult="fail"
                e = "实测返回：" + "“" + delTempKeyResult+ "”"
        else:
            caseResult="fail"
            e = "下证失败，结束用例执行"   
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult

    def negativeCase_oneCert_errParaChoice(self):
        #用例描述：插入1支有1张证书的U盾，输入错误的证书DN或错误公钥ID，点击删除临时公私钥，返回“删除指定证书和临时密钥对失败:未知错误。返回码:-304 Failed Param!”错误提示信息
        caseTitle="用例——插入有1张证书的U盾，输入错误的证书DN或错误公钥ID，点击删除临时公私钥，返回“删除指定证书和临时密钥对失败:未知错误。返回码:-304 Failed Param!”错误提示信息"
        caseResult=None
        e=None
        certResult=self.CertRequest.genCert_with_RSA1024_Mix()
        keypairResult=self.CertRequest.genKeyPair(CertListInfoMap["RSA1024_Mixed"], certResult[2])          
        if certResult[1] and keypairResult[1]: 
            tempCertID=certResult[0][0].replace('Mi','iM')
            tempPubKeyID=int(keypairResult[0][0])+1         
            delTempKeyResult=self.testCtrl.get_GMDelTempKey(tempCertID,tempPubKeyID)
            delTempKeyResult=re.sub(re.compile('\s+'),' ',delTempKeyResult)
            if operator.eq(voidPara_Err, delTempKeyResult): 
                caseResult="pass"
            else:
                caseResult="fail"
                e = "实测返回：" + "“" + delTempKeyResult+ "”"
        else:
            caseResult="fail"
            e = "下证失败，结束用例执行" 
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)           
        return caseResult

    def positiveCase_onePubKey_validParaChoice(self):
        #用例描述：插入1支只有1对临时密钥对的U盾，输入此密钥对对应的公钥ID，点击删除临时公私钥，返回“删除指定证书和临时密钥对成功！”提示
        caseTitle="用例——插入只有1对临时密钥对的U盾，输入此密钥对对应的公钥ID，点击删除临时公私钥，返回“删除指定证书和临时密钥对成功！”提示"
        caseResult=None
        e=None
        keypairResult=self.CertRequest.genKeyPair(CertListInfoMap["RSA1024_Mixed"], str_srcPin,True)          
        if keypairResult[1]:  
            delTempKeyResult=self.testCtrl.get_GMDelTempKey('',keypairResult[0][0])
            delTempKeyResult=re.sub(re.compile('\s+'),' ',delTempKeyResult)
            if operator.eq(correct_Info, delTempKeyResult): 
                caseResult="pass"
            else:
                caseResult="fail"
                e = "实测返回：" + "“" + delTempKeyResult+ "”"
        else:
            caseResult="fail"
            e = "下证失败，结束用例执行" 
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)           
        return caseResult
        
    def operationCase_pressC(self):
        #用例描述：删除证书弹出按键提示框时，按下键盘Esc/空格/回车键，或U盾上下翻页键,应无反应，U盾保持等待按键状态！\
        #        按下U盾取消键，返回“删除指定证书和临时密钥对失败:未知错误。返回码:-100 User cancel!”错误提示
        caseTitle="用例——删除证书等待按键状态，按下键盘Esc/空格/回车键，或U盾上下翻页键,应无反应，U盾保持等待按键状态！按下U盾取消键，返回“删除指定证书和临时密钥对失败:未知错误。返回码:-100 User cancel!”错误提示"
        caseResult=None
        e=None
        win32api.MessageBox(0, "确认删除证书等待按键状态,按下键盘Esc/空格/回车键，或U盾上下翻页键,应无反应，U盾保持等待按键状态！按下U盾取消键，取消操作！", "提示框", win32con.MB_OK)

        certResult=self.CertRequest.genCert_with_RSA1024_Mix()
        if certResult[1]:
            delTempKeyResult=self.testCtrl.get_GMDelTempKey(certResult[0][0])
            delTempKeyResult=re.sub(re.compile('\s+'),' ',delTempKeyResult)
            if operator.eq(cancel_Err, delTempKeyResult): 
                caseResult="pass"
            else:
                caseResult="fail"
                e = "实测返回：" + "“" + delTempKeyResult+ "”"
        else:
            caseResult="fail"
            e = "下证失败，结束用例执行" 
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult                

    def operationCase_timeout(self):
        #用例描述：删除证书等待按键状态，不按键等待超时时间15Min，返回“删除指定证书和临时密钥对失败:未知错误。返回码:-105 Time out!”错误提示
        caseTitle="用例——删除证书等待按键状态，不操作等待15Min，返回“删除指定证书和临时密钥对失败:未知错误。返回码:-105 Time out!”错误提示"
        caseResult=None
        e=None
        win32api.MessageBox(0, "确认删除证书等待按键状态，请不要按键，等待15Min", "提示框", win32con.MB_OK)
        certResult=self.CertRequest.genCert_with_RSA1024_Mix()
        if certResult[1]:
            delTempKeyResult=self.testCtrl.get_GMDelTempKey(certResult[0][0])
            delTempKeyResult=re.sub(re.compile('\s+'),' ',delTempKeyResult)
            if operator.eq(overtime_Err, delTempKeyResult): 
                caseResult="pass"
            else:
                caseResult="fail"
                e = "实测返回：" + "“" + delTempKeyResult+ "”"
        else:
            caseResult="fail"
            e = "下证失败，结束用例执行" 
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult
    
    def operationCase_outKey(self):
        #用例描述：删除证书等待按键状态，直接拔出U盾，返回“删除指定证书和临时密钥对失败:未知错误。返回码:-100 User cancel!”错误提示
        caseTitle="用例——删除证书等待按键状态，直接拔出U盾，返回“删除指定证书和临时密钥对失败:未知错误。返回码:-100 User cancel!”错误提示"
        caseResult=None
        e=None
        win32api.MessageBox(0, "确认删除证书等待按键状态,直接拔出U盾", "提示框", win32con.MB_OK)
        certResult=self.CertRequest.genCert_with_RSA1024_Mix()     
        if certResult[1]: 
            delTempKeyResult=self.testCtrl.get_GMDelTempKey(certResult[0][0])
            delTempKeyResult=re.sub(re.compile('\s+'),' ',delTempKeyResult)            
            if operator.eq(cancel_Err, delTempKeyResult): 
                caseResult="pass"
            else:
                caseResult="fail"
                e = "实测返回：" + "“" + delTempKeyResult+ "”"
        else:
            caseResult="fail"
            e = "下证失败，结束用例执行" 
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)    
        return caseResult
    
    def positiveCase_manyCertAndmanyPubKey(self):        
        #用例描述：插入1支有多张证书（证书DN1、DN2）、多对临时密钥对（公钥ID1、ID2）的U盾；输入其中1张证书对应的证书DN1和1对临时密钥对对应的公钥ID1，点击删除临时公私钥,返回“删除指定证书和临时密钥对成功！”提示
        caseTitle="用例——插入1支有多张证书（证书DN1、DN2）、多对临时密钥对（公钥ID1、ID2）的U盾；输入其中1张证书对应的证书DN1和1对临时密钥对对应的公钥ID1，点击删除临时公私钥,返回“删除指定证书和临时密钥对成功！”提示"
        caseResult=None
        e=None
        certResult=self.CertRequest.genCert_with_rsa1024M_and_rsa2048M()
        keypairResult=self.CertRequest.genKeyPair(CertListInfoMap["RSA1024_M_and_RSA2048_M"], certResult[2])          
        if certResult[1] and keypairResult[1]:
            if certResult[0].count("||"): 
                certDnList=certResult[0]
                delTempKeyResult=self.testCtrl.get_GMDelTempKey(certDnList[0],keypairResult[0][0])
                delTempKeyResult=re.sub(re.compile('\s+'),' ',delTempKeyResult)
                if operator.eq(correct_Info, delTempKeyResult): 
                    caseResult="pass"
                else:
                    caseResult="fail"
                    e = "实测返回：" + "“" + delTempKeyResult+ "”"
        else:
            caseResult="fail"
            e = "下证失败，结束用例执行"         
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)           
        return caseResult

    def negativeCase_manyKey(self):
        #用例描述：插入多支同款U盾，输入合法的证书DN（或公钥ID），点击删除临时公私钥，返回删除指定证书和临时密钥对失败:未知错误。返回码:-104 There is more than one key!
        caseTitle="用例——插入多支同款U盾，输入合法的证书DN（或公钥ID），点击删除临时公私钥，返回删除指定证书和临时密钥对失败:未知错误。返回码:-104 There is more than one key!"
        caseResult=None
        e=None 
        certDnLen = random.randint(0,60)
        certDnRandom=''.join(random.sample(string.ascii_letters + string.digits,certDnLen)).replace(" ","")
        delPubKeyID=''.join(random.sample('0123456789',2)).replace(" ","")

        delTempKeyResult=self.testCtrl.get_GMDelTempKey(certDnRandom,delPubKeyID)
        delTempKeyResult=re.sub(re.compile('\s+'),' ',delTempKeyResult)
        if operator.eq(many_key_Err, delTempKeyResult):        
            caseResult="pass"
        else:
            caseResult="fail"
            e = "实测返回：" + "“" + delTempKeyResult+ "”"               
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)           
        return caseResult
    
    def negativeCase_operation(self):
        #用例描述：插入多支同款U盾，拔出多余U盾，只是1支在位，输入合法的证书DN（或公钥ID），点击删除临时公私钥，返回删除指定证书和临时公私钥对成功
        caseTitle="用例——插入多支同款U盾，拔出多余U盾，只是1支在位，输入合法的证书DN（或公钥ID），点击删除临时公私钥，返回删除指定证书和临时公私钥对成功"
        caseResult=None
        e=None
        #if 0 == TestingType:
            #win32api.MessageBox(0, "插入多支同款U盾，拔出多余U盾，只留1支在位！", "提示框",win32con.MB_OK)  
        certResult=self.CertRequest.genCert_with_RSA1024_Mix()
        keypairResult=self.CertRequest.genKeyPair(CertListInfoMap["RSA1024_Mixed"], str_srcPin)               
        if certResult[1] and keypairResult[1]:  
            delTempKeyResult=self.testCtrl.get_GMDelTempKey(certResult[0][0],keypairResult[0][0])
            delTempKeyResult=re.sub(re.compile('\s+'),' ',delTempKeyResult)
            if operator.eq(correct_Info, delTempKeyResult): 
                caseResult="pass"
            else:
                caseResult="fail"
                e = "实测返回：" + "“" + delTempKeyResult+ "”"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult
      
#########################
#开始测试
#########################
