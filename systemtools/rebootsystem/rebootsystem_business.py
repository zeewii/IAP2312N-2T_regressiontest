#coding=utf-8
#作者：曾祥卫
#时间：2018.09.21
#描述：系统重启的业务逻辑层

from systemtools.rebootsystem.rebootsystem_control import RebootSystemControl
from systemtools.systemtools_control import SystemToolsControl
import time
from data import data
data_basic = data.data_basic()

class RebootSystemBusiness(RebootSystemControl):

    def __init__(self,driver):
        #继承RebootSystemControl类的属性和方法
        RebootSystemControl.__init__(self,driver)

    def reboot_ap(self):
        """在页面上重启设备"""
        #点击系统工具设置菜单
        tmp = SystemToolsControl(self.driver)
        tmp.menu_systemtools()
        #点击系统重启菜单
        self.menu_rebootsystem()
        #点击重启设备
        self.click_reboot_button()
        #点击确认重启系统窗口的确认按钮
        self.click_restart_confirm_button()
        time.sleep(60)

    def check_reboot_ap(self, AP_IP):
        """在页面上点击重启设备后，验证设备是否重启"""
        #点击系统工具设置菜单
        tmp = SystemToolsControl(self.driver)
        tmp.menu_systemtools()
        #点击系统重启菜单
        self.menu_rebootsystem()
        #点击重启设备
        self.click_reboot_button()
        #点击确认重启系统窗口的确认按钮
        self.click_restart_confirm_button()
        #10s后ping不通AP
        time.sleep(10)
        result1 = self.get_ping(AP_IP)
        #50s后能够ping通AP
        time.sleep(70)
        #设置PC的静态IP,能够访问DUT的webpage
        self.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])
        time.sleep(10)
        result2 = self.get_ping(AP_IP)
        #---debug如果ping ap的ip不通，打印一下pc lan口的ip地址
        if result2 != 0:
            print("pc lan'ip is {}".format(self.get_localIp(data_basic['lan_pc'])))
        return result1, result2



