#coding=utf-8
#作者：曾祥卫
#时间：2018.10.29
#描述：ARP绑定的控制层


from publicControl.public_control import PublicControl
import time, os
from selenium.webdriver.support.ui import Select


class ArpBindingControl(PublicControl):

    def __init__(self,driver):
        #继承PublicControl类的属性和方法
        PublicControl.__init__(self,driver)


    def menu_arpbinding(self):
        """
        点击ARP绑定菜单
        """
        try:
            self.driver.find_element_by_css_selector(".left_list_main.apr_binding.child_left_list.b.apr_binding_lang").click()
            self.driver.implicitly_wait(10)
            time.sleep(2)
        except Exception as e:
            raise Exception("Web page click 'arp binding menu' element fail! The reason is %s"%e)

    def click_add_button(self):
        """
        点击添加按钮
        """
        try:
            tmps = self.driver.find_elements_by_css_selector(".right_btn.right_btn1.span.add_lang")
            for tmp in tmps:
                if tmp.is_displayed():
                    tmp.click()
                    break
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'add button' element fail! The reason is %s"%e)

    def click_delete_button(self):
        """
        点击删除所选按钮
        """
        try:
            tmps = self.driver.find_elements_by_css_selector(".del_choose.right_btn.right_btn2.span.selChoose_lang")
            for tmp in tmps:
                if tmp.is_displayed():
                    tmp.click()
                    break
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'delete button' element fail! The reason is %s"%e)

    def click_all_choices_button(self):
        """
        点击IP过滤列表中的全选
        """
        try:
            #self.driver.find_element_by_css_selector("table.ip_filter_tab>tbody>tr>td.all_choose.allChoose_lang").click()
            tmps = self.driver.find_elements_by_css_selector(".all_choose.allChoose_lang")
            for tmp in tmps:
                if tmp.is_displayed():
                    tmp.click()
                    break
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'all choices button' element fail! The reason is %s"%e)

    def click_edit_n_list_button(self, n):
        """
        点击编辑第几个list
        输入：n：第几个
        """
        try:
            tmps = self.driver.find_elements_by_xpath(".//*[@class='apr_filter_tab']//span[@title='编辑' or @title='edit']")
            tmps[n].click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'edit the n list button' element fail! The reason is %s"%e)

    def click_bind_n_list_button(self, n):
        """
        点击第几个list后的绑定按钮
        输入：n：第几个
        """
        try:
            tmps = self.driver.find_elements_by_xpath(".//*[@class='apr_filter_tab']//span[@title='绑定' or @title='bind']")
            tmps[n].click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'bind the n list button' element fail! The reason is %s"%e)

    def click_choice_n_list(self, n):
        """
        点击选择第几个list
        输入：n：第几个
        """
        try:
            tmps = self.driver.find_elements_by_xpath(".//*[@class='apr_filter_tab']//input")
            tmps[n].click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'choice n list' element fail! The reason is %s"%e)

    ###########################################################################################
    ####################以下是添加ARP绑定设置窗口中页面的操作##############################################
    def set_IP_address(self, ip):
        """
        设置IP地址
        输入：ip
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".text.arp_filter_ipadd")
            tmp.clear()
            tmp.send_keys(ip)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'ip address' element fail! The reason is %s"%e)

    def set_mac(self, mac):
        """
        输入mac地址
        输入：mac
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".txt_mac.arp_mac_popup")
            tmp.clear()
            tmp.send_keys(mac)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'mac' element fail! The reason is %s"%e)

    def set_Network(self, mode):
        """
        选择所属网络
        输入：mode:lan,wan
        """
        try:
            element = self.driver.find_element_by_css_selector(".utext.arp_filter_lan")
            Select(element).select_by_value(mode)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'Network' element fail! The reason is %s"%e)


    def set_Remarks(self, str):
        """
        输入备注
        输入：str,备注信息
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".utext.arp_filter_remark")
            tmp.clear()
            tmp.send_keys(str)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'Remarks' element fail! The reason is %s"%e)

    def click_save_button(self):
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
            raise Exception("Web page click 'save button' element fail! The reason is %s"%e)

    def click_close_button(self):
        """
        点击关闭按钮
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".close_arp_filter_popup")
            tmp.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'close button' element fail! The reason is %s"%e)