#coding=utf-8
#作者：曾祥卫
#时间：2018.09.21
#描述：用户设置的控制层


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import Select
from publicControl.public_control import PublicControl
import time
from data import data


class UserSettingsControl(PublicControl):

    def __init__(self,driver):
        #继承PublicControl类的属性和方法
        PublicControl.__init__(self,driver)


    def menu_usersettings(self):
        """
        点击用户设置设置菜单
        """
        try:
            self.driver.find_element_by_css_selector(".left_list_main.User_settings.child_left_list.b.User_settings_lang").click()
            self.driver.implicitly_wait(10)
            time.sleep(2)
        except Exception as e:
            raise Exception("Web page click 'user settings menu' element fail! The reason is %s"%e)

    def set_new_username(self, name):
        """
        输入新用户名称
        输入：name
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".userName_setting.utext")
            tmp.clear()
            tmp.send_keys(name)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'name' element fail! The reason is %s"%e)

    def set_old_password(self, password):
        """
        输入旧密码
        输入：password
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".pwd_old_us.utext")
            tmp.clear()
            tmp.send_keys(password)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'old password' element fail! The reason is %s"%e)

    def set_new_password(self, password):
        """
        输入新密码
        输入：password
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".pwd_new_us.utext")
            tmp.clear()
            tmp.send_keys(password)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'new password' element fail! The reason is %s"%e)






