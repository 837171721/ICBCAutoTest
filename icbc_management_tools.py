# coding=utf-8
'''
Created on 2021.6.1

@author: wsk

'''
from unittest import result
from win_operaton import *
import subprocess
import time
import win32gui


class IcbcManagementTools:
    def __init__(self):
        self.test = EsWinOperation()

    def install(self, install_path):
        try:
            self.test.es_win_open(install_path)
            # "相同版本的工行U盾程序（明华文鼎创）已经在本机上安装了。是否覆盖？"
            # "较新版本的工行U盾程序（明华文鼎创）已经在本机上安装了"
            result = True
            if es_win_window_exits("#32770", "工行U盾程序（明华&文鼎创）安装向导"):
                self.test.es_win_get_hwnd("工行U盾程序（明华&文鼎创）安装向导")
                text = self.test.es_win_get_static("65535")
                if text == "相同版本的工行U盾程序（明华文鼎创）已经在本机上安装了。是否覆盖？":
                    result = '同版本覆盖安装'
                if text == "较新版本的工行U盾程序（明华文鼎创）已经在本机上安装了":
                    result = '低版本无法覆盖高版本'
                self.test.es_win_btnclick('确定')
            # 金融@家界面，等待5s
            time.sleep(5)
            # 选择语言界面
            if es_win_window_exits('#32770', "选择安装语言"):
                self.test.es_win_get_hwnd("选择安装语言")
                self.test.es_win_btnclick('确定')
            # "欢迎使用工行U盾程序（明华文鼎创）安装向导，请点击 <安装> 按钮继续您的操作。"
            if es_win_window_exits("#32770", "工行U盾程序（明华&文鼎创）安装向导"):
                self.test.es_win_get_hwnd("工行U盾程序（明华&文鼎创）安装向导")
                self.test.es_win_btnclick('安装')
                time.sleep(15)
                self.test.es_win_btnclick('完成')
            time.sleep(3)
            if es_win_window_exits("IEFrame", "中国工商银行中国网站 - Internet Explorer"):
                self.test.es_win_get_hwnd("中国工商银行中国网站 - Internet Explorer")
                self.test.es_win_close()
        except Exception as e:
            print(e)
            return '安装失败'
        else:
            return result

    def uninstall(self, path):
        '''
        卸载管理工具
        :param  path:卸载管理工具文件路径
        :return : 卸载结果
        '''
        try:
            self.test.es_win_open(path)
            self.test.es_win_get_hwnd("工行U盾程序（明华&文鼎创）卸载向导")
            self.test.es_win_btnclick('卸载')
            time.sleep(10)
            self.test.es_win_btnclick('完成')
        except Exception as e:
            print(e)
            return '卸载失败'
        else:
            return True



if __name__ == '__main__':
    test = IcbcManagementTools()
    test.install(
        r'E:\工行\测试对象\PC\驱动\V2.5.0.11\ICBC_MW&WDC_UShield2_Install.exe')
    # test.uninstall(
    #     r'C:\Program Files (x86)\ICBCEbankTools\MingWah\Uninstall.exe')
