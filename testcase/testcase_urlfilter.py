#coding=utf-8
#作者：曾祥卫
#时间：2018.11.5
#描述：用例层代码，调用urlfilter_business

import unittest, time, os
from selenium import webdriver
from login.login_business import LoginBusiness
from firewall.urlfilter.urlfilter_business import UrlFilterBusiness
from systemtools.configupdate.configupdate_business import ConfigUpdateBusiness
from workmode.workmode_business import WorkModeBusiness
from data import data
from data.logfile import Log

data_basic = data.data_basic()
data_login = data.data_login()
data_wirless = data.data_wireless()
data_lan = data.data_lan()
data_wan = data.data_wan()

log = Log("URLFilter")

class TestURLFilter(unittest.TestCase):
    """测试URL过滤的用例集(Duration:0.25h)"""
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


    def test_001_check_add_one_list_not_access_url(self):
        """添加一条url过滤规则,PC不能够访问指定的url"""
        #首先启用无线网卡
        tmp = UrlFilterBusiness(self.driver)
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

        #先确定PC能够访问指定的url--baidu
        result1 = tmp.check_access_url("www.baidu.com")
        #添加一条url过滤规则--baidu
        tmp.add_one_list("baidu")
        #确定PC不能够访问指定的url--baidu
        result2 = tmp.check_access_url("www.baidu.com")
        self.assertTrue(result1)
        self.assertFalse(result2)
        log.debug("001\t\tpass")

    def test_002_check_add_one_part_url_list(self):
        """添加一条url过滤规则,只有部分关键字的url，PC不能够访问指定的url"""
        tmp = UrlFilterBusiness(self.driver)
        #编辑第一条url
        tmp.edit_n_list(0, "bai")
        #确定PC不能够访问指定的url--baidu
        result = tmp.check_access_url("www.baidu.com")
        self.assertFalse(result)
        log.debug("002\t\tpass")

    def test_003_check_delete_one_list(self):
        """删除一条url过滤规则,PC能够访问指定的url"""
        tmp = UrlFilterBusiness(self.driver)
        #删除第1条mac过滤的规则list
        tmp.delete_n_list(0)
        #判断PC能够访问指定的url--baidu
        result = tmp.check_access_url("www.baidu.com")
        self.assertTrue(result)
        log.debug("003\t\tpass")

    def test_004_check_add_one_list_access_other_url(self):
        """添加一条url过滤规则,PC能够访问非指定的url"""
        tmp = UrlFilterBusiness(self.driver)
        #添加一条url过滤规则--baidu
        tmp.add_one_list("baidu")
        #确定PC能够访问非指定的url--so
        result = tmp.check_access_url("www.so.com")
        self.assertTrue(result)
        log.debug("004\t\tpass")

    def test_005_check_delete_one_list_access_other_url(self):
        """删除一条url过滤规则,PC能够访问非指定的url"""
        tmp = UrlFilterBusiness(self.driver)
        #删除第1条mac过滤的规则list
        tmp.delete_n_list(0)
        #判断PC能够访问指定的url--so
        result = tmp.check_access_url("www.so.com")
        self.assertTrue(result)
        log.debug("005\t\tpass")

    def test_006_check_add_one_list_access_contains_str_url(self):
        """添加一条url过滤规则,PC能够访问非指定的url，并且包含已过滤的url的其中字符"""
        tmp = UrlFilterBusiness(self.driver)
        #添加一条url过滤规则--sohu
        tmp.add_one_list("sohu")
        #确定PC能够访问非指定的url，并且包含已过滤的url的其中字符--so
        result = tmp.check_access_url("www.so.com")
        self.assertTrue(result)
        log.debug("006\t\tpass")

    def test_007_check_10_list_on_access_url(self):
        """添加10条url过滤规则,,PC不能够访问指定的url"""
        tmp = UrlFilterBusiness(self.driver)
        #编辑一条url过滤规则--baidu
        tmp.edit_n_list(0, "baidu")
        #添加10条规则，mac地址为随机mac地址
        tmp.add_10_list("baidu")
        #确定PC不能够访问指定的url
        result = tmp.check_access_url("www.baidu.com")
        self.assertFalse(result)
        log.debug("007\t\tpass")

    def test_008_check_10_list_access_other_url(self):
        """添加10条url过滤规则,,PC能够访问非指定的url"""
        tmp = UrlFilterBusiness(self.driver)
        #确定PC能够访问非指定的url
        result = tmp.check_access_url("www.so.com")
        self.assertTrue(result)
        log.debug("008\t\tpass")


    def test_009_check_delete_10_list(self):
        """删除所有规则,PC能够访问指定url和非指定url"""
        tmp = UrlFilterBusiness(self.driver)
        #删除所有的url过滤的规则list
        tmp.delete_all_list()
        #确定PC能够访问指定的url
        result1 = tmp.check_access_url("www.baidu.com")
        #确定PC能够访问非指定的url
        result2 = tmp.check_access_url("www.so.com")
        # 删除所有下载的html
        path = os.path.join(os.getcwd(), "index.html*")
        tmp.get_client_cmd_result("rm -rf {}".format(path))
        tmp.disconnect_ap()
        self.assertTrue(result1)
        self.assertTrue(result2)
        log.debug("009\t\tpass")


    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
