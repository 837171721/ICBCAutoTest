#coding=utf-8
'''
Created on 2018.1.23

@author: ys

'''
import ctypes
import base64
import os
import string
import time
import logging
class MyGlobal:
    def __init__(self):
        self.TestingRange = 4    #测试强度,全局变量
        self.UKey = 0            #U盾类型：0-其他盾，1-指纹盾
GL = MyGlobal() 

#获取工程相关路径

proPath=(os.path.abspath(os.path.join(os.getcwd(), "../../..")))
proPath=proPath+"\\Import\\"
browserPath=proPath+"IE\\"

# 操作系统位数                             
OSNum=64            #----------------每次都需要配置

#测试强度： 0:详细 ， 1：验证    2：无Key测试 3：多Key测试  4:基本测试
TestingRange = 1    #----------------每次都需要配置

#控件信息
DriverVer = "2.5.0.11"          #----------------根据测试驱动进行配置
CtrlVer ="1.1.0.0"              #----------------根据控件版本进行配置
CSPVer="M&W CSP for ICBC V5"
#管理工具信息
manage_tool_title = 'U盾客户端管理工具（明华&文鼎创）'
if 64 == OSNum:
    open_path = 'C:\\Program Files (x86)\\ICBCEbankTools\\MingWah\\MWICBCUKeyToolU.exe'
#硬件信息
CardNum = "6900006385"
testUrl_GM_User_Title="明华澳汉控件测试"
testUrl_GM_Manage_Title="明华澳汉管理员控件测试"

if 64 == OSNum:
    # Str_IEServerDrive="C:\\Program Files\\Internet Explorer\\IEDriverServer.exe"
    Str_IEServerDrive = "D:\\python\\IEDriverServer.exe"
    testUrl_GM_User     = browserPath+"Test_GM_Icbc_Usbkey_64.htm"
    testUrl_GM_Manage   = browserPath+"Test_GM_Icbc_Manage_64.htm"
    testUrl_User        = browserPath+"Testicbcmwusbkey_64.htm"
    testUrl_Manage      = browserPath+"Testicbcmwmanage_64.htm"
else:
    path="C:\\Program Files (x86)\\Internet Explorer"
    # Str_IEServerDrive="C:\\Program Files (x86)\\Internet Explorer\\IEDriverServer.exe"
    Str_IEServerDrive = "D:\\python\\IEDriverServer.exe"
    if not os.path.exists(path):
        Str_IEServerDrive="C:\\Program Files\\Internet Explorer\\IEDriverServer.exe"  

    testUrl_GM_User     = browserPath+"Test_GM_Icbc_Usbkey.htm"
    testUrl_GM_Manage   = browserPath+"Test_GM_Icbc_Manage.htm"
    testUrl_User        = browserPath+"Testicbcmwusbkey.htm"
    testUrl_Manage      = browserPath+"Testicbcmwmanage.htm"
    
# 测试控件页   testUrl_GM_User/testUrl_GM_Manage/testUrl_User/testUrl_Manage
main_url=  testUrl_GM_User         #----------------每次都需要配置
   
#系统语言
languageType = 0 # 0:中文          1:繁体        2:英文                          #---------------每次都需要配置
if languageType == 0:
    str_title='输入密码'
    str_changeTitle='修改U盾密码'
    str_verifyTitle='用户提示'
    str_signTitle='请核对签名信息'
elif languageType == 1:
    str_title='輸入密碼'
    str_changeTitle='修改U盾密碼'
    str_verifyTitle='用戶提示'
    str_signTitle='請核對簽名信息'
elif languageType == 2: 
    str_title='Input Password'
    str_changeTitle='Change USB-Shield Password'
    str_verifyTitle='User Tips'
    str_signTitle = 'Verify Critical Information'
    
#日志写入方式
substr=main_url[main_url.rfind("\\",0,len(main_url))+1 : main_url.rfind(".",0,len(main_url))]
systime = time.strftime("%Y%m%d%H%M%S_", time.localtime(time.time()))
report_path=(os.path.abspath(os.path.join(os.getcwd())))+"\\Logs\\"
if not os.path.exists(report_path):
    os.makedirs(report_path)           #获取此py文件路径，在此路径上创建Logs文件夹
    
#日志名称
log_file=report_path+systime+substr+".log"  #日志名称      
log_level = "info"              #日志级别
log_max_byte = 100 * 1024 * 1024 #日志文件大小/个
log_backup_count = 5             #日志文件数目

levels = {      
 "notset" : logging.NOTSET,
 "debug" : logging.DEBUG,
 "info" : logging.INFO,
 "warn" : logging.WARN,
 "error" : logging.ERROR,
 "critical" : logging.CRITICAL}

#文件签名
filepath=proPath+"FileSignInfo\\"
p7FilePath = filepath+"file000.txt"
batFilePath = filepath+"file1K.txt"
batFilePath1K = filepath+"file1K.txt"
batFilePath2K = filepath+"file2K.txt"
batFilePath5K = filepath+"file5K.txt"
batFilePath10K = filepath+"file10K.txt"
batFilePath1M  = filepath+"file1M.txt"
batFilePath5M  = filepath+"file5M.txt"
batFilePath10M  = filepath+"file10M.txt"
batFilePath50M  = filepath+"file50M.txt"
batFilePath90M  = filepath+"file90M.txt"
batFilePath100M  = filepath+"file100M.txt"


#中间工具
midToolPath =proPath+"ExpressTools\\"
AuxTool     = midToolPath+"IcbcOcxAuxTool_rls.exe"
#AutoItExe   = midToolPath+"p10转成p7.exe"

#变量信息
str_srcPin='1q1q1q1q'
str_defaultPin='12345678'
str_verifyPin='12345678'
hashId='SHA1' 
defaultServerRand=""
xmlInfo=r'<?xml version="1.0" encoding="gb2312"?><TradeData><field name="付款人姓名" value="明华公司" DisplayOnScreen="TRUE"/><field name="付款卡号" value="95588202000088888888" DisplayOnScreen="TRUE"/><field name="收款人姓名" value="刘伟伟" DisplayOnScreen="TRUE"/><field name="收款帐号" value="95588202000099999999" DisplayOnScreen="TRUE"/><field name="收款人所在地" value="北京" DisplayOnScreen="TRUE"/><field name="收款人所在网点机构" value="九龙山支行 " DisplayOnScreen="TRUE"/><field name="手续费" value="0" DisplayOnScreen="TRUE"/><field name="总金额" value="100000.00" DisplayOnScreen="TRUE"/><field name="交易提交时间" value="20100402171706" DisplayOnScreen="TRUE"/></TradeData>'    
dispInfo='收款帐号:9558820200009991111111111\n总金额:100000.00RMB手续费:0\n交易提交时间:20100402171706'
DN_info_Temp="DN(CN=TestRSA1024,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA1024)CERTTYPE(02)"
xmlInfoFile=r'E:\myJobLog\TestRecord\AutoTest\ICBCTest\HTMLTestFile\ExpressTools\\xmlInfo.txt'    
AmdinKey_3DES='569C9E50BD52FE9C626261EB7E3382C4' 
AmdinKey_SM4='AAFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'  
AmdinKey_AES_old='FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'
AmdinKey_AES_new='AAFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'
str_Base64Data='1DdS5cZN8BYWb1YYx1en'

#证书信息列表
CertListInfoMap = {
    "RSA1024_Mixed":          "DN(CN=TestRSA1024,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA1024)CERTTYPE(02)",
    "RSA2048_Mixed":          "DN(CN=TestRSA2048,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA2048)CERTTYPE(02)",

    "RSA1024_Sig2_p":         "DN(CN=TestRSA1024.p.0200.0102,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA1024)CERTTYPE(01)",
    "RSA2048_Sig2_p":         "DN(CN=TestRSA2048.p.0200.0102,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA1024)CERTTYPE(01)",
    "SM2256_Sig2_p":          "DN(CN=TestSM2.p.0200.0101,O=rsaperca139.com.cn)HASH(SM3)KEYTYPE(SM2256)CERTTYPE(01)",   
    "RSA1024_Sig2_c":         "DN(CN=TestRSA1024.c.0200.0102,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA1024)CERTTYPE(01)",
    "RSA2048_Sig2_c":         "DN(CN=TestRSA2048.c.0200.0102,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA1024)CERTTYPE(01)",
    "SM2256_Sig2_c":          "DN(CN=TestSM2.c.0200.0101,O=rsaperca139.com.cn)HASH(SM3)KEYTYPE(SM2256)CERTTYPE(01)",    

    "RSA1024_Comm_p":         "DN(CN=TestRSA1024.p.0200.0202,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA1024)CERTTYPE(03)",
    "RSA2048_Comm_p":         "DN(CN=TestRSA2048.p.0200.0202,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA1024)CERTTYPE(03)",
    "SM2256_Comm_p":          "DN(CN=TestSM2.p.0200.0201,O=rsaperca139.com.cn)HASH(SM3)KEYTYPE(SM2256)CERTTYPE(03)",   
    "RSA1024_Comm_c":         "DN(CN=TestRSA1024.c.0200.0202,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA1024)CERTTYPE(03)",
    "RSA2048_Comm_c":         "DN(CN=TestRSA2048.c.0200.0202,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA2048)CERTTYPE(03)",
    "SM2256_Comm_c":          "DN(CN=TestSM2.c.0200.0201,O=rsaperca139.com.cn)HASH(SM3)KEYTYPE(SM2256)CERTTYPE(03)",    

    "RSA2048_M_and_SM2256_S(p)": "DN(CN=TestRSA2048,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA2048)CERTTYPE(02)||DN(CN=TestSM2.p.0200.0101,O=rsaperca139.com.cn)HASH(SM3)KEYTYPE(SM2256)CERTTYPE(01)",
    "RSA1024_M_and_SM2256_S(p)": "DN(CN=TestRSA1024,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA1024)CERTTYPE(02)||DN(CN=TestSM2.p.0200.0101,O=rsaperca139.com.cn)HASH(SM3)KEYTYPE(SM2256)CERTTYPE(01)",
    "RSA2048_M_and_SM2256_S(c)": "DN(CN=TestRSA2048,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA2048)CERTTYPE(02)||DN(CN=TestSM2.c.0200.0101,O=rsaperca139.com.cn)HASH(SM3)KEYTYPE(SM2256)CERTTYPE(01)",
    "RSA1024_M_and_SM2256_S(c)": "DN(CN=TestRSA1024,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA1024)CERTTYPE(02)||DN(CN=TestSM2.c.0200.0101,O=rsaperca139.com.cn)HASH(SM3)KEYTYPE(SM2256)CERTTYPE(01)",

    "RSA2048_C(p)_and_SM2256_S(p)": "DN(CN=TestRSA2048.p.0200.0202,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA2048)CERTTYPE(03)||DN(CN=TestSM2.p.0200.0101,O=rsaperca139.com.cn)HASH(SM3)KEYTYPE(SM2256)CERTTYPE(01)",
    "RSA1024_C(p)_and_SM2256_S(p)": "DN(CN=TestRSA1024.p.0200.0202,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA1024)CERTTYPE(03)||DN(CN=TestSM2.p.0200.0101,O=rsaperca139.com.cn)HASH(SM3)KEYTYPE(SM2256)CERTTYPE(01)",
    "RSA2048_C(c)_and_SM2256_S(c)": "DN(CN=TestRSA2048.c.0200.0202,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA2048)CERTTYPE(03)||DN(CN=TestSM2.c.0200.0101,O=rsaperca139.com.cn)HASH(SM3)KEYTYPE(SM2256)CERTTYPE(01)",
    "RSA1024_C(c)_and_SM2256_S(c)": "DN(CN=TestRSA1024.c.0200.0202,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA1024)CERTTYPE(03)||DN(CN=TestSM2.c.0200.0101,O=rsaperca139.com.cn)HASH(SM3)KEYTYPE(SM2256)CERTTYPE(01)",
    
    "RSA2048_C(p)_and_RSA2048_M": "DN(CN=TestRSA2048.p.0200.0202,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA2048)CERTTYPE(03)||DN(CN=TestRSA2048,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA2048)CERTTYPE(02)",
    "RSA2048_C(c)_and_RSA2048_M": "DN(CN=TestRSA2048.c.0200.0202,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA2048)CERTTYPE(03)||DN(CN=TestRSA2048,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA2048)CERTTYPE(02)", 
    "RSA1024_C(p)_and_RSA2048_M": "DN(CN=TestRSA1024.p.0200.0202,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA1024)CERTTYPE(03)||DN(CN=TestRSA2048,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA2048)CERTTYPE(02)",
    "RSA1024_C(c)_and_RSA2048_M": "DN(CN=TestRSA1024.c.0200.0202,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA1024)CERTTYPE(03)||DN(CN=TestRSA2048,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA2048)CERTTYPE(02)",
    "RSA1024_M_and_RSA2048_M":    "DN(CN=TestRSA1024,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA1024)CERTTYPE(02)||DN(CN=TestRSA2048,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA2048)CERTTYPE(02)",
    "RSA1024_C(p)_and_RSA2048_C(p)": "DN(CN=TestRSA1024.p.0200.0202,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA1024)CERTTYPE(03)||DN(CN=TestRSA2048.p.0200.0202,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA1024)CERTTYPE(03)",

    "SM2256_C(p)_and_SM2256_S(p)":"DN(CN=TestSM2.p.0200.0201,O=rsaperca139.com.cn)HASH(SM3)KEYTYPE(SM2256)CERTTYPE(03)||DN(CN=TestSM2.p.0200.0101,O=rsaperca139.com.cn)HASH(SM3)KEYTYPE(SM2256)CERTTYPE(01)",
    "SM2256_C(c)_and_SM2256_S(p)":"DN(CN=TestSM2.c.0200.0201,O=rsaperca139.com.cn)HASH(SM3)KEYTYPE(SM2256)CERTTYPE(03)||DN(CN=TestSM2.p.0200.0101,O=rsaperca139.com.cn)HASH(SM3)KEYTYPE(SM2256)CERTTYPE(01)",


    "RSA1024_C(p)_and_RSA2048_M_and_SM2256_S(p)":    "DN(CN=TestRSA1024.p.0200.0202,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA1024)CERTTYPE(03)||DN(CN=TestRSA2048,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA2048)CERTTYPE(02)||DN(CN=TestSM2.p.0200.0101,O=rsaperca139.com.cn)HASH(SM3)KEYTYPE(SM2256)CERTTYPE(01)",

    #同DN
    "RSA1024_M_and_RSA1024_M":      "DN(CN=TestRSA1024,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA1024)CERTTYPE(02)||DN(CN=TestRSA1024,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA1024)CERTTYPE(02)",
    "RSA2048_M_and_RSA2048_M":      "DN(CN=TestRSA2048,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA2048)CERTTYPE(02)||DN(CN=TestRSA2048,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA2048)CERTTYPE(02)",
    "SM2256_Sig2_and SM2256_Sig2":  "DN(CN=TestSM2.p.0200.0101,O=rsaperca139.com.cn)HASH(SM3)KEYTYPE(SM2256)CERTTYPE(01)||DN(CN=TestSM2.p.0200.0101,O=rsaperca139.com.cn)HASH(SM3)KEYTYPE(SM2256)CERTTYPE(01)",   
    
    
    #哈希遍历
    "RSA1024_Mixed_sha1":     "DN(CN=TestRSA1024,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA1024)CERTTYPE(02)",    
    "RSA1024_Mixed_sha256":   "DN(CN=TestRSA1024,O=rsaperca139.com.cn)HASH(SHA256)KEYTYPE(RSA1024)CERTTYPE(02)",
    "RSA1024_Mixed_sha384":   "DN(CN=TestRSA1024,O=rsaperca139.com.cn)HASH(SHA384)KEYTYPE(RSA1024)CERTTYPE(02)",
    "RSA1024_Mixed_sha512":   "DN(CN=TestRSA1024,O=rsaperca139.com.cn)HASH(SHA512)KEYTYPE(RSA1024)CERTTYPE(02)",
    
    "RSA2048_Mixed_sha1":     "DN(CN=TestRSA2048,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA2048)CERTTYPE(02)",   
    "RSA2048_Mixed_sha256":   "DN(CN=TestRSA2048,O=rsaperca139.com.cn)HASH(SHA256)KEYTYPE(RSA2048)CERTTYPE(02)",
    "RSA2048_Mixed_sha384":   "DN(CN=TestRSA2048,O=rsaperca139.com.cn)HASH(SHA384)KEYTYPE(RSA2048)CERTTYPE(02)",
    "RSA2048_Mixed_sha512":   "DN(CN=TestRSA2048,O=rsaperca139.com.cn)HASH(SHA512)KEYTYPE(RSA2048)CERTTYPE(02)",

    "RSA1024_Sig2_p_sha1":     "DN(CN=TestRSA1024.p.0200.0102,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA1024)CERTTYPE(01)",    
    "RSA1024_Sig2_p_sha256":   "DN(CN=TestRSA1024.p.0200.0102,O=rsaperca139.com.cn)HASH(SHA256)KEYTYPE(RSA1024)CERTTYPE(01)",
    "RSA1024_Sig2_p_sha384":   "DN(CN=TestRSA1024.p.0200.0102,O=rsaperca139.com.cn)HASH(SHA384)KEYTYPE(RSA1024)CERTTYPE(01)",
    "RSA1024_Sig2_p_sha512":   "DN(CN=TestRSA1024.p.0200.0102,O=rsaperca139.com.cn)HASH(SHA512)KEYTYPE(RSA1024)CERTTYPE(01)",

    "RSA2048_Sig2_p_sha1":     "DN(CN=TestRSA2048.p.0200.0102,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA1024)CERTTYPE(01)",    
    "RSA2048_Sig2_p_sha256":   "DN(CN=TestRSA2048.p.0200.0102,O=rsaperca139.com.cn)HASH(SHA256)KEYTYPE(RSA1024)CERTTYPE(01)",
    "RSA2048_Sig2_p_sha384":   "DN(CN=TestRSA2048.p.0200.0102,O=rsaperca139.com.cn)HASH(SHA384)KEYTYPE(RSA1024)CERTTYPE(01)",
    "RSA2048_Sig2_p_sha512":   "DN(CN=TestRSA2048.p.0200.0102,O=rsaperca139.com.cn)HASH(SHA512)KEYTYPE(RSA1024)CERTTYPE(01)",
 
    "SM2256_Sig2_p_sm3":       "DN(CN=TestSM2.p.0200.0101,O=rsaperca139.com.cn)HASH(SM3)KEYTYPE(SM2256)CERTTYPE(01)",   


    "RSA1024_Comm_p_sha1":     "DN(CN=TestRSA1024.p.0200.0202,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA1024)CERTTYPE(03)",
    "RSA1024_Comm_p_sha256":   "DN(CN=TestRSA1024.p.0200.0202,O=rsaperca139.com.cn)HASH(SHA256)KEYTYPE(RSA1024)CERTTYPE(03)",
    "RSA1024_Comm_p_sha384":   "DN(CN=TestRSA1024.p.0200.0202,O=rsaperca139.com.cn)HASH(SHA384)KEYTYPE(RSA1024)CERTTYPE(03)",
    "RSA1024_Comm_p_sha512":   "DN(CN=TestRSA1024.p.0200.0202,O=rsaperca139.com.cn)HASH(SHA512)KEYTYPE(RSA1024)CERTTYPE(03)",

    "RSA2048_Comm_p_sha1":     "DN(CN=TestRSA2048.p.0200.0202,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA1024)CERTTYPE(03)",    
    "RSA2048_Comm_p_sha256":   "DN(CN=TestRSA2048.p.0200.0202,O=rsaperca139.com.cn)HASH(SHA256)KEYTYPE(RSA1024)CERTTYPE(03)",
    "RSA2048_Comm_p_sha384":   "DN(CN=TestRSA2048.p.0200.0202,O=rsaperca139.com.cn)HASH(SHA384)KEYTYPE(RSA1024)CERTTYPE(03)",
    "RSA2048_Comm_p_sha512":   "DN(CN=TestRSA2048.p.0200.0202,O=rsaperca139.com.cn)HASH(SHA512)KEYTYPE(RSA1024)CERTTYPE(03)",  
    "SM2256_Comm_p_SM3":       "DN(CN=TestSM2.p.0200.0201,O=rsaperca139.com.cn)HASH(SM3)KEYTYPE(SM2256)CERTTYPE(03)",   

}
mixCertDict={
    CertListInfoMap["RSA1024_Mixed_sha1"],
    CertListInfoMap["RSA1024_Mixed_sha256"],          
    CertListInfoMap["RSA1024_Mixed_sha384"],
    CertListInfoMap["RSA1024_Mixed_sha512"],     
    CertListInfoMap["RSA2048_Mixed_sha1"],
    CertListInfoMap["RSA2048_Mixed_sha256"],
    CertListInfoMap["RSA2048_Mixed_sha384"],  
    CertListInfoMap["RSA2048_Mixed_sha512"],                                                                        
    }

commCertDict={
    CertListInfoMap["RSA1024_Comm_p_sha1"],
    CertListInfoMap["RSA1024_Comm_p_sha256"],
    CertListInfoMap["RSA1024_Comm_p_sha384"],
    CertListInfoMap["RSA1024_Comm_p_sha512"],     
    CertListInfoMap["RSA2048_Comm_p_sha1"], 
    CertListInfoMap["RSA2048_Comm_p_sha256"], 
    CertListInfoMap["RSA2048_Comm_p_sha384"], 
    CertListInfoMap["RSA2048_Comm_p_sha512"],    
    CertListInfoMap["SM2256_Comm_p_SM3"],                                                                                               
    }

dispCertDict={
    CertListInfoMap["RSA1024_Sig2_p_sha1"],
    CertListInfoMap["RSA1024_Sig2_p_sha1"],
    CertListInfoMap["RSA1024_Sig2_p_sha384"],
    CertListInfoMap["RSA1024_Sig2_p_sha512"],     
    CertListInfoMap["RSA2048_Sig2_p_sha1"], 
    CertListInfoMap["RSA2048_Sig2_p_sha256"], 
    CertListInfoMap["RSA2048_Sig2_p_sha384"], 
    CertListInfoMap["RSA2048_Sig2_p_sha512"],    
    CertListInfoMap["SM2256_Sig2_p_sm3"],                                                                                               
    } 

