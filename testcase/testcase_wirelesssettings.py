#coding=utf-8
#作者：曾祥卫
#时间：2018.09.26
#描述：用例层代码，调用wirelesssettings_business

import unittest,time
from selenium import webdriver
from login.login_business import LoginBusiness
from network.wirelesssettings.wirelesssettings_business import WirelessSettingsBusiness
from network.wansettings.wansettings_business import WanSettingsBusiness
from systemtools.configupdate.configupdate_business import ConfigUpdateBusiness
from connect.ssh import SSH
from data import data
from data.logfile import Log

data_basic = data.data_basic()
data_login = data.data_login()
data_wireless = data.data_wireless()

log = Log("WirelessSettings")

class TestWirelessSettings(unittest.TestCase):
    """测试无线设置的用例集(Duration:1.42h)"""
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


    def test_001_default_wifi(self):
        """默认无线开关为开启状态"""
        # #首先启用无线网卡
        tmp = WirelessSettingsBusiness(self.driver)
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

        #使用无线网卡扫描，能够连接上默认ssid
        #默认ssid
        default_ssid = "3ONE_2G_"+ data.master_last_6mac()
        print(default_ssid)
        result = tmp.client_connect_ssid(default_ssid, data_basic['wlan_pc'], "open")
        #result = tmp.ssid_scan_result_backup(default_ssid, data_basic['wlan_pc'])
        self.assertTrue(result)
        log.debug("001\t\tpass")

    def test_002_disable_wifi(self):
        """关闭无线，无线网卡扫描不到ssid"""
        #关闭无线
        tmp = WirelessSettingsBusiness(self.driver)
        tmp.change_wifi_switch()
        #使用无线网卡扫描，不能扫描到ssid
        #默认ssid
        default_ssid = "3ONE_2G_"+ data.master_last_6mac()
        result = tmp.ssid_scan_result(default_ssid, data_basic['wlan_pc'])
        self.assertFalse(result)
        log.debug("002\t\tpass")

    def test_003_enable_wifi(self):
        """开启无线，无线网卡能够扫描到ssid"""
        #开启无线
        tmp = WirelessSettingsBusiness(self.driver)
        tmp.change_wifi_switch()
        #使用无线网卡扫描，能够连接上默认ssid
        #默认ssid
        default_ssid = "3ONE_2G_"+ data.master_last_6mac()
        result = tmp.client_connect_ssid(default_ssid, data_basic['wlan_pc'], "open")
        self.assertTrue(result)
        log.debug("003\t\tpass")

    def test_004_hidden_ssid(self):
        """隐藏ssid，无线网卡不能扫描到，但能够连接上"""
        #隐藏ssid
        tmp = WirelessSettingsBusiness(self.driver)
        tmp.change_hidden_ssid()
        #默认ssid
        default_ssid = "3ONE_2G_"+ data.master_last_6mac()
        #无线网卡不能扫描到
        result1 = tmp.ssid_scan_result(default_ssid, data_basic['wlan_pc'])
        #无线能够能够连接隐藏ssid成功
        result2 = tmp.connect_NONE_hiddenssid_AP(default_ssid, data_basic['wlan_pc'])
        self.assertFalse(result1)
        self.assertIn(default_ssid, result2)
        log.debug("004\t\tpass")

    def test_005_cancel_hidden_ssid(self):
        """取消隐藏ssid，无线网卡能够扫描到，也能连接上"""
        #取消隐藏ssid
        tmp = WirelessSettingsBusiness(self.driver)
        tmp.change_hidden_ssid()
        #默认ssid
        default_ssid = "3ONE_2G_"+ data.master_last_6mac()
        #无线网卡能够扫描到
        #result1 = tmp.ssid_scan_result(default_ssid, data_basic['wlan_pc'])
        #无线能够能够连接ssid成功
        result2 = tmp.client_connect_ssid(default_ssid, data_basic['wlan_pc'], "open")
        #self.assertTrue(result1)
        self.assertIn(default_ssid, result2)
        log.debug("005\t\tpass")

    def test_006_change_ssid(self):
        """修改ssid，无线网卡能够扫描到新的ssid，也能连接上。默认ssid无法扫描到"""
        tmp = WirelessSettingsBusiness(self.driver)
        #修改ssid
        tmp.change_ssid(data_wireless['all_ssid'])
        #无线网卡能够扫描到
        #result1 = tmp.ssid_scan_result(data_wireless['all_ssid'], data_basic['wlan_pc'])
        #无线能够能够连接ssid成功
        result2 = tmp.client_connect_ssid(data_wireless['all_ssid'], data_basic['wlan_pc'],
            "open")
        #无线网卡不能扫描到默认的ssid
        #默认ssid
        default_ssid = "3ONE_2G_"+ data.master_last_6mac()
        result3 = tmp.ssid_scan_result(default_ssid, data_basic['wlan_pc'])
        #self.assertTrue(result1)
        self.assertIn(data_wireless['all_ssid'], result2)
        self.assertFalse(result3)
        log.debug("006\t\tpass")

    def test_007_check_ssid_letter(self):
        """SSID对英文的支持"""
        tmp = WirelessSettingsBusiness(self.driver)
        #修改无线的ssid,加密方式和密码
        tmp.change_wifi_ssid_encryption_pwd(data_wireless['letter_ssid'],
            "psk2", data_wireless['short_wpa'])
        #无线能够能够连接ssid成功
        result = tmp.client_connect_ssid(data_wireless['letter_ssid'], data_basic['wlan_pc'],
            "wpa", data_wireless['short_wpa'])
        self.assertIn(data_wireless['letter_ssid'], result)
        log.debug("007\t\tpass")

    def test_008_check_ssid_digital(self):
        """SSID对数字的支持"""
        tmp = WirelessSettingsBusiness(self.driver)
        #修改无线的ssid
        tmp.change_ssid(data_wireless['digital_ssid'])
        #无线能够能够连接ssid成功
        result = tmp.client_connect_ssid(data_wireless['digital_ssid'], data_basic['wlan_pc'],
            "wpa", data_wireless['short_wpa'])
        self.assertIn(data_wireless['digital_ssid'], result)
        log.debug("008\t\tpass")

    def test_009_check_ssid_letter_digital(self):
        """SSID对英文+数字的支持"""
        tmp = WirelessSettingsBusiness(self.driver)
        #修改无线的ssid
        tmp.change_ssid(data_wireless['digital_letter_ssid'])
        #无线能够能够连接ssid成功
        result = tmp.client_connect_ssid(data_wireless['digital_letter_ssid'], data_basic['wlan_pc'],
            "wpa", data_wireless['short_wpa'])
        self.assertIn(data_wireless['digital_letter_ssid'], result)
        log.debug("009\t\tpass")

    def test_010_check_ssid_ASCII(self):
        """SSID对ASCII的支持"""
        tmp = WirelessSettingsBusiness(self.driver)
        #修改无线的ssid
        tmp.change_ssid(data_wireless['ascii_ssid'])
        #获取页面上的ssid
        result = tmp.obtain_ssid()
        self.assertEqual(data_wireless['ascii_ssid'], result)
        log.debug("010\t\tpass")

    def test_011_check_ssid_CN(self):
        """中文SSID的正常配置"""
        tmp = WirelessSettingsBusiness(self.driver)
        #修改无线的ssid
        tmp.change_ssid(data_wireless['CN_ssid'])
        #获取页面上的ssid
        result = tmp.obtain_ssid()
        self.assertEqual(data_wireless['CN_ssid'], result)
        log.debug("011\t\tpass")

    def test_012_check_ssid_special(self):
        """特殊符号的SSID配置"""
        tmp = WirelessSettingsBusiness(self.driver)
        #修改无线的ssid
        tmp.change_ssid(data_wireless['special_ssid'])
        #获取页面上的ssid
        result = tmp.obtain_ssid()
        self.assertEqual(data_wireless['special_ssid'], result)
        log.debug("012\t\tpass")

    def test_013_check_ssid_min(self):
        """验证SSID的字符长度限制-最小"""
        tmp = WirelessSettingsBusiness(self.driver)
        #修改无线的ssid
        tmp.change_ssid(data_wireless['short_ssid'])
        #无线能够能够连接ssid成功
        result = tmp.client_connect_ssid(data_wireless['short_ssid'], data_basic['wlan_pc'],
            "wpa", data_wireless['short_wpa'])
        self.assertIn(data_wireless['short_ssid'], result)
        log.debug("013\t\tpass")

    def test_014_check_ssid_max(self):
        """验证SSID的字符长度限制-最大"""
        tmp = WirelessSettingsBusiness(self.driver)
        #修改无线的ssid
        tmp.change_ssid(data_wireless['long_ssid'])
        #无线能够能够连接ssid成功
        result = tmp.client_connect_ssid(data_wireless['long_ssid'], data_basic['wlan_pc'],
            "wpa", data_wireless['short_wpa'])
        self.assertIn(data_wireless['long_ssid'], result)
        log.debug("014\t\tpass")

    def test_015_check_ssid_more_max(self):
        """验证SSID的字符长度限制-超过最大"""
        tmp = WirelessSettingsBusiness(self.driver)
        #判断ssid输入框是否有红色警告
        result = tmp.check_ssid_warning(data_wireless['long_ssid']+"abc")
        self.assertTrue(result)
        log.debug("015\t\tpass")

    def test_016_check_ssid_blank(self):
        """验证SSID中有空格"""
        tmp = WirelessSettingsBusiness(self.driver)
        #修改无线的ssid
        ssid = data_wireless['letter_ssid']+" "+data_wireless['digital_ssid']
        tmp.change_ssid(ssid)
        #无线能够能够连接ssid成功
        result = tmp.client_connect_ssid(ssid, data_basic['wlan_pc'],
            "wpa", data_wireless['short_wpa'])
        self.assertIn(ssid, result)
        log.debug("016\t\tpass")

    def test_017_encryption_wpa_short_pwd(self):
        """修改加密方式为wpa2-psk,最短密码长度"""
        tmp = WirelessSettingsBusiness(self.driver)
        #修改加密方式为wpa2-psk
        tmp.change_wifi_ssid_encryption_pwd(data_wireless['all_ssid'], "psk2", data_wireless['short_wpa'])
        #使用无线网卡连接该ssid
        result = tmp.client_connect_ssid(data_wireless['all_ssid'], data_basic['wlan_pc'],
            "wpa", data_wireless['short_wpa'])
        self.assertIn(data_wireless['all_ssid'], result)
        log.debug("017\t\tpass")

    def test_018_check_encryption_wpa_less_short_pwd(self):
        """修改加密方式为wpa2-psk,低于最短密码长度"""
        tmp = WirelessSettingsBusiness(self.driver)
        #判断wpa密码输入框是否有红色警告
        result = tmp.check_wpa_password_warning("psk2", "12345")
        self.assertTrue(result)
        log.debug("018\t\tpass")

    def test_019_encryption_wpa_long_pwd(self):
        """修改加密方式为wpa2-psk,最长密码长度"""
        tmp = WirelessSettingsBusiness(self.driver)
        #修改加密方式为wpa2-psk
        tmp.change_wifi_encryption_pwd("psk2", data_wireless['long_wpa'])
        #使用无线网卡连接该ssid
        result = tmp.client_connect_ssid(data_wireless['all_ssid'], data_basic['wlan_pc'],
            "wpa", data_wireless['long_wpa'])
        self.assertIn(data_wireless['all_ssid'], result)
        log.debug("019\t\tpass")

    def test_020_check_encryption_wpa_more_long_pwd(self):
        """修改加密方式为wpa2-psk,高于最长密码长度"""
        tmp = WirelessSettingsBusiness(self.driver)
        #判断wpa密码输入框是否有红色警告
        result = tmp.check_wpa_password_warning("psk2", data_wireless['long_wpa']+"12")
        self.assertTrue(result)
        log.debug("020\t\tpass")

    def test_021_encryption_wep64_5pwd(self):
        """修改加密方式为wep64bit,5位密码"""
        tmp = WirelessSettingsBusiness(self.driver)
        #修改加密方式为wep64bit,5位密码
        tmp.change_wifi_encryption_pwd("wep+shared", data_wireless['wep64'])
        #使用无线网卡连接该ssid
        result = tmp.client_connect_ssid(data_wireless['all_ssid'], data_basic['wlan_pc'],
            "wep", data_wireless['wep64'])
        self.assertIn(data_wireless['all_ssid'], result)
        log.debug("021\t\tpass")

    def test_022_encryption_wep64_10pwd(self):
        """修改加密方式为wep64bit,10位密码"""
        tmp = WirelessSettingsBusiness(self.driver)
        #修改加密方式为wep64bit,10位密码
        tmp.change_wifi_encryption_pwd("wep+shared", data_wireless['wep64-10'])
        #使用无线网卡连接该ssid
        result = tmp.client_connect_ssid(data_wireless['all_ssid'], data_basic['wlan_pc'],
            "wep10_26", data_wireless['wep64-10'])
        self.assertIn(data_wireless['all_ssid'], result)
        log.debug("022\t\tpass")

    def test_023_encryption_wep128_13pwd(self):
        """修改加密方式为wep128bit,13位密码"""
        tmp = WirelessSettingsBusiness(self.driver)
        #修改加密方式为wep128bit,13位密码
        tmp.change_wifi_encryption_pwd("wep+shared", data_wireless['wep128'])
        #使用无线网卡连接该ssid
        result = tmp.client_connect_ssid(data_wireless['all_ssid'], data_basic['wlan_pc'],
            "wep", data_wireless['wep128'])
        self.assertIn(data_wireless['all_ssid'], result)
        log.debug("023\t\tpass")

    def test_024_encryption_wep128_26pwd(self):
        """修改加密方式为wep128bit,26位密码"""
        tmp = WirelessSettingsBusiness(self.driver)
        #修改加密方式为wep128bit,26位密码
        tmp.change_wifi_encryption_pwd("wep+shared", data_wireless['wep128-26'])
        #使用无线网卡连接该ssid
        result = tmp.client_connect_ssid(data_wireless['all_ssid'], data_basic['wlan_pc'],
            "wep10_26", data_wireless['wep128-26'])
        self.assertIn(data_wireless['all_ssid'], result)
        log.debug("024\t\tpass")

    def test_025_channel1(self):
        """验证AP的信道为1时"""
        tmp = WirelessSettingsBusiness(self.driver)
        #首先修改加密方式为wpa2-psk
        tmp.change_wifi_encryption_pwd("psk2", data_wireless['short_wpa'])
        #切换2.4G无线信道，判断，无线网卡连接取出该AP的频率值
        result = tmp.check_wifi_channel(1, data_wireless['all_ssid'], data_wireless['short_wpa'],
            data_basic['wlan_pc'])
        self.assertEqual(result, 2412)
        log.debug("025\t\tpass")

    def test_026_channel2(self):
        """验证AP的信道为2时"""
        tmp = WirelessSettingsBusiness(self.driver)
        #切换2.4G无线信道，判断，无线网卡连接取出该AP的频率值
        result = tmp.check_wifi_channel(2, data_wireless['all_ssid'], data_wireless['short_wpa'],
            data_basic['wlan_pc'])
        self.assertEqual(result, 2417)
        log.debug("026\t\tpass")

    def test_027_channel3(self):
        """验证AP的信道为3时"""
        tmp = WirelessSettingsBusiness(self.driver)
        #切换2.4G无线信道，判断，无线网卡连接取出该AP的频率值
        result = tmp.check_wifi_channel(3, data_wireless['all_ssid'], data_wireless['short_wpa'],
            data_basic['wlan_pc'])
        self.assertEqual(result, 2422)
        log.debug("027\t\tpass")

    def test_028_channel4(self):
        """验证AP的信道为4时"""
        tmp = WirelessSettingsBusiness(self.driver)
        #切换2.4G无线信道，判断，无线网卡连接取出该AP的频率值
        result = tmp.check_wifi_channel(4, data_wireless['all_ssid'], data_wireless['short_wpa'],
            data_basic['wlan_pc'])
        self.assertEqual(result, 2427)
        log.debug("028\t\tpass")

    def test_029_channel5(self):
        """验证AP的信道为5时"""
        tmp = WirelessSettingsBusiness(self.driver)
        #切换2.4G无线信道，判断，无线网卡连接取出该AP的频率值
        result = tmp.check_wifi_channel(5, data_wireless['all_ssid'], data_wireless['short_wpa'],
            data_basic['wlan_pc'])
        self.assertEqual(result, 2432)
        log.debug("029\t\tpass")

    def test_030_channel6(self):
        """验证AP的信道为6时"""
        tmp = WirelessSettingsBusiness(self.driver)
        #切换2.4G无线信道，判断，无线网卡连接取出该AP的频率值
        result = tmp.check_wifi_channel(6, data_wireless['all_ssid'], data_wireless['short_wpa'],
            data_basic['wlan_pc'])
        self.assertEqual(result, 2437)
        log.debug("030\t\tpass")

    def test_031_channel7(self):
        """验证AP的信道为7时"""
        tmp = WirelessSettingsBusiness(self.driver)
        #切换2.4G无线信道，判断，无线网卡连接取出该AP的频率值
        result = tmp.check_wifi_channel(7, data_wireless['all_ssid'], data_wireless['short_wpa'],
            data_basic['wlan_pc'])
        self.assertEqual(result, 2442)
        log.debug("031\t\tpass")

    def test_032_channel8(self):
        """验证AP的信道为8时"""
        tmp = WirelessSettingsBusiness(self.driver)
        #切换2.4G无线信道，判断，无线网卡连接取出该AP的频率值
        result = tmp.check_wifi_channel(8, data_wireless['all_ssid'], data_wireless['short_wpa'],
            data_basic['wlan_pc'])
        self.assertEqual(result, 2447)
        log.debug("032\t\tpass")

    def test_033_channel9(self):
        """验证AP的信道为9时"""
        tmp = WirelessSettingsBusiness(self.driver)
        #切换2.4G无线信道，判断，无线网卡连接取出该AP的频率值
        result = tmp.check_wifi_channel(9, data_wireless['all_ssid'], data_wireless['short_wpa'],
            data_basic['wlan_pc'])
        self.assertEqual(result, 2452)
        log.debug("033\t\tpass")

    def test_034_channel10(self):
        """验证AP的信道为10时"""
        tmp = WirelessSettingsBusiness(self.driver)
        #切换2.4G无线信道，判断，无线网卡连接取出该AP的频率值
        result = tmp.check_wifi_channel(10, data_wireless['all_ssid'], data_wireless['short_wpa'],
            data_basic['wlan_pc'])
        self.assertEqual(result, 2457)
        log.debug("034\t\tpass")

    def test_035_channel11(self):
        """验证AP的信道为11时"""
        tmp = WirelessSettingsBusiness(self.driver)
        #切换2.4G无线信道，判断，无线网卡连接取出该AP的频率值
        result = tmp.check_wifi_channel(11, data_wireless['all_ssid'], data_wireless['short_wpa'],
            data_basic['wlan_pc'])
        self.assertEqual(result, 2462)
        log.debug("035\t\tpass")

    def test_036_channel12(self):
        """验证AP的信道为12时"""
        tmp = WirelessSettingsBusiness(self.driver)
        #切换2.4G无线信道，判断，无线网卡连接取出该AP的频率值
        result = tmp.check_wifi_channel(12, data_wireless['all_ssid'], data_wireless['short_wpa'],
            data_basic['wlan_pc'])
        self.assertEqual(result, 2467)
        log.debug("036\t\tpass")

    def test_037_channel13(self):
        """验证AP的信道为13时"""
        tmp = WirelessSettingsBusiness(self.driver)
        #切换2.4G无线信道，判断，无线网卡连接取出该AP的频率值
        result = tmp.check_wifi_channel(13, data_wireless['all_ssid'], data_wireless['short_wpa'],
            data_basic['wlan_pc'])
        self.assertEqual(result, 2472)
        log.debug("037\t\tpass")

    def test_038_default_bandwidth(self):
        """验证默认带宽是40M"""
        tmp = WirelessSettingsBusiness(self.driver)
        #登录ap的后台，检查带宽
        result = tmp.check_ap_bandwidth(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'],"HT40")
        self.assertTrue(result)
        log.debug("038\t\tpass")

    def test_039_bandwidth_20M(self):
        """修改带宽是20M"""
        tmp = WirelessSettingsBusiness(self.driver)
        #修改带宽
        tmp.change_bandwidth("HT20")
        #登录ap的后台，检查带宽
        result = tmp.check_ap_bandwidth(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'],"HT20")
        self.assertTrue(result)
        log.debug("039\t\tpass")

    def test_040_default_power(self):
        """验证默认发射功率是30dbm"""
        tmp = WirelessSettingsBusiness(self.driver)
        #登录ap的后台，检查发射功率
        result = tmp.check_ap_power(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'],"30")
        self.assertTrue(result)
        log.debug("040\t\tpass")

    def test_041_power_25(self):
        """修改发射功率是25"""
        tmp = WirelessSettingsBusiness(self.driver)
        #修改发射功率
        tmp.change_power("25")
        #登录ap的后台，检查带宽
        result = tmp.check_ap_power(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'],"25")
        self.assertTrue(result)
        log.debug("041\t\tpass")

    def test_042_power_20(self):
        """修改发射功率是20"""
        tmp = WirelessSettingsBusiness(self.driver)
        #修改发射功率
        tmp.change_power("20")
        #登录ap的后台，检查带宽
        result = tmp.check_ap_power(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'],"20")
        self.assertTrue(result)
        log.debug("042\t\tpass")

    def test_043_power_15(self):
        """修改发射功率是15"""
        tmp = WirelessSettingsBusiness(self.driver)
        #修改发射功率
        tmp.change_power("15")
        #登录ap的后台，检查带宽
        result = tmp.check_ap_power(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'],"15")
        self.assertTrue(result)
        log.debug("043\t\tpass")

    def test_044_power_10(self):
        """修改发射功率是10"""
        tmp = WirelessSettingsBusiness(self.driver)
        #修改发射功率
        tmp.change_power("10")
        #登录ap的后台，检查带宽
        result = tmp.check_ap_power(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'],"10")
        self.assertTrue(result)
        log.debug("044\t\tpass")

    def test_045_power_5(self):
        """修改发射功率是5"""
        tmp = WirelessSettingsBusiness(self.driver)
        #修改发射功率
        tmp.change_power("5")
        #登录ap的后台，检查带宽
        result = tmp.check_ap_power(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'],"5")
        #修改回发射功率为默认的20dbm
        tmp.change_power("20")
        self.assertTrue(result)
        log.debug("045\t\tpass")

    def test_046_max_client_number_1(self):
        """修改最大用户数为1"""
        tmp = WirelessSettingsBusiness(self.driver)
        #修改最大用户数
        tmp.change_max_client_number("1")
        #无线网卡只能连上一个
        result1 = tmp.client_connect_ssid(data_wireless['all_ssid'], data_basic['wlan_pc'],
            "wpa", data_wireless['short_wpa'])
        #登录ap的后台，检查最大用户数
        result2 = tmp.check_ap_max_client_number(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'], "1")
        self.assertIn(data_wireless['all_ssid'], result1)
        self.assertTrue(result2)
        log.debug("046\t\tpass")

    def test_047_max_client_number_63(self):
        """修改最大用户数为63"""
        tmp = WirelessSettingsBusiness(self.driver)
        #修改最大用户数
        tmp.change_max_client_number("63")
        #无线网卡能够连上
        result1 = tmp.client_connect_ssid(data_wireless['all_ssid'], data_basic['wlan_pc'],
            "wpa", data_wireless['short_wpa'])
        #登录ap的后台，检查最大用户数
        result2 = tmp.check_ap_max_client_number(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'], "63")
        self.assertIn(data_wireless['all_ssid'], result1)
        self.assertTrue(result2)
        log.debug("047\t\tpass")

    def test_048_max_client_number_64(self):
        """修改最大用户数不限制即设为64"""
        tmp = WirelessSettingsBusiness(self.driver)
        #修改最大用户数
        tmp.change_max_client_number("64")
        #无线网卡能够连上
        result1 = tmp.client_connect_ssid(data_wireless['all_ssid'], data_basic['wlan_pc'],
            "wpa", data_wireless['short_wpa'])
        #登录ap的后台，检查最大用户数
        result2 = tmp.check_ap_max_client_number(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'], "256")
        self.assertIn(data_wireless['all_ssid'], result1)
        self.assertTrue(result2)
        log.debug("048\t\tpass")

    def test_049_add_3ssids(self):
        """添加3个ssid，并验证都能正常工作"""
        tmp = WirelessSettingsBusiness(self.driver)
        #添加3个ssid,加密方式none和wpa
        tmp.add_many_ssids_none_wpa(3, data_wireless['all_ssid'], "psk2",
            data_wireless['short_wpa'])
        #使用无线网卡分别连接这些ssid
        result1 = tmp.client_connect_ssid(data_wireless['all_ssid']+"-%s"%1,
            data_basic['wlan_pc'], "wpa",data_wireless['short_wpa'])
        result2 = tmp.client_connect_ssid(data_wireless['all_ssid']+"-%s"%2,
            data_basic['wlan_pc'], "wpa",data_wireless['short_wpa'])
        result3 = tmp.client_connect_ssid(data_wireless['all_ssid']+"-%s"%3,
            data_basic['wlan_pc'], "wpa",data_wireless['short_wpa'])
        #删除所有的ssid
        tmp.del_all_ssid()
        self.assertIn(data_wireless['all_ssid']+"-%s"%1, result1)
        self.assertIn(data_wireless['all_ssid']+"-%s"%2, result2)
        self.assertIn(data_wireless['all_ssid']+"-%s"%3, result3)
        log.debug("049\t\tpass")

    def test_050_default_shortGI(self):
        """验证默认开启短防护时间间隔"""
        tmp = WirelessSettingsBusiness(self.driver)
        result = tmp.check_ap_shortGI(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'])
        self.assertTrue(result)
        log.debug("050\t\tpass")

    def test_051_close_shortGI(self):
        """验证关闭短防护时间间隔"""
        tmp = WirelessSettingsBusiness(self.driver)
        #关闭短防护时间间隔
        tmp.change_shortGI()
        result = tmp.check_ap_shortGI(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'])
        #开启短防护时间间隔
        tmp.change_shortGI()
        self.assertFalse(result)
        log.debug("051\t\tpass")

    def test_052_default_WDS(self):
        """验证默认开启WDS"""
        tmp = WirelessSettingsBusiness(self.driver)
        result = tmp.check_ap_WDS(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'])
        self.assertTrue(result)
        log.debug("052\t\tpass")

    def test_053_close_WDS(self):
        """验证关闭WDS"""
        tmp = WirelessSettingsBusiness(self.driver)
        #关闭WDS
        tmp.change_WDS()
        result = tmp.check_ap_WDS(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'])
        #开启WDS
        tmp.change_WDS()
        self.assertFalse(result)
        log.debug("053\t\tpass")

    def test_054_default_WMM(self):
        """验证默认开启无线多媒体"""
        tmp = WirelessSettingsBusiness(self.driver)
        result = tmp.check_ap_WMM(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'])
        self.assertTrue(result)
        log.debug("054\t\tpass")

    def test_055_close_WMM(self):
        """验证关闭无线多媒体"""
        tmp = WirelessSettingsBusiness(self.driver)
        #关闭无线多媒体
        tmp.change_WMM()
        result = tmp.check_ap_WMM(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'])
        #开启无线多媒体
        tmp.change_WMM()
        self.assertFalse(result)
        log.debug("055\t\tpass")

    def test_056_default_wireless_isolate(self):
        """验证默认关闭无线隔离"""
        tmp = WirelessSettingsBusiness(self.driver)
        result = tmp.check_ap_wireless_isolate(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'])
        self.assertFalse(result)
        log.debug("056\t\tpass")

    def test_057_open_wireless_isolate(self):
        """验证开启无线隔离"""
        tmp = WirelessSettingsBusiness(self.driver)
        #开启无线隔离
        tmp.change_wireless_isolate()
        result = tmp.check_ap_wireless_isolate(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'])
        #开启无线隔离
        tmp.change_wireless_isolate()
        self.assertTrue(result)
        log.debug("057\t\tpass")

    def test_058_default_fragment_threshold(self):
        """验证默认分割阈值为2346"""
        tmp = WirelessSettingsBusiness(self.driver)
        result = tmp.check_ap_fragment_threshold(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'], 2346)
        self.assertTrue(result)
        log.debug("058\t\tpass")

    def test_059_change_fragment_threshold(self):
        """验证修改分割阈值为1500"""
        tmp = WirelessSettingsBusiness(self.driver)
        #设置分割阈值为1500
        tmp.change_fragment_threshold(1500)
        result = tmp.check_ap_fragment_threshold(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'], 1500)
        #把分割阈值改回默认的2346
        tmp.change_fragment_threshold(2346)
        self.assertTrue(result)
        log.debug("059\t\tpass")

    def test_060_default_rts_threshold(self):
        """验证默认rts阈值为2347"""
        tmp = WirelessSettingsBusiness(self.driver)
        result = tmp.check_ap_rts_threshold(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'], 2347)
        self.assertTrue(result)
        log.debug("060\t\tpass")

    def test_061_change_rts_threshold(self):
        """验证修改rts阈值为1500"""
        tmp = WirelessSettingsBusiness(self.driver)
        #设置rts阈值为1500
        tmp.change_rts_threshold(1500)
        result = tmp.check_ap_rts_threshold(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'], 1500)
        #把rts阈值改回默认的2347
        tmp.change_rts_threshold(2347)
        tmp.disconnect_ap()
        self.assertTrue(result)
        log.debug("061\t\tpass")









    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
