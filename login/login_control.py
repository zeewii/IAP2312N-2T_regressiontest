#coding=utf-8
#作者：曾祥卫
#时间：2018.09.17
#描述：AP登录的控制层

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from publicControl.public_control import PublicControl
from selenium.webdriver.common.keys import Keys
import time
from data import data

class LoginControl(PublicControl):

    def __init__(self,driver,username=None,pwd=None):
        #继承PublicControl类的属性和方法
        PublicControl.__init__(self,driver)
        #自己LoginControl类的属性
        self.username = username
        self.pwd = pwd

    def set_username(self):
        """
        输入用户名
        """
        try:
            WebDriverWait(self.driver,120).until(lambda x:self.driver.find_element_by_class_name("uname"))
        except:
            data_basic = data.data_basic()
            PublicControl.wlan_enable(self,data_basic['lan_pc'])
            PublicControl.dhcp_release_wlan(self,data_basic['wlan_pc'])
            #指定有线网卡的固定ip--能够访问ap的webpage
            PublicControl.set_eth_ip(self, data_basic['lan_pc'], data_basic['static_PC_ip'])
            time.sleep(60)
            #self.driver.close()
            self.driver.refresh()
            self.driver.implicitly_wait(20)
        finally:
            time.sleep(4)
            username_element = self.driver.find_element_by_class_name("uname")
            username_element.clear()
            username_element.send_keys(self.username)


    def set_username_backup(self):
        """
        输入用户名--backup
        """
        try:
            self.driver.find_element_by_class_name("uname")
        except:
            data_basic = data.data_basic()
            PublicControl.wlan_enable(self,data_basic['lan_pc'])
            PublicControl.dhcp_release_wlan(self,data_basic['wlan_pc'])
            PublicControl.dhcp_wlan(self,data_basic['lan_pc'])
            time.sleep(60)
            #self.driver.close()
            self.driver.refresh()
            self.driver.implicitly_wait(20)
            time.sleep(60)
        finally:
            username_element = self.driver.find_element_by_class_name("uname")
            username_element.clear()
            username_element.send_keys(self.username)

    def get_username(self):
        """
        获取用户名
        """
        try:
            username = self.driver.find_element_by_class_name("uname").text
            return username
        except Exception as e:
            raise Exception("Login page get 'username' element is error! The reason is %s"%e)


    def set_pwd(self):
        """
        输入密码
        """
        try:
            pwd_element = self.driver.find_element_by_class_name("upwd")
            pwd_element.clear()
            pwd_element.send_keys(self.pwd)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Login page get 'upwd' element is error! The reason is %s"%e)



    def get_pwd(self):
        """
        获取密码
        """
        try:
            pwd = self.driver.find_element_by_class_name("upwd").text
            return pwd
        except Exception as e:
            raise Exception("Login page get 'upwd' element is error! The reason is %s"%e)

    def submit(self):
        """
        点击登录按钮
        """
        try:
            submit_element = self.driver.find_element_by_css_selector(".btn_login.ligin_lang")
            submit_element.click()
            self.driver.implicitly_wait(20)
            time.sleep(3)
        except Exception as e:
            raise Exception("Login page has not found 'login button' element! The reason is %s"%e)

    def submit_backup(self):
        """
        点击键盘enter键
        """
        try:
            pwd_element = self.driver.find_element_by_class_name("upwd")
            pwd_element.send_keys(Keys.ENTER)
            self.driver.implicitly_wait(20)
            time.sleep(2)
        except Exception as e:
            raise Exception("Login page has not found 'login button' element! The reason is %s"%e)

    def click_uname_rem(self):
        """
        点击记住帐号
        """
        try:
            element = self.driver.find_element_by_id("uname_rem")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("Login page has not found 'remmber name' element! The reason is %s"%e)


    def click_upwd_rem(self):
        """
        点击记住密码
        """
        try:
            element = self.driver.find_element_by_id("upwd_rem")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("Login page has not found 'remmber password' element! The reason is %s"%e)


    def click_change_language(self):
        """
        点击语言切换
        """
        try:
            element = self.driver.find_element_by_css_selector(".btn_lang.btnLogin_lang")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("Login page has not found 'language' element! The reason is %s"%e)

    def get_display_language(self):
        """
        获取登录页面上的语言
        """
        try:
            element = self.driver.find_element_by_css_selector(".btn_lang.btnLogin_lang")
            result = element.get_attribute("value")
            return result
        except Exception as e:
            raise Exception("Login page has not found 'language' element! The reason is %s"%e)


    def click_Navbar_change_language(self):
        """
        点击导航条上的语言切换
        """
        try:
            element = self.driver.find_element_by_css_selector(".btn_top")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("Navbar page has not found 'Navbar change language' element! The reason is %s"%e)

    def get_Navbar_display_language(self):
        """
        获取导航条上的语言
        """
        try:
            element = self.driver.find_element_by_css_selector(".btn_top")
            result = element.get_attribute("value")
            return result
        except Exception as e:
            raise Exception("Navbar page has not found 'Navbar language' element! The reason is %s"%e)

    def click_Navbar_logout(self):
        """
        点击导航条上的退出
        """
        try:
            element = self.driver.find_element_by_css_selector(".btn_top2.btn_Esc")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("Navbar page has not found 'Navbar logout' element! The reason is %s"%e)