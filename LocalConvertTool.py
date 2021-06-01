'''
Created on 2018.03.28
@author: ys
'''
import os
import time
import win32gui
import ctypes
import operator
import win32api,win32con
import win32process
import subprocess
import pyautogui as pag
from GlobalConfigure import *
from GlobalConfigure import levels

from logTest import SysClass, LoggerClass
#from P102P7Test import RECT
conf  = LoggerClass(loglevel=levels.get("info"), logger="LocalConvertTool.py")
logger=conf.getlogger()

pag.PAUSE = 1
pag.FAILSAFE = False  #设置安全属性，在FJQ机器上出现的问题
DialogName="ICBC OCX Auxiliary Tool V1.0.0.6"
#str_BtnName_GenCert_of_p102p7="生成证书"
#str_BtnName_Reset_of_p102p7="重置"

#定义结构体，存储当前窗口坐标
class RECT(ctypes.Structure):
    _fields_ = [('left', ctypes.c_int),
                ('top', ctypes.c_int),
                ('right', ctypes.c_int),
                ('bottom', ctypes.c_int)]

def open_window(file_path):
    hwnd=[]
    #logger.warning("======open the tool starting======")
    while [] == hwnd:
        tool = subprocess.Popen(AuxTool)
        time.sleep(1)
        hwnd = get_hwnds_for_pid(tool.pid)
        #logger.warning("hwnd=%s", hwnd)
    #logger.warning("======open the tool end======")
    if [] != hwnd:
        for hwnd in get_hwnds_for_pid(tool.pid):
            win32gui.SetForegroundWindow(hwnd)
            pag.click()  # 防止鼠标焦点乱跑，定位在当前对话框上
    #print( rect._fields_.count('left'),rect._fields_.count('top'),rect._fields_.count('right'),rect._fields_.count('bottom'))
    return hwnd

def get_hwndCoordinate_for_pid(pid):
    '''
    hwndParent = win32gui.FindWindow(None,DialogName)
    while hwndParent == 0:
        hwndParent = win32gui.FindWindow(None,DialogName)
    '''
    for hwnd in get_hwnds_for_pid (pid):
        #print (hwnd, "=>", win32gui.GetWindowText (hwnd))
        win32gui.SetForegroundWindow(hwnd)
        pag.click() #防止鼠标焦点乱跑，定位在当前对话框上
        #print( rect._fields_.count('left'),rect._fields_.count('top'),rect._fields_.count('right'),rect._fields_.count('bottom'))
    return hwnd

def get_hwnds_for_pid (pid):
    def callback (hwnd, hwnds):
        if win32gui.IsWindowVisible (hwnd) and win32gui.IsWindowEnabled (hwnd):
            _, found_pid = win32process.GetWindowThreadProcessId (hwnd)
            #print(hwnd, "=>", win32gui.GetWindowText(hwnd))
            #print("hwnd=%s,found_pid=%s",hwnd,found_pid)
            if found_pid == pid:
                hwnds.append (hwnd)
            return True
    hwnds = []
    win32gui.EnumWindows (callback, hwnds)
    return hwnds

def get_child_windows(parent):
    '''
    获得parent的所有子窗口句柄
     返回子窗口句柄列表
     '''
    if not parent:
        return
    hwndChildList = []
    win32gui.EnumChildWindows(parent, lambda hwnd, param: param.append(hwnd),  hwndChildList)
    return hwndChildList

class ToolConvert:
    def __init__(self,hwnd,hwnd_coodinate):
        self.hwnd=hwnd
        self.hwnd_coodinate=hwnd_coodinate
        #hwnd_title=win32gui.GetWindowText(self.hwnd)

    def mouseFocus_locate(self):
        try:
            #定位鼠标位置，确保鼠标焦点定位在对话框上
            screenX,screenY=pag.size() #获取屏幕分辨率
            MousePos_X=screenX/2
            MousePos_Y=screenY/3
            #pag.moveTo(MousePos_X, MousePos_Y)
        except Exception as e:
            pass
        return

    def FuncP102P7(self):
        coodRect = self.hwnd_coodinate
        self.mouseFocus_locate()

        Edit_P10_X=coodRect.left + 100   #生成证书按钮坐标位置
        Edit_P10_Y=coodRect.top + 100
        #pag.moveTo(Edit_P10_X, Edit_P10_Y)
        pag.click(Edit_P10_X, Edit_P10_Y)
        pag.hotkey('ctrl','v')#粘贴P10数据
        #time.sleep(0.05)
                
        #生成按钮点击
        str_BtnName_GenCert_of_p102p7="生成证书"
        Btn_GenCert_X=0
        Btn_GenCert_Y=0
        hwndChildList=get_child_windows(self.hwnd)
        for i in range(0, len(hwndChildList) - 1):
            childWndTitlename = win32gui.GetWindowText(hwndChildList[i])
            childWndClsname = win32gui.GetClassName(hwndChildList[i])            
            if operator.eq(str_BtnName_GenCert_of_p102p7,childWndTitlename) and operator.eq("Button",childWndClsname):
                left, top, right, bottom = win32gui.GetWindowRect(hwndChildList[i])
                #logger.warning("%s,%s",childWndTitlename,childWndClsname)
                Btn_GenCert_X = int (left+right)/2  # 生成证书按钮坐标位置
                Btn_GenCert_Y = int (top+bottom)/2
                #pag.moveTo(Btn_GenCert_X, Btn_GenCert_Y)
                pag.click(Btn_GenCert_X, Btn_GenCert_Y)

        #P7框坐标位置定位并粘贴数据
        P7_Edit_X=Btn_GenCert_X
        P7_Edit_Y=Btn_GenCert_Y + 100  #P7框坐标位置
        #pag.moveTo(P7_Edit_X, P7_Edit_Y)
        pag.click(P7_Edit_X, P7_Edit_Y)
        pag.hotkey('ctrl','a')#复制P7数据
        pag.hotkey('ctrl','c')
        time.sleep(0.05)

    def FuncGetCoodinate_With_AdminKey(self):
        self.mouseFocus_locate()
        coodRect=self.hwnd_coodinate

        #设置保密密钥菜单位置
        View_SetAdminKey_X=coodRect.left + 125
        View_SetAdminKey_Y=coodRect.top + 50
        #pag.moveTo(View_SetAdminKey_X, View_SetAdminKey_Y)
        pag.click(View_SetAdminKey_X, View_SetAdminKey_Y)

        #重置
        str_OldBtn="旧"
        OldMidBtn_Y=0
        str_NewBtn="新"
        NewMidBtn_Y=0
        str_BtnName_Reset="重置"
        hwndChildList=get_child_windows(self.hwnd)
        for i in range(0, len(hwndChildList) - 1):
            childWndTitlename = win32gui.GetWindowText(hwndChildList[i])
            childWndClsname = win32gui.GetClassName(hwndChildList[i])
            if operator.eq(str_NewBtn,childWndTitlename) and operator.eq("Button",childWndClsname):
                NewBtn_left, NewBtn_top, NewBtn_right, NewBtn_bottoms = win32gui.GetWindowRect(hwndChildList[i])
                #print(NewBtn_top,NewBtn_bottoms)
                #NewMidBtn_Y=int ((NewBtn_top+NewBtn_bottoms)/2)
                NewMidBtn_Y=int(NewBtn_top)
            elif operator.eq(str_OldBtn,childWndTitlename) and operator.eq("Button",childWndClsname):
                OldBtn_left, OldBtn_top, OldBtn_right, OldBtn_bottom = win32gui.GetWindowRect(hwndChildList[i])
                OldMidBtn_Y=int ((OldBtn_top+OldBtn_bottom)/2)
            elif operator.eq(str_BtnName_Reset,childWndTitlename) and operator.eq("Button",childWndClsname):
                left, top, right, bottoms = win32gui.GetWindowRect(hwndChildList[i])
                Btn_X=int ((left+right) /2)
                Btn_Y=int ((top+bottoms) /2)
                pag.click(Btn_X, Btn_Y)
            else:
                continue
        strStaticComboKeyType="密钥体系："
        strStaticKeyValue="密钥值："
        strStaticComboEncAlg="加密算法："
        strStaticCount="序号："
        childWndTitlename=0
        childWndClsname=0
        KeyType=RECT()
        EncAlg=RECT()
        KeyValue=RECT()
        Count=RECT()
        for j in range(0, len(hwndChildList) - 1):
            childWndTitlename = win32gui.GetWindowText(hwndChildList[j])
            childWndClsname = win32gui.GetClassName(hwndChildList[j])
            #print(childWndTitlename,childWndClsname)
            if operator.eq(strStaticComboKeyType,childWndTitlename) and operator.eq("Static",childWndClsname):
                left, top, right, bottom = win32gui.GetWindowRect(hwndChildList[j])
                tempY=int ((top+bottom)/2)                
                if tempY < NewMidBtn_Y:
                    #print("旧密钥体系X",tempY)
                    KeyType.left= int ((left+right)/2+100)  # 旧密钥体系X
                    KeyType.right= int ((top+bottom)/2)  # 旧密钥体系X
                else:
                    #print("新密钥体系X",tempY)
                    KeyType.top= int ((left+right)/2+100)  # 新密钥体系X
                    KeyType.bottom= int ((top+bottom)/2)  # 新密钥体系Y
            elif operator.eq(strStaticComboEncAlg,childWndTitlename) and operator.eq("Static",childWndClsname):
                left, top, right, bottom = win32gui.GetWindowRect(hwndChildList[j])
                tempY=int ((top+bottom)/2)
                if tempY < NewMidBtn_Y:
                    #print("旧加密算法X",tempY)
                    EncAlg.left= int ((left+right)/2+100)  # 旧加密算法X
                    EncAlg.right= int ((top+bottom)/2)  # 旧加密算法Y
                else:
                    #print("新加密算法X",tempY)
                    EncAlg.top= int ((left+right)/2+100)  # 新加密算法X
                    EncAlg.bottom= int ((top+bottom)/2)  # 新加密算法Y
            elif operator.eq(strStaticKeyValue,childWndTitlename) and operator.eq("Static",childWndClsname):
                left, top, right, bottom = win32gui.GetWindowRect(hwndChildList[j])
                tempY=int (top+bottom)/2
                if tempY < NewMidBtn_Y:
                    KeyValue.left= int ((left+right)/2+100)  # 旧密钥值X
                    KeyValue.right= int ((top+bottom)/2)  # 旧密钥值Y
                else:
                    KeyValue.top= int ((left+right)/2+100)  # 新密钥值X
                    KeyValue.bottom= int ((top+bottom)/2)  # 新密钥值Y
            elif operator.eq(strStaticCount,childWndTitlename) and operator.eq("Static",childWndClsname):
                left, top, right, bottom = win32gui.GetWindowRect(hwndChildList[j])
                Count.left = int ((left+right)/2+50)  # 序号X
                #Count.right = right
                Count.top= int ((top+bottom)/2)  # 序号Y
            else:
                continue
        return  KeyType,EncAlg,KeyValue,Count

    def FuncCalAdminKeyData(self,KeyType,EncAlg,offset1,offset2,offset3,offset4):
        #旧密钥体系
        ##pag.moveTo(KeyType.left, KeyType.right)
        pag.click(KeyType.left, KeyType.right)
        ##pag.moveTo(KeyType.left, KeyType.right+offset1)
        pag.click(KeyType.left, KeyType.right+offset1)

        #旧加密算法
        ##pag.moveTo(EncAlg.left, EncAlg.right)
        pag.click(EncAlg.left, EncAlg.right)
        ##pag.moveTo(EncAlg.left, EncAlg.right+offset2)
        pag.click(EncAlg.left, EncAlg.right+offset2)

        #新密钥体系
        ##pag.moveTo(KeyType.top, KeyType.bottom)
        pag.click(KeyType.top, KeyType.bottom)
        ##pag.moveTo(KeyType.top, KeyType.bottom+offset3)
        pag.click(KeyType.top, KeyType.bottom+offset3)

        #新加密算法
        ##pag.moveTo(EncAlg.top, EncAlg.bottom)
        pag.click(EncAlg.top, EncAlg.bottom)
        ##pag.moveTo(EncAlg.top, EncAlg.bottom+offset4)
        pag.click(EncAlg.top, EncAlg.bottom+offset4)

    def FuncSetAdminKey(self,oldAdminKey,newAdminKey,olgAlgId='3DES',newAlgId='3DES',counts='00'):
        '''
                    参数说明:
            oldAdminKey:旧保护密钥值
            newAdminKey:新保护密钥值
            olgAlgId:旧保护密钥算法Id
            newAlgId:新保护密钥算法Id
            counts:更新序号，仅在新体系更新时有效
        '''

        KeyType,EncAlg,KeyValue,Count=self.FuncGetCoodinate_With_AdminKey()
        
        if '3DES'==olgAlgId and '3DES'==newAlgId: #旧体系->旧体系，默认3DES算法
            self.FuncCalAdminKeyData(KeyType,EncAlg,15,15,15,15)

        elif '3DES'==olgAlgId and '3DES'!=newAlgId: #旧体系->新体系，默认3DES算法
            if 'AES'==newAlgId:
                self.FuncCalAdminKeyData(KeyType,EncAlg,15,15,30,15)
            else:
                self.FuncCalAdminKeyData(KeyType,EncAlg,15,15,30,30)

        elif '3DES'!=olgAlgId and '3DES'!=newAlgId: #新体系->新体系
            if 'AES'==olgAlgId and 'AES'==newAlgId:
                self.FuncCalAdminKeyData(KeyType,EncAlg,30,15,30,15)
            elif 'AES'==olgAlgId and 'SM4'==newAlgId:
                self.FuncCalAdminKeyData(KeyType,EncAlg,30,15,30,30)
            elif 'SM4'==olgAlgId and 'AES'==newAlgId:
                self.FuncCalAdminKeyData(KeyType,EncAlg,30,30,30,15)
            elif 'SM4'==olgAlgId and 'SM4'==newAlgId:
                self.FuncCalAdminKeyData(KeyType,EncAlg,30,30,30,30)
        else:
            logger.warning("不支持新体系转旧体系")
            #不支持00

        #旧密钥值
        #pag.moveTo(KeyValue.left+100, KeyValue.right)
        pag.click(KeyValue.left+100, KeyValue.right)
        pag.typewrite(oldAdminKey)

        #新密钥值
        #pag.moveTo(KeyValue.top+100, KeyValue.bottom)
        pag.click(KeyValue.top+100, KeyValue.bottom)
        pag.typewrite(newAdminKey)

        #序号
        if newAlgId != '3DES':
            ##pag.moveTo(Count.left+100, Count.top)
            pag.click(Count.left, Count.top)
            pag.hotkey('ctrl','a')  #下次使用前选中
            pag.typewrite(counts)

        str_BtnName_AdminData="计算更新密钥指令"
        hwndChildList=get_child_windows(self.hwnd)
        for i in range(0, len(hwndChildList) - 1):
            childWndTitlename = win32gui.GetWindowText(hwndChildList[i])
            childWndClsname = win32gui.GetClassName(hwndChildList[i])
            if operator.eq(str_BtnName_AdminData,childWndTitlename) and operator.eq("Button",childWndClsname):
                left, top, right, bottom = win32gui.GetWindowRect(hwndChildList[i])
                Btn_X=int ((left+right)/2)  #计算更新保护密钥 按钮
                Btn_Y=int ((top+bottom)/2)
                pag.click(Btn_X,Btn_Y)
                #pag.moveTo(Btn_X,Btn_Y+100)
                pag.click(Btn_X,Btn_Y+100)
                pag.hotkey('ctrl','a')      #复制保护密钥数据
                pag.hotkey('ctrl','c')
                time.sleep(0.1)
                break
        
    def FuncSecInitCard(self,str_MediaID,str_AdminKey, str_UkeyRand, AdminAlgId='AES'):
        coodRect = self.hwnd_coodinate
        self.mouseFocus_locate()
        #设置初始化菜单位置
        View_SetAdminKey_X=coodRect.left + 200
        View_SetAdminKey_Y=coodRect.top + 50
        #pag.moveTo(View_SetAdminKey_X, View_SetAdminKey_Y)
        pag.click(View_SetAdminKey_X, View_SetAdminKey_Y)
        #
        src_BtnName_Reset="重置"
        #str_BtnName_initData="获取数据"
        str_BtnName_initData="计算初始化数据"        
        resetBtn_Y=0
        Btn_initData_X=0
        Btn_initData_Y=0
        hwndChildList=get_child_windows(self.hwnd)
        for n in range(0, len(hwndChildList) - 1):
            childWndTitlename = win32gui.GetWindowText(hwndChildList[n])
            childWndClsname = win32gui.GetClassName(hwndChildList[n])
            #print(childWndTitlename,childWndClsname)
            if operator.eq(src_BtnName_Reset,childWndTitlename) and operator.eq("Button",childWndClsname):
                left, top, right, bottom = win32gui.GetWindowRect(hwndChildList[n])
                resetBtn_Y = int ((top+bottom)/2)
            if operator.eq(str_BtnName_initData,childWndTitlename) and operator.eq("Button",childWndClsname):
                left, top, right, bottom = win32gui.GetWindowRect(hwndChildList[n])
                Btn_initData_X = int (left+right)/2  # 初始化数据
                Btn_initData_Y = int (top+bottom)/2

        src_static_mediaID="U盾MediaID:"
        src_static_adminKey="保护密钥值："
        src_static_algId="密钥算法："
        #src_static_base64Data="Base64编码："
        src_static_base64Data="U盾随机数"
        childWndTitlename=0
        childWndClsname=0
        for i in range(0, len(hwndChildList) - 1):
            childWndTitlename = win32gui.GetWindowText(hwndChildList[i])
            childWndClsname = win32gui.GetClassName(hwndChildList[i])
            if operator.eq(src_static_mediaID,childWndTitlename) and operator.eq("Static",childWndClsname):
                left, top, right, bottom = win32gui.GetWindowRect(hwndChildList[i])
                Edit_X = int ((left+right)/2+100)  # 介质序列号
                Edit_Y = int ((top+bottom)/2)
                pag.click(Edit_X, Edit_Y)
                pag.typewrite(str_MediaID)
            elif operator.eq(src_static_adminKey,childWndTitlename) and operator.eq("Static",childWndClsname):
                left, top, right, bottom = win32gui.GetWindowRect(hwndChildList[i])
                Edit_X = int ((left+right)/2+100)  # 保护密钥值
                Edit_Y = int ((top+bottom)/2)
                pag.click(Edit_X, Edit_Y)
                pag.typewrite(str_AdminKey)
            elif operator.eq(src_static_algId,childWndTitlename) and operator.eq("Static",childWndClsname):
                left, top, right, bottom = win32gui.GetWindowRect(hwndChildList[i])
                if 'SM4' == AdminAlgId:
                    Edit_X = int ((left+right)/2+100)  # 密钥算法
                    Edit_Y = int ((top+bottom)/2)
                    pag.click(Edit_X, Edit_Y)
                    pag.click(Edit_X, Edit_Y+30)
            elif operator.eq(src_static_base64Data,childWndTitlename) and operator.eq("Static",childWndClsname):
                left, top, right, bottom = win32gui.GetWindowRect(hwndChildList[i])
                Edit_X = int ((left+right)/2+100)  # Base64编码的随机数
                Edit_Y = int ((top+bottom)/2)
                pag.click(Edit_X, Edit_Y)
                pag.typewrite(str_UkeyRand)
            else:
                continue
            time.sleep(0.01)

        pag.click(Btn_initData_X, Btn_initData_Y)
        time.sleep(0.1)
        #pag.click(Btn_initData_X, Btn_initData_Y+50)
        pag.click(Btn_initData_X, Btn_initData_Y+80)
        pag.hotkey('ctrl', 'a')
        pag.hotkey('ctrl', 'c')
        time.sleep(0.01)
        
    def FuncGetBase64EncodeRandom(self):
        coodRect = self.hwnd_coodinate
        self.mouseFocus_locate()
        #设置初始化菜单位置
        View_SetAdminKey_X=coodRect.left + 200
        View_SetAdminKey_Y=coodRect.top + 50
        pag.click(View_SetAdminKey_X, View_SetAdminKey_Y)
        #
        src_BtnName_GetRandom="获取"
        Btn_GetRandom_X=0
        Btn_GetRandom_Y=0
        hwndChildList=get_child_windows(self.hwnd)
        for n in range(0, len(hwndChildList) - 1):
            childWndTitlename = win32gui.GetWindowText(hwndChildList[n])
            childWndClsname = win32gui.GetClassName(hwndChildList[n])
            #print(childWndTitlename,childWndClsname)
            if operator.eq(src_BtnName_GetRandom,childWndTitlename) and operator.eq("Button",childWndClsname):
                left, top, right, bottom = win32gui.GetWindowRect(hwndChildList[n])
                Btn_GetRandom_X = int (left+right)/2  # 初始化数据
                Btn_GetRandom_Y = int (top+bottom)/2
                pag.click(Btn_GetRandom_X,Btn_GetRandom_Y)

        pag.click(Btn_GetRandom_X-100, Btn_GetRandom_Y)
        pag.hotkey('ctrl', 'a')
        pag.hotkey('ctrl', 'c')
        time.sleep(0.01)   
    def FuncsetImportEncCertInfo(self, str_base64P10, str_AdminAlgId, str_AdminKey, str_TemKeyorRand): 
        coodRect = self.hwnd_coodinate
        self.mouseFocus_locate()

        Edit_P10_X=coodRect.left + 100   #生成证书按钮坐标位置
        Edit_P10_Y=coodRect.top + 100
        pag.click(Edit_P10_X, Edit_P10_Y)
        pag.typewrite(str_base64P10)
        #time.sleep(0.05)

        src_BtnName_Reset="重置"
        str_BtnName_certData2="生成证书2"
        resetBtn_Y=0
        Btn_certData_X=0
        Btn_certData_Y=0
        hwndChildList=get_child_windows(self.hwnd)
        for n in range(0, len(hwndChildList) - 1):
            childWndTitlename = win32gui.GetWindowText(hwndChildList[n])
            childWndClsname = win32gui.GetClassName(hwndChildList[n])
            #print(childWndTitlename,childWndClsname)
            if operator.eq(src_BtnName_Reset,childWndTitlename) and operator.eq("Button",childWndClsname):
                left, top, right, bottom = win32gui.GetWindowRect(hwndChildList[n])
                resetBtn_Y = int ((top+bottom)/2)
            if operator.eq(str_BtnName_certData2,childWndTitlename) and operator.eq("Button",childWndClsname):
                left, top, right, bottom = win32gui.GetWindowRect(hwndChildList[n])
                Btn_certData_X = int (left+right)/2  # 初始化数据
                Btn_certData_Y = int (top+bottom)/2

        src_static_adminKeySystem="密钥体系:"
        src_static_adminKey="密钥值:"
        src_static_algId="加密算法:"
        src_static_TemKeyorRand="临时工作密钥/随机数:"
        childWndTitlename=0
        childWndClsname=0
        for i in range(0, len(hwndChildList) - 1):
            childWndTitlename = win32gui.GetWindowText(hwndChildList[i])
            childWndClsname = win32gui.GetClassName(hwndChildList[i])
            if operator.eq(src_static_adminKeySystem,childWndTitlename) and operator.eq("Static",childWndClsname):
                left, top, right, bottom = win32gui.GetWindowRect(hwndChildList[i])
                if '00' == str_AdminAlgId:
                    Edit_X = int ((left+right)/2+50)  # 密钥体系
                    Edit_Y = int ((top+bottom)/2)
                    #pag.moveTo(Edit_X, Edit_Y)
                    #print(left, top, right, bottom)
                    pag.click(Edit_X, Edit_Y)
                    pag.click(Edit_X, Edit_Y+15)
            elif operator.eq(src_static_algId,childWndTitlename) and operator.eq("Static",childWndClsname):
                left, top, right, bottom = win32gui.GetWindowRect(hwndChildList[i])
                if '02' == str_AdminAlgId:
                    Edit_X = int ((left+right)/2+100)  # 密钥算法
                    Edit_Y = int ((top+bottom)/2)
                    #pag.moveTo(Edit_X, Edit_Y)
                    pag.click(Edit_X, Edit_Y)
                    #pag.moveTo(Edit_X, Edit_Y+30)
                    pag.click(Edit_X, Edit_Y+30)
            elif operator.eq(src_static_adminKey,childWndTitlename) and operator.eq("Static",childWndClsname):
                left, top, right, bottom = win32gui.GetWindowRect(hwndChildList[i])
                Edit_X = int ((left+right)/2+100)  # 保护密钥值
                Edit_Y = int ((top+bottom)/2)
                #pag.moveTo(Edit_X, Edit_Y)
                pag.click(Edit_X, Edit_Y)
                pag.typewrite(str_AdminKey)
            elif operator.eq(src_static_TemKeyorRand,childWndTitlename) and operator.eq("Static",childWndClsname):
                left, top, right, bottom = win32gui.GetWindowRect(hwndChildList[i])
                #print(left, top, right, bottom)
                Edit_X = int ((left+right)/2+100)  # Base64编码的随机数
                Edit_Y = int ((top+bottom)/2)
                #pag.moveTo(Edit_X, Edit_Y)
                pag.click(Edit_X, Edit_Y)
                pag.typewrite(str_TemKeyorRand)
            else:
                continue
            time.sleep(0.01)

        #pag.moveTo(Btn_initData_X, Btn_initData_Y)
        pag.click(Btn_certData_X, Btn_certData_Y)
        time.sleep(0.1)
        #pag.moveTo(Btn_initData_X, Btn_initData_Y+50)
        pag.click(Btn_certData_X, Btn_certData_Y+50)
        pag.hotkey('ctrl', 'a')
        pag.hotkey('ctrl', 'c')
        time.sleep(0.01)

if __name__ == '__main__':
    #测试用
    hwnd=open_window(AuxTool)
    rect=RECT()
    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect)) #获取对话框相对屏幕的坐标位置
    testView=ToolConvert(hwnd, rect)
    P10Info="MIICgzCCAWsCADA/MSAwHgYDVQQDDBdUZXN0UlNBMjA0OC5wLjAyMDAuMDEwMjEbMBkGA1UECgwScnNhcGVyY2ExMzkuY29tLmNuMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAzFFA2Kmq9mW+Mc/UR4FKGiPsbaw5bmZQyFGMYVMGZjc20QKEnECvAUsLtj6sVmH/5QiqEGrKwcxoRQVnI9Ud2cuXZCOwnJoYmcmazkMD11kNXuGkE3chcQI1r+WbIoUPlXptBhMuy1Asd2bCpr0PPH6iZqWCifWZs0wZqNd10j+4hjAvr8dJ6hWdKYUMHrm4giRN0DNVbTdhP+9nNrOTwyEoi7ZR0vTnJyZZsB9+YlccEkK2OJtx4RO6EpSdxn8nuVpXgXQWwWHmIzpRfqvkKlt6nUVDx04PxNbstHciTGr1yib2U7u4PI2BSHLbxMGfU5E+F3Hk/5n48PeGKYFCVQIDAQABoAAwDQYJKoZIhvcNAQEFBQADggEBAGiXJDLVHnEv9jiww1UiYuMPeY7JjQu7hh7zQZ6ThGekrwrJ/Gh/EFRZDDeEMiyaRcMMfI1kpahWkYDWX8etES0H5UrneZGeZXZga7+hvFmu9r48uklcCYUx/tVJnpRDLPRz7LOFZDRsU13T6gT1NDrpzdi4MJgdIEh3aqCTswMznpkHC4asaNh26qh15D46ec7GPKZWIX+esnQOI0hvXdSM2OP9kkAQqPOxGI9GOfdUJFSIF3tZ0q9ijolptxTWGndBFNhseWcMbjd8etjzJ0v2FJMcdHQgZZzIFgakWVu8EqAfJM464AGAgy184YsR0EWIHZE2JJIh2KK5W/g2U6k="

    #testView.FuncP102P7()
    testView.FuncSecInitCard('6990000017',AmdinKey_AES_new,str_Base64Data,'AES')
    #testView.FuncGetBase64EncodeRandom()
    '''
    oldAdminKey_3DES='569C9E50BD52FE9C626261EB7E3382C4'
    newAdminKey_3DES='569C9E50BD52FE9C626261EB7E3382C4'
    oldAdminKey_AES='FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'
    newAdminKey_AES='AAFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'
    newAdminKey_SM4='AAFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'
    oldAlgID='3DES'
    newAlgID='3DES'
    count='00' 
    KeyType=RECT()
    EncAlg=RECT()
    KeyValue=RECT()
    Count=RECT()      
    testView.FuncSetAdminKey(oldAdminKey_3DES,newAdminKey_3DES,oldAlgID,newAlgID,count)    
    testView.FuncSetAdminKey(oldAdminKey_AES,newAdminKey_AES,'3DES','AES',count)    
    testView.FuncSetAdminKey(newAdminKey_AES,newAdminKey_AES,'AES','AES',count)
    testView.FuncSetAdminKey(newAdminKey_AES,newAdminKey_SM4,'AES','SM4',count) 
    testView.FuncSetAdminKey(newAdminKey_SM4,newAdminKey_AES,'SM4','AES',count)   
    testView.FuncSetAdminKey(newAdminKey_SM4,newAdminKey_SM4,'SM4','SM4',count)                 
    time.sleep(0.5)
    '''
    #os.system('taskkill /F /IM IcbcOcxAuxTool_rls.exe')
