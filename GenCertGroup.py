#coding=utf-8
'''
Created on 2018.7.29

@author: ys
'''
import operator
import re
import time
#import operator
import TestIcbcGmUserkey
#from  GlobalConfigure import *
from GlobalConfigure import str_title, str_srcPin, CertListInfoMap,testUrl_Manage,testUrl_User,testUrl_GM_User,testUrl_GM_Manage,levels

from logTest import SysClass, LoggerClass
conf  = LoggerClass(loglevel=levels.get("info"), logger="GenCertGroup.py")
logger=conf.getlogger()

init_str='初始化成功'
write_cert_str = '写入证书成功'
clearCert_str='删除指定证书和临时密钥对成功！'


class GenCertClass():
    def __init__(self,CtrlObj,AdminKeyInfo):
        self.CtrlObj=CtrlObj   #控件测试页
        self.AdminKeyAlgId=AdminKeyInfo
        
    def init_key(self,str_initPin,str_veriPin):       
        result='' 
        cur_url=self.CtrlObj.browser.current_url     
        if '00' == self.AdminKeyAlgId[1]:        
            #logger.warning('非国密盾或国密旧体系盾！')
            if  -1 == cur_url.find(testUrl_GM_User) and -1 == cur_url.find(testUrl_User):
                result=self.CtrlObj.initCardDefaultPin()
                str_initPin='12345678'
                str_veriPin='12345678'
            else:
                result=self.CtrlObj.get_InitCard(str_title,str_initPin,str_veriPin)   
        else:
            #logger.warning('国密新体系盾！')
            #获取介质号
            if -1 == cur_url.find(testUrl_GM_User) and -1 == cur_url.find(testUrl_User) : 
                self.CtrlObj.browser.get(testUrl_GM_User)
            str_MediaID=self.CtrlObj.get_MediaId()
            #安全初始化
            self.CtrlObj.browser.get(testUrl_GM_Manage)            
            result=self.CtrlObj.get_SecInitCard(self.AdminKeyAlgId,str_MediaID)
            str_initPin='12345678'
            str_veriPin='12345678'
        if not operator.eq(cur_url,self.CtrlObj.browser.current_url):
            self.CtrlObj.browser.get(cur_url)
            time.sleep(2)                                 
        if init_str in result:
            result=True
        else:
            result = False
        return result,str_initPin,str_veriPin

    def clearCertAndKeyPairs(self,str_initPin,str_veriPin):
        result=clearCert_str
        cur_url=self.CtrlObj.browser.current_url     
        if  -1 == cur_url.find(testUrl_GM_User):
            self.CtrlObj.browser.get(testUrl_GM_User)
        #获取证书DN
        certDn=self.CtrlObj.get_GMCertDN()
        #获取临时密钥对
        pubKeyId=[]
        tempKeyPair=self.CtrlObj.get_PubKey('NoCertPubKey')
        tempKeyPair=tempKeyPair.replace('公钥：', '')
        if False == tempKeyPair.count("||"):                        
            pubKeyId.append(tempKeyPair[0:2])
        else:
            pubKeyList=tempKeyPair.split("||")
            for n in range(0,len(pubKeyList)) :
                strTmp=pubKeyList[n]
                pubKeyId.append(strTmp[0:2]) 
        tempKeyPair="||".join(pubKeyId) 
        #删除证书及临时密钥对
        if  len(certDn) or len(pubKeyId[0]):
            result=self.CtrlObj.get_GMDelTempKey(certDn,tempKeyPair)
        if not operator.eq(cur_url,self.CtrlObj.browser.current_url):
            self.CtrlObj.browser.get(cur_url)
            time.sleep(2) 
                                            
        if clearCert_str in result:
            result=True
        else:
            result =False
        return result,str_initPin,str_veriPin
    
    def genKeyPair(self,RequestDN,strPin=str_srcPin,initPinFlag=False,clearDnFlag=False):
        flag = True
        pubKeyId=[]
        if initPinFlag:
            result = []
            result=self.init_key(strPin,strPin)
            if result[0]:
                flag=result[0]
                strPin=result[1]
        if clearDnFlag:
            result=self.clearCertAndKeyPairs(strPin,strPin)
            if result[0]:
                flag=result[0]
                strPin=result[1]
        if flag:
            cur_url=self.CtrlObj.browser.current_url
            if -1 == cur_url.find(testUrl_GM_User): 
                self.CtrlObj.browser.get(testUrl_GM_User)       
            base64P10=self.CtrlObj.GMCreatePKCS10(RequestDN,str_title,strPin)
            if not operator.eq(base64P10,''):
                RequestDN= self.CtrlObj.get_PubKey('NoCertPubKey')
                RequestDN=RequestDN.replace('公钥：', '')
                if False == RequestDN.count("||"):                        
                    pubKeyId.append(RequestDN[0:2])
                else:
                    pubKeyList=RequestDN.split("||")
                    for n in range(0,len(pubKeyList)) :
                        strTmp=pubKeyList[n]
                        pubKeyId.append(strTmp[0:2])             
                flag = True
            else:
                flag = False
            if not operator.eq(cur_url,self.CtrlObj.browser.current_url):
                self.CtrlObj.browser.get(cur_url) 
        else:
            flag=False

        return pubKeyId,flag,strPin
                   
    def genCert(self,RequestDN,strPin,initPinFlag=True,clearDnFlag=False):
        flag = True
        result = []
        if initPinFlag: #初始化            
            result=self.init_key(strPin,strPin)
            if result[0]:
                flag=result[0]
                strPin=result[1]
        if clearDnFlag: #删除证书及密钥对
            result=self.clearCertAndKeyPairs(strPin,strPin)
            if result[0]:
                flag=result[0]
                strPin=result[1]
        if flag:
            cur_url=self.CtrlObj.browser.current_url
            if -1 == cur_url.find(testUrl_GM_User): 
                self.CtrlObj.browser.get(testUrl_GM_User)
            base64P10=self.CtrlObj.GMCreatePKCS10(RequestDN,str_title,strPin)
            if '' != base64P10 and len(base64P10)>100: 
                self.CtrlObj.P102P7()
                flag=self.CtrlObj.GMWritePKCS7()
            if not operator.eq(cur_url,self.CtrlObj.browser.current_url):
                self.CtrlObj.browser.get(cur_url)
                
        return flag,strPin
    
    def genCert_With_Verify(self,RequestDN,strPin,initPinFlag=True,clearDnFlag=False):
        result = []
        flag=False
        CertDnList=[]     
        if initPinFlag:
            result=self.init_key(strPin,strPin)
            if result[0]:
                flag=result[0]
                strPin=result[1]
        if clearDnFlag: #删除证书及密钥对
            result=self.clearCertAndKeyPairs(strPin,strPin)  
            if result[0]:
                flag=result[0]
                strPin=result[1]
        if flag:
            cur_url=self.CtrlObj.browser.current_url
            if -1 == cur_url.find(testUrl_GM_User): 
                self.CtrlObj.browser.get(testUrl_GM_User)
            base64P10=self.CtrlObj.GMCreatePKCS10(RequestDN,str_title,strPin)
            if False == operator.eq(base64P10,''): 
                self.CtrlObj.P102P7(base64P10)       
                result=self.CtrlObj.GMWritePKCS7()
                if write_cert_str in result:
                    #验证
                    CertDn=self.CtrlObj.get_GMCertDN()
                    flag=self.certVerify(RequestDN,CertDn)
                    if 0 == CertDn.count("||"):
                        CertDnList.append(CertDn)
                    elif 0 < CertDn.count("||"):
                        CertDnList=CertDn.split("||")
            if not operator.eq(cur_url,self.CtrlObj.browser.current_url):
                self.CtrlObj.browser.get(cur_url) 
        return CertDnList,flag,strPin
        
    def certVerify(self,requestDN,respondDN):
        requestP=re.compile("(CN=[^,]*),") #匹配规则：括号表示组的概念，供match使用。[]表示包含哪些字符，^表示不包含哪些字符，*表示一个或多个字符，最后的逗号用于指示匹配的子串的结束位置
        respondP=requestP        
        #获取源DN请求中的CN信息       
        requestDict= self.getStringCnt(requestDN,requestP)               
        #获取响应DN请求中的CN信息
        respondDict=self.getStringCnt(respondDN,respondP)
        if 1 == operator.eq(requestDict, respondDict):
            return True
        else:
            return False

    def getStringCnt(self,str_src,str_pattern):
        match = str_pattern.findall(str_src)
        dict = {}
        if match:
            for i in match:
                if dict.__contains__(i):
                    dict[i]= dict[i]+1
                else:
                    dict[i]=1
            #logger.warning(dict)
            #print(dict)
        return dict

    def multiExsit(self,srcStr,str1,str2):        
        pattern = re.compile("("+str1+").*("+str2+")" +"|"+ "("+str2+").*("+str1+")")
        match = pattern.findall(srcStr);
        if match:          
            return True
        else:
            return False

    def test(self,requestDN,respondDN):  
        #获取源DN请求中的CN信息
        requestP=re.compile("(CN=[^,]*),") #匹配规则：括号表示组的概念，供match使用。[]表示包含哪些字符，^表示不包含哪些字符，*表示一个或多个字符，最后的逗号用于指示匹配的子串的结束位置
        requestDict= self.getStringCnt(requestDN,requestP)
        
        #获取响应DN请求中的CN信息
        #respondDN=self.CtrlObj.get_GMCertDN()
        respondP=requestP
        respondDict=self.getStringCnt(respondDN,respondP)            
        if operator.eq(requestDict, respondDict):
            return True
        else:
            return False

    def genCert_with_RSA1024_Mix(self,initPinFlag=True,clearDnFlag=False,RequestDN=CertListInfoMap["RSA1024_Mixed"],strPin=str_srcPin):
        CertDnList=[]
        flag=False           
        result=self.genCert(RequestDN,strPin,initPinFlag,clearDnFlag)
        if True == operator.eq(write_cert_str,result[0]):
            #验证
            strPin=result[1]     
            cur_url=self.CtrlObj.browser.current_url       
            if 0 <= cur_url.find(testUrl_GM_User):
                CertDn=self.CtrlObj.get_GMCertDN()
                if 0 == CertDn.count("||"):
                    flag=self.certVerify(RequestDN,CertDn)
                    CertDnList.append(CertDn)
            else:
                flag=True
        return CertDnList,flag,strPin
                     
    def genCert_with_RSA1024_Sign_P(self,initPinFlag=True,clearDnFlag=False,RequestDN=CertListInfoMap["RSA1024_Sig2_p"],strPin=str_srcPin):
        CertDnList=[]
        flag=False           
        result=self.genCert(RequestDN,strPin,initPinFlag,clearDnFlag)
        if True == operator.eq(write_cert_str,result[0]):
            #验证
            strPin=result[1]
            cur_url=self.CtrlObj.browser.current_url            
            if 0 <= cur_url.find(testUrl_GM_User):
                CertDn=self.CtrlObj.get_GMCertDN()
                if 0 == CertDn.count("||"):
                    flag=self.certVerify(RequestDN,CertDn)
                    CertDnList.append(CertDn)
            else:
                flag=True
        return CertDnList,flag,strPin
     
    def genCert_with_RSA1024_Sign_C(self,initPinFlag=True,clearDnFlag=False,RequestDN=CertListInfoMap["RSA1024_Sig2_c"],strPin=str_srcPin):
        CertDnList=[]
        flag=False           
        result=self.genCert(RequestDN,strPin,initPinFlag,clearDnFlag)
        if True == operator.eq(write_cert_str,result[0]):
            #验证
            strPin=result[1]
            cur_url=self.CtrlObj.browser.current_url 
            if 0 <= cur_url.find(testUrl_GM_User):
                CertDn=self.CtrlObj.get_GMCertDN()
                if 0 == CertDn.count("||"):
                    flag=self.certVerify(RequestDN,CertDn)
                    CertDnList.append(CertDn)
            else:
                flag=True
        return CertDnList,flag,strPin
                     
    def genCert_with_RSA1024_Comm_P(self,initPinFlag=True,clearDnFlag=False,RequestDN=CertListInfoMap["RSA1024_Comm_p"],strPin=str_srcPin):
        CertDnList=[]
        flag=False           
        result=self.genCert(RequestDN,strPin,initPinFlag,clearDnFlag)
        if True == operator.eq(write_cert_str,result[0]):
            #验证
            strPin=result[1]
            cur_url=self.CtrlObj.browser.current_url 
            if 0 <= cur_url.find(testUrl_GM_User):
                CertDn=self.CtrlObj.get_GMCertDN()
                if 0 == CertDn.count("||"):
                    flag=self.certVerify(RequestDN,CertDn)
                    CertDnList.append(CertDn)
            else:
                flag=True
        return CertDnList,flag,strPin
     
    def genCert_with_RSA1024_Comm_C(self,initPinFlag=True,clearDnFlag=False,RequestDN=CertListInfoMap["RSA1024_Comm_c"],strPin=str_srcPin):
        CertDnList=[]
        flag=False           
        result=self.genCert(RequestDN,strPin,initPinFlag,clearDnFlag)
        if True == operator.eq(write_cert_str,result[0]):
            #验证
            strPin=result[1]
            cur_url=self.CtrlObj.browser.current_url 
            if 0 <= cur_url.find(testUrl_GM_User):
                CertDn=self.CtrlObj.get_GMCertDN()
                if 0 == CertDn.count("||"):
                    flag=self.certVerify(RequestDN,CertDn)
                    CertDnList.append(CertDn)
            else:
                flag=True
        return CertDnList,flag,strPin
            
    def genCert_with_RSA2048_Mix(self,initPinFlag=True,clearDnFlag=False,RequestDN=CertListInfoMap["RSA2048_Mixed"],strPin=str_srcPin):
        CertDnList=[]
        flag=False           
        result=self.genCert(RequestDN,strPin,initPinFlag,clearDnFlag)
        if True == operator.eq(write_cert_str,result[0]):
            #验证
            strPin=result[1]
            cur_url=self.CtrlObj.browser.current_url 
            if 0 <= cur_url.find(testUrl_GM_User):
                CertDn=self.CtrlObj.get_GMCertDN()
                if 0 == CertDn.count("||"):
                    flag=self.certVerify(RequestDN,CertDn)
                    CertDnList.append(CertDn)
            else:
                flag=True
        return CertDnList,flag,strPin
           
    def genCert_with_RSA2048_Sign_P(self,initPinFlag=True,clearDnFlag=False,RequestDN=CertListInfoMap["RSA2048_Sig2_p"],strPin=str_srcPin):
        CertDnList=[]
        flag=False           
        result=self.genCert(RequestDN,strPin,initPinFlag,clearDnFlag)
        if True == operator.eq(write_cert_str,result[0]):
            #验证
            strPin=result[1]
            cur_url=self.CtrlObj.browser.current_url 
            if 0 <= cur_url.find(testUrl_GM_User):
                CertDn=self.CtrlObj.get_GMCertDN()
                if 0 == CertDn.count("||"):
                    flag=self.certVerify(RequestDN,CertDn)
                    CertDnList.append(CertDn)
            else:
                flag=True
        return CertDnList,flag,strPin
    
    def genCert_with_RSA2048_Sign_C(self,initPinFlag=True,clearDnFlag=False,RequestDN=CertListInfoMap["RSA2048_Sig2_c"],strPin=str_srcPin):
        CertDnList=[]
        flag=False           
        result=self.genCert(RequestDN,strPin,initPinFlag,clearDnFlag)
        if True == operator.eq(write_cert_str,result[0]):
            #验证
            strPin=result[1]
            cur_url=self.CtrlObj.browser.current_url 
            if 0 <= cur_url.find(testUrl_GM_User):
                CertDn=self.CtrlObj.get_GMCertDN()
                if 0 == CertDn.count("||"):
                    flag=self.certVerify(RequestDN,CertDn)
                    CertDnList.append(CertDn)
            else:
                flag=True
        return CertDnList,flag,strPin
             
    def genCert_with_RSA2048_Comm_P(self,initPinFlag=True,clearDnFlag=False,RequestDN=CertListInfoMap["RSA2048_Comm_p"],strPin=str_srcPin):
        CertDnList=[]
        flag=False           
        result=self.genCert(RequestDN,strPin,initPinFlag,clearDnFlag)
        if True == operator.eq(write_cert_str,result[0]):
            #验证
            strPin=result[1]
            cur_url=self.CtrlObj.browser.current_url 
            if 0 <= cur_url.find(testUrl_GM_User):
                CertDn=self.CtrlObj.get_GMCertDN()
                if 0 == CertDn.count("||"):
                    flag=self.certVerify(RequestDN,CertDn)
                    CertDnList.append(CertDn)
            else:
                flag=True
        return CertDnList,flag,strPin
     
    def genCert_with_RSA2048_Comm_C(self,initPinFlag=True,clearDnFlag=False,RequestDN=CertListInfoMap["RSA2048_Comm_c"],strPin=str_srcPin):
        CertDnList=[]
        flag=False           
        result=self.genCert(RequestDN,strPin,initPinFlag,clearDnFlag)
        if True == operator.eq(write_cert_str,result[0]):
            #验证
            strPin=result[1]
            cur_url=self.CtrlObj.browser.current_url 
            if 0 <= cur_url.find(testUrl_GM_User):
                CertDn=self.CtrlObj.get_GMCertDN()
                if 0 == CertDn.count("||"):
                    flag=self.certVerify(RequestDN,CertDn)
                    CertDnList.append(CertDn)
            else:
                flag=True
        return CertDnList,flag,strPin
                   
    def genCert_with_SM2_Sign_P(self,initPinFlag=True,clearDnFlag=False,RequestDN=CertListInfoMap["SM2256_Sig2_p"],strPin=str_srcPin):
        CertDnList=[]
        flag=False           
        result=self.genCert(RequestDN,strPin,initPinFlag,clearDnFlag)
        if True == operator.eq(write_cert_str,result[0]):
            #验证
            strPin=result[1]
            cur_url=self.CtrlObj.browser.current_url 
            if 0 <= cur_url.find(testUrl_GM_User):
                CertDn=self.CtrlObj.get_GMCertDN()
                if 0 == CertDn.count("||"):
                    flag=self.certVerify(RequestDN,CertDn)
                    CertDnList.append(CertDn)
            else:
                flag=True
        return CertDnList,flag,strPin
      
    def genCert_with_SM2_Sign_C(self,initPinFlag=True,clearDnFlag=False,RequestDN=CertListInfoMap["SM2256_Sig2_c"],strPin=str_srcPin):
        CertDnList=[]
        flag=False           
        result=self.genCert(RequestDN,strPin,initPinFlag,clearDnFlag)
        if True == operator.eq(write_cert_str,result[0]):
            #验证
            strPin=result[1]
            cur_url=self.CtrlObj.browser.current_url 
            if 0 <= cur_url.find(testUrl_GM_User):
                CertDn=self.CtrlObj.get_GMCertDN()
                if 0 == CertDn.count("||"):
                    flag=self.certVerify(RequestDN,CertDn)
                    CertDnList.append(CertDn)
            else:
                flag=True
        return CertDnList,flag,strPin
    
    def genCert_with_SM2_Comm_P(self,initPinFlag=True,clearDnFlag=False,RequestDN=CertListInfoMap["SM2256_Comm_p"],strPin=str_srcPin):
        CertDnList=[]
        flag=False           
        result=self.genCert(RequestDN,strPin,initPinFlag,clearDnFlag)
        if True == operator.eq(write_cert_str,result[0]):
            #验证
            strPin=result[1]
            cur_url=self.CtrlObj.browser.current_url 
            if 0 <= cur_url.find(testUrl_GM_User):
                CertDn=self.CtrlObj.get_GMCertDN()
                if 0 == CertDn.count("||"):
                    flag=self.certVerify(RequestDN,CertDn)
                    CertDnList.append(CertDn)
            else:
                flag=True
        return CertDnList,flag,strPin
      
    def genCert_with_SM2_Comm_C(self,initPinFlag=True,clearDnFlag=False,RequestDN=CertListInfoMap["SM2256_Comm_c"],strPin=str_srcPin):
        CertDnList=[]
        flag=False           
        result=self.genCert(RequestDN,strPin,initPinFlag,clearDnFlag)
        if True == operator.eq(write_cert_str,result[0]):
            #验证
            strPin=result[1]
            cur_url=self.CtrlObj.browser.current_url 
            if 0 <= cur_url.find(testUrl_GM_User):
                CertDn=self.CtrlObj.get_GMCertDN()
                if 0 == CertDn.count("||"):
                    flag=self.certVerify(RequestDN,CertDn)
                    CertDnList.append(CertDn)
            else:
                flag=True
        return CertDnList,flag,strPin
        
    def genCert_with_rsa1024M_and_sm2Sp(self,initPinFlag=True,clearDnFlag=False,RequestDN=CertListInfoMap["RSA1024_M_and_SM2256_S(p)"],strPin=str_srcPin):
        CertDnList=[]
        flag=False
        result=self.genCert(RequestDN,strPin,initPinFlag,clearDnFlag)
        if True == operator.eq(write_cert_str,result[0]):
            #验证
            strPin=result[1]
            cur_url=self.CtrlObj.browser.current_url 
            if 0 <= cur_url.find(testUrl_GM_User):
                CertDn=self.CtrlObj.get_GMCertDN()
                if 0 < CertDn.count("||"):
                    flag=self.certVerify(RequestDN,CertDn)
                    CertDnList.append(CertDn)
            else:
                flag=True
                    
        return CertDnList,flag,strPin
    
    def genCert_with_rsa1024M_and_sm2Sc(self,initPinFlag=True,clearDnFlag=False,RequestDN=CertListInfoMap["RSA1024_M_and_SM2256_S(c)"],strPin=str_srcPin):
        CertDnList=[]
        flag=False
        result=self.genCert(RequestDN,strPin,initPinFlag,clearDnFlag)
        if True == operator.eq(write_cert_str,result[0]):
            #验证
            strPin=result[1]
            cur_url=self.CtrlObj.browser.current_url 
            if 0 <= cur_url.find(testUrl_GM_User):
                CertDn=self.CtrlObj.get_GMCertDN()
                if 0 < CertDn.count("||"):
                    flag=self.certVerify(RequestDN,CertDn)
                    CertDnList.append(CertDn)
            else:
                flag=True
        return CertDnList,flag,strPin
    
    def genCert_with_rsa1024Cp_and_sm2Sp(self,initPinFlag=True,clearDnFlag=False,RequestDN=CertListInfoMap["RSA1024_C(p)_and_SM2256_S(p)"],strPin=str_srcPin):
        CertDnList=[]
        flag=False
        result=self.genCert(RequestDN,strPin,initPinFlag,clearDnFlag)
        if True == operator.eq(write_cert_str,result[0]):
            #验证
            strPin=result[1]
            cur_url=self.CtrlObj.browser.current_url 
            if 0 <= cur_url.find(testUrl_GM_User):
                CertDn=self.CtrlObj.get_GMCertDN()
                if 0 < CertDn.count("||"):
                    flag=self.certVerify(RequestDN,CertDn)
                    CertDnList.append(CertDn)
            else:
                flag=True
        return CertDnList,flag,strPin
                
    def genCert_with_rsa1024Cc_and_sm2Sc(self,initPinFlag=True,clearDnFlag=False,RequestDN=CertListInfoMap["RSA1024_C(c)_and_SM2256_S(c)"],strPin=str_srcPin):
        CertDnList=[]
        flag=False
        result=self.genCert(RequestDN,strPin,initPinFlag,clearDnFlag)
        if True == operator.eq(write_cert_str,result[0]):
            #验证
            strPin=result[1]
            cur_url=self.CtrlObj.browser.current_url 
            if 0 <= cur_url.find(testUrl_GM_User):
                CertDn=self.CtrlObj.get_GMCertDN()
                if 0 < CertDn.count("||"):
                    flag=self.certVerify(RequestDN,CertDn)
                    CertDnList.append(CertDn)
            else:
                flag=True
        return CertDnList,flag,strPin

    def genCert_with_rsa2048M_and_sm2Sp(self,initPinFlag=True,clearDnFlag=False,RequestDN=CertListInfoMap["RSA2048_M_and_SM2256_S(p)"],strPin=str_srcPin):
        CertDnList=[]
        flag=False
        result=self.genCert(RequestDN,strPin,initPinFlag,clearDnFlag)
        if True == operator.eq(write_cert_str,result[0]):
            #验证
            strPin=result[1]
            cur_url=self.CtrlObj.browser.current_url
            if 0 <= cur_url.find(testUrl_GM_User):
                CertDn=self.CtrlObj.get_GMCertDN()
                if 0 < CertDn.count("||"):
                    flag=self.certVerify(RequestDN,CertDn)
                    CertDnList.append(CertDn)
            else:
                flag=True
        return CertDnList,flag,strPin
    
    def genCert_with_rsa2048M_and_sm2Sc(self,initPinFlag=True,clearDnFlag=False,RequestDN=CertListInfoMap["RSA2048_M_and_SM2256_S(c)"],strPin=str_srcPin):
        CertDnList=[]
        flag=False
        result=self.genCert(RequestDN,strPin,initPinFlag,clearDnFlag)
        if True == operator.eq(write_cert_str,result[0]):
            #验证
            strPin=result[1]
            cur_url=self.CtrlObj.browser.current_url 
            if 0 <= cur_url.find(testUrl_GM_User):
                CertDn=self.CtrlObj.get_GMCertDN()
                if 0 < CertDn.count("||"):
                    flag=self.certVerify(RequestDN,CertDn)
                    CertDnList.append(CertDn)
            else:
                flag=True
        logger.warning(CertDnList)
        return CertDnList,flag,strPin

    def genCert_with_rsa2048Cp_and_sm2Sp(self,initPinFlag=True,clearDnFlag=False,RequestDN=CertListInfoMap["RSA2048_C(p)_and_SM2256_S(p)"],strPin=str_srcPin):
        CertDnList=[]
        flag=False
        result=self.genCert(RequestDN,strPin,initPinFlag,clearDnFlag)
        if True == operator.eq(write_cert_str,result[0]):
            #验证
            strPin=result[1]
            cur_url=self.CtrlObj.browser.current_url 
            if 0 <= cur_url.find(testUrl_GM_User):
                CertDn=self.CtrlObj.get_GMCertDN()
                if 0 < CertDn.count("||"):
                    flag=self.certVerify(RequestDN,CertDn)
                    CertDnList.append(CertDn)
            else:
                flag=True
        return CertDnList,flag,strPin
                
    def genCert_with_rsa2048Cc_and_sm2Sc(self,initPinFlag=True,clearDnFlag=False,RequestDN=CertListInfoMap["RSA2048_C(c)_and_SM2256_S(c)"],strPin=str_srcPin):
        CertDnList=[]
        flag=False
        result=self.genCert(RequestDN,strPin,initPinFlag,clearDnFlag)
        if True == operator.eq(write_cert_str,result[0]):
            #验证
            strPin=result[1]
            cur_url=self.CtrlObj.browser.current_url 
            if 0 <= cur_url.find(testUrl_GM_User):
                CertDn=self.CtrlObj.get_GMCertDN()
                if 0 < CertDn.count("||"):
                    flag=self.certVerify(RequestDN,CertDn)
                    CertDnList.append(CertDn)
            else:
                flag=True
        return CertDnList,flag,strPin
             
    def genCert_with_rsa2048Cp_and_rsa2048M(self,initPinFlag=True,clearDnFlag=False,RequestDN=CertListInfoMap["RSA2048_C(p)_and_RSA2048_M"],strPin=str_srcPin):
        CertDnList=[]
        flag=False
        result=self.genCert(RequestDN,strPin,initPinFlag,clearDnFlag)
        if True == operator.eq(write_cert_str,result[0]):
            #验证
            strPin=result[1]
            cur_url=self.CtrlObj.browser.current_url 
            if 0 <= cur_url.find(testUrl_GM_User):
                CertDn=self.CtrlObj.get_GMCertDN()
                if 0 < CertDn.count("||"):
                    flag=self.certVerify(RequestDN,CertDn)
                    CertDnList.append(CertDn)
            else:
                flag=True
        return CertDnList,flag,strPin
    
    def genCert_with_rsa2048Cc_and_rsa2048M(self,initPinFlag=True,clearDnFlag=False,RequestDN=CertListInfoMap["RSA2048_C(c)_and_RSA2048_M"],strPin=str_srcPin):
        CertDnList=[]
        flag=False
        result=self.genCert(RequestDN,strPin,initPinFlag,clearDnFlag)
        if True == operator.eq(write_cert_str,result[0]):
            #验证
            strPin=result[1]
            CertDn=self.CtrlObj.get_GMCertDN()
            if  0 < CertDn.count("||"):
                flag=self.certVerify(RequestDN,CertDn)
                CertDnList=CertDn.split("||")
        return CertDnList,flag,strPin

    def genCert_with_rsa1024Cp_and_rsa2048Cp(self,initPinFlag=True,clearDnFlag=False,RequestDN=CertListInfoMap["RSA1024_C(p)_and_RSA2048_C(p)"],strPin=str_srcPin):
        CertDnList=[]
        flag=False
        result=self.genCert(RequestDN,strPin,initPinFlag,clearDnFlag)
        if True == operator.eq(write_cert_str,result[0]):
            #验证
            strPin=result[1]
            cur_url=self.CtrlObj.browser.current_url 
            if 0 <= cur_url.find(testUrl_GM_User):
                CertDn=self.CtrlObj.get_GMCertDN()
                if 0 < CertDn.count("||"):
                    flag=self.certVerify(RequestDN,CertDn)
                    CertDnList.append(CertDn)
            else:
                flag=True
        return CertDnList,flag,strPin
    
    def genCert_with_rsa1024Cp_and_rsa2048M(self,initPinFlag=True,clearDnFlag=False,RequestDN=CertListInfoMap["RSA1024_C(p)_and_RSA2048_M"],strPin=str_srcPin):
        CertDnList=[]
        flag=False
        result=self.genCert(RequestDN,strPin,initPinFlag,clearDnFlag)
        if True == operator.eq(write_cert_str,result[0]):
            #验证
            strPin=result[1]
            cur_url=self.CtrlObj.browser.current_url 
            if 0 <= cur_url.find(testUrl_GM_User):
                CertDn=self.CtrlObj.get_GMCertDN()
                if 0 < CertDn.count("||"):
                    flag=self.certVerify(RequestDN,CertDn)
                    CertDnList.append(CertDn)
            else:
                flag=True
        return CertDnList,flag,strPin
    
    def genCert_with_rsa1024Cc_and_rsa2048M(self,initPinFlag=True,clearDnFlag=False,RequestDN=CertListInfoMap["RSA1024_C(c)_and_RSA2048_M"],strPin=str_srcPin):
        CertDnList=[]
        flag=False
        result=self.genCert(RequestDN,strPin,initPinFlag,clearDnFlag)
        if True == operator.eq(write_cert_str,result[0]):
            #验证
            strPin=result[1]
            cur_url=self.CtrlObj.browser.current_url 
            if 0 <= cur_url.find(testUrl_GM_User):
                CertDn=self.CtrlObj.get_GMCertDN()
                if 0 < CertDn.count("||"):
                    flag=self.certVerify(RequestDN,CertDn)
                    CertDnList.append(CertDn)
            else:
                flag=True
        return CertDnList,flag,strPin
    
    def genCert_with_rsa1024M_and_rsa1024M(self,initPinFlag=True,clearDnFlag=False,RequestDN=CertListInfoMap["RSA1024_M_and_RSA1024_M"],strPin=str_srcPin):
        CertDnList=[]
        flag=False
        result=self.genCert(RequestDN,strPin,initPinFlag,clearDnFlag)
        if True == operator.eq(write_cert_str,result[0]):
            #验证
            strPin=result[1]
            cur_url=self.CtrlObj.browser.current_url 
            if 0 <= cur_url.find(testUrl_GM_User):
                CertDn=self.CtrlObj.get_GMCertDN()
                if 0 < CertDn.count("||"):
                    flag=self.certVerify(RequestDN,CertDn)
                    CertDnList.append(CertDn)
            else:
                flag=True
        return CertDnList,flag,strPin
    
    def genCert_with_rsa2048M_and_rsa2048M(self,initPinFlag=True,clearDnFlag=False,RequestDN=CertListInfoMap["RSA2048_M_and_RSA2048_M"],strPin=str_srcPin):
        CertDnList=[]
        flag=False
        result=self.genCert(RequestDN,strPin,initPinFlag,clearDnFlag)
        if True == operator.eq(write_cert_str,result[0]):
            #验证
            strPin=result[1]
            cur_url=self.CtrlObj.browser.current_url 
            if 0 <= cur_url.find(testUrl_GM_User):
                CertDn=self.CtrlObj.get_GMCertDN()
                if 0 < CertDn.count("||"):
                    flag=self.certVerify(RequestDN,CertDn)
                    CertDnList.append(CertDn)
            else:
                flag=True
        return CertDnList,flag,strPin

    def genCert_with_rsa1024M_and_rsa2048M(self,initPinFlag=True,clearDnFlag=False,RequestDN=CertListInfoMap["RSA1024_M_and_RSA2048_M"],strPin=str_srcPin):
        CertDnList=[]
        flag=False
        result=self.genCert(RequestDN,strPin,initPinFlag,clearDnFlag)
        if True == operator.eq(write_cert_str,result[0]):
            #验证
            strPin=result[1]
            cur_url=self.CtrlObj.browser.current_url 
            if 0 <= cur_url.find(testUrl_GM_User):
                CertDn=self.CtrlObj.get_GMCertDN()
                if 0 < CertDn.count("||"):
                    flag=self.certVerify(RequestDN,CertDn)
                    CertDnList.append(CertDn)
            else:
                flag=True
        return CertDnList,flag,strPin

    def genCert_with_SM2256C_and_SM2256S(self,initPinFlag=True,clearDnFlag=False,RequestDN=CertListInfoMap["SM2256_C(p)_and_SM2256_S(p)"],strPin=str_srcPin):
        CertDnList=[]
        flag=False
        result=self.genCert(RequestDN,strPin,initPinFlag,clearDnFlag)
        if True == operator.eq(write_cert_str,result[0]):
            #验证
            strPin=result[1]
            cur_url=self.CtrlObj.browser.current_url 
            if 0 <= cur_url.find(testUrl_GM_User):
                CertDn=self.CtrlObj.get_GMCertDN()
                if 0 < CertDn.count("||"):
                    flag=self.certVerify(RequestDN,CertDn)
                    CertDnList.append(CertDn)
            else:
                flag=True
        return CertDnList,flag,strPin


    def genCert_with_rsa1024C_and_rsa2048M_andSM2256S(self,initPinFlag=True,clearDnFlag=False,RequestDN=CertListInfoMap["RSA1024_C(p)_and_RSA2048_M_and_SM2256_S(p)"],strPin=str_srcPin):
        CertDnList=[]
        flag=False
        result=self.genCert(RequestDN,strPin,initPinFlag,clearDnFlag)
        if True == operator.eq(write_cert_str,result[0]):
            #验证
            strPin=result[1]
            cur_url=self.CtrlObj.browser.current_url 
            if 0 <= cur_url.find(testUrl_GM_User):
                CertDn=self.CtrlObj.get_GMCertDN()
                if 0 < CertDn.count("||"):
                    flag=self.certVerify(RequestDN,CertDn)
                    CertDnList.append(CertDn)
            else:
                flag=True
        return CertDnList,flag,strPin
       
#########################
#开始测试
#########################
 
if __name__ == '__main__':
    ctrlObj = TestIcbcGmUserkey.TestIcbcGmUser(testUrl_GM_User)
    ctrlObj.open()
    AdminKeyList = ['True', '00', '00']
    gcTest=GenCertClass(ctrlObj,AdminKeyList)  #建立类对象，打开控件测试页
    strPin = str_srcPin
    #print(strPin)
    #gcTest.init_key(strPin, strPin)
    #print(strPin)
    #gcTest.genCert(CertListInfoMap["RSA1024_Mixed"],strPin,initPinFlag=True)
    #RequestDN="DN(CN=TestRSA1024.p.0200.0102,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA1024)CERTTYPE(01)||DN(CN=TestRSA2048.p.0200.0102,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA2048)CERTTYPE(01)"
    #ctrlObj.open()
    #gcTest.genKeyPair(CertListInfoMap["RSA1024_Mixed"], str_srcPin,True)
    #gcTest.genKeyPair(CertListInfoMap["RSA2048_Mixed"], str_srcPin,False)
    #result=gcTest.clearCertAndKeyPairs()
    #result=gcTest.genCert(CertListInfoMap["RSA1024_Mixed"], str_srcPin,False,True)   #测试用例集，根据测试范围定义测试强度
    result=gcTest.genCert_with_RSA2048_Mix(False,True)   #测试用例集，根据测试范围定义测试强度
    gcTest.CtrlObj.close()
 
