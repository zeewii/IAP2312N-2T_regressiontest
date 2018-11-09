#coding=utf-8
#作者：曾祥卫
#时间：2018.09.21
#描述：系统重启的控制层


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import Select
from publicControl.public_control import PublicControl
import time
from data import data


class RebootSystemControl(PublicControl):

    def __init__(self,driver):
        #继承PublicControl类的属性和方法
        PublicControl.__init__(self,driver)


    def menu_rebootsystem(self):
        """
        点击系统重启菜单
        """
        try:
            self.driver.find_element_by_css_selector(".left_list_main.reboot.child_left_list.b.reboot_lang").click()
            self.driver.implicitly_wait(10)
            time.sleep(2)
        except Exception as e:
            raise Exception("Web page click 'reboot system menu' element fail! The reason is %s"%e)

    def click_reboot_button(self):
        """
        点击重启设备
        """
        try:
            self.driver.find_element_by_css_selector(".button.btn_reboot.Estart_lang").click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'reboot button' element fail! The reason is %s"%e)

    def click_restart_confirm_button(self):
        """
        点击确认重启系统窗口的确认按钮
        """
        try:
            element = self.driver.find_element_by_css_selector(".button.confirmBtn.confirmBtn_restart")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'restart confirm button' element fail! The reason is %s"%e)






















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
        except Exception as e:
            raise Exception("Web page set 'select file' element fail! The reason is %s"%e)

    def click_upload_button(self):
        """
        点击上传配置
        """
        try:
            self.driver.find_element_by_id("btn_update").click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'upload button' element fail! The reason is %s"%e)









































