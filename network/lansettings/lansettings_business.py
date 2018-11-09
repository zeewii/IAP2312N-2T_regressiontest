#coding=utf-8
#作者：曾祥卫
#时间：2018.09.20
#描述：内网设置的业务逻辑层

from network.lansettings.lansettings_control import LanSettingsControl
from network.network_control import NetWorkControl
import time, subprocess
from data import data

class LanSettingsBusiness(LanSettingsControl):

    def __init__(self,driver):
        #继承LanSettingsControl类的属性和方法
        LanSettingsControl.__init__(self,driver)

    #开启/关闭DHCP server
    def enable_disable_dhcp_server(self, mode):
        """
        开启/关闭DHCP server
        输入：mode:0：禁用，1：启用
        """
        #首先点击网络设置
        tmp = NetWorkControl(self.driver)
        tmp.menu_network()
        #再点击内网设置
        self.menu_lansettings()
        #关闭dhcp server
        self.set_dhcp_server(mode)
        #点击设置按钮
        self.click_save_button()
        #点击保存
        self.click_confirm_button()

    #判断AP的dhcp server是否开启
    def check_AP_dhcp_server(self, lan, ip_str):
        """
        判断AP的dhcp server是否开启
        """
        #释放有线网卡的ip
        self.dhcp_release_wlan(lan)
        #然后有线网卡获取ip
        self.dhcp_wlan(lan)
        tmp = self.get_client_cmd_result("ifconfig %s"%lan)
        if ip_str in tmp:
            return True
        else:
            return False

    #指定PC接口的ip，掩码，网关，判断client能够上网
    def check_access_internet_after_change_client_ip_netmask_gw(self, pc_pwd, eth, ip, netmask, gateway):
        """
        指定PC接口的ip，掩码，网关，使其能够上网
        """
        for i in range(5):
            #指定PC接口的ip和掩码
            subprocess.call('echo %s |sudo -S ifconfig %s %s netmask %s'%(pc_pwd, eth, ip, netmask), shell=True)
            time.sleep(2)
            #然后设置网关
            subprocess.call('echo %s |sudo -S route add default gw %s'%(pc_pwd, gateway), shell=True)
            time.sleep(60)
            #有线是否能够上网
            result = self.get_ping("180.76.76.76")
            #去掉ip
            self.dhcp_release_wlan(eth)
            #去掉网关
            subprocess.call('echo %s |sudo -S route del default'%(pc_pwd), shell=True)
            time.sleep(2)
            if result == 0:
                return result
        return 1

    #改变AP的ip和掩码
    def change_AP_ip_netmask(self, ip, netmask):
        """
        改变AP的ip
        """
        #首先点击网络设置
        tmp = NetWorkControl(self.driver)
        tmp.menu_network()
        #再点击内网设置
        self.menu_lansettings()
        #修改AP的ip
        self.set_ip(ip)
        #输入内网设置的子网掩码
        self.set_netmask(netmask)
        #点击设置按钮
        self.click_save_button()
        #点击保存
        self.click_confirm_button_no_wait()
        time.sleep(30)
        print("change ap's ip successfully!")
        # #停止页面加载
        # self.driver.execute_script('window.stop()')

