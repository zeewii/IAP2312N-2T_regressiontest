#coding=utf-8
#作者：曾祥卫
#时间：2018.09.19
#描述：用例层代码，调用systemupgrade_business

import unittest, time, os
from selenium import webdriver
from login.login_business import LoginBusiness
from systemtools.systemupgrade.systemupgrade_business import SystemUpgradeBusiness
from systemtools.configupdate.configupdate_business import ConfigUpdateBusiness
from workmode.workmode_business import WorkModeBusiness
from stateinfo.stateinfo_business import StateInfoBusiness
from network.wirelesssettings.wirelesssettings_business import WirelessSettingsBusiness
from network.wansettings.wansettings_business import WanSettingsBusiness
from connect.ssh import SSH
from data import data
from data.logfile import Log

data_basic = data.data_basic()
data_login = data.data_login()
data_wirless = data.data_wireless()
data_wan = data.data_wan()
data_lan = data.data_lan()

log = Log("SystemUpgrade")
AP_model = "IAP2312N-2T"

class TestSystemUpgrade(unittest.TestCase):
    """测试系统升级的用例集(Duration:1.35h)"""
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


    def test_001_system_downgrade(self):
        """系统降级"""
        #首先启用无线网卡
        tmp = SystemUpgradeBusiness(self.driver)
        tmp.wlan_enable(data_basic['wlan_pc'])
        #刷新页面重新登录ap页面
        Lg = LoginBusiness(self.driver)
        Lg.refresh_login_ap()
        #把AP恢复出厂配置
        tmp1 = ConfigUpdateBusiness(self.driver)
        tmp1.restore_AP_factory()

        #固件的http路径：
        PATH_http = data_basic['old_version_http']
        #从http下载固件
        tmp.get_client_cmd_result("wget %s"%PATH_http)
        #选择固件路径，降级固件
        PATH = os.path.join(os.getcwd(), AP_model+'-'+data_basic['old_version']+'.bin')
        print(PATH)
        #重新登录AP
        #逻辑类对象，建一个实例
        Lg = LoginBusiness(self.driver)
        #调用实例的登录AP的web界面
        Lg.login(data_basic['superUser'], data_basic['super_defalut_pwd'])
        #刷新页面重新登录ap页面
        Lg.refresh_login_ap()
        tmp.upgrade_system(PATH)
        #重新登录，并检查固件版本
        Lg.refresh_login_ap()
        result = tmp.check_system_version(data_basic['old_version'])
        # #删除下载固件
        # os.unlink(PATH)
        self.assertTrue(result)
        log.debug("001\t\tpass")

    def test_002_system_upgrade(self):
        """系统升级"""
        tmp = SystemUpgradeBusiness(self.driver)
        #固件的http路径：
        PATH_http = data_basic['new_version_http']
        #从http下载固件
        tmp.get_client_cmd_result("wget %s"%PATH_http)
        #选择固件路径，升级固件
        PATH = os.path.join(os.getcwd(), AP_model+'-'+data_basic['new_version']+'.bin')
        print(PATH)
        tmp.upgrade_system(PATH)
        #重新登录，并检查固件版本
        Lg = LoginBusiness(self.driver)
        Lg.refresh_login_ap()
        result = tmp.check_system_version(data_basic['new_version'])
        # #删除下载固件
        # os.unlink(PATH)
        self.assertTrue(result)
        log.debug("002\t\tpass")

    #路由模式下，修改配置后，系统降级，检查配置
    def test_003_routemode_system_downgrade_check_config(self):
        """路由模式下，修改配置后，系统降级，检查配置"""
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
        #选择固件路径，降级固件
        PATH = os.path.join(os.getcwd(), AP_model+'-'+data_basic['old_version']+'.bin')
        print(PATH)
        tmp = SystemUpgradeBusiness(self.driver)
        tmp.upgrade_system(PATH)
        #刷新页面重新登录ap页面
        Lg.refresh_login_ap()
        tmp1 = StateInfoBusiness(self.driver)
        #获取当前模式
        result1 = tmp1.obtain_AP_current_mode()
        #获取外网的IP获取方式
        result2 = tmp1.obtain_WAN_IP_generation()
        #获取IP地址
        result3 = tmp1.obtain_WAN_IP_address()
        #判断ssid是否恢复
        tmp2 = WirelessSettingsBusiness(self.driver)
        result4 = tmp2.get_first_ssid(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'])
        #判断wan口是否是静态IP
        tmp3 = WanSettingsBusiness(self.driver)
        result5 = tmp3.get_wan_way(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'])
        #检查固件版本
        result6 = tmp.check_system_version(data_basic['old_version'])
        self.assertEqual(result1, "路由模式")
        self.assertEqual(result2, "静态IP")
        self.assertEqual(data_wan['static_IP'], result3)
        self.assertIn(data_wirless['all_ssid'], result4)
        self.assertIn("static", result5)
        self.assertTrue(result6)
        log.debug("003\t\tpass")

    #路由模式下，系统升级，检查配置
    def test_004_routemode_system_upgrade_check_config(self):
        """路由模式下，系统升级，检查配置"""
        tmp = SystemUpgradeBusiness(self.driver)
        #选择固件路径，升级固件
        PATH = os.path.join(os.getcwd(), AP_model+'-'+data_basic['new_version']+'.bin')
        print(PATH)
        tmp.upgrade_system(PATH)
        Lg = LoginBusiness(self.driver)
        Lg.refresh_login_ap()
        tmp1 = StateInfoBusiness(self.driver)
        #获取当前模式
        result1 = tmp1.obtain_AP_current_mode()
        #获取外网的IP获取方式
        result2 = tmp1.obtain_WAN_IP_generation()
        #获取IP地址
        result3 = tmp1.obtain_WAN_IP_address()
        #判断ssid是否恢复
        tmp2 = WirelessSettingsBusiness(self.driver)
        result4 = tmp2.get_first_ssid(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'])
        #判断wan口是否是静态IP
        tmp3 = WanSettingsBusiness(self.driver)
        result5 = tmp3.get_wan_way(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'])
        #检查固件版本
        result6 = tmp.check_system_version(data_basic['new_version'])
        self.assertEqual(result1, "路由模式")
        self.assertEqual(result2, "静态IP")
        self.assertEqual(data_wan['static_IP'], result3)
        self.assertIn(data_wirless['all_ssid'], result4)
        self.assertIn("static", result5)
        self.assertTrue(result6)
        log.debug("004\t\tpass")

    #ap模式下，修改配置后，系统降级，检查配置
    def test_005_apmode_system_downgrade_check_config(self):
        """ap模式下，修改配置后，系统降级，检查配置"""
        tmp1 = WorkModeBusiness(self.driver)
        #设置PC的静态IP,能够访问DUT的webpage
        tmp1.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])
        #修改工作模式为AP模式,内网设置静态IP
        tmp1.change_workmode_to_ap_LANstaticIP(data_basic['DUT_ip'],
            data_lan['netmask1'], data_wirless['all_ssid'], "psk2",
            data_wirless['short_wpa'], "HT20")
        time.sleep(30)
        #逻辑类对象，建一个实例
        Lg = LoginBusiness(self.driver)
        #刷新页面重新登录ap页面
        Lg.refresh_login_ap()
        #选择固件路径，降级固件
        PATH = os.path.join(os.getcwd(), AP_model+'-'+data_basic['old_version']+'.bin')
        print(PATH)
        tmp = SystemUpgradeBusiness(self.driver)
        tmp.upgrade_system(PATH)
        #设置PC的静态IP,能够访问DUT的webpage
        tmp.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])
        #刷新页面重新登录ap页面
        Lg.refresh_login_ap()
        tmp1 = StateInfoBusiness(self.driver)
        #获取当前模式
        result1 = tmp1.obtain_AP_current_mode()
        #获取内网IP获取方式
        result2 = tmp1.obtain_WAN_IP_generation()
        #获取IP地址
        result3 = tmp1.obtain_WAN_IP_address()

        #判断ssid是否恢复
        tmp2 = WirelessSettingsBusiness(self.driver)
        result4 = tmp2.get_first_ssid(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'])
        #登录ap后台，判断ap的工作模式
        tmp3 = WorkModeBusiness(self.driver)
        result5 = tmp3.check_DUT_workmode(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'])
        #检查固件版本
        result6 = tmp.check_system_version(data_basic['old_version'])
        self.assertEqual(result1, "AP模式")
        self.assertEqual(result2, "静态IP")
        self.assertEqual(data_basic['DUT_ip'], result3)
        self.assertIn(data_wirless['all_ssid'], result4)
        self.assertIn("ap", result5)
        self.assertTrue(result6)
        log.debug("005\t\tpass")

    #ap模式下，系统升级，检查配置
    def test_006_apmode_system_upgrade_check_config(self):
        """ap模式下，系统升级，检查配置"""
        tmp = SystemUpgradeBusiness(self.driver)
        #选择固件路径，升级固件
        PATH = os.path.join(os.getcwd(), AP_model+'-'+data_basic['new_version']+'.bin')
        print(PATH)
        tmp.upgrade_system(PATH)

        #设置PC的静态IP,能够访问DUT的webpage
        tmp.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])
        #逻辑类对象，建一个实例
        Lg = LoginBusiness(self.driver)
        #刷新页面重新登录ap页面
        Lg.refresh_login_ap()
        tmp1 = StateInfoBusiness(self.driver)
        #获取当前模式
        result1 = tmp1.obtain_AP_current_mode()
        #获取内网IP获取方式
        result2 = tmp1.obtain_WAN_IP_generation()
        #获取IP地址
        result3 = tmp1.obtain_WAN_IP_address()

        #判断ssid是否恢复
        tmp2 = WirelessSettingsBusiness(self.driver)
        result4 = tmp2.get_first_ssid(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'])
        #登录ap后台，判断ap的工作模式
        tmp3 = WorkModeBusiness(self.driver)
        result5 = tmp3.check_DUT_workmode(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'])
        #检查固件版本
        result6 = tmp.check_system_version(data_basic['new_version'])
        self.assertEqual(result1, "AP模式")
        self.assertEqual(result2, "静态IP")
        self.assertEqual(data_basic['DUT_ip'], result3)
        self.assertIn(data_wirless['all_ssid'], result4)
        self.assertIn("ap", result5)
        self.assertTrue(result6)
        log.debug("006\t\tpass")

    #桥接模式下，修改配置后，系统降级，检查配置
    def test_007_bridgemode_system_downgrade_check_config(self):
        """桥接模式下，修改配置后，系统降级，检查配置"""
        tmp1 = WorkModeBusiness(self.driver)
        #修改工作模式为bridge模式,内网设置静态IP
        tmp1.change_workmode_to_bridge_LANstaticIP(data_basic['DUT_ip'], data_lan['netmask1'],
            data_wirless['bridge_essid'], data_wirless['bridge_encryption'],
            data_wirless['bridge_bssid'], data_wirless['bridge_pwd'], data_wirless['all_ssid'],
            "psk2", data_wirless['short_wpa'], data_basic['ssh_user'], data_basic['ssh_pwd'])
        time.sleep(30)
        #选择固件路径，降级固件
        PATH = os.path.join(os.getcwd(), AP_model+'-'+data_basic['old_version']+'.bin')
        print(PATH)
        #逻辑类对象，建一个实例
        Lg = LoginBusiness(self.driver)
        #刷新页面重新登录ap页面
        Lg.refresh_login_ap()
        tmp = SystemUpgradeBusiness(self.driver)
        tmp.upgrade_system(PATH)
        #设置PC的静态IP,能够访问DUT的webpage
        tmp.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])
        #关闭AP的eth1端口，以免她来分配ip地址，和桥接的dhcp server相冲突
        tmp4 = WorkModeBusiness(self.driver)
        tmp4.down_ap_eth1(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'])
        #刷新页面重新登录ap页面
        Lg.refresh_login_ap()
        tmp1 = StateInfoBusiness(self.driver)
        #获取当前模式
        result1 = tmp1.obtain_AP_current_mode()
        #获取桥接的连接状态
        result2 = tmp1.obtain_WAN_IP_generation()
        #获取信号强度
        result3 = tmp1.obtain_WAN_IP_address()

        #判断ssid是否恢复
        tmp2 = WirelessSettingsBusiness(self.driver)
        result4 = tmp2.get_first_ssid(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'])
        #登录ap后台，判断ap的工作模式
        tmp3 = WorkModeBusiness(self.driver)
        result5 = tmp3.check_DUT_workmode(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'])
        #检查固件版本
        result6 = tmp.check_system_version(data_basic['old_version'])
        self.assertEqual(result1, "网桥模式")
        self.assertEqual(result2, "已连接")
        self.assertIn("dBm", result3)
        self.assertIn(data_wirless['all_ssid'], result4)
        self.assertIn("wds", result5)
        self.assertTrue(result6)
        log.debug("007\t\tpass")

    #桥接模式下，系统升级，检查配置
    def test_008_bridgemode_system_upgrade_check_config(self):
        """桥接模式下，系统升级，检查配置"""
        tmp = SystemUpgradeBusiness(self.driver)
        #选择固件路径，升级固件
        PATH = os.path.join(os.getcwd(), AP_model+'-'+data_basic['new_version']+'.bin')
        print(PATH)
        tmp.upgrade_system(PATH)

        #设置PC的静态IP,能够访问DUT的webpage
        tmp.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])
        #关闭AP的eth1端口，以免她来分配ip地址，和桥接的dhcp server相冲突
        tmp4 = WorkModeBusiness(self.driver)
        tmp4.down_ap_eth1(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'])
        #逻辑类对象，建一个实例
        Lg = LoginBusiness(self.driver)
        #刷新页面重新登录ap页面
        Lg.refresh_login_ap()
        tmp1 = StateInfoBusiness(self.driver)
        #获取当前模式
        result1 = tmp1.obtain_AP_current_mode()
        #获取桥接的连接状态
        result2 = tmp1.obtain_WAN_IP_generation()
        #获取信号强度
        result3 = tmp1.obtain_WAN_IP_address()

        #判断ssid是否恢复
        tmp2 = WirelessSettingsBusiness(self.driver)
        result4 = tmp2.get_first_ssid(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'])
        #登录ap后台，判断ap的工作模式
        tmp3 = WorkModeBusiness(self.driver)
        result5 = tmp3.check_DUT_workmode(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'])
        #检查固件版本
        result6 = tmp.check_system_version(data_basic['new_version'])
        self.assertEqual(result1, "网桥模式")
        self.assertEqual(result2, "已连接")
        self.assertIn("dBm", result3)
        self.assertIn(data_wirless['all_ssid'], result4)
        self.assertIn("wds", result5)
        self.assertTrue(result6)
        log.debug("008\t\tpass")

    #客户端模式下，修改配置后，系统降级，检查配置
    def test_009_clientmode_system_downgrade_check_config(self):
        """客户端模式下，修改配置后，系统降级，检查配置"""
        tmp1 = WorkModeBusiness(self.driver)
        #修改工作模式为client模式,内网设置静态IP,桥接ap无线加密为wpa2
        tmp1.change_workmode_to_client_LANstaticIP(data_basic['DUT_ip'], data_lan['netmask1'],
            data_wirless['bridge_essid'], data_wirless['bridge_encryption'],
            data_wirless['bridge_bssid'], data_wirless['bridge_pwd'],
            data_basic['ssh_user'], data_basic['ssh_pwd'])
        time.sleep(30)
        #逻辑类对象，建一个实例
        Lg = LoginBusiness(self.driver)
        #刷新页面重新登录ap页面
        Lg.refresh_login_ap()
        #选择固件路径，降级固件
        PATH = os.path.join(os.getcwd(), AP_model+'-'+data_basic['old_version']+'.bin')
        print(PATH)
        tmp = SystemUpgradeBusiness(self.driver)
        tmp.upgrade_system(PATH)
        #设置PC的静态IP,能够访问DUT的webpage
        tmp.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])
        #关闭AP的eth1端口，以免她来分配ip地址，和桥接的dhcp server相冲突
        tmp4 = WorkModeBusiness(self.driver)
        tmp4.down_ap_eth1(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'])
        #刷新页面重新登录ap页面
        Lg.refresh_login_ap()
        tmp1 = StateInfoBusiness(self.driver)
        #获取当前模式
        result1 = tmp1.obtain_AP_current_mode()
        #获取桥接的连接状态
        result2 = tmp1.obtain_WAN_IP_generation()
        #获取信号强度
        result3 = tmp1.obtain_WAN_IP_address()

        #登录ap后台，判断ap的工作模式
        tmp3 = WorkModeBusiness(self.driver)
        result5 = tmp3.check_DUT_workmode(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'])
        #检查固件版本
        result6 = tmp.check_system_version(data_basic['old_version'])
        #删除下载固件
        os.unlink(PATH)
        self.assertEqual(result1, "客户端模式")
        self.assertEqual(result2, "已连接")
        self.assertIn("dBm", result3)
        self.assertIn("wds_c", result5)
        self.assertTrue(result6)
        log.debug("009\t\tpass")

    #客户端模式下，系统升级，检查配置
    def test_010_clientmode_system_upgrade_check_config(self):
        """客户端模式下，系统升级，检查配置"""
        tmp = SystemUpgradeBusiness(self.driver)
        #选择固件路径，升级固件
        PATH = os.path.join(os.getcwd(), AP_model+'-'+data_basic['new_version']+'.bin')
        print(PATH)
        tmp.upgrade_system(PATH)

        #设置PC的静态IP,能够访问DUT的webpage
        tmp.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])
        #关闭AP的eth1端口，以免她来分配ip地址，和桥接的dhcp server相冲突
        tmp4 = WorkModeBusiness(self.driver)
        tmp4.down_ap_eth1(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'])
        #逻辑类对象，建一个实例
        Lg = LoginBusiness(self.driver)
        #刷新页面重新登录ap页面
        Lg.refresh_login_ap()
        tmp1 = StateInfoBusiness(self.driver)
        #获取当前模式
        result1 = tmp1.obtain_AP_current_mode()
        #获取桥接的连接状态
        result2 = tmp1.obtain_WAN_IP_generation()
        #获取信号强度
        result3 = tmp1.obtain_WAN_IP_address()

        #登录ap后台，判断ap的工作模式
        tmp3 = WorkModeBusiness(self.driver)
        result5 = tmp3.check_DUT_workmode(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'])
        #检查固件版本
        result6 = tmp.check_system_version(data_basic['new_version'])

        #修改工作模式为路由模式,外网设置dhcp模式
        tmp4.change_workmode_to_route_WANdhcp(data_wirless['all_ssid'],
            "psk2", data_wirless['short_wpa'], "HT40", "auto")
        #client重新获取ip
        tmp.dhcp_release_wlan(data_basic['lan_pc'])
        tmp.dhcp_wlan(data_basic['lan_pc'])
        tmp.disconnect_ap()
        #删除下载固件
        os.unlink(PATH)

        self.assertEqual(result1, "客户端模式")
        self.assertEqual(result2, "已连接")
        self.assertIn("dBm", result3)
        self.assertIn("wds_c", result5)
        self.assertTrue(result6)
        log.debug("010\t\tpass")








    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
