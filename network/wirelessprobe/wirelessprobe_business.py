#coding=utf-8
#作者：曾祥卫
#时间：2018.09.20
#描述：无线探针的业务逻辑层

from network.wirelessprobe.wirelessprobe_control import WirelessProbeControl
from network.network_control import NetWorkControl
import time
from data import data

class WirelessProbeBusiness(WirelessProbeControl):

    def __init__(self,driver):
        #继承WirelessProbeControl类的属性和方法
        WirelessProbeControl.__init__(self,driver)





