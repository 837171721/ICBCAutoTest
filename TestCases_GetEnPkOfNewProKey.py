
#coding=utf-8
'''
Created on 2018.04.05 @author:  lzy
Created on 2018.08.18 @author:  ys
'''
import re
import random
import string
import operator
import GenCertGroup
from GlobalConfigure import levels, log_level,str_srcPin,str_Base64Data,CertListInfoMap
from logTest import SysClass, LoggerClass
conf  = LoggerClass(loglevel=levels.get(log_level), logger="TestCases_GetEnPkOfNewProKey.py")
logger=conf.getlogger()

format_key_Err='''加密公钥：'''
ver_Err = '''获取新保护密钥下的加密公钥:未知错误。返回码:-411 ukey version error!'''
#no_key_Err='''获取新保护密钥下的加密公钥:未知错误。返回码:-102 There is no key!'''
para_Err='''获取新保护密钥下的加密公钥:未知错误。返回码:-304 Failed Param!'''
unmatched_ID_Err='''获取新保护密钥下的加密公钥:未知错误。返回码:-321 DN data error!'''
unmatched_Cert_Err = '''获取新保护密钥下的加密公钥:未知错误。返回码:-300 unKnown error!'''
base64Data_Err = '''获取新保护密钥下的加密公钥:未知错误。返回码:-401 Base64 decoding failed!'''
many_key_Err='''获取新保护密钥下的加密公钥:未知错误。返回码:-104 There is more than one key!'''

def test_GetEncPkeyOfNewAdminKey(ctrlObj,TestingRange,AdminKeyInfo):
    #调用流程    
    testCtrl=GetEncPkeyOfNewAdminKeyCases(ctrlObj,AdminKeyInfo)  #建立类对象，打开控件测试页
    if '00' == AdminKeyInfo[1]:
        casePubKeyCResult=testCtrl.testCtrl.get_GMPubKeyC('02','01','1DdS5cZN8BYWb1YYx1en')
        casePubKeyCResult=re.sub(re.compile('\s+'), ' ', casePubKeyCResult)
        if operator.eq(casePubKeyCResult,ver_Err):
            logger.warning("接口不支持，请选择国密新体系盾进行!")
            return
    testGetEncPkeyOfNewAdminKeyGroup(testCtrl,TestingRange)   #测试用例集，根据测试范围定义测试强度
    
def testGetEncPkeyOfNewAdminKeyGroup(ctrlElemObj,testRange):
    #测试用例集
    if 0 == testRange:  #详细测试
        testResult=ctrlElemObj.positiveCase_validCert_validParaChoice()
        
        testResult=ctrlElemObj.positiveCase_tempKeyPair_validParaChoice()
        
        testResult=ctrlElemObj.negativeCase_validCert_unMatchedParaChoice()

        testResult=ctrlElemObj.negativeCase_tempKeyPair_unMatchedParaChoice()
                               
        testResult=ctrlElemObj.negativeCase_formartKey_voidParaChoice()
        
        testResult=ctrlElemObj.negativeCase_formartKey_ErrParaChoice()

    elif 1 == testRange: #验证测试
        testResult=ctrlElemObj.positiveCase()
      
    elif 2 == testRange:#无Key测试
        testResult = ctrlElemObj.negativeCase_noKey_voidParaChoice()

        testResult = ctrlElemObj.negativeCase_noKey_ErrParaChoice() 
          
    elif 3 == testRange:#多Key测试
        testResult = ctrlElemObj.negativeCase_manyKey_voidParaChoice()
        
        testResult = ctrlElemObj.negativeCase_manyKey_validParaChoice()
        
        testResult = ctrlElemObj.negativeCase_manyKey_ErrParaChoice()    
            
    elif 4 == testRange:#多Key测试
        testResult=ctrlElemObj.positiveCase()
       
class GetEncPkeyOfNewAdminKeyCases():
    def __init__(self,testCtrl,AdminKeyInfo):
        self.testCtrl=testCtrl   #控件测试页
        self.AdminKeyAlgId=AdminKeyInfo  #保护密钥信息
        self.CertRequest=GenCertGroup.GenCertClass(self.testCtrl,AdminKeyInfo)   #创建证书申请对象              
    
    def positiveCase(self):
        #用例描述：插入1支U盾，输入正确的参数，点击获取新保护密钥的加密公钥，期望返回U盾新保护密钥的加密公钥
        caseTitle="用例——插入1支U盾，输入正确的参数，点击获取新保护密钥的加密公钥，期望返回U盾新保护密钥的加密公钥"
        caseResult = None
        e = None

        ParaLists = ['01', '02']

        logger.critical("beginning... || %s ",caseTitle)

        certResult=self.CertRequest.genCert_with_rsa2048M_and_sm2Sp()
        keyPairResult=self.CertRequest.genKeyPair(CertListInfoMap["SM2256_Comm_p"], certResult[2])
        if certResult[1] and keyPairResult[1]:
            for curType in ParaLists:
                tempPara=certResult[0]    #证书DN
                if ParaLists[0] == curType:
                    tempPara= keyPairResult[0]  #临时密钥对   
                testResult=self.testCtrl.get_GMPubKeyC(curType,tempPara[0],str_Base64Data)
                testResult = re.sub(re.compile('\s+'), ' ', testResult)
                #logger.warning("获取类型值为：%s,其他参数有效，测试结果为：%s", curType, testResult)
                if (format_key_Err in testResult) and len(testResult) > 50:
                    caseResult = "pass"
                    logger.critical("%s || %s || %s ", caseResult, curType, testResult)
                else:
                    caseResult = "fail"
                    logger.critical("%s || %s || %s ", caseResult, curType, testResult)
        else:
            caseResult = "fail"
            e = "生成密钥或下证失败，结束用例执行！"
            logger.critical("%s || %s ", caseResult, e)

        logger.critical("end. || %s ",caseTitle)
        return caseResult

    def positiveCase_validCert_validParaChoice(self):    
        #用例描述：插入1支有证书的U盾，1）    获取类型：签名；2）    输入正确的证书DN（由“获取证书DN”获得）；3）    输入正确服务器随机数（如TW9LsstNnt/cDGFB2FXU）点击新加密公钥       
        caseTitle = "用例——插入1支有证书的U盾，1）获取类型设为:签名; 2） 输入正确的证书DN和服务器随机数，获取新体系密钥公钥  ，期望返回正确的密文公钥"
        caseResult = None
        e = None
 
        certResult=self.CertRequest.genCert_with_SM2256C_and_SM2256S()
        if certResult[1]:
            DNorID = certResult[0]
            str_Base64Data =self.testCtrl.get_ServerRandom()
            testResult=self.testCtrl.get_GMPubKeyC('02',DNorID[0],str_Base64Data)
            testResult = re.sub(re.compile('\s+'),' ',testResult)
            #logger.warning("获取类型值为：02,选择证书DN,测试结果为：%s", testResult)
            if (format_key_Err in testResult) and len(testResult) > 50:
                caseResult = "pass"
            else:
                caseResult = "fail"    
                e = "实测返回：" +"“"+testResult +"”"         
        else:
            caseResult = "fail"
            e = "下证失败，结束用例执行！"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult              

    def positiveCase_tempKeyPair_validParaChoice(self):    
        #用例描述：插入1支只有临时密钥对的U盾,1）获取类型：下证；2）输入正确的公钥ID和服务器随机数,获取新体系密钥公钥 ,期望返回正确的密文公钥       
        caseTitle = "用例——插入1支只有临时密钥对的U盾,1）获取类型：下证；2）输入正确的公钥ID和服务器随机数,获取新体系密钥公钥 ,期望返回正确的密文公钥"
        caseResult = None
        e = None
        
        keypairResult=self.CertRequest.genKeyPair(CertListInfoMap["SM2256_Sig2_c"], str_srcPin,True)
        if keypairResult[1]:
            pubID = keypairResult[0]
            str_Base64Data =self.testCtrl.get_ServerRandom()
            testResult=self.testCtrl.get_GMPubKeyC('01',pubID[0],str_Base64Data)
            testResult = re.sub(re.compile('\s+'),' ',testResult)
            #logger.warning("获取类型值为：01,选择公钥ID,测试结果为：%s", testResult)
            if (format_key_Err in testResult) and len(testResult) > 50:
                caseResult = "pass"
            else:
                caseResult =  "fail"
                e = "实测返回：" +"“"+testResult +"”"        
        else:
            caseResult = "fail"
            e = "生成临时密钥对失败，结束用例执行！"
            
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult  

    def negativeCase_validCert_unMatchedParaChoice(self):    
        #用例描述：插入1支有证书的U盾，1） 获取类型：下证；2）输入正确的证书DN和 服务器随机数,获取新体系密钥公钥,期望返回:获取新保护密钥下的加密公钥:未知错误。返回码:-300 unKnown error!"
        caseTitle = "用例——插入1支有证书的U盾，1）获取类型设为：下证;2）输入正确的证书DN和服务器随机数,获取新体系密钥公钥  ，期望返回“获取新保护密钥下的加密公钥:未知错误。返回码:-300 unKnown error!”"
        caseResult = None
        e = None
        certResult=self.CertRequest.genCert_with_rsa2048M_and_sm2Sp()
        if certResult[1]:
            DNorID = certResult[0]
            #str_Base64Data =self.testCtrl.get_Base64Random()
            testResult=self.testCtrl.get_GMPubKeyC('01',DNorID[1],str_Base64Data)
            testResult = re.sub(re.compile('\s+'),' ',testResult)
            #logger.warning("获取类型值为：01,选择证书DN,测试结果为：%s", testResult)
            if operator.eq(testResult,unmatched_Cert_Err):
                caseResult = "pass"
            else:
                caseResult = "fail"    
                e = "实测返回：" +"“"+testResult +"”"        
        else:
            caseResult = "fail"
            e = "下证失败，结束用例执行！"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult              

    def negativeCase_tempKeyPair_unMatchedParaChoice(self):    
        #用例描述：插入1支只有临时密钥对的U盾,1）获取类型设为：签名；2）输入正确的公钥ID和服务器随机数,获取新体系密钥公钥 ,期望返回“获取新保护密钥下的加密公钥:未知错误。返回码:-321”
        caseTitle = "用例——插入1支只有临时密钥对的U盾,1）获取类型设为：签名;2）输入正确的公钥ID和服务器随机数,获取新体系密钥公钥 ,期望返回“获取新保护密钥下的加密公钥:未知错误。返回码:-321 DN data error!”"
        caseResult = None
        e = None
 
        keypairResult=self.CertRequest.genKeyPair(CertListInfoMap["SM2256_Comm_p"], str_srcPin,True)
        if keypairResult[1]:
            pubID = keypairResult[0]
            #SerRand =self.testCtrl.get_Base64Random()
            testResult=self.testCtrl.get_GMPubKeyC('02',pubID[0],str_Base64Data)
            testResult = re.sub(re.compile('\s+'),' ',testResult)
            #logger.warning("获取类型值为：02,选择公钥ID,测试结果为：%s", testResult)
            if operator.eq(testResult,unmatched_ID_Err):
                caseResult = "pass"
            else:
                caseResult = "fail"    
                e = "实测返回：" +"“"+testResult +"”"     
        else:
            caseResult = "fail"
            e = "生成临时密钥对失败，结束用例执行！"
            
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult

    def negativeCase_formartKey_voidParaChoice(self):
        # 用例描述：插入1支格式化的U盾,获取类型为空/正确输入情况下，不输入证书DN或公钥ID，不输入服务器随机数，点击新加密公钥
        caseTitle = "用例——插入1支格式化的U盾,获取类型为空/正确输入情况下，证书DN或公钥ID 及服务器随机数为空，点击获取新体系密文公钥 ,期望返回“获取新保护密钥下的加密公钥:未知错误。返回码:-304 Failed Param!”"
        caseResult = None
        e = None
        ParaLists = ['', '01', '02']
        logger.critical("beginning... || %s ",caseTitle)
        initResult = self.CertRequest.init_key(str_srcPin, str_srcPin)
        if initResult[0]:
            for curType in ParaLists:
                testResult = self.testCtrl.get_GMPubKeyC(curType, None, None)
                testResult = re.sub(re.compile('\s+'), ' ', testResult)
                #logger.warning("获取类型值为：%s,其他参数为空，测试结果为：%s", curType, testResult)
                if operator.eq(testResult, para_Err):
                    caseResult = "pass"
                    logger.critical("%s || %s || %s ", caseResult, curType, testResult)
                else:
                    caseResult = "fail"
                    logger.critical("%s || %s || %s ", caseResult, curType, testResult)
        else:
            caseResult = "fail"
            e = "初始化操作失败，结束用例执行！"
            logger.critical("%s || %s ", caseResult, e)

        logger.critical("end. || %s ",caseTitle)
        return caseResult

    def negativeCase_formartKey_ErrParaChoice(self):
        # 用例描述：插入1支格式化的U盾,分别选择获取类型为：签名/下证，任意输入证书DN或公钥ID，任意输入服务器随机数，点击新加密公钥
        caseTitle = "用例——插入1支格式化的U盾,遍历获取类型(签名/下证)，证书DN或公钥ID 及服务器随机数任意输入，点击获取新体系加密公钥 期望返回“获取新保护密钥下的加密公钥:未知错误。返回码:-401 Base64 decoding failed!”"
        caseResult = None
        e = None
        # no_info_Err = "获取新保护密钥下的加密公钥:未知错误。返回码:-401 Base64 decoding failed!"

        CertDnLen = random.randint(0, 60)
        CertDnRandom = ''.join(random.sample(string.ascii_letters + string.digits, CertDnLen)).replace(" ", "")
        serverRandom = ''.join(random.sample(string.ascii_letters + string.digits + '@#$%^&*()?<>/', 16)).replace(" ",                                                                                                                 "")
        PubIdRandom = random.randint(10, 100)
        ParaLists = ['01', '02']
        logger.critical("beginning... || %s ",caseTitle)
        initResult = self.CertRequest.init_key(str_srcPin, str_srcPin)
        if initResult[0]:
            for curType in ParaLists:
                tempPara = CertDnRandom  # 证书DN
                if ParaLists[0] == curType:
                    tempPara = PubIdRandom  # 临时密钥对
                testResult = self.testCtrl.get_GMPubKeyC(curType, tempPara, serverRandom)
                testResult = re.sub(re.compile('\s+'), ' ', testResult)
                logger.warning("获取类型值为：%s,其他参数任意,测试结果为：%s", curType, testResult)
                logger.warning("%s,%s", curType, testResult)
                if operator.eq(testResult, base64Data_Err):
                    caseResult = "pass"
                    logger.critical("%s || %s || %s ", caseResult, curType, testResult)
                else:
                    caseResult = "fail"
                    logger.critical("%s || %s || %s ", caseResult, curType, testResult)
        else:
            caseResult = "fail"
            e = "初始化操作失败，结束用例执行！"
            logger.critical("%s || %s ", caseResult, e)

        logger.critical("end. || %s ",caseTitle)
        return caseResult

    def negativeCase_noKey_voidParaChoice(self):  
        #用例描述： 未插入U盾，不选择获取类型，不输入证书DN或公钥ID，不输入服务器随机数，点击新加密公钥，期望返回获“获取新保护密钥下的加密公钥:未知错误。返回码:-304           
        caseTitle = "用例——未插入U盾，获取类型为空/正确输入情况下,证书DN或公钥ID及服务器随机数为空,点击获取新体系密文公钥 ,期望返回“获取新保护密钥下的加密公钥:未知错误。返回码:-304 Failed Param!”"
        caseResult = None
        e=None 
        
        ParaLists=['','01','02']
        logger.critical("beginning... || %s ",caseTitle)
        for curType in ParaLists:
            testResult=self.testCtrl.get_GMPubKeyC(curType,None,None)
            testResult = re.sub(re.compile('\s+'),' ',testResult)
            #logger.warning("获取类型值为：%s,其他参数为空,测试结果为：%s", curType, testResult)
            if operator.eq(testResult,para_Err):
                caseResult = "pass"
                logger.critical("%s || %s || %s ", caseResult, curType, testResult)
            else:
                caseResult = "fail"
                logger.critical("%s || %s || %s ", caseResult, curType, testResult)

        logger.critical("end. || %s ",caseTitle)
        return caseResult

    def negativeCase_noKey_ErrParaChoice(self):
        #用例描述：未插入U盾,遍历获取类型(签名/下证)，证书DN或公钥ID 及服务器随机数任意输入，点击获取新体系加密公钥 期望返回“获取新保护密钥下的加密公钥:未知错误。返回码:-304 Failed Param!”"
        caseTitle = "用例——未插入U盾,遍历获取类型(签名/下证)，证书DN或公钥ID 及服务器随机数任意输入，点击获取新体系加密公钥 期望返回“获取新保护密钥下的加密公钥:未知错误。返回码:-304 Failed Param!”"
        caseResult = None
        e=None
        CertDnLen=random.randint(0,60)
        CertDnRandom=''.join(random.sample(string.ascii_letters + string.digits,CertDnLen)).replace(" ","")
        serverRandom=''.join(random.sample(string.ascii_letters+string.digits+'abcdefg&#%^*f012*9',16)).replace(" ","")  
        PubIdRandom=random.randint(10,100)
        ParaLists=['01','02']

        logger.critical("beginning... || %s ",caseTitle)
        for curType in ParaLists:
            tempPara=CertDnRandom    #证书DN
            if ParaLists[0] == curType:
                tempPara= PubIdRandom  #临时密钥对   
            testResult=self.testCtrl.get_GMPubKeyC(curType,tempPara,serverRandom)
            testResult = re.sub(re.compile('\s+'),' ',testResult)
            #logger.warning("获取类型值为：%s,其他参数任意,测试结果为：%s", curType, testResult)
            if operator.eq(testResult,base64Data_Err):
                caseResult = "pass"
                logger.critical("%s || %s || %s ", caseResult, curType, testResult)
            else:
                caseResult = "fail"
                logger.critical("%s || %s || %s ", caseResult, curType, testResult)

        logger.critical("end. || %s ",caseTitle)
        return caseResult

    def negativeCase_manyKey_voidParaChoice(self):
        # 用例描述：插入多支同款U盾，不输入参数，点击新加密公钥
        caseTitle = "用例——插入多支同款U盾，不输入参数，获取新体系的密文公钥,期望返回“获取新保护密钥下的加密公钥:未知错误。返回码:-304 Failed Param!”"
        caseResult = None
        e = None

        testResult = self.testCtrl.get_GMPubKeyC(None, None, None)
        testResult = re.sub(re.compile('\s+'), ' ', testResult)
        #logger.warning("空参数输入，测试结果为：%s", testResult)
        if operator.eq(testResult, para_Err):
            caseResult = "pass"
        else:
            caseResult = "fail"
            e = "实测返回：" + "“" + testResult + "”"

        if e == None:
            logger.critical("%s || %s ", caseTitle, caseResult)
        else:
            logger.critical("%s || %s || %s ", caseTitle, caseResult, e)
        return caseResult

    def negativeCase_manyKey_validParaChoice(self):
        #用例描述：插入多支同款U盾，输入各合法参数，点击新加密公钥       
        caseTitle = "用例——插入多支同款U盾,输入各合法参数,获取新体系的密文公钥,期望返回“获取新保护密钥下的加密公钥:未知错误。返回码:-104 There is more than one key!”"
        caseResult = None
        e = None
        DNorID = 'CN=TestRSA2048,OU=MiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOuMiniCaOu,O=rsaperca139.com.cn'
        PubId ='01'
        ParaLists=['01','02']

        logger.critical("beginning... || %s ",caseTitle)
        for curType in ParaLists:
            tempPara=DNorID    #证书DN
            if ParaLists[0] == curType:
                tempPara= PubId  #临时密钥对   
            testResult=self.testCtrl.get_GMPubKeyC(curType,tempPara,str_Base64Data)
            testResult = re.sub(re.compile('\s+'),' ',testResult)
            #logger.warning("获取类型值为：%s,其他参数有效,测试结果为：%s", curType, testResult)
            if operator.eq(testResult,many_key_Err):
                caseResult = "pass"
                logger.critical("%s || %s || %s ", caseResult, curType, testResult)
            else:
                caseResult = "fail"
                logger.critical("%s || %s || %s ", caseResult, curType, testResult)

        logger.critical("end. || %s ",caseTitle)
        return caseResult
       
    def negativeCase_manyKey_ErrParaChoice(self):
        #用例描述：插入多支同款U盾，任意输入参数，点击新加密公钥       
        caseTitle = "用例——插入多支同款U盾，任意输入参数，点击新加密公钥;期望返回：获取新保护密钥下的加密公钥:未知错误。返回码:-401 Base64 decoding failed!"
        caseResult = None
        e = None

        CertDnLen=random.randint(0,60)
        CertDnRandom=''.join(random.sample(string.ascii_letters + string.digits,CertDnLen)).replace(" ","")
        serverRandom=''.join(random.sample(string.ascii_letters+string.digits+'abcdefg&#%^*f012*9',16)).replace(" ","")  
        PubIdRandom=random.randint(10,100)
        
        ParaLists=['01','02']
        logger.critical("beginning... || %s ",caseTitle)
        for curType in ParaLists:
            tempPara=CertDnRandom    #证书DN
            if ParaLists[0] == curType:
                tempPara= PubIdRandom  #临时密钥对   
            testResult=self.testCtrl.get_GMPubKeyC(curType,tempPara,serverRandom)
            testResult = re.sub(re.compile('\s+'),' ',testResult)
            #logger.warning("获取类型值为：%s,其他参数任意,测试结果为：%s", curType, testResult)
            if operator.eq(testResult,base64Data_Err):
                caseResult = "pass"
                logger.critical("%s || %s || %s ", caseResult, curType, testResult)
            else:
                caseResult = "fail"
                logger.critical("%s || %s || %s ", caseResult, curType, testResult)

        logger.critical("end. || %s ",caseTitle)
        return caseResult            

    def negativeCase_operation(self):    
        #用例描述：插入多支同款U盾，拔出多余U盾，只是1支在位，输入合法参数，点击新加密公钥       
        caseTitle = "用例——插入多支同款U盾，拔出多余U盾，只留1支在位，输入合法参数，点击新加密公钥；期望返回:返回加密公钥结果"
        caseResult = None
        e = None
        certResult=self.CertRequest.genCert_with_rsa2048M_and_sm2Sp()
        if certResult[1]:
                keyType = '02'
                DNorID = certResult[0]
                SerRand =self.testCtrl.get_Base64Random()
                testResult=self.testCtrl.get_GMPubKeyC(keyType,DNorID,SerRand)
                if  len(testResult) > 50 and testResult.count("："):
                        caseResult = "pass"
                else:
                    caseResult =  "fail"
                    if testResult == None:
                        e =" 实测返回：None"
                    else:
                        e =" 实测返回：“"+testResult+"”"        
        else:
            caseResult = "fail"
        if e == None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult              


#########################
#开始测试
#########################
 
    
    
    
    