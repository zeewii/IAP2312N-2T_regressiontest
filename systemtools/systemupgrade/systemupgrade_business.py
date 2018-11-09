#coding=utf-8
#作者：曾祥卫
#时间：2018.09.21
#描述：系统升级的业务逻辑层

from systemtools.systemupgrade.systemupgrade_control import SystemUpgradeControl
from systemtools.systemtools_control import SystemToolsControl
import time
from data import data

class SystemUpgradeBusiness(SystemUpgradeControl):

    def __init__(self,driver):
        #继承SystemUpgradeControl类的属性和方法
        SystemUpgradeControl.__init__(self,driver)

    def upgrade_system(self, path):
        """
        选择固件路径，升级固件
        输入：path：固件文件的路径
        """
        #点击系统工具设置菜单
        tmp = SystemToolsControl(self.driver)
        tmp.menu_systemtools()
        #点击系统升级设置菜单
        self.menu_systemupgrade()
        #选择固件文件
        self.set_select_firmware(path)
        #点击升级固件按钮
        self.click_update_button()
        #点击确认按钮
        self.click_confirm_button_no_wait()
        time.sleep(300)

    def check_system_version(self, version):
        """
        判断系统版本是否正确
        """
        #点击系统工具设置菜单
        tmp = SystemToolsControl(self.driver)
        tmp.menu_systemtools()
        #点击系统升级设置菜单
        self.menu_systemupgrade()
        #获取固件版本
        result = self.get_firmware_version()
        print(version, result)
        if version in result:
            return True
        else:
            return False

