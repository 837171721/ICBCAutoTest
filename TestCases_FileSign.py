#coding=utf-8
'''
Created on 2018.08.18 @author: ys
'''
import re         #引入正在表达式
import operator
import win32api
import win32con 
import GenCertGroup 
from GlobalConfigure import levels, log_level,str_srcPin,str_defaultPin,hashId,xmlInfo,dispInfo
from GlobalConfigure import batFilePath,p7FilePath,dispCertDict,commCertDict,mixCertDict,CertListInfoMap
from GlobalConfigure import batFilePath2K,batFilePath5K,batFilePath10K
from GlobalConfigure import batFilePath1M,batFilePath5M,batFilePath10M,batFilePath50M,batFilePath90M

from logTest import SysClass, LoggerClass
from _ast import Continue
conf  = LoggerClass(loglevel=levels.get(log_level), logger="TestCases_FileSign.py")
logger=conf.getlogger()

#错误信息列表
no_key_Err=  '''签名失败:未知错误。返回码:-102 There is no key!'''
many_key_Err='''签名失败:未知错误。返回码:-104 There is more than one key!'''
cancel_Err='''签名失败:未知错误。返回码:-100 User cancel!'''
para_Err='''签名失败:未知错误。返回码:-304 Failed Param!'''
pin_Err='''签名失败:未知错误。返回码:-205 PIN Error!'''
pin_Lock_Err='''签名失败:未知错误。返回码:-221 Pin Locked!'''
time_out_Err='''签名失败:未知错误。返回码:-105 Time out!'''
unsupported_cert_Err='''签名失败:未知错误。返回码:-405 no matching cert!'''
unmatched_hash_Err='''签名失败:未知错误。返回码:-409 Sign failed!'''  #签名失败:未知错误。返回码:-409 Sign failed!"
ver_Err='''签名失败:未知错误。返回码:-411 ukey version error!'''
file_Err="签名失败:未知错误。返回码:-320 File error!"


disp_sign_Info="MII"
file_sign_info = '''签名成功'''
str_errPin='12121212'
err_bat_path="X:\\"
err_file_path="X:\\"

def test_GetFileSign(ctrlObj,TestingRange,AdminKeyInfo):
    testCtrl=FileSignCases(ctrlObj,AdminKeyInfo)  #建立类对象，打开控件测试页
    if not AdminKeyInfo[0]:
        certResult=GenCertGroup.GenCertClass(testCtrl.testCtrl, AdminKeyInfo).genCert_with_RSA1024_Sign_P()
        if certResult[1]:
            CertDn = certResult[0]
            testResult = testCtrl.testCtrl.get_FileSign(CertDn[0], hashId, xmlInfo, dispInfo, batFilePath, p7FilePath,certResult[2])
            testResult = re.sub(re.compile('\s+'), ' ', testResult)
            if operator.eq(testResult, ver_Err):
                logger.warning("接口不支持，请选择国密盾进行!")
                return

    testFileSignCase(testCtrl,TestingRange)   #测试用例集，根据测试范围定义测试强度
        
def testFileSignCase(ctrlObj,testRange):
    #测试用例集
    if 0 == testRange:  #详细测试
        testResult=ctrlObj.negativeCase_noCert_voidParaChoice()
        
        testResult=ctrlObj.negativeCase_oneCert_voidParaChoice()  
        
        testResult=ctrlObj.negativeCase_oneCert_errPathParaChoice()

        testResult=ctrlObj.operationCase_PinUI_pressC()#15、输入错误密码，直至U盾被锁死
        
        testResult=ctrlObj.operationCase_PinUI_pinErr()#17、按键提示框按C键
        
        testResult=ctrlObj.operationCase_PinUI_pinLock()#18、按键提示框，按U盾上下翻键
        
        testResult=ctrlObj.operationCase_pressC()#19、等待15Min超时时间
        
        testResult=ctrlObj.operationCase_timeout()#20、按键等待时，按下键盘的Esc、空格、回车键
        
        testResult=ctrlObj.operationCase_outKey()#21、拔出key
                      
        testResult=ctrlObj.negativeCase_rsaCert_errHashChoice()#23、RSA证书选择SM
       
        testResult=ctrlObj.negativeCase_sm2Cert_errHashChoice()#24、SM证书选择RSA
        
        #testResult=ctrlObj.positiveCase_supportedSignFileSize()
        
        #testResult=ctrlObj.negativeCase_supportedCommCertSign()

        #testResult=ctrlObj.negativeCase_supportedMixCertSign()
               
        #testResult=ctrlObj.negativeCase_manyKey_validParaChoice()
   
        #testResult=ctrlObj.negativeCase_operation()
                     
    elif 1 == testRange: #验证测试
        testResult=ctrlObj.positiveCase()
        
    elif 2 == testRange: #无key测试
        testResult=ctrlObj.negativeCase_noKey_voidParaChoice()
        
        testResult=ctrlObj.negativeCase_noKey_validParaChoice()        
        
    elif 3 == testRange: #多key测试
        testResult=ctrlObj.negativeCase_manyKey_validParaChoice()
        
    elif 4 == testRange: #多key测试
        testResult=ctrlObj.positiveCase()
    
    else:
        a=0
       
class FileSignCases():
    def __init__(self,testCtrl,AdminKeyInfo):
        self.testCtrl=testCtrl   #控件测试页
        self.AdminKeyAlgId=AdminKeyInfo  #保护密钥信息
        self.CertRequest=GenCertGroup.GenCertClass(self.testCtrl,AdminKeyInfo)   #创建证书申请对象
    
    def positiveCase(self):
        #用例描述：插入U盾，输入合法参数，点击大文件签名测试；期望返回：签名结果返回到P7文件路径文件夹
        caseTitle  = "用例——插入U盾，输入合法参数，点击大文件签名测试；期望返回：签名结果返回到P7文件路径文件夹"
        caseResult = None
        e=None
        certResult=self.CertRequest.genCert_with_RSA2048_Sign_P()  
        if certResult[1]: 
            CertDn=certResult[0]
            testResult=self.testCtrl.get_FileSign(CertDn[0],hashId,xmlInfo,dispInfo,batFilePath,p7FilePath,certResult[2])
            #textResultTestGMUsbKeySign = self.testCtrl.browser.find_element_by_id("ResultTestGMUsbKeySign")                                 
            #testResult=textResultTestGMUsbKeySign.get_attribute('value')
            testResult = re.sub(re.compile('\s+'),' ',testResult)
            if file_sign_info in testResult:
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
    
    def negativeCase_noCert_voidParaChoice(self):        
        #用例描述：插入一支无证书U盾，不输入任何参数，点击大文件签名测试；期望返回“签名失败:未知错误。返回码:-304 Failed Param!”
        caseTitle  = "用例——插入一支无证书U盾,不输入任何参数,点击大文件签名测试,期望返回“签名失败:未知错误。返回码:-304 Failed Param!”"
        caseResult = None
        e=None
        
        initResult = self.CertRequest.init_key(str_srcPin,str_srcPin)
        if initResult[0]:        
            testResult=self.testCtrl.get_FileSign(None,None,None,None,None,None,initResult[1])
            testResult = re.sub(re.compile('\s+'),' ',testResult) 
            if operator.eq(testResult,para_Err):
                caseResult="pass"                        
            else:
                caseResult="fail"
                e="实测返回："+"“"+testResult+"”"
        else:
            caseResult="fail"
            e="实测返回："+"初始化操作失败，结束用例执行！"
                  
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult
        
    def negativeCase_oneCert_voidParaChoice(self):
        #用例描述：插入一支有证书U盾，不输入任何参数，点击大文件签名测试；期望返回“签名失败:未知错误。返回码:-304 Failed Param!”      
        caseTitle  = "用例——插入一支有证书U盾,不输入任何参数,点击大文件签名测试,期望返回“签名失败:未知错误。返回码:-304 Failed Param!”"
        caseResult = None
        e=None
        
        certResult=self.CertRequest.genCert_with_RSA1024_Sign_P()
        if certResult[1]: 
            testResult=self.testCtrl.get_FileSign(None,None,None,None,None,None,certResult[2])
            testResult = re.sub(re.compile('\s+'),' ',testResult) 
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
   
    def positiveCase_supportedSignFileSize(self):
        #用例描述：插入U盾，输入合法参数，遍历批量文件路径文件大小为1K/2K/5K/10K/1M/5M/10M/50M/90M点击大文件签名测试；期望返回：签名结果返回到P7文件路径文件夹
        caseTitle  = "用例——插入U盾，输入合法参数，点击大文件签名测试；期望返回“签名成功，签名结果保存至指定的P7文件中”"
        caseResult = None
        
        pathList = [batFilePath,batFilePath2K,batFilePath5K,batFilePath10K,batFilePath1M,batFilePath5M,batFilePath10M,batFilePath50M,batFilePath90M] 
        #pathList = [batFilePath]
        logger.critical("beginning... || %s ",caseTitle) 
        certResult=self.CertRequest.genCert_with_RSA2048_Sign_P()
        if certResult[1]: 
            CertDn=certResult[0]  
            for str_file in pathList:
                testResult=self.testCtrl.get_FileSign(CertDn[0],hashId,xmlInfo,dispInfo,str_file,p7FilePath,certResult[2])
                testResult = re.sub(re.compile('\s+'),' ',testResult) 
                if  file_sign_info in testResult:
                    caseResult="pass"
                    logger.critical("%s || 签名源文件：%s ||签名结果文件 ：%s",caseResult,str_file,p7FilePath) 
                else:
                    caseResult="fail"
                    logger.critical("%s || 签名源文件：%s || %s",caseResult,str_file,testResult)
        else:
            caseResult="fail"
            e="下证失败，结束本用例执行"
            logger.critical("%s || %s ",caseResult,e)
        
        logger.critical("end. || %s ",caseTitle)  

        return caseResult  
    
    def negativeCase_oneCert_errPathParaChoice(self):
        #用例描述：输入批量文件路径和P7文件路径为空或输入错误，其他项正常输入，进行大文件签名；期望返回“签名失败:未知错误。返回码:-320 File error!”        
        caseTitle  = "用例——输入批量文件路径和P7文件路径为空或输入错误,其他项正常输入,进行大文件签名,期望返回“签名失败:未知错误。返回码:-320 File error!"
        caseResult = None
        e=None
        #batPath=['None']
        #p7filePath=['None']
        #certResult=[["CN=TestRSA1024.p.0200.0102,OU=MiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOu,O=rsaperca139.com.cn"],True,'1q1q1q1q']
        
        logger.critical("beginning... || %s ",caseTitle)       
        batPath=['','None',err_bat_path,batFilePath]
        p7filePath=['','None',err_file_path,p7FilePath]                   
        certResult=self.CertRequest.genCert_with_RSA1024_Sign_P()

        if certResult[1]: 
            CertDn=certResult[0]  
            for str_bat in batPath:           
                for str_file in p7filePath:               
                        testResult=self.testCtrl.get_FileSign(CertDn[0],hashId,xmlInfo,dispInfo,str_bat,str_file,certResult[2])
                        testResult = re.sub(re.compile('\s+'),' ',testResult)
                        if operator.eq(str_bat,'None') or operator.eq(str_bat,batFilePath):
                            if operator.eq(str_file,'None') or operator.eq(str_file,p7filePath):
                                if file_sign_info in testResult:
                                    caseResult="pass"
                                else:
                                    caseResult="fail" 
                            else:
                                if operator.eq(testResult,file_Err):
                                    caseResult="pass"
                                else:
                                    caseResult="fail"
                        else:
                            if operator.eq(testResult,file_Err):
                                caseResult="pass"
                            else:
                                caseResult="fail"
                        logger.critical("%s || 批量文件路径：%s || p7文件路径：%s || %s",caseResult,str_bat,str_file,testResult)                                    
        else:
            caseResult="fail"
            e="实测返回："+"下证失败，结束用例执行！"
            logger.critical("%s || %s ",caseResult,e)
            
        logger.critical("end. || %s ",caseTitle)
        return caseResult
    
    def operationCase_PinUI_pressC(self):
        #用例描述：签名时弹出密码输入框，不输入密码，点取消，期望返回“签名失败:未知错误。返回码:-100 User cancel!”
        caseTitle  = "用例——签名时弹出密码输入框,不输入密码,点取消,返回“签名失败:未知错误。返回码:-100 User cancel!”"
        caseResult = None
        e=None

        certResult=self.CertRequest.genCert_with_RSA1024_Sign_P()  
        if certResult[1]:
            CertDn=certResult[0] 
            testResult=self.testCtrl.get_FileSign(CertDn[0],hashId,xmlInfo,dispInfo,batFilePath,p7FilePath,certResult[2],1,0)
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
        #用例描述：签名时弹出密码输入框，输入错误密码，期望返回“签名失败:未知错误。返回码:-205 PIN Error!”
        caseTitle  = "用例——签名时弹出密码输入框,输入错误密码,请确认弹出错误密码提示框,选择是，返回密码输入界面等待重新输入，为方便测试关闭UI框结束本次操作”"
        caseResult = None
        e=None
        
        certResult=self.CertRequest.genCert_with_RSA1024_Sign_P()
        if certResult[1]:
            CertDn=certResult[0]   
            testResult=self.testCtrl.get_FileSign(CertDn[0],hashId,xmlInfo,dispInfo,batFilePath,p7FilePath,str_errPin)
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
        #用例描述：签名时弹出密码输入框，输入错误密码，直至U盾被锁死,期望返回“签名失败:未知错误。返回码:-221 Pin Locked!”
        caseTitle  = "用例——签名等待输入验证密码状态，输入错误密码，直至U盾被锁死,期望返回“签名失败:未知错误。返回码:-221 Pin Locked!”"
        caseResult = None
        e=None
        
        win32api.MessageBox(0, "等待按键状态,请按U盾确认键", "提示框",win32con.MB_OK)

        certResult=self.CertRequest.genCert_with_RSA1024_Sign_P()  
        if certResult[1]:
            CertDn = certResult[0] 
            count=0
            testResult=""
            while count < 7 :
                testResult=self.testCtrl.get_FileSign(CertDn[0],hashId,xmlInfo,dispInfo,batFilePath,p7FilePath,str_errPin)
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
        #用例描述：签名弹出按键提示框，按下U盾C键,期望返回“签名失败:未知错误。返回码:-100 User cancel!”错误提示
        caseTitle  = "用例——签名弹出按键提示框，按下U盾C键,期望返回“签名失败:未知错误。返回码:-100 User cancel!”错误提示"
        caseResult = None
        e=None
        
        win32api.MessageBox(0, "确认签名等待按键状态,按下键盘Esc/空格/回车键或U盾上下翻页键,应无反应,U盾保持等待按键状态！按下U盾取消键,返回“签名失败:未知错误。返回码:-100 User cancel!”错误提示", "提示框",win32con.MB_OK)

        certResult=self.CertRequest.genCert_with_RSA2048_Sign_P()  
        if certResult[1]:
            CertDn = certResult[0] 
            testResult=self.testCtrl.get_FileSign(CertDn[0],hashId,xmlInfo,dispInfo,batFilePath,p7FilePath,certResult[2])
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
    
    def operationCase_timeout(self):
        #用例描述：签名弹出按键提示框，不按键，等待15Min超时时,期望返回“签名失败:未知错误。返回码:-105 Time out!”
        caseTitle  = "用例——弹签名弹出按键提示框，不按键，等待15Min超时时,期望返回“签名失败:未知错误。返回码:-105 Time out!”错误提示"
        caseResult = None
        e=None
        
        win32api.MessageBox(0, "确认签名等待按键状态,不操作，等待15min", "提示框",win32con.MB_OK)

        certResult=self.CertRequest.genCert_with_RSA1024_Sign_P() 
        if certResult[1]:
            CertDn = certResult[0]          
            testResult=self.testCtrl.get_FileSign(CertDn[0],hashId,xmlInfo,dispInfo,batFilePath,p7FilePath,certResult[2])
            testResult=re.sub(re.compile('\s+'),' ',testResult)
            if operator.eq(testResult,time_out_Err):
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
        caseTitle  = "用例——签名弹出按键提示框，直接拔出U盾,返回“签名失败:未知错误。返回码:-100 User cancel!”"
        caseResult = None
        e=None
        
        win32api.MessageBox(0, "确认签名等待按键状态，直接拔出U盾", "提示框",win32con.MB_OK)

        certResult=self.CertRequest.genCert_with_RSA1024_Sign_P()  
        if certResult[1]:        
            CertDn = certResult[0] 
            testResult=self.testCtrl.get_FileSign(CertDn[0],hashId,xmlInfo,dispInfo,batFilePath,p7FilePath,certResult[2])
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
    
    def positiveCase_supportedDispCertSign(self):
        caseTitle  = "用例——进行初始化-下证-文件签名，覆盖所有专用证书及其哈希方式，文件签名返回成功"
        caseResult = None
        e=None
        
        win32api.MessageBox(0, "确认签名等待按键状态,按下U盾确认键", "提示框",win32con.MB_OK)        
        '''
        dispCertDict={
            CertListInfoMap["RSA1024_Sig2_p_sha1"],
            #CertListInfoMap["RSA1024_Mixed_sha256"], 
            }
        signHash=['SHA384']
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
                    testResult=self.testCtrl.get_FileSign(CertDn[0],str_Hash,str_xml,str_dispData,batFilePath,p7FilePath,certResult[2])
                    testResult=re.sub(re.compile('\s+'),' ',testResult)
                    
                    if file_sign_info in testResult:
                        caseResult="pass"                    
                        logger.critical("%s || %s || %s ",caseResult,disp_cert,str_Hash)                       
                    else:
                        caseResult="fail"
                        logger.critical("%s || %s || %s ||%s",caseResult,disp_cert,str_Hash,testResult)      
            else:
                caseResult="fail"
                e="下证失败，结束本证书执行"
                logger.critical("%s || %s || %s ",caseResult,disp_cert,e)
                continue
        logger.critical("end. || %s ",caseTitle)
        return caseResult 

    def negativeCase_rsaCert_errHashChoice(self):
        #用例描述：RSA证书进行二代签名时，选择Hash算法为SM3,返回码:-409
        caseTitle  = "用例——RSA证书进行二代签名时，选择Hash为SM3,期望返回“签名失败:未知错误。返回码:-409 Sign failed!”错误提示"
        caseResult = None
        e=None
        
        str_Hash='SM3'
        logger.critical("beginnning... || %s ",caseTitle)
        certResult=self.CertRequest.genCert_with_rsa1024M_and_rsa2048M()  
        if certResult[1]: 
            CertDnList = certResult[0]
            for CertDn in CertDnList:
                testResult=self.testCtrl.get_FileSign(CertDn,str_Hash,xmlInfo,dispInfo,batFilePath,p7FilePath,certResult[2])
                testResult=re.sub(re.compile('\s+'),' ',testResult) 
                if operator.eq(testResult,ver_Err):
                    caseResult="pass"              
                    logger.critical("%s || %s || %s ",caseResult,CertDn[0:14],str_Hash)                                             
                else:
                    caseResult="fail"
                    logger.critical("%s || %s || %s || %s ",caseResult,CertDn[0:14],str_Hash,testResult)                                                                 
        else:
            caseResult="fail"
            e="下证失败，结束本证书执行"
            logger.critical("%s || %s",caseResult,e)
                        
        logger.critical("end. || %s ",caseTitle)    
        return caseResult
   
    def negativeCase_sm2Cert_errHashChoice(self):
        #用例描述：SM2证书进行二代签名时，选择Hash算法为SHA1；先弹出密码输入框，输入密码确定后，返回“签名失败:未知错误。返回码:-409 Sign failed!”错误提示
        caseTitle  = "用例——SM2证书进行二代签名时，选择Hash为SHA1/SHA256/SHA384/SHA512,期望返回“签名失败:未知错误。返回码:-409 Sign failed!”错误提示"
        caseResult = None
        e=None

        signHash = ['SHA1','SHA256','SHA384','SHA512'] 
         
        logger.critical("beginning... || %s ",caseTitle)             
        certResult=self.CertRequest.genCert_with_SM2_Sign_P()  
        if certResult[1]: 
            CertDn = certResult[0]      
            for str_Hash in signHash:
                testResult=self.testCtrl.get_FileSign(CertDn[0],str_Hash,xmlInfo,dispInfo,batFilePath,p7FilePath,certResult[2])
                testResult=re.sub(re.compile('\s+'),' ',testResult) 
                if operator.eq(testResult,unmatched_hash_Err):
                    caseResult="pass"              
                    logger.critical("%s || %s || %s ",caseResult,CertDn[0][0:10],str_Hash)                                             
                else:
                    caseResult="fail"
                    logger.critical("%s || %s || %s || %s ",caseResult,CertDn[0][0:10],str_Hash,testResult)                                                                 
        else:
            caseResult="fail"
            e="下证失败，结束本证书执行"
            logger.critical("%s || %s",caseResult,e)
                        
        logger.critical("end. || %s ",caseTitle)    
        return caseResult                     

    def negativeCase_supportedCommCertSign(self):
        caseTitle  = "用例——进行初始化-下证-文件签名，覆盖所有通用证书，文件签名返回“签名失败:未知错误。返回码:-405 no matching cert!”"
        caseResult = None
        e=None
              
        '''
        commCertDict={
            CertListInfoMap["RSA1024_Comm_p_sha1"],
            }
        signHash=['SHA384']
        '''
        str_xml=xmlInfo
        str_dispData=dispInfo
        signHash=['SHA1','SM3']
        logger.critical("beginning... || %s ",caseTitle)        
        for comm_cert in commCertDict:
            certResult=self.CertRequest.genCert_With_Verify(comm_cert,str_srcPin,True)            
            if certResult[1]: 
                CertDn = certResult[0]                  
                for str_Hash in signHash:
                    if (comm_cert.count('RSA') and 'SM3'==str_Hash) or (comm_cert.count('SM2') and 'SM3' != str_Hash):
                        continue                    
                    testResult=self.testCtrl.get_FileSign(CertDn[0],str_Hash,str_xml,str_dispData,batFilePath,p7FilePath,certResult[2])
                    testResult=re.sub(re.compile('\s+'),' ',testResult)
                    
                    if operator.eq(testResult,unsupported_cert_Err):
                        caseResult="pass"                    
                        logger.critical("%s || %s || %s ",caseResult,comm_cert,str_Hash)                       
                    else:
                        caseResult="fail"
                        logger.critical("%s || %s || %s ||%s",caseResult,comm_cert,str_Hash,testResult)      
            else:
                caseResult="fail"
                e="下证失败，结束本证书执行"
                logger.critical("%s || %s || %s ",caseResult,comm_cert,e)
                continue
        logger.critical("end. || %s ",caseTitle)
        return caseResult 
                
    def negativeCase_supportedMixCertSign(self):
        caseTitle  = "用例——进行初始化-下证-文件签名，覆盖所有混用证书，文件签名返回“签名失败:未知错误。返回码:-409 Sign failed!错误提示”"
        caseResult = None
        e=None
              
        '''
        mixCertDict={
            CertListInfoMap["RSA1024_Mixed_sha1"],
            CertListInfoMap["RSA2048_Mixed_sha1"],
            }
        signHash=['SHA384']
        '''
        
        str_xml=xmlInfo
        str_dispData=dispInfo
        signHash=['SHA1','SM3']
        logger.critical("beginning... || %s ",caseTitle)        
        for mix_cert in mixCertDict:
            certResult=self.CertRequest.genCert_With_Verify(mix_cert,str_srcPin,True)            
            if certResult[1]: 
                CertDn = certResult[0]                  
                for str_Hash in signHash:
                    if (mix_cert.count('RSA') and 'SM3'==str_Hash) or (mix_cert.count('SM2') and 'SM3' != str_Hash):
                        continue                    
                    testResult=self.testCtrl.get_FileSign(CertDn[0],str_Hash,str_xml,str_dispData,batFilePath,p7FilePath,certResult[2])
                    testResult=re.sub(re.compile('\s+'),' ',testResult)
                    
                    if operator.eq(testResult,unsupported_cert_Err):
                        caseResult="pass"                    
                        logger.critical("%s || %s || %s ",caseResult,mix_cert,str_Hash)                       
                    else:
                        caseResult="fail"
                        logger.critical("%s || %s || %s ||%s",caseResult,mix_cert,str_Hash,testResult)      
            else:
                caseResult="fail"
                e="下证失败，结束本证书执行"
                logger.critical("%s || %s || %s ",caseResult,mix_cert,e)
                continue
        logger.critical("end. || %s ",caseTitle)
        return caseResult         

    def negativeCase_noKey_voidParaChoice(self):
        #用例描述：未插入U盾，不输入任何参数，点击大文件签名测试；期望返回：签名失败:未知错误。返回码:-102  There is no key!        
        caseTitle  = "用例——未插入U盾,不输入任何参数,点击大文件签名测试,期望返回“签名失败:未知错误。返回码:-102  There is no key!”"
        caseResult = None
        e=None
        
        testResult=self.testCtrl.get_FileSign(None,None,None,None,None,None,str_srcPin)
        testResult = re.sub(re.compile('\s+'),' ',testResult) 
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
        #用例描述：未插入U盾，输入合法参数，点击大文件签名测试；期望返回：签名失败:未知错误。返回码:-102  There is no key!        
        caseTitle  = "用例——未插入U盾，输入合法参数,点击大文件签名测试,期望返回“签名失败:未知错误。返回码:-102  There is no key!”"
        caseResult = None
        e=None
        
        CertDn="CN=TestRSA1024,OU=MiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOu,O=rsaperca139.com.cn"
        testResult=self.testCtrl.get_FileSign(CertDn,hashId,xmlInfo,dispInfo,batFilePath,p7FilePath,str_srcPin)
        testResult = re.sub(re.compile('\s+'),' ',testResult) 
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
    
    def negativeCase_manyKey_validParaChoice(self):
        #用例描述：插入多支同款U盾，点击签名，期望返回签名失败:未知错误。返回码:-104 There is more than one key!!
        caseTitle="用例——插入多支同款U盾，点击签名，期望返回签名失败:未知错误。返回码:-104 There is more than one key"
        caseResult = None
        e=None
        
        CertDn="CN=TestSM2.p.0200.0101,OU=MiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOu,O=rsaperca139.com.cn"
        hashId='SM3'
        testResult=self.testCtrl.get_FileSign(CertDn,hashId,xmlInfo,dispInfo,batFilePath,p7FilePath,str_srcPin)
        testResult=re.sub(re.compile('\s+'),' ',testResult)
        if operator.eq(many_key_Err,testResult):
            caseResult="pass"                        
        else:
            caseResult="fail"
            e="实测返回："+"“"+testResult+"”"
            
        if e==None:
            logger.warning("%s || %s ",caseResult,caseTitle)
        else:
            logger.warning("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult
    '''                
    def negativeCase_voidPathParaChoice(self):
        #用例描述：不输入批量文件路径和P7文件路径，其他项正常输入，进行大文件签名；期望返回“签名失败:未知错误。返回码:-320 File error!”        
        caseTitle  = "用例——不输入批量文件路径和P7文件路径，其他项正常输入，进行大文件签名；期望返回“签名失败:未知错误。返回码:-320 File error!"
        caseResult = None
        e=None
        
        certResult=self.CertRequest.genCert_with_RSA1024_Sign_P()
        if certResult[1]: 
            CertDn=certResult[0] 
            testResult=self.testCtrl.get_FileSign(CertDn[0],hashId,xmlInfo,dispInfo,None,None,certResult[2])
            testResult = re.sub(re.compile('\s+'),' ',testResult) 
            if  operator.eq(testResult,file_Err):
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
       
    def negativeCase_voidBatPathChoice(self):
        #用例描述：不输入批量文件路径，其他项正常输入，进行大文件签名；期望返回“签名成功，签名结果返回到P7文件路径文件夹”        
        caseTitle  = "用例——不输入批量文件路径，其他项正常输入，进行大文件签名；期望返回“签名成功，签名结果返回到P7文件路径文件夹"
        caseResult = None
        e=None
        
        certResult=self.CertRequest.genCert_with_RSA1024_Sign_P()
        if certResult[1]:
            CertDn=certResult[0]   
            testResult=self.testCtrl.get_FileSign(CertDn[0],hashId,xmlInfo,dispInfo,None,p7FilePath,certResult[2])
            testResult = re.sub(re.compile('\s+'),' ',testResult) 
            if  file_sign_info in testResult:
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
    
    def negativeCase_voidFilePathChoice(self):
        #用例描述：不输入P7文件路径，其他项正常输入，进行大文件签名；期望返回“签名失败:未知错误。返回码:-409 Sign failed!”
        caseTitle  = "用例——不输入P7文件路径，其他项正常输入，进行大文件签名；期望返回“签名失败:未知错误。返回码:-320 File error!"
        
        caseResult = None
        e=None
        certResult=self.CertRequest.genCert_with_RSA1024_Sign_P()  
        if certResult[1]:
            CertDn=certResult[0]  
            testResult=self.testCtrl.get_FileSign(CertDn[0],hashId,xmlInfo,dispInfo,batFilePath,None,certResult[2])
            testResult = re.sub(re.compile('\s+'),' ',testResult) 
            if operator.eq(testResult,file_Err):
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
    
    def negativeCase_errBatPathChoice(self):
        #用例描述：输入错误批量文件路径，其他项正常输入，进行大文件签名；期望返回“签名失败:未知错误。返回码:-409 Sign failed!”      
        caseTitle  = "用例——输入错误批量文件路径，其他项正常输入，进行大文件签名；期望返回“签名失败:未知错误。返回码:-409 Sign failed!"
        caseResult = None
        e=None     

        certResult=self.CertRequest.genCert_with_RSA1024_Sign_P()  
        if certResult[1]:
            CertDn=certResult[0]  
            testResult=self.testCtrl.get_FileSign(CertDn[0],hashId,xmlInfo,dispInfo,err_bat_path,p7FilePath,certResult[2])
            testResult = re.sub(re.compile('\s+'),' ',testResult) 
            if operator.eq(testResult,unmatched_hash_Err):
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
       
    def negativeCase_errFilePathChoice(self):
        #用例描述：输入错误P7文件路径，其他项正常输入，进行大文件签名；期望返回“签名失败:未知错误。返回码:-409 Sign failed!”        
        caseTitle  = "用例——不输入P7文件路径，其他项正常输入，进行大文件签名；期望返回“签名失败:未知错误。返回码:-409  Sign failed!"
        caseResult = None
        e=None

        certResult=self.CertRequest.genCert_with_RSA1024_Sign_P()  
        if certResult[1]:
            CertDn=certResult[0]  
            testResult=self.testCtrl.get_FileSign(CertDn[0],hashId,xmlInfo,dispInfo,batFilePath,err_file_path,certResult[2])
            testResult = re.sub(re.compile('\s+'),' ',testResult) 
            if operator.eq(testResult,unmatched_hash_Err):
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
    
    def positveCase_errFileNameChoice(self):
        #用例描述：输入错误P7文件路径，其他项正常输入，进行大文件签名；期望返回“签名成功;签名结果文件名称为54654343134654，位置在桌面”        
        caseTitle  = "用例——不输入P7文件路径，其他项正常输入，进行大文件签名；期望返回“签名成功;签名结果文件名称为54654343134654，位置在桌面"
        caseResult = None
        e=None
        
        temp_file_path = "54654343134654"
        certResult=self.CertRequest.genCert_with_RSA1024_Sign_P()  
        if certResult[1]:
            CertDn=certResult[0] 
            testResult=self.testCtrl.get_FileSign(CertDn[0],hashId,xmlInfo,dispInfo,batFilePath,temp_file_path,certResult[2])
            testResult = re.sub(re.compile('\s+'),' ',testResult) 
            if file_sign_info in testResult:
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
    '''

 #########################
#开始测试
#########################