#coding=utf-8
#作者：曾祥卫
#时间：2018.09.20
#描述：漫游设置的业务逻辑层

from network.roamsettings.roamsettings_control import RoamSettingsControl
from network.network_control import NetWorkControl
import time
from data import data

class RoamSettingsBusiness(RoamSettingsControl):

    def __init__(self,driver):
        #继承RoamSettingsControl类的属性和方法
        RoamSettingsControl.__init__(self,driver)





