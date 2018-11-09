#coding=utf-8
#作者：曾祥卫
#时间：2018.10.29
#描述：mac过滤的业务逻辑层

from firewall.firewall_control import FireWallControl
from firewall.macfilter.macfilter_control import MacFilterControl
import time, subprocess
from data import data

class MacFilterBusiness(MacFilterControl):

    def __init__(self,driver):
        #继承MacFilterControl类的属性和方法
        MacFilterControl.__init__(self,driver)

    def add_one_list(self, mac):
        """添加一条MAC过滤规则"""
        #首先点击防火墙菜单
        tmp = FireWallControl(self.driver)
        tmp.menu_firewall()
        #再点击MAC过滤菜单
        self.menu_macfilter()
        #击添加按钮
        self.click_add_button()
        #输入mac地址
        self.set_mac(mac)
        #点击保存按钮
        self.click_save_button()
        time.sleep(30)

    def delete_n_list(self, n):
        """
        删除第n条mac过滤的规则list
        """
        #首先点击防火墙菜单
        tmp = FireWallControl(self.driver)
        tmp.menu_firewall()
        #再点击MAC过滤菜单
        self.menu_macfilter()
        #点击选择第几个list
        self.click_choice_n_list(n)
        #点击删除所选按钮
        self.click_delete_button()
        time.sleep(30)

    def edit_n_list(self, n, mac):
        """
        编辑第n条mac过滤的规则list
        """
        #首先点击防火墙菜单
        tmp = FireWallControl(self.driver)
        tmp.menu_firewall()
        #再点击MAC过滤菜单
        self.menu_macfilter()
        #点击编辑第几个list
        self.click_edit_n_list_button(n)
        #编辑mac地址
        self.edit_mac(mac)
        #点击保存按钮
        self.click_save_button()
        time.sleep(30)

    def delete_all_list(self):
        """
        删除所有的mac过滤的规则list
        """
        #首先点击防火墙菜单
        tmp = FireWallControl(self.driver)
        tmp.menu_firewall()
        #再点击MAC过滤菜单
        self.menu_macfilter()
        #点击IP过滤列表中的全选
        self.click_all_choices_button()
        #点击删除所选按钮
        self.click_delete_button()
        time.sleep(30)

    def check_wifi_client_access_internet(self, ssid, wlan, wifi_encryption, password=None, internet_ip="180.76.76.76"):
        """
        判断无线客户端是否能够访问internet
        """
        #禁用有线网卡
        self.networkcard_disable()
        #无线网卡能够连接上AP的SSID
        self.client_connect_ssid(ssid, wlan, wifi_encryption, password)
        #无线网卡获取IP地址
        self.dhcp_wlan(wlan)
        time.sleep(60)
        #AP是否能够上网
        result1 = self.get_ping(internet_ip)
        #result1 = self.get_ping("www.baidu.com")
        #释放无线网卡的ip
        self.dhcp_release_wlan(wlan)
        #断开无线网卡
        self.disconnect_ap()
        #最后启用有线网卡
        self.networkcard_enable()
        return result1

    def add_10_list(self):
        """
        添加10条规则，mac地址为随机mac地址
        """
        #首先点击防火墙菜单
        tmp = FireWallControl(self.driver)
        tmp.menu_firewall()
        #再点击MAC过滤菜单
        self.menu_macfilter()
        for i in range(10):
            random_mac = self.randomMAC()
            #击添加按钮
            self.click_add_button()
            #输入mac地址
            self.set_mac(random_mac)
            #点击保存按钮
            self.click_save_button()
            time.sleep(2)
        time.sleep(30)