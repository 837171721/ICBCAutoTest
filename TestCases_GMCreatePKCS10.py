#coding=utf-8
'''
Created on 2018.03.27 @author: lzy
Created on 2018.08.09 @author: syx
Created on 2018.08.18 @author: ys
'''
import re
import operator
import win32api,win32con
import GenCertGroup
from GlobalConfigure import levels,log_level,str_title,str_srcPin,CertListInfoMap,commCertDict,dispCertDict,mixCertDict
from logTest import LoggerClass
conf  = LoggerClass(loglevel=levels.get(log_level), logger="TestCases_GMCreatePKCS10.py")
logger=conf.getlogger()

init_str='初始化成功'
para_Err = '生成P10包失败:未知错误。返回码:-304 Failed Param!'
no_key_Err = '生成P10包失败:未知错误。返回码:-102 There is no key!'
pin_Err = '生成P10包失败:未知错误。返回码:-200 PIN Error!'
cancel_Err='''生成P10包失败:未知错误。返回码:-100 User cancel!'''
lock_Err = '生成P10包失败:未知错误。返回码:-221 Pin Locked!'
many_key_Err = '生成P10包失败:未知错误。返回码:-104 There is more than one key!'

def test_GetGMCreatePKCS10(ctrlObj,TestingRange,AdminKeyInfo):
    testCtrl=GetGMCreatePKCS10Cases(ctrlObj,AdminKeyInfo)  #建立类对象，打开控件测试页 
    testGMCreatePKCS10Group(testCtrl,TestingRange)   #测试用例集，根据测试范围定义测试强度

def testGMCreatePKCS10Group(ctrlElemObj,testRange):
    #测试用例集
    if 0 == testRange:  #详细测试
        testResult = ctrlElemObj.positiveCase()

        testResult = ctrlElemObj.negativeCase_errPin()

        testResult = ctrlElemObj.negativeCase_pinLock()

        testResult = ctrlElemObj.operationCase_PinUI_PressC()

        testResult = ctrlElemObj.operationCase_PinUI_Close()

        #testResult = ctrlElemObj.positiveCase_supportedMixPairKeyTest()

        #testResult = ctrlElemObj.positiveCase_supportedCommPairKeyTest()

        #testResult = ctrlElemObj.positiveCase_supportedDispPairKeyTest()
        
    elif 1 == testRange: #验证测试
        testResult = ctrlElemObj.positiveCase()
                
    elif 2 == testRange: #无key测试
        testResult = ctrlElemObj.negativeCase_nokey_voidParaChoice()

        testResult = ctrlElemObj.negativeCase_noKey_validParaChoice()

        testResult = ctrlElemObj.negativeCase_noKey_errParaChoice()
        
    elif 3 == testRange: #多key测试
        testResult = ctrlElemObj.negativeCase_manyKey()

    elif 4 == testRange: #多key测试
        testResult = ctrlElemObj.positiveCase()
       
class GetGMCreatePKCS10Cases():
    def __init__(self,testCtrl,AdminKeyInfo):
        self.testCtrl=testCtrl   #控件测试页
        self.AdminKeyAlgId=AdminKeyInfo  #保护密钥信息
        self.CertRequest=GenCertGroup.GenCertClass(self.testCtrl,AdminKeyInfo)   #创建证书申请对象
             
    def positiveCase(self):
        #插入1支U盾，输入请求信息：（申请RSA1024-专用）
        caseTitle =  "用例——插入1支U盾，申请RSA1024—sha1-专用证书，期望成功！"
        caseResult = None
        e = None
        P10Result = self.CertRequest.genKeyPair(CertListInfoMap["RSA1024_Sig2_p"],str_srcPin,True)
        if P10Result[1]:
            caseResult =  "pass"
        else:
            caseResult =  "fail"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult    

    def negativeCase_nokey_voidParaChoice(self):
        caseTitle = "用例——未插入U盾,不输入请求信息,点击生成P10包,期望返回“生成P10包失败:未知错误。返回码:-304 Failed Param”"
        e = None
        caseResult = None

        P10Result=self.testCtrl.GMCreatePKCS10('', str_title, str_srcPin)
        if P10Result[1]:
            caseResult = "pass"
        else:
            caseResult = "fail"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult

    def negativeCase_noKey_validParaChoice(self):
        caseTitle = "用例——未插入U盾，输入符合格式的请求信息，点击生成P10包; 期望返回：“生成P10包失败:未知错误。返回码:-102 There is no key!"
        e = None
        caseResult = None

        testResult = self.testCtrl.GMCreatePKCS10(CertListInfoMap["RSA1024_Sig2_p"], str_title, str_srcPin)
        testResult=re.sub(re.compile('\s+'),' ',testResult)
        if operator.eq(no_key_Err, testResult):
            caseResult = "pass"
        else:
            caseResult = "fail" 
            e =" 实测返回："+"“"+testResult+"”" 
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult
    
    def negativeCase_noKey_errParaChoice(self):
        #用例描述：未插入U盾，输入不符合格式的请求信息，点击生成P10包; 期望返回：“生成P10包失败:未知错误。返回码:-102 There is no key!”错误提示；"
        caseTitle = "用例——未插入U盾，输入不符合格式的请求信息，点击生成P10包; 期望返回：“生成P10包失败:未知错误。返回码:-102 There is no key!"
        caseResult = None
        e = None

        Dn_info = '1)KEYTYPE(RSA2048)CERTTYPE(02)'
        testResult = self.testCtrl.GMCreatePKCS10(Dn_info, str_title, str_srcPin)
        testResult=re.sub(re.compile('\s+'),' ',testResult)
        if operator.eq(no_key_Err, testResult):
            caseResult = "pass"
        else:
            caseResult = "fail" 
            e =" 实测返回："+"“"+testResult+"”" 
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult

    def negativeCase_errPin(self):
        #用例描述：生成P10包弹出认证密码框时，输入错误U盾密码  期望返回：生成P10包失败:未知错误。返回码:-205 PIN Error!
        caseTitle = "用例——生成P10包弹出认证密码框时，输入错误密码,请确认弹出错误密码提示框，选择是，返回密码输入界面等待重新输入，为方便测试关闭UI框结束本次操作"
        caseResult = None
        e = None

        initResult=self.CertRequest.init_key(str_srcPin,str_srcPin)
        if initResult[0]:
            err_pin = initResult[1]+"1"
            #testResult = self.CertRequest.genKeyPair(CertListInfoMap["RSA1024_Sig2_p"], err_pin, True)
            testResult=self.testCtrl.GMCreatePKCS10(CertListInfoMap["RSA1024_Sig2_p"],str_title,err_pin)
            testResult = re.sub(re.compile('\s+'),' ',testResult)
            if operator.eq(cancel_Err, testResult):
                caseResult = "pass"
            else:
                caseResult = "fail" 
                e =" 实测返回："+"“"+testResult+"”" 
        else:
            caseResult = "fail"
            e ="初始化失败,结束用例执行"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult      
    
    def negativeCase_pinLock(self):
        #用例描述：生成P10包弹出认证密码框时，输入错误U盾密码，直至U盾被锁死
        caseTitle = "用例——生成P10包弹出认证密码框时，输入错误U盾密码，直至U盾被锁死   期望返回：生成P10包失败:未知错误。返回码:-221 Pin Locked!"
        caseResult = None
        e = None
        win32api.MessageBox(0, "等待按键状态,请按U盾确认键", "提示框",win32con.MB_OK)

        initResult=self.CertRequest.init_key(str_srcPin,str_srcPin)
        if initResult[0]:
            err_pin = initResult[1]+"1"
            for i in range(7):
                testResult=self.testCtrl.GMCreatePKCS10(CertListInfoMap["RSA1024_Sig2_p"],str_title,err_pin)
                testResult = re.sub(re.compile('\s+'),' ',testResult) 
            if operator.eq(lock_Err, testResult):
                caseResult =  "pass"
            else:
                caseResult =  "fail"
                e =" 实测返回："+"“"+testResult+"”"
        else:
            caseResult = "fail"
            e ="初始化失败,结束用例执行"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult      
  
    def operationCase_PinUI_PressC(self):
        #用例描述：生成P10包弹出认证密码框时，点击取消  期望返回：生成P10包失败:未知错误。返回码:-100 User cancel!
        caseTitle = "用例——生成P10包弹出认证密码框时，点击UI框上取消键,期望返回：生成P10包失败:未知错误。返回码:-100 User cancel!"
        caseResult = None
        e = None

        initResult=self.CertRequest.init_key(str_srcPin,str_srcPin)
        if initResult[0]:
            testResult=self.testCtrl.GMCreatePKCS10(CertListInfoMap["RSA1024_Sig2_p"],str_title,initResult[1],1)
            testResult = re.sub(re.compile('\s+'),' ',testResult) 
            if operator.eq(cancel_Err, testResult):
                caseResult = "pass"
            else:
                caseResult = "fail" 
                e =" 实测返回："+"“"+testResult+"”" 
        else:
            caseResult = "fail"
            e ="初始化失败,结束用例执行"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult         
    
    def operationCase_PinUI_Close(self):
        #用例描述：生成P10包弹出认证密码框时，点击叉号  期望返回：生成P10包失败:未知错误。返回码:-100 User cancel!
        caseTitle = "用例——生成P10包弹出认证密码框时，点击叉号  期望返回：生成P10包失败:未知错误。返回码:-100 User cancel!"
        caseResult = None
        e = None

        initResult=self.CertRequest.init_key(str_srcPin,str_srcPin)
        if initResult[0]:
            testResult=self.testCtrl.GMCreatePKCS10(CertListInfoMap["RSA1024_Sig2_p"],str_title,initResult[1],2,0)
            testResult = re.sub(re.compile('\s+'),' ',testResult) 
            if operator.eq(cancel_Err, testResult):
                caseResult = "pass"
            else:
                caseResult = "fail" 
                e =" 实测返回："+"“"+testResult+"”" 
        else:
            caseResult = "fail"
            e = "初始化失败，结束用例执行"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult      
           
    def negativeCase_manyKey(self):    
        #用例描述：插入多支同款U盾，输入合法请求信息，生成P10包   期望返回：生成P10包失败:未知错误。返回码:-104 There is more than one key!
        caseTitle = "用例——插入多个同款U盾，输入合法请求信息，生成P10包   期望返回：生成P10包失败:未知错误。返回码:-104 There is more than one key!"
        caseResult = None
        e = None
        testResult=self.testCtrl.GMCreatePKCS10(CertListInfoMap["RSA1024_Sig2_p"],str_title,str_srcPin)
        testResult = re.sub(re.compile('\s+'),' ',testResult)
        if operator.eq(many_key_Err, testResult):
            caseResult =  "pass"
        else:
            caseResult =  "fail"
            e =" 实测返回："+"“"+testResult+"”"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult               

    def positiveCase_supportedMixPairKeyTest(self):
        # 用例描述：进行初始化-下证-二代签名，覆盖支持的所有证书
        caseTitle = "用例——进行初始化-下证-二代签名，覆盖所有混用证书及其哈希方式，二代签名返回成功"
        caseResult = None
        e = None

        '''        
        mixCertDict={
            CertListInfoMap["RSA1024_Mixed_sha1"],
            #CertListInfoMap["RSA1024_Mixed_sha256"], 
            }
        signHash=['SHA384']
        '''

        logger.critical("beginning... || %s ", caseTitle)
        for mix_cert in mixCertDict:
            P10Result = self.CertRequest.genKeyPair(mix_cert,str_srcPin,True)
            if P10Result[1]:
                caseResult = "pass"
                logger.critical("%s || %s ", caseResult, mix_cert)
            else:
                caseResult = "fail"
                logger.critical("%s || %s ", caseResult, mix_cert)
        logger.critical("end. || %s ", caseTitle)
        return caseResult

    def positiveCase_supportedCommPairKeyTest(self):
        # 用例描述：进行初始化-下证-二代签名，覆盖支持的所有证书
        caseTitle = "用例——进行初始化-下证-二代签名，覆盖所有混用证书及其哈希方式，二代签名返回成功"
        caseResult = None
        e = None

        '''
        commCertDict={
            CertListInfoMap["RSA1024_Comm_p_sha1"],
            #CertListInfoMap["RSA1024_Comm_p_sha256"], 
            }
        signHash=['SHA384']
        '''

        logger.critical("beginning... || %s ", caseTitle)
        for comm_cert in commCertDict:
            P10Result = self.CertRequest.genKeyPair(comm_cert,str_srcPin,True)
            if P10Result[1]:
                caseResult = "pass"
                logger.critical("%s || %s ", caseResult, comm_cert)
            else:
                caseResult = "fail"
                logger.critical("%s || %s ", caseResult, comm_cert)
        logger.critical("end. || %s ", caseTitle)
        return caseResult

    def positiveCase_supportedDispPairKeyTest(self):
        # 用例描述：进行初始化-下证-二代签名，覆盖支持的所有证书
        caseTitle = "用例——进行初始化-下证-二代签名，覆盖所有混用证书及其哈希方式，二代签名返回成功"
        caseResult = None
        e = None

        '''
        dispCertDict={
            CertListInfoMap["RSA1024_Sig2_p_sha1"],
            #CertListInfoMap["RSA1024_Mixed_sha256"], 
            }
        signHash=['SHA384']
        '''

        logger.critical("beginning... || %s ", caseTitle)
        for disp_cert in dispCertDict:
            P10Result = self.CertRequest.genKeyPair(disp_cert,str_srcPin,True)
            if P10Result[1]:
                caseResult = "pass"
                logger.critical("%s || %s ", caseResult, disp_cert)
            else:
                caseResult = "fail"
                logger.critical("%s || %s ", caseResult, disp_cert)
        logger.critical("end. || %s ", caseTitle)
        return caseResult

    def negativeCase_operation(self):
        # 用例描述：插入多支同款U盾，插入多个同款U盾，拔出多余U盾，只留1支在位，生成P10包   期望返回：生成P10包成功；
        caseTitle =  "用例——插入多支同款U盾，插入多个同款U盾，拔出多余U盾，只留1支在位，生成P10包   期望返回：生成P10包成功；"
        caseResult = None
        e = None
        result = self.testCtrl.get_InitCard(str_title,str_srcPin,str_srcPin)
        if  None != result and "" != result and result == init_str:
            testResult=self.testCtrl.GMCreatePKCS10(CertListInfoMap["RSA1024_Sig2_p"],'输入密码',str_srcPin)
            if "" != testResult and None != testResult:
                caseResult =  "pass"
            else:
                caseResult =  "fail"
                e =" 实测返回："+"“"+testResult+"”"
        else:
            caseResult = "fail"
            e =" 实测返回："+"“"+result+"”"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult      
        
#########################
#开始测试
#########################
    