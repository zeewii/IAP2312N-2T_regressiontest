#coding=utf-8
#作者：曾祥卫
#时间：2018.10.26
#描述：IP过滤的业务逻辑层

from firewall.firewall_control import FireWallControl
from firewall.ipfilter.ipfilter_control import IPFilterControl
import time, subprocess
from data import data

class IPFilterBusiness(IPFilterControl):

    def __init__(self,driver):
        #继承IPFilterControl类的属性和方法
        IPFilterControl.__init__(self,driver)


    def add_one_IPFilter_list(self, start_ip, end_ip):
        """添加一条IP过滤规则"""
        #首先点击防火墙菜单
        tmp = FireWallControl(self.driver)
        tmp.menu_firewall()
        #再点击IP过滤菜单
        self.menu_ipfilter()
        #击添加按钮
        self.click_add_button()
        #设置起始IP
        self.set_start_IP(start_ip)
        #设置结束IP
        self.set_end_IP(end_ip)
        #点击保存按钮
        self.click_save_button()
        time.sleep(30)


    def obtain_lan_ip_near_ip(self, eth, low_near, high_near):
        """
        获取PC lan口附近的ip地址
        输入：eth：PC的lan口的接口名,low_near:低多少值，high_low:高多少值
        输出：start_ip, end_ip
        """
        #获取PC lan口的ip
        lan_ip = self.get_localIp(eth)
        #将lan ip转换为列表
        lan_ip_list = lan_ip.split(".")
        #生成起始ip
        start_ip_list = lan_ip_list.copy()
        start_ip_list[-1] = str(int(lan_ip_list[-1])-low_near)
        start_ip = ".".join(start_ip_list)
        #生成结束ip
        end_ip_list = lan_ip_list.copy()
        end_ip_list[-1] = str(int(lan_ip_list[-1])+high_near)
        end_ip = ".".join(end_ip_list)
        print(start_ip, end_ip)
        return start_ip, end_ip

    def obtain_lan_ip_far_ip(self, eth, low_near, high_near):
        """
        获取不在PC lan口附近的ip地址
        输入：eth：PC的lan口的接口名,low_near:最低高pc的ip多少值，high_low:最高高pc的ip多少值
        输出：start_ip, end_ip
        """
        #获取PC lan口的ip
        lan_ip = self.get_localIp(eth)
        #将lan ip转换为列表
        lan_ip_list = lan_ip.split(".")
        #生成起始ip
        start_ip_list = lan_ip_list.copy()
        start_ip_list[-1] = str(int(lan_ip_list[-1])+low_near)
        start_ip = ".".join(start_ip_list)
        #生成结束ip
        end_ip_list = lan_ip_list.copy()
        end_ip_list[-1] = str(int(lan_ip_list[-1])+high_near)
        end_ip = ".".join(end_ip_list)
        print(start_ip, end_ip)
        return start_ip, end_ip

    def add_10_list_far_ip(self, eth):
        """
        添加10条规则，都是高于PC的ip的地址范围
        输入：eth：PC的lan口的接口名,low_near:最低高pc的ip多少值，high_low:最高高pc的ip多少值
        """
        #首先点击防火墙菜单
        tmp = FireWallControl(self.driver)
        tmp.menu_firewall()
        #再点击IP过滤菜单
        self.menu_ipfilter()
        for i in range(0, 30, 3):
            #击添加按钮
            self.click_add_button()
            #获取不在PC lan口附近的ip地址
            start_ip, end_ip = self.obtain_lan_ip_far_ip(eth, i+1, i+2)
            #设置起始IP
            self.set_start_IP(start_ip)
            #设置结束IP
            self.set_end_IP(end_ip)
            #点击保存按钮
            self.click_save_button()
            time.sleep(2)
        time.sleep(30)


    def delete_n_list(self, n):
        """
        删除第n条ip过滤的规则list
        """
        #首先点击防火墙菜单
        tmp = FireWallControl(self.driver)
        tmp.menu_firewall()
        #再点击IP过滤菜单
        self.menu_ipfilter()
        #点击选择第几个list
        self.click_choice_n_list(n)
        #点击删除所选按钮
        self.click_delete_button()
        time.sleep(30)

    def edit_n_list(self, n, start_ip, end_ip):
        """
        编辑第n条ip过滤的规则list
        """
        #首先点击防火墙菜单
        tmp = FireWallControl(self.driver)
        tmp.menu_firewall()
        #再点击IP过滤菜单
        self.menu_ipfilter()
        #点击编辑第几个list
        self.click_edit_n_list_button(n)
        #编辑起始IP
        self.edit_start_IP(start_ip)
        #编辑结束IP
        self.edit_end_IP(end_ip)
        #点击保存按钮
        self.click_save_button()
        time.sleep(30)

    def delete_all_list(self):
        """
        删除所有的ip过滤的规则list
        """
        #首先点击防火墙菜单
        tmp = FireWallControl(self.driver)
        tmp.menu_firewall()
        #再点击IP过滤菜单
        self.menu_ipfilter()
        #点击IP过滤列表中的全选
        self.click_all_choices_button()
        #点击删除所选按钮
        self.click_delete_button()
        time.sleep(30)