#coding=utf-8
#作者：曾祥卫
#时间：2018.09.19
#描述：用例层代码，调用configupdate_business

import unittest,time, os, shutil
from selenium import webdriver
from login.login_business import LoginBusiness
from systemtools.rebootsystem.rebootsystem_business import RebootSystemBusiness
from systemtools.configupdate.configupdate_business import ConfigUpdateBusiness
from network.wirelesssettings.wirelesssettings_business import WirelessSettingsBusiness
from network.wansettings.wansettings_business import WanSettingsBusiness
from workmode.workmode_business import WorkModeBusiness
from stateinfo.stateinfo_business import StateInfoBusiness
from connect.ssh import SSH
from data import data
from data.logfile import Log

data_basic = data.data_basic()
data_login = data.data_login()
data_wirless = data.data_wireless()
data_wan = data.data_wan()
data_lan = data.data_lan()

log = Log("ConfigUpdate")

class TestConfigUpdate(unittest.TestCase):
    """测试配置更新的用例集(Duration:1.05h)"""
    def setUp(self):
        fp = webdriver.FirefoxProfile()
        fp.set_preference("browser.download.folderList",2)
        fp.set_preference("browser.download.manager.showWhenStarting",False)
        fp.set_preference("browser.download.dir", os.getcwd())
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk","application/x-targz")
        self.driver = webdriver.Firefox(firefox_profile=fp)
        self.driver.maximize_window()
        self.driver.get(data_basic['DUT_web'])
        self.driver.implicitly_wait(20)
        #逻辑类对象，建一个实例
        Lg = LoginBusiness(self.driver)
        #调用实例的登录AP的web界面
        Lg.login(data_basic['superUser'], data_basic['super_defalut_pwd'])
        #刷新页面重新登录ap页面
        Lg.refresh_login_ap()

    def test_001_routemode_save_config_file(self):
        """路由模式下保存配置"""
        #首先启用无线网卡
        tmp = ConfigUpdateBusiness(self.driver)
        tmp.wlan_enable(data_basic['wlan_pc'])
        #刷新页面重新登录ap页面
        Lg = LoginBusiness(self.driver)
        Lg.refresh_login_ap()
        #把AP恢复出厂配置
        tmp3 = ConfigUpdateBusiness(self.driver)
        tmp3.restore_AP_factory()
        #重新登录AP
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
        #下载配置文件
        tmp.download_config_file()
        #判断配置文件是否下载
        #文件路径
        PATH = os.path.join(os.getcwd(), "bakup.file")
        print(PATH)
        result = os.path.exists(PATH)
        #判断wan口是否是静态IP
        tmp3 = WanSettingsBusiness(self.driver)
        result5 = tmp3.get_wan_way(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'])
        self.assertTrue(result)
        self.assertIn("static", result5)
        log.debug("001\t\tpass")

    def test_002_routemode_check_restore_AP_factory(self):
        """
        路由模式下验证AP是否恢复出厂配置
        """
        tmp = ConfigUpdateBusiness(self.driver)
        #在AP的web页面上点击恢复出厂设置
        tmp.restore_AP_factory()
        #判断ssid是否恢复出厂
        tmp1 = WirelessSettingsBusiness(self.driver)
        result1 = tmp1.get_first_ssid(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'])
        #判断wan口是否恢复出厂
        tmp2 = WanSettingsBusiness(self.driver)
        result2 = tmp2.get_wan_way(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'])
        #默认ssid
        default_ssid = "3ONE_2G_"+ data.master_last_6mac()
        self.assertIn(default_ssid, result1)
        self.assertIn("dhcp", result2)
        log.debug("002\t\tpass")


    def test_003_routemode_upload_config_file(self):
        """路由模式下验证上传配置文件"""
        tmp = ConfigUpdateBusiness(self.driver)
        #文件路径
        PATH = os.path.join(os.getcwd(), "bakup.file")
        print(PATH)
        #上传配置文件
        tmp.upload_config_file(PATH)

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

        #判断ssid是否恢复
        tmp2 = WirelessSettingsBusiness(self.driver)
        result4 = tmp2.get_first_ssid(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'])
        #判断wan口是否是静态IP
        tmp3 = WanSettingsBusiness(self.driver)
        result5 = tmp3.get_wan_way(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'])
        #测试完成后删除备份文件
        if result2 != "静态IP":
            #如果恢复配置失败，保存配置文件
            dirname = os.path.dirname(os.path.dirname(__file__))
            current_time = time.strftime('%m%d%H%M',time.localtime(time.time()))
            backfile_PATH = os.path.join(dirname, "data", "testresultdata", "routemode_{}_bakup.file".format(current_time))
            shutil.copy(PATH, backfile_PATH)
        os.unlink(PATH)
        self.assertEqual(result1, "路由模式")
        self.assertEqual(result2, "静态IP")
        self.assertEqual(data_wan['static_IP'], result3)
        self.assertIn(data_wirless['all_ssid'], result4)
        self.assertIn("static", result5)
        log.debug("003\t\tpass")

    def test_004_routemode_check_work_normal_after_upload_config_file(self):
        """路由模式下验证上传配置文件后，AP工作正常"""
        tmp = WorkModeBusiness(self.driver)
        #使用无线网卡连接AP，并能够上网
        resutl1, result2 = tmp.check_after_workmode_normal(data_wirless['all_ssid'],
            data_basic['wlan_pc'], "wpa", data_wirless['short_wpa'])
        self.assertEqual(resutl1, 0)
        self.assertIn(data_wirless['all_ssid'], result2)
        log.debug("004\t\tpass")

    def test_005_apmode_save_config_file(self):
        """AP模式下保存配置"""
        tmp = WorkModeBusiness(self.driver)
        #设置PC的静态IP,能够访问DUT的webpage
        tmp.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])
        #修改工作模式为AP模式,内网设置静态IP
        tmp.change_workmode_to_ap_LANstaticIP(data_basic['DUT_ip'],
            data_lan['netmask1'], data_wirless['all_ssid'], "psk2",
            data_wirless['short_wpa'], "HT20")
        time.sleep(30)
        #逻辑类对象，建一个实例
        Lg = LoginBusiness(self.driver)
        #刷新页面重新登录ap页面
        Lg.refresh_login_ap()
        #下载配置文件
        tmp1 = ConfigUpdateBusiness(self.driver)
        tmp1.download_config_file()
        #判断配置文件是否下载
        #文件路径
        PATH = os.path.join(os.getcwd(), "bakup.file")
        print(PATH)
        result = os.path.exists(PATH)
        #登录ap后台，判断ap的工作模式
        result5 = tmp.check_DUT_workmode(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'])
        self.assertTrue(result)
        self.assertIn("ap", result5)
        log.debug("005\t\tpass")

    def test_006_apmode_check_restore_AP_factory(self):
        """
        AP模式下验证AP是否恢复出厂配置
        """
        tmp = ConfigUpdateBusiness(self.driver)
        #在AP的web页面上点击恢复出厂设置
        tmp.restore_AP_factory()
        #判断ssid是否恢复出厂
        tmp1 = WirelessSettingsBusiness(self.driver)
        result1 = tmp1.get_first_ssid(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'])
        #判断wan口是否恢复出厂
        tmp2 = WanSettingsBusiness(self.driver)
        result2 = tmp2.get_wan_way(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'])
        #默认ssid
        default_ssid = "3ONE_2G_"+ data.master_last_6mac()
        #登录ap后台，判断ap的工作模式
        tmp3 = WorkModeBusiness(self.driver)
        result3 = tmp3.check_DUT_workmode(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'])

        #设置PC的静态IP,能够访问DUT的webpage
        tmp.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])

        self.assertIn(default_ssid, result1)
        self.assertIn("dhcp", result2)
        self.assertNotIn("ap", result3)
        log.debug("006\t\tpass")

    def test_007_apmode_upload_config_file(self):
        """AP模式下验证上传配置文件"""
        tmp = ConfigUpdateBusiness(self.driver)
        #文件路径
        PATH = os.path.join(os.getcwd(), "bakup.file")
        print(PATH)
        #上传配置文件
        tmp.upload_config_file(PATH)

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
        #测试完成后删除备份文件
        if result1 != "AP模式":
            #如果恢复配置失败，保存配置文件
            dirname = os.path.dirname(os.path.dirname(__file__))
            current_time = time.strftime('%m%d%H%M',time.localtime(time.time()))
            backfile_PATH = os.path.join(dirname, "data", "testresultdata", "apmode_{}_bakup.file".format(current_time))
            shutil.copy(PATH, backfile_PATH)
        os.unlink(PATH)
        self.assertEqual(result1, "AP模式")
        self.assertEqual(result2, "静态IP")
        self.assertEqual(data_basic['DUT_ip'], result3)
        self.assertIn(data_wirless['all_ssid'], result4)
        self.assertIn("ap", result5)
        log.debug("007\t\tpass")

    def test_008_apmode_check_work_normal_after_upload_config_file(self):
        """AP模式下验证上传配置文件后，AP工作正常"""
        tmp = WorkModeBusiness(self.driver)
        #判断AP模式设置后，AP正常：PC的有线能上网
        result1 = tmp.check_apmode_normal(data_basic['PC_pwd'], data_basic['lan_pc'],
            data_wan['static_IP'], data_wan['netmask'], data_wan['gateway'])
        #无线网卡能够连接上AP的SSID
        result2 = tmp.client_connect_ssid(data_wirless['all_ssid'],
            data_basic['wlan_pc'], "wpa", data_wirless['short_wpa'])
        #指定有线网卡的固定ip--能够访问ap的webpage
        tmp.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])
        self.assertEqual(result1, 0)
        self.assertIn(data_wirless['all_ssid'], result2)
        log.debug("008\t\tpass")

    def test_009_bridgemode_save_config_file(self):
        """桥接模式下保存配置"""
        tmp = WorkModeBusiness(self.driver)
        #修改工作模式为bridge模式,内网设置静态IP
        tmp.change_workmode_to_bridge_LANstaticIP(data_basic['DUT_ip'], data_lan['netmask1'],
            data_wirless['bridge_essid'], data_wirless['bridge_encryption'],
            data_wirless['bridge_bssid'], data_wirless['bridge_pwd'], data_wirless['all_ssid'],
            "psk2", data_wirless['short_wpa'], data_basic['ssh_user'], data_basic['ssh_pwd'])
        #逻辑类对象，建一个实例
        Lg = LoginBusiness(self.driver)
        #刷新页面重新登录ap页面
        Lg.refresh_login_ap()
        #下载配置文件
        tmp1 = ConfigUpdateBusiness(self.driver)
        tmp1.download_config_file()
        #判断配置文件是否下载
        #文件路径
        PATH = os.path.join(os.getcwd(), "bakup.file")
        print(PATH)
        result = os.path.exists(PATH)
        #登录ap后台，判断ap的工作模式
        result5 = tmp.check_DUT_workmode(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'])
        self.assertTrue(result)
        self.assertIn("wds", result5)
        log.debug("009\t\tpass")

    def test_010_bridgemode_check_restore_AP_factory(self):
        """
        桥接模式下验证AP是否恢复出厂配置
        """
        tmp = ConfigUpdateBusiness(self.driver)
        #在AP的web页面上点击恢复出厂设置
        tmp.restore_AP_factory()
        #判断ssid是否恢复出厂
        tmp1 = WirelessSettingsBusiness(self.driver)
        result1 = tmp1.get_first_ssid(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'])
        #判断wan口是否恢复出厂
        tmp2 = WanSettingsBusiness(self.driver)
        result2 = tmp2.get_wan_way(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'])
        #默认ssid
        default_ssid = "3ONE_2G_"+ data.master_last_6mac()
        #登录ap后台，判断ap的工作模式
        tmp3 = WorkModeBusiness(self.driver)
        result3 = tmp3.check_DUT_workmode(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'])

        #设置PC的静态IP,能够访问DUT的webpage
        tmp.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])

        self.assertIn(default_ssid, result1)
        self.assertIn("dhcp", result2)
        self.assertNotIn("wds", result3)
        log.debug("010\t\tpass")

    def test_011_bridgemode_upload_config_file(self):
        """桥接模式下验证上传配置文件"""
        tmp = ConfigUpdateBusiness(self.driver)
        #文件路径
        PATH = os.path.join(os.getcwd(), "bakup.file")
        print(PATH)
        #上传配置文件
        tmp.upload_config_file(PATH)

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
        #测试完成后删除备份文件
        if result1 != "网桥模式":
            #如果恢复配置失败，保存配置文件
            dirname = os.path.dirname(os.path.dirname(__file__))
            current_time = time.strftime('%m%d%H%M',time.localtime(time.time()))
            backfile_PATH = os.path.join(dirname, "data", "testresultdata", "bridgemode_{}_bakup.file".format(current_time))
            shutil.copy(PATH, backfile_PATH)
        os.unlink(PATH)
        self.assertEqual(result1, "网桥模式")
        self.assertEqual(result2, "已连接")
        self.assertIn("dBm", result3)
        self.assertIn(data_wirless['all_ssid'], result4)
        self.assertIn("wds", result5)
        log.debug("011\t\tpass")

    def test_012_bridgemode_check_work_normal_after_upload_config_file(self):
        """桥接模式下验证上传配置文件后，AP工作正常"""
        tmp = WorkModeBusiness(self.driver)
        #判断运行模式设置后，AP正常：能上网，无线网卡能够连接上AP的SSID
        resutl1, result2 = tmp.check_after_workmode_normal(data_wirless['all_ssid'],
            data_basic['wlan_pc'], "wpa", data_wirless['short_wpa'], data_wirless['bridge_ip'])
        #指定有线网卡的固定ip--能够访问ap的webpage
        tmp.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])
        self.assertEqual(resutl1, 0)
        self.assertIn(data_wirless['all_ssid'], result2)
        log.debug("012\t\tpass")

    def test_013_clientmode_save_config_file(self):
        """客户端模式下保存配置"""
        tmp = WorkModeBusiness(self.driver)
        #修改工作模式为client模式,内网设置静态IP,桥接ap无线加密为wpa2
        tmp.change_workmode_to_client_LANstaticIP(data_basic['DUT_ip'], data_lan['netmask1'],
            data_wirless['bridge_essid'], data_wirless['bridge_encryption'],
            data_wirless['bridge_bssid'], data_wirless['bridge_pwd'],
            data_basic['ssh_user'], data_basic['ssh_pwd'])
        #逻辑类对象，建一个实例
        Lg = LoginBusiness(self.driver)
        #刷新页面重新登录ap页面
        Lg.refresh_login_ap()
        #下载配置文件
        tmp1 = ConfigUpdateBusiness(self.driver)
        tmp1.download_config_file()
        #判断配置文件是否下载
        #文件路径
        PATH = os.path.join(os.getcwd(), "bakup.file")
        print(PATH)
        result = os.path.exists(PATH)
        #登录ap后台，判断ap的工作模式
        result5 = tmp.check_DUT_workmode(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'])
        self.assertTrue(result)
        self.assertIn("wds_c", result5)
        log.debug("013\t\tpass")

    def test_014_clientmode_check_restore_AP_factory(self):
        """
        客户端模式下验证AP是否恢复出厂配置
        """
        tmp = ConfigUpdateBusiness(self.driver)
        #在AP的web页面上点击恢复出厂设置
        tmp.restore_AP_factory()
        #判断ssid是否恢复出厂
        tmp1 = WirelessSettingsBusiness(self.driver)
        result1 = tmp1.get_first_ssid(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'])
        #判断wan口是否恢复出厂
        tmp2 = WanSettingsBusiness(self.driver)
        result2 = tmp2.get_wan_way(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'])
        #默认ssid
        default_ssid = "3ONE_2G_"+ data.master_last_6mac()
        #登录ap后台，判断ap的工作模式
        tmp3 = WorkModeBusiness(self.driver)
        result3 = tmp3.check_DUT_workmode(data_basic['DUT_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'])

        #设置PC的静态IP,能够访问DUT的webpage
        tmp.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])

        self.assertIn(default_ssid, result1)
        self.assertIn("dhcp", result2)
        self.assertNotIn("wds_c", result3)
        log.debug("014\t\tpass")

    def test_015_clientmode_upload_config_file(self):
        """客户端模式下验证上传配置文件"""
        tmp = ConfigUpdateBusiness(self.driver)
        #文件路径
        PATH = os.path.join(os.getcwd(), "bakup.file")
        print(PATH)
        #上传配置文件
        tmp.upload_config_file(PATH)

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
        #测试完成后删除备份文件
        if result1 != "客户端模式":
            #如果恢复配置失败，保存配置文件
            dirname = os.path.dirname(os.path.dirname(__file__))
            current_time = time.strftime('%m%d%H%M',time.localtime(time.time()))
            backfile_PATH = os.path.join(dirname, "data", "testresultdata", "clientmode_{}_bakup.file".format(current_time))
            shutil.copy(PATH, backfile_PATH)
        os.unlink(PATH)
        self.assertEqual(result1, "客户端模式")
        self.assertEqual(result2, "已连接")
        self.assertIn("dBm", result3)
        self.assertIn("wds_c", result5)
        log.debug("015\t\tpass")

    def test_016_clientmode_check_work_normal_after_upload_config_file(self):
        """客户端模式模式下验证上传配置文件后，AP工作正常"""
        tmp = WorkModeBusiness(self.driver)
        #判断client模式设置后，AP正常：PC的有线能上网，无线网卡不能够扫描到原来AP的SSID
        resutl1, result2 = tmp.check_clientmode_normal(data_wirless['all_ssid'],
            data_basic['lan_pc'], data_basic['wlan_pc'], data_wirless['bridge_ip'])
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
        self.assertFalse(result2)
        log.debug("016\t\tpass")





    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()

