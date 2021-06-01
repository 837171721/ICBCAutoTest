#coding=utf-8
'''
Created on 2018.07.23 @author: SYX
'''

import re         #引入正在表达式
import operator
from  GlobalConfigure import levels,log_level,AmdinKey_3DES,AmdinKey_SM4,AmdinKey_AES_old,AmdinKey_AES_new

from logTest import SysClass, LoggerClass
conf  = LoggerClass(loglevel=levels.get(log_level), logger="TestCases_GMSetNewAmdinKeyC.py")
logger=conf.getlogger()

#错误信息列表
right_info= "灌入密钥成功"
param_Err=  "灌入密钥失败:未知错误。返回码:-304 Failed Param!"
many_key_Err="灌入密钥失败:未知错误。返回码:-104 There is more than one key!"
no_key_Err= "灌入密钥失败:未知错误。返回码:-102 There is no key!"

def test_GMSetNewAmdinKeyC(ctrlObj,TestingRange,AdminKeyInfo):
    testCtrl=GMSetNewAmdinKeyCases(ctrlObj,AdminKeyInfo)  #建立类对象，打开控件测试页 
    testGMSetNewAmdinKeyCase(testCtrl,TestingRange)   #测试用例集，根据测试范围定义测试强度    
    
def testGMSetNewAmdinKeyCase(AdminKeyInfoCtrl,testRange):
    #测试用例集
    if 0 == testRange:  #详细测试
        testResult = AdminKeyInfoCtrl.positiveCase()
        #testResult = AdminKeyInfoCtrl.negativeCase_noKey()
        #testResult = AdminKeyInfoCtrl.negativeCase_manyKey()
        #testResult = AdminKeyInfoCtrl.negativeCase_manyKeyvoidPara()
        #testResult = AdminKeyInfoCtrl.negativeCase_operation()
        
    elif 1 == testRange: #验证测试
        testResult = AdminKeyInfoCtrl.positiveCase()
                
    elif 2 == testRange: #无key测试
        testResult = AdminKeyInfoCtrl.negativeCase_noKey_voidParaChoice()
        testResult = AdminKeyInfoCtrl.negativeCase_noKey_randParaChoice()
        
    elif 3 == testRange: #多key测试
        testResult = AdminKeyInfoCtrl.negativeCase_manyKey_validParaChoice()
        testResult = AdminKeyInfoCtrl.negativeCase_manyKey_voidParaChoice()
        testResult = AdminKeyInfoCtrl.negativeCase_manyKey_randParaChoice()
        
    elif 4 == testRange: #U盾在位
        testResult = AdminKeyInfoCtrl.positiveCase()
        
    else:
        a=0
       
class GMSetNewAmdinKeyCases():
    def __init__(self,testCtrl,AdminKeyInfo):
        self.testCtrl=testCtrl   #控件测试页
        self.AdminKeyAlgId=AdminKeyInfo  #保护密钥信息

    def positiveCase(self):
        #用例描述：插入1支U盾，点击保护密钥更新
        caseTitle  = "用例——插入1支U盾,点击保护密钥更新,期望更新成功"
        caseResult = None
        e=None
        testResult=''
        if '00' == self.AdminKeyAlgId[1]: #非国密盾或国密旧体系
            #旧体系->旧体系
            testResult=self.testCtrl.GMSetNewAmdinKeyC(AmdinKey_3DES,AmdinKey_3DES,'3DES','3DES')
            testResult=re.sub(re.compile('\s+'),' ',testResult)
        else:
            '''
            adminKeyInfo = self.testCtrl.get_AdminKeyInfoC()
            tempcounts = adminKeyInfo[0:2]
            tempcounts = int(tempcounts)
            if tempcounts == 99:
                tempcounts = 0
            tempcounts += 1
            tempcounts = "%02d" % tempcounts
            '''
            tempcounts=int(self.AdminKeyAlgId[2])
            if 99 == tempcounts:
                tempcounts = 0
            tempcounts += 1
            tempcounts = "%02d" % tempcounts
            if '01' == self.AdminKeyAlgId[1]: #判断为国密盾新体系 AES->AES
                #新体系AES->新体系AES
                testResult=self.testCtrl.GMSetNewAmdinKeyC(AmdinKey_AES_new,AmdinKey_AES_new,'AES','AES',tempcounts)
                testResult=re.sub(re.compile('\s+'),' ',testResult)

            elif  '02' == self.AdminKeyAlgId[1]: #判断为体系SM4->新体系SM4
                testResult=self.testCtrl.GMSetNewAmdinKeyC(AmdinKey_SM4,AmdinKey_SM4,'SM4','SM4',tempcounts)
                testResult=re.sub(re.compile('\s+'),' ',testResult)

        if operator.eq(right_info, testResult):
            caseResult = "pass"
        else:
            caseResult="fail"
            e="实测返回："+"“"+testResult+"”"

        if e==None:
            caseResult="pass"
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult
    '''
    def positiveCase(self):
        #用例描述：插入1支U盾，点击保护密钥更新
        caseTitle  = "用例——插入1支U盾，点击保护密钥更新"  
        caseResult = None
        e=None
        if '00' == self.AdminKeyAlgId: #非国密盾或国密旧体系
            #旧体系->旧体系
            testResult=self.testCtrl.GMSetNewAmdinKeyC(AmdinKey_3DES,AmdinKey_3DES,'3DES','3DES')
            testResult=re.sub(re.compile('\s+'),' ',testResult)
            if operator.eq(right_info, testResult) == False:
                caseResult="fail"
                e="实测返回："+"“"+testResult+"”"
        else:
            adminKeyInfo = self.testCtrl.get_AdminKeyInfoC()
            tempcounts = adminKeyInfo[0:2]
            tempcounts = int(tempcounts)
            if tempcounts == 99:
                tempcounts = 0
            tempcounts += 1
            tempcounts = "%02d" % tempcounts

            if '01' == self.AdminKeyAlgId: #判断为国密盾新体系 AES
                #新体系AES->新体系AES
                testResult=self.testCtrl.GMSetNewAmdinKeyC(AmdinKey_AES_new,AmdinKey_AES_new,'AES','AES',tempcounts)
                testResult=re.sub(re.compile('\s+'),' ',testResult)
                if not operator.eq(right_info, testResult):
                    caseResult="fail"
                    e="实测返回："+"“"+testResult+"”"
            elif  '02' == self.AdminKeyAlgId: #判断为体系AES->新体系SM4
                testResult=self.testCtrl.GMSetNewAmdinKeyC(AmdinKey_SM4,AmdinKey_SM4,'SM4','SM4',tempcounts)
                testResult=re.sub(re.compile('\s+'),' ',testResult)
                if operator.eq(right_info, testResult) == False:
                    caseResult="fail"
                    e="实测返回："+"“"+testResult+"国密盾新体系SM4

            
                #新”"
            #新体系SM4->新体系SM4
            tempcounts=int(tempcounts)
            tempcounts=tempcounts+1
            tempcounts="%02d" %tempcounts
            testResult=self.testCtrl.GMSetNewAmdinKeyC(AmdinKey_SM4,AmdinKey_SM4,'SM4','SM4',tempcounts)
            testResult=re.sub(re.compile('\s+'),' ',testResult)
            if operator.eq(right_info, testResult) == False:
                caseResult="fail"
                e="实测返回："+"“"+testResult+"”"
            #新体系SM4->新体系AES
            tempcounts=int(tempcounts)
            tempcounts=tempcounts+1
            tempcounts="%02d" %tempcounts
            testResult=self.testCtrl.GMSetNewAmdinKeyC(AmdinKey_SM4,AmdinKey_AES_new,'SM4','AES',tempcounts)
            testResult=re.sub(re.compile('\s+'),' ',testResult)
            if operator.eq(right_info, testResult) == False:
                caseResult="fail"
                e="实测返回："+"“"+testResult+"”"
        else:
        #保护密钥算法为SM4
            tempcounts=flag_NeworOld[0:2]
            tempcounts=int(tempcounts)
            if tempcounts == 99:
                tempcounts=0
            tempcounts=tempcounts+1
            tempcounts="%02d" %tempcounts
            #新体系SM4->新体系SM4
            testResult=self.testCtrl.GMSetNewAmdinKeyC(AmdinKey_SM4,AmdinKey_SM4,'SM4','SM4',tempcounts)
            testResult=re.sub(re.compile('\s+'),' ',testResult)
            if operator.eq(right_info, testResult) == False:
                caseResult="fail"
                e="实测返回："+"“"+testResult+"”"
            #新体系SM4->新体系AES
            tempcounts=int(tempcounts)
            tempcounts=tempcounts+1
            tempcounts="%02d" %tempcounts
            testResult=self.testCtrl.GMSetNewAmdinKeyC(AmdinKey_SM4,AmdinKey_AES_new,'SM4','AES',tempcounts)
            testResult=re.sub(re.compile('\s+'),' ',testResult)
            if operator.eq(right_info, testResult) == False:
                caseResult="fail"
                e="实测返回："+"“"+testResult+"”"
            #新体系AES->新体系AES
            tempcounts=int(tempcounts)
            tempcounts=tempcounts+1
            tempcounts="%02d" %tempcounts
            testResult=self.testCtrl.GMSetNewAmdinKeyC(AmdinKey_AES_new,AmdinKey_AES_new,'AES','AES',tempcounts)
            testResult=re.sub(re.compile('\s+'),' ',testResult)
            if operator.eq(right_info, testResult) == False:
                caseResult="fail"
                e="实测返回："+"“"+testResult+"”"
            #新体系AES->新体系SM4
            tempcounts=int(tempcounts)
            tempcounts=tempcounts+1
            tempcounts="%02d" %tempcounts
            testResult=self.testCtrl.GMSetNewAmdinKeyC(AmdinKey_AES_new,AmdinKey_SM4,'AES','SM4',tempcounts)
            testResult=re.sub(re.compile('\s+'),' ',testResult)
            if operator.eq(right_info, testResult) == False:
                caseResult="fail"
                e="实测返回："+"“"+testResult+"”"
        
        if e==None:
            caseResult="pass"
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult
    '''

    def positiveCase_3DES_to_3DES(self):
        caseTitle =  "非国密盾或国密旧体系盾，旧体系->旧体系，期望灌密成功"
        caseResult=None
        e = None

        if '00' == self.AdminKeyAlgId[1]:  # 非国密盾或国密旧体系
            testResult=self.testCtrl.GMSetNewAmdinKeyC(AmdinKey_3DES,AmdinKey_3DES,'3DES','3DES')
            testResult=re.sub(re.compile('\s+'),' ',testResult)
            if operator.eq(right_info, testResult):
                caseResult="pass"
            else:
                caseResult="fail"
                e="实测返回："+"“"+testResult+"”"
        else:
            caseResult = "fail"
            e = "测试U盾类型不符，请选择非国密盾或国密盾旧体系进行！"

        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult

    def positiveCase_3DES_to_AES(self):
        caseTitle =  "国密盾，旧体系->新体系(AES)，期望灌密成功"
        caseResult=None
        e = None

        if not self.AdminKeyAlgId[0]:
            if '00' == self.AdminKeyAlgId[1]: #国密旧体系
                tempcounts = int(self.AdminKeyAlgId[2])
                if 99 == tempcounts:
                    tempcounts = 0
                tempcounts += 1
                tempcounts = "%02d" % tempcounts          #序号

                testResult=self.testCtrl.GMSetNewAmdinKeyC(AmdinKey_AES_old,AmdinKey_AES_new,'3DES','AES')
                testResult=re.sub(re.compile('\s+'),' ',testResult)
                if operator.eq(right_info, testResult):
                    caseResult="pass"
                else:
                    caseResult="fail"
                    e="实测返回："+"“"+testResult+"”"
            else:
                caseResult = "fail"
                e = "测试U盾类型不符，请选择国密盾旧体系进行！"
        else:
            caseResult = "fail"
            e = "测试U盾类型不符，请选择国密盾旧体系进行！"

        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult

    def positiveCase_3DES_to_SM4(self):
        caseTitle =  "国密盾，旧体系->新体系(SM4)，期望灌密成功"
        caseResult=None
        e=None

        if not self.AdminKeyAlgId[0]:
            if '00' == self.AdminKeyAlgId[1]: #国密旧体系
                tempcounts = int(self.AdminKeyAlgId[2])
                if 99 == tempcounts:
                    tempcounts = 0
                tempcounts += 1
                tempcounts = "%02d" % tempcounts          #序号

                testResult=self.testCtrl.GMSetNewAmdinKeyC(AmdinKey_AES_old,AmdinKey_SM4,'3DES','SM4')
                testResult=re.sub(re.compile('\s+'),' ',testResult)
                if operator.eq(right_info, testResult):
                    caseResult="pass"
                else:
                    caseResult="fail"
                    e="实测返回："+"“"+testResult+"”"
            else:
                caseResult = "fail"
                e = "测试U盾类型不符，请选择国密盾旧体系进行！"
        else:
            caseResult = "fail"
            e = "测试U盾类型不符，请选择国密盾旧体系进行！"

        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult

    def positiveCase_AES_SM4_AES(self):
        caseTitle =  "国密盾，新体系AES->新体系SM4->新体系AES，期望灌密成功"
        caseResult=None
        e=None

        if  '00' == self.AdminKeyAlgId[1]:
            if '01' == self.AdminKeyAlgId[1]: #国密新体系AES
                tempcounts = int(self.AdminKeyAlgId[2])
                if 99 == tempcounts:
                    tempcounts = 0
                tempcounts += 1
                tempcounts = "%02d" % tempcounts  # 序号
                testResult=self.testCtrl.GMSetNewAmdinKeyC(AmdinKey_AES_new,AmdinKey_SM4,'AES','SM4',tempcounts)
                testResult=re.sub(re.compile('\s+'),' ',testResult)
                if operator.eq(right_info, testResult):
                    if tempcounts == 99:
                        tempcounts = 0
                    tempcounts += 1
                    tempcounts = "%02d" % tempcounts
                    testResult=self.testCtrl.GMSetNewAmdinKeyC(AmdinKey_SM4,AmdinKey_AES_new,'SM4','AES',tempcounts)
                    testResult=re.sub(re.compile('\s+'),' ',testResult)
                    if operator.eq(right_info, testResult):
                        caseResult = "pass"
                    else:
                        caseResult = "fail"
                        e = "实测返回：" + "“" + testResult + "”"
                else:
                    caseResult="fail"
                    e="实测返回："+"“"+testResult+"”"
            else:
                caseResult = "fail"
                e = "测试U盾类型不符，请选择国密盾新体系（AES）进行！"
        else:
            caseResult = "fail"
            e = "测试U盾类型不符，请选择国密盾新体系进行！"

        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult

    def positiveCase_AES_to_AES(self):
        caseTitle =  "国密盾，新体系AES->新体系AES，期望灌密成功"
        caseResult=None
        e=None

        if  '01' == self.AdminKeyAlgId[1]:
            tempcounts = int(self.AdminKeyAlgId[2])
            if 99 == tempcounts:
                tempcounts = 0
            tempcounts += 1
            tempcounts = "%02d" % tempcounts  # 序号
            testResult = self.testCtrl.GMSetNewAmdinKeyC(AmdinKey_AES_new, AmdinKey_AES_new, 'AES', 'AES',tempcounts)
            testResult = re.sub(re.compile('\s+'), ' ', testResult)
            if operator.eq(right_info, testResult):
                caseResult = "pass"
            else:
                caseResult = "fail"
                e = "实测返回：" + "“" + testResult + "”"
        else:
            caseResult = "fail"
            e = "测试U盾类型不符，请选择国密盾新体系AES进行！"

        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult

    def positiveCase_SM4_to_SM4(self):
        caseTitle =  "国密盾，新体系SM4->新体系SM4，期望灌密成功"
        caseResult=None
        e = None

        if  '02' == self.AdminKeyAlgId[1]:
            tempcounts =  int(self.AdminKeyAlgId[2])
            if tempcounts == 99:
                tempcounts = 0
            tempcounts += 1
            tempcounts = "%02d" % tempcounts
            testResult = self.testCtrl.GMSetNewAmdinKeyC(AmdinKey_SM4, AmdinKey_SM4, 'SM4', 'SM4',tempcounts)
            testResult = re.sub(re.compile('\s+'), ' ', testResult)
            if operator.eq(right_info, testResult):
                caseResult = "pass"
            else:
                caseResult = "fail"
                e = "实测返回：" + "“" + testResult + "”"
        else:
            caseResult = "fail"
            e = "测试U盾类型不符，请选择国密盾新体系SM4进行！"

        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult

    def negativeCase_noKey_voidParaChoice(self):
        #用例描述：未插入U盾，新保护密钥栏不输入字符，点击保护密钥更新,返回“灌入密钥失败:未知错误。返回码:-304 Failed Param!”
        caseTitle  = "用例——未插入U盾,新保护密钥栏不输入字符,点击保护密钥更新,返回“灌入密钥失败:未知错误。返回码:-304 Failed Param! 或-102 There is no key!(实测返回)”"
        caseResult = None
        e=None
        testResult=self.testCtrl.GMSetNewAmdinKeyC(AmdinKey_3DES,AmdinKey_3DES,'3DES','3DES','00',1,False)
        testResult=re.sub(re.compile('\s+'),' ',testResult)
        if operator.eq(param_Err,testResult) or operator.eq(no_key_Err,testResult) :
            caseResult="pass"                     
        else:
            caseResult="fail"
            e="实测返回："+"“"+testResult+"”"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult

    def negativeCase_noKey_randParaChoice(self):
        #用例描述：未插入U盾，新保护密钥栏任意输入字符，点击保护密钥更新,返回“灌入密钥失败:未知错误。返回码:-304 Failed Param! ”
        caseTitle  = "用例——未插入U盾,新保护密钥栏任意输入字符,点击保护密钥更新,返回“灌入密钥失败:未知错误。返回码:-304 Failed Param! 或-102 There is no key!(实测返回)”"
        caseResult = None
        e=None
        testResult=self.testCtrl.GMSetNewAmdinKeyC(AmdinKey_3DES,AmdinKey_3DES,'3DES','3DES','00','',False)
        testResult=re.sub(re.compile('\s+'),' ',testResult)
        if operator.eq(param_Err,testResult) or operator.eq(no_key_Err,testResult) :
            caseResult="pass"                     
        else:
            caseResult="fail"
            e="实测返回："+"“"+testResult+"”"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult               
    
    def negativeCase_manyKey_validParaChoice(self):
        #用例描述：插入多支同款U盾，输入合法的新保护密钥值参数，点击保护密钥更新
        caseTitle="用例——插入多支同款U盾,输入合法的新保护密钥值参数,点击保护密钥更新，返回“灌入密钥失败:未知错误。返回码:-104 There is more than one key! 或-304 Failed Param!”"
        caseResult = None
        e=None
        testResult=self.testCtrl.GMSetNewAmdinKeyC(AmdinKey_3DES,AmdinKey_3DES,'3DES','3DES')
        testResult=re.sub(re.compile('\s+'),' ',testResult)
        if operator.eq(many_key_Err,testResult) or operator.eq(param_Err,testResult) :
            caseResult="pass"                        
        else:
            caseResult="fail"
            e="实测返回："+"“"+testResult+"”"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult

    def negativeCase_manyKey_voidParaChoice(self):
        #用例描述：插入多支同款U盾，不输入新保护密钥值参数，点击保护密钥更新
        caseTitle="用例——插入多支同款U盾,不输入新保护密钥值参数,点击保护密钥更新,返回“灌入密钥失败:未知错误。返回码:-104 There is more than one key! 或-304 Failed Param!”"
        caseResult = None
        e=None
        testResult=self.testCtrl.GMSetNewAmdinKeyC(AmdinKey_3DES,AmdinKey_3DES,'3DES','3DES','00','',False)
        testResult=re.sub(re.compile('\s+'),' ',testResult)
        if operator.eq(many_key_Err,testResult) or operator.eq(param_Err,testResult) :
            caseResult="pass"                        
        else:
            caseResult="fail"
            e="实测返回："+"“"+testResult+"”"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult

    def negativeCase_manyKey_randParaChoice(self):
        #用例描述：插入多支同款U盾，任意输入新保护密钥值参数，点击保护密钥更新
        caseTitle="用例——插入多支同款U盾,任意输入新保护密钥值参数,点击保护密钥更新,返回“灌入密钥失败:未知错误。返回码:-104 There is more than one key! 或-304 Failed Param!”"
        caseResult = None
        e=None
        testResult=self.testCtrl.GMSetNewAmdinKeyC(AmdinKey_3DES,AmdinKey_3DES,'3DES','3DES','00',1,False)
        testResult=re.sub(re.compile('\s+'),' ',testResult)
        if operator.eq(many_key_Err,testResult) or operator.eq(param_Err,testResult) :
            caseResult="pass"                        
        else:
            caseResult="fail"
            e="实测返回："+"“"+testResult+"”"
        if e==None:
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult

    def negativeCase_operation(self):
        #用例描述：插入多支同款U盾，拔出多余U盾，只留1支在位，点击保护密钥更新
        caseTitle="用例——插入多支同款U盾,拔出多余U盾,只留1支在位,点击保护密钥更新"
        caseResult = None
        e=None        
        #if 0 == TestingType:    
            #win32api.MessageBox(0, "请确认已接入多支同款U盾，并拔出多余U盾，只留一支测试U盾在位", "提示框",win32con.MB_OK)  
        flag_NeworOld=self.testCtrl.get_AdminKeyInfoC()
        if '' == flag_NeworOld or "0" == flag_NeworOld[3]: 
        #非国密盾或国密旧体系
            #旧体系->旧体系
            testResult=self.testCtrl.GMSetNewAmdinKeyC(AmdinKey_3DES,AmdinKey_3DES,'3DES','3DES')
            testResult=re.sub(re.compile('\s+'),' ',testResult)
            if right_info != testResult:
                caseResult="fail"
                e="实测返回："+"“"+testResult+"”"
        #判断为国密盾新体系 
        elif flag_NeworOld[3] == "1":
        #保护密钥算法为AES 
            tempcounts=flag_NeworOld[0:2]
            tempcounts=int(tempcounts)
            if tempcounts == 99:
                tempcounts=0
            tempcounts+=1
            tempcounts="%02d" %tempcounts
            #新体系AES->新体系AES
            testResult=self.testCtrl.GMSetNewAmdinKeyC(AmdinKey_AES_new,AmdinKey_AES_new,'AES','AES',tempcounts)
            testResult=re.sub(re.compile('\s+'),' ',testResult)
            if right_info != testResult:
                caseResult="fail"
                e="实测返回："+"“"+testResult+"”"
        else:
        #保护密钥算法为SM4
            tempcounts=flag_NeworOld[0:2]
            tempcounts=int(tempcounts)
            if tempcounts == 99:
                tempcounts=0
            tempcounts=tempcounts+1
            tempcounts="%02d" %tempcounts
            #新体系SM4->新体系SM4
            testResult=self.testCtrl.GMSetNewAmdinKeyC(AmdinKey_SM4,AmdinKey_SM4,'SM4','SM4',tempcounts)
            testResult=re.sub(re.compile('\s+'),' ',testResult)
            if right_info != testResult:
                caseResult="fail"
                e="实测返回："+"“"+testResult+"”"
        if e==None:
            caseResult="pass"
            logger.critical("%s || %s ",caseResult,caseTitle)
        else:
            logger.critical("%s || %s || %s ",caseResult,caseTitle,e)
        return caseResult 
    
       
        
#########################
#开始测试
#########################
