# import logging
# import pyautogui
import subprocess
from time import sleep

# LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
# logging.basicConfig(filename='logtest.txt', filemode= 'a', format=LOG_FORMAT, level= logging.DEBUG)
# logging.debug('this is adebug log')
# pyautogui.alert(text='This is an alert box.', title='Test')
# pyautogui.confirm('Enter option.', buttons=['A', 'B', 'C'])
# a = pyautogui.password('Enter password (text will be hidden)')
# print(a)
# subprocess.Popen(
#     'E:\\SVN-自动化脚本\\ICBC\\Import\\驱动安装包\\V2.5.0.11\\ICBC_MW_UShield2_Install.exe')
subprocess.Popen(
    'E:\SVN-自动化脚本\ICBC\Import\驱动安装包\V2.5.0.11\ICBC_MW&WDC_UShield2_Install.exe')
sleep(5)
