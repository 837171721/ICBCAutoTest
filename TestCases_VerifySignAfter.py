#coding=utf-8
'''
Created on 2018.07.23 @author: FJQ
Created on 2018.08.15 @author: SYX
Created on 2018.08.18 @author: YS
'''

import re         #引入正在表达式
import operator
import GenCertGroup
from GlobalConfigure import levels,log_level,hashId,xmlInfo,dispInfo,str_srcPin
from GlobalConfigure import  CertListInfoMap,testUrl_GM_User

from logTest import SysClass, LoggerClass
conf  = LoggerClass(loglevel=levels.get(log_level), logger="TestCases_verifysign.py")
logger=conf.getlogger()

#错误信息列表
verifysign_Err='''事后验签失败:未知错误。返回码:-410 verifysign failed!'''
nothing_Err=  ""
right_info='''事后验签成功'''

def test_VerifySignAfter(ctrlObj,TestingRange,AdminKeyInfo):
    testCtrl=VerifySignAfterCases(ctrlObj,AdminKeyInfo)  #建立类对象，打开控件测试页 
    testVerifySignAfterCase(testCtrl,TestingRange)   #测试用例集，根据测试范围定义测试强度
    
def testVerifySignAfterCase(VerifySignCtrl,testRange):
    #测试用例集
    if 0 == testRange:  #详细测试
        testResult = VerifySignCtrl.positiveCase()

        testResult = VerifySignCtrl.positiveCase_supportedCertTest()  # 5、覆盖测试签名

        #testResult = VerifySignCtrl.positiveCase_coverageTest()#5、覆盖测试签名

    elif 1 == testRange: #验证测试
        testResult = VerifySignCtrl.positiveCase()
        
    elif 2 == testRange: #无key测试
        testResult = VerifySignCtrl.negativeCase_noKey_voidParaChoice()
        
        testResult = VerifySignCtrl.negativeCase_noKey_errParaChoice()

        testResult = VerifySignCtrl.negativeCase_noKey_getXmlMagAndDispMsgDirectly()
        
    elif 3 == testRange: #多key测试
        testResult = VerifySignCtrl.negativeCase_manyKey()     
        
    elif 4 == testRange: #U盾在位
        testResult = VerifySignCtrl.positiveCase()
        
    else:
        a = 0

class VerifySignAfterCases():
    def __init__(self,testCtrl,AdminKeyInfo):
        self.testCtrl=testCtrl   #控件测试页
        self.AdminKeyAlgId = AdminKeyInfo  # 保护密钥信息
        self.CertRequest=GenCertGroup.GenCertClass(self.testCtrl,AdminKeyInfo)   #创建证书申请对象

    def positiveCase(self):
        # 用例描述：插入1支有证书的U盾，进行一次事后验签、获取XML信息、获取屏显信息
        caseTitle  = "用例——插入1支有证书的U盾，进行一次事后验签、获取XML信息、获取屏显信息，应都能获取成功"
        caseResult = None
        e=None

        cur_url=self.testCtrl.browser.current_url
        logger.critical("beginning... || %s ",caseTitle)
        #打开用户控件页
        if operator.eq(-1, cur_url.find(testUrl_GM_User)):
            self.testCtrl.browser.get(testUrl_GM_User)
        certResult=self.CertRequest.genCert_with_RSA1024_Mix()
        if certResult[1]:
            p7SignedData=self.testCtrl.get_DispSign(certResult[0][0],hashId,xmlInfo,dispInfo,certResult[2])
            #打开管理员控件页
            if len(p7SignedData)>100:
                self.testCtrl.browser.get(cur_url) #切回原页面

                testResult=self.testCtrl.verifySignAfter(p7SignedData)
                testResult = re.sub(re.compile('\s+'), ' ', testResult)
                if operator.eq(right_info,testResult):
                    caseResult = "pass"
                    logger.critical("%s || %s ", caseResult,testResult )
                    testResult_XmlMsg = self.testCtrl.get_XmlMsg()
                    if operator.eq(testResult_XmlMsg, xmlInfo):
                        logger.critical("%s || 验签成功，获取XML数据成功！", caseResult)
                    else:
                        caseResult = "fail"
                        logger.critical("%s || 验签成功，获取XML数据失败！", caseResult)

                    testResult_KeyDispMsg = self.testCtrl.get_KeyDispMsg()
                    testResult_KeyDispMsg = re.sub(re.compile('\s+'), ' ', testResult_KeyDispMsg)
                    tempdispInfo = re.sub(re.compile('\s+'), ' ', dispInfo)
                    if operator.eq(testResult_KeyDispMsg, tempdispInfo):
                        logger.critical("%s || 验签成功，获取屏显信息成功！", caseResult)
                    else:
                        caseResult = "fail"
                        logger.critical("%s || 验签成功，获取屏显信息失败！", caseResult)
                else:
                    caseResult = "fail"
                    logger.critical("%s || %s ", caseResult,testResult )
            else:
                caseResult = "fail"
                e = "签名失败,结束用例执行"
                logger.critical("%s || %s ", caseResult, e)
        else:
            caseResult="fail"
            e="下证失败,结束用例执行"
            logger.critical("%s || %s ", caseResult, e)
        logger.critical("end. || %s ",caseTitle)
        
        return caseResult
    
    def negativeCase_noKey_errParaChoice(self):
        # 用例描述：未插入U盾，签名数据栏任意输入字符，点击事后验签，返回“事后验签失败:未知错误。返回码:-410 verifysign failed!”
        caseTitle  = "用例——未插入U盾，签名数据栏任意输入字符，点击事后验签，返回“事后验签失败:未知错误。返回码:-410 verifysign failed!”"  
        caseResult = None
        e=None
        testResult=self.testCtrl.verifySignAfter('1111122223333','')  
        testResult=re.sub(re.compile('\s+'),' ',testResult)      
        if operator.eq(verifysign_Err, testResult):
            caseResult="pass"
        else:
            caseResult="fail"
            e="实测返回："+"“"+testResult+"”"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult
    
    def negativeCase_noKey_voidParaChoice(self):
        # 用例描述：未插入U盾，签名数据栏不输入字符，点击事后验签，返回“事后验签失败:未知错误。返回码:-410 verifysign failed!”
        caseTitle  = "用例——未插入U盾，签名数据栏不输入字符，点击事后验签，返回“事后验签失败:未知错误。返回码:-410 verifysign failed!”"
        caseResult = None
        e=None

        testResult=self.testCtrl.verifySignAfter(None,None)
        testResult=re.sub(re.compile('\s+'),' ',testResult)
        if operator.eq(verifysign_Err, testResult):
            caseResult="pass"
        else:
            caseResult="fail"
            e="实测返回："+"“"+testResult+"”"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult

    def negativeCase_noKey_getXmlMagAndDispMsgDirectly(self):
        # 用例描述：未插入U盾，未执行过事后验签，点击获取XML信息、获取屏显信息，结果栏中为空
        caseTitle  = "用例——未插入U盾，未执行过事后验签，点击获取XML信息、获取屏显信息，结果栏中为空"  
        caseResult = None
        e=None
        logger.critical("beginning... || %s ",caseTitle)

        testResult_XmlMsg=self.testCtrl.get_XmlMsg()
        if operator.eq(testResult_XmlMsg, nothing_Err):
            caseResult = "pass"
            logger.critical("%s || 未进行验签，获取XML数据为空！ || %s", caseResult,testResult_XmlMsg)
        else:
            caseResult = "fail"
            logger.critical("%s || 未进行验签，获取XML数据失败！ || %s", caseResult,testResult_XmlMsg)

        testResult_KeyDispMsg = self.testCtrl.get_KeyDispMsg()
        if operator.eq(testResult_KeyDispMsg, nothing_Err):
            caseResult = "pass"
            logger.critical("%s || 未进行验签，获取屏显信息为空！ || %s", caseResult,testResult_KeyDispMsg)
        else:
            caseResult = "fail"
            logger.critical("%s || 未进行验签，获取屏显信息失败！ || %s", caseResult,testResult_KeyDispMsg)

        logger.critical("end. || %s ",caseTitle)
        return caseResult

    def positiveCase_supportedCertTest(self):
        caseTitle  = "用例——对二代签名结果进行验签，覆盖支持的所有证书及哈希方式"  
        caseResult = None
        
        certType=[]
        logger.critical("beginning... || %s ",caseTitle)
        fp=open('signResult.txt','r',encoding='utf-8')
        if fp:
            tempSignResult=fp.readline() 
            if tempSignResult:
                testResult=self.testCtrl.verifySignAfter(tempSignResult,'')
                testResult=re.sub(re.compile('\s+'),' ',testResult)
                if right_info in testResult:
                    caseResult="pass"
                    logger.critical("%s || %s ",caseResult,certType)
                    testResult_XmlMsg=self.testCtrl.get_XmlMsg()
                    if operator.eq(testResult_XmlMsg,xmlInfo):
                        logger.critical(" %s || 验签成功，获取XML数据成功！",caseResult)
                    else:
                        caseResult="fail"
                        logger.critical(" %s || 验签成功，获取XML数据失败！",caseResult)
                        
                    testResult_KeyDispMsg=self.testCtrl.get_KeyDispMsg()
                    if operator.eq(testResult_KeyDispMsg,dispInfo):
                        logger.critical(" %s || 验签成功，获取屏显信息成功！",caseResult)
                    else:
                        caseResult="fail"
                        logger.critical(" %s || 验签成功，获取屏显信息失败！",caseResult)
                else:
                    caseResult="fail"
                    logger.critical("事后验签失败 || %s ",certType)
                    
        logger.critical("end. || %s ",caseTitle)
        fp.truncate()                   #清空文件内容       
        fp.close()
        #os.remove('signResult.txt')    #删除文件
        return caseResult 
   
    def positiveCase_converageTest(self):
        caseTitle  = "用例——对二代签名结果进行验签，覆盖支持的所有证书及哈希方式"  
        caseResult = None
        e=None
                
        #RSA1024-专用-SHA1
        #打开用户控件页
        self.testCtrl.browser.get(testUrl_GM_User)   
        CertDn=self.CertRequest.genCert_with_RSA1024_Sign_P()  
        p7SignedData=self.testCtrl.get_DispSign(CertDn[0][0],hashId,xmlInfo,dispInfo,CertDn[2])
        #打开管理员控件页
        cur_url = self.testCtrl.browser.current_url
        self.testCtrl.browser.get(cur_url)
        if None != p7SignedData: 
            testResult=self.testCtrl.verifySignAfter(p7SignedData,'')
            testResult_XmlMsg=self.testCtrl.get_XmlMsg()
            testResult_KeyDispMsg=self.testCtrl.get_KeyDispMsg()
            
            testResult=re.sub(re.compile('\s+'),' ',testResult)
            testResult_XmlMsg=re.sub(re.compile('\s+'),' ',testResult_XmlMsg)
            testResult_KeyDispMsg=re.sub(re.compile('\s+'),' ',testResult_KeyDispMsg) 
            tempdispInfo=re.sub(re.compile('\s+'),' ',dispInfo)           
            if operator.eq(right_info,testResult) and operator.eq(xmlInfo,testResult_XmlMsg) and operator.eq(tempdispInfo,testResult_KeyDispMsg):
                caseResult="pass"
            else:
                caseResult="fail"
                e="实测返回："+"“"+testResult+"”"
        else:
            caseResult="fail"
            e="签名失败"     

        #RSA1024-混用-SHA1
        #打开用户控件页
        self.testCtrl.browser.get(testUrl_GM_User) 
        CertDn=self.CertRequest.genCert_with_RSA1024_Mix()  
        p7SignedData=self.testCtrl.get_DispSign(CertDn[0][0],hashId,xmlInfo,dispInfo,CertDn[2])
        #打开管理员控件页
        self.testCtrl.browser.get(cur_url)
        if None != p7SignedData: 
            testResult=self.testCtrl.verifySignAfter(p7SignedData,'')
            testResult_XmlMsg=self.testCtrl.get_XmlMsg()
            testResult_KeyDispMsg=self.testCtrl.get_KeyDispMsg()
            
            testResult=re.sub(re.compile('\s+'),' ',testResult)
            testResult_XmlMsg=re.sub(re.compile('\s+'),' ',testResult_XmlMsg)
            testResult_KeyDispMsg=re.sub(re.compile('\s+'),' ',testResult_KeyDispMsg) 
            tempdispInfo=re.sub(re.compile('\s+'),' ',dispInfo)           
            if operator.eq(right_info,testResult) and operator.eq(xmlInfo,testResult_XmlMsg) and operator.eq(tempdispInfo,testResult_KeyDispMsg):
                caseResult="pass"
            else:
                caseResult="fail"
                e="实测返回："+"“"+testResult+"”"
        else:
            caseResult="fail"
            e="签名失败"     
        
        #RSA1024-混用-SHA256
        #打开用户控件页
        self.testCtrl.browser.get(testUrl_GM_User) 
        CertDn=self.CertRequest.genCert_With_Verify(CertListInfoMap["RSA1024_Mixed_sha256"],str_srcPin)  
        p7SignedData=self.testCtrl.get_DispSign(CertDn[0][0],'SHA256',xmlInfo,dispInfo,CertDn[2])
        #打开管理员控件页
        self.testCtrl.browser.get(cur_url)
        if None != p7SignedData: 
            testResult=self.testCtrl.verifySignAfter(p7SignedData,'')
            testResult_XmlMsg=self.testCtrl.get_XmlMsg()
            testResult_KeyDispMsg=self.testCtrl.get_KeyDispMsg()
            
            testResult=re.sub(re.compile('\s+'),' ',testResult)
            testResult_XmlMsg=re.sub(re.compile('\s+'),' ',testResult_XmlMsg)
            testResult_KeyDispMsg=re.sub(re.compile('\s+'),' ',testResult_KeyDispMsg) 
            tempdispInfo=re.sub(re.compile('\s+'),' ',dispInfo)           
            if operator.eq(right_info,testResult) and operator.eq(xmlInfo,testResult_XmlMsg) and operator.eq(tempdispInfo,testResult_KeyDispMsg):
                caseResult="pass"
            else:
                caseResult="fail"
                e="实测返回："+"“"+testResult+"”"
        else:
            caseResult="fail"
            e="签名失败"     
        
        #RSA2048-专用-SHA1
        #打开用户控件页
        self.testCtrl.browser.get(testUrl_GM_User) 
        CertDn=self.CertRequest.genCert_with_RSA2048_Sign_P()  
        testResult=self.testCtrl.get_DispSign(CertDn[0][0],'SHA512',xmlInfo,dispInfo,CertDn[2])
        #打开管理员控件页
        self.testCtrl.browser.get(cur_url)
        if None != p7SignedData: 
            testResult=self.testCtrl.verifySignAfter(p7SignedData,'')
            testResult_XmlMsg=self.testCtrl.get_XmlMsg()
            testResult_KeyDispMsg=self.testCtrl.get_KeyDispMsg()
            
            testResult=re.sub(re.compile('\s+'),' ',testResult)
            testResult_XmlMsg=re.sub(re.compile('\s+'),' ',testResult_XmlMsg)
            testResult_KeyDispMsg=re.sub(re.compile('\s+'),' ',testResult_KeyDispMsg) 
            tempdispInfo=re.sub(re.compile('\s+'),' ',dispInfo)           
            if operator.eq(right_info,testResult) and operator.eq(xmlInfo,testResult_XmlMsg) and operator.eq(tempdispInfo,testResult_KeyDispMsg):
                caseResult="pass"
            else:
                caseResult="fail"
                e="实测返回："+"“"+testResult+"”"
        else:
            caseResult="fail"
            e="签名失败"     
        
        #打开用户控件页
        self.testCtrl.browser.get(testUrl_GM_User)
        #RSA2048-专用-SHA384
        CertDn=self.CertRequest.genCert_With_Verify(CertListInfoMap["RSA2048_Sig2_p_sha384"],str_srcPin)  
        testResult=self.testCtrl.get_DispSign(CertDn[0][0],'SHA384',xmlInfo,dispInfo,CertDn[2])
        #打开管理员控件页
        self.testCtrl.browser.get(cur_url)
        if None != p7SignedData: 
            testResult=self.testCtrl.verifySignAfter(p7SignedData,'')
            testResult_XmlMsg=self.testCtrl.get_XmlMsg()
            testResult_KeyDispMsg=self.testCtrl.get_KeyDispMsg()
            
            testResult=re.sub(re.compile('\s+'),' ',testResult)
            testResult_XmlMsg=re.sub(re.compile('\s+'),' ',testResult_XmlMsg)
            testResult_KeyDispMsg=re.sub(re.compile('\s+'),' ',testResult_KeyDispMsg) 
            tempdispInfo=re.sub(re.compile('\s+'),' ',dispInfo)           
            if operator.eq(right_info,testResult) and operator.eq(xmlInfo,testResult_XmlMsg) and operator.eq(tempdispInfo,testResult_KeyDispMsg):
                caseResult="pass"
            else:
                caseResult="fail"
                e="实测返回："+"“"+testResult+"”"
        else:
            caseResult="fail"
            e="签名失败"     
        
        #RSA2048-混用-SHA1
        #打开用户控件页
        self.testCtrl.browser.get(testUrl_GM_User)
        CertDn=self.CertRequest.genCert_with_RSA2048_Mix()  
        p7SignedData=self.testCtrl.get_DispSign(CertDn[0][0],hashId,xmlInfo,dispInfo,CertDn[2])
        #打开管理员控件页
        self.testCtrl.browser.get(cur_url)
        if None != p7SignedData: 
            testResult=self.testCtrl.verifySignAfter(p7SignedData,'')
            testResult_XmlMsg=self.testCtrl.get_XmlMsg()
            testResult_KeyDispMsg=self.testCtrl.get_KeyDispMsg()
            
            testResult=re.sub(re.compile('\s+'),' ',testResult)
            testResult_XmlMsg=re.sub(re.compile('\s+'),' ',testResult_XmlMsg)
            testResult_KeyDispMsg=re.sub(re.compile('\s+'),' ',testResult_KeyDispMsg) 
            tempdispInfo=re.sub(re.compile('\s+'),' ',dispInfo)           
            if operator.eq(right_info,testResult) and operator.eq(xmlInfo,testResult_XmlMsg) and operator.eq(tempdispInfo,testResult_KeyDispMsg):
                caseResult="pass"
            else:
                caseResult="fail"
                e="实测返回："+"“"+testResult+"”"
        else:
            caseResult="fail"
            e="签名失败"     
              
        #RSA2048-混用-SHA512
        #打开用户控件页
        self.testCtrl.browser.get(testUrl_GM_User)
        CertDn=self.CertRequest.genCert_With_Verify(CertListInfoMap["RSA2048_Mixed_sha512"],str_srcPin)  
        p7SignedData=self.testCtrl.get_DispSign(CertDn[0][0],'SHA512',xmlInfo,dispInfo,CertDn[2])
        #打开管理员控件页
        self.testCtrl.browser.get(cur_url)
        if None != p7SignedData: 
            testResult=self.testCtrl.verifySignAfter(p7SignedData,'')
            testResult_XmlMsg=self.testCtrl.get_XmlMsg()
            testResult_KeyDispMsg=self.testCtrl.get_KeyDispMsg()
            
            testResult=re.sub(re.compile('\s+'),' ',testResult)
            testResult_XmlMsg=re.sub(re.compile('\s+'),' ',testResult_XmlMsg)
            testResult_KeyDispMsg=re.sub(re.compile('\s+'),' ',testResult_KeyDispMsg) 
            tempdispInfo=re.sub(re.compile('\s+'),' ',dispInfo)           
            if operator.eq(right_info,testResult) and operator.eq(xmlInfo,testResult_XmlMsg) and operator.eq(tempdispInfo,testResult_KeyDispMsg):
                caseResult="pass"
            else:
                caseResult="fail"
                e="实测返回："+"“"+testResult+"”"
        else:
            caseResult="fail"
            e="签名失败"     
            
        #SM2-专用-SM3
        #判断为国密盾
        #打开用户控件页
        self.testCtrl.browser.get(testUrl_GM_User)
        testCardNum=self.testCtrl.get_MediaId() 
        if testCardNum[0:2] == "69":
            CertDn=self.CertRequest.genCert_with_SM2_Sign_P()  
            p7SignedData=self.testCtrl.get_DispSign(CertDn[0][0],'SM3',xmlInfo,dispInfo,CertDn[2])
            #打开管理员控件页
            self.testCtrl.browser.get(cur_url)
            if None != p7SignedData: 
                testResult=self.testCtrl.verifySignAfter(p7SignedData,'')
                testResult_XmlMsg=self.testCtrl.get_XmlMsg()
                testResult_KeyDispMsg=self.testCtrl.get_KeyDispMsg()
                
                testResult=re.sub(re.compile('\s+'),' ',testResult)
                testResult_XmlMsg=re.sub(re.compile('\s+'),' ',testResult_XmlMsg)
                testResult_KeyDispMsg=re.sub(re.compile('\s+'),' ',testResult_KeyDispMsg) 
                tempdispInfo=re.sub(re.compile('\s+'),' ',dispInfo)           
                if operator.eq(right_info,testResult) and operator.eq(xmlInfo,testResult_XmlMsg) and operator.eq(tempdispInfo,testResult_KeyDispMsg):
                    caseResult="pass"
                else:
                    caseResult="fail"
                    e="实测返回："+"“"+testResult+"”"
            else:
                caseResult="fail"
                e="签名失败"     
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult

    def negativeCase_manyKey(self):
        # 用例描述：插入多支同款U盾，进行事后验签、获取XML信息、获取屏显信息;1.返回“事后验签失败:未知错误。返回码:-410 verifysign failed!”错误提示；2.获取XML信息和获取屏显信息没内容
        caseTitle  = "用例——插入多支同款U盾，进行事后验签、获取XML信息、获取屏显信息;1.返回“事后验签失败:未知错误。返回码:-410 verifysign failed!”错误提示；2.获取XML信息和获取屏显信息没内容"
        caseResult = None
        e=None
        logger.critical("beginning... || %s ",caseTitle)

        testResult=self.testCtrl.verifySignAfter('111','')
        testResult=re.sub(re.compile('\s+'),' ',testResult)
        if operator.eq(verifysign_Err, testResult):
            caseResult = "pass"
            logger.critical("%s || %s", caseResult, testResult)

            testResult_XmlMsg = self.testCtrl.get_XmlMsg()
            if operator.eq(testResult_XmlMsg, nothing_Err):
                logger.critical("%s || 验签失败，获取XML数据成功！ || %s", caseResult, testResult_XmlMsg)
            else:
                caseResult = "fail"
                logger.critical("%s || 验签失败，获取XML数据失败！ || %s", caseResult, testResult_XmlMsg)

            testResult_KeyDispMsg = self.testCtrl.get_KeyDispMsg()
            if operator.eq(testResult_KeyDispMsg, nothing_Err):
                caseResult = "pass"
                logger.critical("|| %s 验签失败，获取屏显信息成功！ || %s", caseResult,testResult_KeyDispMsg)
            else:
                caseResult = "fail"
                logger.critical("|| %s 验签失败，获取屏显信息失败！ || %s", caseResult,testResult_KeyDispMsg)
        else:
            caseResult = "fail"
            logger.critical("%s || 实测返回：%s", caseResult, testResult)

        logger.critical("end. || %s ",caseTitle)
        return caseResult
'''    
    #用例描述：插入多支同款U盾，拔出多余U盾，只留1支在位，进行事后验签,验签成功
    def positiveCase(self):
        caseTitle  = "用例——插入多支同款U盾，拔出多余U盾，只留1支在位，进行事后验签,验签成功"  
        caseResult = None
        e=None

        CertDn=self.CertRequest.genCert_with_RSA1024_Mix()
        p7SignedData=self.testCtrl.get_DispSign(CertDn[0][0],hashId,xmlInfo,dispInfo,CertDn[2])
        #打开管理员控件页
        self.testCtrl.browser.get(testUrl_GM_Manage)
        
        testResult=self.testCtrl.verifySignAfter(p7SignedData)
        
        testResult=re.sub(re.compile('\s+'),' ',testResult)
        
        if right_info == testResult:
            caseResult="pass"
        else:
            caseResult="fail"
            e="实测返回："+"“"+re.sub(re.compile('\s+'),' ',testResult)+"”"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult
'''