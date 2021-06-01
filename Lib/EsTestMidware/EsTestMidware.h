#ifndef _ESTESTMIDWARE_H_
#define _ESTESTMIDWARE_H_

// ��Ӧ������Bitλ��������(���Զ������豸�й�)
#define KEY_TYPE_BIT_CANCEL         0x04
#define KEY_TYPE_BIT_ENTER          0x03
#define KEY_TYPE_BIT_PAGEDOWN       0x01
#define KEY_TYPE_BIT_PAGEUP         0x02

#ifdef __cplusplus
extern "C"
{
#endif

    u4 CALL_TYPE EsTestMidwareInit(void);
    u4 CALL_TYPE EsTestMidwareRelease(void);
    // �Զ����µ�ӿ�
    u4 CALL_TYPE EsPowerOffEnumDev(u4* pu4SlotIdList, u4* pu4SlotCount);
    u4 CALL_TYPE EsPowerOffOpenDev(u4* pu4SlotId);
    u4 CALL_TYPE EsPowerOffCloseDev(u4* pu4SlotId);
    u4 CALL_TYPE EsPowerOffSetOff(u4 u4SlotId, u4 u4Us);
    u4 CALL_TYPE EsPowerOffSetOn(u4 u4SlotId, u4 u4WaitTimeMs);
    // �Զ������ӿ�
    u4 CALL_TYPE EsAutoPressEnumDev(u4* pu4SlotIdList, u4* pu4SlotCount);
    u4 CALL_TYPE EsAutoPressOpenDev(u4* pu4SlotId);
    u4 CALL_TYPE EsAutoPressCloseDev(u4* pu4SlotId);
    u4 CALL_TYPE EsAutoPressKey(u4 u4SlotId, u4 u4KeyType, u4 u4DelayCount);
    // ���ư��������뵯���������ӿ���Ҫ�������ã��Ұ������Ͷ�����Ҫ��ͬ�����򷵻ش���
    u4 CALL_TYPE EsAutoPressKeyDo(u4 u4SlotId, u4 u4KeyType);
    u4 CALL_TYPE EsAutoPressKeyUndo(u4 u4SlotId, u4 u4KeyType);
    // Ӧ�ýӿ�
    u4 CALL_TYPE EsUsbKeyEnumDev(u4* pu4SlotIdList, u4* pu4SlotCount);
    u4 CALL_TYPE EsUsbKeyOpenDev(u4* pu4SlotId);
    u4 CALL_TYPE EsUsbKeyCloseDev(u4* pu4SlotId);
    u4 CALL_TYPE EsUsbKeyGetMediaId(u4 u4SlotId, char* pszMediaId);
    // ���� u4Keyȡֵ
    //     HKEY_CLASSES_ROOT                   0x80000000
    //     HKEY_CURRENT_USER                   0x80000001
    //     HKEY_LOCAL_MACHINE                  0x80000002
    //     HKEY_USERS                          0x80000003
    //     HKEY_PERFORMANCE_DATA               0x80000004
    //     HKEY_PERFORMANCE_TEXT               0x80000050
    //     HKEY_PERFORMANCE_NLSTEXT            0x80000060
    //     HKEY_CURRENT_CONFIG                 0x80000005
    //     HKEY_DYN_DATA                       0x80000006
    //���� pu4DataType�ķ���ֵ
    //     REG_NONE                    ( 0 )   // No value type
    //     REG_SZ                      ( 1 )   // Unicode nul terminated string
    //     REG_EXPAND_SZ               ( 2 )   // Unicode nul terminated string
    //     REG_BINARY                  ( 3 )   // Free form binary
    //     REG_DWORD                   ( 4 )   // 32-bit number
    //     REG_DWORD_LITTLE_ENDIAN     ( 4 )   // 32-bit number (same as REG_DWORD)
    //     REG_DWORD_BIG_ENDIAN        ( 5 )   // 32-bit number
    //     REG_LINK                    ( 6 )   // Symbolic Link (unicode)
    //     REG_MULTI_SZ                ( 7 )   // Multiple Unicode strings
    //     REG_RESOURCE_LIST           ( 8 )   // Resource list in the resource map
    //     REG_FULL_RESOURCE_DESCRIPTOR ( 9 )  // Resource list in the hardware description
    //     REG_RESOURCE_REQUIREMENTS_LIST ( 10 )
    //     REG_QWORD                   ( 11 )  // 64-bit number
    //     REG_QWORD_LITTLE_ENDIAN     ( 11 )  // 64-bit number (same as REG_QWORD)
    // ��ȡע�����Ϣ
    u4  CALL_TYPE EsRegQueryValue(IN u4 u4Key, IN char* pszSubKey, IN char* pszValueName, OUT u4* pu4DataType, OUT char* pszData, INOUT u4* pu4Datasize);
    // ö��ע��������Ӽ���ֵ
    // ����ѭ��ö��ָ��Ŀ¼�µ��Ӽ���ֵ��ÿ�ζ�ȡ�ɹ��󷵻�0��ֱ������ERROR_COMMON_LIST_TAIL(0xE060000D)����ȡ����
    u4  CALL_TYPE EsRegEnumValue(u4 u4Key, char* pszSubKey, char* pszValueName,u4* pu4ValueNameLen, u4* pu4DataType, char* pszData, u4* pu4Datasize);
#ifdef __cplusplus
};
#endif
#endif
