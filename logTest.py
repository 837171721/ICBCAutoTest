#coding=utf-8
'''
Created on 2018.3.21
Desc: output log to console and file  
@author: ys
@log level:  notset < debug < info < warn< error < critial
'''
'============================================'
#导入模块
from GlobalConfigure import *
import sys
import logging
import logging.handlers

class SysClass(): 
    def OpenFile(self,fileName,accMode):
        fp = open(fileName, accMode,encoding="UTF-8")
        sys.stdout = fp
        return fp
    def PerformanceSummary(self,CaseCounts=0,CaseSuccessNum=0,CaseFailNum=0,CaseTimeOut=0,PercentPass=100,placeHolderCnt=0):  #整体性能统计函数
        print(u"*============测试结果统计============*")
        print(u"\t \t测试用例数：%s" %CaseCounts)
        print(u"\t \t成功用例数：%s" %CaseSuccessNum)
        print(u"\t \t失败用例数：%s" %CaseFailNum)
        print(u"\t \t测试总耗时：%s min" %CaseTimeOut)
        print(u"\t \t通过百分比：%s %%" %PercentPass)
        print(u"*=================================*")
        if placeHolderCnt: #打印占位符，解决统计信息输出时，后续日志信息被覆盖的问题
            str = ""
            for i in range(0,placeHolderCnt):
                str =str+" "
            print(str)
            print("*测试详情如下：")

    def CloseFile(self,fp):
        fp.close()       
    def getSysLog(self,fileName,accMode="w+",CaseCounts=0,CaseSuccessNum=0,CaseFailNum=0,CaseTimeOut=0,PercentPass=100,placeHolderCnt=0):
        stdout_backup = sys.stdout
        fp=self.OpenFile(fileName,accMode)
        sys.stdout = fp
        self.PerformanceSummary(CaseCounts,CaseSuccessNum,CaseFailNum,CaseTimeOut,PercentPass,placeHolderCnt)
        fp.close()

class LoggerClass():  
    def __init__(self,loglevel,logger):
        #创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)      
        #创建一个handler,用于写入日志文件
        #fh = logging.FileHandler(log_file)
        fh = logging.handlers.RotatingFileHandler(filename = log_file,maxBytes = log_max_byte,backupCount = log_backup_count,encoding="UTF-8")
        fh.setLevel(logging.CRITICAL)
         
        #再创建一个handler,用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(loglevel)
              
        #定义handler的输出格式
#        log_format = logging.Formatter('%(asctime)s || %(funcName)s() : %(filename)-60s || %(message)s')  # 定义该handler格式
        log_format_fh = logging.Formatter('%(asctime)s  || %(message)s || %(filename)s : %(funcName)s()')  # 定义该handler格式
#        log_format = logging.Formatter('%(asctime)s || %(filename)s : %(funcName)s() || %(message)s')  # 定义该handler格式
        log_format_fh.datefmt='%Y-%m-%d %H:%M:%S'    
        
        log_format_ch = logging.Formatter('%(asctime)s || %(filename)s : %(funcName)s() || %(message)s')  # 定义该handler格式
        log_format_ch.datefmt='%Y-%m-%d %H:%M:%S'    
        fh.setFormatter(log_format_fh)          
        ch.setFormatter(log_format_ch)  
                
        # 给logger添加handler  
        self.logger.addHandler(fh) 
        self.logger.addHandler(ch)                
    def getlogger(self):  
        return self.logger

if __name__ == "__main__":   
    #创建LoggerClass对象 
    outlogger = LoggerClass(loglevel="INFO", logger="logTest.py")
    logger=outlogger.getlogger()
    #创建SysClass对象
    outSys = SysClass()
    #第一步：日志文件头部写入总体测试情况的初始数据，仅占用位置
    outSys.getSysLog(log_file, "w",0,0,0,0,100)
    #第二步：日志文件写入用例执行去情况信息
    #logger.info("info message",)  
    logger.debug("debug message")  
    #logger.info("info message")   
    logger.warning("warning message")    
    logger.error("error message")     
    logger.critical("critical message")
    #第三部：日志文件头部插入总体测试情况的统计数据，覆盖最开始写入的初始数据
    outSys.getSysLog(log_file, "r+",5,3,2,3,60)
