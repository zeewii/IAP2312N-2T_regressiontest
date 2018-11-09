#coding=utf-8
#作者：曾祥卫
#时间：2018.09.20
#描述：网络设置的控制层


from publicControl.public_control import PublicControl
import time, os
dirname = os.path.dirname(os.path.dirname(__file__))
png_PATH = os.path.join(dirname, "data", "testresultdata")

class NetWorkControl(PublicControl):

    def __init__(self,driver):
        #继承PublicControl类的属性和方法
        PublicControl.__init__(self,driver)


    def menu_network(self):
        """
        点击网络设置菜单
        """
        try:
            #首先找内网设置的元素
            element = self.driver.find_element_by_css_selector(".left_list_main.Intranet.child_left_list.b.Intranet_lang")
            #如果内网设置的元素没有显示出来，则点击网络设置菜单，如果有显示出来，则不点击网络设置菜单
            if not element.is_displayed():
                self.driver.find_element_by_css_selector(".net_lang.span_lang").click()
                self.driver.implicitly_wait(10)
                time.sleep(2)
        except Exception as e:
            self.get_picture("menu_network")
            raise Exception("Web page click 'network menu' element fail! The reason is %s"%e)


