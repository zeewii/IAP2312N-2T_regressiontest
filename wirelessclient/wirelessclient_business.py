#coding=utf-8
#作者：曾祥卫
#时间：2018.09.20
#描述：无线用户的业务逻辑层

from wirelessclient.wirelessclient_control import WirelessClientControl
from network.network_control import NetWorkControl
import time
from data import data

class WirelessClientBusiness(WirelessClientControl):

    def __init__(self,driver):
        #继承WirelessClientControl类的属性和方法
        WirelessClientControl.__init__(self,driver)

    #当只有唯一一个设备连接时,判断当前连接设备的设备的mac地址是否正确
    def check_current_devices_client_mac(self, wlan):
        """"
        当只有唯一一个设备连接时,判断设备的mac地址是否正确
        #输入：wlan：无线网卡的接口名
        """
        #点击无线用户菜单
        self.menu_wirelessclient()
        #获取client的mac地址
        result = self.get_current_devices_mac()
        print(result)
        #获取本地无线mac地址
        client_mac = self.get_wlan_mac(wlan)
        if result.upper() == client_mac.upper():
            return True
        else:
            return False

    #将当前连接设备页面的mac地址加入到待定名单
    def join_client_mac_to_undecided_list(self, n):
        """
        将当前连接设备页面的mac地址加入到待定名单
        """
        #点击无线用户菜单
        self.menu_wirelessclient()
        #当前设备中-点击选择第几个list
        self.click_current_choice_n_list(n)
        #点击加入所选
        self.click_join_choice_button()
        time.sleep(30)

    #当只有唯一一个设备连接时,判断待定名单的设备的mac地址是否正确
    def check_undecided_list_client_mac(self, wlan):
        """"
        当只有唯一一个设备连接时,判断待定名单的设备的mac地址是否正确
        #输入：wlan：无线网卡的接口名
        """
        #点击无线用户菜单
        self.menu_wirelessclient()
        #点击待定/白/黑名单按钮
        self.set_undecided_list()
        #获取client的mac地址
        result = self.get_undecided_client_mac()
        print(result)
        #获取本地无线mac地址
        client_mac = self.get_wlan_mac(wlan)
        if result.upper() == client_mac.upper():
            return True
        else:
            return False

    #将名单改为黑名单
    def change_to_black(self):
        """
        将名单改为黑名单
        """
        #点击无线用户菜单
        self.menu_wirelessclient()
        #点击待定/白/黑名单按钮
        self.set_undecided_list()
        #点击过滤规则按钮
        self.click_filter_rules_button()
        #点击黑名单按钮
        self.set_filter_black_list()
        time.sleep(30)

    #将名单改为白名单
    def change_to_white(self):
        """
        将名单改为白名单
        """
        #点击无线用户菜单
        self.menu_wirelessclient()
        #点击待定/白/黑名单按钮
        self.set_undecided_list()
        #点击过滤规则按钮
        self.click_filter_rules_button()
        #点击白名单按钮
        self.set_filter_white_list()
        time.sleep(30)

    #将名单改为待定名单
    def change_to_undecided(self):
        """
        将名单改为定名单
        """
        #点击无线用户菜单
        self.menu_wirelessclient()
        #点击待定/白/黑名单按钮
        self.set_undecided_list()
        #点击过滤规则按钮
        self.click_filter_rules_button()
        #点击停止过滤按钮
        self.set_stop_filter()
        time.sleep(30)

    #修改黑名单的第n条的mac地址
    def change_black_mac(self, n, mac):
        #点击无线用户菜单
        self.menu_wirelessclient()
        #点击待定/白/黑名单按钮
        self.set_undecided_list()
        #点击编辑第几个list
        self.click_edit_n_list_button(n)
        #设置点击编辑按钮后的窗口中的mac地址
        self.set_edit_windows_mac(mac)
        #击保存按钮
        self.click_namelist_save_button()
        time.sleep(30)



    #修改白名单的第n条的mac地址
    def change_white_mac(self, n, mac):
        """
        修改白名单的第n条的mac地址
        """
        #点击无线用户菜单
        self.menu_wirelessclient()
        #点击待定/白/黑名单按钮
        self.set_undecided_list()
        #点击编辑第几个list
        self.click_edit_n_list_button(n)
        #设置点击编辑按钮后的窗口中的mac地址
        self.set_edit_windows_mac(mac)
        #击保存按钮
        self.click_namelist_save_button()
        time.sleep(30)

    #添加多条list
    def add_many_lists(self, n):
        """
        添加多条list
        """
        #点击无线用户菜单
        self.menu_wirelessclient()
        #点击待定/白/黑名单按钮
        self.set_undecided_list()
        for i in range(n):
            #点击添加按钮
            self.click_add_button()
            #设置点击添加按钮后的窗口中的设备名称
            self.set_add_windows_equipment_name("list%s"%i)
            #设置点击添加按钮后的窗口中的mac地址
            random_mac = self.randomMAC()
            self.set_add_windows_mac(random_mac)
            #点击保存按钮
            self.click_namelist_save_button()
            #time.sleep(2)
        time.sleep(60)

    #删除所有的list
    def del_all_lists(self):
        #点击无线用户菜单
        self.menu_wirelessclient()
        #点击待定/白/黑名单按钮
        self.set_undecided_list()
        #点击当前连接设备页面的全选
        self.click_undecided_devices_all_choices_button()
        #点击删除所选按钮
        self.click_delete_button()
        time.sleep(60)


























