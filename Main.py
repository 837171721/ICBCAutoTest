# coding=utf-8
'''
Created on 2018.07.14

Desc: Program entrance  

@author: ys
'''
import os
import sys
import time
import re  # 引入正在表达式
import operator
import win32api
import win32con
import TestIcbcGmUserkey
from GlobalConfigure import *
from TestCases_GetMediaID import *
from TestCases_GetGMCertDN import *
from TestCases_GetPublicKey import *
from TestCases_GetEnPkOfOriginalProKey import *
from TestCases_GetEnPkOfNewProKey import *
from TestCases_GetVer import *
from TestCases_GetDriverVer import *
from TestCases_GMDelTempKey import *
from TestCases_InitCard import *
from TestCases_ChangePin import *
from TestCases_GetCharsetList import *
from TestCases_SetCharset import *
from TestCases_GetLanguageList import *
from TestCases_SetLanguageList import *
from TestCases_SetWarningMsg import *
from TestCases_GMCreatePKCS10 import *
from TestCases_GMWritePKCS7 import *
from TestCases_GetCSPInfo import *
from TestCases_GetPubKeyNum import *
from TestCases_RegisterCertC import *
from TestCases_UnRegisterCertC import *
from TestCases_GetAdminKeyInfoC import *
from TestCases_GMSetNewAmdinKeyC import *
from TestCases_VerifySignAfter import *
from TestCases_SecInitCard import *
from TestCases_GetBase64Random import *
from TestCases_GetBase64Decode import *
from TestCases_initCardDefaultPin import *
if GL.UKey:
    from TestCases_DispSign_FP import *
    from TestCases_FileSign_FP import *
else:
    from TestCases_DispSign import *
    from TestCases_FileSign import *
from TestCases_ImportEncCert import *

from logTest import SysClass, LoggerClass
from _codecs import encode
conf = LoggerClass(loglevel=levels.get(log_level), logger="Main.py")
logger = conf.getlogger()

AdminKeyList = ['True', '00', '00']  # 参数1：U盾类型，参数2：保护密钥值，参数3：序号


def testCases_noKey(testCtrl, TestingRange, AdminKeyInfo):
    if 2 == TestingRange:
        GL.TestingRange = TestingRange
        win32api.MessageBox(0, "请确认未插入任何U盾！按【确认】键后开始测试！",
                            "提示框", win32con.MB_OK)
        test_CasesGroup(testCtrl, TestingRange, AdminKeyInfo)


def testCases_manyKey(testCtrl, TestingRange, AdminKeyInfo):
    if 3 == TestingRange:
        GL.TestingRange = TestingRange
        win32api.MessageBox(0, "请插入多支同款U盾！按【确认】键后开始测试！", "提示框", win32con.MB_OK)
        test_CasesGroup(testCtrl, TestingRange, AdminKeyInfo)


def testCasestest_oneKey_Verify(testCtrl, TestingRange, AdminKeyInfo):
    if 1 == TestingRange:
        GL.TestingRange = TestingRange
        win32api.MessageBox(0, "请插入一支测试U盾！按【确认】键后开始测试！", "提示框", win32con.MB_OK)
        # 获取U盾类型
        if not (operator.eq(main_url, testUrl_GM_User) or operator.eq(main_url, testUrl_GM_Manage)):
            testCtrl.browser.get(testUrl_GM_User)
        AdminKeyList = testCtrl.get_UkeyType()
        testCtrl.browser.get(main_url)
        AdminKeyInfo = AdminKeyList
        test_CasesGroup(testCtrl, TestingRange, AdminKeyInfo)


def testCasestest_oneKey_Detail(testCtrl, TestingRange, AdminKeyInfo):
    if 0 == TestingRange:
        GL.TestingRange = 2
        win32api.MessageBox(0, "请确认未插入任何U盾！按【确认】键后开始测试！",
                            "提示框", win32con.MB_OK)
        test_CasesGroup(testCtrl, 2, AdminKeyInfo)

        GL.TestingRange = 3
        win32api.MessageBox(0, "请插入多支同款U盾！按【确认】键后开始测试！", "提示框", win32con.MB_OK)
        test_CasesGroup(testCtrl, 3, AdminKeyInfo)

        GL.TestingRange = TestingRange
        win32api.MessageBox(
            0, "请拔除多余U盾，确保仅插入一支测试U盾！按【确认】键后开始测试！", "提示框", win32con.MB_OK)
        # 获取U盾类型
        if not (operator.eq(main_url, testUrl_GM_User) or operator.eq(main_url, testUrl_GM_Manage)):
            testCtrl.browser.get(testUrl_GM_User)
        AdminKeyList = testCtrl.get_UkeyType()
        testCtrl.browser.get(main_url)
        AdminKeyInfo = AdminKeyList
        test_CasesGroup(testCtrl, TestingRange, AdminKeyInfo)


def testCasestest_oneKey_Base(testCtrl, TestingRange, AdminKeyInfo):
    if 4 == TestingRange:

        GL.TestingRange = 2
        win32api.MessageBox(0, "请确认未插入任何U盾！按【确认】键后开始测试！",
                            "提示框", win32con.MB_OK)
        test_CasesGroup(testCtrl, 2, AdminKeyInfo)

        GL.TestingRange = TestingRange
        win32api.MessageBox(0, "请插入一支测试U盾！按【确认】键后开始测试！", "提示框", win32con.MB_OK)
        # 获取U盾类型
        if not (operator.eq(main_url, testUrl_GM_User) or operator.eq(main_url, testUrl_GM_Manage)):
            testCtrl.browser.get(testUrl_GM_User)
        AdminKeyList = testCtrl.get_UkeyType()
        testCtrl.browser.get(main_url)

        AdminKeyInfo = AdminKeyList
        test_CasesGroup(testCtrl, TestingRange, AdminKeyInfo)


def test_CasesGroup(testCtrl, TestingRange, AdminKeyInfo):  # 测试用例集
    if operator.eq(testUrl_GM_User, main_url):
        test_GetAdminKeyInfo(testCtrl, TestingRange, AdminKeyInfo)  # 获取保护密钥信息
        test_GetMediaId(testCtrl, TestingRange)  # 获取介质号
        test_GetVer(testCtrl, TestingRange, AdminKeyInfo)  # 控件版本
        test_GetDriverVer(testCtrl, TestingRange, AdminKeyInfo)  # 驱动版本号
        test_GetCharsetList(testCtrl, TestingRange, AdminKeyInfo)  # 获取支持的字符集
        test_SetCharset(testCtrl, TestingRange, AdminKeyInfo)  # 设置即将签名的明文字符
        test_GetLanguageList(testCtrl, TestingRange, AdminKeyInfo)  # 获取支持的语言
        test_SetLanguageList(testCtrl, TestingRange, AdminKeyInfo)  # 设置支持的语言
        test_SetWarningMsg(testCtrl, TestingRange, AdminKeyInfo)  # 设置屏幕警告语
        test_GetCSPInfo(testCtrl, TestingRange)  # 获取CSP信息
        test_GetPublicKey(testCtrl, TestingRange, AdminKeyInfo)  # 公钥明文
        test_GetPubKeyNum(testCtrl, TestingRange, AdminKeyInfo)  # 获取公钥数目
        test_GetResgisterCert(testCtrl, TestingRange, AdminKeyInfo)  # 注册证书
        test_GetUnResgisterCertC(testCtrl, TestingRange, AdminKeyInfo)  # 注销证书
        test_GetEncPkeyOfOldAdminKey(
            testCtrl, TestingRange, AdminKeyInfo)  # 原保护密钥的加密公钥
        test_GetEncPkeyOfNewAdminKey(
            testCtrl, TestingRange, AdminKeyInfo)  # 新保护密钥的加密公钥
        test_GetCertDN(testCtrl, TestingRange, AdminKeyInfo)  # 证书DN
        test_GetGMCreatePKCS10(testCtrl, TestingRange, AdminKeyInfo)  # 生成P10
        test_GetGMWritePKCS7(testCtrl, TestingRange, AdminKeyInfo)  # 写入证书
        test_GetChangePin(testCtrl, TestingRange, AdminKeyInfo)  # 修改PIN
        test_GetDelTempKey(testCtrl, TestingRange, AdminKeyInfo)  # 删除临时公私钥
        test_GetInitCard(testCtrl, TestingRange, AdminKeyInfo)  # 初始化U盾
        if GL.UKey:
            test_GetDispSign_FP(testCtrl, TestingRange, AdminKeyInfo)  # 显示签名
            test_GetFileSign_FP(testCtrl, TestingRange, AdminKeyInfo)  # 文件签名
        else:
            test_GetDispSign(testCtrl, TestingRange, AdminKeyInfo)  # 显示签名
            test_GetFileSign(testCtrl, TestingRange, AdminKeyInfo)  # 文件签名
        test_ImportEncCert(testCtrl, TestingRange, AdminKeyInfo)  # 导入加密证书

    elif operator.eq(testUrl_GM_Manage, main_url):
        test_GetAdminKeyInfo(testCtrl, TestingRange, AdminKeyInfo)  # 获取保护密钥信息
        test_GetBase64Random(testCtrl, TestingRange, AdminKeyInfo)  # 获取随机数
        test_GMSetNewAmdinKeyC(testCtrl, TestingRange, AdminKeyInfo)  # 保护密钥更新
        test_VerifySignAfter(testCtrl, TestingRange, AdminKeyInfo)  # 事后验签
        test_SecInitCard(testCtrl, TestingRange, AdminKeyInfo)  # 安全初始化
        test_InitCardDefaultPin(testCtrl, TestingRange,
                                AdminKeyInfo)  # 默认PIN码初始化
        test_GetBase64Decode(testCtrl, TestingRange, AdminKeyInfo)  # Base64解码

    elif operator.eq(testUrl_User, main_url):
        test_GetMediaId(testCtrl, TestingRange)  # 获取介质号
        test_GetVer(testCtrl, TestingRange, AdminKeyInfo)  # 控件版本
        test_GetCharsetList(testCtrl, TestingRange, AdminKeyInfo)  # 获取支持的字符集
        test_SetCharset(testCtrl, TestingRange, AdminKeyInfo)  # 设置即将签名的明文字符
        test_GetLanguageList(testCtrl, TestingRange, AdminKeyInfo)  # 获取支持的语言
        test_SetLanguageList(testCtrl, TestingRange, AdminKeyInfo)  # 获取支持的语言
        test_SetWarningMsg(testCtrl, TestingRange, AdminKeyInfo)  # 设置屏幕警告语
        test_GetCSPInfo(testCtrl, TestingRange)  # 获取CSP信息
        test_GetChangePin(testCtrl, TestingRange, AdminKeyInfo)  # 修改PIN
        test_GetInitCard(testCtrl, TestingRange, AdminKeyInfo)  # 初始化U盾
        test_GetPublicKey(testCtrl, TestingRange, AdminKeyInfo)  # 公钥明文
        test_GetPubKeyNum(testCtrl, TestingRange, AdminKeyInfo)  # 获取公钥数目
        test_GetResgisterCert(testCtrl, TestingRange, AdminKeyInfo)  # 注册证书
        test_GetUnResgisterCertC(testCtrl, TestingRange, AdminKeyInfo)  # 注销证书
        test_GetEncPkeyOfOldAdminKey(
            testCtrl, TestingRange, AdminKeyInfo)  # 原保护密钥的加密公钥

    elif operator.eq(testUrl_Manage, main_url):
        test_GMSetNewAmdinKeyC(testCtrl, TestingRange, AdminKeyInfo)  # 保护密钥更新
        test_InitCardDefaultPin(testCtrl, TestingRange,
                                AdminKeyInfo)  # 默认PIN码初始化


def output_staticData(logFileName, outSys, starttime, endtime):
    '''
          通过日志文档中输出的信息进行统计
    '''
    # 用例总数
    caseCounts = 0
    # 通过数
    successCounts = 0
    # 失败数
    failCounts = 0
    str1 = "|| pass"
    str2 = "|| fail"
    fp = open(logFileName, "r", encoding="UTF-8")
    for line in fp.readlines():
        if (str1 in line) or (str2 in line):
            caseCounts = caseCounts+1
            if str1 in line:
                successCounts = successCounts+1
                # logger.warning(successCounts)
            if str2 in line:
                failCounts = failCounts+1
        else:
            continue

    fp.close()

    # 耗时
    timeOut = float('%.2f' % ((endtime-starttime)/60))
    # 通过率
    percentPass = 0
    if 0 != caseCounts:
        percentPass = float('%.2f' % ((successCounts/caseCounts)*100))

    outSys.getSysLog(logFileName, "r+", caseCounts,
                     successCounts, failCounts, timeOut, percentPass)


if __name__ == '__main__':
    # 创建SysClass对象
    outSys = SysClass()

    # 第一步：日志文件头部写入总体测试情况的初始数据，仅占用位置
    outSys.getSysLog(log_file, "w", 0, 0, 0, 0, 100, 200)

    # 打开控件测试页
    testCtrl = TestIcbcGmUserkey.TestIcbcGmUser(main_url)
    testCtrl.open()
    # 执行测试用例文档
    starttime = time.time()

    GmNewAdminKey = AdminKeyList
    if 0 == TestingRange:  # 详细测试
        testCasestest_oneKey_Detail(testCtrl, TestingRange, GmNewAdminKey)
    elif 1 == TestingRange:  # 验证测试
        testCasestest_oneKey_Verify(testCtrl, TestingRange, GmNewAdminKey)
    elif 2 == TestingRange:  # 无key测试
        testCases_noKey(testCtrl, TestingRange, GmNewAdminKey)
    elif 3 == TestingRange:  # 多key测试
        testCases_manyKey(testCtrl, TestingRange, GmNewAdminKey)
    elif 4 == TestingRange:  # 待补充
        testCasestest_oneKey_Base(testCtrl, TestingRange, GmNewAdminKey)

    endtime = time.time()

    # 关闭控件测试页
    time.sleep(1)
    testCtrl.close()

    # 最后一步：日志文件头部插入总体测试情况的统计数据，覆盖最开始写入的初始数据
    output_staticData(log_file, outSys, starttime, endtime)
