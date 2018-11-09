#coding=utf-8
#作者：曾祥卫
#时间：2018.11.5
#描述：用例层代码，调用dmzsettings_business

import unittest, time, os
from selenium import webdriver
from login.login_business import LoginBusiness
from firewall.dmzsettings.dmzsettings_business import DMZSettingsBusiness
from firewall.ipfilter.ipfilter_business import IPFilterBusiness
from systemtools.configupdate.configupdate_business import ConfigUpdateBusiness
from workmode.workmode_business import WorkModeBusiness
from data import data
from data.logfile import Log

data_basic = data.data_basic()
data_login = data.data_login()
data_wirless = data.data_wireless()
data_lan = data.data_lan()
data_wan = data.data_wan()

log = Log("DMZSettings")

class TestDMZSettings(unittest.TestCase):
    """测试DMZ的用例集(Duration:0.14h)"""
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


    def test_001_check_DMZ_function_when_enable_dmz(self):
        """启用DMZ功能,验证规则是否生效"""
        #首先启用无线网卡
        tmp = DMZSettingsBusiness(self.driver)
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
        #刷新页面重新登录ap页面
        Lg.refresh_login_ap()
        #获取PC的ip地址
        pc_ip = tmp.get_localIp(data_basic['lan_pc'])
        #启用DMZ功能
        tmp.open_DMZ(pc_ip)
        #判断DMZ功能是否有效--验证80端口
        result = tmp.check_DMZ_function(data_basic['scp_server'], data_basic['scp_name'],
            data_basic['scp_pwd'], data_wan['static_IP'])
        self.assertTrue(result)
        log.debug("001\t\tpass")

    def test_002_check_DMZ_function_when_disable_dmz(self):
        """禁用DMZ功能,验证规则不再生效"""
        tmp = DMZSettingsBusiness(self.driver)
        #禁用DMZ功能
        tmp.close_DMZ()
        #判断DMZ功能是否有效--验证80端口
        result = tmp.check_DMZ_function(data_basic['scp_server'], data_basic['scp_name'],
            data_basic['scp_pwd'], data_wan['static_IP'])
        self.assertFalse(result)
        log.debug("002\t\tpass")

    def test_003_check_DMZ_function_when_other_ip(self):
        """启用DMZ功能,ip指定为非本机pc的ip，验证本机的dmz无效"""
        tmp1 = IPFilterBusiness(self.driver)
        ip = tmp1.obtain_lan_ip_far_ip(data_basic['lan_pc'], 2,3)
        tmp = DMZSettingsBusiness(self.driver)
        #启用DMZ功能
        tmp.open_DMZ(ip[0])
        #判断DMZ功能是否有效--验证80端口
        result = tmp.check_DMZ_function(data_basic['scp_server'], data_basic['scp_name'],
            data_basic['scp_pwd'], data_wan['static_IP'])
        tmp.disconnect_ap()
        self.assertFalse(result)
        log.debug("003\t\tpass")




    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
