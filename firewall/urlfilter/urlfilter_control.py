#coding=utf-8
#作者：曾祥卫
#时间：2018.10.29
#描述：URL过滤的控制层


from publicControl.public_control import PublicControl
import time, os
from selenium.webdriver.support.ui import Select


class UrlFilterControl(PublicControl):

    def __init__(self,driver):
        #继承PublicControl类的属性和方法
        PublicControl.__init__(self,driver)


    def menu_urlfilter(self):
        """
        点击url过滤菜单
        """
        try:
            self.driver.find_element_by_css_selector(".left_list_main.url_Filter.child_left_list.b.url_Filter_lang").click()
            self.driver.implicitly_wait(10)
            time.sleep(2)
        except Exception as e:
            raise Exception("Web page click 'url filter menu' element fail! The reason is %s"%e)

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
            tmps = self.driver.find_elements_by_xpath(".//*[@class='url_filter_tab']//span")
            tmps[n].click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'edit the n list button' element fail! The reason is %s"%e)

    def click_choice_n_list(self, n):
        """
        点击选择第几个list
        输入：n：第几个
        """
        try:
            tmps = self.driver.find_elements_by_xpath(".//*[@class='url_filter_tab']//input")
            tmps[n].click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'choice n list' element fail! The reason is %s"%e)

    ###########################################################################################
    ####################以下是添加URL过滤窗口中页面的操作##############################################
    def set_url_address(self, url):
        """
        设置URL地址
        输入：url关键字
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".urltext.url_agree")
            tmp.clear()
            tmp.send_keys(url)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'url address' element fail! The reason is %s"%e)

    def edit_url_address(self, url):
        """
        编辑URL地址
        输入：url关键字
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".urltext.url_agree_edit")
            tmp.clear()
            tmp.send_keys(url)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page edit 'url address' element fail! The reason is %s"%e)

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
            tmp = self.driver.find_element_by_css_selector(".close_url_filter_popup")
            tmp.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'close button' element fail! The reason is %s"%e)

    def click_close_edit_button(self):
        """
        点击编辑窗口的关闭按钮
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".close_url_filter_popup_edit")
            tmp.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'close edit button' element fail! The reason is %s"%e)