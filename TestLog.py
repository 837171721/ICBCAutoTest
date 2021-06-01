#coding=utf-8
'''
Created on 2018.3.19

Desc: output log to console and file  
@author: 蜗牛

@log level:  notset < debug < info < warn< error < critial
'''
'============================================'
import sys
import logging
from GlobalConfigure import *

class LogConfig():  
    def __init__(self,loglevel,logger):
        #创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)
        
        #创建一个handler,用于写入日志文件
        #fh = logging.FileHandler(logName)
        fh = logging.handlers.RotatingFileHandler(
            filename = log_file,\
            maxBytes = log_max_byte,\
            backupCount = log_backup_count)
        fh.setLevel(loglevel)
        
        #再创建一个handler,用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(loglevel)
        
        #定义handler的输出格式
        log_format = logging.Formatter('%(asctime)s || %(filename)s: %(funcName)s() || %(message)s')  # 定义该handler格式
        log_format.datefmt='%Y-%m-%d %H:%M:%S'
        fh.setFormatter(log_format)  
        ch.setFormatter(log_format)  
         
        # 给logger添加handler  
        self.logger.addHandler(fh)  
        self.logger.addHandler(ch) 
        
    def getlogger(self):  
        return self.logger

'''
if __name__ == "__main__":  
    conf = LogConfig(loglevel="INFO", logger="TestLog.py")
    logger=conf.getlogger()
    logger.info('foorbar')
    student="\033[0;31;47"
    student="jenny"  
    isStaff=True  
    logger.info("student=%s,isStaff=%s",student,isStaff)  
    # Print information    # 输出日志级别  
    logger.debug("debug message")  
    logger.info("info message")   
    logger.warning("warning message")    
    logger.error("error message")     
    logger.critical("critical message")
    # any command line that you will execute
    test_log_file.close()
'''
'''
Formatter日志格式
Formatter对象定义了log信息的结构和内容，构造时需要带两个参数：
一个是格式化的模板fmt，默认会包含最基本的level和 message信息
一个是格式化的时间样式datefmt，默认为 2003-07-08 16:49:45,896 (%Y-%m-%d %H:%M:%S)
fmt中允许使用的变量可以参考下表。

%(name)s Logger的名字
%(levelno)s 数字形式的日志级别
%(levelname)s 文本形式的日志级别
%(pathname)s 调用日志输出函数的模块的完整路径名，可能没有
%(filename)s 调用日志输出函数的模块的文件名
%(module)s 调用日志输出函数的模块名|
%(funcName)s 调用日志输出函数的函数名|
%(lineno)d 调用日志输出函数的语句所在的代码行
%(created)f 当前时间，用UNIX标准的表示时间的浮点数表示|
%(relativeCreated)d 输出日志信息时的，自Logger创建以来的毫秒数|
%(asctime)s 字符串形式的当前时间。默认格式是“2003-07-08 16:49:45,896”。逗号后面的是毫秒
%(thread)d 线程ID。可能没有
%(threadName)s 线程名。可能没有
%(process)d 进程ID。可能没有
%(message)s 用户输出的消息
'''