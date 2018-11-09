#coding=utf-8
#作者：曾祥卫
#时间：2018.11.2
#描述：用例层代码，调用ipfilter_business

import unittest,time
from selenium import webdriver
from login.login_business import LoginBusiness
from firewall.ipfilter.ipfilter_business import IPFilterBusiness
from systemtools.configupdate.configupdate_business import ConfigUpdateBusiness
from data import data
from data.logfile import Log

data_basic = data.data_basic()
data_login = data.data_login()
data_wirless = data.data_wireless()
data_lan = data.data_lan()

log = Log("IPFilter")

class TestIPFilter(unittest.TestCase):
    """测试IP过滤的用例集(Duration:0.18h)"""
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
        """添加一条IP过滤规则,PC的ip在范围之内,PC不能访问internet"""
        #首先启用无线网卡
        tmp = IPFilterBusiness(self.driver)
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

        #先确定PC能够上网
        result1 = tmp.get_ping("www.baidu.com")
        #获取PC lan口附近的ip地址
        start_end_ip = tmp.obtain_lan_ip_near_ip(data_basic['lan_pc'], 5, 5)
        #添加一条IP过滤规则,PC的ip在范围之内
        tmp.add_one_IPFilter_list(*start_end_ip)
        #判断PC是否能够上网
        result2 = tmp.get_ping("www.baidu.com")
        self.assertEqual(result1, 0)
        self.assertNotEqual(result2, 0)
        log.debug("001\t\tpass")

    def test_002_check_delete_one_list(self):
        """删除一条,PC的ip在范围之内的IP过滤规则,PC能够访问internet"""
        tmp = IPFilterBusiness(self.driver)
        #删除第1条ip过滤的规则list
        tmp.delete_n_list(0)
        #判断PC是否能够上网
        result = tmp.get_ping("www.baidu.com")
        self.assertEqual(result, 0)
        log.debug("002\t\tpass")

    def test_003_check_add_one_list_far_PC_ip(self):
        """添加一条IP过滤规则,PC的ip不在范围之内,PC能够访问internet"""
        tmp = IPFilterBusiness(self.driver)
        #获取不在PC lan口附近的ip地址
        start_end_ip = tmp.obtain_lan_ip_far_ip(data_basic['lan_pc'], 5, 10)
        #添加一条IP过滤规则,PC的ip不在范围之内
        tmp.add_one_IPFilter_list(*start_end_ip)
        #判断PC是否能够上网
        result = tmp.get_ping("www.baidu.com")
        self.assertEqual(result, 0)
        log.debug("003\t\tpass")

    def test_004_check_delete_one_list_far_PC_ip(self):
        """删除一条,PC的ip不在范围之内的IP过滤规则,PC能够访问internet"""
        tmp = IPFilterBusiness(self.driver)
        #删除第1条ip过滤的规则list
        tmp.delete_n_list(0)
        #判断PC是否能够上网
        result = tmp.get_ping("www.baidu.com")
        self.assertEqual(result, 0)
        log.debug("004\t\tpass")

    def test_005_check_add_one_list_is_PC_ip(self):
        """添加一条IP过滤规则,起始ip和结束ip都是PC的ip,PC不能够访问internet"""
        tmp = IPFilterBusiness(self.driver)
        #获取PC的ip地址
        pc_ip = tmp.get_localIp(data_basic['lan_pc'])
        #添加一条IP过滤规则,起始ip和结束ip都是PC的ip
        tmp.add_one_IPFilter_list(pc_ip, pc_ip)
        #判断PC是否能够上网
        result = tmp.get_ping("www.baidu.com")
        self.assertNotEqual(result, 0)
        log.debug("005\t\tpass")

    def test_006_check_add_one_list_isnot_PC_ip(self):
        """添加一条IP过滤规则,起始ip和结束ip都不是PC的ip,PC能够访问internet"""
        tmp = IPFilterBusiness(self.driver)
        #获取不在PC lan口附近的ip地址
        start_end_ip = tmp.obtain_lan_ip_far_ip(data_basic['lan_pc'], 5, 10)
        #编辑第n条ip过滤的规则list
        tmp.edit_n_list(0, start_end_ip[0], start_end_ip[0])
        #判断PC是否能够上网
        result = tmp.get_ping("www.baidu.com")
        #删除所有的ip过滤的规则list
        tmp.delete_all_list()
        self.assertEqual(result, 0)
        log.debug("006\t\tpass")

    def test_007_check_10_list_PC_ip_in_list(self):
        """添加10条IP过滤规则,PC的ip在范围之内,PC不能够访问internet"""
        tmp = IPFilterBusiness(self.driver)
        #获取PC lan口附近的ip地址
        start_end_ip = tmp.obtain_lan_ip_near_ip(data_basic['lan_pc'], 2, 2)
        #添加一条IP过滤规则,PC的ip在范围之内
        tmp.add_one_IPFilter_list(*start_end_ip)
        #添加10条规则，都是高于PC的ip的地址范围
        tmp.add_10_list_far_ip(data_basic['lan_pc'])
        #判断PC是否能够上网
        result = tmp.get_ping("www.baidu.com")
        #删除所有的ip过滤的规则list
        tmp.delete_all_list()
        self.assertNotEqual(result, 0)
        log.debug("007\t\tpass")

    def test_008_check_10_list_PC_ip_out_list(self):
        """添加10条IP过滤规则,PC的ip不在范围之内,PC能够访问internet"""
        tmp = IPFilterBusiness(self.driver)
        #获取不在PC lan口附近的ip地址
        start_end_ip = tmp.obtain_lan_ip_far_ip(data_basic['lan_pc'], 2, 10)
        #添加一条IP过滤规则,PC的ip不在范围之内
        tmp.add_one_IPFilter_list(*start_end_ip)
        #添加10条规则，都是高于PC的ip的地址范围
        tmp.add_10_list_far_ip(data_basic['lan_pc'])
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
