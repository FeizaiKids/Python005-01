#编写一个函数, 当函数被调用时，将调用的时间记录在日志中, 日志文件的保存位置建议为：/var/log/python- 当前日期 /xxxx.log
import logging
from datetime import datetime
import os

def testLog(): 
    logDir = 'D:/log/python-' + str(datetime.today().date())   
    logPath = 'D:/log/python-' + str(datetime.today().date()) + '/' + __name__ + '.log'
    if not os.path.exists(logPath):
        os.makedirs(os.path.abspath(logDir))
    logging.basicConfig(filename=os.path.abspath(logPath), level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S', format='%(asctime)s %(name)-8s %(levelname)-8s [line: %(lineno)d] %(message)s')
    logging.info(datetime.now())

if __name__ == '__main__':
    testLog()
