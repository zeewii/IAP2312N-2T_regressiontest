#coding=utf-8
#作者：曾祥卫
#时间：2018.10.29
#描述：DMZ设置的业务逻辑层

from firewall.firewall_control import FireWallControl
from firewall.dmzsettings.dmzsettings_control import DMZSettingsControl
import time, subprocess
from data import data
from connect.ssh import SSH

class DMZSettingsBusiness(DMZSettingsControl):

    def __init__(self,driver):
        #继承DMZSettingsControl类的属性和方法
        DMZSettingsControl.__init__(self,driver)

    def open_DMZ(self, ip):
        """启用DMZ功能"""
        #首先点击防火墙菜单
        tmp = FireWallControl(self.driver)
        tmp.menu_firewall()
        #再点击DMZ设置菜单
        self.menu_DMZSettings()
        #选择DMZ开关
        self.set_DMZ_switch(1)
        #设置主机IP
        self.set_Host_IP(ip)
        #点击保存按钮
        self.click_save_button()
        time.sleep(30)

    def close_DMZ(self):
        """禁用DMZ功能"""
        #首先点击防火墙菜单
        tmp = FireWallControl(self.driver)
        tmp.menu_firewall()
        #再点击DMZ设置菜单
        self.menu_DMZSettings()
        #选择DMZ开关
        self.set_DMZ_switch(0)
        #点击保存按钮
        self.click_save_button()
        time.sleep(30)

    def check_DMZ_function(self, host, user, pwd, ap_wan_ip):
        """
        判断DMZ功能是否有效--验证80端口
        输入：host,远程主机ip--现在是192.168.5.250;user,远程主机的用户名;
            pwd:远程主机的密码;ap_wan_ip：ap的wan口的ip地址
        """
        try:
            #先本机自己下载自己http服务器的文件
            self.get_client_cmd_result("wget http://127.0.0.1/test_http -O file1")
            #取出md5的值
            result1 = self.get_client_cmd_result("md5sum file1").replace("  file1", "").strip()
            print("result1={}".format(result1))
            #删除文件
            self.get_client_cmd_result("rm -rf file1")
            ssh_pc = SSH(host, pwd)
            #然后登录远程主机，访问ap的wan口的ip，下载http服务器的文件
            ssh_pc.ssh_pc_cmd(user, "wget http://{}/test_http -O file2".format(ap_wan_ip))
            #取出md5的值
            result2 = ssh_pc.ssh_pc_cmd(user, "md5sum file2").replace("  file2", "").strip()
            print("result2={}".format(result2))
            #删除文件
            ssh_pc.ssh_pc_cmd(user, "rm -rf file2")
            if result1 in result2:
                return True
            else:
                return False
        except:
            return False
