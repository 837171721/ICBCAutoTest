
#coding=utf-8
'''
Created on 2018.03.27 @author:  lzy
Created on 2018.08.09 @author: YS
'''
import re
import operator
import GenCertGroup 
from GlobalConfigure import levels, log_level,str_srcPin,CertListInfoMap

from logTest import SysClass, LoggerClass
conf  = LoggerClass(loglevel=levels.get(log_level), logger="TestCases_GetEnPkOfOriginalProKey.py")
logger=conf.getlogger()

#错误信息列表
format_key_Err='加密公钥：'
no_key_Err='''取旧保护密钥下的加密公钥失败:未知错误。返回码:-102 There is no key!'''
many_key_Err='''取旧保护密钥下的加密公钥失败:未知错误。返回码:-104 There is more than one key!'''
ver_Err = '''取旧保护密钥下的加密公钥失败:未知错误。返回码:-411 ukey version error!'''

def test_GetEncPkeyOfOldAdminKey(ctrlObj,TestingRange,AdminKeyInfo):
    #调用流程    
    testCtrl=GetEncPkeyOfOldAdminKeyCases(ctrlObj,AdminKeyInfo)  #建立类对象，打开控件测试页
    if '00' != AdminKeyInfo[1]:
        casePubKeyCResult=testCtrl.testCtrl.get_PubKeyC()
        casePubKeyCResult=re.sub(re.compile('\s+'), ' ', casePubKeyCResult)
        if operator.eq(casePubKeyCResult,ver_Err):
            logger.warning("接口不支持，请选择旧体系盾或非国密盾进行!")
            return
    testGetEncPkeyOfOldAdminKeyGroup(testCtrl,TestingRange)   #测试用例集，根据测试范围定义测试强度

def testGetEncPkeyOfOldAdminKeyGroup(ctrlElemObj,testRange):
    #测试用例集
    if 0 == testRange:  #详细测试              
        testResult=ctrlElemObj.positiveCase_oneCert() #插入1支只有1张证书的U盾，点击原加密公钥
        
        testResult=ctrlElemObj.positiveCase_manyCert() #插入1支有多张证书的U盾，点击原加密公钥
       
        testResult=ctrlElemObj.positiveCase_tempKeyPair() #插入1支只有1对临时密钥对的U盾，点击原加密公钥
         
        testResult=ctrlElemObj.positiveCase_oneCertAndtempKeyPair() #插入1支只有1对临时密钥对的U盾，点击原加密公钥

        testResult=ctrlElemObj.negativeCase_formatKey() #插入1支格式化的U盾，点击原加密公钥
               
        #testResult=ctrlElemObj.negativeCase_noKey()  #未插入U盾，点击原加密公钥
        
        #testResult=ctrlElemObj.negativeCase_operation() #操作
                                          
    elif 1 == testRange: #验证测试
        testResult=ctrlElemObj.positiveCase()
       
    elif 2 == testRange:
        testResult = ctrlElemObj.negativeCase_noKey()
   
    elif 3 == testRange:
        testResult = ctrlElemObj.negativeCase_manyKey()
        
    elif 4 == testRange:
        testResult=ctrlElemObj.negativeCase_formatKey()
        
        testResult=ctrlElemObj.positiveCase()
        
       
class GetEncPkeyOfOldAdminKeyCases():
    def __init__(self,testCtrl,AdminKeyInfo):
        self.testCtrl=testCtrl   #控件测试页
        self.AdminKeyAlgId=AdminKeyInfo  #保护密钥信息
        self.CertRequest=GenCertGroup.GenCertClass(self.testCtrl,AdminKeyInfo)   #创建证书申请对象
    
    def positiveCase(self):
        #用例描述：插入1支U盾，点击获取原保护密钥的加密公钥，期望返回U盾原保护密钥的加密公钥
        caseTitle="用例——插入1支U盾，点击获取原保护密钥的加密公钥，期望返回U盾原保护密钥的加密公钥"
        caseResult = None
        e = None        
        certResult=self.CertRequest.genCert_with_RSA2048_Mix()
        if certResult[1]:            
            casePubKeyCResult=self.testCtrl.get_PubKeyC()
            casePubKeyCResult=re.sub(re.compile('\s+'), ' ', casePubKeyCResult)
            if (format_key_Err in casePubKeyCResult) and len(casePubKeyCResult)>5 :
                # #logger.warning("响应密文公钥为:%s",casePubKeyCResult)
                caseResult="pass"
            else:
                caseResult="false"
                e = "实测返回：" + "“" + casePubKeyCResult + "”"
        else:
            caseResult="false"
            e = "证书下载失败，结束用例执行！"
           
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult
        
    def negativeCase_formatKey(self):
        #用例描述：插入1支格式化的U盾，点击原加密公钥     期望返回：  返回“加密公钥：”后面为空；
        caseTitle="用例——插入1支格式化的U盾，点击原加密公钥，期望返回 :“加密公钥：”后面为空；"
        caseResult = None
        e = None
        initResult=self.CertRequest.init_key(str_srcPin,str_srcPin)
        if initResult[0]:        
            casePubKeyCResult=self.testCtrl.get_PubKeyC()
            casePubKeyCResult=re.sub(re.compile('\s+'), ' ', casePubKeyCResult)
            if operator.eq(format_key_Err,casePubKeyCResult):
                #logger.warning("响应密文公钥为:%s",casePubKeyCResult)
                caseResult="pass"
            else:
                caseResult="false"
                e = "实测返回：" + "“" + casePubKeyCResult + "”"
        else:
            caseResult="false"
            e = "初始化操作失败，结束用例执行！"            
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult
     
    def positiveCase_oneCert(self):    
        #用例描述：插入1支只有1张证书的U盾，点击原加密公钥     期望返回：返回1个公钥数据；    
        caseTitle="用例——插入只有1张证书的U盾 ，点击原加密公钥,期望返回 :返回1个公钥数据；"
        caseResult = None
        e = None
             
        certResult=self.CertRequest.genCert_with_RSA1024_Mix()
        if certResult[1]:         
            casePubKeyCResult=self.testCtrl.get_PubKeyC() 
            casePubKeyCResult=re.sub(re.compile('\s+'), ' ', casePubKeyCResult)
            if False == casePubKeyCResult.count("||") \
            and (format_key_Err in casePubKeyCResult) and len(casePubKeyCResult)>5:            
                #logger.warning("响应密文公钥为:%s",casePubKeyCResult)
                caseResult="pass"
            else:
                caseResult="false"
                e = "实测返回：" + "“" + casePubKeyCResult + "”"
        else:
            caseResult="false"
            e = "证书下载失败，结束用例执行！"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult
         
    def positiveCase_manyCert(self):    
        #用例描述：插入1支有多张证书的U盾，点击原加密公钥     期望返回：返回多个公钥信息，多个公钥之间以||间隔；      
        caseTitle="用例——插入1支有多张证书的U盾 ，获取原加密公钥，期望返回 多个公钥信息，多个公钥之间以||间隔；"
        caseResult = None
        e = None                
        
        certResult = self.CertRequest.genCert_with_rsa1024M_and_rsa2048M()
        if certResult[1]:  
            casePubKeyCResult=self.testCtrl.get_PubKeyC()
            casePubKeyCResult=re.sub(re.compile('\s+'), ' ', casePubKeyCResult) 
            if casePubKeyCResult.count("||") \
            and (format_key_Err in casePubKeyCResult) and len(casePubKeyCResult)>5:            
                #logger.warning("响应密文公钥为:%s",casePubKeyCResult)
                caseResult="pass"
            else:
                caseResult="false"
                e = "实测返回：" + "“" + casePubKeyCResult + "”"
        else:
            caseResult="false"
            e = "证书下载失败，结束用例执行！"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult
            
    def positiveCase_tempKeyPair(self):
        #用例——插入1支只有1对临时密钥对的U盾，点击原加密公钥   
        caseTitle="用例——插入1支只有1对临时密钥对的U盾，点击原加密公钥"
        caseResult = None
        e = None          
        
        keyPairResult=self.CertRequest.genKeyPair(CertListInfoMap["RSA2048_Mixed"], str_srcPin,True)          
        if keyPairResult[1]:
            casePubKeyCResult=self.testCtrl.get_PubKeyC() 
            casePubKeyCResult=re.sub(re.compile('\s+'), ' ', casePubKeyCResult)             
            if False == casePubKeyCResult.count("||") \
            and (format_key_Err in casePubKeyCResult) and len(casePubKeyCResult)>5: 
                #logger.warning("响应密文公钥为:%s",casePubKeyCResult)
                caseResult="pass"
            else:
                caseResult="false"
                e = "实测返回：" + "“" + casePubKeyCResult + "”"
        else:
            caseResult="false"
            e = "生成临时密钥对失败，结束用例执行！"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult
 
    def positiveCase_oneCertAndtempKeyPair(self):    
        #用例——插入1支既有证书，又有临时密钥对的U盾，点击原加密公钥,返回2个公钥数据，多个公钥之间以||间隔；
        caseTitle="用例——插入1支既有证书，又有临时密钥对的U盾，点击原加密公钥"
        caseResult = None
        e = None        
       
        certResult = self.CertRequest.genCert_with_RSA1024_Mix()
        keypairResult=self.CertRequest.genKeyPair(CertListInfoMap["RSA2048_Mixed"], certResult[2])          
        if certResult[1] and keypairResult[1]:
            casePubKeyCResult=self.testCtrl.get_PubKeyC() 
            casePubKeyCResult=re.sub(re.compile('\s+'), ' ', casePubKeyCResult)              
            if casePubKeyCResult.count("||") \
            and (format_key_Err in casePubKeyCResult) and len(casePubKeyCResult)>5:
                #logger.warning("响应密文公钥为:%s",casePubKeyCResult)
                caseResult="pass"
            else:
                caseResult="false"
                e = "实测返回：" + "“" + casePubKeyCResult + "”"
        else:
            caseResult="false"
            e = "生成临时密钥对或下载证书失败，结束用例执行！"
                       
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult            
    
    def negativeCase_noKey(self):
        #用例描述：未插入U盾，点击获取保护密钥的加密公钥，期望返回获取获取旧保护密钥下的加密公钥失败:未知错误。返回码:-102 There is no key!          
        caseTitle="用例——未插入U盾，点击获取保护密钥的加密公钥，期望返回获取旧保护密钥下的加密公钥失败:未知错误。返回码:-102 There is no key!"
        caseResult = None
        e = None   
              
        casePubKeyCResult=self.testCtrl.get_PubKeyC() 
        casePubKeyCResult=re.sub(re.compile('\s+'), ' ', casePubKeyCResult)
        if operator.eq(no_key_Err,casePubKeyCResult):
            #logger.warning("响应密文公钥为:%s",casePubKeyCResult)
            caseResult="pass"
        else:
            caseResult="false"
            e = "实测返回：" + "“" + casePubKeyCResult + "”"
            
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult
            
    def negativeCase_manyKey(self):
        #用例描述：插入多支同款U盾，点击原加密公钥  期望返回：“取旧保护密钥下的加密公钥失败:未知错误。返回码:-104 There is more than one key!”错误提示；
        caseTitle="用例——插入多支同款U盾，点击原加密公钥  期望返回：“取旧保护密钥下的加密公钥失败:未知错误。返回码:-104 There is more than one key!" 
        caseResult=None
        e=None
              
        casePubKeyCResult=self.testCtrl.get_PubKeyC()
        casePubKeyCResult=re.sub(re.compile('\s+'), ' ', casePubKeyCResult)
        if operator.eq(many_key_Err,casePubKeyCResult):
            #logger.warning("响应密文公钥为:%s",casePubKeyCResult)
            caseResult="pass"
        else:
            caseResult="false"
            e = "实测返回：" + "“" + casePubKeyCResult + "”"
            
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult
            
    def negativeCase_operation(self):
        #用例描述：插入多支同款U盾，拔出多余U盾，只留1支在位，点击原加密公钥,期望返回公钥数据
        caseTitle="用例——插入多支同款U盾，拔出多余U盾，只留1支在位，点击原保护密钥的加密公钥,期望返回公钥数据"
        caseResult=None
        e=None
       
        casePubKeyCResult=self.testCtrl.get_PubKeyC()
        if (format_key_Err in casePubKeyCResult) and len(casePubKeyCResult)>=5: 
            #logger.warning("响应密文公钥为:%s",casePubKeyCResult)
            caseResult="pass"
        else:
            caseResult="false"
            e = "实测返回：" + "“" + casePubKeyCResult + "”"
            
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult
    
#########################
#开始测试
#########################

 
    
    
    
    