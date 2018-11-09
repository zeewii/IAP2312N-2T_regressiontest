#coding=utf-8
#作者：曾祥卫
#时间：2018.09.21
#描述：配置更新的控制层


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import Select
from publicControl.public_control import PublicControl
import time
from data import data


class ConfigUpdateControl(PublicControl):

    def __init__(self,driver):
        #继承PublicControl类的属性和方法
        PublicControl.__init__(self,driver)


    def menu_configupdate(self):
        """
        点击配置更新菜单
        """
        try:
            self.driver.find_element_by_css_selector(".left_list_main.config.child_left_list.b.config_lang").click()
            self.driver.implicitly_wait(10)
            time.sleep(2)
        except Exception as e:
            raise Exception("Web page click 'config update menu' element fail! The reason is %s"%e)

    def click_download_button(self):
        """
        点击下载配置
        """
        try:
            self.driver.find_element_by_css_selector(".btn_config_backups.downloadConfig_lang").click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'download button' element fail! The reason is %s"%e)

    def click_restore_factory_button(self):
        """
        点击恢复出厂设置
        """
        try:
            self.driver.find_element_by_css_selector(".btn_config_reduction.recovery_lang").click()
            self.driver.implicitly_wait(10)
            time.sleep(2)
        except Exception as e:
            raise Exception("Web page click 'restore factory button' element fail! The reason is %s"%e)

    def set_select_fle(self, path):
        """
        选择文件
        输入：path：文件的路径
        """
        try:
            element = self.driver.find_element_by_css_selector(".txt_file_update")
            element.send_keys(path)
            self.driver.implicitly_wait(10)
            time.sleep(10)
        except Exception as e:
            raise Exception("Web page set 'select file' element fail! The reason is %s"%e)

    def click_upload_button(self):
        """
        点击上传配置
        """
        try:
            self.driver.find_element_by_id("btn_update").click()
            self.driver.implicitly_wait(10)
            time.sleep(10)
        except Exception as e:
            raise Exception("Web page click 'upload button' element fail! The reason is %s"%e)

    def click_upload_confirm_button(self):
        """
        点击确认上传配置文件窗口的确认按钮
        """
        try:
            element = self.driver.find_element_by_css_selector(".button.confirmBtn.confirmBtn_upload")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'upload confirm button' element fail! The reason is %s"%e)

    def click_recovery_confirm_button(self):
        """
        点击确认恢复出厂设置窗口的确认按钮
        """
        try:
            element = self.driver.find_element_by_css_selector(".button.confirmBtn.confirmBtn_recovery")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'recovery confirm button' element fail! The reason is %s"%e)





































