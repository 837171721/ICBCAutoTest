#coding=utf-8
'''
Created on 2018.08.18 @author: ys
'''
import re
import sys
import operator
import GenCertGroup
import win32api,win32con
from GlobalConfigure import levels, log_level,str_srcPin,str_verifyPin,hashId,xmlInfo,dispInfo
from GlobalConfigure import CertListInfoMap,mixCertDict,commCertDict,dispCertDict,batFilePath,p7FilePath

from logTest import SysClass, LoggerClass
conf  = LoggerClass(loglevel=levels.get(log_level), logger="TestCases_DispSign.py")
logger=conf.getlogger()

#错误信息列表
no_key_Err= '''签名失败:未知错误。返回码:-102 There is no key!'''
many_key_Err='''签名失败:未知错误。返回码:-104 There is more than one key!'''
cancel_Err='''签名失败:未知错误。返回码:-100 User cancel!'''
para_Err='''签名失败:未知错误。返回码:-304 Failed Param!'''
pin_Err='''签名失败:未知错误。返回码:-205 PIN Error!'''
pin_Lock_Err='''签名失败:未知错误。返回码:-221 Pin Locked!'''
time_out_Err='''签名失败:未知错误。返回码:-105 Time out!'''
unsupported_cert_Err='''签名失败:未知错误。返回码:-405 no matching cert!'''
unmatched_hash_Err='''签名失败:未知错误。返回码:-409 Sign failed!'''
ver_Err='''签名失败:未知错误。返回码:-411 ukey version error!'''

file_sign_info = '''签名成功'''
right_Info="MII"
str_errPin='12121212'

def test_GetDispSign(ctrlObj,TestingRange,AdminKeyInfo):
    testCtrl=DispSignCases(ctrlObj,AdminKeyInfo)  #建立类对象，打开控件测试页     
    testDispSignGroup(testCtrl,TestingRange)   #测试用例集，根据测试范围定义测试强度

def testDispSignGroup(ctrlObj,testRange):
    #测试用例集
    if 0 == testRange:  #详细测试      
        testResult= ctrlObj.negativeCase_formatKey_voidParaChoice()
 
        testResult= ctrlObj.negativeCase_oneCert_voidParaChoice()
         
        testResult= ctrlObj.operationCase_PinUI_pressC()
         
        testResult= ctrlObj.operationCase_PinUI_pinErr()
# 
        testResult= ctrlObj.operationCase_PinUI_pinLock()
 
        testResult= ctrlObj.operationCase_pressC()
  
        testResult= ctrlObj.operationCase_timeout()
#  
        testResult= ctrlObj.operationCase_outKey()
         
        testResult= ctrlObj.negativeCase_rsaCert_errHashChoice()
         
        testResult= ctrlObj.negativeCase_sm2Cert_errHashChoice()
         
        testResult= ctrlObj.positiveCase_supportedDispCertTest()
                  
        testResult= ctrlObj.positiveCase_supportedMixCertTest()
          
        testResult= ctrlObj.negativeCase_supportedCommCertTest()
           
    elif 1 == testRange: #验证测试
        testResult= ctrlObj.positiveCase()
 
    elif 2 == testRange: #无key测试
        testResult= ctrlObj.negativeCase_noKey_voidParaChoice()
        
        testResult= ctrlObj.negativeCase_noKey_validParaChoice()
        
    elif 3 == testRange: #多key测试
        testResult= ctrlObj.nagativeCase_manyKey_validParaChoice()
        
    elif 4 == testRange: #多key测试
        testResult= ctrlObj.positiveCase()
       
class DispSignCases():
    def __init__(self,testCtrl,AdminKeyInfo):
        self.testCtrl=testCtrl   #控件测试页
        self.AdminKeyAlgId=AdminKeyInfo  #保护密钥信息
        self.CertRequest=GenCertGroup.GenCertClass(self.testCtrl,AdminKeyInfo)   #创建证书申请对象
    
    def positiveCase(self):
        #插入1支有证书的U盾，输入有效参数值，点击签名测试，网页签名结果栏返回签名结果        
        caseTitle =  "插入1支有证书的U盾，输入有效参数值，点击签名测试，网页签名结果栏返回签名结果"
        caseResult=None
        e = None
      
        certResult = self.CertRequest.genCert_with_RSA2048_Mix()
        if certResult[1]:
            CertDn=certResult[0]        
            testResult=self.testCtrl.get_DispSign(CertDn[0],hashId,xmlInfo,dispInfo,certResult[2])
            testResult=re.sub(re.compile('\s+'),' ',testResult)
            if right_Info in testResult[0:3] and len(testResult)>100:
                caseResult="pass"                        
            else:
                caseResult="fail"
                e="实测返回："+"“"+testResult+"”"
        else:
            caseResult="fail"
            e="实测返回："+"下证失败，结束用例执行！"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult         
            
    def negativeCase_formatKey_voidParaChoice(self):
        #用例描述：插入1支无证书的U盾，不输入任何参数值，点击签名测试，期望返回“签名失败:未知错误。返回码:-304 Failed Param!”
        caseTitle  = "用例——插入1支无证书的U盾，不输入任何参数值，点击签名测试，期望返回“签名失败:未知错误。返回码:-304 Failed Param!”"
        caseResult=None
        e=None

        initResult=self.CertRequest.init_key(str_srcPin,str_srcPin) 
        if initResult[0]:
            testResult=self.testCtrl.get_DispSign(None,None,None,None,initResult[1])
            testResult=re.sub(re.compile('\s+'),' ',testResult)      
            if operator.eq(testResult,para_Err):
                caseResult="pass"                        
            else:
                caseResult="fail"
                e="实测返回："+"“"+re.sub(re.compile('\s+'),' ',testResult)+"”"
        else:
            caseResult="fail"
            e="实测返回："+"初始化操作失败，结束用例执行！"
            
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult 
                    
    def negativeCase_oneCert_voidParaChoice(self):
        #用例描述：插入1支有证书的U盾，不输入任何参数值，点击签名测试，期望返回“签名失败:未知错误。返回码:-405 no matching cert!”
        caseTitle  = "用例——插入1支有证书的U盾，不输入任何参数值，点击签名测试，期望返回“签名失败:未知错误。返回码:-304 Failed Param!”"
        caseResult=None
        e=None

        certResult=self.CertRequest.genCert_with_RSA1024_Mix() 
        if certResult[1]: 
            testResult=self.testCtrl.get_DispSign(None,None,None,None,certResult[2])
            testResult=re.sub(re.compile('\s+'),' ',testResult)      
            if operator.eq(testResult,para_Err):
                caseResult="pass"                        
            else:
                caseResult="fail"
                e="实测返回："+"“"+testResult+"”"
        else:
            caseResult="fail"
            e="实测返回："+"下证失败，结束用例执行！"
            
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult     
       
    def operationCase_PinUI_pressC(self):
        #用例描述：签名等待输入验证密码状态，点击UI弹框上的取消,返回“签名失败:未知错误。返回码:-100 User cancel!”
        caseTitle  = "用例——签名等待输入验证密码状态,点击UI弹框上的取消,返回“签名失败:未知错误。返回码:-100 User cancel!”"
        caseResult=None
        e=None

        certResult=self.CertRequest.genCert_with_RSA1024_Mix()  
        if certResult[1]:
            CertDn = certResult[0]
            testResult=self.testCtrl.get_DispSign(CertDn[0],hashId,xmlInfo,dispInfo,certResult[2],1,0)
            testResult=re.sub(re.compile('\s+'),' ',testResult) 
            if operator.eq(testResult,cancel_Err):
                caseResult="pass"                        
            else:
                caseResult="fail"
                e="实测返回："+"“"+testResult+"”"
        else:
            caseResult="fail"
            e="实测返回："+"下证失败，结束用例执行！"
                    
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult 
           
    def operationCase_PinUI_pinErr(self):
        #用例描述：签名时弹出密码输入框，输入错误密码,返回“签名失败:未知错误。返回码:-205 PIN Error!”
        caseTitle  = "用例——签名等待输入验证密码状态，输入错误密码,请确认弹出错误密码提示框，选择是，返回密码输入界面等待重新输入，为方便测试关闭UI框结束本次操作"
        caseResult=None        
        e=None

        certResult=self.CertRequest.genCert_with_RSA1024_Sign_P() 
        if certResult[1]:
            CertDn = certResult[0] 
            testResult=self.testCtrl.get_DispSign(CertDn[0],hashId,xmlInfo,dispInfo,str_errPin)
            testResult=re.sub(re.compile('\s+'),' ',testResult) 
            if operator.eq(testResult,cancel_Err):
                caseResult="pass"                        
            else:
                caseResult="fail"
                e="实测返回："+"“"+testResult+"”"
        else:
            caseResult="fail"
            e="实测返回："+"下证失败，结束用例执行！"
            
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult  
       
    def operationCase_PinUI_pinLock(self):
        #用例描述：签名时弹出密码输入框，输入错误密码，直至U盾被锁死,返回“签名失败:未知错误。返回码:-221 Pin Locked!”
        caseTitle  = "用例——签名等待输入验证密码状态，输入错误密码,直至U盾被锁死,返回“签名失败:未知错误。返回码:-221 Pin Locked!”"
        caseResult=None
        e=None
        
        win32api.MessageBox(0, "等待按键状态,请按U盾确认键", "提示框",win32con.MB_OK)
        #CertDn=["CN=TestRSA1024,OU=MiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOu,O=rsaperca139.com.cn"]
        #testResult=self.testCtrl.get_DispSign(CertDn[0],hashId,xmlInfo,dispInfo,str_errPin)
        
        certResult=self.CertRequest.genCert_with_RSA1024_Mix()          
        if certResult[1]:
            CertDn = certResult[0] 
            count=0
            testResult=""
            while count < 7 :
                testResult=self.testCtrl.get_DispSign(CertDn[0],hashId,xmlInfo,dispInfo,str_errPin)
                count += 1
            testResult=re.sub(re.compile('\s+'),' ',testResult) 
            if operator.eq(testResult,pin_Lock_Err):
                caseResult="pass"                        
            else:
                caseResult="fail"
                e="实测返回："+"“"+testResult+"”"
        else:
            caseResult="fail"
            e="实测返回："+"下证失败，结束用例执行！"
            
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult
          
    def operationCase_pressC(self):
        #用例描述：签名等待按键状态，按下键盘Esc/空格/回车键，或U盾上下翻页键,应无反应，U盾保持等待按键状态！\
        #        按下U盾取消键，返回“签名失败:未知错误。返回码:-100 User cancel!”错误提示
        caseTitle  = "用例——签名等待按键状态,按下键盘Esc/空格/回车键或U盾上下翻页键,应无反应,U盾保持等待按键状态！按下U盾取消键,返回“签名失败:未知错误。返回码:-100 User cancel!”错误提示"
        caseResult=None
        e=None 
        win32api.MessageBox(0, "确认签名等待按键状态,按下键盘Esc/空格/回车键或U盾上下翻页键,应无反应,U盾保持等待按键状态！按下U盾取消键,返回“签名失败:未知错误。返回码:-100 User cancel!”错误提示", "提示框",win32con.MB_OK)
        
        certResult=self.CertRequest.genCert_with_RSA1024_Mix()  
        if certResult[1]:
            CertDn = certResult[0] 
            testResult=self.testCtrl.get_DispSign(CertDn[0],hashId,xmlInfo,dispInfo,certResult[2])
            testResult=re.sub(re.compile('\s+'),' ',testResult)
            if cancel_Err == testResult:
                caseResult="pass"                        
            else:
                caseResult="fail"
                e="实测返回："+"“"+testResult+"”"
        else:
            caseResult="fail"
            e="实测返回："+"下证失败，结束用例执行！" 
                   
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult  
       
    def operationCase_timeout(self):
        #用例描述：签名弹出按键提示框，不按键，等待15Min超时时,返回“签名失败:未知错误。返回码:-105 Time out!”
        caseTitle  = "用例——签名等待按键状态,不按键，等待15Min超时时,返回“签名失败:未知错误。返回码:-105 Time out!”错误提示"
        caseResult = None
        e=None
        
        win32api.MessageBox(0, "确认签名等待按键状态,不操作，等待15min", "提示框",win32con.MB_OK)

        certResult=self.CertRequest.genCert_with_RSA2048_Mix()  
        if certResult[1]:
            CertDn = certResult[0] 
            testResult=self.testCtrl.get_DispSign(CertDn[0],hashId,xmlInfo,dispInfo,certResult[2])
            testResult=re.sub(re.compile('\s+'),' ',testResult)
            if operator.eq(testResult, time_out_Err):
                caseResult="pass"                        
            else:
                caseResult="fail"
                e="实测返回："+"“"+re.sub(re.compile('\s+'),' ',testResult)+"”"
        else:
            caseResult="fail"
            e="实测返回："+"下证失败，结束用例执行！" 
                    
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult  
       
    def operationCase_outKey(self):
        #用例描述：签名弹出按键提示框，直接拔出U盾,返回“签名失败:未知错误。返回码:-100 User cancel!”
        caseTitle  = "用例——签名等待按键状态,直接拔出U盾,返回“签名失败:未知错误。返回码:-100 User cancel!”"
        caseResult = None
        e=None
        win32api.MessageBox(0, "确认签名等待按键状态，直接拔出U盾", "提示框",win32con.MB_OK)

        certResult=self.CertRequest.genCert_with_RSA1024_Mix()  
        if certResult[1]:        
            CertDn = certResult[0] 
            testResult=self.testCtrl.get_DispSign(CertDn[0],hashId,xmlInfo,dispInfo,certResult[2])
            testResult=re.sub(re.compile('\s+'),' ',testResult)
            if operator.eq(cancel_Err,testResult) or operator.eq(no_key_Err,testResult):
                caseResult="pass"                        
            else:
                caseResult="fail"
                e="实测返回："+"“"+testResult+"”"
        else:
            caseResult="fail"
            e="实测返回："+"下证失败，结束用例执行！" 
                            
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
            
        win32api.MessageBox(0, "确认U盾已重新插入，确保后续测试顺利进行", "提示框",win32con.MB_OK)
        return caseResult 

    def positiveCase_supportedMixCertTest(self):
        #用例描述：进行初始化-下证-二代签名/文件签名，覆盖支持的所有证书
        caseTitle  = "用例——进行初始化-下证-二代签名/文件签名，覆盖所有混用证书及其哈希方式，二代签名返回成功"
        caseResult = None
        e=None
        
        win32api.MessageBox(0, "确认签名等待按键状态,按下U盾确认键", "提示框",win32con.MB_OK)        
        '''        
        mixCertDict={
            CertListInfoMap["RSA1024_Mixed_sha1"],
            #CertListInfoMap["RSA1024_Mixed_sha256"], 
            }
        signHash=['SHA384']
        '''
        str_xml=xmlInfo
        str_dispData=dispInfo
        signHash=['SHA1','SHA256','SHA384','SHA512']
        logger.critical("beginning... || %s ",caseTitle)        
        for mix_cert in mixCertDict:
            certResult=self.CertRequest.genCert_With_Verify(mix_cert,str_srcPin,True)            
            if certResult[1]: 
                CertDn = certResult[0]                  
                for str_Hash in signHash:
                    if (mix_cert.count('RSA') and 'SM3'==str_Hash) or (mix_cert.count('SM2') and 'SM3' != str_Hash):
                        continue
                    #显示签名
                    testResult=self.testCtrl.get_DispSign(CertDn[0],str_Hash,str_xml,str_dispData,certResult[2])
                    testResult=re.sub(re.compile('\s+'),' ',testResult)
                    if 'SHA512' == str_Hash and mix_cert.count("RSA1024"): #RSA混用证书不支持sha512签名
                        logger.critical("该证书不支持显示签名 || %s || %s ",mix_cert,str_Hash)
                        continue
                    else:
                        if right_Info in testResult[0:3] and len(testResult)>100:
                            caseResult="pass"                    
                            logger.critical("DispSign || %s || %s || %s ",caseResult,mix_cert,str_Hash)
                        else:
                            caseResult="fail"
                            logger.critical("DispSign || %s || %s || %s || %s",caseResult,mix_cert,str_Hash,testResult)
                    #文件签名
                    testResult=self.testCtrl.get_FileSign(CertDn[0],str_Hash,str_xml,str_dispData,batFilePath,p7FilePath,certResult[2])
                    testResult=re.sub(re.compile('\s+'),' ',testResult)
                    if operator.eq(testResult, unsupported_cert_Err) or (operator.eq(testResult, ver_Err)and False==self.AdminKeyAlgId[0]):
                        caseResult = "pass"
                        logger.critical("FileSign ||%s || %s || %s ", caseResult, mix_cert, str_Hash)
                    else:
                        caseResult = "fail"
                        logger.critical("FileSign ||%s || %s || %s ||%s", caseResult, mix_cert, str_Hash, testResult)
            else:
                caseResult="fail"
                e="下证失败，结束本证书执行"
                logger.critical("%s || %s || %s ",caseResult,mix_cert,e)
                continue
        logger.critical("end. || %s ",caseTitle) 
        return caseResult 
        
    def negativeCase_supportedCommCertTest(self):
        #用例描述：进行初始化-下证-二代签名，覆盖支持的所有证书
        caseTitle  = "用例——进行初始化-下证-二代签名，覆盖所有通用证书及其哈希方式,二代签名返回“签名失败:未知错误。返回码:-405 no matching cert!”"
        caseResult = None
        e=None
        '''
        commCertDict={
            CertListInfoMap["RSA1024_Comm_p_sha1"],
            #CertListInfoMap["RSA1024_Comm_p_sha256"], 
            }
        signHash=['SHA384']
        '''
        str_xml=xmlInfo
        str_dispData=dispInfo
        signHash=['SHA1','SHA256','SHA384','SHA512','SM3']
        logger.critical("beginning... || %s ",caseTitle)        
        for comm_cert in commCertDict:
            certResult=self.CertRequest.genCert_With_Verify(comm_cert,str_srcPin,True)            
            if certResult[1]: 
                CertDn = certResult[0]                  
                for str_Hash in signHash:
                    if (comm_cert.count('RSA') and 'SM3'==str_Hash) or (comm_cert.count('SM2') and 'SM3' != str_Hash):
                        continue
                    #显示签名
                    testResult=self.testCtrl.get_DispSign(CertDn[0],str_Hash,str_xml,str_dispData,certResult[2])
                    testResult=re.sub(re.compile('\s+'),' ',testResult)                                   
                    if operator.eq(unsupported_cert_Err,testResult) or (operator.eq(testResult, ver_Err)and False==self.AdminKeyAlgId[0]):
                        caseResult="pass"                    
                        logger.critical("DispSign || %s || %s || %s ",caseResult,comm_cert,str_Hash)
                    else:
                        caseResult="fail"
                        logger.critical("DispSign || %s || %s || %s || %s",caseResult,comm_cert,str_Hash,testResult)

                    #文件签名
                    testResult=self.testCtrl.get_FileSign(CertDn[0],str_Hash,str_xml,str_dispData,batFilePath,p7FilePath,certResult[2])
                    testResult=re.sub(re.compile('\s+'),' ',testResult)
                    if operator.eq(unsupported_cert_Err,testResult):
                        caseResult = "pass"
                        logger.critical("FileSign || %s || %s || %s ", caseResult, comm_cert, str_Hash)
                    else:
                        caseResult = "fail"
                        logger.critical("FileSign || %s || %s || %s || %s", caseResult, comm_cert, str_Hash, testResult)
            else:
                caseResult="fail"
                e="下证失败，结束本证书执行"
                logger.critical("%s || %s || %s ",caseResult,comm_cert,e)
                continue
        logger.critical("end. || %s ",caseTitle)    
        return caseResult 
 
    def positiveCase_supportedDispCertTest(self):
        #用例描述：进行初始化-下证-二代签名，覆盖支持的所有证书
        caseTitle  = "用例——进行初始化-下证-二代签名，覆盖所有显示证书及其哈希方式，二代签名返回成功"
        caseResult = None
        e=None
        win32api.MessageBox(0, "确认签名等待按键状态,按下U盾确认键", "提示框",win32con.MB_OK)        
        signResultList=[]
        '''
        dispCertDict={
            CertListInfoMap["RSA2048_Sig2_p_sha1"],
            #CertListInfoMap["RSA1024_Mixed_sha256"], 
            }
        signHash=['SHA1']
        '''
        str_xml=xmlInfo
        str_dispData=dispInfo
        signHash=['SHA1','SHA256','SHA384','SHA512','SM3']
        logger.critical("beginning... || %s ",caseTitle)        
        for disp_cert in dispCertDict:
            certResult=self.CertRequest.genCert_With_Verify(disp_cert,str_srcPin,True)            
            if certResult[1]: 
                CertDn = certResult[0]                  
                for str_Hash in signHash:
                    if (disp_cert.count('RSA') and 'SM3'==str_Hash) or (disp_cert.count('SM2') and 'SM3' != str_Hash):
                        continue
                    #显示签名
                    testResult=self.testCtrl.get_DispSign(CertDn[0],str_Hash,str_xml,str_dispData,certResult[2])
                    testResult=re.sub(re.compile('\s+'),' ',testResult)                                                          
                    if right_Info in testResult[0:3] and len(testResult)>100:
                        caseResult="pass"                    
                        logger.critical("DispSign || %s || %s || %s ",caseResult,disp_cert,str_Hash)
                        temp=disp_cert[6:disp_cert.find(",")]+" || "
                        testResult=temp+testResult
                        signResultList.append(testResult)
                    else:
                        caseResult="fail"
                        logger.critical("DispSign || %s || %s || %s ||%s",caseResult,disp_cert,str_Hash,testResult)

                    #文件签名
                    testResult = self.testCtrl.get_FileSign(CertDn[0], str_Hash, str_xml, str_dispData, batFilePath,p7FilePath,certResult[2])
                    testResult = re.sub(re.compile('\s+'), ' ', testResult)
                    if file_sign_info in testResult or (operator.eq(testResult, ver_Err)and False==self.AdminKeyAlgId[0]):
                        caseResult = "pass"
                        logger.critical("FileSign || %s || %s || %s ", caseResult, disp_cert, str_Hash)
                    else:
                        caseResult = "fail"
                        logger.critical("FileSign || %s || %s || %s ||%s", caseResult, disp_cert, str_Hash, testResult)
            else:
                caseResult="fail"
                e="下证失败，结束本证书执行"
                logger.critical("%s || %s || %s ",caseResult,disp_cert,e)
                continue
        logger.critical("end. || %s ",caseTitle)
         
        #保存签名结果至文件，便于后续验签操作
        if len(signResultList):
            fp=open('signResult.txt','a+',encoding='utf-8')
            if fp:
                for i in signResultList:
                    fp.write(i)
                    fp.write('\n')
            fp.close()    
        return caseResult 
      
    def negativeCase_rsaCert_errHashChoice(self):
        #用例描述：RSA证书进行二代签名时，选择Hash算法为SM3,期望返回“签名失败:未知错误。返回码:-409 Sign failed!”错误提示
        caseTitle  = "用例——RSA证书二代签名，选择Hash为SM3,期望返回“签名失败:未知错误。返回码:-409 Sign failed!”错误提示"
        caseResult=None
        e=None
        str_Hash='SM3'
        logger.critical("beginnning... || %s ",caseTitle)
        certResult=self.CertRequest.genCert_with_rsa1024M_and_rsa2048M()
        #certResult=self.CertRequest.genCert_with_RSA1024_Mix()  
        if certResult[1]: 
            CertDnList = certResult[0]
            for CertDn in CertDnList:
                #显示签名
                testResult=self.testCtrl.get_DispSign(CertDn,str_Hash,xmlInfo,dispInfo,certResult[2])
                testResult=re.sub(re.compile('\s+'),' ',testResult) 
                if operator.eq(testResult,unmatched_hash_Err):
                    caseResult="pass"              
                    logger.critical("%s || %s || %s ",caseResult,CertDn[0:CertDn.find(",")],str_Hash)                                             
                else:
                    caseResult="fail"
                    logger.critical("%s || %s || %s || %s ",caseResult,CertDn[0:CertDn.find(",")],str_Hash,testResult)                                                                 
        else:
            caseResult="fail"
            e="下证失败，结束本证书执行"
            logger.critical("%s || %s",caseResult,e)
                        
        logger.critical("end. || %s ",caseTitle)    
        return caseResult         
    
    def negativeCase_sm2Cert_errHashChoice(self):
        #用例描述：SM2证书进行二代签名时，选择Hash算法为SHA1,返回码:-409
        caseTitle  = "用例——SM2证书二代签名时，选择Hash为SHA1/SHA256/SHA384/SHA512,期望返回“签名失败:未知错误。返回码:-409 Sign failed!”错误提示"
        caseResult=None        
        e=None          
        signHash = ['SHA1','SHA256','SHA384','SHA512'] 
         
        logger.critical("beginning... || %s ",caseTitle)             
        certResult=self.CertRequest.genCert_with_SM2_Sign_P()  
        if certResult[1]: 
            CertDn = certResult[0]      
            for str_Hash in signHash:
                testResult=self.testCtrl.get_DispSign(CertDn[0],str_Hash,xmlInfo,dispInfo,certResult[2])
                testResult=re.sub(re.compile('\s+'),' ',testResult) 
                if operator.eq(testResult,unmatched_hash_Err):
                    caseResult="pass"        
                    logger.critical("%s || %s || %s ",caseResult,CertDn[0][0:CertDn[0].find(",")],str_Hash)                                             
                else:
                    caseResult="fail"
                    logger.critical("%s || %s || %s || %s ",caseResult,CertDn[0][0:CertDn[0].find(",")],str_Hash,testResult)                                                                 
        else:
            caseResult="fail"
            e="下证失败，结束本证书执行"
            logger.critical("%s || %s",caseResult,e)
                        
        logger.critical("end. || %s ",caseTitle)    
        return caseResult                     
    
    def negativeCase_noKey_voidParaChoice(self):
        #用例描述：未插入U盾，不输入任何参数，点击签名测试，期望返回签名失败:未知错误。返回码:-102 There is no key!
        caseTitle  = "用例——未插入U盾，不输入任何参数，点击签名测试，期望返回“签名失败:未知错误。返回码:-102 There is no key!”"
        caseResult=None        
        e=None
 
        testResult=self.testCtrl.get_DispSign(None,None,None,None,str_verifyPin)
        #textResultTestGMUsbKeySign = self.testCtrl.browser.find_element_by_id("ResultTestGMUsbKeySign")                                 
        #testResult=textResultTestGMUsbKeySign.get_attribute('value')
        testResult=re.sub(re.compile('\s+'),' ',testResult)      
        if operator.eq(testResult,no_key_Err):
            caseResult="pass"                        
        else:
            caseResult="fail"
            e="实测返回："+"“"+testResult+"”"
            
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult                      
    
    def negativeCase_noKey_validParaChoice(self):
        #用例描述：未插入U盾，各参数栏输入合法参数，点击签名测试，期望返回获取介质号失败:未知错误。返回码:-102 There is no key!
        caseTitle  = "用例——未插入U盾，各参数栏输入合法参数，点击签名测试，期望返回“签名失败:未知错误。返回码:-102 There is no key!”"
        caseResult=None
        e=None

        certDn="CN=TestRSA1024,OU=MiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOu,O=rsaperca139.com.cn" 
        strHashId=hashId
        strXmlInfo=xmlInfo
        strDispData=dispInfo
        strPin=str_srcPin  
        testResult=self.testCtrl.get_DispSign(certDn,strHashId,strXmlInfo,strDispData,strPin)
        #textResultTestGMUsbKeySign = self.testCtrl.browser.find_element_by_id("ResultTestGMUsbKeySign")                                 
        #testResult=textResultTestGMUsbKeySign.get_attribute('value')
        testResult=re.sub(re.compile('\s+'),' ',testResult)      
        if operator.eq(testResult,no_key_Err):
            caseResult="pass"                        
        else:
            caseResult="fail"
            e="实测返回："+"“"+testResult+"”"
            
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult  

    def nagativeCase_manyKey_validParaChoice(self):           
        #用例描述：插入多支同款U盾，输入合法请求信息，测试签名   期望返回：“签名失败:未知错误。返回码:-104 There is more than one key!”
        caseTitle = "用例——插入多个同款U盾，输入合法请求信息，生成P10包   期望返回：“签名失败:未知错误。返回码:-104 There is more than one key!”"
        e = None
 
        certDn="CN=TestRSA1024,OU=MiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOu,O=rsaperca139.com.cn"
        strHashId=hashId
        strXmlInfo=xmlInfo
        strDispData=dispInfo
        strPin=str_srcPin
         
        testResult=self.testCtrl.get_DispSign(certDn,strHashId,strXmlInfo,strDispData,strPin)
        #textResultTestGMUsbKeySign = self.testCtrl.browser.find_element_by_id("ResultTestGMUsbKeySign")                                 
        #testResult=textResultTestGMUsbKeySign.get_attribute('value')
        testResult=re.sub(re.compile('\s+'),' ',testResult)
        if operator.eq(testResult,many_key_Err):
            caseResult="pass"                        
        else:
            caseResult="fail"
            e="实测返回："+"“"+testResult+"”"
            
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult 

#########################
#开始测试
#########################
