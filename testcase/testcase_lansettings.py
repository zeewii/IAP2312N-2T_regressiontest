#coding=utf-8
#作者：曾祥卫
#时间：2018.09.26
#描述：用例层代码，调用lansettings_business

import unittest,time
from selenium import webdriver
from login.login_business import LoginBusiness
from network.lansettings.lansettings_business import LanSettingsBusiness
from systemtools.configupdate.configupdate_business import ConfigUpdateBusiness
from connect.ssh import SSH
from data import data
from data.logfile import Log

data_basic = data.data_basic()
data_login = data.data_login()
data_wirless = data.data_wireless()
data_lan = data.data_lan()

log = Log("LanSettings")

class TestLanSettings(unittest.TestCase):
    """测试内网设置的用例集(Duration:0.52h)"""
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


    def test_001_disable_dhcp_server(self):
        """禁用dhcp server，client无法获取到ip地址"""
        #首先启用无线网卡
        tmp = LanSettingsBusiness(self.driver)
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
        #关闭ap的dhcp server
        tmp.enable_disable_dhcp_server(0)
        result = tmp.check_AP_dhcp_server(data_basic['lan_pc'], "192.168.1")
        #指定有线网卡的固定ip--能够访问ap的webpage
        tmp.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])
        self.assertFalse(result)
        log.debug("001\t\tpass")

    def test_002_client_staticIP_when_disable_dhcp_server(self):
        """禁用dhcp server，client指定静态ip地址，确认client能够上网"""
        tmp = LanSettingsBusiness(self.driver)
        #指定PC接口的ip，掩码，网关，判断client能够上网
        result = tmp.check_access_internet_after_change_client_ip_netmask_gw(
            data_basic['PC_pwd'], data_basic['lan_pc'], data_basic['PC_ip'],
            data_lan['netmask1'], data_basic['DUT_ip'])
        #指定有线网卡的固定ip--能够访问ap的webpage
        tmp.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])
        #刷新页面重新登录ap页面
        Lg = LoginBusiness(self.driver)
        Lg.refresh_login_ap()
        #开启ap的dhcp server
        tmp.enable_disable_dhcp_server(1)
        #client重新获取ip
        tmp.dhcp_release_wlan(data_basic['lan_pc'])
        tmp.dhcp_wlan(data_basic['lan_pc'])
        self.assertEqual(0, result)
        log.debug("002\t\tpass")

    def test_003_change_ap_ip(self):
        """启用AP的dhcp server，改变AP的ip,确认client能得到ip，并且能够上网"""
        tmp = LanSettingsBusiness(self.driver)
        #改变AP的ip
        tmp.change_AP_ip_netmask(data_lan['ap_test_IP1'], data_lan['netmask1'])
        #client重新获取ip
        tmp.dhcp_release_wlan(data_basic['lan_pc'])
        tmp.dhcp_wlan(data_basic['lan_pc'])
        result = tmp.get_localIp(data_basic['lan_pc'])
        #刷新页面重新登录ap页面
        Lg = LoginBusiness(self.driver)
        Lg.refresh_login_ap()
        #用AP改回默认ip
        tmp.change_AP_ip_netmask(data_basic['DUT_ip'], data_lan['netmask1'])
        #client重新获取ip
        tmp.dhcp_release_wlan(data_basic['lan_pc'])
        tmp.dhcp_wlan(data_basic['lan_pc'])
        str = data_lan['ap_test_IP1'].split(".")
        #ip的前三段和client所获IP的前三段一样
        self.assertIn(str[0], result)
        self.assertIn(str[1], result)
        self.assertIn(str[2], result)
        log.debug("003\t\tpass")

    def test_004_set_AP_A_Class(self):
        """设置AP的内网IP为A类地址和A类子网掩码"""
        tmp = LanSettingsBusiness(self.driver)
        #改变AP的ip
        tmp.change_AP_ip_netmask(data_lan['ap_test_IP3'], data_lan['netmask3'])
        #client重新获取ip
        tmp.dhcp_release_wlan(data_basic['lan_pc'])
        tmp.dhcp_wlan(data_basic['lan_pc'])
        result = tmp.get_localIp(data_basic['lan_pc'])
        #刷新页面重新登录ap页面
        Lg = LoginBusiness(self.driver)
        Lg.refresh_login_ap()
        #用AP改回默认ip
        tmp.change_AP_ip_netmask(data_basic['DUT_ip'], data_lan['netmask1'])
        #client重新获取ip
        tmp.dhcp_release_wlan(data_basic['lan_pc'])
        tmp.dhcp_wlan(data_basic['lan_pc'])
        str = data_lan['ap_test_IP3'].split(".")
        #ip的第一段和client所获IP的第一段一样
        self.assertIn(str[0], result)
        log.debug("004\t\tpass")

    def test_005_set_AP_B_Class(self):
        """设置AP的内网IP为B类地址和B类子网掩码"""
        tmp = LanSettingsBusiness(self.driver)
        #改变AP的ip
        tmp.change_AP_ip_netmask(data_lan['ap_test_IP2'], data_lan['netmask2'])
        #client重新获取ip
        tmp.dhcp_release_wlan(data_basic['lan_pc'])
        tmp.dhcp_wlan(data_basic['lan_pc'])
        result = tmp.get_localIp(data_basic['lan_pc'])
        #刷新页面重新登录ap页面
        Lg = LoginBusiness(self.driver)
        Lg.refresh_login_ap()
        #用AP改回默认ip
        tmp.change_AP_ip_netmask(data_basic['DUT_ip'], data_lan['netmask1'])
        #client重新获取ip
        tmp.dhcp_release_wlan(data_basic['lan_pc'])
        tmp.dhcp_wlan(data_basic['lan_pc'])
        str = data_lan['ap_test_IP2'].split(".")
        #ip的前两段和client所获IP的前两段一样
        self.assertIn(str[0], result)
        self.assertIn(str[1], result)
        log.debug("005\t\tpass")

    def test_006_set_AP_custom_netmask1(self):
        """设置AP的内网子网掩码为255.255.255.128"""
        tmp = LanSettingsBusiness(self.driver)
        #改变AP的ip
        tmp.change_AP_ip_netmask(data_basic['DUT_ip'], data_lan['custom_netmask1'])
        #client重新获取ip
        tmp.dhcp_release_wlan(data_basic['lan_pc'])
        tmp.dhcp_wlan(data_basic['lan_pc'])
        result = tmp.get_localIp(data_basic['lan_pc'])
        str = data_basic['DUT_ip'].split(".")
        #ip的前三段和client所获IP的前三段一样
        self.assertIn(str[0], result)
        self.assertIn(str[1], result)
        self.assertIn(str[2], result)
        log.debug("006\t\tpass")

    def test_007_set_AP_custom_netmask2(self):
        """设置AP的内网子网掩码为255.255.128.0"""
        tmp = LanSettingsBusiness(self.driver)
        #改变AP的ip
        tmp.change_AP_ip_netmask(data_basic['DUT_ip'], data_lan['custom_netmask2'])
        #client重新获取ip
        tmp.dhcp_release_wlan(data_basic['lan_pc'])
        tmp.dhcp_wlan(data_basic['lan_pc'])
        result = tmp.get_localIp(data_basic['lan_pc'])
        str = data_basic['DUT_ip'].split(".")
        #ip的前两段和client所获IP的前两段一样
        self.assertIn(str[0], result)
        self.assertIn(str[1], result)
        log.debug("007\t\tpass")

    def test_008_set_AP_custom_netmask3(self):
        """设置AP的内网子网掩码为255.128.0.0"""
        tmp = LanSettingsBusiness(self.driver)
        #改变AP的ip
        tmp.change_AP_ip_netmask(data_basic['DUT_ip'], data_lan['custom_netmask3'])
        #client重新获取ip
        tmp.dhcp_release_wlan(data_basic['lan_pc'])
        tmp.dhcp_wlan(data_basic['lan_pc'])
        result = tmp.get_localIp(data_basic['lan_pc'])
        #用AP改回默认的子网掩码
        tmp.change_AP_ip_netmask(data_basic['DUT_ip'], data_lan['netmask1'])
        #client重新获取ip
        tmp.dhcp_release_wlan(data_basic['lan_pc'])
        tmp.dhcp_wlan(data_basic['lan_pc'])
        str = data_basic['DUT_ip'].split(".")
        tmp.disconnect_ap()
        #ip的前一段和client所获IP的前一段一样
        self.assertIn(str[0], result)
        log.debug("008\t\tpass")




    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
