#coding=utf-8
#作者：曾祥卫
#时间：2018.09.20
#描述：状态信息的业务逻辑层

from stateinfo.stateinfo_control import StateInfoControl
from login.login_business import LoginBusiness
import time, subprocess
from data import data

data_basic = data.data_basic()


class StateInfoBusiness(StateInfoControl):

    def __init__(self,driver):
        #继承StateInfoControl类的属性和方法
        StateInfoControl.__init__(self,driver)

    #AP 下载流量-50M
    def run_AP_download_50M(self, ssid, password, wlan, lan):
        #无线网卡连接master ap
        self.connect_DHCP_WPA_AP(ssid, password, wlan)
        #禁用有线网卡
        self.wlan_disable(lan)
        i =0
        while i<3:
            tmp = self.get_ping(data_basic['iperf_ip'])
            if tmp == 0:
                #描述：使用iperf3进行下载
                tmp1 = subprocess.call("iperf3 -c %s -n 50M -R"%data_basic['iperf_ip'], shell=True)
                print (tmp1)
                break
            else:
                self.wlan_enable(lan)
                self.dhcp_release_wlan(wlan)
                self.dhcp_wlan(wlan)
                self.wlan_disable(lan)
                print ("run iperf3 fail,try %s again!"%(i+1))
                i = i+1
                continue
        #启用有线网卡
        self.wlan_enable(lan)
        #使无线网卡释放IP地址
        self.dhcp_release_wlan(wlan)

    #AP 上传流量-50M
    def run_AP_upload_50M(self, ssid, password, wlan, lan):
        #无线网卡连接master ap
        self.connect_DHCP_WPA_AP(ssid, password, wlan)
        #禁用有线网卡
        self.wlan_disable(lan)
        i =0
        while i<3:
            tmp = self.get_ping(data_basic['iperf_ip'])
            if tmp == 0:
                #描述：使用iperf3进行上传
                tmp1 = subprocess.call("iperf3 -c %s -n 50M"%data_basic['iperf_ip'], shell=True)
                print (tmp1)
                break
            else:
                self.wlan_enable(lan)
                self.dhcp_release_wlan(wlan)
                self.dhcp_wlan(wlan)
                self.wlan_disable(lan)
                print ("run iperf3 fail,try %s again!"%(i+1))
                i = i+1
                continue
        #启用有线网卡
        self.wlan_enable(lan)
        #使无线网卡释放IP地址
        self.dhcp_release_wlan(wlan)

    #取出WIFI总上行
    def obtain_wifi_upload(self):
        #点击状态信息设置菜单
        self.menu_stateinfo()
        #取WIFI总上行
        time.sleep(30)
        value, unit = self.get_wifi_upload()
        return value, unit

    #取出WIFI总下行
    def obtain_wifi_download(self):
        #点击状态信息设置菜单
        self.menu_stateinfo()
        #取WIFI总下行
        time.sleep(30)
        value, unit = self.get_wifi_download()
        return value, unit

    #判断WIFI总上行是否正确--50M
    def check_wifi_upload(self, ssid, password, wlan, lan):
        #AP 上传流量-50M
        self.run_AP_upload_50M(ssid, password, wlan, lan)
        #等待30s，刷新页面
        time.sleep(30)
        Lg = LoginBusiness(self.driver)
        Lg.refresh_login_ap()
        #取出WIFI总上行
        value, unit = self.obtain_wifi_upload()
        if unit == "MB":
            if int(value) >= 50:
                return True
        return False

    #判断WIFI总下行是否正确--50M
    def check_wifi_download(self, ssid, password, wlan, lan):
        #AP 下载流量-50M
        self.run_AP_download_50M(ssid, password, wlan, lan)
        #等待30s，刷新页面
        time.sleep(30)
        Lg = LoginBusiness(self.driver)
        Lg.refresh_login_ap()
        #取出WIFI总下行
        value, unit = self.obtain_wifi_download()
        if unit == "MB":
            if int(value) >= 50:
                return True
        return False

    #获取当前模式
    def obtain_AP_current_mode(self):
        #点击状态信息设置菜单
        self.menu_stateinfo()
        #取当前模式
        time.sleep(5)
        result = self.get_current_mode()
        return result

    #获取无线用户数
    def obtain_AP_wireless_client(self):
        #点击状态信息设置菜单
        self.menu_stateinfo()
        #取无线用户数
        time.sleep(30)
        result = self.get_wireless_client()
        return result

    #判断无线用户数是否正确
    def check_AP_wireless_client(self,ssid, wlan, wifi_encryption, password=None):
        #使用无线网卡连接ap
        self.client_connect_ssid(ssid, wlan, wifi_encryption, password)
        #等待30s，刷新页面
        time.sleep(30)
        Lg = LoginBusiness(self.driver)
        Lg.refresh_login_ap()
        #获取无线用户数
        result = self.obtain_AP_wireless_client()
        #无线网卡断开连接
        self.disconnect_ap()
        return result



    #获取AP的mac地址--为WAN口的mac地址
    def obtain_AP_MAC_address(self):
        #点击状态信息设置菜单
        self.menu_stateinfo()
        #取MAC地址
        result = self.get_MAC_address()
        return result

    #判断AP的mac地址是否正确
    def check_AP_MAC_address(self, host, user, pwd):
        #获取AP的mac地址--为WAN口的mac地址
        web_mac = self.obtain_AP_MAC_address()
        #从AP后台取出接口eth1（即WAN口的mac地址）
        ssh_mac = self.get_router_mac(host, user, pwd)
        if web_mac.upper() == ssh_mac.upper():
            return True
        else:
            return False

    #获取设备型号
    def obtain_AP_equipment_model(self):
        #点击状态信息设置菜单
        self.menu_stateinfo()
        #取设备型号
        result = self.get_equipment_model()
        return result

    #获取固件版本
    def obtain_AP_firmware_version(self):
        #点击状态信息设置菜单
        self.menu_stateinfo()
        #获取固件版本
        result = self.get_firmware_version()
        return result

    #获取2.4G的ssid
    def obtain_AP_24g_ssid(self):
        #点击状态信息设置菜单
        self.menu_stateinfo()
        #获取2.4G的ssid
        result = self.get_24g_ssid()
        return result

    #获取外网的IP获取方式
    def obtain_WAN_IP_generation(self):
        #点击状态信息设置菜单
        self.menu_stateinfo()
        #获取IP获取方式
        result = self.get_WAN_IP_generation()
        return result

    #获取IP地址
    def obtain_WAN_IP_address(self):
        #点击状态信息设置菜单
        self.menu_stateinfo()
        #获取IP地址
        result = self.get_WAN_IP_address()
        return result







