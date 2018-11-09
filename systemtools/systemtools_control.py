#coding=utf-8
#作者：曾祥卫
#时间：2018.09.21
#描述：系统工具的控制层


from publicControl.public_control import PublicControl
import time, os
dirname = os.path.dirname(os.path.dirname(__file__))
png_PATH = os.path.join(dirname, "data", "testresultdata")


class SystemToolsControl(PublicControl):

    def __init__(self,driver):
        #继承PublicControl类的属性和方法
        PublicControl.__init__(self,driver)


    def menu_systemtools(self):
        """
        点击系统工具设置菜单
        """
        try:
            #首先找用户设置的元素
            element = self.driver.find_element_by_css_selector(".left_list_main.User_settings.child_left_list.b.User_settings_lang")
            #如果用户设置的元素没有显示出来，则点击系统工具菜单，如果有显示出来，则不点击系统工具菜单
            if not element.is_displayed():
                self.driver.find_element_by_css_selector(".System_tools_lang.span_lang").click()
                self.driver.implicitly_wait(10)
                time.sleep(2)
        except Exception as e:
            self.get_picture("systemtools")
            raise Exception("Web page click 'systemtools menu' element fail! The reason is %s"%e)


