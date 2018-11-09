#coding=utf-8
#作者：曾祥卫
#时间：2018.11.2
#描述：用例层代码，调用macfilter_business

import unittest,time
from selenium import webdriver
from login.login_business import LoginBusiness
from firewall.macfilter.macfilter_business import MacFilterBusiness
from systemtools.configupdate.configupdate_business import ConfigUpdateBusiness
from workmode.workmode_business import WorkModeBusiness
from data import data
from data.logfile import Log

data_basic = data.data_basic()
data_login = data.data_login()
data_wirless = data.data_wireless()
data_lan = data.data_lan()
data_wan = data.data_wan()

log = Log("MACFilter")

class TestMACFilter(unittest.TestCase):
    """测试MAC过滤的用例集(Duration:0.27h)"""
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


    def test_001_check_add_one_list(self):
        """添加一条MAC过滤规则,为PC的mac地址,PC不能访问internet"""
        #首先启用无线网卡
        tmp = MacFilterBusiness(self.driver)
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
        #修改工作模式为路由模式,外网设置static IP模式
        tmp1 = WorkModeBusiness(self.driver)
        tmp1.change_workmode_to_route_WANstaticIP(data_wan['static_IP'],
            data_wan['netmask'], data_wan['gateway'], data_wan['DNS'],
            data_wirless['all_ssid'],"psk2", data_wirless['short_wpa'], "HT20", "auto")
        time.sleep(60)
        #逻辑类对象，建一个实例
        Lg = LoginBusiness(self.driver)
        #刷新页面重新登录ap页面
        Lg.refresh_login_ap()

        #先确定PC能够上网
        result1 = tmp.get_ping("www.baidu.com")
        #添加一条MAC过滤规则
        lan_mac = tmp.get_localmac()
        tmp.add_one_list(lan_mac)
        #判断PC是否能够上网
        result2 = tmp.get_ping("www.baidu.com")
        self.assertEqual(result1, 0)
        self.assertNotEqual(result2, 0)
        log.debug("001\t\tpass")

    def test_002_check_delete_one_list(self):
        """删除一条,PC的mac在的过滤规则,PC能够访问internet"""
        tmp = MacFilterBusiness(self.driver)
        #删除第1条mac过滤的规则list
        tmp.delete_n_list(0)
        #判断PC是否能够上网
        result = tmp.get_ping("www.baidu.com")
        self.assertEqual(result, 0)
        log.debug("002\t\tpass")

    def test_003_check_add_one_list_not_PCMac(self):
        """添加一条mac过滤规则,不是PC的mac地址,PC能够访问internet"""
        tmp = MacFilterBusiness(self.driver)
        #获取随机mac
        random_mac = tmp.randomMAC()
        #添加一条MAC过滤规则
        tmp.add_one_list(random_mac)
        #判断PC是否能够上网
        result = tmp.get_ping("www.baidu.com")
        self.assertEqual(result, 0)
        log.debug("003\t\tpass")

    def test_004_check_delete_one_list_not_PCMac(self):
        """删除一条mac过滤规则,不是PC的mac地址,PC能够访问internet"""
        tmp = MacFilterBusiness(self.driver)
        #删除第1条mac过滤的规则list
        tmp.delete_n_list(0)
        #判断PC是否能够上网
        result = tmp.get_ping("www.baidu.com")
        self.assertEqual(result, 0)
        log.debug("004\t\tpass")

    def test_005_check_add_one_list_is_wifi_client_mac(self):
        """添加一条无线客户端的mac过滤规则,无线客户端不能够访问internet"""
        tmp = MacFilterBusiness(self.driver)
        #获取无线网卡的mac地址
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        #添加一条MAC过滤规则
        tmp.add_one_list(wlan_mac)
        #判断无线客户端是否能够访问internet
        result = tmp.check_wifi_client_access_internet(data_wirless['all_ssid'],
            data_basic['wlan_pc'],"wpa", data_wirless['short_wpa'])
        self.assertNotEqual(result, 0)
        log.debug("005\t\tpass")

    def test_006_check_delete_one_list_is_wifi_client_mac(self):
        """删除一条无线客户端的mac过滤规则,,PC能够访问internet"""
        tmp = MacFilterBusiness(self.driver)
        #删除第1条mac过滤的规则list
        tmp.delete_n_list(0)
         #判断无线客户端是否能够访问internet
        result = tmp.check_wifi_client_access_internet(data_wirless['all_ssid'],
            data_basic['wlan_pc'],"wpa", data_wirless['short_wpa'])
        self.assertEqual(result, 0)
        log.debug("006\t\tpass")

    def test_007_check_10_list_PC_mac_in_list(self):
        """添加10条mac过滤规则,PC的mac在范围之内,PC不能够访问internet"""
        tmp = MacFilterBusiness(self.driver)
        #添加一条MAC过滤规则
        lan_mac = tmp.get_localmac()
        tmp.add_one_list(lan_mac)
        #添加10条规则，mac地址为随机mac地址
        tmp.add_10_list()
        #判断PC是否能够上网
        result = tmp.get_ping("www.baidu.com")
        self.assertNotEqual(result, 0)
        log.debug("007\t\tpass")

    def test_008_check_10_list_PC_mac_out_list(self):
        """添加10条mac过滤规则,PC的mac不在范围之内,PC能够访问internet"""
        tmp = MacFilterBusiness(self.driver)
        #删除第一条list
        tmp.delete_n_list(0)
        #判断PC是否能够上网
        result = tmp.get_ping("www.baidu.com")
        #删除所有的ip过滤的规则list
        tmp.delete_all_list()
        tmp.disconnect_ap()
        self.assertEqual(result, 0)
        log.debug("008\t\tpass")



    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
