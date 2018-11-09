#coding=utf-8
#作者：曾祥卫
#时间：2018.09.20
#描述：无线用户的控制层

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import Select
from publicControl.public_control import PublicControl
import time
from data import data

class WirelessClientControl(PublicControl):

    def __init__(self,driver):
        #继承PublicControl类的属性和方法
        PublicControl.__init__(self,driver)


    def menu_wirelessclient(self):
        """
        点击无线用户菜单
        """
        try:
            self.driver.find_element_by_css_selector(".wifiUser_lang.span_lang").click()
            self.driver.implicitly_wait(10)
            time.sleep(2)
        except Exception as e:
            self.get_picture("menu_wirelessclient")
            raise Exception("Web page click 'wirelessclient menu' element fail! The reason is %s"%e)

    def set_current_devices(self):
        """
        点击当前连接设备
        """
        try:
            self.driver.find_element_by_css_selector(".equipment_now.equipment_now_lang").click()
            self.driver.implicitly_wait(10)
            time.sleep(2)
        except Exception as e:
            raise Exception("Web page click 'current devices' element fail! The reason is %s"%e)

    def set_undecided_list(self):
        """
        #点击待定/白/黑名单按钮
        """
        try:
            self.driver.find_element_by_css_selector(".wireless_close.wireless_close_choose.filterList_lang").click()
            self.driver.implicitly_wait(10)
            time.sleep(2)
        except Exception as e:
            raise Exception("Web page click 'undecided list' element fail! The reason is %s"%e)

    ###########################################################################################
    ####################以下是当前连接设备页面的操作#################################################
    def click_refreh_button(self):
        """
        点击刷新按钮
        """
        try:
            self.driver.find_element_by_css_selector(".Refresh_wl.span.refresh_lang").click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'refresh button' element fail! The reason is %s"%e)

    def click_join_choice_button(self):
        """
        点击加入所选
        """
        try:
            self.driver.find_element_by_css_selector(".add_choose.span_wl.span.addChoose_lang").click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'join choice button' element fail! The reason is %s"%e)

    def click_current_devices_all_choices_button(self):
        """
        当前设备中-点击当前连接设备页面的全选
        """
        try:
            self.driver.find_element_by_css_selector(".all_Wireless_user.allChoose_wl.allChoose_lang").click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'current devices all choices button' element fail! The reason is %s"%e)

    def click_current_choice_n_list(self, n):
        """
        当前设备中-点击选择第几个list
        输入：n：第几个
        """
        try:
            tmps = self.driver.find_elements_by_css_selector(".uw_cbox")
            tmps[n].click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'choice n list' element fail! The reason is %s"%e)

    def get_current_devices_mac(self):
        """
        当前设备中-点获取client的mac地址--当只有唯一一个设备连接时
        """
        try:
            element = self.driver.find_element_by_css_selector(".mac_wuser")
            result = element.text
            return result
        except Exception as e:
            self.get_picture("get_current_devices_mac")
            raise Exception("Web page get 'current devices client's mac' element fail! The reason is %s"%e)

    ###########################################################################################
    ####################以下是待定名单页面的操作####################################################
    def click_add_button(self):
        """
        点击添加按钮
        """
        try:
            self.driver.find_element_by_css_selector(".span.span_wl.span_wl_add.hide_now.add_lang").click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'add button' element fail! The reason is %s"%e)

    def set_add_windows_equipment_name(self, name):
        """
        设置点击添加按钮后的窗口中的设备名称
        输入：name:设备名称
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".etext.name_user_wireless_add")
            tmp.clear()
            tmp.send_keys(name)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'add windows equipment name' element fail! The reason is %s"%e)

    def set_add_windows_mac(self, mac):
        """
        设置点击添加按钮后的窗口中的mac地址
        输入：mac
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".txt_mac.mac_user_wireless_add")
            tmp.clear()
            tmp.send_keys(mac)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'add windows mac address' element fail! The reason is %s"%e)

    def click_edit_n_list_button(self, n):
        """
        点击编辑第几个list
        输入：n：第几个
        """
        try:
            tmps = self.driver.find_elements_by_css_selector(".edit_wireless.glyphicon.glyphicon-wrench")
            tmps[n].click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'edit the n list button' element fail! The reason is %s"%e)

    def set_edit_windows_equipment_name(self, name):
        """
        设置点击编辑按钮后的窗口中的设备名称
        输入：name:设备名称
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".utext.name_user_wireless")
            tmp.clear()
            tmp.send_keys(name)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'edit windows equipment name' element fail! The reason is %s"%e)

    def set_edit_windows_mac(self, mac):
        """
        设置点击编辑按钮后的窗口中的mac地址
        输入：mac
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".utext.mac_user_wireless")
            tmp.clear()
            tmp.send_keys(mac)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'edit windows mac address' element fail! The reason is %s"%e)

    def click_namelist_save_button(self):
        """
        点击保存按钮
        """
        try:
            #定位一组元素
            tmps = self.driver.find_elements_by_xpath(".//input[@type='button' and (@value='保存' or @value='Save')]")
            for tmp in tmps:
                #如果有元素在页面上是显示状态，则点击
                if tmp.is_displayed():
                    tmp.click()
                    self.driver.implicitly_wait(10)
                    break
        except Exception as e:
            raise Exception("Web page click 'namelist save button' element fail! The reason is %s"%e)


    def click_undecided_devices_all_choices_button(self):
        """
        待定名单中-点击当前连接设备页面的全选
        """
        try:
            self.driver.find_element_by_css_selector(".all_choose_wl.allChoose_lang").click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'current devices all choices button' element fail! The reason is %s"%e)

    def click_undecided_choice_n_list(self, n):
        """
        待定名单中-点击选择第几个list
        输入：n：第几个
        """
        try:
            tmps = self.driver.find_elements_by_css_selector(".cbox_wireless")
            tmps[n].click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'choice n list' element fail! The reason is %s"%e)

    def get_undecided_client_mac(self):
        """
        获取待定名单中的mac地址--当只有唯一一个设备时
        """
        try:
            element = self.driver.find_element_by_css_selector(".mac_wireless")
            result = element.text
            return result
        except Exception as e:
            raise Exception("Web page get 'undecided client mac' element fail! The reason is %s"%e)

    def click_delete_button(self):
        """
        点击删除所选按钮
        """
        try:
            self.driver.find_element_by_css_selector(".span.span_wl.span_wl_del.hide_now.selChoose_lang").click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'delete button' element fail! The reason is %s"%e)

    def click_filter_rules_button(self):
        """
        点击过滤规则按钮
        """
        try:
            self.driver.find_element_by_css_selector(".span.span_wl.span_wl_choose.hide_now.filterRule_lang").click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'filter rules button' element fail! The reason is %s"%e)

    def set_filter_black_list(self):
        """
        点击黑名单按钮
        """
        try:
            self.driver.find_element_by_css_selector(".span_uw.blank_lang").click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'filter black_list' element fail! The reason is %s"%e)

    def set_filter_white_list(self):
        """
        点击白名单按钮
        """
        try:
            self.driver.find_element_by_css_selector(".span_uw.wriht_lang").click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'filter black_list' element fail! The reason is %s"%e)

    def set_stop_filter(self):
        """
        点击停止过滤按钮
        """
        try:
            self.driver.find_element_by_css_selector(".span_uw.stopFilter_lang").click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'stop filter' element fail! The reason is %s"%e)

