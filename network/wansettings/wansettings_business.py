#coding=utf-8
#作者：曾祥卫
#时间：2018.09.20
#描述：外网设置的业务逻辑层

from network.wansettings.wansettings_control import WanSettingsControl
from network.network_control import NetWorkControl
from connect.ssh import SSH
import time
from data import data

class WanSettingsBusiness(WanSettingsControl):

    def __init__(self,driver):
        #继承WanSettingsControl类的属性和方法
        WanSettingsControl.__init__(self,driver)

    #设置外网为pppoe
    def change_wan_to_pppoe(self, pppoe_user, pppoe_password, dns):
        """
        设置外网为pppoe
        """
        #首先点击网络设置
        tmp = NetWorkControl(self.driver)
        tmp.menu_network()
        #再点击外网设置
        self.menu_wansettings()
        #点击PPPoE按钮
        self.set_pppoe()
        #输入用户名
        self.set_pppoe_user(pppoe_user)
        #输入密码
        self.set_pppoe_password(pppoe_password)
        #输入dns
        self.set_pppoe_dns(dns)
        #点击设置按钮
        self.click_save_button()
        #点击保存
        self.click_confirm_button()

    #设置外网为staticIP
    def change_wan_to_staticIP(self, ip, netmask, gateway, dns):
        """
        设置外网为staticIP
        """
        #首先点击网络设置
        tmp = NetWorkControl(self.driver)
        tmp.menu_network()
        #再点击外网设置
        self.menu_wansettings()
        #点击静态IP按钮
        self.set_staticIP()
        #输入静态ip的ip地址
        self.set_staticIP_IP(ip)
        #输入静态ip的子网掩码
        self.set_staticIP_netmask(netmask)
        #输入静态ip的gateway
        self.set_staticIP_gateway(gateway)
        #输入静态ip的dns
        self.set_staticIP_dns(dns)
        #点击设置按钮
        self.click_save_button()
        #点击保存
        self.click_confirm_button()

    #设置外网为动态获取
    def change_wan_to_dhcp(self):
        """
        设置外网为动态获取
        """
        #首先点击网络设置
        tmp = NetWorkControl(self.driver)
        tmp.menu_network()
        #再点击外网设置
        self.menu_wansettings()
        #点击动态获取按钮
        self.set_dhcp()
        #点击设置按钮
        self.click_save_button()
        #点击保存
        self.click_confirm_button()

    #判断wan口的上网方式
    def get_wan_way(self, host, user, pwd):
        """
        判断wan口的上网方式
        """
        ssh = SSH(host, pwd)
        result = ssh.ssh_cmd(user, "uci show network.wan.proto")
        return result
