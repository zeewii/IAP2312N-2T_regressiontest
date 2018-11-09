#coding:utf-8
#描述：公用控制层代码，包括页面共有元素的获取和设置，为基础类
#作者：曾祥卫
#时间：2018.09.17

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import uuid,random,sys,os
import subprocess,time,pexpect,codecs
import locale
from connect.ssh import SSH
from data import data
dirname = os.path.dirname(os.path.dirname(__file__))
PATH_data = os.path.join(dirname, "data")
png_PATH = os.path.join(dirname, "data", "testresultdata")

data_basic = data.data_basic()
data_login = data.data_login()


class PublicControl:
    def __init__(self,driver):
        self.driver = driver

    ###################################################
    #以下是所以页面的公用方法
    ###################################################
    def click_save_button(self):
        """
        点击设置按钮--保存
        """
        try:
            #定位一组元素
            tmps = self.driver.find_elements_by_xpath(".//input[@type='button' and (@value='设置' or @value='Save')]")
            for tmp in tmps:
                #如果有元素在页面上是显示状态，则点击
                if tmp.is_displayed():
                    tmp.click()
                    self.driver.implicitly_wait(10)
                    break
        except Exception as e:
            self.get_picture("click_save_button")
            raise Exception("Web page click 'save button' element fail! The reason is %s"%e)

    def click_reset_button(self):
        """
        点击重置按钮--取消
        """
        try:
            #定位一组元素
            tmps = self.driver.find_elements_by_xpath(".//input[@type='reset' and (@value='重置' or @value='Reset')]")
            for tmp in tmps:
                #如果有元素在页面上是显示状态，则点击
                if tmp.is_displayed():
                    tmp.click()
                    self.driver.implicitly_wait(10)
                    break
        except Exception as e:
            self.get_picture("click_reset_button")
            raise Exception("Web page click 'reset button' element fail! The reason is %s"%e)

    def click_confirm_button(self):
        """
        点击确认按钮
        """
        try:
            time.sleep(2)
            #定位一组元素
            tmps = self.driver.find_elements_by_xpath(".//input[@type='button' and (@value='确认' or @value='YES')]")
            for tmp in tmps:
                #如果有元素在页面上是显示状态，则点击
                if tmp.is_displayed():
                    tmp.click()
                    self.driver.implicitly_wait(10)
                    time.sleep(30)
                    self.driver.refresh()
                    time.sleep(3)
                    break
        except Exception as e:
            self.get_picture("click_confirm_button")
            raise Exception("Web page click 'confirm button' element fail! The reason is %s"%e)

    def click_cancel_button(self):
        """
        点击取消按钮
        """
        try:
            time.sleep(3)
            #定位一组元素
            tmps = self.driver.find_elements_by_xpath(".//input[@type='button' and (@value='取消' or @value='NO')]")
            for tmp in tmps:
                #如果有元素在页面上是显示状态，则点击
                if tmp.is_displayed():
                    tmp.click()
                    self.driver.implicitly_wait(10)
                    break
        except Exception as e:
            self.get_picture("click_cancel_button")
            raise Exception("Web page click 'cancel button' element fail! The reason is %s"%e)

    def click_confirm_button_no_wait(self):
        """
        点击确认按钮,不等待30s
        """
        try:
            time.sleep(2)
            #定位一组元素
            tmps = self.driver.find_elements_by_xpath(".//input[@type='button' and (@value='确认' or @value='YES')]")
            for tmp in tmps:
                #如果有元素在页面上是显示状态，则点击
                if tmp.is_displayed():
                    tmp.click()
                    #self.driver.implicitly_wait(10)
                    break
        except Exception as e:
            self.get_picture("click_confirm_button_no_wait")
            raise Exception("Web page click 'confirm button' element fail! The reason is %s"%e)

    def check_waitbar_displayed(self):
        """判断点击保持后的等待页面是否显示"""
        try:

            tmp = self.driver.find_element_by_css_selector(".p_wait_setComp.wait_lang")
            #如果有元素在页面上是显示状态，则返回True
            if tmp.is_displayed():
                return True
            else:
                return False
        except:
            self.get_picture("check_waitbar_displayed")
            return False

    ###################################################
    #以下是PC端操作
    ###################################################


    def get_client_cmd_result(self,cmd):
        """
        描述：Client端在终端输入命令,命令结果返回给函数
        输入：self,cmd-client在终端输入的命令
        输出：output-在终端显示的结果
        """
        try:
            #Client端在终端输入命令,命令结果返回给函数
            result = subprocess.check_output(cmd, shell=True).decode('utf-8')
            print("Input cmd %s in PC successfully!"%cmd)
            print(result)
            return result
        #捕捉异常并打印异常信息
        except Exception as e:
            raise Exception("input command in PC fail! The reason is %s"%e)

    #描述:获取本地mac地址
    #输入:无
    #输出:mac-字符串类型，本地mac
    def get_localmac(self):
        try:
            tmp = uuid.UUID(int=uuid.getnode()).hex[-12:]
            mac = ":".join([tmp[e:e+2] for e in range(0,11,2)])
            return mac
        except Exception as e:
            raise Exception("get local mac address fail! The reason is %s"%e)

    #描述：获取本地无线mac地址
    #输入：wlan：本机无线接口名
    #输出：本机的无线mac地址
    def get_wlan_mac(self,wlan):
        try:
            tmp1 = PublicControl.get_client_cmd_result(self,'ifconfig %s'%wlan)
            tmp2 = tmp1.split('\n')
            tmp3 = tmp2[0]
            #tmp4 = tmp3.strip(" ")
            result =tmp3[-19:-2]
            print(result)
            return result
        except Exception as e:
            raise Exception("get wlan mac fail! The reason is %s"%e)

    #描述:mac地址去冒号
    #输入:无
    #输出:mac-字符串类型
    def mac_drop(self,mac):
        try:
            tmp = mac.split(":")
            tmp1 = ''.join(tmp)
            print(tmp1)
            return tmp1
        except Exception as e:
            raise Exception("mac drop : fail! The reason is %s"%e)

    #描述：获取本地IP
    #输入：eth：本机网卡接口名
    #输出：本机的IP地址
    def get_localIp(self,eth):
        try:
            language = locale.getdefaultlocale()#获取系统语言
            result1 = PublicControl.get_client_cmd_result(self,'ifconfig %s'%eth)
            result2 = result1.split('inet')
            result = result2[1].split(" ")
            if 'en_US' in language:
                ip =  result[1].strip('addr:')
            else:
                ip =  result[1].strip(u'地址:')
            print(ip)
            return ip
        except Exception as e:
            raise Exception("get local ip fail! The reason is %s"%e)

    #描述:ping IP地址
    #输入:str-ip地址或域名
    #输出:ping结果0或非0
    def get_ping(self,str):
        try:
            ping = "ping %s -c 3"%str
            result = subprocess.call(ping,shell=True)
            print("the result of ping %s is %s"%(str,result))
            return result
        except Exception as e:
            raise Exception("ping ip address fail! The reason is %s"%e)

    #描述:用以在后台判断某个进程在不在
    #输入:某个进程
    #输出:True-存在，反之
    def ssh_ps(self,host,user,pwd,process):
        try:
            i =0
            while(i<5):
                ssh = SSH(host,pwd)
                result = ssh.ssh_cmd(user,"ps")
                if process in result:
                    return True
                time.sleep(20)
                i+=1
            return False
        except Exception as e:
            raise Exception("judge the process in AP fail! The reason is %s"%e)


    #描述：禁用网卡,然后再启用网卡
    #输入：self
    #输出：None
    def networkcard_disable_enable(self):
        try:
            d = data.data_basic()
            #禁用eth0网卡
            down = pexpect.spawn('sudo ifconfig %s down'%d['lan_pc'],timeout=5)
            down.expect([':',pexpect.TIMEOUT,pexpect.EOF])
            down.sendline(d["PC_pwd"])
            time.sleep(15)

            #启用eth0网卡
            up = pexpect.spawn('sudo ifconfig %s up'%d['lan_pc'],timeout=5)
            up.expect([':',pexpect.TIMEOUT,pexpect.EOF])
            up.sendline(d["PC_pwd"])
            time.sleep(15)
        #捕捉异常并打印异常信息
        except Exception as e:
            raise Exception("disable/enable eth of PC fail! The reason is %s"%e)


    #描述：通过ssh登录路由后台,输入reboot重启路由,并等待60s
    #输入：self
    #输出：None
    def reboot_router(self,host,user,pwd):
        try:
            #在路由器中输入reboot
            ssh = SSH(host,pwd)
            ssh.ssh_cmd(user,"reboot")
            #time.sleep(180)
        #捕捉异常并打印异常信息
        except Exception as e:
            raise Exception("input reboot after login AP fail! The reason is %s"%e)

    #描述：通过ssh登录路由后台，取出路由当前的版本号
    #输入：self
    #输出：路由当前的版本号
    def get_router_version(self,host,user,pwd):
        try:
            #在路由器中输入cat /tmp/gs_version
            ssh = SSH(host,pwd)
            result = ssh.ssh_cmd(user,"cat /tmp/gs_version")
            return result
        #捕捉异常并打印异常信息
        except Exception as e:
            raise Exception("get_router_version fail! The reason is %s"%e)


    #描述：通过ssh登录路由后台，取出路由的mac地址
    #输入：self
    #输出：路由的mac地址
    def get_router_mac(self, host, user, pwd):
        try:
            #在路由器后台
            ssh = SSH(host,pwd)
            result1 = ssh.ssh_cmd(user,"ifconfig eth1 | grep HWaddr")
            result = result1[-21:-4]
            return result
        #捕捉异常并打印异常信息
        except Exception as e:
            raise Exception("get_router_mac fail! The reason is %s"%e)

    def get_ap_ip(self, host, user, pwd, MAC):
        """
        登录上级路由器，获取ap的ip地址
        输入：host,usr,pwd上级路由器的ip，ssh用户名，ssh密码;MAC下级ap的br-lan的mac地址
        """
        try:
            ssh = SSH(host,pwd)
            tmp = ssh.ssh_cmd(user,"cat /tmp/dhcp.leases")
            mac = MAC.lower()
            a = tmp.split("\n")
            for i in a:
                if mac in i:
                    ip = i.split(mac)
                    result = ip[1].split("*")
                    result_ip =result[0].strip()
                    print(result_ip)
                    return result_ip
        #捕捉异常并打印异常信息
        except Exception as e:
            raise Exception("get_ap_ip fail! The reason is %s"%e)

    #取随机mac
    def randomMAC(self):
        try:
            mac = [ 0x00, 0x0c,
            random.randint(0x00, 0x7f),
            random.randint(0x00, 0x7f),
            random.randint(0x00, 0xff),
            random.randint(0x00, 0xff) ]
            return ':'.join(map(lambda x: "%02x" % x, mac))
        #捕捉异常并打印异常信息
        except Exception as e:
            raise Exception("get random MAC fail! The reason is %s"%e)

    #取随机ip地址
    def randomip(self):
        try:
            a = random.randint(1,254)
            b = random.randint(1,254)
            c = random.randint(1,254)
            d = random.randint(1,254)
            ip = '%s.%s.%s.%s'%(a,b,c,d)
            return ip
        #捕捉异常并打印异常信息
        except Exception as e:
            raise Exception("get random IP address fail! The reason is %s"%e)



    ###################################################
    #以下是无线网卡的控制方法
    ###################################################

    #描述：禁用无线网卡
    #输入：pinself
    #输出：None
    def wlan_disable(self,wlan):
        try:
            d = data.data_basic()
            #禁用无线网卡
            down = pexpect.spawn('sudo ifconfig %s down'%wlan,timeout=5)
            down.expect([':',pexpect.TIMEOUT,pexpect.EOF])
            down.sendline(d["PC_pwd"])
            time.sleep(30)
            print("Disable %s successfully!"%wlan)
        #捕捉异常并打印异常信息
        except Exception as e:
            raise Exception("disable wlan of PC fail! The reason is %s"%e)

    #描述：启用网卡
    def wlan_enable(self,wlan):
        try:
            d = data.data_basic()
            #启用无线网卡
            up = pexpect.spawn('sudo ifconfig %s up'%wlan,timeout=5)
            up.expect([':',pexpect.TIMEOUT,pexpect.EOF])
            up.sendline(d["PC_pwd"])
            time.sleep(30)
            print("Enable %s successfully!"%wlan)
        #捕捉异常并打印异常信息
        except Exception as e:
            raise Exception("enable wlan of PC fail! The reason is %s"%e)

    #描述：扫描无线信号,返回扫描的结果-----备用,不准
    def ssid_scan_backup(self,ssid,wlan):
        try:
            #输入命令进行无线ssid扫描
            result = subprocess.check_output('iwlist %s scanning | grep %s'%(wlan,ssid),shell=True).decode('utf-8')
            f = open('./data/testresultdata/ssidScanResult.txt','a')
            f.write(result)
            f.close()
            print(result)
            return result
        #捕捉异常并打印异常信息
        except:
            return False

    #描述：扫描无线信号,返回扫描的结果
    def ssid_scan(self,ssid,wlan):
        try:
            #获取测试主机密码
            d = data.data_basic()
            #通过wpa_cli命令来断开已连接的无线网络
            PublicControl.disconnect_ap(self)
            time.sleep(20)
            while True:
                #输入命令进行无线ssid扫描
                result = subprocess.check_output('echo %s |sudo -S iw dev %s scan | grep %s'%(d['PC_pwd'],wlan,ssid),shell=True).decode('utf-8')
                time.sleep(30)
                if "command failed" in result:
                    print("command failed,scan AP again!")
                    PublicControl.get_client_cmd_result(self,"echo %s |sudo -S /etc/init.d/network-manager restart"%d["PC_pwd"])
                    time.sleep(60)
                    continue
                f = open('./data/testresultdata/ssidScanResult.txt','a')
                f.write(result)
                f.close()
                print("scan AP has finished!")
                print(result)
                return result
        #捕捉异常并打印异常信息
        except :
            print("scan AP no result")
            return "scan AP no result!"

    #描述：连接AP后，验证AP的加密类型
    def check_AP_encryption(self):
        try:
            #获取测试主机密码
            d = data.data_basic()
            #输入命令进行无线ssid扫描
            result = PublicControl.get_client_cmd_result(self,\
                'echo %s |sudo -S iwlist %s wpakeys'%(d['PC_pwd'],d['wlan_pc']))
            #print result
            return result
        #捕捉异常并打印异常信息
        except:
            return False


    #描述：扫描无线信号,判断是否能够扫描到AP的SSID
    #输入：指定的无线ssid,无线网卡接口名wlan
    #输出：扫描的结果 如下：
    def ssid_scan_result(self,ssid,wlan):
        result = PublicControl.ssid_scan(self,ssid,wlan)
        #获取无线SSID
        ssid1 = result.strip('	SSID: ')
        print(ssid1)
        if ssid in ssid1:
            print("scan AP successfully!")
            return True
        else:
            print("scan AP failed!")
            return False

    #描述：扫描无线信号,判断是否能够扫描到AP的SSID--备份
    #输入：指定的无线ssid,无线网卡接口名wlan
    #输出：扫描的结果 如下：
    def ssid_scan_result_backup(self,ssid,wlan):
        for i in range(3):
            result = PublicControl.ssid_scan(self,ssid,wlan)
            #获取无线SSID
            ssid1 = result.strip('	SSID: ')
            if ssid in ssid1:
                print("scan AP successfully!")
                return True
            time.sleep(60)
        print("scan AP failed!")
        return False

    #描述：通过wpa_cli命令来连接不加密的无线网络
    #输入：ssid:需要连接的无线网络的ssid,wlan:无线网卡的接口名
    #输出：输入命令返回的结果
    def connect_NONE_AP(self,ssid,wlan):
        try:
            for i in range(3):
                #获取测试主机密码
                d = data.data_basic()
                #进入wpa_cli的配置命令
                child = pexpect.spawn('sudo wpa_cli',timeout=5)
                child.expect([':',pexpect.TIMEOUT,pexpect.EOF])
                child.sendline(d['PC_pwd'])
                time.sleep(5)

                #删除无线网络id为0的配置
                child.expect('>')
                child.sendline('remove_network 0')
                'remove_network 0'
                #增加无线网络id为0的配置
                child.expect('>')
                child.sendline('add_network')
                print('add_network')
                #设置无线网络id为0的无线ssid
                child.expect('>')
                ESSID = 'set_network 0 ssid \"%s\"'%str(ssid)
                print(ESSID)
                child.sendline(ESSID)
                #设置无线网络id为0的加密为非加密
                child.expect('>')
                child.sendline('set_network 0 key_mgmt NONE')
                print('set_network 0 key_mgmt NONE')
                #禁用无线网络id为0网络
                child.expect('>')
                child.sendline('disable_network 0')
                print('disable_network 0')
                #启用无线网络id为0网络
                child.expect('>')
                child.sendline('enable_network 0')
                print('enable_network 0')
                time.sleep(10)
                #退出wpa_cli
                child.expect('>')
                time.sleep(20)
                child.sendline('quit')
                print('quit')
                #退出wpa_cli交互模式
                child.close(force=True)

                #判断是否连接AP成功
                result1 = subprocess.check_output("iw dev %s link"%wlan,shell=True).decode('utf-8')
                if "Not connected" in result1:
                    print("Connect AP failed,wait 60s and try again the times:%s"%(i+1))
                    #断开已连接的无线网络
                    PublicControl.disconnect_ap(self)
                    #disable/enable 无线网卡
                    PublicControl.wlan_disable(self,wlan)
                    PublicControl.wlan_enable(self,wlan)
                    PublicControl.ssid_scan_result(self,ssid,wlan)
                    ssh = SSH(d['DUT_ip'],d['ssh_pwd'])
                    ssh.ssh_cmd(d['ssh_user'],"iwconfig")
                    subprocess.call("echo %s |sudo -S /etc/init.d/network-manager restart"%d["PC_pwd"],shell=True)
                    time.sleep(60)
                else:
                    print("Connect AP successfully!")
                    break

            #判断是否连接AP成功
            result = subprocess.check_output("iw dev %s link"%wlan,shell=True).decode('utf-8')
            print(result)
            return result
        #捕捉异常并打印异常信息
        except Exception as e:
            raise Exception("connect AP of NONE encryption fail! The reason is %s"%e)

    #描述：通过wpa_cli命令来连接不加密的无线网络--备份
    #输入：ssid:需要连接的无线网络的ssid,wlan:无线网卡的接口名
    #输出：输入命令返回的结果
    def connect_NONE_AP_backup(self,ssid,wlan):
        try:
            #获取测试主机密码
            d = data.data_basic()
            #进入wpa_cli的配置命令
            child = pexpect.spawn('sudo wpa_cli',timeout=5)
            child.expect([':',pexpect.TIMEOUT,pexpect.EOF])
            child.sendline(d['PC_pwd'])
            time.sleep(5)

            #删除无线网络id为0的配置
            child.expect('>')
            child.sendline('remove_network 0')
            print('remove_network 0')
            #增加无线网络id为0的配置
            child.expect('>')
            child.sendline('add_network')
            print('add_network')
            #设置无线网络id为0的无线ssid
            child.expect('>')
            ESSID = 'set_network 0 ssid \"%s\"'%str(ssid)
            print(ESSID)
            child.sendline(ESSID)
            #设置无线网络id为0的加密为非加密
            child.expect('>')
            child.sendline('set_network 0 key_mgmt NONE')
            print('set_network 0 key_mgmt NONE')
            #禁用无线网络id为0网络
            child.expect('>')
            child.sendline('disable_network 0')
            print('disable_network 0')
            #启用无线网络id为0网络
            child.expect('>')
            child.sendline('enable_network 0')
            print('enable_network 0')
            time.sleep(10)
            #退出wpa_cli
            child.expect('>')
            time.sleep(20)
            child.sendline('quit')
            print('quit')
            #退出wpa_cli交互模式
            child.close(force=True)
            #判断是否连接AP成功
            result = subprocess.check_output("iw dev %s link"%wlan,shell=True).decode('utf-8')
            print(result)
            return result
        #捕捉异常并打印异常信息
        except Exception as e:
            raise Exception("connect AP of NONE encryption fail! The reason is %s"%e)

    #描述：通过wpa_cli命令来连接WEP的无线网络
    #输入：ssid:需要连接的无线网络的ssid,wlan:无线网卡的接口名,password:wep的密码
    #输出：输入命令返回的结果
    def connect_WEP_AP(self,ssid,password,wlan):
        try:
            for i in range(3):
                #获取测试主机密码
                d = data.data_basic()
                #进入wpa_cli的配置命令
                child = pexpect.spawn('sudo wpa_cli',timeout=5)
                child.expect([':',pexpect.TIMEOUT,pexpect.EOF])
                child.sendline(d['PC_pwd'])
                time.sleep(5)

                #删除无线网络id为0的配置
                child.expect('>')
                child.sendline('remove_network 0')
                print ('remove_network 0')
                #增加无线网络id为0的配置
                child.expect('>')
                child.sendline('add_network')
                print ('add_network')
                #设置无线网络id为0的无线ssid
                child.expect('>')
                ESSID = 'set_network 0 ssid \"%s\"'%str(ssid)
                print (ESSID)
                child.sendline(ESSID)
                #设置无线网络id为0的加密为非加密
                child.expect('>')
                child.sendline('set_network 0 key_mgmt NONE')
                print ('set_network 0 key_mgmt NONE')
                #设置无线网络id为0的密码
                child.expect('>')
                key = 'set_network 0 wep_key0 \"%s\"'%str(password)
                print (key)
                child.sendline(key)
                child.expect('>')
                child.sendline('set_network 0 wep_tx_keyidx 0')
                print ('set_network 0 wep_tx_keyidx 0')
                #选择无线网络id为0网络
                child.expect('>')
                child.sendline('select_network 0')
                print ('select_network 0')
                time.sleep(10)
                #启用无线网络id为0网络
                child.expect('>')
                child.sendline('enable_network 0')
                print ('enable_network 0')
                #退出wpa_cli
                child.expect('>')
                time.sleep(20)
                child.sendline('quit')
                print ('quit')
                #退出wpa_cli交互模式
                child.close(force=True)

                #判断是否连接AP成功
                result1 = subprocess.check_output("iw dev %s link"%wlan,shell=True).decode('utf-8')
                if "Not connected" in result1:
                    print ("Connect AP failed,wait 60s and try again the times:%s"%(i+1))
                    #断开已连接的无线网络
                    PublicControl.disconnect_ap(self)
                    #disable/enable 无线网卡
                    PublicControl.wlan_disable(self,wlan)
                    PublicControl.wlan_enable(self,wlan)
                    PublicControl.ssid_scan_result(self,ssid,wlan)
                    ssh = SSH(d['DUT_ip'],d['ssh_pwd'])
                    ssh.ssh_cmd(d['ssh_user'],"iwconfig")
                    subprocess.call("echo %s |sudo -S /etc/init.d/network-manager restart"%d["PC_pwd"],shell=True)
                    time.sleep(60)
                else:
                    print ("Connect AP successfully!")
                    break

            #判断是否连接AP成功
            result = subprocess.check_output("iw dev %s link"%wlan,shell=True).decode('utf-8')
            print (result)
            return result
        #捕捉异常并打印异常信息
        except Exception as e:
            raise Exception("connect AP of WEP encryption fail! The reason is %s"%e)

    #描述：通过wpa_cli命令来连接WEP的无线网络--备份
    #输入：ssid:需要连接的无线网络的ssid,wlan:无线网卡的接口名,password:wep的密码
    #输出：输入命令返回的结果
    def connect_WEP_AP_backup(self,ssid,password,wlan):
        try:
            #获取测试主机密码
            d = data.data_basic()
            #进入wpa_cli的配置命令
            child = pexpect.spawn('sudo wpa_cli',timeout=5)
            child.expect([':',pexpect.TIMEOUT,pexpect.EOF])
            child.sendline(d['PC_pwd'])
            time.sleep(5)

            #删除无线网络id为0的配置
            child.expect('>')
            child.sendline('remove_network 0')
            print ('remove_network 0')
            #增加无线网络id为0的配置
            child.expect('>')
            child.sendline('add_network')
            print ('add_network')
            #设置无线网络id为0的无线ssid
            child.expect('>')
            ESSID = 'set_network 0 ssid \"%s\"'%str(ssid)
            print (ESSID)
            child.sendline(ESSID)
            #设置无线网络id为0的加密为非加密
            child.expect('>')
            child.sendline('set_network 0 key_mgmt NONE')
            print ('set_network 0 key_mgmt NONE')
            #设置无线网络id为0的密码
            child.expect('>')
            key = 'set_network 0 wep_key0 \"%s\"'%str(password)
            print (key)
            child.sendline(key)
            child.expect('>')
            child.sendline('set_network 0 wep_tx_keyidx 0')
            print ('set_network 0 wep_tx_keyidx 0')
            #选择无线网络id为0网络
            child.expect('>')
            child.sendline('select_network 0')
            print ('select_network 0')
            time.sleep(10)
            #启用无线网络id为0网络
            child.expect('>')
            child.sendline('enable_network 0')
            print ('enable_network 0')
            #退出wpa_cli
            child.expect('>')
            time.sleep(20)
            child.sendline('quit')
            print ('quit')
            #退出wpa_cli交互模式
            child.close(force=True)

            #判断是否连接AP成功
            result = subprocess.check_output("iw dev %s link"%wlan,shell=True).decode('utf-8')
            print (result)
            return result
        #捕捉异常并打印异常信息
        except Exception as e:
            raise Exception("connect AP of WEP encryption fail! The reason is %s"%e)

    #描述：通过wpa_cli命令来连接WEP-10位或26位的无线网络
    #输入：ssid:需要连接的无线网络的ssid,wlan:无线网卡的接口名,password:wep的密码
    #输出：输入命令返回的结果
    def connect_WEP10_26_AP(self,ssid,password,wlan):
        try:
            for i in range(3):
                #获取测试主机密码
                d = data.data_basic()
                #进入wpa_cli的配置命令
                child = pexpect.spawn('sudo wpa_cli',timeout=5)
                child.expect([':',pexpect.TIMEOUT,pexpect.EOF])
                child.sendline(d['PC_pwd'])
                time.sleep(5)

                #删除无线网络id为0的配置
                child.expect('>')
                child.sendline('remove_network 0')
                print ('remove_network 0')
                #增加无线网络id为0的配置
                child.expect('>')
                child.sendline('add_network')
                print ('add_network')
                #设置无线网络id为0的无线ssid
                child.expect('>')
                ESSID = 'set_network 0 ssid \"%s\"'%str(ssid)
                print (ESSID)
                child.sendline(ESSID)
                #设置无线网络id为0的加密为非加密
                child.expect('>')
                child.sendline('set_network 0 key_mgmt NONE')
                print ('set_network 0 key_mgmt NONE')
                #设置无线网络id为0的密码
                child.expect('>')
                key = 'set_network 0 wep_key0 %s'%str(password)
                print (key)
                child.sendline(key)
                child.expect('>')
                child.sendline('set_network 0 wep_tx_keyidx 0')
                print ('set_network 0 wep_tx_keyidx 0')
                #选择无线网络id为0网络
                child.expect('>')
                child.sendline('select_network 0')
                print ('select_network 0')
                time.sleep(10)
                #启用无线网络id为0网络
                child.expect('>')
                child.sendline('enable_network 0')
                print ('enable_network 0')
                #退出wpa_cli
                child.expect('>')
                time.sleep(20)
                child.sendline('quit')
                print ('quit')
                #退出wpa_cli交互模式
                child.close(force=True)

                #判断是否连接AP成功
                result1 = subprocess.check_output("iw dev %s link"%wlan,shell=True).decode('utf-8')
                if "Not connected" in result1:
                    print ("Connect AP failed,wait 60s and try again the times:%s"%(i+1))
                    #断开已连接的无线网络
                    PublicControl.disconnect_ap(self)
                    #disable/enable 无线网卡
                    PublicControl.wlan_disable(self,wlan)
                    PublicControl.wlan_enable(self,wlan)
                    PublicControl.ssid_scan_result(self,ssid,wlan)
                    ssh = SSH(d['DUT_ip'],d['ssh_pwd'])
                    ssh.ssh_cmd(d['ssh_user'],"iwconfig")
                    subprocess.call("echo %s |sudo -S /etc/init.d/network-manager restart"%d["PC_pwd"],shell=True)
                    time.sleep(60)
                else:
                    print ("Connect AP successfully!")
                    break

            #判断是否连接AP成功
            result = subprocess.check_output("iw dev %s link"%wlan,shell=True).decode('utf-8')
            print (result)
            return result
        #捕捉异常并打印异常信息
        except Exception as e:
            raise Exception("connect AP of WEP encryption fail! The reason is %s"%e)


    #描述：通过wpa_cli命令来连接WPA的无线网络--备份
    #输入：ssid:需要连接的无线网络的ssid,wlan:无线网卡的接口名,password:wpa的密码
    #输出：输入命令返回的结果
    def connect_WPA_AP_backup(self,ssid,password,wlan):
        try:
            #获取测试主机密码
            d = data.data_basic()
            #进入wpa_cli的配置命令
            child = pexpect.spawn('sudo wpa_cli',timeout=5)
            child.expect([':',pexpect.TIMEOUT,pexpect.EOF])
            child.sendline(d['PC_pwd'])
            time.sleep(5)

            #删除无线网络id为0的配置
            child.expect('>')
            child.sendline('remove_network 0')
            print ('remove_network 0')
            #增加无线网络id为0 的配置
            child.expect('>')
            child.sendline('add_network')
            print ('add_network')
            #设置无线网络id为0的无线ssid
            child.expect('>')
            ESSID = 'set_network 0 ssid \"%s\"'%str(ssid)
            print (ESSID)
            child.sendline(ESSID)
            #设置无线网络id为0的密码
            child.expect('>')
            key = 'set_network 0 psk \"%s\"'%str(password)
            print (key)
            child.sendline(key)

            #选择无线网络id为0网络
            child.expect('>')
            child.sendline('select_network 0')
            print ('select_network 0')
            time.sleep(10)
            #启用无线网络id为0网络
            child.expect('>')
            child.sendline('enable_network 0')
            print ('enable_network 0')
            #退出wpa_cli
            child.expect('>')
            time.sleep(20)
            child.sendline('quit')
            print ('quit')
            #退出wpa_cli交互模式
            child.close(force=True)

            #判断是否连接AP成功
            result = subprocess.check_output("iw dev %s link"%wlan,shell=True).decode('utf-8')
            print (result)
            return result
        #捕捉异常并打印异常信息
        except Exception as e:
            raise Exception("connect AP of WPA encryption fail! The reason is %s"%e)

    #描述：通过wpa_cli命令来连接WPA的无线网络
    #输入：ssid:需要连接的无线网络的ssid,wlan:无线网卡的接口名,password:wpa的密码
    #输出：输入命令返回的结果
    def connect_WPA_AP(self,ssid,password,wlan):
        try:
            for i in range(3):
                #获取测试主机密码
                d = data.data_basic()
                #进入wpa_cli的配置命令
                child = pexpect.spawn('sudo wpa_cli',timeout=5)
                child.expect([':',pexpect.TIMEOUT,pexpect.EOF])
                child.sendline(d['PC_pwd'])
                time.sleep(5)

                #删除无线网络id为0的配置
                child.expect('>')
                child.sendline('remove_network 0')
                print ('remove_network 0')
                #增加无线网络id为0 的配置
                child.expect('>')
                child.sendline('add_network')
                print ('add_network')
                #设置无线网络id为0的无线ssid
                child.expect('>')
                ESSID = 'set_network 0 ssid \"%s\"'%str(ssid)
                print (ESSID)
                child.sendline(ESSID)
                #设置无线网络id为0的密码
                child.expect('>')
                key = 'set_network 0 psk \"%s\"'%str(password)
                print (key)
                child.sendline(key)

                #选择无线网络id为0网络
                child.expect('>')
                child.sendline('select_network 0')
                print ('select_network 0')
                time.sleep(10)
                #启用无线网络id为0网络
                child.expect('>')
                child.sendline('enable_network 0')
                print ('enable_network 0')
                #退出wpa_cli
                child.expect('>')
                time.sleep(20)
                child.sendline('quit')
                print ('quit')
                #退出wpa_cli交互模式
                child.close(force=True)
                #判断是否连接AP成功
                result1 = subprocess.check_output("iw dev %s link"%wlan,shell=True).decode('utf-8')
                if "Not connected" in result1:
                    print ("Connect AP failed,wait 60s and try again the times:%s"%(i+1))
                    #断开已连接的无线网络
                    PublicControl.disconnect_ap(self)
                    #disable/enable 无线网卡
                    PublicControl.wlan_disable(self,wlan)
                    PublicControl.wlan_enable(self,wlan)
                    PublicControl.ssid_scan_result(self,ssid,wlan)
                    ssh = SSH(d['DUT_ip'],d['ssh_pwd'])
                    ssh.ssh_cmd(d['ssh_user'],"iwconfig")
                    subprocess.call("echo %s |sudo -S /etc/init.d/network-manager restart"%d["PC_pwd"],shell=True)
                    time.sleep(60)
                else:
                    print ("Connect AP successfully!")
                    break
            #判断是否连接AP成功
            result = subprocess.check_output("iw dev %s link"%wlan,shell=True).decode('utf-8')
            print (result)
            return result
        #捕捉异常并打印异常信息
        except Exception as e:
            raise Exception("connect AP of WPA encryption fail! The reason is %s"%e)

    #描述：通过wpa_cli命令来连接802.1x的无线网络
    #输入：ssid:需要连接的无线网络的ssid,wlan:无线网卡的接口名,password:wpa的密码
    #输出：输入命令返回的结果
    def connect_8021x_AP(self,ssid,username,password,wlan):
        try:
            for i in range(3):
                #获取测试主机密码
                d = data.data_basic()
                #进入wpa_cli的配置命令
                child = pexpect.spawn('sudo wpa_cli',timeout=5)
                child.expect([':',pexpect.TIMEOUT,pexpect.EOF])
                child.sendline(d['PC_pwd'])
                time.sleep(5)

                #删除无线网络id为0的配置
                child.expect('>')
                child.sendline('remove_network 0')
                print ('remove_network 0')
                #增加无线网络id为0 的配置
                child.expect('>')
                child.sendline('add_network')
                print ('add_network')
                #设置无线网络id为0的无线ssid
                child.expect('>')
                ESSID = 'set_network 0 ssid \"%s\"'%str(ssid)
                print (ESSID)
                child.sendline(ESSID)

                child.expect('>')
                print ('set_network 0 key_mgmt WPA-EAP')
                child.sendline('set_network 0 key_mgmt WPA-EAP')
                child.expect('>')
                print ('set_network 0 eap PEAP')
                child.sendline('set_network 0 eap PEAP')
                child.expect('>')
                #输入用户名
                Uname = 'set_network 0 identity \"%s\"'%str(username)
                print (Uname)
                child.sendline(Uname)
                child.expect('>')
                #输入密码
                PW = 'set_network 0 password \"%s\"'%str(password)
                print (PW)
                child.sendline(PW)
                child.expect('>')

                print ('set_network 0 eapol_flags 0')
                child.sendline('set_network 0 eapol_flags 0')

                #选择无线网络id为0网络
                child.expect('>')
                child.sendline('select_network 0')
                print ('select_network 0')
                time.sleep(10)
                #启用无线网络id为0网络
                child.expect('>')
                child.sendline('enable_network 0')
                print ('enable_network 0')
                #退出wpa_cli
                child.expect('>')
                time.sleep(20)
                child.sendline('quit')
                print ('quit')
                #退出wpa_cli交互模式
                child.close(force=True)
                #判断是否连接AP成功
                result1 = subprocess.check_output("iw dev %s link"%wlan,shell=True).decode('utf-8')
                if "Not connected" in result1:
                    print ("Connect AP failed,wait 60s and try again the times:%s"%(i+1))
                    #断开已连接的无线网络
                    PublicControl.disconnect_ap(self)
                    #disable/enable 无线网卡
                    PublicControl.wlan_disable(self,wlan)
                    PublicControl.wlan_enable(self,wlan)
                    PublicControl.ssid_scan_result(self,ssid,wlan)
                    ssh = SSH(d['DUT_ip'],d['ssh_pwd'])
                    ssh.ssh_cmd(d['ssh_user'],"iwconfig")
                    subprocess.call("echo %s |sudo -S /etc/init.d/network-manager restart"%d["PC_pwd"],shell=True)
                    time.sleep(60)
                else:
                    print ("Connect AP successfully!")
                    break
            #判断是否连接AP成功
            result = subprocess.check_output("iw dev %s link"%wlan,shell=True).decode('utf-8')
            print (result)
            return result

        #捕捉异常并打印异常信息
        except Exception as e:
            raise Exception("connect AP of WPA 802.1x encryption fail! The reason is %s"%e)

    #描述：通过wpa_cli命令来连接802.1x的无线网络--备份
    #输入：ssid:需要连接的无线网络的ssid,wlan:无线网卡的接口名,password:wpa的密码
    #输出：输入命令返回的结果
    def connect_8021x_AP_backup(self,ssid,username,password,wlan):
        try:
                #获取测试主机密码
                d = data.data_basic()
                #进入wpa_cli的配置命令
                child = pexpect.spawn('sudo wpa_cli',timeout=5)
                child.expect([':',pexpect.TIMEOUT,pexpect.EOF])
                child.sendline(d['PC_pwd'])
                time.sleep(5)

                #删除无线网络id为0的配置
                child.expect('>')
                child.sendline('remove_network 0')
                print ('remove_network 0')
                #增加无线网络id为0 的配置
                child.expect('>')
                child.sendline('add_network')
                print ('add_network')
                #设置无线网络id为0的无线ssid
                child.expect('>')
                ESSID = 'set_network 0 ssid \"%s\"'%str(ssid)
                print (ESSID)
                child.sendline(ESSID)

                child.expect('>')
                print ('set_network 0 key_mgmt WPA-EAP')
                child.sendline('set_network 0 key_mgmt WPA-EAP')
                child.expect('>')
                print ('set_network 0 eap PEAP')
                child.sendline('set_network 0 eap PEAP')
                child.expect('>')
                #输入用户名
                Uname = 'set_network 0 identity \"%s\"'%str(username)
                print (Uname)
                child.sendline(Uname)
                child.expect('>')
                #输入密码
                PW = 'set_network 0 password \"%s\"'%str(password)
                print (PW)
                child.sendline(PW)
                child.expect('>')

                print ('set_network 0 eapol_flags 0')
                child.sendline('set_network 0 eapol_flags 0')

                #选择无线网络id为0网络
                child.expect('>')
                child.sendline('select_network 0')
                print ('select_network 0')
                time.sleep(10)
                #启用无线网络id为0网络
                child.expect('>')
                child.sendline('enable_network 0')
                print ('enable_network 0')
                #退出wpa_cli
                child.expect('>')
                time.sleep(20)
                child.sendline('quit')
                print ('quit')
                #退出wpa_cli交互模式
                child.close(force=True)
                #判断是否连接AP成功
                result = subprocess.check_output("iw dev %s link"%wlan,shell=True).decode('utf-8')
                print (result)
                return result

        #捕捉异常并打印异常信息
        except Exception as e:
            raise Exception("connect AP of WPA 802.1x encryption fail! The reason is %s"%e)


    #描述：通过wpa_cli命令来断开已连接的无线网络
    def disconnect_ap(self):
        try:
            #获取测试主机密码
            d = data.data_basic()
            #进入wpa_cli的配置命令
            child = pexpect.spawn('sudo wpa_cli',timeout=5)
            child.expect([':',pexpect.TIMEOUT,pexpect.EOF])
            child.sendline(d['PC_pwd'])
            time.sleep(5)

            #删除无线网络id为0的配置
            child.expect('>')
            child.sendline('remove_network 0')
            #退出wpa_cli
            child.expect('>')
            time.sleep(2)
            child.sendline('quit')
            #退出wpa_cli交互模式
            child.close(force=True)
            print ("disconnect ap successfully!")
        #捕捉异常并打印异常信息
        except Exception as e:
            raise Exception("disconnect ap fail! The reason is %s"%e)


    #描述：通过wpa_cli命令来连接不加密的隐藏无线网络
    #输入：ssid:需要连接的无线网络的ssid,wlan:无线网卡的接口名
    #输出：输入命令返回的结果
    def connect_NONE_hiddenssid_AP(self,ssid,wlan):
        try:
            for i in range(3):
                #获取测试主机密码
                d = data.data_basic()
                #进入wpa_cli的配置命令
                child = pexpect.spawn('sudo wpa_cli',timeout=5)
                child.expect([':',pexpect.TIMEOUT,pexpect.EOF])
                child.sendline(d['PC_pwd'])
                time.sleep(5)

                #删除无线网络id为0的配置
                child.expect('>')
                child.sendline('remove_network 0')
                #增加无线网络id为0的配置
                child.expect('>')
                child.sendline('add_network')
                #设置无线网络id为0的无线ssid
                child.expect('>')
                ESSID = 'set_network 0 ssid \"%s\"'%str(ssid)
                print (ESSID)
                child.sendline(ESSID)
                #设置无线网络id为0的ssid进行特定扫描，即隐藏的ssid
                child.expect('>')
                print ('set_network 0 scan_ssid 1')
                child.sendline('set_network 0 scan_ssid 1')
                #设置无线网络id为0的加密为非加密
                child.expect('>')
                child.sendline('set_network 0 key_mgmt NONE')
                #禁用无线网络id为0网络
                child.expect('>')
                child.sendline('disable_network 0')
                #启用无线网络id为0网络
                child.expect('>')
                child.sendline('enable_network 0')
                time.sleep(10)
                #退出wpa_cli
                child.expect('>')
                time.sleep(20)
                child.sendline('quit')
                #退出wpa_cli交互模式
                child.close(force=True)

                #判断是否连接AP成功
                result1 = subprocess.check_output("iw dev %s link"%wlan,shell=True).decode('utf-8')
                if "Not connected" in result1:
                    print ("Connect AP failed,wait 60s and try again the times:%s"%(i+1))
                    #断开已连接的无线网络
                    PublicControl.disconnect_ap(self)
                    #disable/enable 无线网卡
                    PublicControl.wlan_disable(self,wlan)
                    PublicControl.wlan_enable(self,wlan)
                    PublicControl.ssid_scan_result(self,ssid,wlan)
                    subprocess.call("echo %s |sudo -S /etc/init.d/network-manager restart"%d["PC_pwd"],shell=True)
                    time.sleep(60)
                else:
                    print ("Connect hide AP successfully!")
                    break

            #判断是否连接AP成功
            result = subprocess.check_output("iw dev %s link"%wlan,shell=True).decode('utf-8')
            print (result)
            return result
        #捕捉异常并打印异常信息
        except Exception as e:
            raise Exception("connect AP of NONE encryption and hiddenssid fail! The reason is %s"%e)

    #描述：通过wpa_cli命令来连接不加密的隐藏无线网络--备份
    #输入：ssid:需要连接的无线网络的ssid,wlan:无线网卡的接口名
    #输出：输入命令返回的结果
    def connect_NONE_hiddenssid_AP_backup(self,ssid,wlan):
        try:
            #获取测试主机密码
            d = data.data_basic()
            #进入wpa_cli的配置命令
            child = pexpect.spawn('sudo wpa_cli',timeout=5)
            child.expect([':',pexpect.TIMEOUT,pexpect.EOF])
            child.sendline(d['PC_pwd'])
            time.sleep(5)

            #删除无线网络id为0的配置
            child.expect('>')
            child.sendline('remove_network 0')
            #增加无线网络id为0的配置
            child.expect('>')
            child.sendline('add_network')
            #设置无线网络id为0的无线ssid
            child.expect('>')
            ESSID = 'set_network 0 ssid \"%s\"'%str(ssid)
            print (ESSID)
            child.sendline(ESSID)
            #设置无线网络id为0的ssid进行特定扫描，即隐藏的ssid
            child.expect('>')
            print ('set_network 0 scan_ssid 1')
            child.sendline('set_network 0 scan_ssid 1')
            #设置无线网络id为0的加密为非加密
            child.expect('>')
            child.sendline('set_network 0 key_mgmt NONE')
            #禁用无线网络id为0网络
            child.expect('>')
            child.sendline('disable_network 0')
            #启用无线网络id为0网络
            child.expect('>')
            child.sendline('enable_network 0')
            time.sleep(10)
            #退出wpa_cli
            child.expect('>')
            time.sleep(20)
            child.sendline('quit')
            #退出wpa_cli交互模式
            child.close(force=True)

            #判断是否连接AP成功
            result = subprocess.check_output("iw dev %s link"%wlan,shell=True).decode('utf-8')
            print (result)
            return result
        #捕捉异常并打印异常信息
        except Exception as e:
            raise Exception("connect AP of NONE encryption and hiddenssid fail! The reason is %s"%e)

    #描述：通过wpa_cli命令来连接WEP的隐藏无线网络
    #输入：ssid:需要连接的无线网络的ssid,wlan:无线网卡的接口名,password:wep的密码
    #输出：输入命令返回的结果
    def connect_WEP_hiddenssid_AP(self,ssid,password,wlan):
        try:
            for i in range(3):
                #获取测试主机密码
                d = data.data_basic()
                #进入wpa_cli的配置命令
                child = pexpect.spawn('sudo wpa_cli',timeout=5)
                child.expect([':',pexpect.TIMEOUT,pexpect.EOF])
                child.sendline(d['PC_pwd'])
                time.sleep(5)

                #删除无线网络id为0的配置
                child.expect('>')
                child.sendline('remove_network 0')
                #增加无线网络id为0的配置
                child.expect('>')
                child.sendline('add_network')
                #设置无线网络id为0的无线ssid
                child.expect('>')
                ESSID = 'set_network 0 ssid \"%s\"'%str(ssid)
                print (ESSID)
                child.sendline(ESSID)
                #设置无线网络id为0的ssid进行特定扫描，即隐藏的ssid
                child.expect('>')
                print ('set_network 0 scan_ssid 1')
                child.sendline('set_network 0 scan_ssid 1')
                #设置无线网络id为0的加密为非加密
                child.expect('>')
                child.sendline('set_network 0 key_mgmt NONE')
                #设置无线网络id为0的密码
                child.expect('>')
                key = 'set_network 0 wep_key0 \"%s\"'%str(password)
                print (key)
                child.sendline(key)
                child.expect('>')
                child.sendline('set_network 0 wep_tx_keyidx 0')

                #选择无线网络id为0网络
                child.expect('>')
                child.sendline('select_network 0')
                time.sleep(10)
                #启用无线网络id为0网络
                child.expect('>')
                child.sendline('enable_network 0')
                #退出wpa_cli
                child.expect('>')
                time.sleep(20)
                child.sendline('quit')
                #退出wpa_cli交互模式
                child.close(force=True)

                #判断是否连接AP成功
                result1 = subprocess.check_output("iw dev %s link"%wlan,shell=True).decode('utf-8')
                if "Not connected" in result1:
                    print ("Connect AP failed,wait 60s and try again the times:%s"%(i+1))
                    #断开已连接的无线网络
                    PublicControl.disconnect_ap(self)
                    #disable/enable 无线网卡
                    PublicControl.wlan_disable(self,wlan)
                    PublicControl.wlan_enable(self,wlan)
                    PublicControl.ssid_scan_result(self,ssid,wlan)
                    subprocess.call("echo %s |sudo -S /etc/init.d/network-manager restart"%d["PC_pwd"],shell=True)
                    time.sleep(60)
                else:
                    print ("Connect hide AP successfully!")
                    break

            #判断是否连接AP成功
            result = subprocess.check_output("iw dev %s link"%wlan,shell=True).decode('utf-8')
            print (result)
            return result
        #捕捉异常并打印异常信息
        except Exception as e:
            raise Exception("connect AP of WEP encryption and hiddenssid fail! The reason is %s"%e)

    #描述：通过wpa_cli命令来连接WEP的隐藏无线网络--备份
    #输入：ssid:需要连接的无线网络的ssid,wlan:无线网卡的接口名,password:wep的密码
    #输出：输入命令返回的结果
    def connect_WEP_hiddenssid_AP_backup(self,ssid,password,wlan):
        try:
            #获取测试主机密码
            d = data.data_basic()
            #进入wpa_cli的配置命令
            child = pexpect.spawn('sudo wpa_cli',timeout=5)
            child.expect([':',pexpect.TIMEOUT,pexpect.EOF])
            child.sendline(d['PC_pwd'])
            time.sleep(5)

            #删除无线网络id为0的配置
            child.expect('>')
            child.sendline('remove_network 0')
            #增加无线网络id为0的配置
            child.expect('>')
            child.sendline('add_network')
            #设置无线网络id为0的无线ssid
            child.expect('>')
            ESSID = 'set_network 0 ssid \"%s\"'%str(ssid)
            print (ESSID)
            child.sendline(ESSID)
            #设置无线网络id为0的ssid进行特定扫描，即隐藏的ssid
            child.expect('>')
            print ('set_network 0 scan_ssid 1')
            child.sendline('set_network 0 scan_ssid 1')
            #设置无线网络id为0的加密为非加密
            child.expect('>')
            child.sendline('set_network 0 key_mgmt NONE')
            #设置无线网络id为0的密码
            child.expect('>')
            key = 'set_network 0 wep_key0 \"%s\"'%str(password)
            print (key)
            child.sendline(key)
            child.expect('>')
            child.sendline('set_network 0 wep_tx_keyidx 0')

            #选择无线网络id为0网络
            child.expect('>')
            child.sendline('select_network 0')
            time.sleep(10)
            #启用无线网络id为0网络
            child.expect('>')
            child.sendline('enable_network 0')
            #退出wpa_cli
            child.expect('>')
            time.sleep(20)
            child.sendline('quit')
            #退出wpa_cli交互模式
            child.close(force=True)

            #判断是否连接AP成功
            result = subprocess.check_output("iw dev %s link"%wlan,shell=True).decode('utf-8')
            print (result)
            return result
        #捕捉异常并打印异常信息
        except Exception as e:
            raise Exception("connect AP of WEP encryption and hiddenssid fail! The reason is %s"%e)


    #描述：通过wpa_cli命令来连接WPA的隐藏无线网络
    #输入：ssid:需要连接的无线网络的ssid,wlan:无线网卡的接口名,password:wpa的密码
    #输出：输入命令返回的结果
    def connect_WPA_hiddenssid_AP(self,ssid,password,wlan):
        try:
            for i in range(3):
                #获取测试主机密码
                d = data.data_basic()
                #进入wpa_cli的配置命令
                child = pexpect.spawn('sudo wpa_cli',timeout=5)
                child.expect([':',pexpect.TIMEOUT,pexpect.EOF])
                child.sendline(d['PC_pwd'])
                time.sleep(5)

                #删除无线网络id为0的配置
                child.expect('>')
                child.sendline('remove_network 0')
                #增加无线网络id为0 的配置
                child.expect('>')
                child.sendline('add_network')
                #设置无线网络id为0的无线ssid
                child.expect('>')
                ESSID = 'set_network 0 ssid \"%s\"'%str(ssid)
                print (ESSID)
                child.sendline(ESSID)
                #设置无线网络id为0的ssid进行特定扫描，即隐藏的ssid
                child.expect('>')
                print ('set_network 0 scan_ssid 1')
                child.sendline('set_network 0 scan_ssid 1')
                #设置无线网络id为0的密码
                child.expect('>')
                key = 'set_network 0 psk \"%s\"'%str(password)
                print (key)
                child.sendline(key)

                #选择无线网络id为0网络
                child.expect('>')
                child.sendline('select_network 0')
                time.sleep(10)
                #启用无线网络id为0网络
                child.expect('>')
                child.sendline('enable_network 0')
                #退出wpa_cli
                child.expect('>')
                time.sleep(20)
                child.sendline('quit')
                #退出wpa_cli交互模式
                child.close(force=True)

                #判断是否连接AP成功
                result1 = subprocess.check_output("iw dev %s link"%wlan,shell=True).decode('utf-8')
                if "Not connected" in result1:
                    print ("Connect AP failed,wait 60s and try again the times:%s"%(i+1))
                    #断开已连接的无线网络
                    PublicControl.disconnect_ap(self)
                    #disable/enable 无线网卡
                    PublicControl.wlan_disable(self,wlan)
                    PublicControl.wlan_enable(self,wlan)
                    PublicControl.ssid_scan_result(self,ssid,wlan)
                    subprocess.call("echo %s |sudo -S /etc/init.d/network-manager restart"%d["PC_pwd"],shell=True)
                    time.sleep(60)
                else:
                    print ("Connect hide AP successfully!")
                    break

            #判断是否连接AP成功
            result = subprocess.check_output("iw dev %s link"%wlan,shell=True).decode('utf-8')
            print (result)
            return result
        #捕捉异常并打印异常信息
        except Exception as e:
            raise Exception("connect AP of WPA encryption and hiddenssid fail! The reason is %s"%e)

    #描述：通过wpa_cli命令来连接WPA的隐藏无线网络--备份
    #输入：ssid:需要连接的无线网络的ssid,wlan:无线网卡的接口名,password:wpa的密码
    #输出：输入命令返回的结果
    def connect_WPA_hiddenssid_AP_backup(self,ssid,password,wlan):
        try:
            #获取测试主机密码
            d = data.data_basic()
            #进入wpa_cli的配置命令
            child = pexpect.spawn('sudo wpa_cli',timeout=5)
            child.expect([':',pexpect.TIMEOUT,pexpect.EOF])
            child.sendline(d['PC_pwd'])
            time.sleep(5)

            #删除无线网络id为0的配置
            child.expect('>')
            child.sendline('remove_network 0')
            #增加无线网络id为0 的配置
            child.expect('>')
            child.sendline('add_network')
            #设置无线网络id为0的无线ssid
            child.expect('>')
            ESSID = 'set_network 0 ssid \"%s\"'%str(ssid)
            print (ESSID)
            child.sendline(ESSID)
            #设置无线网络id为0的ssid进行特定扫描，即隐藏的ssid
            child.expect('>')
            print ('set_network 0 scan_ssid 1')
            child.sendline('set_network 0 scan_ssid 1')
            #设置无线网络id为0的密码
            child.expect('>')
            key = 'set_network 0 psk \"%s\"'%str(password)
            print (key)
            child.sendline(key)

            #选择无线网络id为0网络
            child.expect('>')
            child.sendline('select_network 0')
            time.sleep(10)
            #启用无线网络id为0网络
            child.expect('>')
            child.sendline('enable_network 0')
            #退出wpa_cli
            child.expect('>')
            time.sleep(20)
            child.sendline('quit')
            #退出wpa_cli交互模式
            child.close(force=True)

            #判断是否连接AP成功
            result = subprocess.check_output("iw dev %s link"%wlan,shell=True).decode('utf-8')
            print (result)
            return result
        #捕捉异常并打印异常信息
        except Exception as e:
            raise Exception("connect AP of WPA encryption and hiddenssid fail! The reason is %s"%e)

    #无线网卡通过各种加密方式连接ssid
    #输入：wifi_encryption：ssid的加密方式
    def client_connect_ssid(self, ssid, wlan, wifi_encryption, password=None):
        if wifi_encryption == "open":
            return self.connect_NONE_AP(ssid,wlan)
        elif wifi_encryption == "wep":
            return self.connect_WEP_AP(ssid,password,wlan)
        elif wifi_encryption == "wep10_26":
            return self.connect_WEP10_26_AP(ssid,password,wlan)
        elif wifi_encryption == "wpa":
            return self.connect_WPA_AP(ssid,password,wlan)
        elif wifi_encryption == "wpa_hiddenssid":
            return self.connect_WPA_hiddenssid_AP(ssid,password,wlan)
        else:
            print("please choose the right wifi encryption!")


    #描述：使无线网卡获取IP地址
    #输入：wlan:无线网卡的接口名
    #输出：无
    def dhcp_wlan(self,wlan):
        try:
            #获取测试主机密码
            d = data.data_basic()
            #输入无线网卡获取IP地址的命令
            down = pexpect.spawn('sudo dhclient %s'%wlan,timeout=5)
            down.expect([':',pexpect.TIMEOUT,pexpect.EOF])
            down.sendline(d["PC_pwd"])
            time.sleep(30)
            print ("renew %s ip successfully!"%wlan)
        except Exception as e:
            raise Exception("dhcp wlan ip address fail! The reason is %s"%e)

    #描述：使无线网卡释放IP地址
    #输入：wlan:无线网卡的接口名
    #输出：无
    def dhcp_release_wlan(self,wlan):
        try:
            #获取测试主机密码
            d = data.data_basic()
            #输入无线网卡获取IP地址的命令
            down = pexpect.spawn('sudo dhclient -r %s'%wlan,timeout=5)
            down.expect([':',pexpect.TIMEOUT,pexpect.EOF])
            down.sendline(d["PC_pwd"])
            time.sleep(10)
            #subprocess.call('echo %s |sudo -S /etc/init.d/network-manager force-reload'%d["PC_pwd"],shell=True)
            time.sleep(20)
            print ("release %s ip successfully!"%wlan)
        except Exception as e:
            raise Exception("dhcp release wlan ip address fail! The reason is %s"%e)

    #判断使用无线网卡能够连接上ssid,并正常使用
    def connect_DHCP_WPA_AP(self,ssid,password,wlan):
        result = PublicControl.connect_WPA_AP(self,ssid,password,wlan)
        if "Not connected" not in result:
            PublicControl.dhcp_wlan(self,wlan)
            print (ssid)
            return result
        else:
            print ("wifi card hasn't connected AP! ")
            return result

    #使用无线网卡连接上AP后，取出该AP的频率值
    def connected_AP_Freq(self,ssid,password,wlan):
        a = PublicControl.connect_WPA_AP(self,ssid,password,wlan)
        if "Not connected" not in a:
            b = a.split("\n\t")
            d = b[-8].strip("freq: ")
            print (int(d))
            return int(d)
        else:
            print ("wifi card hasn't connected AP! ")

    #使用无线网卡连接上AP后，取出该AP的linkspeed
    def connected_AP_linkspeed(self,ssid,password,wlan):
        a = PublicControl.connect_WPA_AP(self,ssid,password,wlan)
        if "Not connected" not in a:
            b = a.split("\n\t")
            c = b[-4].split(" ")
            d = float(c[2])
            print (int(d))
            return int(d)
        else:
            print ("wifi card hasn't connected AP! ")

    #扫描双频的AP，扫描5次，当扫描到有两个相同SSID时就退出，没有就返回None
    def scan_dual_band_same_SSID(self,ssid,wlan):
        for i in range(5):
            tmp = PublicControl.ssid_scan(self,ssid,wlan)
            tmp1 = tmp.split("\n\t")
            result = len(tmp1)
            print (result)
            if result == 2:
                print ("wifi card can scan two same SSID!")
                return result
            print ("wifi card can't scan two same SSID,wait 60s and go on...")
            time.sleep(60)
        print ("scan 5 times,wifi card can't scan two same SSID!")

    #描述：登录ftp后ftp上传文件
    def ftp_put(self,putfilename):
        d = data.data_basic()
        #使用spawn构造一个函数，生成一个spawn类的对象
        child = pexpect.spawn('ftp %s'%d['ftp_server'],timeout=5)
        #期望具有提示输入用户名的字符出现
        index = child.expect(["(?i)Unknown host", "(?i)Name", pexpect.EOF, pexpect.TIMEOUT])
        #匹配到了"(?i)Name"，表明接下来要输入用户名
        if index != 0 :
            #输入用户名
            child.sendline(d['ftp_name'])
            #期望具体有提示输入密码的字符出现
            child.expect(["(?i)Password", pexpect.EOF, pexpect.TIMEOUT])
            child.sendline(d['ftp_pwd'])
            #期望登录成功并出现'ftp>'的字符出现
            index = child.expect( ['ftp>', 'Login incorrect', 'Service not available',pexpect.EOF, pexpect.TIMEOUT])
            #匹配到了'ftp>'，则表示登录ftp成功
            if index == 0:
                print (u'恭喜！ftp登录成功')
                # 发送 'bin'+ 换行符给子程序，表示接下来使用二进制模式来传输文件.
                child.sendline("bin")
                child.expect('>')
                child.sendline("cd %s"%d['ftp_dir'])
                print (u'正在上传文件...')
                #输入上传文件的命令
                child.sendline('put %s'%putfilename)
                time.sleep(180)
                #期望下载成功后，出现 'Transfer complete*ftp>'的字符
                index = child.expect( ['ftp>', pexpect.EOF, pexpect.TIMEOUT] )
                #没有匹配到'*ftp>'的字符，表示EOF或超时，打印超时并退出
                if index != 0:
                    print ("上传文件时出现EOF或超时")
                    #强制退出
                    child.close(force=True)
                #匹配到了 '*ftp>'，表明上传文件成功，打印成功信息.
                print (u'成功上传文件%s'%putfilename)

                #输入 'bye'，结束 ftp session.
                child.sendline("bye")
                print (u'传输文件完成，程序退出！')

            #匹配到了'Login incorrect'，则表示登录ftp失败，用户名或密码错误
            elif index == 1:
                print ("登录ftp失败，用户名或密码错误!程序退出")
                child.close(force=True)

            #匹配到其他值（'Service not available',pexpect.EOF, pexpect.TIMEOUT），则表示登录ftp失败.
            else:
                print ("登录ftp失败，服务器不可用或ftp命令退出或超时!程序退出")
                child.close(force=True)

        #匹配到了"(?i)Unknown host"，则表示主机未知
        elif index == 1 :
            print ("没有找到ftp主机!程序退出")
            child.close(force=True)

        #匹配到了 pexpect.EOF 或 pexpect.TIMEOUT，表示超时或者 EOF，程序打印提示信息并退出
        else:
            print ("连接ftp时出现EOF或超时")
            child.close(force=True)

    #描述：登录ftp后ftp下载文件
    def ftp_get(self,putfilename):
        d = data.data_basic()
        #使用spawn构造一个函数，生成一个spawn类的对象
        child = pexpect.spawn('ftp %s'%d['ftp_server'],timeout=5)
        #期望具有提示输入用户名的字符出现
        index = child.expect(["(?i)Unknown host", "(?i)Name", pexpect.EOF, pexpect.TIMEOUT])
        #匹配到了"(?i)Name"，表明接下来要输入用户名
        if index != 0 :
            #输入用户名
            child.sendline(d['ftp_name'])
            #期望具体有提示输入密码的字符出现
            child.expect(["(?i)Password", pexpect.EOF, pexpect.TIMEOUT])
            child.sendline(d['ftp_pwd'])
            #期望登录成功并出现'ftp>'的字符出现
            index = child.expect( ['ftp>', 'Login incorrect', 'Service not available',pexpect.EOF, pexpect.TIMEOUT])
            #匹配到了'ftp>'，则表示登录ftp成功
            if index == 0:
                print (u'恭喜！ftp登录成功')
                # 发送 'bin'+ 换行符给子程序，表示接下来使用二进制模式来传输文件.
                child.sendline("bin")
                child.expect('>')
                child.sendline("cd %s"%d['ftp_dir'])
                print (u'正在下载文件...')
                #输入上传文件的命令
                child.sendline('get %s'%putfilename)
                time.sleep(180)
                #期望下载成功后，出现 'Transfer complete*ftp>'的字符
                index = child.expect( ['ftp>', pexpect.EOF, pexpect.TIMEOUT] )
                #没有匹配到'*ftp>'的字符，表示EOF或超时，打印超时并退出
                if index != 0:
                    print ("上传文件时出现EOF或超时")
                    #强制退出
                    child.close(force=True)
                #匹配到了 '*ftp>'，表明上传文件成功，打印成功信息.
                print (u'成功下载文件%s'%putfilename)

                #输入 'bye'，结束 ftp session.
                child.sendline("bye")
                print (u'传输文件完成，程序退出！')

            #匹配到了'Login incorrect'，则表示登录ftp失败，用户名或密码错误
            elif index == 1:
                print ("登录ftp失败，用户名或密码错误!程序退出")
                child.close(force=True)

            #匹配到其他值（'Service not available',pexpect.EOF, pexpect.TIMEOUT），则表示登录ftp失败.
            else:
                print ("登录ftp失败，服务器不可用或ftp命令退出或超时!程序退出")
                child.close(force=True)

        #匹配到了"(?i)Unknown host"，则表示主机未知
        elif index == 1 :
            print ("没有找到ftp主机!程序退出")
            child.close(force=True)

        #匹配到了 pexpect.EOF 或 pexpect.TIMEOUT，表示超时或者 EOF，程序打印提示信息并退出
        else:
            print ("连接ftp时出现EOF或超时")
            child.close(force=True)

    #判断是否能够连接ftp成功
    def check_ftp_connect(self, host):
        try:
            # 为 ssh 命令生成一个 spawn 类的子程序对象.
            child = pexpect.spawn('ftp', timeout=10)
            #期望具有提示输入用户名的字符出现
            child.expect(['ftp>', pexpect.TIMEOUT])
            child.sendline("open {}".format(host))
            i = child.expect(["(?i)Name",'(?i)No route to host', '(?i)Connection refused', pexpect.TIMEOUT])
            if i == 0:
                print("能够连接成功")
                print(child.before, child.after)
                child.close(force=True)
                return True
            else:
                print("不能够连接成功")
                print(child.before, child.after)
                child.close(force=True)
                return False
        except Exception as e:
            print("ftp连接失败")
            print(e)


    #移动resolv.conf到/etc/目录下
    def move_resolv(self):
        d = data.data_basic()
        subprocess.call('echo %s |sudo -S cp ./data/resolv.conf /etc/'%(d["PC_pwd"]),shell=True)
        time.sleep(10)
        print ("move resolv.conf to /etc/ successfully!")


    #判断并等待直到slave ap已经在可解除配对的状态
    def enable_unpair_slave_ap(self,slave_ip):
        try:
            while True:
                #在路由器中输入netstat -ant
                ssh = SSH(data_basic['DUT_ip'],data_login['all'])
                result = ssh.ssh_cmd(data_basic['ssh_user'],"netstat -ant | grep %s"%slave_ip)
                if ("TIME_WAIT" not in result) and ("ESTABLISHED" in result):
                    break
                time.sleep(30)
        #捕捉异常并打印异常信息
        except Exception as e:
            raise Exception("check slave ap can been unpair fail! The reason is %s"%e)

    #将ap恢复出厂设置
    def set_ap_factory(self,ip):
        try:
            #在路由器中输入netstat -ant
            ssh = SSH(ip,data_login['all'])
            ssh.ssh_cmd(data_basic['ssh_user'],"ubus call controller.icc factory_reset")
        #捕捉异常并打印异常信息
        except Exception as e:
            raise Exception("set ap factory fail! The reason is %s"%e)

    #给网卡固定ip
    #eth为网卡接口名，ip为要设置的固定ip
    def set_eth_ip(self, eth, ip):
        try:
            d = data.data_basic()
            #使用spawn构造一个函数，生成一个spawn类的对象
            #将要设置的网卡名和固定ip拼接成一个字符串
            child = pexpect.spawn('sudo ifconfig %s %s'%(eth, ip),timeout=5)
            child.expect([':',pexpect.TIMEOUT,pexpect.EOF])
            child.sendline(d['PC_pwd'])
            print('set eth static ip successfully!')
            time.sleep(5)
        except Exception as e:
            raise Exception("set PC ip fail! The reason is %s"%e)


    #取消网卡固定ip
    def remove_eth_ip(self, eth):
        try:
            d = data.data_basic()
            #使用spawn构造一个函数，生成一个spawn类的对象
            child = pexpect.spawn('sudo dhclient -r %s'%eth,timeout=5)
            child.expect([':',pexpect.TIMEOUT,pexpect.EOF])
            child.sendline(d['PC_pwd'])
            print('remove eth static ip successfully!')
            time.sleep(5)
        except Exception as e:
            raise Exception("remove PC ip fail! The reason is %s"%e)

    #描述：禁用网卡
    #输入：self
    #输出：None
    def networkcard_disable(self):
        try:
            d = data.data_basic()
            #禁用eth0网卡
            down = pexpect.spawn('sudo ifconfig %s down'%d['lan_pc'],timeout=5)
            down.expect([':',pexpect.TIMEOUT,pexpect.EOF])
            down.sendline(d["PC_pwd"])
            time.sleep(15)
        #捕捉异常并打印异常信息
        except Exception as e:
            raise Exception("disable eth of PC fail! The reason is %s"%e)

    #描述：启用网卡
    #输入：self
    #输出：None
    def networkcard_enable(self):
        try:
            d = data.data_basic()
            #启用eth0网卡
            up = pexpect.spawn('sudo ifconfig %s up'%d['lan_pc'],timeout=5)
            up.expect([':',pexpect.TIMEOUT,pexpect.EOF])
            up.sendline(d["PC_pwd"])
            time.sleep(15)
            #self.dhcp_wlan(d['lan_pc'])
        #捕捉异常并打印异常信息
        except Exception as e:
            raise Exception("enable eth of PC fail! The reason is %s"%e)


    #抓图方法
    def get_picture(self,picture_name):
        current_time = time.strftime('%m%d%H%M',time.localtime(time.time()))
        png = "error_{}_{}.png".format(picture_name, str(current_time))
        self.driver.get_screenshot_as_file(os.path.join(png_PATH, png))

