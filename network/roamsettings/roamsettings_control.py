#coding=utf-8
#作者：曾祥卫
#时间：2018.09.20
#描述：漫游设置的控制层


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import Select
from publicControl.public_control import PublicControl
import time
from data import data


class RoamSettingsControl(PublicControl):

    def __init__(self,driver):
        #继承PublicControl类的属性和方法
        PublicControl.__init__(self,driver)


    def menu_roamsettings(self):
        """
        点击漫游设置菜单
        """
        try:
            self.driver.find_element_by_css_selector(".left_list_main.Roam.child_left_list.b.Roam_lang").click()
            self.driver.implicitly_wait(10)
            time.sleep(2)
        except Exception as e:
            raise Exception("Web page click 'roam settings menu' element fail! The reason is %s"%e)

    def set_roam_ssid(self, ssid):
        """
        设置漫游的ssid
        输入：ssid
        """
        try:
            element = self.driver.find_element_by_css_selector(".utext.ssid_roam")
            Select(element).select_by_value(ssid)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'roam ssid' element fail! The reason is %s"%e)

    def enable_disable_roam(self, value):
        """
        开启或关闭AP漫游
        输入：value：0：关闭;1:开启--输入格式str或int皆可
        """
        try:
            element = self.driver.find_element_by_css_selector(".utext.ieee80211r_ap_roam.enableChoose_lang")
            Select(element).select_by_value(str(value))
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'enable/disable roam' element fail! The reason is %s"%e)

    def set_mobility_domain_identifier(self, value):
        """
        输入漫游标识符
        输入：value
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".utext.mark16_Roam")
            tmp.clear()
            tmp.send_keys(value)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'mobility domain identifier' element fail! The reason is %s"%e)

    def set_mobility_domain_BSSID_list(self, value):
        """
        输入漫游BSSID列表
        输入：value 格式：00:11:22:33:44:55;22:33:44:55:66:77
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".mac_Roam")
            tmp.clear()
            tmp.send_keys(value)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'mobility domain BSSID list' element fail! The reason is %s"%e)





