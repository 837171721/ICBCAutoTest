import logging

class loggerClass:
    def __init__(self,logger_name,logger_level,logger_file='log.txt'):
        #创建logger对象
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logger_level)
        #创建处理器，输出日志到logger_file
        #file_handler = logging.FileHandler(logger_file)
        #file_handler.setLevel(logger_level)
        #创建处理器，输出日志到控制台上
        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setLevel(logger_level)

        #定义处理器的输出格式
        self.fmt_log = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        #self.date_fmt = '%Y%m%d %H : %M : %s'
        formatter = logging.Formatter(self.fmt_log)
        #file_handler.setFormatter(formatter)
        self.stream_handler.setFormatter(formatter)

        #添加处理器到logger对象
        #self.logger.addHandler(file_handler)
        self.logger.addHandler(self.stream_handler)


    def getlogger(self):
        return self.logger

    def Release(self):
        self.logger.removeHandler(self.stream_handler)

if __name__ == '__main__':
    logtest = loggerClass(logger_name='logger.py',logger_level='INFO')
    logger = logtest.getlogger()
    logger.info('info message')
