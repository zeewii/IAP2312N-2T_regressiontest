#coding=utf-8
#作者：曾祥卫
#时间：2018.10.09
#描述：用例层代码，调用wirelessclient_business

import unittest,time
from selenium import webdriver
from login.login_business import LoginBusiness
from network.wirelesssettings.wirelesssettings_business import WirelessSettingsBusiness
from wirelessclient.wirelessclient_business import WirelessClientBusiness
from systemtools.configupdate.configupdate_business import ConfigUpdateBusiness
from connect.ssh import SSH
from data import data
from data.logfile import Log

data_basic = data.data_basic()
data_login = data.data_login()
data_wirless = data.data_wireless()

log = Log("WirelessClient")

class TestWirelessClient(unittest.TestCase):
    """测试无线用户的用例集(Duration:0.50h)"""
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


    def test_001_check_current_devices_client_mac(self):
        """无线client显示在当前连接设备页面"""
        # #首先启用无线网卡
        tmp2 = WirelessSettingsBusiness(self.driver)
        tmp2.wlan_enable(data_basic['wlan_pc'])
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
        #修改无线的ssid,加密方式和密码
        tmp2.change_wifi_ssid_encryption_pwd(data_wirless['all_ssid'],
            "psk2", data_wirless['short_wpa'])
        #使用无线网卡连接ap
        tmp2.client_connect_ssid(data_wirless['all_ssid'], data_basic['wlan_pc'],
            "wpa", data_wirless['short_wpa'])
        # tmp2.connect_DHCP_WPA_AP(data_wirless['all_ssid'], data_wirless['short_wpa'],
        #     data_basic['wlan_pc'])
        #判断设备的mac地址是否正确
        Lg.refresh_login_ap()
        time.sleep(60)
        tmp = WirelessClientBusiness(self.driver)
        result = tmp.check_current_devices_client_mac(data_basic['wlan_pc'])
        self.assertTrue(result)
        log.debug("001\t\tpass")

    def test_002_check_undecided_list_client_mac(self):
        """无线client显示在待定名单中"""
        tmp = WirelessClientBusiness(self.driver)
        #将当前连接设备页面的mac地址加入到待定名单
        tmp.join_client_mac_to_undecided_list(0)
        #判断待定名单的设备的mac地址是否正确
        result = tmp.check_undecided_list_client_mac(data_basic['wlan_pc'])
        self.assertTrue(result)
        log.debug("002\t\tpass")

    def test_003_check_blacklist_function1(self):
        """验证黑名单功能1"""
        tmp = WirelessClientBusiness(self.driver)
        #将待定名单改为黑名单
        tmp.change_to_black()
        #验证无线网卡不能连接上ap了
        result = tmp.connect_WPA_AP_backup(data_wirless['all_ssid'],
            data_wirless['short_wpa'], data_basic['wlan_pc'])
        self.assertIn("Not connected", result)
        log.debug("003\t\tpass")

    def test_004_check_blacklist_function2(self):
        """验证黑名单功能2"""
        tmp = WirelessClientBusiness(self.driver)
        #修改黑名单的第1条的mac地址为随机mac地址
        random_mac = tmp.randomMAC()
        tmp.change_black_mac(0, random_mac)
        #验证无线网卡能够连接上ap了
        result = tmp.connect_WPA_AP(data_wirless['all_ssid'],
            data_wirless['short_wpa'], data_basic['wlan_pc'])
        self.assertIn(data_wirless['all_ssid'], result)
        log.debug("004\t\tpass")

    def test_005_check_whitelist_function1(self):
        """验证白名单功能1"""
        tmp = WirelessClientBusiness(self.driver)
        #将黑名单改为白名单
        tmp.change_to_white()
        #验证无线网卡不能连接上ap了
        result = tmp.connect_WPA_AP_backup(data_wirless['all_ssid'],
            data_wirless['short_wpa'], data_basic['wlan_pc'])
        self.assertIn("Not connected", result)
        log.debug("005\t\tpass")

    def test_006_check_whitelist_function2(self):
        """验证白名单功能2"""
        tmp = WirelessClientBusiness(self.driver)
        #修改白名单的第1条的mac地址为无线网卡的mac
        client_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        tmp.change_white_mac(0, client_mac)
        #验证无线网卡能够连接上ap了
        result = tmp.connect_WPA_AP(data_wirless['all_ssid'],
            data_wirless['short_wpa'], data_basic['wlan_pc'])
        self.assertIn(data_wirless['all_ssid'], result)
        log.debug("006\t\tpass")

    def test_007_check_many_whitelists_function1(self):
        """验证多条白名单列表时白名单功能1"""
        tmp = WirelessClientBusiness(self.driver)
        #添加10条白名单
        tmp.add_many_lists(10)
        #验证当无线网卡mac在白名单的list中，能够连接上ap
        result = tmp.connect_WPA_AP(data_wirless['all_ssid'],
            data_wirless['short_wpa'], data_basic['wlan_pc'])
        #删除所有的list
        tmp.del_all_lists()
        self.assertIn(data_wirless['all_ssid'], result)
        log.debug("007\t\tpass")

    def test_008_check_many_whitelists_function2(self):
        """验证多条白名单列表时白名单功能2"""
        tmp = WirelessClientBusiness(self.driver)
        #添加10条白名单
        tmp.add_many_lists(10)
        #验证当无线网卡mac不在白名单的list中，不能够连接上ap
        result = tmp.connect_WPA_AP_backup(data_wirless['all_ssid'],
            data_wirless['short_wpa'], data_basic['wlan_pc'])
        self.assertIn("Not connected", result)
        log.debug("008\t\tpass")

    def test_009_check_many_blacklists_function1(self):
        """验证多条黑名单列表时黑名单功能1"""
        tmp = WirelessClientBusiness(self.driver)
        #将名单改为黑名单
        tmp.change_to_black()
        time.sleep(30)
        #验证当无线网卡mac不在黑名单的list中，能够连接上ap
        result = tmp.connect_WPA_AP(data_wirless['all_ssid'],
            data_wirless['short_wpa'], data_basic['wlan_pc'])
        self.assertIn(data_wirless['all_ssid'], result)
        log.debug("009\t\tpass")

    def test_010_check_many_blacklists_function2(self):
        """验证多条黑名单列表时黑名单功能2"""
        tmp = WirelessClientBusiness(self.driver)
        #修改黑名单的第0条的mac地址为无线网卡的mac地址
        client_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        tmp.change_black_mac(0, client_mac)
        #验证当无线网卡mac在黑名单的list中，不能够连接上ap
        result = tmp.connect_WPA_AP_backup(data_wirless['all_ssid'],
            data_wirless['short_wpa'], data_basic['wlan_pc'])
        self.assertIn("Not connected", result)
        log.debug("010\t\tpass")

    def test_011_check_change_black_to_undecided(self):
        """验证黑名单切换到待定名单时list里面的mac地址过滤无效"""
        tmp = WirelessClientBusiness(self.driver)
        #将名单改为待定名单
        tmp.change_to_undecided()
        time.sleep(30)
        #验证当无线网卡mac在待定名单的list中，能够连接上ap
        result = tmp.connect_WPA_AP(data_wirless['all_ssid'],
            data_wirless['short_wpa'], data_basic['wlan_pc'])
        self.assertIn(data_wirless['all_ssid'], result)
        log.debug("011\t\tpass")

    def test_012_check_change_white_to_undecided(self):
        """验证白名单切换到待定名单时list里面的mac地址过滤无效"""
        tmp = WirelessClientBusiness(self.driver)
        #切换名单为白名单
        tmp.change_to_white()
        #修改白名单的第1条的mac地址为随机mac
        random_mac = tmp.randomMAC()
        tmp.change_white_mac(0, random_mac)
        #切换白名单为待定名单
        tmp.change_to_undecided()
        time.sleep(60)
        #验证当无线网卡mac不在待定名单的list中，能够连接上ap
        result = tmp.connect_WPA_AP(data_wirless['all_ssid'],
            data_wirless['short_wpa'], data_basic['wlan_pc'])
        tmp.disconnect_ap()
        self.assertIn(data_wirless['all_ssid'], result)
        log.debug("012\t\tpass")




    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
