#coding=utf-8
'''
Created on 2018.03.27  @author: FJQ
Created on 2018.07.15  @author: YS
Created on 2018.08.08  @author: SYX
Created on 2018.08.018  @author: YS
'''
import re
import operator
import GenCertGroup
from GlobalConfigure import levels,log_level,str_srcPin,CertListInfoMap,testUrl_GM_User,main_url

from logTest import SysClass, LoggerClass
conf  = LoggerClass(loglevel=levels.get(log_level), logger="TestCases_GetPublicKey.py")
logger=conf.getlogger()

#错误信息列表
no_key_Err='''获取公钥失败:未知错误。返回码:-102 There is no key!'''
many_key_Err='''获取公钥失败:未知错误。返回码:-104 There is more than one key!'''
para_Err='''获取公钥失败:未知错误。返回码:-304 Failed Param!'''

def test_GetPublicKey(ctrlObj,TestingRange,AdminKeyInfo):
    #调用流程
    testCtrl=GetPublicKeyCases(ctrlObj,AdminKeyInfo)  #建立类对象，打开控件测试页
    testGetPublicKeyGroup(testCtrl,TestingRange)   #测试用例集，根据测试范围定义测试强度

def testGetPublicKeyGroup(PublicKeyCtrl,testRange):
    #测试用例集
    if 0 == testRange:  #详细测试
        testResult = PublicKeyCtrl.negativeCase_formatKey_voidParachoice()#插入一只格式化key，未选择类型

        testResult = PublicKeyCtrl.positiveCase_formatKey_validParaChoice()#插入一只格式化key，遍历正确的参数类型

        testResult = PublicKeyCtrl.negativeCase_oneCert_voidParachoice()#插入一只一张证书的key，不选择类型

        testResult = PublicKeyCtrl.positiveCase_oneCert_validParaChoice()#插入一只一张证书的key，遍历正确的参数类型

        testResult = PublicKeyCtrl.negativeCase_manyCert_voidParaChoice()#插入一只多张证书的key，不选择类型

        testResult = PublicKeyCtrl.positiveCase_manyCert_validParaChoice()#插入一只多张证书的key，遍历正确的参数类型

        testResult = PublicKeyCtrl.negativeCase_oneCertAndtempKeyPair_voidParaChoice()#插入一只有1张证书和1对临时密钥对，不选择类型

        testResult = PublicKeyCtrl.positiveCase_oneCertAndtempKeyPair_validParaChoice()#插入一只有1张证书和1对临时密钥对，遍历正确的参数类型

        testResult = PublicKeyCtrl.negativeCase_manyCertAndmanyTempKeyPair_voidParaChoice()#插入一只有2张证书和2对临时密钥对，不选择类型

        testResult = PublicKeyCtrl.positiveCase_manyCertAndmanyTempKeyPair_validParaChoice()#插入一只有2张证书和2对临时密钥对，遍历正确的参数类型

        #testResult = PublicKeyCtrl.negativeCase_nokey_voidParaChoice()#未插key，未选择类型
        #testResult = PublicKeyCtrl.negativeCase_nokey_validParaChoice()#未插key，遍历正确的参数类型
        #testResult = PublicKeyCtrl.negativeCase_manyKey()#插入多只key，选择默认参数类型
        #testResult = PublicKeyCtrl.positiveCase_operation()#插入多只，拔出多余key，留一只，遍历正确的参数类型
              
    elif 1 == testRange: #验证测试
        testResult = PublicKeyCtrl.positiveCase()
                
    elif 2 == testRange: #无key测试
        testResult = PublicKeyCtrl.negativeCase_nokey_voidParaChoice()#未插key，未选择类型

        testResult = PublicKeyCtrl.negativeCase_nokey_validParaChoice()#未插key，遍历正确的参数类型
        
    elif 3 == testRange: #多key测试
        testResult = PublicKeyCtrl.negativeCase_manyKey()#插入多只key，选择默认参数类型
        
    elif 4 == testRange: #多key测试
        testResult = PublicKeyCtrl.positiveCase()

class GetPublicKeyCases():
    def __init__(self,testCtrl,AdminKeyInfo):
        self.testCtrl=testCtrl   #控件测试页
        self.AdminKeyAlgId=AdminKeyInfo  #保护密钥信息
        self.CertRequest=GenCertGroup.GenCertClass(self.testCtrl,AdminKeyInfo)   #创建证书申请对象
        
    def positiveCase(self):
        #用例描述："插入一只有1张证书的U盾，选择获取类型所有公钥、证书中的公钥、非证书中的公钥，点击获取公钥明文，期望返回正确公钥值"
        caseTitle="用例——插入有1张证书的U盾，遍历不同的参数类型，点击获取公钥明文，期望返回正确公钥值"
        caseResult = None
        e = None

        #certResult=['',True,'1q1q1q1q']
        ParaLists = ['AllPubKey', 'CertPubKey', 'NoCertPubKey']            
        logger.critical("beginning... || %s ", caseTitle)
        
        certResult = self.CertRequest.genCert_with_RSA1024_Mix()
        if certResult[1]:
            for testReadType in ParaLists:
                pubKeyResult = self.testCtrl.get_PubKey(testReadType)
                pubKeyResult = re.sub(re.compile('\s+'), ' ', pubKeyResult)
                if pubKeyResult.count("公钥："):
                    if operator.eq(testUrl_GM_User,main_url):
                        if (len(pubKeyResult)>3 and (operator.eq(testReadType, ParaLists[0]) or operator.eq(testReadType, ParaLists[1])))\
                         or (len(pubKeyResult)== 3 and operator.eq(testReadType, ParaLists[2])):
                            caseResult = "pass"
                            logger.critical("%s || %s", caseResult, testReadType    )
                        else:
                            caseResult = "fail"
                            logger.critical("%s || %s || %s ", caseResult, testReadType, pubKeyResult)                    
                    else:
                        if len(pubKeyResult)>3:    
                            caseResult = "pass"
                            logger.critical("%s || %s", caseResult, testReadType    )
                        else:
                            caseResult = "fail"
                            logger.critical("%s || %s || %s ", caseResult, testReadType, pubKeyResult)
                else:
                    caseResult = "fail"
                    logger.critical("%s || %s || %s ", caseResult, testReadType, pubKeyResult)
        else:
            caseResult = "fail"
            e = "证书下载失败，结束用例执行"
            logger.critical("%s || %s ", caseResult, e)

        logger.critical("end. || %s ",caseTitle)
        return caseResult

    def negativeCase_nokey_voidParaChoice(self):
        # 用例描述：未插入U盾，不选择获取类型，点击获取公钥明文，期望返回获取公钥失败:未知错误。返回码:-304Failed Param!
        caseTitle="用例——未插入U盾，不选择获取类型，点击获取公钥明文，期望返回获取公钥失败:未知错误。返回码:-304 Failed Param! 或-102 There is no Key!(非国密控件页返回码)"
        caseResult = None
        e = None
        ReadType=''

        pubKeyResult=self.testCtrl.get_PubKey(ReadType)
        pubKeyResult=re.sub(re.compile('\s+'),' ',pubKeyResult)
        if operator.eq(para_Err, pubKeyResult) or operator.eq(no_key_Err, pubKeyResult) :
            caseResult = "pass"
        else:
            caseResult = "fail"
            e = "实测返回：" + "“" + pubKeyResult+ "”"

        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult
        
    def negativeCase_nokey_validParaChoice(self):
        # 用例描述：未插入U盾，获取类型分别选择：所有公钥、证书中的公钥、非证书中的公钥，点击获取公钥明文，期望返回获取公钥失败:未知错误。返回码:-304Failed Param!
        caseTitle="用例——未插入U盾，遍历不同的参数类型，点击获取公钥明文，期望返回获取公钥失败:未知错误。返回码:-304Failed Param!"
        caseResult = None
        e = None
        ParaLists = ['AllPubKey', 'CertPubKey', 'NoCertPubKey']
        
        logger.critical("beginning... || %s ", caseTitle)
        for testReadType in ParaLists:
            pubKeyResult = self.testCtrl.get_PubKey(testReadType)
            #logger.warning(testReadType+"||"+pubKeyResult)
            pubKeyResult = re.sub(re.compile('\s+'), ' ', pubKeyResult)
            if operator.eq(no_key_Err, pubKeyResult):
                caseResult = "pass"
                logger.critical("%s || %s ", caseResult, testReadType)
            else:
                caseResult = "fail"
                logger.critical("%s || %s || %s ", caseResult, testReadType, pubKeyResult)

        logger.critical("end. || %s ",caseTitle)
        return caseResult
                
    def negativeCase_formatKey_voidParachoice(self):
        # 用例描述：插入一只无证U盾，不选择获取类型，点击获取公钥明文，期望返回获取公钥失败:未知错误。返回码:-304 Failed Param!
        caseTitle="用例——插入一只无证U盾，不选择获取类型，点击获取公钥明文，期望返回获取公钥失败:未知错误。返回码:-304 Failed Param!"
        caseResult = None
        e = None
        initResult=self.CertRequest.init_key(str_srcPin,str_srcPin)
        if initResult[0]:
            ReadType=''
            pubKeyResult=self.testCtrl.get_PubKey(ReadType)
            pubKeyResult=re.sub(re.compile('\s+'),' ',pubKeyResult)
            if operator.eq(para_Err, pubKeyResult):
                caseResult = "pass"
            else:
                caseResult = "fail"
                e = "实测返回：" + "“" + pubKeyResult+ "”"
        else:
            caseResult = "fail"
            e = "初始化失败,结束用例执行"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult
    
    def positiveCase_formatKey_validParaChoice(self):
        # 用例描述：插入一只无证U盾，获取类型分别选择：所有公钥、证书中的公钥、非证书中的公钥，点击获取公钥明文，期望返回'公钥：'
        caseTitle="用例——未插入U盾，选择正确的参数类型，点击获取公钥明文，期望返回'公钥：'"
        caseResult = None
        e = None
        ParaLists = ['AllPubKey', 'CertPubKey', 'NoCertPubKey']

        logger.critical("beginning... || %s ", caseTitle)
        initResult=self.CertRequest.init_key(str_srcPin,str_srcPin)
        if initResult[0]:
            for testReadType in ParaLists:
                pubKeyResult = self.testCtrl.get_PubKey(testReadType)
                #logger.warning(testReadType+"||"+pubKeyResult)
                pubKeyResult = re.sub(re.compile('\s+'), ' ', pubKeyResult)
                if 3==len(pubKeyResult) and operator.eq('公钥：', pubKeyResult):
                    caseResult = "pass"
                    logger.critical("%s || %s", caseResult, testReadType)
                else:
                    caseResult = "fail"
                    logger.critical("%s || %s || %s ", caseResult, testReadType, pubKeyResult)
        else:
            caseResult = "fail"
            e = "初始化失败,结束用例执行"
            logger.critical("%s || %s ", caseResult, e)

        logger.critical("end. || %s ",caseTitle)
        return caseResult

    def negativeCase_oneCert_voidParachoice(self):
        #用例描述：插入一只有1张证书的U盾，不选择获取类型，点击获取公钥明文，期望返回获取公钥失败:未知错误。返回码:-304Failed Param!    
        caseTitle="用例——插入有1张证书的U盾，不选择获取类型，点击获取公钥明文，期望返回获取公钥失败:未知错误。返回码:-304Failed Param!"    
        caseResult = None
        e = None

        ReadType = ''
        certResult=self.CertRequest.genCert_with_RSA1024_Mix()
        if certResult[1]:
            pubKeyResult=self.testCtrl.get_PubKey(ReadType)
            pubKeyResult=re.sub(re.compile('\s+'),' ',pubKeyResult)
            if operator.eq(para_Err, pubKeyResult):
                caseResult = "pass"
            else:
                caseResult = "fail"
                e = "实测返回：" + "“" + pubKeyResult+ "”"
        else:
            caseResult = "fail"
            e = "证书下载失败,结束用例执行"

        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult            

    def positiveCase_oneCert_validParaChoice(self):
        #用例描述：插入一只有1张证书的U盾，选择获取类型所有公钥、证书中的公钥、非证书中的公钥，点击获取公钥明文，期望返回正确公钥值     
        caseTitle="用例——插入有1张证书的U盾，遍历不同的参数类型，点击获取公钥明文，期望返回正确公钥值"
        caseResult = None
        e = None

        ParaLists = ['AllPubKey', 'CertPubKey', 'NoCertPubKey']
        logger.critical("beginning... || %s ", caseTitle)

        certResult = self.CertRequest.genCert_with_RSA1024_Mix()
        if certResult[1]:
            for testReadType in ParaLists:
                pubKeyResult = self.testCtrl.get_PubKey(testReadType)
                #logger.warning(testReadType+"||"+pubKeyResult)
                pubKeyResult = re.sub(re.compile('\s+'), ' ', pubKeyResult)
                if pubKeyResult.count("公钥："):
                    if (len(pubKeyResult)>3 and (operator.eq(testReadType, ParaLists[0]) or operator.eq(testReadType, ParaLists[1])))\
                     or (len(pubKeyResult)== 3 and operator.eq(testReadType, ParaLists[2])):
                        caseResult = "pass"
                        logger.critical("%s || %s", caseResult, testReadType)
                    else:
                        caseResult = "fail"
                        logger.critical("%s || %s || %s ", caseResult, testReadType, pubKeyResult)
                else:
                    caseResult = "fail"
                    logger.critical("%s || %s || %s ", caseResult, testReadType, pubKeyResult)
        else:
            caseResult = "fail"
            e = "证书下载失败,结束用例执行"
            logger.critical("%s || %s ", caseResult, e)

        logger.critical("end. || %s ",caseTitle)
        return caseResult  
     
    def negativeCase_manyCert_voidParaChoice(self):
        #用例描述：插入一只有多张证书的U盾，不选择获取类型，点击获取公钥明文，期望返回获取公钥失败:未知错误。返回码:-304Failed Param!
        caseTitle="用例——插入有多张证书的U盾，不选择获取类型，点击获取公钥明文，期望返回获取公钥失败:未知错误。返回码:-304Failed Param!"
        caseResult = None
        e = None

        ReadType = ''
        certResult = self.CertRequest.genCert_with_rsa1024M_and_rsa2048M()      
        if certResult[1]:
            pubKeyResult=self.testCtrl.get_PubKey(ReadType)
            pubKeyResult=re.sub(re.compile('\s+'),' ',pubKeyResult)
            if operator.eq(para_Err, pubKeyResult):
                caseResult = "pass"
            else:
                caseResult = "fail"
                e = "实测返回：" + "“" + pubKeyResult+ "”"
        else:
            caseResult = "fail"
            e = "证书下载失败,结束用例执行"

        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult 
        
    def positiveCase_manyCert_validParaChoice(self):
        #用例描述：插入一只有多张证书的U盾，选择获取类型所有公钥，点击获取公钥明文，期望返回正确公钥值 
        caseTitle="用例——插入有多张证书的U盾，遍历不同的参数类型，点击获取公钥明文，期望返回正确公钥值"
        caseResult = None
        e = None

        ParaLists = ['AllPubKey', 'CertPubKey', 'NoCertPubKey']
        logger.critical("beginning... || %s ", caseTitle)
        certResult = self.CertRequest.genCert_with_rsa1024M_and_rsa2048M()
        if certResult[1]:
            for testReadType in ParaLists:
                pubKeyResult = self.testCtrl.get_PubKey(testReadType)
                #logger.warning(testReadType+"||"+pubKeyResult)
                pubKeyResult = re.sub(re.compile('\s+'), ' ', pubKeyResult)
                if pubKeyResult.count("公钥："):
                    if (len(pubKeyResult)>3 and (operator.eq(testReadType, ParaLists[0]) or operator.eq(testReadType, ParaLists[1])))\
                     or (len(pubKeyResult)== 3 and operator.eq(testReadType, ParaLists[2])):
                        caseResult = "pass"
                        logger.critical("%s || %s", caseResult, testReadType)
                    else:
                        caseResult = "fail"
                        logger.critical("%s || %s || %s ", caseResult, testReadType, pubKeyResult)
                else:
                    caseResult = "fail"
                    logger.critical("%s || %s || %s ", caseResult, testReadType, pubKeyResult)
        else:
            caseResult = "fail"
            e = "证书下载失败,结束用例执行"
            logger.critical("%s || %s ", caseResult, e)

        logger.critical("end. || %s ", caseTitle)
        return caseResult
        
    def negativeCase_oneCertAndtempKeyPair_voidParaChoice(self):
        #用例描述：插入一只有1张证书、1对临时密钥对的U盾，不选择获取类型，点击获取公钥明文，期望返回获取公钥失败:未知错误。返回码:-304Failed Param! 
        caseTitle="用例——插入有1张证书、1对临时密钥对的U盾，不选择获取类型，点击获取公钥明文，期望返回获取公钥失败:未知错误。返回码:-304Failed Param!"
        caseResult = None
        e = None
        ReadType = ''

        certResult = self.CertRequest.genCert_with_RSA1024_Mix()
        keypairResult=self.CertRequest.genKeyPair(CertListInfoMap["RSA1024_Mixed"], certResult[2])          
        if certResult[1] and keypairResult[1]:
            pubKeyResult=self.testCtrl.get_PubKey(ReadType)
            pubKeyResult=re.sub(re.compile('\s+'),' ',pubKeyResult)
            if operator.eq(para_Err, pubKeyResult):
                caseResult = "pass"
            else:
                caseResult = "fail"
                e = "实测返回：" + "“" + pubKeyResult+ "”"
        else:
            caseResult = "fail"
            e = "生成密钥或证书下载失败，结束用例执行"

        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult 
        
    def positiveCase_oneCertAndtempKeyPair_validParaChoice(self):
        #用例描述：插入一只有1张证书、1对临时密钥对的U盾，选择获取类型所有公钥，点击获取公钥明文，期望返回正确公钥值   
        caseTitle="用例——插入有1张证书、1对临时密钥对的U盾，遍历不同的参数类型，点击获取公钥明文，期望返回正确公钥值"
        caseResult = None
        e = None

        ParaLists = ['AllPubKey', 'CertPubKey', 'NoCertPubKey']
        logger.critical("beginning... || %s ", caseTitle)
        certResult = self.CertRequest.genCert_with_RSA1024_Mix()
        keypairResult=self.CertRequest.genKeyPair(CertListInfoMap["RSA1024_Mixed"], certResult[2])
        if certResult[1] and keypairResult[1]: 
            for testReadType in ParaLists:
                pubKeyResult = self.testCtrl.get_PubKey(testReadType)
                #logger.warning(testReadType+"||"+pubKeyResult)
                pubKeyResult = re.sub(re.compile('\s+'), ' ', pubKeyResult)
                if pubKeyResult.count("公钥：") and len(pubKeyResult)>3:
                    caseResult = "pass"
                    logger.critical("%s || %s", caseResult, testReadType)
                else:
                    caseResult = "fail"
                    logger.critical("%s || %s || %s ", caseResult, testReadType, pubKeyResult)
        else:
            caseResult = "fail"
            e = "生成密钥或证书下载失败，结束用例执行"
            logger.critical("%s || %s ", caseResult, e)

        logger.critical("end. || %s ", caseTitle)
        return caseResult
             
    def negativeCase_manyCertAndmanyTempKeyPair_voidParaChoice(self):
        #用例描述：插入一只有2张证书，2对临时密钥对的U盾，不选择获取类型，点击获取公钥明文，期望返回获取公钥失败:未知错误。返回码:-304 Failed Param!
        caseTitle="用例——插入有2张证书，2对临时密钥对的U盾，不选择获取类型，点击获取公钥明文，期望返回获取公钥失败:未知错误。返回码:-304 Failed Param!"
        caseResult = None
        e = None
        ReadType = ''

        certResult = self.CertRequest.genCert_with_rsa1024M_and_rsa2048M() 
        keypairResult=self.CertRequest.genKeyPair(CertListInfoMap["RSA1024_M_and_RSA2048_M"], certResult[2])                              
        if certResult[1] and keypairResult[1]:
            pubKeyResult=self.testCtrl.get_PubKey(ReadType)
            pubKeyResult=re.sub(re.compile('\s+'),' ',pubKeyResult)
            if operator.eq(para_Err, pubKeyResult):
                caseResult = "pass"
            else:
                caseResult = "fail"
                e = "实测返回：" + "“" + pubKeyResult+ "”"
        else:
            caseResult = "fail"
            e = "生成密钥或证书下载失败，结束用例执行"
            
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult 
        
    def positiveCase_manyCertAndmanyTempKeyPair_validParaChoice(self):
        #用例描述：插入一只有2张证书，2对临时密钥对的U盾，选择获取类型所有公钥，点击获取公钥明文，期望返回正确公钥值
        caseTitle="用例——插入一只有2张证书，2对临时密钥对的U盾，选择获取类型所有公钥，点击获取公钥明文，期望返回正确公钥值"
        caseResult=None
        e=None
        ParaLists = ['AllPubKey', 'CertPubKey', 'NoCertPubKey']
        logger.critical("beginning... || %s ", caseTitle)
        certResult = self.CertRequest.genCert_with_rsa1024M_and_rsa2048M() 
        keypairResult=self.CertRequest.genKeyPair(CertListInfoMap["RSA1024_M_and_RSA2048_M"], certResult[2])
        if certResult[1] and keypairResult[1]: 
            for testReadType in ParaLists:
                pubKeyResult = self.testCtrl.get_PubKey(testReadType)
                #logger.warning(testReadType+"||"+pubKeyResult)
                pubKeyResult = re.sub(re.compile('\s+'), ' ', pubKeyResult)
                if pubKeyResult.count("公钥：") and len(pubKeyResult)>3:
                    caseResult = "pass"
                    logger.critical("%s || %s", caseResult, testReadType)
                else:
                    caseResult = "fail"
                    logger.critical("%s || %s || %s ", caseResult, testReadType, pubKeyResult)
        else:
            caseResult = "fail"
            e = "生成密钥或证书下载失败，结束用例执行"
            logger.critical("%s || %s ", caseResult, e)

        logger.critical("end. || %s ", caseTitle)
        return caseResult
            
    def negativeCase_manyKey(self):
        #用例描述：插入多支同款U盾，点击获取公钥明文，期望返回获取公钥失败:未知错误。返回码:-104 There is more than one key!
        caseTitle="用例——插入多支同款U盾，点击获取公钥明文，期望返回获取公钥失败:未知错误。返回码:-104 There is more than one key!"
        caseResult=None
        e=None
        testReadType='AllPubKey'
        pubKeyResult = self.testCtrl.get_PubKey(testReadType)
        #logger.warning(testReadType+"||"+pubKeyResult)
        pubKeyResult = re.sub(re.compile('\s+'), ' ', pubKeyResult)
        if operator.eq(many_key_Err, pubKeyResult):
            caseResult = "pass"
        else:
            caseResult = "fail"
            e = "实测返回：" + "“" + pubKeyResult+ "”"   
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle, e)
        return caseResult
                   
    def positiveCase_operation(self):
        #用例描述：插入多支同款U盾，拔出多余U盾，只留1支在位，选择获取类型所有公钥，点击获取公钥明文，期望返回正确公钥值
        caseTitle="用例——插入多支同款U盾，拔出多余U盾，只留1支在位，点击获取公钥明文,期望返回公钥明文字符串信息"
        caseResult=None
        e=None

        ParaLists = ['AllPubKey', 'CertPubKey', 'NoCertPubKey']

        logger.critical("beginning... || %s ", caseTitle)
        for testReadType in ParaLists:
            pubKeyResult = self.testCtrl.get_PubKey(testReadType)
            #logger.warning(testReadType+"||"+pubKeyResult)
            pubKeyResult = re.sub(re.compile('\s+'), ' ', pubKeyResult)
            if pubKeyResult.count("公钥："):
                caseResult = "pass"
                logger.critical("%s || %s", caseResult, testReadType)
            else:
                caseResult = "fail"
                logger.critical("%s || %s || %s ", caseResult, testReadType, pubKeyResult)
        else:
            caseResult = "fail"
            e = "证书下载失败，结束用例执行"
            logger.critical("%s || %s ", caseResult, e)

        logger.critical("end. || %s ", caseTitle)
        return caseResult 

#########################
#开始测试
#########################