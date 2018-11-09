#coding=utf-8
#作者：曾祥卫
#时间：2018.09.17
#描述：用例层代码，调用login_business

import unittest,time
from selenium import webdriver
from login.login_business import LoginBusiness
from systemtools.configupdate.configupdate_business import ConfigUpdateBusiness
from connect.ssh import SSH
from data import data
from data.logfile import Log

data_basic = data.data_basic()
data_login = data.data_login()

log = Log("Login")

class TestLogin(unittest.TestCase):
    """测试登录的用例集(Duration:0.17h)"""
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.get(data_basic['DUT_web'])
        self.driver.implicitly_wait(20)


    def test_001_correct_user_pwd_login(self):
        """输入正确的管理员的用户名和密码，登录AP的web界面"""
        #首先启用无线网卡
        Lg = LoginBusiness(self.driver)
        Lg.wlan_enable(data_basic['wlan_pc'])
        #调用实例的登录AP的web界面
        Lg.login(data_basic['superUser'], data_basic['super_defalut_pwd'])
        #刷新页面重新登录ap页面
        Lg.refresh_login_ap()
        #把AP恢复出厂配置
        tmp1 = ConfigUpdateBusiness(self.driver)
        tmp1.restore_AP_factory()
        #重新登录AP
        #调用实例的登录AP的web界面
        Lg.login(data_basic['superUser'], data_basic['super_defalut_pwd'])
        #检测是否登录成功
        result = Lg.login_test()
        self.assertTrue(result)
        log.debug("001\t\tpass")

    def test_002_user_logout(self):
        """登录web页面后，点击登出按钮，能够登出成功"""
        Lg = LoginBusiness(self.driver)
        #首先登录
        time.sleep(20)
        Lg.login(data_basic['superUser'], data_basic['super_defalut_pwd'])
        #检测是否登录成功
        result1 = Lg.login_test()
        #登出AP的web界面
        Lg.logout()
        #检测是否登录成功
        result2 = Lg.login_test()
        self.assertTrue(result1)
        self.assertFalse(result2)
        log.debug("002\t\tpass")

    def test_003_wrong_user_pwd_login(self):
        """输入错误的管理员的用户名和密码，登录AP的web界面"""
        #逻辑类对象，建一个实例
        Lg = LoginBusiness(self.driver)
        #调用实例的登录AP的web界面
        Lg.login(data_basic['superUser'], data_login['digital_letter'])
        #检测是否登录成功
        result = Lg.login_test()
        self.assertFalse(result)
        log.debug("003\t\tpass")

    def test_004_wifi_login(self):
        """使用无线网卡连接ssid，输入正确的管理员的用户名和密码，登录AP的web界面"""
        #逻辑类对象，建一个实例
        Lg = LoginBusiness(self.driver)
        #复位AP后的默认ssid
        ssid = "3ONE_2G_"+ data.master_last_6mac()
        #使用无线网卡连接ssid
        Lg.connect_NONE_AP(ssid, data_basic['wlan_pc'])
        #无线网卡获取ip地址
        Lg.dhcp_wlan(data_basic['wlan_pc'])
        #PC禁用有线网卡
        Lg.networkcard_disable()
        #调用实例的登录AP的web界面
        Lg.login(data_basic['superUser'], data_basic['super_defalut_pwd'])
        #检测是否登录成功
        result = Lg.login_test()

        #启用有线网卡
        Lg.networkcard_enable()
        #释放无线网卡的ip
        Lg.dhcp_release_wlan(data_basic['wlan_pc'])
        #断开无线网卡的连接
        Lg.disconnect_ap()

        self.assertTrue(result)
        log.debug("004\t\tpass")

    def atest_005_webpage_timeout(self):
        """登录AP的web界面后，等待超时时间，确认ap退出登录"""
        #逻辑类对象，建一个实例
        Lg = LoginBusiness(self.driver)
        #调用实例的登录AP的web界面
        Lg.login(data_basic['superUser'], data_basic['super_defalut_pwd'])
        #等待一个超时时间
        time.sleep(600)
        #刷新web页面
        self.driver.refresh()
        self.driver.implicitly_wait(20)
        #检测是否登录成功
        result = Lg.login_test()
        self.assertFalse(result)
        log.debug("005\t\tpass")


    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
