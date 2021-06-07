# -*- coding: utf-8 -*-
import uiautomation
import os
import subprocess
import win32gui
import win32api
import win32con
from SetUp import *
from EsTestMidware import *
import socket
import getpass
import sys

# 申请buffer对象
BUFFER_LEN = 40
STR_BUFFER = win32gui.PyMakeBuffer(BUFFER_LEN)

# 获取U盾序列号
EsMidware = EsTest_Midware()
KEYID = EsMidware.GetMediaId()

# 当前系统用户名称
user_name = getpass.getuser()

if 32 == TEST_SYSTEM:
    # 打开路径
    OPEN_PATH = 'C:\\ProgramFiles\\ICBCEbankTools\\MingWah\\MWICBCUKeyToolU.exe'
    # 卸载路径
    UNINSTALL_PATH = 'C:\\Program Files\\ICBCEbankTools\\MingWah\\Uninstall.exe'
    # 安装目录和文件
    FILE_PATH = 'C:\\Program Files\\ICBCEbankTools\\MingWah'
    FILE_LIST = ['Res', 'ICBC User Manual_SC.chm', 'MWICBCUKeyToolU.exe', 'MWICBCUKeyUI.exe', 'MWREGICBC.exe', 'NetBankMidwareV2Cfg_AR.ini', 'NetBankMidwareV2Cfg_CN.ini', 'NetBankMidwareV2Cfg_DE.ini', 'NetBankMidwareV2Cfg_EN.ini',  'NetBankMidwareV2Cfg_FR.ini', 'NetBankMidwareV2Cfg_ID.ini',
                 'NetBankMidwareV2Cfg_JP.ini', 'NetBankMidwareV2Cfg_KR.ini', 'NetBankMidwareV2Cfg_KZ.ini', 'NetBankMidwareV2Cfg_NL.ini', 'NetBankMidwareV2Cfg_PL.ini', 'NetBankMidwareV2Cfg_RU.ini', 'NetBankMidwareV2Cfg_TC.ini', 'NetBankMidwareV2Cfg_TH.ini', 'Uninstall.exe']

    # 动态库路径和文件
    DLL_PATH = 'C:/Windows/System32/'
    DLL_FILE = ['ICBCPkcs11_v1.DLL', 'ICBCPkcs11_v1.bin', 'icbcPkcs11_v1.sig',
                'icbccsps.dll', 'EsMiniCA.dll', 'MidwareV2Config_ICBC.BIN']
    # 卸载目录和文件
    UNINSTALL_FILE_PATH = 'C:\\Program Files'
    UNINSTALL_FILE = ['ICBCEbankTools']
    # 
if 64 == TEST_SYSTEM:
    # 打开路径
    OPEN_PATH = 'C:\\Program Files (x86)\\ICBCEbankTools\\MingWah\\MWICBCUKeyToolU.exe'
    # 卸载路径
    UNINSTALL_PATH = 'C:\\Program Files (x86)\\ICBCEbankTools\\MingWah\\Uninstall.exe'
    # 安装目录和文件
    FILE_PATH = 'C:\\Program Files (x86)\\ICBCEbankTools\\MingWah'
    FILE_LIST = ['Res', 'ICBC User Manual_SC.chm', 'MWICBCUKeyToolU.exe', 'MWICBCUKeyUI.exe', 'MWREGICBC.exe', 'NetBankMidwareV2Cfg_AR.ini', 'NetBankMidwareV2Cfg_CN.ini', 'NetBankMidwareV2Cfg_DE.ini', 'NetBankMidwareV2Cfg_EN.ini',  'NetBankMidwareV2Cfg_FR.ini', 'NetBankMidwareV2Cfg_ID.ini',
                 'NetBankMidwareV2Cfg_JP.ini', 'NetBankMidwareV2Cfg_KR.ini', 'NetBankMidwareV2Cfg_KZ.ini', 'NetBankMidwareV2Cfg_NL.ini', 'NetBankMidwareV2Cfg_PL.ini', 'NetBankMidwareV2Cfg_RU.ini', 'NetBankMidwareV2Cfg_TC.ini', 'NetBankMidwareV2Cfg_TH.ini', 'Uninstall.exe']
    # 动态库目录和文件
    DLL_PATH = 'C:/Windows/SysWOW64/'
    DLL_FILE = ['ICBCPkcs11_v1.DLL', 'ICBCPkcs11_v1.bin', 'icbcPkcs11_v1.sig',
                'icbccsps.dll', 'EsMiniCA.dll', 'MidwareV2Config_ICBC.BIN']
    # 卸载目录和文件
    UNINSTALL_FILE_PATH = 'C:\\Program Files (x86)'
    UNINSTALL_FILE = ['ICBCEbankTools']
# 开始菜单路径
START_PATH = 'C:/ProgramData/Microsoft/Windows/Start Menu/Programs/工行网银客户端软件/明华&文鼎创'
START_FILE = ['ICBC在线银行.lnk', 'Ｕ盾客户端管理工具（明华&文鼎创）.lnk', 'U盾使用指南.lnk', '卸载.lnk']
UNINSTALL_START_PATH = 'C:/ProgramData/Microsoft/Windows/Start Menu/Programs'
UNINSTALL_FILE = ['工行网银客户端软件/明华&文鼎创']

# 桌面快捷方式
DESKTOP_PATH = 'C:\\Users\\Public\\Desktop'
DESKTOP_FILE = ['ICBC在线银行.lnk']

# 控件路径
os.chdir('../../../')
PATH = os.getcwd()
TESTURL_GM_USER_32 = PATH + '\\Import\IE\Test_GM_Icbc_Usbkey.htm'  # 32位国密控件页
TESTURL_GM_MANAGE_32 = PATH + '\Import\IE\Test_GM_Icbc_Manage.htm'
TESTURL_USER_32 = PATH + '\Import\IE\Testicbcmwusbkey.htm'  # 32位非国密控件页
TESTURL_MANAGE_32 = PATH + '\Import\IE\Testicbcmwmanage.htm'

TESTURL_GM_USER_64 = PATH + 'Import\IE\Test_GM_Icbc_Usbkey_64.htm'  # 64位国密控件页
TESTURL_GM_MANAGE_64 = PATH + 'Import\IE\Test_GM_Icbc_Manage_64.htm'
TESTURL_USER_64 = PATH + 'Import\IE\Testicbcmwusbkey_64.htm'  # 64位非国密控件页
TESTURL_MANAGE_64 = PATH + 'Import\IE\Testicbcmwmanage_64.htm'

# 系统语言
# 0:中文          1:繁体        2:英文                          #---------------每次都需要配置
languageType = 0
if languageType == 0:
    str_title = '输入密码'
    str_changeTitle = '修改U盾密码'
    str_verifyTitle = '用户提示'
    str_signTitle = '请核对签名信息'
elif languageType == 1:
    str_title = '輸入密碼'
    str_changeTitle = '修改U盾密碼'
    str_verifyTitle = '用戶提示'
    str_signTitle = '請核對簽名信息'
elif languageType == 2:
    str_title = 'Input Password'
    str_changeTitle = 'Change USB-Shield Password'
    str_verifyTitle = 'User Tips'
    str_signTitle = 'Verify Critical Information'

HTMLREPORT_PATH = PATH + '\Output'+'\\'  # 测试结果报告路径
P10_TOOL = PATH + '\Import\P10解析工具\P10TOCertTool.exe'  # P10转P7工具路径
INSTALL_PATH = PATH + '\\Import\\驱动安装包\\V2.5.0.11\\ICBC_MW&WDC_UShield2_Install.exe'
INSTALL_SILENT_PATH = PATH + \
    '\\Import\\驱动安装包\\V2.5.0.11\\ICBC_MW&WDC_UShield2_Install.exe'
INSTALL_GG_PATH = PATH + \
    '\\Import\驱动安装包\\V2.5.0.11\\ICBC_MW&WDC_UShield2_Install.exe'
INSTALL_PATH_OLD = PATH + \
    '\\Import\驱动安装包\\V2.5.0.10\\ICBC_MW&WDC_UShield2_Install.exe'
# os.chdir('./Modules/venv')

# 日志写入方式
# substr = main_url[main_url.rfind("\\", 0, len(
#     main_url)) + 1: main_url.rfind(".", 0, len(main_url))]
# systime = time.strftime("%Y%m%d%H%M%S_", time.localtime(time.time()))
# report_path = (os.path.abspath(os.path.join(os.getcwd()))) + "\\Logs\\"
# if not os.path.exists(report_path):
#     os.makedirs(report_path)  # 获取此py文件路径，在此路径上创建Logs文件夹

# 日志名称
# log_file = report_path + systime + substr + ".log"  # 日志名称
# log_level = "info"  # 日志级别
# log_max_byte = 100 * 1024 * 1024  # 日志文件大小/个
# log_backup_count = 5  # 日志文件数目

# levels = {
#     "notset": logging.NOTSET,
#     "debug": logging.DEBUG,
#     "info": logging.INFO,
#     "warn": logging.WARN,
#     "error": logging.ERROR,
#     "critical": logging.CRITICAL}

# 文件签名
FILEPATH = PATH+"FileSignInfo\\"
P7FILEPATH = FILEPATH+"file000.txt"
BATFILEPATH = FILEPATH+"file1K.txt"
BATFILEPATH1K = FILEPATH+"file1K.txt"
BATFILEPATH2K = FILEPATH+"file2K.txt"
BATFILEPATH5K = FILEPATH+"file5K.txt"
BATFILEPATH10K = FILEPATH+"file10K.txt"
BATFILEPATH1M = FILEPATH+"file1M.txt"
BATFILEPATH5M = FILEPATH+"file5M.txt"
BATFILEPATH10M = FILEPATH+"file10M.txt"
BATFILEPATH50M = FILEPATH+"file50M.txt"
BATFILEPATH90M = FILEPATH+"file90M.txt"
BATFILEPATH100M = FILEPATH+"file100M.txt"

# 对应按键的Bit位，可配置(与自动按键设备有关)
# KEY_TYPE_BIT_PAGEDOWN = 1
# KEY_TYPE_BIT_PAGEUP = 2
# KEY_TYPE_BIT_ENTER = 3
# KEY_TYPE_BIT_CANCEL = 4

KEY_TYPE_BIT_PAGEDOWN = 3
KEY_TYPE_BIT_PAGEUP = 1
KEY_TYPE_BIT_ENTER = 4
KEY_TYPE_BIT_CANCEL = 2

# 主键配置（读取注册表接口）
HKEY_CLASSES_ROOT = b'0x80000000'
HKEY_CURRENT_USER = b'0x80000001'
HKEY_LOCAL_MACHINE = b'0x80000002'
HKEY_USERS = b'0x80000003'
HKEY_PERFORMANCE_DATA = b'0x80000004'
HKEY_PERFORMANCE_TEXT = b'0x80000050'
HKEY_PERFORMANCE_NLSTEXT = b'0x80000060'
HKEY_CURRENT_CONFIG = b'0x80000005'
HKEY_DYN_DATA = b'0x80000006'

# 值项数据类型
REG_NONE = 0  # No value type
REG_SZ = 1  # Unicode nul terminated string
REG_EXPAND_SZ = 2  # Unicode nul terminated string
REG_BINARY = 3  # Free form binary
REG_DWORD = 4  # 32-bit number
REG_DWORD_LITTLE_ENDIAN = 4  # 32-bit number (same as REG_DWORD)
REG_DWORD_BIG_ENDIAN = 5  # 32-bit number
REG_LINK = 6  # Symbolic Link (unicode)
REG_MULTI_SZ = 7  # Multiple Unicode strings
REG_RESOURCE_LIST = 8  # Resource list in the resource map
REG_FULL_RESOURCE_DESCRIPTOR = 9  # Resource list in the hardware description
REG_RESOURCE_REQUIREMENTS_LIST = 10
REG_QWORD = 11  # 64-bit number
REG_QWORD_LITTLE_ENDIAN = 11  # 64-bit number (same as REG_QWORD)

# 注册表路径(32位)
CSP_RE = b'SOFTWARE\\Microsoft\\Cryptography\\Defaults\\Provider\\M&W CSP for ICBC V5'
# 注册表路径(64位)
CSP_RE_64 = b'SOFTWARE\\Microsoft\\Cryptography\\DefaultsP\\rovider\\M&W CSP for ICBC V5'
CSP_RE_64_2 = b'SOFTWARE\\Wow6432Node\\Microsoft\\Cryptography\\Defaults\\Provider\\M&W CSP for ICBC V5'

# 屏幕警告语
SCR_WARNING_CH = '请核对签名信息是否正确'
SCR_WARNING_EN = 'Please check the signature information is correct'

# xml报文
XML_INFO_GBK = '''
<?xml version="1.0" encoding="gb2312"?>
<TradeData>
<field name="付款人姓名" value="明华公司" DisplayOnScreen="TRUE"/>
<field name="付款卡号" value="95588202000088888888" DisplayOnScreen="TRUE"/>
<field name="收款人姓名" value="刘伟伟" DisplayOnScreen="TRUE"/>
<field name="收款帐号" value="95588202000099999999" DisplayOnScreen="TRUE"/>
<field name="收款人所在地" value="北京" DisplayOnScreen="TRUE"/>
<field name="收款人所在网点机构" value="九龙山支行 " DisplayOnScreen="TRUE"/>
<field name="手续费" value="0" DisplayOnScreen="TRUE"/>
<field name="总金额" value="100000.00" DisplayOnScreen="TRUE"/>
<field name="交易提交时间" value="20100402171706" DisplayOnScreen="TRUE"/>
</TradeData>
'''
XML_INFO_UTF8 = '''
<?xml version="1.0" encoding="utf-8"?>
<TradeData>
<field name="付款人姓名" value="明华公司" DisplayOnScreen="TRUE"/>
<field name="付款卡号" value="95588202000088888888" DisplayOnScreen="TRUE"/>
<field name="收款人姓名" value="刘伟伟" DisplayOnScreen="TRUE"/>
<field name="收款帐号" value="95588202000099999999" DisplayOnScreen="TRUE"/>
<field name="收款人所在地" value="北京" DisplayOnScreen="TRUE"/>
<field name="收款人所在网点机构" value="九龙山支行 " DisplayOnScreen="TRUE"/>
<field name="手续费" value="0" DisplayOnScreen="TRUE"/>
<field name="总金额" value="100000.00" DisplayOnScreen="TRUE"/>
<field name="交易提交时间" value="20100402171706" DisplayOnScreen="TRUE"/>
</TradeData>
'''

# KEY显
DISP_INFO_CH = '''
收款帐号:9558820200009991111111111
总金额:100000.00RMB
手续费:0
交易提交时间:20100402171706
'''
DISP_INFO_TW = '''
收款帳號:9558820200009991111111111
總金額:100000.00RMB
手續費:0
交易提交時間:20100402171706
'''

DISP_INFO_EN = '''
Collection account: 9558820200009991111111111
Total amount: 100000.00RMB
Fee: 0
Transaction commit time: 20100402171706
'''

# 证书申请 P10请求
# 非国密U盾：RSA混用证书
RSA1024_MIXED = 'DN(CN=TestRSA1024,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA1024)CERTTYPE(02)'
RSA2048_MIXED = 'DN(CN=TestRSA2048,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA2048)CERTTYPE(02)'

# 国密U盾:混用证书
RSA1024_MIXED_GM = 'DN(CN=TestRSA1024,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA1024)CERTTYPE(02)'
RSA2048_MIXED_GM = 'DN(CN=TestRSA2048,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA2048)CERTTYPE(02)'

# 国密U盾：专用证书
RSA1024_SPE_P = 'DN(CN=TestRSA1024.p.0200.0102,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA1024)CERTTYPE(01)'
RSA2048_SPE_P = 'DN(CN=TestRSA2048.p.0200.0102,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA2048)CERTTYPE(01)'
SM2_SPE_P = 'DN(CN=TestSM2.p.0200.0101,O=rsaperca139.com.cn)HASH(SM3)KEYTYPE(SM2256)CERTTYPE(01)'
RSA1024_SPE_C = 'DN(CN=TestRSA1024.c.0200.0102,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA1024)CERTTYPE(01)'
RSA2048_SPE_C = 'DN(CN=TestRSA2048.c.0200.0102,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA2048)CERTTYPE(01)'
SM2_SPE_C = 'DN(CN=TestSM2.c.0200.0101,O=rsaperca139.com.cn)HASH(SM3)KEYTYPE(SM2256)CERTTYPE(01)'

# 国密U盾：通用证书
RSA1024_COMM_P = 'DN(CN=TestRSA1024.p.0200.0202,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA1024)CERTTYPE(03)'
RSA2048_COMM_P = 'DN(CN=TestRSA2048.p.0200.0202,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA2048)CERTTYPE(03)'
SM2_COMM_P = 'DN(CN=TestSM2.p.0200.0201,O=rsaperca139.com.cn)HASH(SM3)KEYTYPE(SM2256)CERTTYPE(03)'
RSA1024_COMM_C = 'DN(CN=TestRSA1024.c.0200.0202,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA1024)CERTTYPE(03)'
RSA2048_COMM_C = 'DN(CN=TestRSA2048.c.0200.0202,O=rsaperca139.com.cn)HASH(SHA1)KEYTYPE(RSA2048)CERTTYPE(03)'
SM2_COMM_C = 'DN(CN=TestSM2.c.0200.0201,O=rsaperca139.com.cn)HASH(SM3)KEYTYPE(SM2256)CERTTYPE(03)'

# 密钥更新
# 旧体系保护密钥原始值（32字节）
ADMIN_KEY_AES_OLD = 'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'
# 新体系AES密钥参考值（32字节）
AMDIN_KEY_AES_NEW = 'AAFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'
# 新体系SM4密钥参考值
AMDINKEY_SM4 = 'AAFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'
# 旧体系转旧体系时原始密钥为（16字节）
AMDIN_KEY_3DES_OLD_1 = '569C9E50BD52FE9C626261EB7E3382C4'
AMDIN_KEY_3DES_OLD_2 = '112233445566778811223344556677FF'
