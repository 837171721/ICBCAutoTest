#coding=utf-8
import os
import time
from GlobalConfigure import *
import random 
import win32gui  
import win32api,win32con  
import pyautogui as pag
#定义结构体，存储当前窗口坐标  
os.startfile(AuxTool)
time.sleep(2)
P10Temp="MIICdzCCAV8CADAzMRQwEgYDVQQDDAtUZXN0UlNBMjA0ODEbMBkGA1UECgwScnNhcGVyY2ExMzkuY29tLmNuMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAzFFA2Kmq9mW+Mc/UR4FKGiPsbaw5bmZQyFGMYVMGZjc20QKEnECvAUsLtj6sVmH/5QiqEGrKwcxoRQVnI9Ud2cuXZCOwnJoYmcmazkMD11kNXuGkE3chcQI1r+WbIoUPlXptBhMuy1Asd2bCpr0PPH6iZqWCifWZs0wZqNd10j+4hjAvr8dJ6hWdKYUMHrm4giRN0DNVbTdhP+9nNrOTwyEoi7ZR0vTnJyZZsB9+YlccEkK2OJtx4RO6EpSdxn8nuVpXgXQWwWHmIzpRfqvkKlt6nUVDx04PxNbstHciTGr1yib2U7u4PI2BSHLbxMGfU5E+F3Hk/5n48PeGKYFCVQIDAQABoAAwDQYJKoZIhvcNAQEFBQADggEBABGqRlwNN5pBjOaaQLaeLgO/NV45hzDoKGZ7eagLdk1PtHqqeD9QKVCSYPmERlWFs7goWAjNW4cH7NXlY2/FXKP8iCEE7MaGA9m9GP0UZ/DzEBvaUgTfnlK6YrztOpLoEDwbV+cJdJLsWkkoR5cxWw80d0uDvFU8ERlCI1TpCojPc0Xwb7+GuqDm8z9tC8FqkO+KFb55NsmxZMukCxs1vPbrCGXcwvfwLNL/8jyDr39pEoHP9SX+u18cva74N+MlMgjSmwqnlLloTGMj1VQ7mjPcwDbNUnURoWo9K5y+qfN/utq/RJkBWU+axnMMMu46ocGF4vtfEZHpti24i08I8TU=||MIH2MIGcAgAwOzEcMBoGA1UEAwwTVGVzdFNNMi5wLjAyMDAuMDEwMTEbMBkGA1UECgwScnNhcGVyY2ExMzkuY29tLmNuMFkwEwYHKoZIzj0CAQYIKoEcz1UBgi0DQgAEolKcgfSooekMifP7gUH9qH8tQvBTfsnLxwL57txvUJYZ25FZXFf2OSv+wh6RNiQKkWiZj068xojc5rayy2swGKAAMAwGCCqBHM9VAYN1BQADRwAwRAIgPRF2SPO/4mVK8MjPePf3sISnHehJ3AEixcfW5IbAWKkCIDDvo6L3Ka0ygXdZ/6xNyjWgDS2yJpE+0yt60eW6EKGi"
class RECT(ctypes.Structure):  
    _fields_ = [('left', ctypes.c_int),  
                ('top', ctypes.c_int),  
                ('right', ctypes.c_int),  
                ('bottom', ctypes.c_int)] 
    
DialogName="ICBC OCX Auxiliary Tool V1.0.0.4"
win = win32gui.GetForegroundWindow()
while win == 0:
    win = win32gui.GetForegroundWindow()
#HWND = win32gui.GetForegroundWindow()#获取当前窗口句柄  
rect = RECT()
ctypes.windll.user32.GetWindowRect(win, ctypes.byref(rect))#获取当前窗口坐标  
print( rect._fields_.count('left'),rect._fields_.count('top'),rect._fields_.count('right'),rect._fields_.count('bottom'))
pag.click(rect.left, rect.top)
pag.hotkey('ctrl','v')
time.sleep(2)
pag.moveTo(rect.left+200, rect.top+240)
pag.click(rect.left+200, rect.top+240)
#关闭p10转p7工具
#os.system('taskkill /F /IM IcbcOcxAuxTool_rls.exe')