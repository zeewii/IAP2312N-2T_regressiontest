#coding=utf-8
#作者：曾祥卫
#时间：2018.09.20
#描述：内网设置的控制层


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import Select
from publicControl.public_control import PublicControl
import time
from data import data


class LanSettingsControl(PublicControl):

    def __init__(self,driver):
        #继承PublicControl类的属性和方法
        PublicControl.__init__(self,driver)


    def menu_lansettings(self):
        """
        点击内网设置菜单
        """
        try:
            self.driver.find_element_by_css_selector(".left_list_main.Intranet.child_left_list.b.Intranet_lang").click()
            self.driver.implicitly_wait(10)
            time.sleep(2)
        except Exception as e:
            raise Exception("Web page click 'lan settings menu' element fail! The reason is %s"%e)

    def set_ip(self, ip):
        """
        输入内网设置的ip地址
        输入：ip：ip地址
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".text.Intranet_nei_ip")
            tmp.clear()
            tmp.send_keys(ip)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'ip' element fail! The reason is %s"%e)

    def set_netmask(self, netmask):
        """
        输入内网设置的子网掩码
        输入：netmask：子网掩码
        """
        try:
            element = self.driver.find_element_by_css_selector(".utext.client_mask_01.netmask_lan_Intranet")
            Select(element).select_by_value(netmask)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'netmask' element fail! The reason is %s"%e)

    def set_dhcp_server(self, mode):
        """
        配置DHCP服务器
        输入：mode:0：禁用，1：启用
        """
        try:
            element = self.driver.find_element_by_css_selector(".utext.dhcp_lan_Intranet.enableChoose_lang")
            Select(element).select_by_value(str(mode))
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'DHCP Server mode' element fail! The reason is %s"%e)

    def set_dhcp_start_address(self, ip):
        """
        输入DHCP开始地址
        输入：ip：ip地址
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".etext.dhcp_lan_start_Intranet")
            tmp.clear()
            tmp.send_keys(ip)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'dhcp start address' element fail! The reason is %s"%e)

    def set_dhcp_ip_size(self, n):
        """
        输入DHCP地址个数
        输入：n:地址数--int和str类型都可
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".etext.count_lan_Intranet")
            tmp.clear()
            tmp.send_keys(str(n))
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'dhcp ip size' element fail! The reason is %s"%e)

    def set_dhcp_lease_time(self, t):
        """
        输入DHCP租约时间
        输入：t:时间--int和str类型都可
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".etext.dncp_leasetime_Intranet")
            tmp.clear()
            tmp.send_keys(str(t))
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'dhcp lease time' element fail! The reason is %s"%e)

    def set_dhcp_lease_timeunit(self, unit):
        """
        配置DHCP租约时间的单位
        输入：unit:h,m,d
        """
        try:
            element = self.driver.find_element_by_css_selector(".timelength_change")
            Select(element).select_by_value(unit)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'DHCP lease timeunit' element fail! The reason is %s"%e)

    def set_domain_name(self, name):
        """
        输入域名名称
        输入：name:域名名称
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".utext.domain_lan_Intranet")
            tmp.clear()
            tmp.send_keys(name)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'domain name' element fail! The reason is %s"%e)


