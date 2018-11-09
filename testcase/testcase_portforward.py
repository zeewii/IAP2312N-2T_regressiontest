#coding=utf-8
#作者：曾祥卫
#时间：2018.11.5
#描述：用例层代码，调用portforward_business

import unittest, time, os
from selenium import webdriver
from login.login_business import LoginBusiness
from firewall.portforward.portforward_business import PortForwardBusiness
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

log = Log("PortForward")

class TestPortForward(unittest.TestCase):
    """测试端口转发的用例集(Duration:0.25h)"""
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


    def test_001_check_portforward_function_add_one_list(self):
        """添加一条端口转发规则,验证规则是否生效"""
        #首先启用无线网卡
        tmp = PortForwardBusiness(self.driver)
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
        #添加一条端口转发规则
        tmp.add_one_list(pc_ip, "tcp udp", 79, 81)
        #判断端口转发功能是否有效--验证80端口
        result = tmp.check_portforward_function(data_basic['scp_server'], data_basic['scp_name'],
            data_basic['scp_pwd'], data_wan['static_IP'])
        self.assertTrue(result)
        log.debug("001\t\tpass")

    def test_002_check_portforward_invalid_delete_list(self):
        """删除端口转发规则,验证规则是否生效"""
        tmp = PortForwardBusiness(self.driver)
        #删除第1条端口转发的规则list
        tmp.delete_n_list(0)
        #判断端口转发功能是否有效--验证80端口
        result = tmp.check_portforward_function(data_basic['scp_server'], data_basic['scp_name'],
            data_basic['scp_pwd'], data_wan['static_IP'])
        self.assertFalse(result)
        log.debug("002\t\tpass")

    def test_003_check_portforward_invalid_out_of_port(self):
        """添加一条端口转发规则,验证不在规则的端口范围内的端口无效"""
        tmp = PortForwardBusiness(self.driver)
        #获取PC的ip地址
        pc_ip = tmp.get_localIp(data_basic['lan_pc'])
        #添加一条端口转发规则
        tmp.add_one_list(pc_ip, "tcp udp", 20, 25)
        #判断端口转发功能是否有效--验证80端口
        result = tmp.check_portforward_function(data_basic['scp_server'], data_basic['scp_name'],
            data_basic['scp_pwd'], data_wan['static_IP'])
        self.assertFalse(result)
        log.debug("003\t\tpass")

    def test_004_check_startport_equal_endport(self):
        """当起始端口和结束端口相同时，验证规则是否生效"""
        tmp = PortForwardBusiness(self.driver)
        #获取PC的ip地址
        pc_ip = tmp.get_localIp(data_basic['lan_pc'])
        tmp.edit_n_list(0, pc_ip, "tcp udp", 80, 80)
        #判断端口转发功能是否有效--验证80端口
        result = tmp.check_portforward_function(data_basic['scp_server'], data_basic['scp_name'],
            data_basic['scp_pwd'], data_wan['static_IP'])
        self.assertTrue(result)
        log.debug("004\t\tpass")

    def test_005_check_Protocol_tcp(self):
        """当协议是only tcp时，验证规则是否生效"""
        tmp = PortForwardBusiness(self.driver)
        #获取PC的ip地址
        pc_ip = tmp.get_localIp(data_basic['lan_pc'])
        tmp.edit_n_list(0, pc_ip, "tcp", 80, 80)
        #判断端口转发功能是否有效--验证80端口
        result = tmp.check_portforward_function(data_basic['scp_server'], data_basic['scp_name'],
            data_basic['scp_pwd'], data_wan['static_IP'])
        self.assertTrue(result)
        log.debug("005\t\tpass")

    def test_006_check_other_ip(self):
        """规则指定其他ip地址时，验证本PC的端口转发功能无效"""
        tmp1 = IPFilterBusiness(self.driver)
        ip = tmp1.obtain_lan_ip_far_ip(data_basic['lan_pc'], 2,3)
        tmp = PortForwardBusiness(self.driver)
        tmp.edit_n_list(0, ip[0], "tcp udp", 80, 80)
        #判断端口转发功能是否有效--验证80端口
        result = tmp.check_portforward_function(data_basic['scp_server'], data_basic['scp_name'],
            data_basic['scp_pwd'], data_wan['static_IP'])
        self.assertFalse(result)
        log.debug("006\t\tpass")

    def test_007_check_portforward_when_add_many_list(self):
        """当添加多条端口转发规则时，验证规则是否生效"""
        tmp = PortForwardBusiness(self.driver)
        #获取PC的ip地址
        pc_ip = tmp.get_localIp(data_basic['lan_pc'])
        tmp.edit_n_list(0, pc_ip, "tcp udp", 70, 90)
        #添加10条规则
        tmp.add_10_list(pc_ip, "tcp udp")
        #判断端口转发功能是否有效--验证80端口
        result = tmp.check_portforward_function(data_basic['scp_server'], data_basic['scp_name'],
            data_basic['scp_pwd'], data_wan['static_IP'])
        self.assertTrue(result)
        log.debug("007\t\tpass")

    def test_008_check_portforward_invalid_delete_all_lists(self):
        """删除所有的规则后，端口转发功能无效"""
        tmp = PortForwardBusiness(self.driver)
        #删除所有的规则
        tmp.delete_all_list()
        #判断端口转发功能是否有效--验证80端口
        result = tmp.check_portforward_function(data_basic['scp_server'], data_basic['scp_name'],
            data_basic['scp_pwd'], data_wan['static_IP'])
        tmp.disconnect_ap()
        self.assertFalse(result)
        log.debug("008\t\tpass")







    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
