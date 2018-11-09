#coding=utf-8
#作者：曾祥卫
#时间：2018.09.20
#描述：无线探针的控制层


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import Select
from publicControl.public_control import PublicControl
import time
from data import data


class WirelessProbeControl(PublicControl):

    def __init__(self,driver):
        #继承PublicControl类的属性和方法
        PublicControl.__init__(self,driver)


    def menu_wirelessprobe(self):
        """
        点击无线探针菜单
        """
        try:
            self.driver.find_element_by_css_selector(".left_list_main.probe.child_left_list.b.probe_lang").click()
            self.driver.implicitly_wait(10)
            time.sleep(2)
        except Exception as e:
            raise Exception("Web page click 'wireless probe menu' element fail! The reason is %s"%e)

    def enable_wirless_probe(self):
        """
        开启无线探针
        """
        try:
            element = self.driver.find_element_by_id("probeOn")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'enable wirless probe' element fail! The reason is %s"%e)

    def disable_wirless_probe(self):
        """
        关闭无线探针
        """
        try:
            element = self.driver.find_element_by_id("probeOff")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'disable wirless probe' element fail! The reason is %s"%e)

    def set_server_address(self, address):
        """
        输入服务器地址
        输入：address
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".uetext.server_porbe.words_kpng")
            tmp.clear()
            tmp.send_keys(address)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'server address' element fail! The reason is %s"%e)

    def set_udp_port_number(self, port):
        """
        输入UDP端口号
        输入：port
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".uetext.dport_porbe.words_kpng")
            tmp.clear()
            tmp.send_keys(port)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'udp port number' element fail! The reason is %s"%e)

    def set_max_PDU(self, value):
        """
        输入最大的PDU
        输入：value
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".uetext.max_pdu_porbe")
            tmp.clear()
            tmp.send_keys(value)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'max PDU' element fail! The reason is %s"%e)

    def set_message_upload_interval(self, t):
        """
        输入报文上传间隔
        输入：t:间隔时间
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".uetext.report_interval_porbe")
            tmp.clear()
            tmp.send_keys(t)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'message upload interval' element fail! The reason is %s"%e)

    def set_upload_interval_of_the_same_device(self, t):
        """
        同一设备上传间隔
        输入：t:间隔时间
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".uetext.air_interval_porbe")
            tmp.clear()
            tmp.send_keys(t)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'upload interval of the same device' element fail! The reason is %s"%e)

    def set_effective_signal_threshold(self, value):
        """
        有效信号阀值
        输入：value
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".uetext.air_min_signal")
            tmp.clear()
            tmp.send_keys(value)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'effective signal threshold' element fail! The reason is %s"%e)
















