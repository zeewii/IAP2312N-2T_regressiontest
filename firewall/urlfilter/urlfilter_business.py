#coding=utf-8
#作者：曾祥卫
#时间：2018.10.29
#描述：URL过滤的业务逻辑层

from firewall.firewall_control import FireWallControl
from firewall.urlfilter.urlfilter_control import UrlFilterControl
import time, subprocess
from data import data

class UrlFilterBusiness(UrlFilterControl):

    def __init__(self,driver):
        #继承UrlFilterControl类的属性和方法
        UrlFilterControl.__init__(self,driver)

    def add_one_list(self, url):
        """添加一条URL过滤规则"""
        #首先点击防火墙菜单
        tmp = FireWallControl(self.driver)
        tmp.menu_firewall()
        #再点击url过滤菜单
        self.menu_urlfilter()
        #击添加按钮
        self.click_add_button()
        #设置URL地址
        self.set_url_address(url)
        #点击保存按钮
        self.click_save_button()
        time.sleep(30)

    def delete_n_list(self, n):
        """
        删除第n条url过滤的规则list
        """
        #首先点击防火墙菜单
        tmp = FireWallControl(self.driver)
        tmp.menu_firewall()
        #再点击url过滤菜单
        self.menu_urlfilter()
        #点击选择第几个list
        self.click_choice_n_list(n)
        #点击删除所选按钮
        self.click_delete_button()
        time.sleep(30)

    def edit_n_list(self, n, url):
        """
        编辑第n条url过滤的规则list
        """
        #首先点击防火墙菜单
        tmp = FireWallControl(self.driver)
        tmp.menu_firewall()
        #再点击url过滤菜单
        self.menu_urlfilter()
        #点击编辑第几个list
        self.click_edit_n_list_button(n)
        #编辑url
        self.edit_url_address(url)
        #点击保存按钮
        self.click_save_button()
        time.sleep(30)

    def delete_all_list(self):
        """
        删除所有的url过滤的规则list
        """
        #首先点击防火墙菜单
        tmp = FireWallControl(self.driver)
        tmp.menu_firewall()
        #再点击url过滤菜单
        self.menu_urlfilter()
        #点击IP过滤列表中的全选
        self.click_all_choices_button()
        #点击删除所选按钮
        self.click_delete_button()
        time.sleep(30)

    def check_access_url(self, url):
        """
        判断是否能够访问指定的url
        url:指定的url
        """
        try:
            tmp = subprocess.call("wget {}".format(url), shell=True, timeout=5)
            if tmp == 0:
                return True
            else:
                return False
        except:
            return False

    def add_10_list(self, url):
        """
        添加10条规则
        """
        #首先点击防火墙菜单
        tmp = FireWallControl(self.driver)
        tmp.menu_firewall()
        #再点击url过滤菜单
        self.menu_urlfilter()
        for i in range(10):
            #击添加按钮
            self.click_add_button()
            #设置URL地址
            self.set_url_address(url+str(i))
            #点击保存按钮
            self.click_save_button()
            time.sleep(2)
        time.sleep(30)
