#coding=utf-8
#作者：曾祥卫
#时间：2018.09.19
#描述：用例层代码，调用workmode_business

import unittest,time
from selenium import webdriver
from login.login_business import LoginBusiness
from workmode.workmode_business import WorkModeBusiness
from systemtools.configupdate.configupdate_business import ConfigUpdateBusiness
from stateinfo.stateinfo_business import StateInfoBusiness
from network.wirelesssettings.wirelesssettings_business import WirelessSettingsBusiness
from connect.ssh import SSH
from data import data
from data.logfile import Log

data_basic = data.data_basic()
data_login = data.data_login()
data_wirless = data.data_wireless()
data_wan = data.data_wan()
data_lan = data.data_lan()

log = Log("WorkMode")

class TestWorkMode(unittest.TestCase):
    """测试工作模式的用例集(Duration:4.00h)"""
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


    def test_001_default_routemode_dhcp(self):
        """默认情况下，工作模式为路由模式，DHCP功能开启"""
        #首先启用无线网卡
        tmp = WorkModeBusiness(self.driver)
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
        tmp1 = StateInfoBusiness(self.driver)
        #获取当前模式
        result1 = tmp1.obtain_AP_current_mode()
        #获取外网的IP获取方式
        result2 = tmp1.obtain_WAN_IP_generation()
        #获取IP地址
        result3 = tmp1.obtain_WAN_IP_address()
        self.assertEqual(result1, "路由模式")
        self.assertEqual(result2, "动态获取")
        self.assertIn(data_wan['wan_str'], result3)
        log.debug("001\t\tpass")

    def test_002_routemode_WANpppoe_stateinfo(self):
        """修改工作模式为路由模式,外网设置pppoe模式-检查状态信息页面"""
        tmp = WorkModeBusiness(self.driver)
        #修改工作模式为路由模式,外网设置pppoe模式
        tmp.change_workmode_to_route_WANpppoe(data_wan['pppoe_user'],
            data_wan['pppoe_password'], data_wirless['all_ssid'],
            "psk2", data_wirless['short_wpa'], "HT20", "auto")

        tmp1 = StateInfoBusiness(self.driver)
        self.driver.refresh()
        self.driver.implicitly_wait(10)
        #获取当前模式
        result1 = tmp1.obtain_AP_current_mode()
        #获取外网的IP获取方式
        result2 = tmp1.obtain_WAN_IP_generation()
        #获取IP地址
        result3 = tmp1.obtain_WAN_IP_address()
        self.assertEqual(result1, "路由模式")
        self.assertEqual(result2, "PPPOE拨号")
        self.assertIn(data_wan['wan_str'], result3)
        log.debug("002\t\tpass")

    def test_003_routemode_WANpppoe_wifi_access_internet(self):
        """修改工作模式为路由模式,外网设置pppoe模式-无线能访问internet"""
        tmp = WorkModeBusiness(self.driver)
        #判断运行模式设置后，AP正常：能上网，无线网卡能够连接上AP的SSID
        resutl1, result2 = tmp.check_after_workmode_normal(data_wirless['all_ssid'],
            data_basic['wlan_pc'], "wpa", data_wirless['short_wpa'])
        self.assertEqual(resutl1, 0)
        self.assertIn(data_wirless['all_ssid'], result2)
        log.debug("003\t\tpass")

    def test_004_routemode_WANpppoe_wpa2(self):
        """修改工作模式为路由模式,外网设置pppoe模式-无线加密为wpa2"""
        tmp = WorkModeBusiness(self.driver)
        #无线网卡能够连接上AP的SSID
        result = tmp.client_connect_ssid(data_wirless['all_ssid'],
            data_basic['wlan_pc'], "wpa", data_wirless['short_wpa'])
        self.assertIn(data_wirless['all_ssid'], result)
        log.debug("004\t\tpass")

    def test_005_routemode_WANpppoe_None(self):
        """修改工作模式为路由模式,外网设置pppoe模式-无线加密为None"""
        tmp = WorkModeBusiness(self.driver)
        #修改工作模式为路由模式,外网设置pppoe模式
        tmp.change_workmode_to_route_WANpppoe(data_wan['pppoe_user'],
            data_wan['pppoe_password'], data_wirless['all_ssid'],
            "none", "", "HT20", "auto")
        #无线网卡能够连接上AP的SSID
        result = tmp.client_connect_ssid(data_wirless['all_ssid'],
            data_basic['wlan_pc'], "open")
        self.assertIn(data_wirless['all_ssid'], result)
        log.debug("005\t\tpass")

    def test_006_routemode_WANpppoe_wep64_5ACSII(self):
        """修改工作模式为路由模式,外网设置pppoe模式-无线加密为wep64,5位ACSII密码"""
        tmp = WorkModeBusiness(self.driver)
        #修改工作模式为路由模式,外网设置pppoe模式
        tmp.change_workmode_to_route_WANpppoe(data_wan['pppoe_user'],
            data_wan['pppoe_password'], data_wirless['all_ssid'],
            "wep+shared", data_wirless['wep64'], "HT20", "auto")
        #无线网卡能够连接上AP的SSID
        result = tmp.client_connect_ssid(data_wirless['all_ssid'],
            data_basic['wlan_pc'], "wep", data_wirless['wep64'])
        self.assertIn(data_wirless['all_ssid'], result)
        log.debug("006\t\tpass")

    def test_007_routemode_WANpppoe_wep64_10HEX(self):
        """修改工作模式为路由模式,外网设置pppoe模式-无线加密为wep64,10位16进制密码"""
        tmp = WorkModeBusiness(self.driver)
        #修改工作模式为路由模式,外网设置pppoe模式
        tmp.change_workmode_to_route_WANpppoe(data_wan['pppoe_user'],
            data_wan['pppoe_password'], data_wirless['all_ssid'],
            "wep+shared", data_wirless['wep64-10'], "HT20", "auto")
        #无线网卡能够连接上AP的SSID
        result = tmp.client_connect_ssid(data_wirless['all_ssid'],
            data_basic['wlan_pc'], "wep10_26", data_wirless['wep64-10'])
        self.assertIn(data_wirless['all_ssid'], result)
        log.debug("007\t\tpass")

    def test_008_routemode_WANpppoe_wep128_13ACSII(self):
        """修改工作模式为路由模式,外网设置pppoe模式-无线加密为wep128,13位ACSII密码"""
        tmp = WorkModeBusiness(self.driver)
        #修改工作模式为路由模式,外网设置pppoe模式
        tmp.change_workmode_to_route_WANpppoe(data_wan['pppoe_user'],
            data_wan['pppoe_password'], data_wirless['all_ssid'],
            "wep+shared", data_wirless['wep128'], "HT20", "auto")
        #无线网卡能够连接上AP的SSID
        result = tmp.client_connect_ssid(data_wirless['all_ssid'],
            data_basic['wlan_pc'], "wep", data_wirless['wep128'])
        self.assertIn(data_wirless['all_ssid'], result)
        log.debug("008\t\tpass")

    def test_009_routemode_WANpppoe_wep128_26HEX(self):
        """修改工作模式为路由模式,外网设置pppoe模式-无线加密为wep128,26位16进制密码"""
        tmp = WorkModeBusiness(self.driver)
        #修改工作模式为路由模式,外网设置pppoe模式
        tmp.change_workmode_to_route_WANpppoe(data_wan['pppoe_user'],
            data_wan['pppoe_password'], data_wirless['all_ssid'],
            "wep+shared", data_wirless['wep128-26'], "HT20", "auto")
        #无线网卡能够连接上AP的SSID
        result = tmp.client_connect_ssid(data_wirless['all_ssid'],
            data_basic['wlan_pc'], "wep10_26", data_wirless['wep128-26'])
        self.assertIn(data_wirless['all_ssid'], result)
        log.debug("009\t\tpass")

    def test_010_routemode_WANpppoe_wifi_width_HT20(self):
        """修改工作模式为路由模式,外网设置pppoe模式-HT20"""
        tmp = WorkModeBusiness(self.driver)
        #修改工作模式为路由模式,外网设置pppoe模式
        tmp.change_workmode_to_route_WANpppoe(data_wan['pppoe_user'],
            data_wan['pppoe_password'], data_wirless['all_ssid'],
            "psk2", data_wirless['short_wpa'], "HT20", "auto")
        tmp1 = WirelessSettingsBusiness(self.driver)
        #登录ap的后台，检查带宽
        result = tmp1.check_ap_bandwidth(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'],"HT20")
        self.assertTrue(result)
        log.debug("010\t\tpass")

    def test_011_routemode_WANpppoe_wifi_width_HT40(self):
        """修改工作模式为路由模式,外网设置pppoe模式-HT40"""
        tmp = WorkModeBusiness(self.driver)
        #修改工作模式为路由模式,外网设置pppoe模式
        tmp.change_workmode_to_route_WANpppoe(data_wan['pppoe_user'],
            data_wan['pppoe_password'], data_wirless['all_ssid'],
            "psk2", data_wirless['short_wpa'], "HT40", "auto")
        tmp1 = WirelessSettingsBusiness(self.driver)
        #登录ap的后台，检查带宽
        result = tmp1.check_ap_bandwidth(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'],"HT40")
        self.assertTrue(result)
        log.debug("011\t\tpass")

    def test_012_routemode_WANpppoe_wifi_channel_1(self):
        """修改工作模式为路由模式,外网设置pppoe模式-channel1"""
        tmp = WorkModeBusiness(self.driver)
        #修改工作模式为路由模式,外网设置pppoe模式
        tmp.change_workmode_to_route_WANpppoe(data_wan['pppoe_user'],
            data_wan['pppoe_password'], data_wirless['all_ssid'],
            "psk2", data_wirless['short_wpa'], "HT20", 1)
        #判断，无线网卡连接取出该AP的频率值
        result = tmp.connected_AP_Freq(data_wirless['all_ssid'], data_wirless['short_wpa'],
            data_basic['wlan_pc'])
        self.assertEqual(result, 2412)
        log.debug("012\t\tpass")

    def test_013_routemode_WANpppoe_wifi_channel_6(self):
        """修改工作模式为路由模式,外网设置pppoe模式-channel6"""
        tmp = WorkModeBusiness(self.driver)
        #修改工作模式为路由模式,外网设置pppoe模式
        tmp.change_workmode_to_route_WANpppoe(data_wan['pppoe_user'],
            data_wan['pppoe_password'], data_wirless['all_ssid'],
            "psk2", data_wirless['short_wpa'], "HT20", 6)
        #判断，无线网卡连接取出该AP的频率值
        result = tmp.connected_AP_Freq(data_wirless['all_ssid'], data_wirless['short_wpa'],
            data_basic['wlan_pc'])
        self.assertEqual(result, 2437)
        log.debug("013\t\tpass")

    def test_014_routemode_WANpppoe_wifi_channel_13(self):
        """修改工作模式为路由模式,外网设置pppoe模式-channel13"""
        tmp = WorkModeBusiness(self.driver)
        #修改工作模式为路由模式,外网设置pppoe模式
        tmp.change_workmode_to_route_WANpppoe(data_wan['pppoe_user'],
            data_wan['pppoe_password'], data_wirless['all_ssid'],
            "psk2", data_wirless['short_wpa'], "HT20", 13)
        #判断，无线网卡连接取出该AP的频率值
        result = tmp.connected_AP_Freq(data_wirless['all_ssid'], data_wirless['short_wpa'],
            data_basic['wlan_pc'])
        self.assertEqual(result, 2472)
        log.debug("014\t\tpass")

    def test_015_routemode_WANdhcp_stateinfo(self):
        """修改工作模式为路由模式,外网设置dhcp模式-检查状态信息页面"""
        tmp = WorkModeBusiness(self.driver)
        #修改工作模式为路由模式,外网设置dhcp模式
        tmp.change_workmode_to_route_WANdhcp(data_wirless['all_ssid'],
            "psk2", data_wirless['short_wpa'], "HT40", "auto")

        tmp1 = StateInfoBusiness(self.driver)
        self.driver.refresh()
        self.driver.implicitly_wait(10)
        #获取当前模式
        result1 = tmp1.obtain_AP_current_mode()
        #获取外网的IP获取方式
        result2 = tmp1.obtain_WAN_IP_generation()
        #获取IP地址
        result3 = tmp1.obtain_WAN_IP_address()
        self.assertEqual(result1, "路由模式")
        self.assertEqual(result2, "动态获取")
        self.assertIn(data_wan['wan_str'], result3)
        log.debug("015\t\tpass")

    def test_016_routemode_WANdhcp_wifi_access_internet(self):
        """修改工作模式为路由模式,外网设置dhcp模式-无线能访问internet"""
        tmp = WorkModeBusiness(self.driver)
        #判断运行模式设置后，AP正常：能上网，无线网卡能够连接上AP的SSID
        resutl1, result2 = tmp.check_after_workmode_normal(data_wirless['all_ssid'],
            data_basic['wlan_pc'], "wpa", data_wirless['short_wpa'])
        self.assertEqual(resutl1, 0)
        self.assertIn(data_wirless['all_ssid'], result2)
        log.debug("016\t\tpass")

    def test_017_routemode_WANdhcp_wpa2(self):
        """修改工作模式为路由模式,外网设置dhcp模式-无线加密为wpa2"""
        tmp = WorkModeBusiness(self.driver)
        #无线网卡能够连接上AP的SSID
        result = tmp.client_connect_ssid(data_wirless['all_ssid'],
            data_basic['wlan_pc'], "wpa", data_wirless['short_wpa'])
        self.assertIn(data_wirless['all_ssid'], result)
        log.debug("017\t\tpass")

    def test_018_routemode_WANdhcp_None(self):
        """修改工作模式为路由模式,外网设置dhcp模式-无线加密为None"""
        tmp = WorkModeBusiness(self.driver)
        #修改工作模式为路由模式,外网设置dhcp模式
        tmp.change_workmode_to_route_WANdhcp(data_wirless['all_ssid'],
            "none", "", "HT20", "auto")
        #无线网卡能够连接上AP的SSID
        result = tmp.client_connect_ssid(data_wirless['all_ssid'],
            data_basic['wlan_pc'], "open")
        self.assertIn(data_wirless['all_ssid'], result)
        log.debug("018\t\tpass")

    def test_019_routemode_WANdhcp_wep64_5ACSII(self):
        """修改工作模式为路由模式,外网设置dhcp模式-无线加密为wep64,5位ACSII密码"""
        tmp = WorkModeBusiness(self.driver)
        #修改工作模式为路由模式,外网设置dhcp模式
        tmp.change_workmode_to_route_WANdhcp(data_wirless['all_ssid'],
            "wep+shared", data_wirless['wep64'], "HT20", "auto")
        #无线网卡能够连接上AP的SSID
        result = tmp.client_connect_ssid(data_wirless['all_ssid'],
            data_basic['wlan_pc'], "wep", data_wirless['wep64'])
        self.assertIn(data_wirless['all_ssid'], result)
        log.debug("019\t\tpass")

    def test_020_routemode_WANdhcp_wep64_10HEX(self):
        """修改工作模式为路由模式,外网设置dhcp模式-无线加密为wep64,10位16进制密码"""
        tmp = WorkModeBusiness(self.driver)
        #修改工作模式为路由模式,外网设置dhcp模式
        tmp.change_workmode_to_route_WANdhcp(data_wirless['all_ssid'],
            "wep+shared", data_wirless['wep64-10'], "HT20", "auto")
        #无线网卡能够连接上AP的SSID
        result = tmp.client_connect_ssid(data_wirless['all_ssid'],
            data_basic['wlan_pc'], "wep10_26", data_wirless['wep64-10'])
        self.assertIn(data_wirless['all_ssid'], result)
        log.debug("020\t\tpass")

    def test_021_routemode_WANdhcp_wep128_13ACSII(self):
        """修改工作模式为路由模式,外网设置dhcp模式-无线加密为wep128,13位ACSII密码"""
        tmp = WorkModeBusiness(self.driver)
        #修改工作模式为路由模式,外网设置dhcp模式
        tmp.change_workmode_to_route_WANdhcp( data_wirless['all_ssid'],
            "wep+shared", data_wirless['wep128'], "HT20", "auto")
        #无线网卡能够连接上AP的SSID
        result = tmp.client_connect_ssid(data_wirless['all_ssid'],
            data_basic['wlan_pc'], "wep", data_wirless['wep128'])
        self.assertIn(data_wirless['all_ssid'], result)
        log.debug("021\t\tpass")

    def test_022_routemode_WANdhcp_wep128_26HEX(self):
        """修改工作模式为路由模式,外网设置dhcp模式-无线加密为wep128,26位16进制密码"""
        tmp = WorkModeBusiness(self.driver)
        #修改工作模式为路由模式,外网设置dhcp模式
        tmp.change_workmode_to_route_WANdhcp(data_wirless['all_ssid'],
            "wep+shared", data_wirless['wep128-26'], "HT20", "auto")
        #无线网卡能够连接上AP的SSID
        result = tmp.client_connect_ssid(data_wirless['all_ssid'],
            data_basic['wlan_pc'], "wep10_26", data_wirless['wep128-26'])
        self.assertIn(data_wirless['all_ssid'], result)
        log.debug("022\t\tpass")

    def test_023_routemode_WANdhcp_wifi_width_HT20(self):
        """修改工作模式为路由模式,外网设置dhcp模式-HT20"""
        tmp = WorkModeBusiness(self.driver)
        #修改工作模式为路由模式,外网设置dhcp模式
        tmp.change_workmode_to_route_WANdhcp(data_wirless['all_ssid'],
            "psk2", data_wirless['short_wpa'], "HT20", "auto")
        tmp1 = WirelessSettingsBusiness(self.driver)
        #登录ap的后台，检查带宽
        result = tmp1.check_ap_bandwidth(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'],"HT20")
        self.assertTrue(result)
        log.debug("023\t\tpass")

    def test_024_routemode_WANdhcp_wifi_width_HT40(self):
        """修改工作模式为路由模式,外网设置dhcp模式-HT40"""
        tmp = WorkModeBusiness(self.driver)
        #修改工作模式为路由模式,外网设置dhcp模式
        tmp.change_workmode_to_route_WANdhcp(data_wirless['all_ssid'],
            "psk2", data_wirless['short_wpa'], "HT40", "auto")
        tmp1 = WirelessSettingsBusiness(self.driver)
        #登录ap的后台，检查带宽
        result = tmp1.check_ap_bandwidth(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'],"HT40")
        self.assertTrue(result)
        log.debug("024\t\tpass")

    def test_025_routemode_WANdhcp_wifi_channel_2(self):
        """修改工作模式为路由模式,外网设置dhcp模式-channel2"""
        tmp = WorkModeBusiness(self.driver)
        #修改工作模式为路由模式,外网设置dhcp模式
        tmp.change_workmode_to_route_WANdhcp(data_wirless['all_ssid'],
            "psk2", data_wirless['short_wpa'], "HT20", 2)
        #判断，无线网卡连接取出该AP的频率值
        result = tmp.connected_AP_Freq(data_wirless['all_ssid'], data_wirless['short_wpa'],
            data_basic['wlan_pc'])
        self.assertEqual(result, 2417)
        log.debug("025\t\tpass")

    def test_026_routemode_WANdhcp_wifi_channel_7(self):
        """修改工作模式为路由模式,外网设置dhcp模式-channel7"""
        tmp = WorkModeBusiness(self.driver)
        #修改工作模式为路由模式,外网设置dhcp模式
        tmp.change_workmode_to_route_WANdhcp(data_wirless['all_ssid'],
            "psk2", data_wirless['short_wpa'], "HT20", 7)
        #判断，无线网卡连接取出该AP的频率值
        result = tmp.connected_AP_Freq(data_wirless['all_ssid'], data_wirless['short_wpa'],
            data_basic['wlan_pc'])
        self.assertEqual(result, 2442)
        log.debug("026\t\tpass")

    def test_027_routemode_WANdhcp_wifi_channel_12(self):
        """修改工作模式为路由模式,外网设置dhcp模式-channel12"""
        tmp = WorkModeBusiness(self.driver)
        #修改工作模式为路由模式,外网设置dhcp模式
        tmp.change_workmode_to_route_WANdhcp(data_wirless['all_ssid'],
            "psk2", data_wirless['short_wpa'], "HT20", 12)
        #判断，无线网卡连接取出该AP的频率值
        result = tmp.connected_AP_Freq(data_wirless['all_ssid'], data_wirless['short_wpa'],
            data_basic['wlan_pc'])
        self.assertEqual(result, 2467)
        log.debug("027\t\tpass")

    def test_028_routemode_WANstaticIP_stateinfo(self):
        """修改工作模式为路由模式,外网设置staticIP模式-检查状态信息页面"""
        #修改工作模式为路由模式,外网设置static IP模式
        tmp = WorkModeBusiness(self.driver)
        tmp.change_workmode_to_route_WANstaticIP(data_wan['static_IP'],
            data_wan['netmask'], data_wan['gateway'], data_wan['DNS'],
            data_wirless['all_ssid'],"psk2", data_wirless['short_wpa'], "HT20", "auto")

        tmp1 = StateInfoBusiness(self.driver)
        self.driver.refresh()
        self.driver.implicitly_wait(10)
        #获取当前模式
        result1 = tmp1.obtain_AP_current_mode()
        #获取外网的IP获取方式
        result2 = tmp1.obtain_WAN_IP_generation()
        #获取IP地址
        result3 = tmp1.obtain_WAN_IP_address()
        self.assertEqual(result1, "路由模式")
        self.assertEqual(result2, "静态IP")
        self.assertEqual(data_wan['static_IP'], result3)
        log.debug("028\t\tpass")

    def test_029_routemode_WANstaticIP_wifi_access_internet(self):
        """修改工作模式为路由模式,外网设置staticIP模式-无线能访问internet"""
        tmp = WorkModeBusiness(self.driver)
        #判断运行模式设置后，AP正常：能上网，无线网卡能够连接上AP的SSID
        resutl1, result2 = tmp.check_after_workmode_normal(data_wirless['all_ssid'],
            data_basic['wlan_pc'], "wpa", data_wirless['short_wpa'])
        self.assertEqual(resutl1, 0)
        self.assertIn(data_wirless['all_ssid'], result2)
        log.debug("029\t\tpass")

    def test_030_routemode_WANstaticIP_wpa2(self):
        """修改工作模式为路由模式,外网设置staticIP模式-无线加密为wpa2"""
        tmp = WorkModeBusiness(self.driver)
        #无线网卡能够连接上AP的SSID
        result = tmp.client_connect_ssid(data_wirless['all_ssid'],
            data_basic['wlan_pc'], "wpa", data_wirless['short_wpa'])
        self.assertIn(data_wirless['all_ssid'], result)
        log.debug("030\t\tpass")

    def test_031_routemode_WANstaticIP_None(self):
        """修改工作模式为路由模式,外网设置staticIP模式-无线加密为None"""
        tmp = WorkModeBusiness(self.driver)
        #修改工作模式为路由模式,外网设置staticIP模式
        tmp.change_workmode_to_route_WANstaticIP(data_wan['static_IP'],
            data_wan['netmask'], data_wan['gateway'], data_wan['DNS'],
            data_wirless['all_ssid'],
            "none", "", "HT20", "auto")
        #无线网卡能够连接上AP的SSID
        result = tmp.client_connect_ssid(data_wirless['all_ssid'],
            data_basic['wlan_pc'], "open")
        self.assertIn(data_wirless['all_ssid'], result)
        log.debug("031\t\tpass")

    def test_032_routemode_WANstaticIP_wep64_5ACSII(self):
        """修改工作模式为路由模式,外网设置staticIP模式-无线加密为wep64,5位ACSII密码"""
        tmp = WorkModeBusiness(self.driver)
        #修改工作模式为路由模式,外网设置staticIP模式
        tmp.change_workmode_to_route_WANstaticIP(data_wan['static_IP'],
            data_wan['netmask'], data_wan['gateway'], data_wan['DNS'],
            data_wirless['all_ssid'],
            "wep+shared", data_wirless['wep64'], "HT20", "auto")
        #无线网卡能够连接上AP的SSID
        result = tmp.client_connect_ssid(data_wirless['all_ssid'],
            data_basic['wlan_pc'], "wep", data_wirless['wep64'])
        self.assertIn(data_wirless['all_ssid'], result)
        log.debug("032\t\tpass")

    def test_033_routemode_WANstaticIP_wep64_10HEX(self):
        """修改工作模式为路由模式,外网设置staticIP模式-无线加密为wep64,10位16进制密码"""
        tmp = WorkModeBusiness(self.driver)
        #修改工作模式为路由模式,外网设置staticIP模式
        tmp.change_workmode_to_route_WANstaticIP(data_wan['static_IP'],
            data_wan['netmask'], data_wan['gateway'], data_wan['DNS'],
            data_wirless['all_ssid'],
            "wep+shared", data_wirless['wep64-10'], "HT20", "auto")
        #无线网卡能够连接上AP的SSID
        result = tmp.client_connect_ssid(data_wirless['all_ssid'],
            data_basic['wlan_pc'], "wep10_26", data_wirless['wep64-10'])
        self.assertIn(data_wirless['all_ssid'], result)
        log.debug("033\t\tpass")

    def test_034_routemode_WANstaticIP_wep128_13ACSII(self):
        """修改工作模式为路由模式,外网设置staticIP模式-无线加密为wep128,13位ACSII密码"""
        tmp = WorkModeBusiness(self.driver)
        #修改工作模式为路由模式,外网设置staticIP模式
        tmp.change_workmode_to_route_WANstaticIP(data_wan['static_IP'],
            data_wan['netmask'], data_wan['gateway'], data_wan['DNS'],
            data_wirless['all_ssid'],
            "wep+shared", data_wirless['wep128'], "HT20", "auto")
        #无线网卡能够连接上AP的SSID
        result = tmp.client_connect_ssid(data_wirless['all_ssid'],
            data_basic['wlan_pc'], "wep", data_wirless['wep128'])
        self.assertIn(data_wirless['all_ssid'], result)
        log.debug("034\t\tpass")

    def test_035_routemode_WANstaticIP_wep128_26HEX(self):
        """修改工作模式为路由模式,外网设置staticIP模式-无线加密为wep128,26位16进制密码"""
        tmp = WorkModeBusiness(self.driver)
        #修改工作模式为路由模式,外网设置staticIP模式
        tmp.change_workmode_to_route_WANstaticIP(data_wan['static_IP'],
            data_wan['netmask'], data_wan['gateway'], data_wan['DNS'],
            data_wirless['all_ssid'],
            "wep+shared", data_wirless['wep128-26'], "HT20", "auto")
        #无线网卡能够连接上AP的SSID
        result = tmp.client_connect_ssid(data_wirless['all_ssid'],
            data_basic['wlan_pc'], "wep10_26", data_wirless['wep128-26'])
        self.assertIn(data_wirless['all_ssid'], result)
        log.debug("035\t\tpass")

    def test_036_routemode_WANstaticIP_wifi_width_HT20(self):
        """修改工作模式为路由模式,外网设置staticIP模式-HT20"""
        tmp = WorkModeBusiness(self.driver)
        #修改工作模式为路由模式,外网设置staticIP模式
        tmp.change_workmode_to_route_WANstaticIP(data_wan['static_IP'],
            data_wan['netmask'], data_wan['gateway'], data_wan['DNS'],
            data_wirless['all_ssid'],
            "psk2", data_wirless['short_wpa'], "HT20", "auto")
        tmp1 = WirelessSettingsBusiness(self.driver)
        #登录ap的后台，检查带宽
        result = tmp1.check_ap_bandwidth(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'],"HT20")
        self.assertTrue(result)
        log.debug("036\t\tpass")

    def test_037_routemode_WANstaticIP_wifi_width_HT40(self):
        """修改工作模式为路由模式,外网设置staticIP模式-HT40"""
        tmp = WorkModeBusiness(self.driver)
        #修改工作模式为路由模式,外网设置staticIP模式
        tmp.change_workmode_to_route_WANstaticIP(data_wan['static_IP'],
            data_wan['netmask'], data_wan['gateway'], data_wan['DNS'],
            data_wirless['all_ssid'],
            "psk2", data_wirless['short_wpa'], "HT40", "auto")
        tmp1 = WirelessSettingsBusiness(self.driver)
        #登录ap的后台，检查带宽
        result = tmp1.check_ap_bandwidth(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'],"HT40")
        self.assertTrue(result)
        log.debug("037\t\tpass")

    def test_038_routemode_WANstaticIP_wifi_channel_3(self):
        """修改工作模式为路由模式,外网设置staticIP模式-channel3"""
        tmp = WorkModeBusiness(self.driver)
        #修改工作模式为路由模式,外网设置staticIP模式
        tmp.change_workmode_to_route_WANstaticIP(data_wan['static_IP'],
            data_wan['netmask'], data_wan['gateway'], data_wan['DNS'],
            data_wirless['all_ssid'],
            "psk2", data_wirless['short_wpa'], "HT20", 3)
        #判断，无线网卡连接取出该AP的频率值
        result = tmp.connected_AP_Freq(data_wirless['all_ssid'], data_wirless['short_wpa'],
            data_basic['wlan_pc'])
        self.assertEqual(result, 2422)
        log.debug("038\t\tpass")

    def test_039_routemode_WANstaticIP_wifi_channel_8(self):
        """修改工作模式为路由模式,外网设置staticIP模式-channel8"""
        tmp = WorkModeBusiness(self.driver)
        #修改工作模式为路由模式,外网设置staticIP模式
        tmp.change_workmode_to_route_WANstaticIP(data_wan['static_IP'],
            data_wan['netmask'], data_wan['gateway'], data_wan['DNS'],
            data_wirless['all_ssid'],
            "psk2", data_wirless['short_wpa'], "HT20", 8)
        #判断，无线网卡连接取出该AP的频率值
        result = tmp.connected_AP_Freq(data_wirless['all_ssid'], data_wirless['short_wpa'],
            data_basic['wlan_pc'])
        self.assertEqual(result, 2447)
        log.debug("039\t\tpass")

    def test_040_routemode_WANstaticIP_wifi_channel_11(self):
        """修改工作模式为路由模式,外网设置staticIP模式-channel11"""
        tmp = WorkModeBusiness(self.driver)
        #修改工作模式为路由模式,外网设置staticIP模式
        tmp.change_workmode_to_route_WANstaticIP(data_wan['static_IP'],
            data_wan['netmask'], data_wan['gateway'], data_wan['DNS'],
            data_wirless['all_ssid'],
            "psk2", data_wirless['short_wpa'], "HT20", 11)
        #判断，无线网卡连接取出该AP的频率值
        result = tmp.connected_AP_Freq(data_wirless['all_ssid'], data_wirless['short_wpa'],
            data_basic['wlan_pc'])
        self.assertEqual(result, 2462)
        log.debug("040\t\tpass")

    def test_041_bridgemode_LANstaticIP_BridgeEncryptionwpa2_stateinfo(self):
        """修改工作模式为桥接模式,内网设置为静态IP模式，桥接ap无线加密为wpa2-检查状态信息页面"""
        tmp = WorkModeBusiness(self.driver)
        #指定有线网卡的固定ip--能够访问ap的webpage
        tmp.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])
        #修改工作模式为bridge模式,内网设置静态IP
        tmp.change_workmode_to_bridge_LANstaticIP(data_basic['DUT_ip'], data_lan['netmask1'],
            data_wirless['bridge_essid'], data_wirless['bridge_encryption'],
            data_wirless['bridge_bssid'], data_wirless['bridge_pwd'], data_wirless['all_ssid'],
            "psk2", data_wirless['short_wpa'], data_basic['ssh_user'], data_basic['ssh_pwd'])
        tmp1 = StateInfoBusiness(self.driver)
        self.driver.refresh()
        self.driver.implicitly_wait(10)
        #获取当前模式
        result1 = tmp1.obtain_AP_current_mode()
        #获取桥接的连接状态
        result2 = tmp1.obtain_WAN_IP_generation()
        #获取信号强度
        result3 = tmp1.obtain_WAN_IP_address()
        self.assertEqual(result1, "网桥模式")
        self.assertEqual(result2, "已连接")
        self.assertIn("dBm", result3)
        log.debug("041\t\tpass")

    def test_042_bridgemode_LANstaticIP_BridgeEncryptionwpa2_wifi_access_internet(self):
        """修改工作模式为桥接模式,内网设置为静态IP模式，桥接ap无线加密为wpa2-无线能访问上级无线路由的ip"""
        tmp = WorkModeBusiness(self.driver)
        #判断运行模式设置后，AP正常：能上网，无线网卡能够连接上AP的SSID
        resutl1, result2 = tmp.check_after_workmode_normal(data_wirless['all_ssid'],
            data_basic['wlan_pc'], "wpa", data_wirless['short_wpa'], data_wirless['bridge_ip'])
        #指定有线网卡的固定ip--能够访问ap的webpage
        tmp.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])
        self.assertEqual(resutl1, 0)
        self.assertIn(data_wirless['all_ssid'], result2)
        log.debug("042\t\tpass")

    # def test_043_bridgemode_LANDHCP_BridgeEncryptionwpa2_wifi_access_internet(self):
    #     """修改工作模式为桥接模式,内网设置为DHCP模式，桥接ap无线加密为wpa2-无线能访问上级无线路由的ip"""
    #     tmp = WorkModeBusiness(self.driver)
    #     #修改工作模式为bridge模式,内网设置动态获取
    #     ap_ip = tmp.change_workmode_to_bridge_LANDHCP(data_wirless['bridge_essid'], data_wirless['bridge_encryption'],
    #         data_wirless['bridge_bssid'], data_wirless['bridge_pwd'], data_wirless['all_ssid'],
    #         "psk2", data_wirless['short_wpa'], data_basic['ssh_user'], data_basic['ssh_pwd'])
    #     #判断运行模式设置后，AP正常：能上网，无线网卡能够连接上AP的SSID
    #     resutl1, result2 = tmp.check_after_workmode_normal(data_wirless['all_ssid'],
    #         data_basic['wlan_pc'], "wpa", data_wirless['short_wpa'], data_wirless['bridge_ip'])
    #     #设置PC的静态IP和桥接的路由的IP端一致
    #     tmp.dhcp_release_wlan(data_basic['lan_pc'])
    #     tmp.set_eth_ip(data_basic['lan_pc'], data_wirless['bridge_static_ip'])
    #     #用dhcp分配的ip地址登录ap的web页面
    #     self.driver.get("http://{}".format(ap_ip))
    #     self.driver.implicitly_wait(20)
    #     #逻辑类对象，建一个实例
    #     Lg = LoginBusiness(self.driver)
    #     #调用实例的登录AP的web界面
    #     Lg.login(data_basic['superUser'], data_basic['super_defalut_pwd'])
    #     #刷新页面重新登录ap页面
    #     Lg.refresh_login_ap()
    #     #修改工作模式为bridge模式,内网设置静态IP
    #     tmp.change_workmode_to_bridge_LANstaticIP(data_basic['DUT_ip'], data_lan['netmask1'],
    #         data_wirless['bridge_essid'], data_wirless['bridge_encryption'],
    #         data_wirless['bridge_bssid'], data_wirless['bridge_pwd'], data_wirless['all_ssid'],
    #         "psk2", data_wirless['short_wpa'], data_basic['ssh_user'], data_basic['ssh_pwd'])
    #     self.assertEqual(resutl1, 0)
    #     self.assertIn(data_wirless['all_ssid'], result2)
    #     log.debug("043\t\tpass")

    def test_043_bridgemode_LANstaticIP_BridgeEncryptionwpa2_APwpa2(self):
        """修改工作模式为桥接模式,内网设置为静态IP模式，桥接ap无线加密为wpa2-DUT无线加密为wpa2"""
        tmp = WorkModeBusiness(self.driver)
        #无线网卡能够连接上AP的SSID
        result = tmp.client_connect_ssid(data_wirless['all_ssid'],
            data_basic['wlan_pc'], "wpa", data_wirless['short_wpa'])
        #指定有线网卡的固定ip--能够访问ap的webpage
        tmp.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])
        self.assertIn(data_wirless['all_ssid'], result)
        log.debug("043\t\tpass")

    def test_044_bridgemode_LANstaticIP_BridgeEncryptionwpa2_APNone(self):
        """修改工作模式为桥接模式,内网设置为静态IP模式，桥接ap无线加密为wpa2-DUT无线加密为None"""
        tmp = WorkModeBusiness(self.driver)
        #修改工作模式为桥接模式,内网设置为静态IP模式，桥接ap无线加密为wpa2-DUT无线加密为None
        tmp.change_workmode_to_bridge_LANstaticIP(data_basic['DUT_ip'], data_lan['netmask1'],
            data_wirless['bridge_essid'], data_wirless['bridge_encryption'],
            data_wirless['bridge_bssid'], data_wirless['bridge_pwd'], data_wirless['all_ssid'],
            "none", "", data_basic['ssh_user'], data_basic['ssh_pwd'])
        tmp1 = StateInfoBusiness(self.driver)
        self.driver.refresh()
        self.driver.implicitly_wait(10)
        #获取当前模式
        result1 = tmp1.obtain_AP_current_mode()
        #获取桥接的连接状态
        result2 = tmp1.obtain_WAN_IP_generation()
        #获取信号强度
        result3 = tmp1.obtain_WAN_IP_address()
        self.assertEqual(result1, "网桥模式")
        self.assertEqual(result2, "已连接")
        self.assertIn("dBm", result3)
        log.debug("044\t\tpass")

    def test_045_bridgemode_LANstaticIP_BridgeEncryptionwpa2_APNone_wifi_access_internet(self):
        """修改工作模式为桥接模式,内网设置为静态IP模式，桥接ap无线加密为wpa2,DUT无线加密为None-无线能访问上级无线路由的ip"""
        tmp = WorkModeBusiness(self.driver)
        #判断运行模式设置后，AP正常：能上网，无线网卡能够连接上AP的SSID
        resutl1, result2 = tmp.check_after_workmode_normal(data_wirless['all_ssid'],
            data_basic['wlan_pc'], "open", internet_ip=data_wirless['bridge_ip'])
        #指定有线网卡的固定ip--能够访问ap的webpage
        tmp.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])
        self.assertEqual(resutl1, 0)
        self.assertIn(data_wirless['all_ssid'], result2)
        log.debug("045\t\tpass")

    def test_046_bridgemode_LANstaticIP_BridgeEncryptionwpa2_APwep64_5ACSII(self):
        """修改工作模式为桥接模式,内网设置为静态IP模式，桥接ap无线加密为wpa2-DUT无线加密为wep64,5位ACSII密码"""
        tmp = WorkModeBusiness(self.driver)
        #修改工作模式为桥接模式,内网设置为静态IP模式，桥接ap无线加密为wpa2-DUT无线加密为wep64,5位ACSII密码
        tmp.change_workmode_to_bridge_LANstaticIP(data_basic['DUT_ip'], data_lan['netmask1'],
            data_wirless['bridge_essid'], data_wirless['bridge_encryption'],
            data_wirless['bridge_bssid'], data_wirless['bridge_pwd'], data_wirless['all_ssid'],
            "wep+shared", data_wirless['wep64'], data_basic['ssh_user'], data_basic['ssh_pwd'])
        tmp1 = StateInfoBusiness(self.driver)
        self.driver.refresh()
        self.driver.implicitly_wait(10)
        #获取当前模式
        result1 = tmp1.obtain_AP_current_mode()
        #获取桥接的连接状态
        result2 = tmp1.obtain_WAN_IP_generation()
        #获取信号强度
        result3 = tmp1.obtain_WAN_IP_address()
        self.assertEqual(result1, "网桥模式")
        self.assertEqual(result2, "已连接")
        self.assertIn("dBm", result3)
        log.debug("046\t\tpass")

    def test_047_bridgemode_LANstaticIP_BridgeEncryptionwpa2_APwep64_5ACSII_wifi_access_internet(self):
        """修改工作模式为桥接模式,内网设置为静态IP模式，桥接ap无线加密为wpa2,DUT无线加密为wep64,5位ACSII密码-\
        无线能访问上级无线路由的ip    \
        BUG:设置DUT为桥接模式时，当DUT为wep加密，桥接的AP为wpa2加密时，无线网卡都无法连接DUT.  \
        这里所有的DUT为wep加密，桥接AP为wpa2加密时，无线网卡都无法连接DUT，其他的wep加密方式验证自动化没添加，\
        如果该问题修复了再添加----BUG"""
        tmp = WorkModeBusiness(self.driver)
        #判断运行模式设置后，AP正常：能上网，无线网卡能够连接上AP的SSID
        resutl1, result2 = tmp.check_after_workmode_normal(data_wirless['all_ssid'],
            data_basic['wlan_pc'], "wep", data_wirless['wep64'],data_wirless['bridge_ip'])
        #指定有线网卡的固定ip--能够访问ap的webpage
        tmp.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])
        self.assertEqual(resutl1, 0)
        self.assertIn(data_wirless['all_ssid'], result2)
        log.debug("047\t\tpass")

    def test_048_bridgemode_LANstaticIP_BridgeEncryptionwpa2_APwep64_10HEX(self):
        """修改工作模式为桥接模式,内网设置为静态IP模式，桥接ap无线加密为wpa2-DUT无线加密为wep64,10位16进制密码"""
        tmp = WorkModeBusiness(self.driver)
        #修改工作模式为桥接模式,内网设置为静态IP模式，桥接ap无线加密为wpa2-DUT无线加密为wep64,10位16进制密码
        tmp.change_workmode_to_bridge_LANstaticIP(data_basic['DUT_ip'], data_lan['netmask1'],
            data_wirless['bridge_essid'], data_wirless['bridge_encryption'],
            data_wirless['bridge_bssid'], data_wirless['bridge_pwd'], data_wirless['all_ssid'],
            "wep+shared", data_wirless['wep64-10'], data_basic['ssh_user'], data_basic['ssh_pwd'])
        tmp1 = StateInfoBusiness(self.driver)
        self.driver.refresh()
        self.driver.implicitly_wait(10)
        #获取当前模式
        result1 = tmp1.obtain_AP_current_mode()
        #获取桥接的连接状态
        result2 = tmp1.obtain_WAN_IP_generation()
        #获取信号强度
        result3 = tmp1.obtain_WAN_IP_address()
        self.assertEqual(result1, "网桥模式")
        self.assertEqual(result2, "已连接")
        self.assertIn("dBm", result3)
        log.debug("048\t\tpass")

    def test_049_bridgemode_LANstaticIP_BridgeEncryptionwpa2_APwep128_13ACSII(self):
        """修改工作模式为桥接模式,内网设置为静态IP模式，桥接ap无线加密为wpa2-DUT无线加密为wep128,13位ACSII密码"""
        tmp = WorkModeBusiness(self.driver)
        #修改工作模式为桥接模式,内网设置为静态IP模式，桥接ap无线加密为wpa2-DUT无线加密为wep128,13位ACSII密码
        tmp.change_workmode_to_bridge_LANstaticIP(data_basic['DUT_ip'], data_lan['netmask1'],
            data_wirless['bridge_essid'], data_wirless['bridge_encryption'],
            data_wirless['bridge_bssid'], data_wirless['bridge_pwd'], data_wirless['all_ssid'],
            "wep+shared", data_wirless['wep128'], data_basic['ssh_user'], data_basic['ssh_pwd'])
        tmp1 = StateInfoBusiness(self.driver)
        self.driver.refresh()
        self.driver.implicitly_wait(10)
        #获取当前模式
        result1 = tmp1.obtain_AP_current_mode()
        #获取桥接的连接状态
        result2 = tmp1.obtain_WAN_IP_generation()
        #获取信号强度
        result3 = tmp1.obtain_WAN_IP_address()
        self.assertEqual(result1, "网桥模式")
        self.assertEqual(result2, "已连接")
        self.assertIn("dBm", result3)
        log.debug("049\t\tpass")

    def test_050_bridgemode_LANstaticIP_BridgeEncryptionwpa2_APwep128_26HEX(self):
        """修改工作模式为桥接模式,内网设置为静态IP模式，桥接ap无线加密为wpa2-DUT无线加密为wep128,26位16进制密码"""
        tmp = WorkModeBusiness(self.driver)
        #修改工作模式为桥接模式,内网设置为静态IP模式，桥接ap无线加密为wpa2-DUT无线加密为wep128,26位16进制密码
        tmp.change_workmode_to_bridge_LANstaticIP(data_basic['DUT_ip'], data_lan['netmask1'],
            data_wirless['bridge_essid'], data_wirless['bridge_encryption'],
            data_wirless['bridge_bssid'], data_wirless['bridge_pwd'], data_wirless['all_ssid'],
            "wep+shared", data_wirless['wep128-26'], data_basic['ssh_user'], data_basic['ssh_pwd'])
        tmp1 = StateInfoBusiness(self.driver)
        self.driver.refresh()
        self.driver.implicitly_wait(10)
        #获取当前模式
        result1 = tmp1.obtain_AP_current_mode()
        #获取桥接的连接状态
        result2 = tmp1.obtain_WAN_IP_generation()
        #获取信号强度
        result3 = tmp1.obtain_WAN_IP_address()
        self.assertEqual(result1, "网桥模式")
        self.assertEqual(result2, "已连接")
        self.assertIn("dBm", result3)
        log.debug("050\t\tpass")

    def test_051_bridgemode_LANstaticIP_BridgeEncryptionNone_APwpa2_stateinfo(self):
        """修改工作模式为桥接模式,内网设置为静态IP模式，桥接ap无线加密为none,DUT为wpa2-检查状态信息页面"""
        #登录桥接路由的web端，修改桥接路由的无线加密为none
        tmp1 = WirelessSettingsBusiness(self.driver)
        tmp1.change_bridge_AP_wifi_encryption_pwd(data_wirless['bridge_static_ip'],
            data_wirless['bridge_ip'], "none", "")

        tmp = WorkModeBusiness(self.driver)
        #设置PC的静态IP,能够访问DUT的webpage
        tmp.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])
        #登录DUT的webpage
        self.driver.get(data_basic['DUT_web'])
        self.driver.implicitly_wait(20)
        #逻辑类对象，建一个实例
        Lg = LoginBusiness(self.driver)
        #调用实例的登录AP的web界面
        Lg.login(data_basic['superUser'], data_basic['super_defalut_pwd'])
        #刷新页面重新登录ap页面
        Lg.refresh_login_ap()

        #修改工作模式为bridge模式,内网设置静态IP,桥接ap无线加密为none,DUT为wpa2
        tmp.change_workmode_to_bridge_LANstaticIP(data_basic['DUT_ip'], data_lan['netmask1'],
            data_wirless['bridge_essid'], "none",
            data_wirless['bridge_bssid'], "", data_wirless['all_ssid'],
            "psk2", data_wirless['short_wpa'], data_basic['ssh_user'], data_basic['ssh_pwd'])
        tmp1 = StateInfoBusiness(self.driver)
        self.driver.refresh()
        self.driver.implicitly_wait(10)
        #获取当前模式
        result1 = tmp1.obtain_AP_current_mode()
        #获取桥接的连接状态
        result2 = tmp1.obtain_WAN_IP_generation()
        #获取信号强度
        result3 = tmp1.obtain_WAN_IP_address()
        self.assertEqual(result1, "网桥模式")
        self.assertEqual(result2, "已连接")
        self.assertIn("dBm", result3)
        log.debug("051\t\tpass")

    def test_052_bridgemode_LANstaticIP_BridgeEncryptionNone_APwpa2_wifi_access_internet(self):
        """修改工作模式为桥接模式,内网设置为静态IP模式，桥接ap无线加密为none,DUT为wpa2-无线能访问上级无线路由的ip"""
        tmp = WorkModeBusiness(self.driver)
        #判断运行模式设置后，AP正常：能上网，无线网卡能够连接上AP的SSID
        resutl1, result2 = tmp.check_after_workmode_normal(data_wirless['all_ssid'],
            data_basic['wlan_pc'], "wpa", data_wirless['short_wpa'], data_wirless['bridge_ip'])
        #指定有线网卡的固定ip--能够访问ap的webpage
        tmp.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])
        self.assertEqual(resutl1, 0)
        self.assertIn(data_wirless['all_ssid'], result2)
        log.debug("052\t\tpass")

    def test_053_bridgemode_LANstaticIP_BridgeEncryptionwep_APwpa2_stateinfo(self):
        """修改工作模式为桥接模式,内网设置为静态IP模式，桥接ap无线加密为wep,DUT为wpa2-检查状态信息页面"""
        #登录桥接路由的web端，修改桥接路由的无线加密为wep
        tmp1 = WirelessSettingsBusiness(self.driver)
        tmp1.change_bridge_AP_wifi_encryption_pwd(data_wirless['bridge_static_ip'],
            data_wirless['bridge_ip'], "wep+shared", data_wirless['wep64'])

        tmp = WorkModeBusiness(self.driver)
        #设置PC的静态IP,能够访问DUT的webpage
        tmp.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])
        #登录DUT的webpage
        self.driver.get(data_basic['DUT_web'])
        self.driver.implicitly_wait(20)
        #逻辑类对象，建一个实例
        Lg = LoginBusiness(self.driver)
        #调用实例的登录AP的web界面
        Lg.login(data_basic['superUser'], data_basic['super_defalut_pwd'])
        #刷新页面重新登录ap页面
        Lg.refresh_login_ap()

        #修改工作模式为bridge模式,内网设置静态IP,桥接ap无线加密为wep,DUT为wpa2
        tmp.change_workmode_to_bridge_LANstaticIP(data_basic['DUT_ip'], data_lan['netmask1'],
            data_wirless['bridge_essid'], "wep+shared",
            data_wirless['bridge_bssid'], data_wirless['wep64'], data_wirless['all_ssid'],
            "psk2", data_wirless['short_wpa'], data_basic['ssh_user'], data_basic['ssh_pwd'])
        tmp1 = StateInfoBusiness(self.driver)
        self.driver.refresh()
        self.driver.implicitly_wait(10)
        #获取当前模式
        result1 = tmp1.obtain_AP_current_mode()
        #获取桥接的连接状态
        result2 = tmp1.obtain_WAN_IP_generation()
        #获取信号强度
        result3 = tmp1.obtain_WAN_IP_address()
        self.assertEqual(result1, "网桥模式")
        self.assertEqual(result2, "已连接")
        self.assertIn("dBm", result3)
        log.debug("053\t\tpass")

    def test_054_bridgemode_LANstaticIP_BridgeEncryptionwep_APwpa2_wifi_access_internet(self):
        """修改工作模式为桥接模式,内网设置为静态IP模式，桥接ap无线加密为wep,DUT为wpa2-无线能访问上级无线路由的ip"""
        tmp = WorkModeBusiness(self.driver)
        #判断运行模式设置后，AP正常：能上网，无线网卡能够连接上AP的SSID
        resutl1, result2 = tmp.check_after_workmode_normal(data_wirless['all_ssid'],
            data_basic['wlan_pc'], "wpa", data_wirless['short_wpa'], data_wirless['bridge_ip'])
        #指定有线网卡的固定ip--能够访问ap的webpage
        tmp.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])
        self.assertEqual(resutl1, 0)
        self.assertIn(data_wirless['all_ssid'], result2)
        log.debug("054\t\tpass")

    def test_055_clientmode_LANstaticIP_BridgeEncryptionwpa2_stateinfo(self):
        """修改工作模式为客户端模式,内网设置为静态IP模式，桥接ap无线加密为wpa2-检查状态信息页面"""
        #登录桥接路由的web端，修改桥接路由的无线加密为wpa2
        tmp1 = WirelessSettingsBusiness(self.driver)
        tmp1.change_bridge_AP_wifi_encryption_pwd(data_wirless['bridge_static_ip'],
            data_wirless['bridge_ip'], "psk2", data_wirless['short_wpa'])

        tmp = WorkModeBusiness(self.driver)
        #设置PC的静态IP,能够访问DUT的webpage
        tmp.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])
        #登录DUT的webpage
        self.driver.get(data_basic['DUT_web'])
        self.driver.implicitly_wait(20)
        #逻辑类对象，建一个实例
        Lg = LoginBusiness(self.driver)
        #调用实例的登录AP的web界面
        Lg.login(data_basic['superUser'], data_basic['super_defalut_pwd'])
        #刷新页面重新登录ap页面
        Lg.refresh_login_ap()

        #修改工作模式为client模式,内网设置静态IP,桥接ap无线加密为wpa2
        tmp.change_workmode_to_client_LANstaticIP(data_basic['DUT_ip'], data_lan['netmask1'],
            data_wirless['bridge_essid'], data_wirless['bridge_encryption'],
            data_wirless['bridge_bssid'], data_wirless['bridge_pwd'],
            data_basic['ssh_user'], data_basic['ssh_pwd'])
        tmp1 = StateInfoBusiness(self.driver)
        self.driver.refresh()
        self.driver.implicitly_wait(10)
        #获取当前模式
        result1 = tmp1.obtain_AP_current_mode()
        #获取桥接的连接状态
        result2 = tmp1.obtain_WAN_IP_generation()
        #获取信号强度
        result3 = tmp1.obtain_WAN_IP_address()
        self.assertEqual(result1, "客户端模式")
        self.assertEqual(result2, "已连接")
        self.assertIn("dBm", result3)
        log.debug("055\t\tpass")

    def test_056_clientmode_LANstaticIP_BridgeEncryptionwpa2_lan_access_internet(self):
        """修改工作模式为客户端模式,内网设置为静态IP模式，桥接ap无线加密为wpa2-有线能访问上级无线路由的ip"""
        tmp = WorkModeBusiness(self.driver)
        #判断client模式设置后，AP正常：PC的有线能上网，无线网卡不能够扫描到原来AP的SSID
        resutl1, result2 = tmp.check_clientmode_normal(data_wirless['all_ssid'],
            data_basic['lan_pc'], data_basic['wlan_pc'], data_wirless['bridge_ip'])
        #指定有线网卡的固定ip--能够访问ap的webpage
        tmp.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])
        self.assertEqual(resutl1, 0)
        self.assertFalse(result2)
        log.debug("056\t\tpass")

    # def test_057_clientmode_LANDHCP_BridgeEncryptionwpa2_wifi_access_internet(self):
    #     """修改工作模式为客户端模式,内网设置为DHCP模式，桥接ap无线加密为wpa2-无线能访问上级无线路由的ip"""
    #     tmp = WorkModeBusiness(self.driver)
    #     #修改工作模式为client模式,内网设置动态获取
    #     ap_ip = tmp.change_workmode_to_client_LANDHCP(data_wirless['bridge_essid'], data_wirless['bridge_encryption'],
    #         data_wirless['bridge_bssid'], data_wirless['bridge_pwd'],
    #         data_basic['ssh_user'], data_basic['ssh_pwd'])
    #     #判断client模式设置后，AP正常：PC的有线能上网，无线网卡不能够扫描到原来AP的SSID
    #     resutl1, result2 = tmp.check_clientmode_normal(data_wirless['all_ssid'],
    #         data_basic['lan_pc'], data_basic['wlan_pc'], data_wirless['bridge_ip'])
    #     #设置PC的静态IP和桥接的路由的IP端一致
    #     tmp.dhcp_release_wlan(data_basic['lan_pc'])
    #     tmp.set_eth_ip(data_basic['lan_pc'], data_wirless['bridge_static_ip'])
    #     #用dhcp分配的ip地址登录ap的web页面
    #     self.driver.get("http://{}".format(ap_ip))
    #     self.driver.implicitly_wait(20)
    #     #逻辑类对象，建一个实例
    #     Lg = LoginBusiness(self.driver)
    #     #调用实例的登录AP的web界面
    #     Lg.login(data_basic['superUser'], data_basic['super_defalut_pwd'])
    #     #刷新页面重新登录ap页面
    #     Lg.refresh_login_ap()
    #     #修改工作模式为client模式,内网设置静态IP,桥接ap无线加密为wpa2
    #     tmp.change_workmode_to_client_LANstaticIP(data_basic['DUT_ip'], data_lan['netmask1'],
    #         data_wirless['bridge_essid'], data_wirless['bridge_encryption'],
    #         data_wirless['bridge_bssid'], data_wirless['bridge_pwd'],
    #         data_basic['ssh_user'], data_basic['ssh_pwd'])
    #     self.assertEqual(resutl1, 0)
    #     self.assertFalse(result2)
    #     log.debug("057\t\tpass")

    def test_057_clientmode_LANstaticIP_BridgeEncryptionNone_stateinfo(self):
        """修改工作模式为客户端模式,内网设置为静态IP模式，桥接ap无线加密为none-检查状态信息页面"""
        #登录桥接路由的web端，修改桥接路由的无线加密为none
        tmp1 = WirelessSettingsBusiness(self.driver)
        tmp1.change_bridge_AP_wifi_encryption_pwd(data_wirless['bridge_static_ip'],
            data_wirless['bridge_ip'], "none", "")

        tmp = WorkModeBusiness(self.driver)
        #设置PC的静态IP,能够访问DUT的webpage
        tmp.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])
        #登录DUT的webpage
        self.driver.get(data_basic['DUT_web'])
        self.driver.implicitly_wait(20)
        #逻辑类对象，建一个实例
        Lg = LoginBusiness(self.driver)
        #调用实例的登录AP的web界面
        Lg.login(data_basic['superUser'], data_basic['super_defalut_pwd'])
        #刷新页面重新登录ap页面
        Lg.refresh_login_ap()

        #修改工作模式为client模式,内网设置静态IP,桥接ap无线加密为none
        tmp.change_workmode_to_client_LANstaticIP(data_basic['DUT_ip'], data_lan['netmask1'],
            data_wirless['bridge_essid'], "none",
            data_wirless['bridge_bssid'], "",
            data_basic['ssh_user'], data_basic['ssh_pwd'])
        tmp1 = StateInfoBusiness(self.driver)
        self.driver.refresh()
        self.driver.implicitly_wait(10)
        #获取当前模式
        result1 = tmp1.obtain_AP_current_mode()
        #获取桥接的连接状态
        result2 = tmp1.obtain_WAN_IP_generation()
        #获取信号强度
        result3 = tmp1.obtain_WAN_IP_address()
        self.assertEqual(result1, "客户端模式")
        self.assertEqual(result2, "已连接")
        self.assertIn("dBm", result3)
        log.debug("057\t\tpass")

    def test_058_clientmode_LANstaticIP_BridgeEncryptionNone_lan_access_internet(self):
        """修改工作模式为客户端模式,内网设置为静态IP模式，桥接ap无线加密为None-有线能访问上级无线路由的ip"""
        tmp = WorkModeBusiness(self.driver)
        #判断client模式设置后，AP正常：PC的有线能上网，无线网卡不能够扫描到原来AP的SSID
        resutl1, result2 = tmp.check_clientmode_normal(data_wirless['all_ssid'],
            data_basic['lan_pc'], data_basic['wlan_pc'], data_wirless['bridge_ip'])
        #指定有线网卡的固定ip--能够访问ap的webpage
        tmp.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])
        self.assertEqual(resutl1, 0)
        self.assertFalse(result2)
        log.debug("058\t\tpass")

    def test_059_clientmode_LANstaticIP_BridgeEncryptionwep_stateinfo(self):
        """修改工作模式为客户端模式,内网设置为静态IP模式，桥接ap无线加密为wep-检查状态信息页面"""
        #登录桥接路由的web端，修改桥接路由的无线加密为wep
        tmp1 = WirelessSettingsBusiness(self.driver)
        tmp1.change_bridge_AP_wifi_encryption_pwd(data_wirless['bridge_static_ip'],
            data_wirless['bridge_ip'], "wep+shared", data_wirless['wep64'])

        tmp = WorkModeBusiness(self.driver)
        #设置PC的静态IP,能够访问DUT的webpage
        tmp.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])
        #登录DUT的webpage
        self.driver.get(data_basic['DUT_web'])
        self.driver.implicitly_wait(20)
        #逻辑类对象，建一个实例
        Lg = LoginBusiness(self.driver)
        #调用实例的登录AP的web界面
        Lg.login(data_basic['superUser'], data_basic['super_defalut_pwd'])
        #刷新页面重新登录ap页面
        Lg.refresh_login_ap()

        #修改工作模式为client模式,内网设置静态IP,桥接ap无线加密为wep
        tmp.change_workmode_to_client_LANstaticIP(data_basic['DUT_ip'], data_lan['netmask1'],
            data_wirless['bridge_essid'], "wep+shared",
            data_wirless['bridge_bssid'], data_wirless['wep64'],
            data_basic['ssh_user'], data_basic['ssh_pwd'])
        tmp1 = StateInfoBusiness(self.driver)
        self.driver.refresh()
        self.driver.implicitly_wait(10)
        #获取当前模式
        result1 = tmp1.obtain_AP_current_mode()
        #获取桥接的连接状态
        result2 = tmp1.obtain_WAN_IP_generation()
        #获取信号强度
        result3 = tmp1.obtain_WAN_IP_address()
        self.assertEqual(result1, "客户端模式")
        self.assertEqual(result2, "已连接")
        self.assertIn("dBm", result3)
        log.debug("059\t\tpass")

    def test_060_clientmode_LANstaticIP_BridgeEncryptionwep_lan_access_internet(self):
        """修改工作模式为客户端模式,内网设置为静态IP模式，桥接ap无线加密为wep-有线能访问上级无线路由的ip"""
        tmp = WorkModeBusiness(self.driver)
        #判断client模式设置后，AP正常：PC的有线能上网，无线网卡不能够扫描到原来AP的SSID
        resutl1, result2 = tmp.check_clientmode_normal(data_wirless['all_ssid'],
            data_basic['lan_pc'], data_basic['wlan_pc'], data_wirless['bridge_ip'])
        #指定有线网卡的固定ip--能够访问ap的webpage
        tmp.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])
        self.assertEqual(resutl1, 0)
        self.assertFalse(result2)
        log.debug("060\t\tpass")

    def test_061_apmode_LANstaticIP_APwpa2_stateinfo(self):
        """修改工作模式为AP模式,内网设置为静态IP模式,DUT无线加密为wpa2-检查状态信息页面    \
        BUG：AP模式下，在状态信息页面上内网信息显示的是外网信息----BUG"""
        #登录桥接路由的web端，修改桥接路由的无线加密为wpa2
        tmp1 = WirelessSettingsBusiness(self.driver)
        tmp1.change_bridge_AP_wifi_encryption_pwd(data_wirless['bridge_static_ip'],
            data_wirless['bridge_ip'], "psk2", data_wirless['short_wpa'])

        tmp = WorkModeBusiness(self.driver)
        #设置PC的静态IP,能够访问DUT的webpage
        tmp.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])
        #登录DUT的webpage
        self.driver.get(data_basic['DUT_web'])
        self.driver.implicitly_wait(20)
        #逻辑类对象，建一个实例
        Lg = LoginBusiness(self.driver)
        #调用实例的登录AP的web界面
        Lg.login(data_basic['superUser'], data_basic['super_defalut_pwd'])
        #刷新页面重新登录ap页面
        Lg.refresh_login_ap()

        #修改工作模式为AP模式,内网设置静态IP
        tmp.change_workmode_to_ap_LANstaticIP(data_basic['DUT_ip'],
            data_lan['netmask1'], data_wirless['all_ssid'], "psk2",
            data_wirless['short_wpa'], "HT20")
        tmp1 = StateInfoBusiness(self.driver)
        self.driver.refresh()
        self.driver.implicitly_wait(10)
        #获取当前模式
        result1 = tmp1.obtain_AP_current_mode()
        #获取内网IP获取方式
        result2 = tmp1.obtain_WAN_IP_generation()
        #获取IP地址
        result3 = tmp1.obtain_WAN_IP_address()
        self.assertEqual(result1, "AP模式")
        self.assertEqual(result2, "静态IP")
        self.assertEqual(data_basic['DUT_ip'], result3)
        log.debug("061\t\tpass")

    def test_062_apmode_LANstaticIP_APwpa2_lan_access_internet(self):
        """修改工作模式为AP模式,内网设置为静态IP模式,DUT无线加密为wpa2-有线能访问internet"""
        tmp = WorkModeBusiness(self.driver)
        #判断AP模式设置后，AP正常：PC的有线能上网
        result = tmp.check_apmode_normal(data_basic['PC_pwd'], data_basic['lan_pc'],
            data_wan['static_IP'], data_wan['netmask'], data_wan['gateway'])
        #指定有线网卡的固定ip--能够访问ap的webpage
        tmp.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])
        self.assertEqual(result, 0)
        log.debug("062\t\tpass")

    def test_063_apmode_LANstaticIP_APwpa2(self):
        """修改工作模式为AP模式,内网设置为静态IP模式,DUT无线加密为wpa2-无线网卡能连接"""
        tmp = WorkModeBusiness(self.driver)
        #无线网卡能够连接上AP的SSID
        result = tmp.client_connect_ssid(data_wirless['all_ssid'],
            data_basic['wlan_pc'], "wpa", data_wirless['short_wpa'])
        #指定有线网卡的固定ip--能够访问ap的webpage
        tmp.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])
        self.assertIn(data_wirless['all_ssid'], result)
        log.debug("063\t\tpass")

    def test_064_apmode_LANstaticIP_APwpa2_wifi_access_internet(self):
        """修改工作模式为AP模式,内网设置为静态IP模式,DUT无线加密为wpa2-无线能访问internet    \
        BUG:AP模式下，使用无线网卡连接AP上网，网络非常卡，ping上级网关也无法ping通----BUG"""
        tmp = WorkModeBusiness(self.driver)
        #判断运行模式设置后，AP正常：能上网，无线网卡能够连接上AP的SSID
        resutl1, result2 = tmp.check_apmode_after_workmode_normal(data_wirless['all_ssid'],
            data_basic['wlan_pc'], "wpa", data_basic['PC_pwd'], data_wan['static_IP'],
            data_wan['netmask'], data_wan['gateway'], data_wirless['short_wpa'])
        #指定有线网卡的固定ip--能够访问ap的webpage
        tmp.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])
        self.assertEqual(resutl1, 0)
        self.assertIn(data_wirless['all_ssid'], result2)
        log.debug("064\t\tpass")

    def test_065_apmode_LANstaticIP_APNone_stateinfo(self):
        """修改工作模式为AP模式,内网设置为静态IP模式,DUT无线加密为None-检查状态信息页面    \
        BUG：AP模式下，在状态信息页面上内网信息显示的是外网信息----BUG"""
        tmp = WorkModeBusiness(self.driver)
        #修改工作模式为AP模式,内网设置静态IP
        tmp.change_workmode_to_ap_LANstaticIP(data_basic['DUT_ip'],
            data_lan['netmask1'], data_wirless['all_ssid'], "none",
            "", "HT20")
        tmp1 = StateInfoBusiness(self.driver)
        self.driver.refresh()
        self.driver.implicitly_wait(10)
        #获取当前模式
        result1 = tmp1.obtain_AP_current_mode()
        #获取内网IP获取方式
        result2 = tmp1.obtain_WAN_IP_generation()
        #获取IP地址
        result3 = tmp1.obtain_WAN_IP_address()
        self.assertEqual(result1, "AP模式")
        self.assertEqual(result2, "静态IP")
        self.assertEqual(data_basic['DUT_ip'], result3)
        log.debug("065\t\tpass")

    def test_066_apmode_LANstaticIP_APNone_lan_access_internet(self):
        """修改工作模式为AP模式,内网设置为静态IP模式,DUT无线加密为None-有线能访问internet"""
        tmp = WorkModeBusiness(self.driver)
        #判断AP模式设置后，AP正常：PC的有线能上网
        result = tmp.check_apmode_normal(data_basic['PC_pwd'], data_basic['lan_pc'],
            data_wan['static_IP'], data_wan['netmask'], data_wan['gateway'])
        #指定有线网卡的固定ip--能够访问ap的webpage
        tmp.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])
        self.assertEqual(result, 0)
        log.debug("066\t\tpass")

    def test_067_apmode_LANstaticIP_APNone(self):
        """修改工作模式为AP模式,内网设置为静态IP模式,DUT无线加密为None-无线网卡能连接"""
        tmp = WorkModeBusiness(self.driver)
        #无线网卡能够连接上AP的SSID
        result = tmp.client_connect_ssid(data_wirless['all_ssid'],
            data_basic['wlan_pc'], "open")
        #指定有线网卡的固定ip--能够访问ap的webpage
        tmp.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])
        self.assertIn(data_wirless['all_ssid'], result)
        log.debug("067\t\tpass")

    def test_068_apmode_LANstaticIP_APNone_wifi_access_internet(self):
        """修改工作模式为AP模式,内网设置为静态IP模式,DUT无线加密为None-无线能访问internet    \
        BUG:AP模式下，使用无线网卡连接AP上网，网络非常卡，ping上级网关也无法ping通----BUG"""
        tmp = WorkModeBusiness(self.driver)
        #判断运行模式设置后，AP正常：能上网，无线网卡能够连接上AP的SSID
        resutl1, result2 = tmp.check_apmode_after_workmode_normal(data_wirless['all_ssid'],
            data_basic['wlan_pc'], "open", data_basic['PC_pwd'], data_wan['static_IP'],
            data_wan['netmask'], data_wan['gateway'])
        #指定有线网卡的固定ip--能够访问ap的webpage
        tmp.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])
        self.assertEqual(resutl1, 0)
        self.assertIn(data_wirless['all_ssid'], result2)
        log.debug("068\t\tpass")

    def test_069_apmode_LANstaticIP_APWEP_stateinfo(self):
        """修改工作模式为AP模式,内网设置为静态IP模式,DUT无线加密为wep-检查状态信息页面    \
        BUG：AP模式下，在状态信息页面上内网信息显示的是外网信息----BUG"""
        tmp = WorkModeBusiness(self.driver)
        #修改工作模式为AP模式,内网设置静态IP
        tmp.change_workmode_to_ap_LANstaticIP(data_basic['DUT_ip'],
            data_lan['netmask1'], data_wirless['all_ssid'], "wep+shared",
            data_wirless['wep64'], "HT20")
        tmp1 = StateInfoBusiness(self.driver)
        self.driver.refresh()
        self.driver.implicitly_wait(10)
        #获取当前模式
        result1 = tmp1.obtain_AP_current_mode()
        #获取内网IP获取方式
        result2 = tmp1.obtain_WAN_IP_generation()
        #获取IP地址
        result3 = tmp1.obtain_WAN_IP_address()
        self.assertEqual(result1, "AP模式")
        self.assertEqual(result2, "静态IP")
        self.assertEqual(data_basic['DUT_ip'], result3)
        log.debug("069\t\tpass")

    def test_070_apmode_LANstaticIP_APWEP_lan_access_internet(self):
        """修改工作模式为AP模式,内网设置为静态IP模式,DUT无线加密为WEP-有线能访问internet"""
        tmp = WorkModeBusiness(self.driver)
        #判断AP模式设置后，AP正常：PC的有线能上网
        result = tmp.check_apmode_normal(data_basic['PC_pwd'], data_basic['lan_pc'],
            data_wan['static_IP'], data_wan['netmask'], data_wan['gateway'])
        #指定有线网卡的固定ip--能够访问ap的webpage
        tmp.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])
        self.assertEqual(result, 0)
        log.debug("070\t\tpass")

    def test_071_apmode_LANstaticIP_APWEP(self):
        """修改工作模式为AP模式,内网设置为静态IP模式,DUT无线加密为wep-无线网卡能连接    \
        BUG:设置DUT为AP模式时，当DUT为wep加密，无线网卡都无法连接DUT----BUG"""
        tmp = WorkModeBusiness(self.driver)
        #无线网卡能够连接上AP的SSID
        result = tmp.client_connect_ssid(data_wirless['all_ssid'],
            data_basic['wlan_pc'], "wep",
            data_wirless['wep64'])
        #指定有线网卡的固定ip--能够访问ap的webpage
        tmp.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])
        self.assertIn(data_wirless['all_ssid'], result)
        log.debug("071\t\tpass")

    def test_072_apmode_LANstaticIP_APWEP_wifi_access_internet(self):
        """修改工作模式为AP模式,内网设置为静态IP模式,DUT无线加密为WEP-无线能访问internet    \
        BUG:AP模式下，使用无线网卡连接AP上网，网络非常卡，ping上级网关也无法ping通----BUG"""
        tmp = WorkModeBusiness(self.driver)
        #判断运行模式设置后，AP正常：能上网，无线网卡能够连接上AP的SSID
        resutl1, result2 = tmp.check_apmode_after_workmode_normal(data_wirless['all_ssid'],
            data_basic['wlan_pc'], "wep", data_basic['PC_pwd'], data_wan['static_IP'],
            data_wan['netmask'], data_wan['gateway'], data_wirless['wep64'])

        #指定有线网卡的固定ip--能够访问ap的webpage
        tmp.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])
        #刷新页面重新登录ap页面
        Lg = LoginBusiness(self.driver)
        Lg.refresh_login_ap()
        #修改工作模式为路由模式,外网设置dhcp模式
        tmp.change_workmode_to_route_WANdhcp(data_wirless['all_ssid'],
            "psk2", data_wirless['short_wpa'], "HT40", "auto")
        #client重新获取ip
        tmp.dhcp_release_wlan(data_basic['lan_pc'])
        tmp.dhcp_wlan(data_basic['lan_pc'])
        tmp.disconnect_ap()
        self.assertEqual(resutl1, 0)
        self.assertIn(data_wirless['all_ssid'], result2)
        log.debug("072\t\tpass")







    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
