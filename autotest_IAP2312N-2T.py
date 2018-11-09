#!/usr/bin/python3
#coding=utf-8
#描述:本模块测试所有测试用例
#描述：本模块还包括测试结束后自动发送邮件给测试人员目前发送方仅限foxmail
#作者：曾祥卫
#时间：2018.09.17

import unittest
import pexpect
import smtplib
import time
import subprocess
from email.mime.text import MIMEText
from email.header import Header
from  email.utils import  parseaddr,formataddr
from email.mime.multipart import MIMEMultipart
import sys,importlib
import os

from testcase import testcase_login, testcase_workmode, testcase_configupdate, \
    testcase_lansettings,testcase_rebootsystem, testcase_wansettings, testcase_wirelesssettings, \
    testcase_wirelesssclient, testcase_stateinfo, testcase_systemupgrade, testcase_ipfilter, \
    testcase_macfilter, testcase_urlfilter, testcase_portforward, testcase_dmzsettings
from data import data, HTMLTestRunner_py3_3onedata
from data import gui

#importlib.reload(sys)
#sys.setdefaultencoding('utf-8')

#取测试平台的name
PC_name = subprocess.check_output("hostname",shell=True).decode('utf-8').strip("\n")
hostname = "(test_bed_name:%s)"%PC_name
#取出data文件中basic_conf的数据
d = data.data_basic()
d_login = data.data_login()

#选择AP型号
AP_name = "IAP2312N-2T"
#欢迎确认框
gui.welcome()
#选择测试用例框
cases = gui.choice_case()
#设置每个用例集是否需要逐个测试并发送邮件
onebyone = gui.testcase_onebyone()
#输入发送测试报告的email地址和密码
sender = gui.send_email()
#输入接收测试报告的email地址
receiver = gui.receive_email()
#设置用例执行的次数
loop_times = gui.loop_times()
#设置自动化执行人
test_executor = gui.test_executor()
#是选择定时开始测试，还是选择需要检查Internet上有固件后才进行测试
#gui.choose_timing_or_download_FW()
#设置开始时间
gui.start_time()


#定义一个字典对应gui里面的用例
dicts1 ={
        'A_login':'A',
        'B_stateinfo':'B',
        'C_workmode':'C',
        'D_lansettings':'D',
        'E_wansettings':'E',
        'F_wirelesssettings':'F',
        'G_wirelessclient':'G',
        'H_ipfilter':'H',
        'I_macfilter':"I",
        'J_urlfilter':"J",
        'K_portforward':"K",
        'L_dmzsettings':"L",
        'M_systemupgrade':"M",
        'N_configupdate':"N",
        'O_rebootsystem':"O",

    }

#定义一个字典对应creatsuite1()中的测试用例类
dicts={
    'A': testcase_login.TestLogin,
    'B': testcase_stateinfo.TestStateInfo,
    'C': testcase_workmode.TestWorkMode,
    'D': testcase_lansettings.TestLanSettings,
    'E': testcase_wansettings.TestWanSettings,
    'F': testcase_wirelesssettings.TestWirelessSettings,
    'G': testcase_wirelesssclient.TestWirelessClient,
    'H': testcase_ipfilter.TestIPFilter,
    'I': testcase_macfilter.TestMACFilter,
    'J': testcase_urlfilter.TestURLFilter,
    'K': testcase_portforward.TestPortForward,
    'L': testcase_dmzsettings.TestDMZSettings,
    'M': testcase_systemupgrade.TestSystemUpgrade,
    'N': testcase_configupdate.TestConfigUpdate,
    'O': testcase_rebootsystem.TestRebootSystem,
    }

#制定testcase文件夹路径
list = './testcase'
#构造测试集
def creatsuite1(all_cases):
    testunit = unittest.TestSuite()
    #将测试用例加入到测试容器中
    for case in all_cases:
        print (case)
        testunit.addTest(unittest.makeSuite(dicts[dicts1[case]]))
    print (testunit)
    return testunit

def _format_addr(s):
    name,addr = parseaddr(s)
    return formataddr((
        Header(name,'utf-8').encode(),
               addr.encode('utf-8').decode('utf-8')
               if isinstance(addr,str) else addr))


#描述：已附件的格式群发邮件，只限foxmail邮箱
#输入：fp-测试报告地址，sender-发送者邮箱仅限foxmail
def send(fp, log_name):
    #发送主题
    subject = '%s_%s_RegressionTest_AutoTestReport%s'%(AP_name,d['new_version'],hostname)
    #发送邮箱服务器
    smtpserver = "smtp.qiye.163.com"

    #发件邮箱用户和密码
    username = sender[0]
    password = sender[1]

    #获取测试报告
    f = open(fp,'rb')
    mail_body = f.read()
    f.close()

   #中文需参数'utf-8'，单字节字符不需要
    header = MIMEText('Dear all:\n\
    %s_%s RegressionTest的自动化测试完毕，请查看测试报告！\n\
    如果出现Fail的测试用例,可以到服务器http://%s/log/下载log文件：%s，谢谢！\n\n测试执行人：%s'
                      %(AP_name,d['new_version'],d['scp_server'],log_name,test_executor),\
                       'plain','utf-8') #中文需参数‘utf-8'，单字节字符不需要

    header = header


    #附件传送
    msgroot = MIMEMultipart('related')
    #添加发件人
    #msgroot['From'] = _format_addr('The Automation Tester<%s>'%sender[0])
    msgroot['From'] = _format_addr('三旺自动化测试<%s>'%sender[0])
    #添加收件人,首先将收件人生生成邮件格式即：XXX<xx@grandstream.cn>
    to =[]
    for i in receiver:
       to.append(_format_addr(i))
    #群发收件人使用逗号链接
    strto = ','.join(to)

    msgroot['To'] = strto
    #添加主题
    msgroot['Subject'] = subject

    #构造附件--测试报告
    att = MIMEText(mail_body,'base64','utf-8')
    att["content-type"] = 'application/octet-stream'
    att["content-Disposition"] = 'attachment;filename=%s'%fp


    msgroot.attach(header)
    msgroot.attach(att)

    i = 0
    while (i<10):
        ping = subprocess.call("ping mail.3onedata.com -c 3",shell=True)
        if ping == 0 :
            #开启smtp链接，发送邮件
            smtp = smtplib.SMTP()
            smtp.connect(smtpserver)
            smtp.login(username,password)
            smtp.sendmail(sender[0],receiver,msgroot.as_string())
            smtp.quit()
            print ('email has send out!')
            break
        else:
            print ("DNS nslookup fail,reboot router and try again!")
            time.sleep(60)
            i = i + 1

#描述：本函数实现登录路由器后通过scp拷贝文件到linux主机上
#输入：filename-本地文件名(也可以是文件的路径)，user-登录名,ip-登录ip,
    # password-登录密码,dir-remote主机的文件路径(也可以远程主机的文件名)
#输出：无/home/test
def scp_to_remote(filename):
    try:
        scp_newkey = 'Are you sure you want to continue connecting (yes/no)?'
        # 为scp命令生成一个spawn类的子程序对象
        child = pexpect.spawn('scp %s %s@%s:%s'%(filename,d['scp_name'],d['scp_server'],d['scp_dir']))
        #列出期望出现的字符串，超时，'password',scp_newkey
        i = child.expect([pexpect.TIMEOUT,scp_newkey,'password: '])

        #如果匹配到了超时
        if i == 0:
            print ("scp登录时出现超时:")
            #打印出错信息
            print (child.before, child.after)
            return None

        #如果出现的字符串为ssh_newkey，即第一次登录，没有public key
        if i == 1:
           #输入'yes'
            child.sendline('yes')
            #列出期望出现的字符串，超时或'password:'
            i = child.expect([pexpect.TIMEOUT, 'password: '])
            #如果出现的字符串为pexpect.TIMEOUT超时
            if i == 0:
                print ('scp登录时出现超时:')
                #打印出错信息
                print (child.before, child.after)
                return None

        #如果匹配到了密码字符
        child.sendline(d['scp_pwd'])

        #列出输入密码后期望出现的字符串，'password',EOF，超时'
        i = child.expect(["(?i)password",pexpect.EOF,pexpect.TIMEOUT])
        #匹配到pexpect.EOF，
        if i == 0:
            print ('密码输入错误！')
        elif i == 1:
            print ('恭喜,scp上传文件成功！')
        else:
            print ('传输文件超时！')

    except Exception as e:
        print ("scp连接失败",str(e))
        pexpect.run("rm -rf ~/.ssh")

#打包log文件
def tar_log_core(now):
    #拷贝com口日志和syslog到./data/log
    basic_PATH = "~/PycharmProjects/IAP2312N-2T_regressiontest"
    com_PATH = os.path.join(basic_PATH, "data", "log", "com.log")
    subprocess.call('cp ~/minicom.log %s'%com_PATH,shell=True)
    #拷贝slave ap的syslog到./data/log
    #now = time.strftime('%Y%m%d%H%M',time.localtime(time.time()))
    #打包log文件
    log_PATH = os.path.join(basic_PATH, "data", "log")
    subprocess.call('tar -cvzf %s_%s_log_%s.tgz %s'%(AP_name,d['new_version'],now,log_PATH),shell=True)
    #上传到scp服务器
    scp_to_remote("%s_%s_log_%s.tgz"%(AP_name,d['new_version'],now))
    print ('tar and scp put log file successfully!')
    return "%s_%s_log_%s.tgz"%(AP_name,d['new_version'],now)

#测试机的准备工作
def ready_test():
    basic_PATH = "~/PycharmProjects/IAP2312N-2T_regressiontest"
    log_PATH = os.path.join(basic_PATH, "data", "log", "*.log")
    testresultdata_PATH = os.path.join(basic_PATH, "data", "testresultdata", "*.txt")
    tgz_PATH = os.path.join(basic_PATH, "*log*.tgz")

    subprocess.call('echo %s |sudo -S rm -rf ~/.ssh %s  \
    %s %s *log*.tgz *.file'%(d["PC_pwd"],log_PATH,testresultdata_PATH,tgz_PATH),shell=True)


#设置测试报告名字，并运行用例集
def run_testcase(alltestnames, case=None):
        now = time.strftime('%Y%m%d%H%M',time.localtime(time.time()))
        #先配置测试报告的名称
        #1.如果需要所有用例集一起生成一个报告
        if onebyone == 1:
            if int(loop_times) == 1:
                subject ='%s_%s_RegressionTest_AutoTestReport_'%(AP_name,d['new_version'])
            else:
                subject ='%s_%s_RegressionTest_AutoTestReport_%s_'%(AP_name,d['new_version'],(i+1))
        #2.如果需要每个用例集单独生成报告，然后再打包
        else:
            #首先取出测试用例集的名称
            onetestname = case[2:].strip("_").upper()
            if int(loop_times) == 1:
                subject ='%s_%s_%s_AutoTestReport_'%(AP_name,d['new_version'],onetestname)
            else:
                subject ='%s_%s_%s_AutoTestReport_%s_'%(AP_name,d['new_version'],onetestname,(i+1))
        #测试报告名字
        filename =subject+now+'.html'
        fp = open(filename, 'wb')
        Auto_version = '1.1.0'
        runner = HTMLTestRunner_py3_3onedata.HTMLTestRunner(
            stream=fp,
            description='The Result of TestCase Execution:',
            AP_Name=AP_name,
            AP_FW=d['new_version'],
            Tester=test_executor,
            Test_Bed=PC_name,
            Automation_Test_Version=Auto_version,
            verbosity=2)
        #执行测试用例
        runner.run(alltestnames)
        #关闭文件
        fp.close()
        return now,filename


if __name__ == '__main__':
    for i in range(int(loop_times)):
        #设置每个用例集是否需要逐个测试并发送邮件
        if onebyone == 1:
            #测试机的准备工作
            ready_test()
            alltestnames= creatsuite1(cases)
            now,filename = run_testcase(alltestnames)
            #打包log文件
            log_name = tar_log_core(now)
            #发送测试报告
            send(filename, log_name)
        else:
            #测试机的准备工作
            ready_test()
            for c in cases:
                testname= creatsuite1([c])
                run_testcase(testname, c)
            now = time.strftime('%Y%m%d%H%M',time.localtime(time.time()))
            #打包log文件
            log_name = tar_log_core(now)
            filename = "%s_%s_RegressionTest_AutoTestReport.tgz"%(AP_name, d['new_version'])
            #发送测试报告
            send(filename, log_name)



























