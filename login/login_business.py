#coding=utf-8
#作者：曾祥卫
#时间：2018.09.17
#描述：AP登录的业务层,包含所有的测试步骤


from login.login_control import LoginControl
from data import data
import time, os

dirname = os.path.dirname(os.path.dirname(__file__))
png_PATH = os.path.join(dirname, "data", "testresultdata")

data_basic = data.data_basic()
data_login = data.data_login()

class LoginBusiness(LoginControl):

    def __init__(self,driver):
        #继承LoginControl类的属性和方法
        LoginControl.__init__(self,driver)

    #登录AP的web界面
    def login(self,username,pwd):
        """
        登录AP的web界面
        """
        current_time = time.strftime('%m-%d %H:%M',time.localtime(time.time()))
        print("The current time of running this case is %s"%current_time)
        #通过控制层对象LoginControl建一个实例,并指定该实例的属性：username,password
        Lg = LoginControl(self.driver,username,pwd)
        #输入用户名
        Lg.set_username()
        #输入密码
        Lg.set_pwd()
        #点击登录
        Lg.submit()
        print("Input username:%s and password:%s,click submit!"%(username,pwd))

    #登出AP的web界面
    def logout(self):
        #点击导航条上的退出
        self.click_Navbar_logout()
        time.sleep(2)


    #登录后判断登录后的“概览”的页面元素，如果有返回True，如果没有返回False,来检测是否登录成功
    def login_test(self):
        """
        登录后判断登录后的“概览”的页面元素，如果有返回True，如果没有返回False,来检测是否登录成功
        """
        try:
            time.sleep(2)
            self.driver.find_element_by_css_selector(".status_info_lang.span_lang")
            print("login AP successfully!")
            return True
        except Exception:
            print("login AP failed!")
            return False


    #判断登录页面是否有用户名的元素
    def loginweb_test(self):
        """
        判断登录页面是否有用户名的元素
        """
        try:
            time.sleep(10)
            self.driver.find_element_by_class_name("uname")
            print("login web have username!")
            return True
        except Exception:
            print("login web haven't username!")
            return False

    #刷新页面重新登录ap页面
    def refresh_login_ap(self):
        """
        刷新页面重新登录ap页面
        """
        try:
            #一直刷新登录AP，重复10次
            for i in range(10):
                self.driver.refresh()
                self.driver.implicitly_wait(60)
                Lg = LoginBusiness(self.driver)
                #如果登录AP成功，退出循环
                if Lg.login_test():
                    break
                else:
                    time.sleep(5)
                    Lg.login(data_basic['superUser'],data_basic['super_defalut_pwd'])
                    print("login AP again at {} time!".format(i+1))
        except Exception as e:
            self.get_picture("refresh_login_ap")
            raise Exception("Login page get 'username' element is error! The reason is %s"%e)

    #刷新页面重新登录ap页面
    def refresh_login_ap_bak(self):
        """
        刷新页面重新登录ap页面
        """
        try:
            self.driver.refresh()
            self.driver.implicitly_wait(60)
            #登录AP
            Lg = LoginBusiness(self.driver)
            if Lg.login_test() == False:
                Lg.login(data_basic['superUser'],data_basic['super_defalut_pwd'])
                print("login AP successfully again!")
        except Exception as e:
            self.get_picture("refresh_login_ap")
            raise Exception("Login page get 'username' element is error! The reason is %s"%e)