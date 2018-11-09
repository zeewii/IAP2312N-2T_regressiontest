#coding=utf-8
#作者：曾祥卫
#时间：2018.09.21
#描述：状态信息的控制层

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import Select
from publicControl.public_control import PublicControl
import time
from data import data

class StateInfoControl(PublicControl):

    def __init__(self,driver):
        #继承PublicControl类的属性和方法
        PublicControl.__init__(self,driver)


    def menu_stateinfo(self):
        """
        点击状态信息设置菜单
        """
        try:
            self.driver.find_element_by_css_selector(".status_info_lang.span_lang").click()
            self.driver.implicitly_wait(10)
            time.sleep(2)
        except Exception as e:
            self.get_picture("menu_stateinfo")
            raise Exception("Web page click 'stateinfo menu' element fail! The reason is %s"%e)

    def get_wifi_upload(self):
        """
        获取WIFI总上行：由数字和单位组成，如50MB
        """
        try:
            #取WIFI总上行的数字
            value = self.driver.find_element_by_css_selector(".col-xs-4.tx_history").text.strip()
            #取WIFI总上行的单位
            unit = self.driver.find_element_by_css_selector(".col-xs-1.kb_mb_tx").text.strip()
            print(value, unit)
            return value, unit
        except Exception as e:
            raise Exception("Web page get 'wifi upload' element fail! The reason is %s"%e)

    def get_wifi_download(self):
        """
        获取WIFI总下行：由数字和单位组成，如50MB
        """
        try:
            #取WIFI总下行的数字
            value = self.driver.find_element_by_css_selector(".col-xs-4.rx_history").text.strip()
            #取WIFI总下行的单位
            unit = self.driver.find_element_by_css_selector(".col-xs-1.kb_mb_rx").text.strip()
            print(value, unit)
            return value, unit
        except Exception as e:
            raise Exception("Web page get 'wifi download' element fail! The reason is %s"%e)

    def get_cpu_utilization(self):
        """
        获取CPU使用率
        """
        try:
            tmp = self.driver.find_element_by_id("s1").text.strip("%")
            #转换为int
            result = int(tmp)
            print(result)
            return result
        except Exception as e:
            raise Exception("Web page get 'cpu utilization' element fail! The reason is %s"%e)

    def get_memory_utilization(self):
        """
        获取内存使用率
        """
        try:
            tmp = self.driver.find_element_by_id("s2").text.strip("%")
            #转换为int
            result = int(tmp)
            print(result)
            return result
        except Exception as e:
            raise Exception("Web page get 'memory utilization' element fail! The reason is %s"%e)

    def get_current_mode(self):
        """
        获取当前模式
        """
        try:
            result = self.driver.find_element_by_css_selector(".midel_now").text
            print(result)
            return result
        except Exception as e:
            self.get_picture("get_current_mode")
            raise Exception("Web page get 'current mode' element fail! The reason is %s"%e)

    def get_wireless_client(self):
        """
        获取无线用户数
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".wifi_user_sys").text
            #转换为int
            result = int(tmp)
            print(result)
            return result
        except Exception as e:
            raise Exception("Web page get 'wireless client' element fail! The reason is %s"%e)

    def get_running_time(self):
        """
        获取运行时长
        """
        try:
            result = self.driver.find_element_by_css_selector(".running_time").text
            print(result)
            return result
        except Exception as e:
            raise Exception("Web page get 'running time' element fail! The reason is %s"%e)

    def get_MAC_address(self):
        """
        获取MAC地址
        """
        try:
            result = self.driver.find_element_by_css_selector(".sys_macAddr").text
            print(result)
            return result
        except Exception as e:
            raise Exception("Web page get 'MAC address' element fail! The reason is %s"%e)

    def get_equipment_model(self):
        """
        获取设备型号
        """
        try:
            result = self.driver.find_element_by_css_selector(".equ_model").text
            print(result)
            return result
        except Exception as e:
            raise Exception("Web page get 'equipment model' element fail! The reason is %s"%e)

    def get_firmware_version(self):
        """
        获取固件版本
        """
        try:
            result = self.driver.find_element_by_css_selector(".firmware_version").text
            print(result)
            return result
        except Exception as e:
            raise Exception("Web page get 'firmware version' element fail! The reason is %s"%e)

    def get_24g_ssid(self):
        """
        获取2.4G的ssid
        """
        try:
            result = self.driver.find_element_by_css_selector(".ssid_24g_one").text
            print(result)
            return result
        except Exception as e:
            raise Exception("Web page get '2.4G ssid' element fail! The reason is %s"%e)

    def get_WAN_IP_generation(self):
        """
        获取IP获取方式
        """
        try:
            result = self.driver.find_element_by_css_selector(".method_obtain_con").text
            print(result)
            return result
        except Exception as e:
            raise Exception("Web page get 'IP generation' element fail! The reason is %s"%e)

    def get_WAN_IP_address(self):
        """
        获取IP地址
        """
        try:
            result = self.driver.find_element_by_css_selector(".ipAddr_lu_qiao_con").text
            print(result)
            return result
        except Exception as e:
            raise Exception("Web page get 'IP address' element fail! The reason is %s"%e)