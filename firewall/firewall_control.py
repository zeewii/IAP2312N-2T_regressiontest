#coding=utf-8
#作者：曾祥卫
#时间：2018.10.26
#描述：防火墙的控制层


from publicControl.public_control import PublicControl
import time, os
dirname = os.path.dirname(os.getcwd())
png_PATH = os.path.join(dirname, "data", "testresultdata")

class FireWallControl(PublicControl):

    def __init__(self,driver):
        #继承PublicControl类的属性和方法
        PublicControl.__init__(self,driver)


    def menu_firewall(self):
        """
        点击防火墙菜单
        """
        try:
            #首先找IP过滤的元素
            element = self.driver.find_element_by_css_selector(".left_list_main.ip_filter.child_left_list.b.ip_filter_lang")
            #如果IP过滤的元素没有显示出来，则点击防火墙菜单，如果有显示出来，则不点击防火墙菜单
            if not element.is_displayed():
                self.driver.find_element_by_css_selector(".firewall_lang.span_lang").click()
                self.driver.implicitly_wait(10)
                time.sleep(2)
        except Exception as e:
            self.get_picture("menu_firewall")
            raise Exception("Web page click 'firewall menu' element fail! The reason is %s"%e)


