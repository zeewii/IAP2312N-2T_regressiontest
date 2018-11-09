#coding=utf-8
#作者：曾祥卫
#时间：2018.09.20
#描述：外网设置的控制层


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import Select
from publicControl.public_control import PublicControl
import time
from data import data


class WanSettingsControl(PublicControl):

    def __init__(self,driver):
        #继承PublicControl类的属性和方法
        PublicControl.__init__(self,driver)


    def menu_wansettings(self):
        """
        点击外网设置设置菜单
        """
        try:
            self.driver.find_element_by_css_selector(".left_list_main.Extranet.child_left_list.b.Extranet_lang").click()
            self.driver.implicitly_wait(10)
            time.sleep(2)
        except Exception as e:
            raise Exception("Web page click 'wan settings menu' element fail! The reason is %s"%e)

    def set_pppoe(self):
        """
        点击pppoe按钮
        """
        try:
            self.driver.find_element_by_css_selector(".first_span.span.choose_span").click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'pppoe button' element fail! The reason is %s"%e)

    def set_staticIP(self):
        """
        点击静态IP按钮
        """
        try:
            self.driver.find_element_by_css_selector(".second_span.span.choose_span.static_lang").click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'staticIP button' element fail! The reason is %s"%e)

    def set_dhcp(self):
        """
        点击动态获取按钮
        """
        try:
            self.driver.find_element_by_css_selector(".thied_span.span.choose_span.dhcp_lang").click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'dhcp button' element fail! The reason is %s"%e)

    def set_pppoe_user(self, pppoe_user):
        """
        输入pppoe的用户名
        输入：pppoe_user：pppoe的用户名
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".etext.Extranet_uname.empty_text")
            tmp.clear()
            tmp.send_keys(pppoe_user)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'pppoe user' element fail! The reason is %s"%e)

    def set_pppoe_password(self, pppoe_password):
        """
        输入pppoe的密码
        输入：pppoe_password：pppoe的密码
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".etext.Extranet_pwd.empty_text")
            tmp.clear()
            tmp.send_keys(pppoe_password)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'pppoe password' element fail! The reason is %s"%e)

    def set_pppoe_mtu(self, mtu):
        """
        输入pppoe的mtu
        输入：mtu值：int和str都可
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".etext.Extranet_mt")
            tmp.clear()
            tmp.send_keys(str(mtu))
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'pppoe mtu' element fail! The reason is %s"%e)

    def set_pppoe_server_name(self, name):
        """
        输入pppoe的服务名称
        输入：name:服务名称
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".etext.Extranet_server")
            tmp.clear()
            tmp.send_keys(name)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'pppoe server name' element fail! The reason is %s"%e)

    def set_pppoe_dns(self, dns):
        """
        输入pppoe的dns
        输入：dns
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".uetext.Extranet_dns_pp")
            tmp.clear()
            tmp.send_keys(dns)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'pppoe dns' element fail! The reason is %s"%e)

    def set_staticIP_IP(self, ip):
        """
        输入静态ip的ip地址
        输入：ip：ip地址
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".text.Extranet_ip_wan")
            tmp.clear()
            tmp.send_keys(ip)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'staticIP ip address' element fail! The reason is %s"%e)

    def set_staticIP_netmask(self, netmask):
        """
        输入静态ip的子网掩码
        输入：netmask：子网掩码
        """
        try:
            element = self.driver.find_element_by_css_selector(".utext.netmask_wan_Extranet")
            Select(element).select_by_value(netmask)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'staticIP netmask' element fail! The reason is %s"%e)

    def set_staticIP_gateway(self, gateway):
        """
        输入静态ip的gateway
        输入：gateway：gateway地址
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".text.Extranet_gateway")
            tmp.clear()
            tmp.send_keys(gateway)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'staticIP gateway' element fail! The reason is %s"%e)

    def set_staticIP_dns(self, dns):
        """
        输入静态ip的dns
        输入：dns：dns地址
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".uetext.Extranet_dns_static")
            tmp.clear()
            tmp.send_keys(dns)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'staticIP dns' element fail! The reason is %s"%e)

    def set_dhcp_dns(self, dns):
        """
        输入dhcp的dns
        输入：dns：dns地址
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".uetext.Extranet_dns_dhcp")
            tmp.clear()
            tmp.send_keys(dns)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'dhcp dns' element fail! The reason is %s"%e)










































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
            Select(element).select_by_value(mode)
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

    def click_save_button(self):
        """
        点击设置按钮--保存
        """
        try:
            #定位一组元素
            tmps = self.driver.find_elements_by_xpath(".//input[@type='button' and (@value='设置' or @value='Save')]")
            for tmp in tmps:
                #如果有元素在页面上是显示状态，则点击
                if tmp.is_displayed():
                    tmp.click()
                    self.driver.implicitly_wait(10)
                    time.sleep(1)
                    break
        except Exception as e:
            raise Exception("Web page click 'save button' element fail! The reason is %s"%e)

    def click_reset_button(self):
        """
        点击重置按钮--取消
        """
        try:
            #定位一组元素
            tmps = self.driver.find_elements_by_xpath(".//input[@type='reset' and (@value='重置' or @value='Reset')]")
            for tmp in tmps:
                #如果有元素在页面上是显示状态，则点击
                if tmp.is_displayed():
                    tmp.click()
                    self.driver.implicitly_wait(10)
                    break
        except Exception as e:
            raise Exception("Web page click 'reset button' element fail! The reason is %s"%e)
