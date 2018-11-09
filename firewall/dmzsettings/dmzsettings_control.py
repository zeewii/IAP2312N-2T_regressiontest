#coding=utf-8
#作者：曾祥卫
#时间：2018.10.29
#描述：DMZ设置的控制层


from publicControl.public_control import PublicControl
import time, os
from selenium.webdriver.support.ui import Select


class DMZSettingsControl(PublicControl):

    def __init__(self,driver):
        #继承PublicControl类的属性和方法
        PublicControl.__init__(self,driver)


    def menu_DMZSettings(self):
        """
        点击DMZ设置菜单
        """
        try:
            self.driver.find_element_by_css_selector(".left_list_main.dnz_filter.child_left_list.b.dnz_filter_lang").click()
            self.driver.implicitly_wait(10)
            time.sleep(2)
        except Exception as e:
            raise Exception("Web page click 'DMZ settings menu' element fail! The reason is %s"%e)


    def set_DMZ_switch(self, mode):
        """
        选择DMZ开关
        输入：mode:0,1
        """
        try:
            element = self.driver.find_element_by_css_selector(".switch_dmz.utext.enableChoose_lang")
            Select(element).select_by_value(str(mode))
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'DMZ switch' element fail! The reason is %s"%e)

    def set_Host_IP(self, ip):
        """
        设置主机IP
        输入：ip
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".text.ip_Host")
            tmp.clear()
            tmp.send_keys(ip)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'Host ip' element fail! The reason is %s"%e)

