#coding=utf-8
#作者：曾祥卫
#时间：2018.09.19
#描述：模式设置的控制层

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import Select
from publicControl.public_control import PublicControl
import time
from data import data

class WorkModeControl(PublicControl):

    def __init__(self,driver):
        #继承PublicControl类的属性和方法
        PublicControl.__init__(self,driver)


    def menu_workmode(self):
        """
        点击模式设置菜单
        """
        try:
            self.driver.find_element_by_css_selector(".setup_lang.span_lang").click()
            self.driver.implicitly_wait(10)
            time.sleep(2)
        except Exception as e:
            raise Exception("Web page click 'workmode menu' element fail! The reason is %s"%e)


    def set_mode(self, mode):
        """
        描述：点击路由设置菜单
        输入：mode：route，ap，bridge, client
        """
        try:
            elements = self.driver.find_elements_by_css_selector(".col-xs-3.img_Guide")
            if mode == "route":
                element = elements[0]
            elif mode == "ap":
                element = elements[1]
            elif mode == "bridge":
                element = elements[2]
            elif mode == "client":
                element = elements[3]
            else:
                print("Please input route, ap, birge, client mode!")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'mode type' element fail! The reason is %s"%e)


    ###########################################################################################
    ####################以下是路由模式设置页面的操作#################################################
    def set_route_WAN_pppoe(self):
        """
        点击pppoe按钮
        """
        try:
            self.driver.find_element_by_css_selector(".span_pppoe.choose.choose_span.pppoe_lang").click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'route pppoe button' element fail! The reason is %s"%e)

    def set_route_WAN_staticIP(self):
        """
        点击静态IP按钮
        """
        try:
            self.driver.find_element_by_css_selector(".span_static.choose.choose_span.static_lang").click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'route staticIP button' element fail! The reason is %s"%e)

    def set_route_WAN_dhcp(self):
        """
        点击动态获取按钮
        """
        try:
            self.driver.find_element_by_css_selector(".span_dhcp.choose.choose_span.dhcp_lang").click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'route dhcp button' element fail! The reason is %s"%e)

    def set_route_WAN_pppoe_user(self, pppoe_user):
        """
        输入pppoe的用户名
        输入：pppoe_user：pppoe的用户名
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".etext.luyou_wan_username")
            tmp.clear()
            tmp.send_keys(pppoe_user)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'route pppoe user' element fail! The reason is %s"%e)

    def set_route_WAN_pppoe_password(self, pppoe_password):
        """
        输入pppoe的密码
        输入：pppoe_password：pppoe的密码
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".etext.luyou_wan_pwd")
            tmp.clear()
            tmp.send_keys(pppoe_password)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'route pppoe password' element fail! The reason is %s"%e)

    def set_route_WAN_pppoe_server(self, pppoe_server):
        """
        输入pppoe的服务名称
        输入：pppoe_server：pppoe的服务名称
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".etext.luyou_wan_service")
            tmp.clear()
            tmp.send_keys(pppoe_server)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'route pppoe server name' element fail! The reason is %s"%e)

    def set_route_WAN_staticIP_IP(self, ip):
        """
        输入静态ip的ip地址
        输入：ip：ip地址
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".text.luyou_wan_ip")
            tmp.clear()
            tmp.send_keys(ip)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'route staticIP ip address' element fail! The reason is %s"%e)


    def set_route_WAN_staticIP_netmask(self, netmask):
        """
        输入静态ip的子网掩码
        输入：netmask：子网掩码
        """
        try:
            element = self.driver.find_element_by_css_selector(".utext.luypi_wan_netmask.client_mask_01")
            Select(element).select_by_value(netmask)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'route staticIP netmask' element fail! The reason is %s"%e)

    def set_route_WAN_staticIP_gateway(self, gateway):
        """
        输入静态ip的gateway
        输入：gateway：gateway地址
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".text.luypi_wan_gateway")
            tmp.clear()
            tmp.send_keys(gateway)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'route staticIP gateway' element fail! The reason is %s"%e)

    def set_route_WAN_staticIP_dns(self, dns):
        """
        输入静态ip的dns
        输入：dns：dns地址
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".dns_text.utext.liyou_wan_dns")
            tmp.clear()
            tmp.send_keys(dns)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'route staticIP dns' element fail! The reason is %s"%e)

    def set_route_WAN_dhcp_dns(self, dns):
        """
        输入dhcp的dns
        输入：dns：dns地址
        """
        try:
            tmp = self.driver.find_element_by_xpath(".//*[@id='Pattern_luyou']/div[3]/div[2]/table[3]/tbody/tr[4]/td[2]/input")
            tmp.clear()
            tmp.send_keys(dns)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'route dhcp dns' element fail! The reason is %s"%e)

    def set_route_LAN_ip(self, ip):
        """
        输入内网设置的ip地址
        输入：ip：ip地址
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".text.luyou_lan_ip")
            tmp.clear()
            tmp.send_keys(ip)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'route LAN ip' element fail! The reason is %s"%e)

    def set_route_LAN_netmask(self, netmask):
        """
        输入内网设置的子网掩码
        输入：netmask：子网掩码
        """
        try:
            element = self.driver.find_element_by_css_selector(".utext.luyou_lan_netmask.client_mask_01")
            Select(element).select_by_value(netmask)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'route LAN netmask' element fail! The reason is %s"%e)


    def set_route_24g_ssid(self, ssid):
        """
        输入2.4G无线的ssid
        输入：ssid
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".empty_text.utext.luyou_24G_ssid.words_kpng")
            tmp.clear()
            tmp.send_keys(ssid)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'route 2.4G ssid' element fail! The reason is %s"%e)

    def set_route_24g_encryption(self, mode):
        """
        输入2.4G无线的加密方式
        输入：mode：加密方式:none,psk2,wep+shared
        """
        try:
            element = self.driver.find_element_by_css_selector(".utext.luyou_24G_encryption.client_mask_01.encryption_choose.encryptionChoose_lang")
            Select(element).select_by_value(mode)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'route 2.4G encryption' element fail! The reason is %s"%e)

    def set_route_24g_password(self, pwd):
        """
        输入2.4G无线的密码
        输入：pwd：无线的密码
        """
        try:
            #wpa加密
            tmp = self.driver.find_element_by_css_selector(".key8_64.utext.luyou_24G_key.key_choose.key_pwd")
            tmp.clear()
            tmp.send_keys(pwd)
            self.driver.implicitly_wait(10)
        except:
            #wep加密
            tmp = self.driver.find_element_by_css_selector(".key1_pwd.utext.luyou_24G_key1.key1_choose")
            tmp.clear()
            tmp.send_keys(pwd)
            self.driver.implicitly_wait(10)

    def set_route_24g_bandwidth(self, width):
        """
        输入2.4G无线的无线频宽
        输入：width：无线频宽,HT20,HT40
        """
        try:
            element = self.driver.find_element_by_css_selector(".utext.luyou_24G_htmode")
            Select(element).select_by_value(width)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'route 2.4G bandwidth' element fail! The reason is %s"%e)

    def set_route_24g_country(self, country):
        """
        输入2.4G无线的国家
        输入：country：CN,US
        """
        try:
            element = self.driver.find_element_by_css_selector(".utext.luyou_24G_country.country_select_24.countryChoose_lang")
            Select(element).select_by_value(country)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'route 2.4G country' element fail! The reason is %s"%e)

    def set_route_24g_channel(self, channel):
        """
        输入2.4G无线的信道
        输入：channel：中国：1-13;美国：1-11
        """
        try:
            element = self.driver.find_element_by_css_selector(".utext.luyou_24G_channel.channel_select_24")
            Select(element).select_by_value(str(channel))
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'route 2.4G channel' element fail! The reason is %s"%e)



    ###########################################################################################
    ####################以下是AP模式设置页面的操作##################################################
    def set_AP_LAN_staticIP(self):
        """
        点击静态IP按钮
        """
        try:
            self.driver.find_element_by_css_selector(".static_ap_lan.span.span_apLn.choose_span.static_lang").click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'AP staticIP button' element fail! The reason is %s"%e)

    def check_AP_LAN_staticIP_in_webpage(self):
        """
        判断web页面上是否有AP模式下的静态IP的元素
        输出：True，False
        """
        try:
            self.driver.find_element_by_css_selector(".static_ap_lan.span.span_apLn.choose_span.static_lang")
            return True
        except:
            return False




    def set_AP_LAN_dhcp(self):
        """
        点击动态获取按钮
        """
        try:
            self.driver.find_element_by_css_selector(".dhcp_ap_lan.span.span_apLn.choose_span.dhcp_lang").click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'AP dhcp button' element fail! The reason is %s"%e)

    def set_AP_LAN_staticIP_ip(self, ip):
        """
        输入静态IP的ip地址
        输入：ip：ip地址
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".text.ap_lan_ip")
            tmp.clear()
            tmp.send_keys(ip)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'AP LAN staticIP ip' element fail! The reason is %s"%e)

    def set_AP_LAN_staticIP_netmask(self, netmask):
        """
        输入静态IP的子网掩码
        输入：netmask：子网掩码
        """
        try:
            element = self.driver.find_element_by_css_selector(".utext.ap_lan_netmask")
            Select(element).select_by_value(netmask)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'AP LAN staticIP netmask' element fail! The reason is %s"%e)

    def set_AP_LAN_staticIP_gateway(self, gateway):
        """
        输入静态ip的gateway
        输入：gateway：gateway地址
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".text.gateway_lan_ap")
            tmp.clear()
            tmp.send_keys(gateway)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'AP LAN staticIP gateway' element fail! The reason is %s"%e)

    def set_AP_LAN_dns(self, dns):
        """
        输入的dns--静态ip和动态获取可通用
        输入：dns：dns地址
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".dns_text.utext.dns_lan_ap")
            tmp.clear()
            tmp.send_keys(dns)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'AP LAN staticIP dns' element fail! The reason is %s"%e)

    def set_AP_24g_ssid(self, ssid):
        """
        输入2.4G无线的ssid
        输入：ssid
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".utext.words_kpng.ap_24G_ssid")
            tmp.clear()
            tmp.send_keys(ssid)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'AP 2.4G ssid' element fail! The reason is %s"%e)

    def set_AP_24g_encryption(self, mode):
        """
        输入2.4G无线的加密方式
        输入：mode：加密方式:none,psk2,wep+shared
        """
        try:
            element = self.driver.find_element_by_css_selector(".utext.ap_24G_encryption.encryption_choose.encryptionChoose_lang")
            Select(element).select_by_value(mode)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'AP 2.4G encryption' element fail! The reason is %s"%e)

    def set_AP_24g_password(self, pwd):
        """
        输入2.4G无线的密码
        输入：pwd：无线的密码
        """
        try:
            #wpa加密
            tmp = self.driver.find_element_by_css_selector(".key8_64.utext.ap_24G_key.key_choose.key_pwd")
            tmp.clear()
            tmp.send_keys(pwd)
            self.driver.implicitly_wait(10)
        except:
            #wep加密
            tmp = self.driver.find_element_by_css_selector(".key1_pwd.utext.ap_24G_key1.key1_choose")
            tmp.clear()
            tmp.send_keys(pwd)
            self.driver.implicitly_wait(10)

    def set_AP_24g_bandwidth(self, width):
        """
        输入2.4G无线的无线频宽
        输入：width：无线频宽,HT20,HT40
        """
        try:
            element = self.driver.find_element_by_css_selector(".utext.ap_24G_htmode")
            Select(element).select_by_value(width)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'AP 2.4G bandwidth' element fail! The reason is %s"%e)

    def set_AP_24g_country(self, country):
        """
        输入2.4G无线的国家
        输入：country：CN,US
        """
        try:
            element = self.driver.find_element_by_css_selector(".utext.ap_24G_country.country_select_24.countryChoose_lang")
            Select(element).select_by_value(country)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'AP 2.4G country' element fail! The reason is %s"%e)

    def set_AP_24g_channel(self, channel):
        """
        输入2.4G无线的信道
        输入：channel：中国：1-13;美国：1-11
        """
        try:
            element = self.driver.find_element_by_css_selector(".utext.ap_24G_channel.channel_select_24")
            Select(element).select_by_value(channel)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'AP 2.4G channel' element fail! The reason is %s"%e)



    ###########################################################################################
    ####################以下是网桥模式设置页面的操作#################################################
    def set_bridge_LAN_staticIP(self):
        """
        点击静态IP按钮
        """
        try:
            self.driver.find_element_by_css_selector(".static_wq_lan.span.span_apLn_wq.choose_span.static_lang").click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'bridge staticIP button' element fail! The reason is %s"%e)

    def set_bridge_LAN_dhcp(self):
        """
        点击动态获取按钮
        """
        try:
            self.driver.find_element_by_css_selector(".dhcp_wq_lan.span.span_apLn_wq.choose_span.dhcp_lang").click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'bridge dhcp button' element fail! The reason is %s"%e)

    def set_bridge_LAN_staticIP_ip(self, ip):
        """
        输入静态IP的ip地址
        输入：ip：ip地址
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".text.ip_lan_wqq")
            tmp.clear()
            tmp.send_keys(ip)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'bridge LAN staticIP ip' element fail! The reason is %s"%e)

    def set_bridge_LAN_staticIP_netmask(self, netmask):
        """
        输入静态IP的子网掩码
        输入：netmask：子网掩码
        """
        try:
            element = self.driver.find_element_by_css_selector(".utext.netmask_lan_wqq")
            Select(element).select_by_value(netmask)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'bridge LAN staticIP netmask' element fail! The reason is %s"%e)

    def set_bridge_LAN_staticIP_gateway(self, gateway):
        """
        输入静态ip的gateway
        输入：gateway：gateway地址
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".text.gateway_lan_wq")
            tmp.clear()
            tmp.send_keys(gateway)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'bridge LAN staticIP gateway' element fail! The reason is %s"%e)

    def set_bridge_LAN_dns(self, dns):
        """
        输入的dns--静态ip和动态获取可通用
        输入：dns：dns地址
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".dns_text.utext.dns_lan_wq")
            tmp.clear()
            tmp.send_keys(dns)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'bridge LAN staticIP dns' element fail! The reason is %s"%e)

    def set_bridge_bridge_connection_mode(self, mode):
        """
        桥接设置选择桥接连接模式
        输入：mode:pTop_qj_wq,roam_qj_wq
        """
        try:
            element = self.driver.find_element_by_css_selector(".utext.netmask_lan_wqq")
            Select(element).select_by_value(mode)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'bridge bridge setting connection mode' element fail! The reason is %s"%e)


    def set_bridge_bridge_ssid(self, ssid):
        """
        桥接设置输入要桥接的ssid
        输入：ssid
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".utext.words_kpng.ssid_qj_wq")
            tmp.clear()
            tmp.send_keys(ssid)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'bridge bridge setting ssid' element fail! The reason is %s"%e)

    def click_bridge_bridge_scan_button(self):
        """
        桥接设置页面点击扫描
        """
        try:
            self.driver.find_element_by_css_selector(".button.scanning_wq.scanning_lang.scan_td").click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'bridge bridge setting scan button' element fail! The reason is %s"%e)

    def set_bridge_bridge_scan_operat(self, bssid):
        """
        扫描页面中，根据扫描到的ap的mac地址点击对应的操作按钮
        输入：bssid：需要连接的ap的无线mac地址
        """
        try:
            i = 2
            while i<20:
                element = self.driver.find_element_by_xpath(".//*[@id='client_scanning']/div[3]/ul[%s]/li[2]"%i)
                print(element.text, bssid.upper())
                #如果ap的mac地址和输入的mac地址一致，则点击对应的操作按钮
                if element.text.strip() == bssid.upper():
                    tmp = self.driver.find_element_by_xpath(".//*[@id='client_scanning']/div[3]/ul[%s]/li[7]/span"%i)
                    tmp.click()
                    self.driver.implicitly_wait(10)
                    time.sleep(2)
                    break
                i +=1
        except Exception as e:
            raise Exception("Web page click 'bridge bridge setting operat button' element fail! The reason is %s"%e)

    def set_bridge_bridge_encryption(self, mode):
        """
        桥接设置要桥接的无线的加密方式
        输入：mode：加密方式:none,psk2,wep+shared
        """
        try:
            element = self.driver.find_element_by_css_selector(".utext.encryption_qj_wq.encryption_choose.encryptionChoose_lang")
            Select(element).select_by_value(mode)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'bridge bridge setting 2.4G encryption' element fail! The reason is %s"%e)

    def set_bridge_bridge_password(self, pwd):
        """
        桥接设置要桥接的无线的密码
        输入：pwd：无线的密码
        """
        try:
            #wpa加密
            tmp = self.driver.find_element_by_css_selector(".utext.pwd_qj_wq.key8_64.key_choose.key_pwd")
            tmp.clear()
            tmp.send_keys(pwd)
            self.driver.implicitly_wait(10)
        except:
            #wep加密
            tmp = self.driver.find_element_by_css_selector(".key1_pwd.utext.pwd1_qj_wq.key_choose")
            tmp.clear()
            tmp.send_keys(pwd)
            self.driver.implicitly_wait(10)

    def set_bridge_bridge_BSSID(self, bssid):
        """
        桥接设置要桥接的对端无线mac地址
        输入：bssid
        """
        try:
            element = self.driver.find_element_by_css_selector(".txt_mac.mac_qj_wq")
            element.clear()
            element.send_keys(bssid)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'bridge bridge BSSID' element fail! The reason is %s"%e)



    def set_bridge_24g_ssid(self, ssid):
        """
        桥接设置输入2.4G的ssid
        输入：ssid
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".utext.ssid_24G_wq")
            tmp.clear()
            tmp.send_keys(ssid)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'bridge 2.4G setting ssid' element fail! The reason is %s"%e)

    def set_bridge_24g_encryption(self, mode):
        """
        输入2.4G无线的加密方式
        输入：mode：加密方式:none,psk2,wep+shared
        """
        try:
            element = self.driver.find_element_by_css_selector(".utext.encryption_24G_wq.encryption_choose.encryptionChoose_lang")
            Select(element).select_by_value(mode)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'bridge 2.4G encryption' element fail! The reason is %s"%e)

    def set_bridge_24g_password(self, pwd):
        """
        输入2.4G无线的密码
        输入：pwd：无线的密码
        """
        try:
            #wpa加密
            tmp = self.driver.find_element_by_css_selector(".utext.key_24G_wq.key8_64.key_choose.key_pwd")
            tmp.clear()
            tmp.send_keys(pwd)
            self.driver.implicitly_wait(10)
        except:
            #wep加密
            tmp = self.driver.find_element_by_css_selector(".key1_pwd.utext.key1_24G_wq.key1_choose")
            tmp.clear()
            tmp.send_keys(pwd)
            self.driver.implicitly_wait(10)



    ###########################################################################################
    ####################以下是客户端模式设置页面的操作###############################################
    def set_client_LAN_staticIP(self):
        """
        点击静态IP按钮
        """
        try:
            self.driver.find_element_by_css_selector(".static_c_lan.span.span_apLn_c.choose_span.static_lang").click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'client staticIP button' element fail! The reason is %s"%e)

    def set_client_LAN_dhcp(self):
        """
        点击动态获取按钮
        """
        try:
            self.driver.find_element_by_css_selector(".dhcp_c_lan.span.span_apLn_c.choose_span.dhcp_lang").click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'client dhcp button' element fail! The reason is %s"%e)

    def set_client_LAN_staticIP_ip(self, ip):
        """
        输入静态IP的ip地址
        输入：ip：ip地址
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".text.client_lan_ip")
            tmp.clear()
            tmp.send_keys(ip)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'client LAN staticIP ip' element fail! The reason is %s"%e)

    def set_client_LAN_staticIP_netmask(self, netmask):
        """
        输入静态IP的子网掩码
        输入：netmask：子网掩码
        """
        try:
            element = self.driver.find_element_by_css_selector(".utext.client_lan_netmask")
            Select(element).select_by_value(netmask)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'client LAN staticIP netmask' element fail! The reason is %s"%e)

    def set_client_LAN_staticIP_gateway(self, gateway):
        """
        输入静态ip的gateway
        输入：gateway：gateway地址
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".text.gateway_lan_client")
            tmp.clear()
            tmp.send_keys(gateway)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'client LAN staticIP gateway' element fail! The reason is %s"%e)

    def set_client_LAN_dns(self, dns):
        """
        输入的dns--静态ip和动态获取可通用
        输入：dns：dns地址
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".dns_text.utext.dns_lan_client")
            tmp.clear()
            tmp.send_keys(dns)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'client LAN staticIP dns' element fail! The reason is %s"%e)

    def set_client_bridge_connection_mode(self, mode):
        """
        桥接设置选择桥接连接模式
        输入：mode:pointToPoint_client,roam_client
        """
        try:
            element = self.driver.find_element_by_css_selector(".utext.connectionMode_client.connectChoose_lang2")
            Select(element).select_by_value(mode)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'client bridge setting connection mode' element fail! The reason is %s"%e)


    def set_client_bridge_ssid(self, ssid):
        """
        桥接设置输入要桥接的ssid
        输入：ssid
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".utext.ssid_q_client.words_kpng")
            tmp.clear()
            tmp.send_keys(ssid)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'client bridge setting ssid' element fail! The reason is %s"%e)

    def click_client_bridge_scan_button(self):
        """
        桥接设置页面点击扫描
        """
        try:
            self.driver.find_element_by_css_selector(".button.scanning_client.scanning_lang.scan_td").click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'client bridge setting scan button' element fail! The reason is %s"%e)

    def set_client_bridge_scan_operat(self, bssid):
        """
        扫描页面中，根据扫描到的ap的mac地址点击对应的操作按钮
        输入：bssid：需要连接的ap的无线mac地址
        """
        try:
            i = 2
            while i<20:
                element = self.driver.find_element_by_xpath(".//*[@id='client_scanning']/div[3]/ul[%s]/li[2]"%i)
                print(element.text, bssid.upper())
                #如果ap的mac地址和输入的mac地址一致，则点击对应的操作按钮
                if element.text.strip() == bssid.upper():
                    tmp = self.driver.find_element_by_xpath(".//*[@id='client_scanning']/div[3]/ul[%s]/li[7]/span"%i)
                    tmp.click()
                    self.driver.implicitly_wait(10)
                    break
                i +=1
        except Exception as e:
            raise Exception("Web page click 'client bridge setting operat button' element fail! The reason is %s"%e)

    def set_client_bridge_encryption(self, mode):
        """
        桥接设置要桥接的无线的加密方式
        输入：mode：加密方式:none,psk2,wep+shared
        """
        try:
            element = self.driver.find_element_by_css_selector(".encryption_qj_client.utext.encryption_choose.encryptionChoose_lang")
            Select(element).select_by_value(mode)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'client bridge setting 2.4G encryption' element fail! The reason is %s"%e)

    def set_client_bridge_password(self, pwd):
        """
        接设置要桥接的无线的密码
        输入：pwd：无线的密码
        """
        try:
            #wpa加密
            tmp = self.driver.find_element_by_css_selector(".utext.pwd_qj_client.key8_64.key_choose.key_pwd")
            tmp.clear()
            tmp.send_keys(pwd)
            self.driver.implicitly_wait(10)
        except:
            #wep加密
            tmp = self.driver.find_element_by_css_selector(".key1_pwd.utext.pwd1_qj_client.key_choose")
            tmp.clear()
            tmp.send_keys(pwd)
            self.driver.implicitly_wait(10)

    def set_client_bridge_BSSID(self, bssid):
        """
        桥接设置要桥接的对端无线mac地址
        输入：bssid
        """
        try:
            element = self.driver.find_element_by_css_selector(".txt_mac.mac_qj_client")
            element.clear()
            element.send_keys(bssid)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'client bridge BSSID' element fail! The reason is %s"%e)










    ###########################################################################################
    ####################以下是通用的页面操作#######################################################
    def click_prev_button(self):
        """
        点击上一步的按钮
        """
        try:
            #定位一组元素
            tmps = self.driver.find_elements_by_xpath(".//input[@type='button' and (@value='上一步' or @value='Prev')]")
            for tmp in tmps:
                #如果有元素在页面上是显示状态，则点击
                if tmp.is_displayed():
                    tmp.click()
                    self.driver.implicitly_wait(10)
                    break
        except Exception as e:
            raise Exception("Web page click 'prev button' element fail! The reason is %s"%e)

    def click_next_button(self):
        """
        点击下一步的按钮
        """
        try:
            #time.sleep(2)
            #定位一组元素
            tmps = self.driver.find_elements_by_xpath(".//input[@type='button' and (@value='下一步' or @value='Next')]")
            for tmp in tmps:
                #如果有元素在页面上是显示状态，则点击
                if tmp.is_displayed():
                    tmp.click()
                    self.driver.implicitly_wait(10)
                    time.sleep(2)
                    break
        except Exception as e:
            raise Exception("Web page click 'next button' element fail! The reason is %s"%e)

    def click_finish_button(self):
        """
        点击下完成的按钮
        """
        try:
            #定位一组元素
            tmps = self.driver.find_elements_by_xpath(".//input[@type='button' and (@value='完成' or @value='Finish')]")
            for tmp in tmps:
                #如果有元素在页面上是显示状态，则点击
                if tmp.is_displayed():
                    tmp.click()
                    self.driver.implicitly_wait(10)
                    break
        except Exception as e:
            raise Exception("Web page click 'finish button' element fail! The reason is %s"%e)