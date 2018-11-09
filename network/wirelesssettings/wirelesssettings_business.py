#coding=utf-8
#作者：曾祥卫
#时间：2018.09.20
#描述：无线设置的业务逻辑层

from network.wirelesssettings.wirelesssettings_control import WirelessSettingsControl
from network.network_control import NetWorkControl
from connect.ssh import SSH
from login.login_business import LoginBusiness
import time
from data import data
data_basic = data.data_basic()

class WirelessSettingsBusiness(WirelessSettingsControl):

    def __init__(self,driver):
        #继承WirelessSettingsControl类的属性和方法
        WirelessSettingsControl.__init__(self,driver)

    def change_wifi_switch(self):
        """
        点击无线开关
        """
        #首先点击网络设置
        tmp = NetWorkControl(self.driver)
        tmp.menu_network()
        #再点击无线设置
        self.menu_wirelesssettings()
        #点击无线开关
        self.set_wireless_switch()
        #点击设置按钮
        self.click_save_button()
        #点击保存
        self.click_confirm_button()

    def change_hidden_ssid(self):
        """
        点击隐藏ssid
        """
        #首先点击网络设置
        tmp = NetWorkControl(self.driver)
        tmp.menu_network()
        #再点击无线设置
        self.menu_wirelesssettings()
        #点击隐藏无线SSID
        self.set_hidden_ssid()
        #点击设置按钮
        self.click_save_button()
        #点击保存
        self.click_confirm_button()

    def change_ssid(self, ssid):
        """
        修改ssid
        """
        #首先点击网络设置
        tmp = NetWorkControl(self.driver)
        tmp.menu_network()
        #再点击无线设置
        self.menu_wirelesssettings()
        #输入ssid名称
        self.set_ssid(ssid)
        #点击设置按钮
        self.click_save_button()
        #点击保存
        self.click_confirm_button()

    def obtain_ssid(self):
        """
        获取页面上的ssid
        """
        #首先点击网络设置
        tmp = NetWorkControl(self.driver)
        tmp.menu_network()
        #再点击无线设置
        self.menu_wirelesssettings()
        #获取ssid
        result = self.get_ssid()
        return result

    def check_ssid_warning(self, ssid):
        """
        判断ssid输入框是否有红色警告
        输出：True:有警告;False：无警告
        """
        #首先点击网络设置
        tmp = NetWorkControl(self.driver)
        tmp.menu_network()
        #再点击无线设置
        self.menu_wirelesssettings()
        #输入ssid名称
        self.set_ssid(ssid)
        time.sleep(2)
        #判断ssid输入框是否有红色警告
        result = self.check_ssid_InputBox_red()
        return result


    #获取第一个wifi的ssid
    def get_first_ssid(self, host, user, pwd):
        """
        获取第一个wifi的ssid
        """
        ssh = SSH(host, pwd)
        result = ssh.ssh_cmd(user, "uci show wireless.wlan0.ssid")
        return result


    def change_wifi_encryption_pwd(self, encryption, pwd):
        """
        修改无线的加密方式和密码
        encryption:none,psk2,wep+shared
        pwd:空，wpa，wep加密
        """
        #首先点击网络设置
        tmp = NetWorkControl(self.driver)
        tmp.menu_network()
        #再点击无线设置
        self.menu_wirelesssettings()
        #输入无线的加密方式
        self.set_encryption(encryption)
        #输入2.4G无线的密码
        self.set_route_24g_password(pwd)
        #点击设置按钮
        self.click_save_button()
        #点击保存
        self.click_confirm_button()

    def check_wpa_password_warning(self, encryption, pwd):
        """
        判断wpa密码输入框是否有红色警告
        输出：True:有警告;False：无警告
        """
        #首先点击网络设置
        tmp = NetWorkControl(self.driver)
        tmp.menu_network()
        #再点击无线设置
        self.menu_wirelesssettings()
        #输入无线的加密方式
        self.set_encryption(encryption)
        #输入2.4G无线的密码
        self.set_route_24g_password(pwd)
        time.sleep(2)
        #判断wpa密码输入框是否有红色警告
        result = self.check_wpa_password_InputBox_red()
        return result

    def change_wifi_ssid_encryption_pwd(self, ssid, encryption, pwd):
        """
        修改无线的ssid,加密方式和密码
        ssid
        encryption:none,psk2,wep+shared
        pwd:空，wpa，wep加密
        """
        #首先点击网络设置
        tmp = NetWorkControl(self.driver)
        tmp.menu_network()
        #再点击无线设置
        self.menu_wirelesssettings()
        #输入ssid名称
        self.set_ssid(ssid)
        #输入无线的加密方式
        self.set_encryption(encryption)
        #输入2.4G无线的密码
        self.set_route_24g_password(pwd)
        #点击设置按钮
        self.click_save_button()
        #点击保存
        self.click_confirm_button()

    def change_wifi_channel(self, channel):
        """
        修改无线的信道
        输入：channel：中国：1-13;美国：1-11;auto
        """
        #首先点击网络设置
        tmp = NetWorkControl(self.driver)
        tmp.menu_network()
        #再点击无线设置
        self.menu_wirelesssettings()
        #点击更多设置
        self.set_More_settings()
        #输入2.4G无线的信道
        self.set_channel(channel)
        #点击设置按钮
        self.click_save_button()
        #点击保存
        self.click_confirm_button()

    #切换2.4G无线信道，判断，无线网卡连接取出该AP的频率值
    def check_wifi_channel(self,channel,ssid,password,wlan):
        """切换2.4G无线信道，判断，无线网卡连接取出该AP的频率值"""
        #设修改无线的信道
        self.change_wifi_channel(channel)
        #使用无线网卡连接上AP后，取出该AP的频率值
        result = self.connected_AP_Freq(ssid,password,wlan)
        print(result)
        return result

    #修改带宽
    def change_bandwidth(self, width):
        """
        修改带宽
        输入：width：无线频宽,HT20,HT40
        """
        #首先点击网络设置
        tmp = NetWorkControl(self.driver)
        tmp.menu_network()
        #再点击无线设置
        self.menu_wirelesssettings()
        #点击更多设置
        self.set_More_settings()
        #输入2.4G无线的无线频宽
        self.set_bandwidth(width)
        #点击设置按钮
        self.click_save_button()
        #点击保存
        self.click_confirm_button()

    #登录ap的后台，检查带宽
    def check_ap_bandwidth(self, host, user, pwd, width):
        """登录ap的后台，检查带宽"""
        ssh = SSH(host, pwd)
        result = ssh.ssh_cmd(user, "uci show wireless.radio0.htmode")
        if width in result:
            return True
        else:
            return False

    #修改发射功率
    def change_power(self, power):
        """
        修改发射功率
        输入：power：功率值
        """
        #首先点击网络设置
        tmp = NetWorkControl(self.driver)
        tmp.menu_network()
        #再点击无线设置
        self.menu_wirelesssettings()
        #点击更多设置
        self.set_More_settings()
        #输入发射功率
        self.set_power(power)
        #点击设置按钮
        self.click_save_button()
        #点击保存
        self.click_confirm_button()

    #登录ap的后台，检查发射功率
    def check_ap_power(self, host, user, pwd, power):
        """登录ap的后台，发射功率"""
        ssh = SSH(host, pwd)
        result = ssh.ssh_cmd(user, "uci show wireless.radio0.txpower")
        if power in result:
            return True
        else:
            return False

    #修改最大用户数
    def change_max_client_number(self, n):
        """
        修改最大用户数
        输入：n:最大用户数--str和int类型皆可
        """
        #首先点击网络设置
        tmp = NetWorkControl(self.driver)
        tmp.menu_network()
        #再点击无线设置
        self.menu_wirelesssettings()
        #点击更多设置
        self.set_More_settings()
        #输入最大用户数
        self.set_max_client_number(n)
        #点击设置按钮
        self.click_save_button()
        #点击保存
        self.click_confirm_button()

    #登录ap的后台，检查最大用户数
    def check_ap_max_client_number(self, host, user, pwd, n):
        """登录ap的后台，最大用户数"""
        ssh = SSH(host, pwd)
        result = ssh.ssh_cmd(user, "uci show wireless.wlan0.maxassoc")
        if n in result:
            return True
        else:
            return False

    #设置第n个ssid的ssid，加密方式none和wpa，密码(默认的ssid为第0个)
    def config_n_ssid_none_wpa(self, n ,ssid ,mode, password):
        """
        设置第n个ssid的ssid，加密方式，密码
        输入：mode:none,psk2
        """
        #输入第n个ssid名称
        self.set_n_ssid(n, ssid+"-%s"%n)
        #输入第n个ssid的加密方式
        self.set_n_encryption(n, mode)
        #输入第n个ssid的wpa加密密码或不加密
        self.set_n_wpa_password(n, password)

    #设置第n个ssid的ssid，加密方式wep，密码(默认的ssid为第0个)
    def config_n_ssid_wep(self, n ,ssid , password):
        """设置第n个ssid的ssid，加密方式，密码"""
        #输入第n个ssid名称
        self.set_n_ssid(n, ssid+"-%s"%n)
        #输入第n个ssid的加密方式
        self.set_n_encryption(n, "wep+shared")
        #输入第n个ssid的wep加密密码
        self.set_n_wep_password(n, password)




    #添加多个ssid,加密方式none和wpa
    def add_many_ssids_none_wpa(self, n, ssid, mode, password):
        """添加多个ssid"""
        #首先点击网络设置
        tmp = NetWorkControl(self.driver)
        tmp.menu_network()
        #再点击无线设置
        self.menu_wirelesssettings()
        for i in range(1, n+1):
            #点击+号
            self.click_plus_button()
            #设置第n个ssid的ssid，加密方式none和wpa，密码(默认的ssid为第0个)
            self.config_n_ssid_none_wpa(i ,ssid ,mode, password)
        #点击设置按钮
        self.click_save_button()
        #点击保存
        self.click_confirm_button()

    #删除所有的ssid
    def del_all_ssid(self):
        """删除所有的ssid"""
        #首先点击网络设置
        tmp = NetWorkControl(self.driver)
        tmp.menu_network()
        #再点击无线设置
        self.menu_wirelesssettings()
        #依次点击所有的-号
        self.click_all_minus_button()
        #点击设置按钮
        self.click_save_button()
        #点击保存
        self.click_confirm_button()














    ##########################################################################################
    ############以下是高级配置页面操作#############################################################
    #开启/关闭短防护时间间隔
    def change_shortGI(self):
        """
        开启/关闭短防护时间间隔
        """
        #首先点击网络设置
        tmp = NetWorkControl(self.driver)
        tmp.menu_network()
        #再点击无线设置
        self.menu_wirelesssettings()
        #点击高级配置
        self.set_Advanced()
        #点击短防护时间间隔
        self.set_shortGI()
        #点击设置按钮
        self.click_save_button()
        #点击保存
        self.click_confirm_button()

    #登录ap的后台，检查短防护时间间隔
    def check_ap_shortGI(self, host, user, pwd):
        """登录ap的后台，检查短防护时间间隔是否开启"""
        ssh = SSH(host, pwd)
        result = ssh.ssh_cmd(user, "uci show wireless.radio0.shortgi")
        if "1" in result:
            return True
        else:
            return False

    #开启/关闭WDS
    def change_WDS(self):
        """
        开启/关闭WDS
        """
        #首先点击网络设置
        tmp = NetWorkControl(self.driver)
        tmp.menu_network()
        #再点击无线设置
        self.menu_wirelesssettings()
        #点击高级配置
        self.set_Advanced()
        #点击WDS
        self.set_WDS()
        #点击设置按钮
        self.click_save_button()
        #点击保存
        self.click_confirm_button()

    #登录ap的后台，检查WDS是否开启
    def check_ap_WDS(self, host, user, pwd):
        """登录ap的后台，检查WDS是否开启"""
        ssh = SSH(host, pwd)
        result = ssh.ssh_cmd(user, "uci show wireless.wlan0.wds")
        if "1" in result:
            return True
        else:
            return False

    #开启/关闭无线多媒体
    def change_WMM(self):
        """
        开启/关闭无线多媒体
        """
        #首先点击网络设置
        tmp = NetWorkControl(self.driver)
        tmp.menu_network()
        #再点击无线设置
        self.menu_wirelesssettings()
        #点击高级配置
        self.set_Advanced()
        #点击无线多媒体
        self.set_WMM()
        #点击设置按钮
        self.click_save_button()
        #点击保存
        self.click_confirm_button()

    #登录ap的后台，检查无线多媒体是否开启
    def check_ap_WMM(self, host, user, pwd):
        """登录ap的后台，检查无线多媒体是否开启"""
        ssh = SSH(host, pwd)
        result = ssh.ssh_cmd(user, "uci show wireless.wlan0.wmm")
        if "1" in result:
            return True
        else:
            return False

    #开启/关闭无线隔离
    def change_wireless_isolate(self):
        """
        开启/关闭无线隔离
        """
        #首先点击网络设置
        tmp = NetWorkControl(self.driver)
        tmp.menu_network()
        #再点击无线设置
        self.menu_wirelesssettings()
        #点击高级配置
        self.set_Advanced()
        #点击无线隔离
        self.set_wireless_isolate()
        #点击设置按钮
        self.click_save_button()
        #点击保存
        self.click_confirm_button()

    #登录ap的后台，检查无线隔离是否开启
    def check_ap_wireless_isolate(self, host, user, pwd):
        """登录ap的后台，检查无线隔离是否开启"""
        ssh = SSH(host, pwd)
        result = ssh.ssh_cmd(user, "uci show wireless.wlan0.isolate")
        if "1" in result:
            return True
        else:
            return False

    #设置分割阈值
    def change_fragment_threshold(self, value):
        """设置分割阈值"""
         #首先点击网络设置
        tmp = NetWorkControl(self.driver)
        tmp.menu_network()
        #再点击无线设置
        self.menu_wirelesssettings()
        #点击高级配置
        self.set_Advanced()
        #输入分割阈值
        self.set_fragment_threshold(value)
        #点击设置按钮
        self.click_save_button()
        #点击确认
        self.click_confirm_button()

    #登录ap的后台，检查分割阈值
    def check_ap_fragment_threshold(self, host, user, pwd, value):
        """登录ap的后台，检查分割阈值"""
        ssh = SSH(host, pwd)
        result = ssh.ssh_cmd(user, "uci show wireless.radio0.frag")
        if str(value) in result:
            return True
        else:
            return False

    #设置rts阈值
    def change_rts_threshold(self, value):
        """设置rts阈值"""
         #首先点击网络设置
        tmp = NetWorkControl(self.driver)
        tmp.menu_network()
        #再点击无线设置
        self.menu_wirelesssettings()
        #点击高级配置
        self.set_Advanced()
        #输入rts
        self.set_RTS_threshold(value)
        #点击设置按钮
        self.click_save_button()
        #点击确认
        self.click_confirm_button()

    #登录ap的后台，检查rts阈值
    def check_ap_rts_threshold(self, host, user, pwd, value):
        """登录ap的后台，检查rts阈值"""
        ssh = SSH(host, pwd)
        result = ssh.ssh_cmd(user, "uci show wireless.radio0.rts")
        if str(value) in result:
            return True
        else:
            return False

    #获取无线的带宽
    def obtain_width(self):
        #首先点击网络设置
        tmp = NetWorkControl(self.driver)
        tmp.menu_network()
        #再点击无线设置
        self.menu_wirelesssettings()
        #点击更多设置
        self.set_More_settings()
        #获取2.4G无线的无线频宽
        result = self.get_bandwidth()
        return result

    def change_bridge_AP_wifi_encryption_pwd(self,bridge_static_ip,
            bridge_ip, encryption, pwd):
        """
        改变桥接路由的无线加密和密码
        """
        #设置PC的静态IP和桥接的路由的IP端一致
        self.set_eth_ip(data_basic['lan_pc'], bridge_static_ip)

        #登录桥接路由的web端，修改桥接路由的无线加密为none
        self.driver.get("http://{}".format(bridge_ip))
        self.driver.implicitly_wait(20)
        #逻辑类对象，建一个实例
        Lg = LoginBusiness(self.driver)
        #调用实例的登录AP的web界面
        Lg.login(data_basic['superUser'], data_basic['super_defalut_pwd'])
        #刷新页面重新登录ap页面
        Lg.refresh_login_ap()
        #修改桥接路由的无线加密
        self.change_wifi_encryption_pwd(encryption, pwd)