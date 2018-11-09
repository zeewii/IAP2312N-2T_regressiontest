#coding=utf-8
#作者：曾祥卫
#时间：2018.10.29
#描述：端口转发的业务逻辑层

from firewall.firewall_control import FireWallControl
from firewall.portforward.portforward_control import PortForwardControl
import time, subprocess, filecmp
from connect.ssh import SSH
from data import data

class PortForwardBusiness(PortForwardControl):

    def __init__(self,driver):
        #继承PortForwardControl类的属性和方法
        PortForwardControl.__init__(self,driver)

    def add_one_list(self, ip, mode, s_port, e_port):
        """添加一条端口转发规则"""
        #首先点击防火墙菜单
        tmp = FireWallControl(self.driver)
        tmp.menu_firewall()
        #再点击端口转发菜单
        self.menu_portforward()
        #击添加按钮
        self.click_add_button()
        #设置IP地址
        self.set_IP_address(ip)
        #选择协议
        self.set_Protocol(mode)
        #设置起始端口
        self.set_start_port(s_port)
        #设置结束端口
        self.set_end_port(e_port)
        #点击保存按钮
        self.click_save_button()
        time.sleep(30)

    def delete_n_list(self, n):
        """
        删除第n条端口转发的规则list
        """
        #首先点击防火墙菜单
        tmp = FireWallControl(self.driver)
        tmp.menu_firewall()
        #再点击端口转发菜单
        self.menu_portforward()
        #点击选择第几个list
        self.click_choice_n_list(n)
        #点击删除所选按钮
        self.click_delete_button()
        time.sleep(30)

    def edit_n_list(self, n, ip, mode, s_port, e_port):
        """
        编辑第n条端口转发的规则list
        """
        #首先点击防火墙菜单
        tmp = FireWallControl(self.driver)
        tmp.menu_firewall()
        #再点击端口转发菜单
        self.menu_portforward()
        #点击编辑第几个list
        self.click_edit_n_list_button(n)
        #编辑IP地址
        self.edit_IP_address(ip)
        #编辑选择协议
        self.edit_Protocol(mode)
        #编辑起始端口
        self.edit_start_port(s_port)
        #编辑结束端口
        self.edit_end_port(e_port)
        #点击保存按钮
        self.click_save_button()
        time.sleep(30)

    def delete_all_list(self):
        """
        删除所有的url过滤的规则list
        """
        #首先点击防火墙菜单
        tmp = FireWallControl(self.driver)
        tmp.menu_firewall()
        #再点击端口转发菜单
        self.menu_portforward()
        #点击IP过滤列表中的全选
        self.click_all_choices_button()
        #点击删除所选按钮
        self.click_delete_button()
        time.sleep(30)

    def check_portforward_function(self, host, user, pwd, ap_wan_ip):
        """
        判断端口转发功能是否有效--验证80端口
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

    def add_10_list(self, ip, mode):
        """
        添加10条规则
        """
        #首先点击防火墙菜单
        tmp = FireWallControl(self.driver)
        tmp.menu_firewall()
        #再点击端口转发菜单
        self.menu_portforward()
        for i in range(0, 20, 2):
            #击添加按钮
            self.click_add_button()
            #设置IP地址
            self.set_IP_address(ip)
            #选择协议
            self.set_Protocol(mode)
            #设置起始端口
            self.set_start_port(60000+i)
            #设置结束端口
            self.set_end_port(60001+i)
            #点击保存按钮
            self.click_save_button()
            time.sleep(2)
        time.sleep(30)


