#coding=utf-8
'''
Created on 2021.6.1

@author: wsk

'''
import struct
from ctypes import *
# from SetUp import *
test_python = 64
if 64 == test_python:
    lib = cdll.LoadLibrary("./Lib/EsTestMidware/EsTestMidware_x64.dll")
    # lib = windll.LoadLibrary("./Lib/EsTestMidware/EsTestMidware_x64.dll")
else:
    lib = windll.LoadLibrary("./Lib/EsTestMidware/EsTestMidware.dll")


class EsTest_Midware:

    def __init__(self):
        lib.EsTestMidwareInit()  # 初始化EsTestMidware
        self.p = create_string_buffer(4)
        self.u4SlotId = c_ulong(0)
        self.c_ulong_p = POINTER(c_ulong)

    def Power_OnAndOff(self, Us=100, WaitTimeMs=100):
        lib.EsPowerOffOpenDev(self.p)  # 获取掉电设备端口号
        pu4SlotId = struct.unpack('<L', bytes(self.p.raw))
        pu4SlotId = pu4SlotId[0]
        on_result = lib.EsPowerOffSetOff(pu4SlotId, Us)  # 掉电设备下电
        off_result = lib.EsPowerOffSetOn(pu4SlotId, WaitTimeMs)  # 掉电设备上电
        lib.EsPowerOffCloseDev()  # 关闭掉电设备
        return pu4SlotId, on_result, off_result

    def PressKey(self, KeyType, DelayCount=100):  # 按下+弹起
        lib.EsAutoPressOpenDev(self.p)  # 获取按键设备端口号
        pu4SlotId = struct.unpack('<L', bytes(self.p.raw))
        pu4SlotId = pu4SlotId[0]
        lib.EsAutoPressKey(pu4SlotId, KeyType, DelayCount)
        # lib.EsAutoPressCloseDev(self.pu4SlotId)

    def PressKeyDo(self, KeyType):  # 按下
        lib.EsAutoPressOpenDev(self.p)  # 获取按键设备端口号
        pu4SlotId = struct.unpack('<L', bytes(self.p.raw))
        pu4SlotId = pu4SlotId[0]
        lib.EsAutoPressKeyDo(pu4SlotId, KeyType)

    def PressKeyUndo(self, KeyType):  # 弹起
        lib.EsAutoPressOpenDev(self.p)  # 获取按键设备端口号
        pu4SlotId = struct.unpack('<L', bytes(self.p.raw))
        pu4SlotId = pu4SlotId[0]
        lib.EsAutoPressKeyUndo(pu4SlotId, KeyType)

    # def PressKeyUndo(self,KeyType): # 弹起
    #     lib.EsAutoPressOpenDev(self.p) # 获取按键设备端口号
    #     pu4SlotId = struct.unpack('<L', bytes(self.p.raw))
    #     pu4SlotId = pu4SlotId[0]
    #     lib.EsAutoPressKeyUndo(pu4SlotId,KeyType)

    # def GetMediaId(self): # 获取设备ID
    #     lib.EsUsbKeyOpenDev(self.p)  # 获取USBKEY设备端口号
    #     pu4SlotId = struct.unpack('<L', bytes(self.p.raw))
    #     pu4SlotId = pu4SlotId[0]
    #     output = create_string_buffer(16,b'00')
    #     lib.EsUsbKeyGetMediaId(pu4SlotId,output)
    #     outputTemp = struct.unpack('<16s', output)
    #     result = outputTemp[0]
    #     result = str(result, encoding = "utf-8")
    #     #bytes.decode(result)
    #     #lib.EsUsbKeyCloseDev(pu4SlotId)
    #     return result

    def GetMediaId(self):  # 获取设备ID
        lib.EsUsbKeyOpenDev.argtypes = [self.c_ulong_p]
        result = lib.EsUsbKeyOpenDev(byref(self.u4SlotId))  # 获取USBKEY设备端口号
        pszMediaId = create_string_buffer(16)
        lib.EsUsbKeyGetMediaId.argtypes = [c_ulong, c_char_p]
        lib.EsUsbKeyGetMediaId(self.u4SlotId.value, pszMediaId)
        MediaId = pszMediaId.value
        #MediaId = MediaId.decode('utf-8')
        MediaId = str(MediaId, 'utf-8')
        return MediaId

    def GetRegistryValue(self, u4Key, pszSubKey, pszValueName):  # 获取注册表项
        pszData = create_string_buffer(300)
        pu4DataType = c_ulong(0)
        pu4Datasize = c_ulong(300)
        pszSubKey_p = c_char_p(pszSubKey)
        pszValueName_p = c_char_p(pszValueName)
        pointer = POINTER(c_ulong)
        lib.EsRegQueryValue.argtypes = [
            c_ulong, c_char_p, c_char_p, pointer, c_char_p, pointer]  # 输入参数类型转换
        lib.EsRegQueryValue.restype = c_ulong
        result = lib.EsRegQueryValue(u4Key, pszSubKey_p, pszValueName_p, byref(
            pu4DataType), pszData, byref(pu4Datasize))
        return pszData.value, pu4DataType.value, pu4Datasize.value, result

    def Release(self):
        lib.EsTestMidwareRelease()  # 反初始化


if __name__ == '__main__':
    EsTestMidware = EsTest_Midware()
    result = EsTestMidware.GetMediaId()
    print(result)
