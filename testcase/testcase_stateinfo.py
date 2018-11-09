#coding=utf-8
#作者：曾祥卫
#时间：2018.10.10
#描述：用例层代码，调用stateinfo_business

import unittest,time
from selenium import webdriver
from login.login_business import LoginBusiness
from network.wirelesssettings.wirelesssettings_business import WirelessSettingsBusiness
from stateinfo.stateinfo_business import StateInfoBusiness
from systemtools.configupdate.configupdate_business import ConfigUpdateBusiness
from connect.ssh import SSH
from data import data
from data.logfile import Log

data_basic = data.data_basic()
data_login = data.data_login()
data_wirless = data.data_wireless()

log = Log("StateInfo")

class TestStateInfo(unittest.TestCase):
    """测试状态信息的用例集(Duration:0.28h)"""
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


    def test_001_check_wifi_upload(self):
        """判断WIFI总上行是否正确"""
        #首先启用无线网卡
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
        #判断WIFI总上行是否正确
        tmp = StateInfoBusiness(self.driver)
        result = tmp.check_wifi_upload(data_wirless['all_ssid'],
            data_wirless['short_wpa'], data_basic['wlan_pc'],
            data_basic['lan_pc'])
        self.assertTrue(result)
        log.debug("001\t\tpass")

    def test_002_check_wifi_download(self):
        """判断WIFI总下行是否正确"""
        #判断WIFI总上行是否正确
        tmp = StateInfoBusiness(self.driver)
        result = tmp.check_wifi_download(data_wirless['all_ssid'],
            data_wirless['short_wpa'], data_basic['wlan_pc'],
            data_basic['lan_pc'])
        self.assertTrue(result)
        log.debug("002\t\tpass")

    def test_003_check_AP_current_mode_routemode(self):
        """判断当前模式是否正确--路由模式"""
        tmp = StateInfoBusiness(self.driver)
        #获取当前模式
        result = tmp.obtain_AP_current_mode()
        self.assertEqual(result, "路由模式")
        log.debug("003\t\tpass")

    def test_004_check_AP_wireless_client(self):
        """判断无线用户数是否正确"""
        #判断无线用户数是否正确
        tmp = StateInfoBusiness(self.driver)
        result = tmp.check_AP_wireless_client(data_wirless['all_ssid'],
            data_basic['wlan_pc'], "wpa", data_wirless['short_wpa'])
        self.assertEqual(result, 1)
        log.debug("004\t\tpass")

    def test_005_check_AP_MAC_address(self):
        """判断AP的mac地址是否正确"""
        tmp = StateInfoBusiness(self.driver)
        #判断AP的mac地址是否正确
        result = tmp.check_AP_MAC_address(data_basic['DUT_ip'],
            data_basic['ssh_user'],data_basic['ssh_pwd'])
        self.assertTrue(result)
        log.debug("005\t\tpass")

    def test_006_check_AP_equipment_model(self):
        """判断设备型号是否正确"""
        tmp = StateInfoBusiness(self.driver)
        #获取设备型号
        result = tmp.obtain_AP_equipment_model()
        AP_model = "IAP2312N-2T"
        self.assertEqual(result, AP_model)
        log.debug("006\t\tpass")

    def test_007_check_AP_firmware_version(self):
        """判断固件版本是否正确"""
        tmp = StateInfoBusiness(self.driver)
        #获取固件版本
        result = tmp.obtain_AP_firmware_version()
        self.assertEqual(result, data_basic['new_version'])
        log.debug("007\t\tpass")

    def test_008_check_AP_24g_ssid(self):
        """判断2.4G的ssid是否正确"""
        tmp = StateInfoBusiness(self.driver)
        #获取2.4G的ssid
        result = tmp.obtain_AP_24g_ssid()
        tmp.disconnect_ap()
        self.assertEqual(result, data_wirless['all_ssid'])
        log.debug("008\t\tpass")






    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
