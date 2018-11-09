#coding=utf-8
#作者：曾祥卫
#时间：2018.09.21
#描述：配置更新的业务逻辑层

from systemtools.configupdate.configupdate_control import ConfigUpdateControl
from systemtools.systemtools_control import SystemToolsControl
import time
from data import data

class ConfigUpdateBusiness(ConfigUpdateControl):

    def __init__(self,driver):
        #继承ConfigUpdateControl类的属性和方法
        ConfigUpdateControl.__init__(self,driver)

    def restore_AP_factory(self):
        """
        在AP的web页面上点击恢复出厂设置
        """
        #点击系统工具设置菜单
        tmp = SystemToolsControl(self.driver)
        tmp.menu_systemtools()
        #点击配置更新菜单
        self.menu_configupdate()
        #点击恢复出厂设置
        self.click_restore_factory_button()
        #点击确认恢复出厂设置窗口的确认按钮
        self.click_recovery_confirm_button()
        time.sleep(120)
        print("click restore AP factory successfully!")

    def download_config_file(self):
        """
        下载配置文件
        """
        #点击系统工具设置菜单
        tmp = SystemToolsControl(self.driver)
        tmp.menu_systemtools()
        #点击配置更新菜单
        self.menu_configupdate()
        #点击下载配置
        self.click_download_button()
        time.sleep(20)

    def upload_config_file(self, path):
        """
        上传配置文件
        """
        #点击系统工具设置菜单
        tmp = SystemToolsControl(self.driver)
        tmp.menu_systemtools()
        #点击配置更新菜单
        self.menu_configupdate()
        #选择文件
        self.set_select_fle(path)
        #点击上传配置
        self.click_upload_button()
        #点击确认上传配置文件窗口的确认按钮
        self.click_upload_confirm_button()
        time.sleep(100)