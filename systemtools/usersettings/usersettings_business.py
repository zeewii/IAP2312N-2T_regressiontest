#coding=utf-8
#作者：曾祥卫
#时间：2018.09.21
#描述：用户设置的业务逻辑层

from systemtools.usersettings.usersettings_control import UserSettingsControl
from systemtools.systemtools_control import SystemToolsControl
import time
from data import data

class UserSettingsBusiness(UserSettingsControl):

    def __init__(self,driver):
        #继承UserSettingsControl类的属性和方法
        UserSettingsControl.__init__(self,driver)





