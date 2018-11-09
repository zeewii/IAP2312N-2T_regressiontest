#coding=utf-8
#作者：曾祥卫
#时间：2018.09.19
#描述：模式设置的业务层,包含所有的测试步骤

#BUG:有时候点击设置向导最后的完成按钮后，页面会马上跳到登录页面，而无法完成设置向导的配置。


from workmode.workmode_control import WorkModeControl
from data import data
from connect.ssh import SSH
import time, subprocess
from login.login_business import LoginBusiness
from network.lansettings.lansettings_business import LanSettingsBusiness

data_basic = data.data_basic()
data_login = data.data_login()
data_wireless = data.data_wireless()

class WorkModeBusiness(WorkModeControl):

    def __init__(self,driver):
        #继承WorkModeControl类的属性和方法
        WorkModeControl.__init__(self,driver)

    def check_after_workmode_normal(self, ssid, wlan, wifi_encryption, password=None, internet_ip="180.76.76.76"):
        """
        判断运行模式设置后，AP正常：能上网，无线网卡能够连接上AP的SSID
        """
        #禁用有线网卡
        self.networkcard_disable()
        #无线网卡能够连接上AP的SSID
        result2 = self.client_connect_ssid(ssid, wlan, wifi_encryption, password)
        #无线网卡获取IP地址
        self.dhcp_wlan(wlan)
        time.sleep(60)
        #AP是否能够上网
        result1 = self.get_ping(internet_ip)
        #result1 = self.get_ping("www.baidu.com")
        #释放无线网卡的ip
        self.dhcp_release_wlan(wlan)
        #断开无线网卡
        self.disconnect_ap()
        #最后启用有线网卡
        self.networkcard_enable()
        return result1, result2

    def check_clientmode_normal(self, ssid, lan, wlan, internet_ip="180.76.76.76"):
        """
        判断client模式设置后，AP正常：PC的有线能上网，无线网卡不能够扫描到原来AP的SSID
        """
        #取消给网卡固定ip
        self.remove_eth_ip(lan)
        #有线网卡获取ip
        self.dhcp_wlan(lan)
        #有线是否能够上网
        result1 = self.get_ping(internet_ip)
        #无线网卡不能扫描到原来的ssid
        result2 = self.ssid_scan_result(ssid, wlan)
        return result1, result2

    def check_apmode_normal(self, pc_pwd, eth, ip, netmask, gateway):
        """
        判断AP模式设置后，AP正常：PC的有线能上网
        """
        #指定PC接口的ip，掩码，网关，判断client能够上网
        tmp = LanSettingsBusiness(self.driver)
        result = tmp.check_access_internet_after_change_client_ip_netmask_gw(pc_pwd, eth, ip, netmask, gateway)
        return result

    def check_apmode_after_workmode_normal(self, ssid, wlan, wifi_encryption, pc_pwd,
            ip, netmask, gateway, password=None):
        """
        判断运行模式设置后，AP正常：能上网，无线网卡能够连接上AP的SSID
        """
        #禁用有线网卡
        self.networkcard_disable()
        #无线网卡能够连接上AP的SSID
        result2 = self.client_connect_ssid(ssid, wlan, wifi_encryption, password)
        #指定PC wlan接口的ip，掩码，网关，判断client能够上网
        tmp = LanSettingsBusiness(self.driver)
        #指定PC接口的ip和掩码
        subprocess.call('echo %s |sudo -S ifconfig %s %s netmask %s'%(pc_pwd, wlan, ip, netmask), shell=True)
        time.sleep(2)
        #然后设置网关
        subprocess.call('echo %s |sudo -S route add default gw %s'%(pc_pwd, gateway), shell=True)
        time.sleep(60)
        #有线是否能够上网
        result1 = self.get_ping("180.76.76.76")
        #去掉ip
        self.dhcp_release_wlan(wlan)
        #去掉网关
        subprocess.call('echo %s |sudo -S route del default'%(pc_pwd), shell=True)
        time.sleep(2)
        #断开无线网卡
        self.disconnect_ap()
        #最后启用有线网卡
        self.networkcard_enable()
        return result1, result2

    def change_workmode_to_route_WANdhcp(self, ssid, encryption_mode,
            password, width, channel):
        """
        修改工作模式为路由模式,外网设置dhcp模式
        """
        for i in range(3):
            #点击工作模式菜单
            self.menu_workmode()
            #选择路由模式
            self.set_mode("route")
            time.sleep(10)
            #外网设置点击dhcp
            self.set_route_WAN_dhcp()
            #点击下一步
            self.click_next_button()
            #点击下一步
            self.click_next_button()
            #无线设置
            self.set_route_24g_ssid(ssid)
            self.set_route_24g_encryption(encryption_mode)
            self.set_route_24g_password(password)
            self.set_route_24g_bandwidth(width)
            self.set_route_24g_channel(channel)
            #点击下一步
            self.click_next_button()
            #点击完成
            self.click_finish_button()
            time.sleep(5)
            if self.check_waitbar_displayed():
                time.sleep(25)
                print("set route mode successfull!")
                break
            else:
                Lg = LoginBusiness(self.driver)
                #刷新页面重新登录ap页面
                Lg.refresh_login_ap()

    def change_workmode_to_route_WANstaticIP(self, wan_ip, netmask,
            gateway, dns, ssid, encryption_mode, password, width, channel):
        """
        修改工作模式为路由模式,外网设置static IP模式
        """
        for i in range(3):
            #点击工作模式菜单
            self.menu_workmode()
            #选择路由模式
            self.set_mode("route")
            time.sleep(10)
            #外网设置点击静态IP按钮
            self.set_route_WAN_staticIP()
            #输入静态ip的ip地址
            self.set_route_WAN_staticIP_IP(wan_ip)
            #输入静态ip的子网掩码
            self.set_route_WAN_staticIP_netmask(netmask)
            #输入静态ip的gateway
            self.set_route_WAN_staticIP_gateway(gateway)
            #输入静态ip的dns
            self.set_route_WAN_staticIP_dns(dns)
            #点击下一步
            self.click_next_button()
            #点击下一步
            self.click_next_button()
            #无线设置
            self.set_route_24g_ssid(ssid)
            self.set_route_24g_encryption(encryption_mode)
            self.set_route_24g_password(password)
            self.set_route_24g_bandwidth(width)
            self.set_route_24g_channel(channel)
            #点击下一步
            self.click_next_button()
            #点击完成
            self.click_finish_button()
            time.sleep(5)
            if self.check_waitbar_displayed():
                time.sleep(25)
                print("set route mode successfull!")
                break
            else:
                Lg = LoginBusiness(self.driver)
                #刷新页面重新登录ap页面
                Lg.refresh_login_ap()

    def change_workmode_to_route_WANpppoe(self, pppoe_user,
            pppoe_password, ssid, encryption_mode, password, width, channel):
        """
        修改工作模式为路由模式,外网设置pppoe模式
        """
        for i in range(3):
            #点击工作模式菜单
            self.menu_workmode()
            #选择路由模式
            self.set_mode("route")
            time.sleep(10)
            #外网设置点击pppoe按钮
            self.set_route_WAN_pppoe()
            #输入输入pppoe的用户名
            self.set_route_WAN_pppoe_user(pppoe_user)
            #输入pppoe的密码
            self.set_route_WAN_pppoe_password(pppoe_password)
            #点击下一步
            self.click_next_button()
            #点击下一步
            self.click_next_button()
            #无线设置
            self.set_route_24g_ssid(ssid)
            self.set_route_24g_encryption(encryption_mode)
            self.set_route_24g_password(password)
            self.set_route_24g_bandwidth(width)
            self.set_route_24g_channel(channel)
            #点击下一步
            self.click_next_button()
            #点击完成
            self.click_finish_button()
            time.sleep(5)
            if self.check_waitbar_displayed():
                time.sleep(25)
                print("set route mode successfull!")
                break
            else:
                Lg = LoginBusiness(self.driver)
                #刷新页面重新登录ap页面
                Lg.refresh_login_ap()

    def change_workmode_to_ap_LANstaticIP(self, ip, netmask, ssid, encryption_mode,
            password, width):
        """
        修改工作模式为ap模式,内网设置静态IP
        """
        for i in range(3):
            #点击工作模式菜单
            self.menu_workmode()
            #选择ap模式
            self.set_mode("ap")
            time.sleep(10)
            #内网设置点击静态IP按钮
            self.set_AP_LAN_staticIP()
            #输入静态IP的ip地址
            self.set_AP_LAN_staticIP_ip(ip)
            #输入静态IP的子网掩码
            self.set_AP_LAN_staticIP_netmask(netmask)
            #输入静态ip的gateway
            self.set_AP_LAN_staticIP_gateway("")
            #点击下一步
            self.click_next_button()
            # #防止AP模式下有时候点击下一步没有后跳到无线配置页面，判断web页面上是否有AP模式下的静态IP的元素
            # for i in range(3):
            #     if not self.check_AP_LAN_staticIP_in_webpage():
            #         #再次点击下一步
            #         self.click_next_button()
            #     else:
            #         break
            #无线设置
            self.set_AP_24g_ssid(ssid)
            self.set_AP_24g_encryption(encryption_mode)
            self.set_AP_24g_password(password)
            self.set_AP_24g_bandwidth(width)
            #点击下一步
            self.click_next_button()
            #点击完成
            self.click_finish_button()
            time.sleep(5)
            if self.check_waitbar_displayed():
                time.sleep(85)
                break
            else:
                Lg = LoginBusiness(self.driver)
                #刷新页面重新登录ap页面
                Lg.refresh_login_ap()

        #指定有线网卡的固定ip--能够访问ap的webpage
        self.dhcp_release_wlan(data_basic['lan_pc'])
        self.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])
        print("set ap mode successfull!")

    #关闭AP的eth1端口，以免她来分配ip地址，和桥接的dhcp server相冲突
    def down_ap_eth1(self, host, user, pwd):
        ssh = SSH(host, pwd)
        ssh.ssh_cmd(user, "ifconfig eth1 down")

    def change_workmode_to_bridge_LANstaticIP(self, ip, netmask,
            bridge_essid, bridge_encryption_mode,bridge_bssid,
            bridge_pwd, ssid, encryption_mode,
            password, user, pwd):
        """
        修改工作模式为bridge模式,内网设置静态IP
        """
        for i in range(3):
            #点击工作模式菜单
            self.menu_workmode()
            #选择桥接模式
            self.set_mode("bridge")
            time.sleep(10)
            #内网设置点击静态IP按钮
            self.set_bridge_LAN_staticIP()
            #输入静态IP的ip地址
            self.set_bridge_LAN_staticIP_ip(ip)
            #输入静态IP的子网掩码
            self.set_bridge_LAN_staticIP_netmask(netmask)
            #输入静态ip的gateway
            self.set_bridge_LAN_staticIP_gateway("")
            #点击下一步
            self.click_next_button()

            #桥接设置
            # #点击扫描
            # self.click_bridge_bridge_scan_button()
            # time.sleep(10)
            # #扫描页面中，根据扫描到的ap的mac地址点击对应的操作按钮
            # self.set_bridge_bridge_scan_operat(bridge_bssid)
            #桥接设置输入要桥接的ssid
            self.set_bridge_bridge_ssid(bridge_essid)
            #桥接设置要桥接的无线的加密方式
            self.set_bridge_bridge_encryption(bridge_encryption_mode)
            #输入桥接ap的无线密码
            self.set_bridge_bridge_password(bridge_pwd)
            #桥接设置要桥接的对端无线mac地址
            self.set_bridge_bridge_BSSID(bridge_bssid)
            #点击下一步
            self.click_next_button()

            #无线设置
            self.set_bridge_24g_ssid(ssid)
            self.set_bridge_24g_encryption(encryption_mode)
            self.set_bridge_24g_password(password)
            #点击下一步
            self.click_next_button()
            #点击完成
            self.click_finish_button()
            time.sleep(5)
            if self.check_waitbar_displayed():
                time.sleep(85)
                break
            else:
                Lg = LoginBusiness(self.driver)
                #刷新页面重新登录ap页面
                Lg.refresh_login_ap()

        #指定有线网卡的固定ip--能够访问ap的webpage
        self.dhcp_release_wlan(data_basic['lan_pc'])
        self.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])
        #关闭AP的eth1端口，以免她来分配ip地址，和桥接的dhcp server相冲突
        self.down_ap_eth1(ip, user, pwd)
        print("set bridge mode successfull!")





    def change_workmode_to_client_LANstaticIP(self, ip, netmask,
            bridge_essid, bridge_encryption_mode,bridge_bssid,
            bridge_pwd, user, pwd):
        """
        修改工作模式为client模式,内网设置静态IP
        """
        for i in range(3):
            #点击工作模式菜单
            self.menu_workmode()
            #选择桥接模式
            self.set_mode("client")
            time.sleep(10)
            #内网设置点击静态IP按钮
            self.set_client_LAN_staticIP()
            #输入静态IP的ip地址
            self.set_client_LAN_staticIP_ip(ip)
            #输入静态IP的子网掩码
            self.set_client_LAN_staticIP_netmask(netmask)
            #输入静态ip的gateway
            self.set_client_LAN_staticIP_gateway("")
            #点击下一步
            self.click_next_button()

            #桥接设置
            # #点击扫描
            # self.click_bridge_bridge_scan_button()
            # time.sleep(10)
            # #扫描页面中，根据扫描到的ap的mac地址点击对应的操作按钮
            # self.set_bridge_bridge_scan_operat(bridge_bssid)
            #桥接设置输入要桥接的ssid
            self.set_client_bridge_ssid(bridge_essid)
            #桥接设置要桥接的无线的加密方式
            self.set_client_bridge_encryption(bridge_encryption_mode)
            #输入桥接ap的无线密码
            self.set_client_bridge_password(bridge_pwd)
            #桥接设置要桥接的对端无线mac地址
            self.set_client_bridge_BSSID(bridge_bssid)
            #点击下一步
            self.click_next_button()

            #点击完成
            self.click_finish_button()
            time.sleep(5)
            if self.check_waitbar_displayed():
                time.sleep(85)
                break
            else:
                Lg = LoginBusiness(self.driver)
                #刷新页面重新登录ap页面
                Lg.refresh_login_ap()

        #指定有线网卡的固定ip--能够访问ap的webpage
        self.dhcp_release_wlan(data_basic['lan_pc'])
        self.set_eth_ip(data_basic['lan_pc'], data_basic['static_PC_ip'])
        #关闭AP的eth1端口，以免她来分配ip地址，和桥接的dhcp server相冲突
        self.down_ap_eth1(ip, user, pwd)
        print("set client mode successfull!")


    #登录ap后台，判断ap的工作模式
    def check_DUT_workmode(self, host ,user, pwd):
        ssh = SSH(host, pwd)
        result = ssh.ssh_cmd(user, "uci show network.workmode")
        return result










    ############以下是非路由模式下，内网为上级dhcp分配得到###########################################
    def change_workmode_to_bridge_LANDHCP(self,
            bridge_essid, bridge_encryption_mode,bridge_bssid,
            bridge_pwd, ssid, encryption_mode,
            password, user, pwd):
        """
        修改工作模式为bridge模式,内网设置动态获取
        """
        for i in range(3):
            #点击工作模式菜单
            self.menu_workmode()
            #选择桥接模式
            self.set_mode("bridge")
            time.sleep(10)
            #内网设置点击点击动态获取按钮
            self.set_bridge_LAN_dhcp()
            #点击下一步
            self.click_next_button()

            #桥接设置
            # #点击扫描
            # self.click_bridge_bridge_scan_button()
            # time.sleep(10)
            # #扫描页面中，根据扫描到的ap的mac地址点击对应的操作按钮
            # self.set_bridge_bridge_scan_operat(bridge_bssid)
            #桥接设置输入要桥接的ssid
            self.set_bridge_bridge_ssid(bridge_essid)
            #桥接设置要桥接的无线的加密方式
            self.set_bridge_bridge_encryption(bridge_encryption_mode)
            #输入桥接ap的无线密码
            self.set_bridge_bridge_password(bridge_pwd)
            #桥接设置要桥接的对端无线mac地址
            self.set_bridge_bridge_BSSID(bridge_bssid)
            #点击下一步
            self.click_next_button()

            #无线设置
            self.set_bridge_24g_ssid(ssid)
            self.set_bridge_24g_encryption(encryption_mode)
            self.set_bridge_24g_password(password)
            #点击下一步
            self.click_next_button()
            #点击完成
            self.click_finish_button()
            time.sleep(5)
            if self.check_waitbar_displayed():
                time.sleep(85)
                break
            else:
                Lg = LoginBusiness(self.driver)
                #刷新页面重新登录ap页面
                Lg.refresh_login_ap()

        #设置PC的静态IP和桥接的路由的IP端一致
        self.dhcp_release_wlan(data_basic['lan_pc'])
        self.set_eth_ip(data_basic['lan_pc'], data_wireless['bridge_static_ip'])
        #非路由模式下，获取ap的当前ip地址
        ap_ip = self.get_ap_ip(data_wireless['bridge_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'], data_basic['ap_brlan_mac'])
        #关闭AP的eth1端口，以免她来分配ip地址，和桥接的dhcp server相冲突
        self.down_ap_eth1(ap_ip, user, pwd)
        print("set bridge mode successfull!")
        return ap_ip

    def change_workmode_to_client_LANDHCP(self,
            bridge_essid, bridge_encryption_mode,bridge_bssid,
            bridge_pwd, user, pwd):
        """
        修改工作模式为client模式,内网设置动态获取
        """
        for i in range(3):
            #点击工作模式菜单
            self.menu_workmode()
            #选择桥接模式
            self.set_mode("client")
            time.sleep(10)
            #内网设置点击点击动态获取按钮
            self.set_client_LAN_dhcp()
            #点击下一步
            self.click_next_button()

            #桥接设置
            # #点击扫描
            # self.click_bridge_bridge_scan_button()
            # time.sleep(10)
            # #扫描页面中，根据扫描到的ap的mac地址点击对应的操作按钮
            # self.set_bridge_bridge_scan_operat(bridge_bssid)
            #桥接设置输入要桥接的ssid
            self.set_client_bridge_ssid(bridge_essid)
            #桥接设置要桥接的无线的加密方式
            self.set_client_bridge_encryption(bridge_encryption_mode)
            #输入桥接ap的无线密码
            self.set_client_bridge_password(bridge_pwd)
            #桥接设置要桥接的对端无线mac地址
            self.set_client_bridge_BSSID(bridge_bssid)
            #点击下一步
            self.click_next_button()

            #点击完成
            self.click_finish_button()
            time.sleep(5)
            if self.check_waitbar_displayed():
                time.sleep(85)
                break
            else:
                Lg = LoginBusiness(self.driver)
                #刷新页面重新登录ap页面
                Lg.refresh_login_ap()

        #设置PC的静态IP和桥接的路由的IP端一致
        self.dhcp_release_wlan(data_basic['lan_pc'])
        self.set_eth_ip(data_basic['lan_pc'], data_wireless['bridge_static_ip'])
        #非路由模式下，获取ap的当前ip地址
        ap_ip = self.get_ap_ip(data_wireless['bridge_ip'], data_basic['ssh_user'],
            data_basic['ssh_pwd'], data_basic['ap_brlan_mac'])
        #关闭AP的eth1端口，以免她来分配ip地址，和桥接的dhcp server相冲突
        self.down_ap_eth1(ap_ip, user, pwd)
        print("set bridge mode successfull!")
        return ap_ip

