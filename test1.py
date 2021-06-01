#coding=utf-8
testString='''获取介质号失败:未知错误。返回码:-102 There is no key!'''
'''
import re           #导入正则表达式模块
p=re.compile('\s+') # \s查找字符串中的空白符(制表符、空格、换行符)，至少匹配一次到多次
new_string1=re.sub(p,'',testString) #将空白符剔除，
new_string2=re.sub(p,' ',testString) #将空白符替换为空格
print("testString=", testString)
print("new_string1=", new_string1)
print("new_string2=", new_string2)
'''

import sys
import time
import os
import win32api 
import win32con
import win32gui
import operator
import subprocess
import base64
from ctypes import *
from ctypes.wintypes import *
import string
import binascii as B
import win32process
from ctypes import c_ubyte, cast, POINTER

P10Info="MIICgzCCAWsCADA/MSAwHgYDVQQDDBdUZXN0UlNBMjA0OC5wLjAyMDAuMDEwMjEbMBkGA1UECgwScnNhcGVyY2ExMzkuY29tLmNuMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAzFFA2Kmq9mW+Mc/UR4FKGiPsbaw5bmZQyFGMYVMGZjc20QKEnECvAUsLtj6sVmH/5QiqEGrKwcxoRQVnI9Ud2cuXZCOwnJoYmcmazkMD11kNXuGkE3chcQI1r+WbIoUPlXptBhMuy1Asd2bCpr0PPH6iZqWCifWZs0wZqNd10j+4hjAvr8dJ6hWdKYUMHrm4giRN0DNVbTdhP+9nNrOTwyEoi7ZR0vTnJyZZsB9+YlccEkK2OJtx4RO6EpSdxn8nuVpXgXQWwWHmIzpRfqvkKlt6nUVDx04PxNbstHciTGr1yib2U7u4PI2BSHLbxMGfU5E+F3Hk/5n48PeGKYFCVQIDAQABoAAwDQYJKoZIhvcNAQEFBQADggEBAGiXJDLVHnEv9jiww1UiYuMPeY7JjQu7hh7zQZ6ThGekrwrJ/Gh/EFRZDDeEMiyaRcMMfI1kpahWkYDWX8etES0H5UrneZGeZXZga7+hvFmu9r48uklcCYUx/tVJnpRDLPRz7LOFZDRsU13T6gT1NDrpzdi4MJgdIEh3aqCTswMznpkHC4asaNh26qh15D46ec7GPKZWIX+esnQOI0hvXdSM2OP9kkAQqPOxGI9GOfdUJFSIF3tZ0q9ijolptxTWGndBFNhseWcMbjd8etjzJ0v2FJMcdHQgZZzIFgakWVu8EqAfJM464AGAgy184YsR0EWIHZE2JJIh2KK5W/g2U6k="

dll = ctypes.CDLL("E:\\myJobLog\\TestRecord\\AutoTest\\ICBCTest\\HTMLTestFile\\MiniCA\\EsMiniCA.dll")
print(dll)
rootCert='E:\\myJobLog\\TestRecord\\AutoTest\\ICBCTest\\HTMLTestFile\\MiniCA\\MyOpenSSLRootCA.pfx'  #根证书和私钥
rootCertPin='1234'

p10Temp = base64.b64decode(P10Info)
p10Temp=B.b2a_hex(p10Temp)
p10Len = len(p10Temp)

pStr_p10 = ctypes.c_char_p()
pStr_p10.value = p10Temp

pVoid_p10 = ctypes.cast(pStr_p10, ctypes.c_void_p).value
szP7 = ctypes.create_string_buffer('\0'.encode('utf_8')*8192)
intPara = ctypes.c_ulong(8192)

x = (c_int * 100)()
intPara=ctypes.cast(x, POINTER(c_int))

ConstructX509Cert=dll.ConstructX509Cert
ConstructX509Cert.argtypes=[c_void_p,c_ulong,c_char_p,c_char_p,c_char_p,c_char_p,POINTER(c_int),]
ConstructX509Cert.restype=c_int
errorCode=ConstructX509Cert(
    pVoid_p10,   #void类型的P10字符串
    p10Len,      #P10长度
    ctypes.c_char_p(rootCert.encode('utf_8')), #根证书
    ctypes.c_char_p(rootCertPin.encode('utf-8')),  #根证书密码
    ctypes.c_char_p('1'.encode('utf-8')), #证书类型
    byref(szP7),     #P7包       
    byref(intPara))
'''
errorCode = dll.ConstructX509Cert(
    pVoid_p10,   #void类型的P10字符串
    p10Len,      #P10长度
    ctypes.c_char_p(rootCert.encode('utf_8')), #根证书
    ctypes.c_char_p(rootCertPin.encode('utf-8')),  #根证书密码
    ctypes.c_char_p('1'.encode('utf-8')), #证书类型
    ctypes.byref(szP7),     #P7包       
    ctypes.byref(intPara))
  
print (errorCode)
szP7Temp = ctypes.string_at(szP7, intPara.value)
print("szP7Temp:", szP7Temp)
base64p7 = base64.b64encode(szP7Temp)
print("base64p7:", base64p7)
'''

