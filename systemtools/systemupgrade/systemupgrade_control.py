#coding=utf-8
#作者：曾祥卫
#时间：2018.09.21
#描述：系统升级的控制层


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import Select
from publicControl.public_control import PublicControl
import time
from data import data


class SystemUpgradeControl(PublicControl):

    def __init__(self,driver):
        #继承PublicControl类的属性和方法
        PublicControl.__init__(self,driver)


    def menu_systemupgrade(self):
        """
        点击系统升级设置菜单
        """
        try:
            self.driver.find_element_by_css_selector(".left_list_main.System_upgrade.child_left_list.b.System_upgrade_lang").click()
            self.driver.implicitly_wait(10)
            time.sleep(2)
        except Exception as e:
            raise Exception("Web page click 'system upgrade menu' element fail! The reason is %s"%e)

    def get_firmware_version(self):
        """
        获取固件版本
        """
        try:
            element = self.driver.find_element_by_css_selector(".version_System")
            version = element.text
            return version
        except Exception as e:
            raise Exception("Web page get 'firmware version' element fail! The reason is %s"%e)

    def set_select_firmware(self, path):
        """
        选择固件文件
        输入：path：固件文件的路径
        """
        try:
            element = self.driver.find_element_by_css_selector(".txt_file")
            element.send_keys(path)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'select firmware' element fail! The reason is %s"%e)

    def click_update_button(self):
        """
        点击升级固件按钮
        """
        try:
            element = self.driver.find_element_by_css_selector(".button.btn_upgrade.UpdateFirmware_lang")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'update button' element fail! The reason is %s"%e)





















