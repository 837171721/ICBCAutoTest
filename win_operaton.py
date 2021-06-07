# coding=utf-8
'''
Created on 2021.6.1

@author: wsk

'''
import subprocess
import time
from pyautogui import sleep
import pyautogui
import uiautomation as auto
from pymouse import PyMouse
from pykeyboard import PyKeyboard
from uiautomation.uiautomation import ComboBoxControl
import win32gui
import win32con
import win32api
import win32com.client
from GlobalConfigure import *
import traceback


class EsWinOperation:
    def __init__(self):
        self.m = PyMouse()
        self.k = PyKeyboard()
        self.hwnd = None

    def es_win_open(self, path):
        '''
        打开文件
        :param path: 文件路径
        return:无
        '''
        # try:
        subprocess.Popen(path)
        time.sleep(2)
        # except:
        # traceback.print_exc()
        # print('发生异常')

    def es_win_close(self):
        '''
        关闭文件
        '''
        try:
            self.hwnd.ButtonControl(Name='关闭').Click()
        except Exception as e:
            traceback.print_exc()
            return e

    def es_win_get_hwnd(self, win_name):
        '''
        获取窗口句柄
        :param win_name:窗口名称
        :return 窗口句柄
        '''
        self.hwnd = auto.WindowControl(
            searchDepth=1, Name=win_name)
        self.hwnd.SetTopmost(True)
        # return self.hwnd

    def es_win_btnclick(self, button_name):
        '''
        点击窗口按钮
        :param button_name: 按钮名称
        :return:
        '''
        try:
            self.hwnd.ButtonControl(Name=button_name).Click()
        except Exception as e:
            traceback.print_exc()
            # return e

    def es_win_combox_select(self, comboxid, optionid):
        '''
        下拉框选择
        :pamam comboxid: 组合框的AutomationId属性
        :param optionid: 选项的Name属性
        :return: 
        '''
        self.hwnd.ComboBoxControl(AutomationId=comboxid).Click()
        self.hwnd.ListItemControl(Name=optionid).Click()

    def es_win_tabcontrol_select(self, option_name):
        '''
        选项卡选择
        :param option_name: 选项的name属性
        :return:
        '''
        self.hwnd.TabItemControl(Name=option_name).Click()

    def es_win_get_childwindow_hwnd(self, window_name):
        '''
        获取子窗口句柄
        :param window_name :窗口名称
        :return 子窗口句柄
        '''
        win_hwnd = auto.WindowControl(searchDepth=2, Name=window_name)
        return win_hwnd

    def es_win_set_edit(self, automationid, str):
        '''
        设置编辑框内容
        :param automationid : 编辑框AutomationId
        :param str : 需要输入的字符串
        :return 无
        '''
        edit = auto.EditControl(AutomationId=automationid)
        edit.Click()
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('backspace')
        edit.SendKeys(str)

    def es_win_get_edit(self, automationid):
        '''
        获取编辑框内容
        :param autionmationid:编辑框的AutomationId
        :return 编辑框内容
        '''
        text_element = auto.TextControl(AutomationId=automationid)
        return text_element.Name

    def es_win_checkbox_select(self, automationid):
        '''
        复选框选择
        :param automationid: 复选框的AutomationId
        return ： 无
        '''
        self.hwnd.CheckBoxControl(AutomationId=automationid).Click()

    def es_win_get_static(self, automationid):
        '''
        获取静态框文本内容
        :param 
        '''
        text_value = auto.TextControl(AutionmationId=automationid)
        return text_value.Name


def es_win_check_all():
    '''
    ctrl + A 全选
    :return: 无
    '''
    # 中行的P10转P7工具无法使用ctrl A 复制
    # pyautogui.rightClick()
    # sleep(1)
    # pyautogui.typewrite(['down','down', 'down', 'down', 'down', 'down', 'enter'])
    pyautogui.hotkey('ctrl', 'c')


def es_win_copy():
    '''
    ctrl + c 复制
    '''
    pyautogui.hotkey('ctrl', 'c')


def es_win_paste():
    '''
    ctrl + v 粘贴
    '''
    pyautogui.hotkey('ctrl', 'v')


def es_win_get_filelist(dir):
    '''
    获取指定目录下的文件列表（包括文件夹）
    :param dir:指定目录
    return :文件列表
    '''
    file_list = []
    for files in os.listdir(dir):
        file_list.append(files)
    return file_list


def es_win_file_exits(dir_path,file_list):
    '''
    查找某文件是否存在(可以传入多个文件)
    :param dir_path 路径
    :param file_list:文件列表
    :return : 全部存在，返回True，否则返回False
    '''
    for files in file_list:
        result = True
        path = dir_path + '\\' + str(files)
        if False == os.path.exists(path):
            result = False
    return result

def es_win_file_notexits(dir_path,file_list):
    '''
    查找某文件是否不存在(可以传入多个文件)
    :param dir_path 路径
    :param file_list:文件列表
    :return ：文件全部不存在，返回True，否则返回False
    '''
    for files in file_list:
        result = True
        path = dir_path + '\\' + str(files)
        if os.path.exists(path):
            result = False
    return result


def es_win_window_exits(win_class, win_name):
    '''
    判断某主窗口是否存在
    :param win_class:字符型，窗口的类名
    :param win_name:字符型，窗口名
    :return 窗口存在返回True,不存在返回False
    '''
    if win32gui.FindWindow(win_class, win_name):
        return True
    else:
        return False


if __name__ == '__main__':
    test = EsWinOperation()
    test.es_win_open(
        r'C:\Program Files (x86)\ICBCEbankTools\MingWah\MWICBCUKeyToolU.exe')
    test.es_win_get_hwnd("U盾客户端管理工具（明华&文鼎创）")
    test.es_win_btnclick('修改U盾密码')
    test.es_win_get_hwnd('修改U盾密码')
    test.es_win_set_edit('1266', '123456')
    time.sleep(5)
    # test.es_win_close()
    # boc = EsWinOperation()
    # boc.es_win_open(r'E:\SVN-自动化脚本\BOC\Import\P10解析工具\P10TOCertTool.exe')
    # boc.es_win_set_edit(automationid='1000', str=' ')
    # es_win_paste()
    # boc.es_win_checkbox_select(automationid='1007')
    # boc.es_win_btnclick(button_name='生成')
    # boc.es_win_close()
