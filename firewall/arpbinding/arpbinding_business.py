#coding=utf-8
#作者：曾祥卫
#时间：2018.10.29
#描述：ARP绑定的业务逻辑层

from firewall.firewall_control import FireWallControl
from firewall.arpbinding.arpbinding_control import ArpBindingControl
import time, subprocess
from data import data

class ArpBindingBusiness(ArpBindingControl):

    def __init__(self,driver):
        #继承ArpBindingControl类的属性和方法
        ArpBindingControl.__init__(self,driver)

