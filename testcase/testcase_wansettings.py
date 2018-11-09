#coding=utf-8
#作者：曾祥卫
#时间：2018.09.26
#描述：用例层代码，调用wansettings_business

import unittest,time
from selenium import webdriver
from login.login_business import LoginBusiness
from network.wansettings.wansettings_business import WanSettingsBusiness
from systemtools.configupdate.configupdate_business import ConfigUpdateBusiness
from stateinfo.stateinfo_business import StateInfoBusiness
from connect.ssh import SSH
from data import data
from data.logfile import Log

data_basic = data.data_basic()
data_login = data.data_login()
data_wirless = data.data_wireless()
data_wan = data.data_wan()

log = Log("WanSettings")

class TestWanSettings(unittest.TestCase):
    """测试外网设置的用例集(Duration:0.14h)"""
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.get(data_basic['DUT_web'])
        self.driver.implicitly_wait(20)
        #逻辑类对象，建一个实例
        Lg = LoginBusiness(self.driver)
        #调用实例的登录AP的web界面
        Lg.login(data_basic['superUser'], data_basic['super_defalut_pwd'])
        #刷新页面重新登录ap页面
        Lg.refresh_login_ap()


    def test_001_set_wan_pppoe(self):
        """外网设置为pppoe，能否上网"""
        #首先启用无线网卡
        tmp = WanSettingsBusiness(self.driver)
        tmp.wlan_enable(data_basic['wlan_pc'])
        #刷新页面重新登录ap页面
        Lg = LoginBusiness(self.driver)
        Lg.refresh_login_ap()
        #把AP恢复出厂配置
        tmp1 = ConfigUpdateBusiness(self.driver)
        tmp1.restore_AP_factory()
        #重新登录AP
        #逻辑类对象，建一个实例
        Lg = LoginBusiness(self.driver)
        #调用实例的登录AP的web界面
        Lg.login(data_basic['superUser'], data_basic['super_defalut_pwd'])
        #刷新页面重新登录ap页面
        Lg.refresh_login_ap()
        #设置外网为pppoe
        tmp.change_wan_to_pppoe(data_wan['pppoe_user'],
            data_wan['pppoe_password'], data_wan['DNS'])
        time.sleep(30)
        #逻辑类对象，建一个实例
        Lg = LoginBusiness(self.driver)
        #刷新页面重新登录ap页面
        Lg.refresh_login_ap()
        #判断ap能够上网
        result4 = tmp.get_ping("www.baidu.com")
        tmp1 = StateInfoBusiness(self.driver)
        #获取当前模式
        result1 = tmp1.obtain_AP_current_mode()
        #获取外网的IP获取方式
        result2 = tmp1.obtain_WAN_IP_generation()
        #获取IP地址
        result3 = tmp1.obtain_WAN_IP_address()
        self.assertEqual(result1, "路由模式")
        self.assertEqual(result2, "PPPOE拨号")
        self.assertIn(data_wan['wan_str'], result3)
        self.assertEqual(0, result4)
        log.debug("001\t\tpass")

    def test_002_set_wan_staticIP(self):
        """外网设置为静态IP，能否上网"""
        tmp = WanSettingsBusiness(self.driver)
        #设置外网为staticIP
        tmp.change_wan_to_staticIP(data_wan['static_IP'],
            data_wan['netmask'], data_wan['gateway'], data_wan['DNS'])

        #判断ap能够上网
        time.sleep(30)
        #逻辑类对象，建一个实例
        Lg = LoginBusiness(self.driver)
        #刷新页面重新登录ap页面
        Lg.refresh_login_ap()
        tmp1 = StateInfoBusiness(self.driver)
        #获取当前模式
        result1 = tmp1.obtain_AP_current_mode()
        #获取外网的IP获取方式
        result2 = tmp1.obtain_WAN_IP_generation()
        #获取IP地址
        result3 = tmp1.obtain_WAN_IP_address()
        result4 = tmp.get_ping("www.baidu.com")
        self.assertEqual(result1, "路由模式")
        self.assertEqual(result2, "静态IP")
        self.assertEqual(data_wan['static_IP'], result3)
        self.assertEqual(0, result4)
        log.debug("002\t\tpass")

    def test_003_set_wan_dhcp(self):
        """外网设置为动态获取，能否上网"""
        tmp = WanSettingsBusiness(self.driver)
        #设置外网为动态获取
        tmp.change_wan_to_dhcp()
        time.sleep(30)
        #逻辑类对象，建一个实例
        Lg = LoginBusiness(self.driver)
        #刷新页面重新登录ap页面
        Lg.refresh_login_ap()
        tmp1 = StateInfoBusiness(self.driver)
        #获取当前模式
        result1 = tmp1.obtain_AP_current_mode()
        #获取外网的IP获取方式
        result2 = tmp1.obtain_WAN_IP_generation()
        #获取IP地址
        result3 = tmp1.obtain_WAN_IP_address()
        #判断ap能够上网
        result4 = tmp.get_ping("www.baidu.com")
        tmp.disconnect_ap()
        self.assertEqual(result1, "路由模式")
        self.assertEqual(result2, "动态获取")
        self.assertIn(data_wan['wan_str'], result3)
        self.assertEqual(0, result4)
        log.debug("003\t\tpass")



    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
