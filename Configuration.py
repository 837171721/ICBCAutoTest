# -*- coding: utf-8 -*-
import uiautomation
import os
import subprocess
import win32gui,win32api,win32con
from SetUp import *
from EsTestMidware import *
import socket,getpass
import sys

#####申请buffer对象
buffer_len = 40
str_buffer = win32gui.PyMakeBuffer(buffer_len)

# 获取U盾序列号
EsMidware = EsTest_Midware()
KeyID = EsMidware.GetMediaId()

# 当前系统用户名称
user_name = getpass.getuser()

if 32 == test_System:
    open_path = 'C:\\Program Files\\BOC\\USBKEY II\\IBank\\BOCUK2IBankAdmin.exe'
    uninstall_path = 'C:\\Program Files\\BOC\\USBKEY II\\IBank\\Uninstall.exe'
    file_path = 'C:\\Program Files\\BOC\\USBKEY II\\IBank'
    uninstall_file_path = 'C:\\Program Files'
if 64 == test_System:
    open_path = 'C:\\Program Files (x86)\\\BOC\\USBKEY II\\IBank\\BOCUK2IBankAdmin.exe'
    uninstall_path = 'C:\\Program Files (x86)\\BOC\\USBKEY II\\IBank\\Uninstall.exe'
    file_path = 'C:\\Program Files (x86)\\BOC\\USBKEY II\\IBank'
    dll_path = 'C:/Windows/SysWOW64/'
    dll_file = ['NetBankCspBOC.bin', 'NetBankCspBOC.dll', 'NetBankCspBOC.sig', 'NetBankCspBOCS.dll']
    uninstall_file_path = 'C:\\Program Files (x86)'
# 开始菜单路径
start_path = 'C:/ProgramData/Microsoft/Windows/Start Menu/Programs/中行网银USBKey数字安全证书管理工具/文鼎创'
start_file = ['中行网银USBKey数字安全证书管理工具.lnk', '卸载.lnk']
uninstall_start_path = 'C:/ProgramData/Microsoft/Windows/Start Menu/Programs'

#管理工具打开/卸载路径，包含32位与64位
open_path_32 = 'C:\\Program Files\\BOC\\USBKEY II\\IBank\\BOCUK2IBankAdmin.exe'
open_path_64 = 'C:\\Program Files (x86)\\\BOC\\USBKEY II\\IBank\\BOCUK2IBankAdmin.exe'

uninstall_path_32 = 'C:\\Program Files\\BOC\\USBKEY II\\IBank\\Uninstall.exe'
uninstall_path_64 = 'C:\\Program Files (x86)\\BOC\\USBKEY II\\IBank\\Uninstall.exe'

os.chdir('../../')
path = os.getcwd()
testsign_path_IE = path + '\Import\Windows签名控件\IE\-3.4.1.3\程序\Demo\Cryptokit.BOC.html'    #签名测试页路径
testsign_path_NotIE = path + '\Import\Windows签名控件\\非IE\-3.4.1.1-X78\程序\Demo\\npCryptokit.BOC.html'
signtext_path = path + '\Import\Windows签名控件\IE\-3.4.1.3\程序\Demo\DataTobeSigned.txt'    #签名报文路径
testsign_path = path + '\Import\Windows签名控件\非IE\-3.4.1.1-X78\程序\Demo\\npCryptokit.BOC.html'
HTMLReport_path = path + '\Output'+'\\'                                                     #测试结果报告路径
downloadcert_path = path + '\Import\CFCA下证控件\IE\Demo\CryptoKit.CertEnrollment.BOC.html'  #下证测试页路径
downloadcert_path_NotIE = path + '\Import\CFCA下证控件\非IE\Demo\CryptoKit.CertEnrollment.BOC.html' # 非IE下证测试页路径
P10_tool = path + '\Import\P10解析工具\P10TOCertTool.exe'                                    #P10转P7工具路径
install_path = path + '\Import\驱动安装包\\2.1.0.17\BOCNetbankUSBKey.exe'
old_install_path = path + '\Import\驱动安装包\\2.1.0.8\BOCNetbankUSBKey.exe'
os.chdir('./Modules/venv')

# 安装路径下的文件列表(32位）
file_list = ['BOCFfxP11Loader.exe', 'BOCFfxP11Loader_x64.exe', 'BOCNET_CN.chm', 'BOCNET_EN.chm', 'BOCNET_HK.chm', 'BOCUK2IBankAdmin.exe', 'EsBOCExtUI.exe', 'NetBankMidwareV2Cfg_CN.bin', 'NetBankMidwareV2Cfg_EN.bin', 'NetBankMidwareV2Cfg_TC.bin', 'Res', 'Uninstall.exe']

# 安装路径下的文件列表(64位）
file_list_64 = ['BOCFfxP11Loader.exe', 'BOCFfxP11Loader_x64.exe', 'BOCNET_CN.chm', 'BOCNET_EN.chm', 'BOCNET_HK.chm', 'BOCUK2IBankAdmin.exe', 'EsBOCExtUI.exe', 'NetBankMidwareV2Cfg_CN.bin', 'NetBankMidwareV2Cfg_EN.bin', 'NetBankMidwareV2Cfg_TC.bin', 'Res', 'Uninstall.exe']


System32_path = 'C:/Windows/System32/'
System32_dll = ['EsServiceBOC.exe', 'NetBankCspBOC.bin', 'MidwareV2Config_BOC.bin', 'NetBankCspBOC.dll',
                'NetBankCspBOCS.dll']
SysWOW64_path = 'C:/Windows/SysWOW64/'
SysWOW64_dll = ['NetBankCspBOC.bin', 'NetBankCspBOC.dll', 'NetBankCspBOC.sig', 'NetBankCspBOCS.dll']


# 下载证书类型
BOC_DoubleCert_RSA1024 = '1024'  # RSA1024证书
BOC_DoubleCert_RSA2048 = '2048'  # RSA2048证书
BOC_DoubleCert_SM2 = 'SM2'       # SM2证书
BOC_ThreeCert = 0                # 国内复合证书
# HASH算法
BOC_HASH_ALG_MD5 = b'0x80000001'
BOC_HASH_ALG_SHA1 = b'0x80000002'
BOC_HASH_ALG_SHA256 = b'0x80000003'
BOC_HASH_ALG_SHA384 = b'0x80000004'
BOC_HASH_ALG_SHA512 = b'0x80000005'
BOC_HASH_ALG_SM3 = b'0x80000006'

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
REG_SZ = 1 # Unicode nul terminated string
REG_EXPAND_SZ = 2 # Unicode nul terminated string
REG_BINARY = 3 # Free form binary
REG_DWORD = 4 # 32-bit number
REG_DWORD_LITTLE_ENDIAN = 4 # 32-bit number (same as REG_DWORD)
REG_DWORD_BIG_ENDIAN = 5 # 32-bit number
REG_LINK = 6 # Symbolic Link (unicode)
REG_MULTI_SZ = 7 # Multiple Unicode strings
REG_RESOURCE_LIST = 8 # Resource list in the resource map
REG_FULL_RESOURCE_DESCRIPTOR = 9 # Resource list in the hardware description
REG_RESOURCE_REQUIREMENTS_LIST = 10
REG_QWORD = 11 # 64-bit number
REG_QWORD_LITTLE_ENDIAN = 11 # 64-bit number (same as REG_QWORD)

# 注册表路径(32位)
Excelsecu_RE = b'SOFTWARE\\Excelsecu\\EXCELSECU_BOC'
CSP_RE = b'SOFTWARE\\Microsoft\\Cryptography\\Defaults\\Provider\\Excelsecu BOC USBKey CSP V1.0'
RUN_RE = b'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run'
Uninstall_RE = b'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\BOCNetBankExcelsecuTool'
# 注册表路径(64位)
Excelsecu_RE_64 = b'SOFTWARE\\Wow6432Node\\Excelsecu\\EXCELSECU_BOC'
CSP_RE_64 = b'SOFTWARE\\Wow6432Node\\Microsoft\\Cryptography\\Defaults\\Provider\\Excelsecu BOC USBKey CSP V1.0'
RUN_RE_64 = b'SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Run'
Uninstall_RE_64 = b'SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\BOCNetBankExcelsecuTool'

# 注册表中的信息
Image_Path = b'%SystemRoot%\\System32\\NetBankCspBOCS.dll'
Image_Path_64 = b'%SystemRoot%\\system32\\NetBankCspBOCS.dll'
CSPName = b"NetBankCspBOC.dll"
BOCUK2IBankAdmin_64 = b'"C:\\Program Files (x86)\\BOC\\USBKEY II\\IBank\\BOCUK2IBankAdmin.exe" /RunMode AutoRun'
BOCUK2IBankMon_64 = b'"C:\\Program Files (x86)\\BOC\\USBKEY II\\IBank\\BOCUK2IBankMon.exe"'
BOCUK2IBankAdmin = b'"C:\\Program Files\\BOC\\USBKEY II\\IBank\\BOCUK2IBankAdmin.exe" /RunMode AutoRun'
BOCUK2IBankMon = b'"C:\\Program Files\\BOC\\USBKEY II\\IBank\\BOCUK2IBankMon.exe"'
DisplayName = '中行网银USBKey数字安全证书管理工具'
DisplayName_utf8 = DisplayName.encode('UTF-8')
DisplayName_gbk = DisplayName.encode('GBK')
Publisher = '文鼎创'
Publisher_utf8 = Publisher.encode('UTF-8')
Publisher_gbk = Publisher.encode('GBK')
DisplayVersion = ManagerVersion.encode('GBK')
DisplayIcon_64 = b'"C:\\Program Files (x86)\\BOC\\USBKEY II\\IBank\\BOCUK2IBankAdmin.exe"'
UninstallString_64 = b'"C:\\Program Files (x86)\\BOC\\USBKEY II\\IBank\\Uninstall.exe"'
DisplayIcon = b'"C:\\Program Files\\BOC\\USBKEY II\\IBank\\BOCUK2IBankAdmin.exe"'
UninstallString = b'"C:\\Program Files\\BOC\\USBKEY II\\IBank\\Uninstall.exe"'
print(sys.argv[0])

