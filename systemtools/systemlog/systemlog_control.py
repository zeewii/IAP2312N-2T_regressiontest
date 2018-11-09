#coding=utf-8
#作者：曾祥卫
#时间：2018.09.21
#描述：系统日志的控制层


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import Select
from publicControl.public_control import PublicControl
import time
from data import data


class SystemLogControl(PublicControl):

    def __init__(self,driver):
        #继承PublicControl类的属性和方法
        PublicControl.__init__(self,driver)


    def menu_systemlog(self):
        """
        点击系统日志菜单
        """
        try:
            self.driver.find_element_by_css_selector(".left_list_main.system_log.child_left_list.b.system_log_lang").click()
            self.driver.implicitly_wait(10)
            time.sleep(2)
        except Exception as e:
            raise Exception("Web page click 'system log menu' element fail! The reason is %s"%e)

    def click_export_button(self):
        """
        点击导出按钮
        """
        try:
            self.driver.find_element_by_css_selector(".log_s.log_s_1.export_log.span.export_lang").click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'export button' element fail! The reason is %s"%e)

    def click_refresh_button(self):
        """
        点击刷新按钮
        """
        try:
            self.driver.find_element_by_css_selector(".log_s.reloaded.span.refresh_lang").click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'refresh button' element fail! The reason is %s"%e)

    def set_Num(self, num):
        """
        选择序号
        输入：num:none_ch,err_log,warn_log
        """
        try:
            element = self.driver.find_element_by_css_selector(".sel_statistics_log")
            Select(element).select_by_value(num)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'Num' element fail! The reason is %s"%e)

    def click_time_button(self):
        """
        点击时间按钮
        """
        try:
            self.driver.find_element_by_css_selector(".timeChose_log").click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'time button' element fail! The reason is %s"%e)

    def click_filter_button(self):
        """
        点击筛选按钮
        """
        try:
            #定位一组元素
            tmps = self.driver.find_elements_by_xpath(".//input[@type='button' and (@value='筛选' or @value='Filter')]")
            for tmp in tmps:
                #如果有元素在页面上是显示状态，则点击
                if tmp.is_displayed():
                    tmp.click()
                    self.driver.implicitly_wait(10)
                    break
        except Exception as e:
            raise Exception("Web page click 'filter button' element fail! The reason is %s"%e)

    def click_close_button(self):
        """
        点击关闭按钮
        """
        try:
            #定位一组元素
            tmps = self.driver.find_elements_by_xpath(".//input[@type='button' and (@value='关闭' or @value='Close')]")
            for tmp in tmps:
                #如果有元素在页面上是显示状态，则点击
                if tmp.is_displayed():
                    tmp.click()
                    self.driver.implicitly_wait(10)
                    break
        except Exception as e:
            raise Exception("Web page click 'Close button' element fail! The reason is %s"%e)
































