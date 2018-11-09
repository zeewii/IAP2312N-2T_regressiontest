#coding=utf-8
#作者：曾祥卫
#时间：2018.09.20
#描述：无线设置的控制层


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import Select
from publicControl.public_control import PublicControl
import time
from data import data


class WirelessSettingsControl(PublicControl):

    def __init__(self,driver):
        #继承PublicControl类的属性和方法
        PublicControl.__init__(self,driver)


    def menu_wirelesssettings(self):
        """
        点击无线设置设置菜单
        """
        try:
            self.driver.find_element_by_css_selector(".left_list_main.wireless.child_left_list.b.wireless_lang").click()
            self.driver.implicitly_wait(10)
            time.sleep(2)
        except Exception as e:
            raise Exception("Web page click 'wireless settings menu' element fail! The reason is %s"%e)

    def set_24g_settings(self):
        """
        点击2.4G配置
        """
        try:
            self.driver.find_element_by_css_selector(".wireless_24g.span.g24_lang").click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click '2.4G settings button' element fail! The reason is %s"%e)

    def set_Advanced(self):
        """
        点击高级配置
        """
        try:
            self.driver.find_element_by_css_selector(".wireless_senior.span.superSet_lang").click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'Advanced button' element fail! The reason is %s"%e)



    ###########################################################################################
    ####################以下是2.4G配置页面的操作###################################################
    def set_wireless_switch(self):
        """
        点击无线开关
        """
        try:
            self.driver.find_element_by_xpath(".//*[@id='btn_onOff']/div[1]/img").click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'wireless switch' element fail! The reason is %s"%e)

    def set_hidden_ssid(self):
        """
        点击隐藏无线SSID
        """
        try:
            self.driver.find_element_by_xpath(".//*[@id='btn_onOff']/div[2]/img").click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'hidden ssid' element fail! The reason is %s"%e)

    def set_ssid(self, ssid):
        """
        输入ssid名称
        输入：ssid
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".text_2.ssid_wireless.utext.ssid_24g0.words_kpng")
            tmp.clear()
            tmp.send_keys(ssid)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'ssid' element fail! The reason is %s"%e)

    def get_ssid(self):
        """
        获取ssid
        输出：ssid
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".text_2.ssid_wireless.utext.ssid_24g0.words_kpng")
            result = tmp.get_attribute('value')
            print(result)
            return result
        except Exception as e:
            raise Exception("Web page get 'ssid' element fail! The reason is %s"%e)

    def check_ssid_InputBox_red(self):
        """
        判断ssid输入框是否有红色警告
        输出：True:有警告;False：无警告
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".text_2.ssid_wireless.utext.ssid_24g0.words_kpng")
            result = tmp.get_attribute('style')
            print(result)
            if "red" in result:
                return True
            else:
                return False
        except Exception as e:
            raise Exception("Web page 'check ssid InputBox red' element fail! The reason is %s"%e)


    def set_encryption(self, mode):
        """
        输入无线的加密方式
        输入：mode：加密方式:none,psk2,wep+shared
        """
        try:
            element = self.driver.find_element_by_css_selector(".text_2.encryption_wireless.encryption_24g.encryption_choose")
            Select(element).select_by_value(mode)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'encryption' element fail! The reason is %s"%e)

    def set_route_24g_password(self, pwd):
        """
        输入2.4G无线的密码
        输入：pwd：无线的密码
        """
        try:
            #wpa加密
            tmp = self.driver.find_element_by_css_selector(".text_2.pwd_wireless.text_empty.pwd_24g0.key8_64.key_choose")
            tmp.clear()
            tmp.send_keys(pwd)
            self.driver.implicitly_wait(10)
        except:
            #wep加密
            tmp = self.driver.find_element_by_css_selector(".key1_pwd.text_2.pwd1_wireless.text_empty.pwd1_24g0.key1_choose")
            tmp.clear()
            tmp.send_keys(pwd)
            self.driver.implicitly_wait(10)

    def check_wpa_password_InputBox_red(self):
        """
        判断wpa密码输入框是否有红色警告
        输出：True:有警告;False：无警告
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".text_2.pwd_wireless.text_empty.pwd_24g0.key8_64.key_choose")
            result = tmp.get_attribute('style')
            print(result)
            if "red" in result:
                return True
            else:
                return False
        except Exception as e:
            raise Exception("Web page 'check wpa password InputBox red' element fail! The reason is %s"%e)

    def click_plus_button(self):
        """
        点击+号
        """
        try:
            self.driver.find_element_by_css_selector(".radio.radio_24g").click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'plus button' element fail! The reason is %s"%e)

    def click_minus_button(self, n):
        """
        点击某个-号
        输入:n:第几个-号
        """
        try:
            self.driver.find_elements_by_css_selector(".del.del_24g")[n].click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'the n minus button' element fail! The reason is %s"%e)

    def click_all_minus_button(self):
        """
        依次点击所有的-号
        """
        try:
            tmps = self.driver.find_elements_by_css_selector(".del.del_24g")
            for tmp in tmps:
                tmp.click()
                self.driver.implicitly_wait(10)
                time.sleep(2)
        except Exception as e:
            raise Exception("Web page click 'all minus button' element fail! The reason is %s"%e)


    def set_n_ssid(self, n, ssid):
        """
        输入第n个ssid名称
        输入：ssid,n:第几个
        """
        try:
            tmps = self.driver.find_elements_by_css_selector(".text_2.words_kpng.ssid_wireless.words_kpng")
            tmps[n].clear()
            tmps[n].send_keys(ssid)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'the n ssid' element fail! The reason is %s"%e)

    def set_n_encryption(self, n, mode):
        """
        输入第n个ssid的加密方式
        输入：mode：加密方式:none,psk2,wep+shared;n:第几个
        """
        try:
            element = self.driver.find_element_by_xpath(".//*[@id='right_main']/div[9]/div[1]/div[2]/table/tbody/tr[%s]/td[2]/select"%(n+2))
            Select(element).select_by_value(mode)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'the n ssid's encryption' element fail! The reason is %s"%e)

    def set_n_wpa_password(self, n, password):
        """
        输入第n个ssid的wpa加密密码
        输入：ssid,n:第几个
        """
        try:
            tmps = self.driver.find_elements_by_css_selector(".key8_64.text_2.pwd_wireless.text_empty.pwd_24g0.key_choose")
            tmps[n].clear()
            tmps[n].send_keys(password)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'the n ssid's wpa password' element fail! The reason is %s"%e)

    def set_n_wep_password(self, n, password):
        """
        输入第n个ssid的wep加密密码
        输入：ssid,n:第几个
        """
        try:
            tmps = self.driver.find_elements_by_css_selector(".key1_pwd.text_2.pwd1_wireless.text_empty.pwd1_24g0.key1_choose")
            tmps[n].clear()
            tmps[n].send_keys(password)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'the n ssid's wep password' element fail! The reason is %s"%e)

    def set_More_settings(self):
        """
        点击更多设置
        """
        try:
            self.driver.find_elements_by_css_selector(".more_point.moreSet_lang")[0].click()
            self.driver.implicitly_wait(10)
            time.sleep(2)
        except Exception as e:
            raise Exception("Web page click 'more settings button' element fail! The reason is %s"%e)

    def set_channel(self, channel):
        """
        输入2.4G无线的信道
        输入：channel：中国：1-13;美国：1-11;auto
        """
        try:
            element = self.driver.find_element_by_css_selector(".text_2.channel_wireless")
            Select(element).select_by_value(str(channel))
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set '2.4G channel' element fail! The reason is %s"%e)

    def set_bandwidth(self, width):
        """
        输入2.4G无线的无线频宽
        输入：width：无线频宽,HT20,HT40
        """
        try:
            element = self.driver.find_element_by_css_selector(".text_2.htmode_wireless")
            Select(element).select_by_value(width)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set '2.4G bandwidth' element fail! The reason is %s"%e)

    def get_bandwidth(self):
        """
        获取2.4G无线的无线频宽
        """
        try:
            element = self.driver.find_element_by_css_selector(".text_2.htmode_wireless")
            result = element.text
            print(result)
            return result
        except Exception as e:
            raise Exception("Web page get '2.4G bandwidth' element fail! The reason is %s"%e)

    def set_power(self, power):
        """
        输入发射功率
        输入：power：功率值
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".text_2.txpower_wireless")
            tmp.clear()
            tmp.send_keys(str(power))
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'power' element fail! The reason is %s"%e)

    def set_max_client_number(self, n):
        """
        输入最大用户数
        输入：n:最大用户数--str和int类型皆可
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".text_2.max_userCount_24g.text_empty")
            tmp.clear()
            tmp.send_keys(str(n))
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'max client number' element fail! The reason is %s"%e)


    ###########################################################################################
    ####################以下是高级配置页面的操作###################################################
    def set_shortGI(self):
        """
        点击短防护时间间隔
        """
        try:
            self.driver.find_element_by_xpath(".//*[@id='btn_onoff_second']/div[1]/img").click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'short GI button' element fail! The reason is %s"%e)

    def set_WDS(self):
        """
        点击WDS
        """
        try:
            self.driver.find_element_by_css_selector(".switch_wds.img_choose").click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'WDS button' element fail! The reason is %s"%e)

    def set_WMM(self):
        """
        点击无线多媒体
        """
        try:
            self.driver.find_element_by_xpath(".//*[@id='btn_onoff_third']/div[1]/img").click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'WMM button' element fail! The reason is %s"%e)

    def set_wireless_isolate(self):
        """
        点击无线隔离
        """
        try:
            self.driver.find_element_by_css_selector(".switch_ge.img_choose").click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page click 'wireless isolate button' element fail! The reason is %s"%e)

    def set_fragment_threshold(self, value):
        """
        输入分割阈值
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".utext.threshold_senior")
            tmp.clear()
            tmp.send_keys(str(value))
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'fragment threshold' element fail! The reason is %s"%e)

    def set_RTS_threshold(self, value):
        """
        输入RTS阈值
        """
        try:
            tmp = self.driver.find_element_by_css_selector(".utext.rts_senior")
            tmp.clear()
            tmp.send_keys(str(value))
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'RTS threshold' element fail! The reason is %s"%e)

    def set_country(self, country):
        """
        设置国家
        输入：country:CN,US
        """
        try:
            element = self.driver.find_element_by_css_selector(".utext.country_wireless_5g.countryChoose_lang")
            Select(element).select_by_value(country)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Web page set 'country' element fail! The reason is %s"%e)




