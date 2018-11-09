#coding=utf-8
#作者：曾祥卫
#时间：2018.09.21
#描述：系统日志的业务逻辑层

from systemtools.systemlog.systemlog_control import SystemLogControl
from systemtools.systemtools_control import SystemToolsControl
import time
from data import data

class SystemLogBusiness(SystemLogControl):

    def __init__(self,driver):
        #继承SystemLogControl类的属性和方法
        SystemLogControl.__init__(self,driver)





