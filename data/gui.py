#coding=utf-8
#作者：曾祥卫
#描述：执行测试用例前的准备工作
#时间：2018.09.17

import sys,time,subprocess, easygui
import os
#from data import easygui
dirname = os.path.dirname(__file__)
PATH_map = os.path.join(dirname, "topological_map.gif")
PATH_data = os.path.join(dirname, "data.xlsx")

#开始欢迎确认框
def welcome():
    msg1="请先把DUT，测试PC，服务器按以下拓扑图连接好.\n桥接的AP和DUT设为不同的网段,并修改无线加密为wpa2."
    msg2='请确定data.xlsx的数据是否正确'
    msg3='即将要开始AP的自动化测试\n\n'\
         '1.请将AP的串口接入到该测试机中，安装minicom(或securecrt)，并保存串口打印信息为/home/test/minicom.log。\n\n'\
         '2.请在该测试PC的http服务器的根路径下上传一个文件，文件名为test_http。\n\n'\
         '3.请先将三旺的AP恢复出厂设置。'
    title = '欢迎进行三旺AP的自动化测试'
    image= PATH_map
    choice=["正确并继续","点击该按钮先去设置"]
    #欢迎页面拓扑图
    easygui.msgbox(msg3,title)
    easygui.msgbox(msg1,title,image=image)
    #欢迎页面确定data.xlsx数据正确
    welcome = easygui.ccbox(msg2,title,choices=choice)
    #点击"先去设置"，打开data.xlsx
    if welcome == 0:
        subprocess.call("xdg-open %s"%PATH_data, shell=True)
        print("退出自动化测试")
        sys.exit(0)



#选择测试用例框
def choice_case():
    case = []
    msg="请先选择需要执行的测试用例集"
    title="选择用例集"
    choices=['A_login',
             'B_stateinfo',
             'C_workmode',
             'D_lansettings',
             'E_wansettings',
             'F_wirelesssettings',
             'G_wirelessclient',
             'H_ipfilter',
             'I_macfilter',
             'J_urlfilter',
             'K_portforward',
             'L_dmzsettings',
             'M_systemupgrade',
             'N_configupdate',
             'O_rebootsystem',
             ]

    while True:
        #测试用例选择框
        case=easygui.multchoicebox(msg,title,choices)
        #点击取消退出测试
        if case == None :
            print("退出自动化测试")
            sys.exit(0)
        #不选择任何一个用例，提示
        elif len(case) ==0:
            easygui.msgbox("你没有选择任何一个测试用例集，请必须选择一个！","错误")
            continue
        else:
            msg1 = ""
            for i in range(len(case)):
                msg1 += ('%s\n'%case[i])
            #显示所选择的测试用例，并再次确认
            confirm_again=easygui.ccbox(msg=msg1,title="请确认所需测试集的用例是否正确：",
                                        choices=("正确并继续","再去选择"))
            #点击再去选择，重新选择用例
            if confirm_again == 0:
                continue
            break
    return case




#输入发送测试报告的email地址和密码
def send_email():
    send_email = []
    msg='请输入你的eamil地址和密码'
    title="你的email"
    field = ["*email地址", "*密码"]
    values_self = ["zxw-920@3onedata.com"]
    while True:
        #输入用户名和密码框，密码为不显示明文
        send_email=easygui.multpasswordbox(msg, title,field,values_self)
        #点击取消退出测试
        if send_email == None :
            print ("退出自动化测试")
            sys.exit(0)
        #地址和密码都不输入，提示
        elif send_email == ["",""]:
            easygui.msgbox("你必须输入email地址和密码！","错误")
            continue
        #地址为空，提示
        elif send_email[0].strip()=="":
            easygui.msgbox("你必须输入email地址！","错误")
            continue
        #密码为空，提示
        elif send_email[1].strip()=="":
            easygui.msgbox("你必须输入密码！","错误")
        else:
            break
    return send_email


#输入接收测试报告的email地址
def receive_email():
    receive_email = []
    msg="至少必须输入一个emai地址，多个email地址用逗号隔开"
    title="接收测试报告的email地址"
    fields=["email地址1","email地址2","email地址3","email地址4","email地址5","email地址6","email地址7","email地址8"]
    values_self = ["zxw-920@3onedata.com"]
    while True:
        #email地址输入框
        receive_email=easygui.multenterbox(msg,title,fields,values_self)
        #点击取消退出测试
        if receive_email == None:
            print ("退出自动化测试")
            sys.exit(0)
        msg1 =""
        for i in range(len(fields)):
            msg1 +=(receive_email[i])
        #一个地址都不输入，提示
        if msg1 == '':
            easygui.msgbox("请至少必须输入一个emai地址！","错误")
            continue
        else:
            break
    return receive_email

#设置用例执行的次数
def loop_times():
    loop = easygui.ccbox('是否需要循环多次执行？','循环执行测试',choices=['否','是'])
    if loop == 0:
        times = easygui.enterbox(msg='格式如：5',title='请输入循环执行的次数')
        print ("Run loop times is %s"%times)
        return times
    return loop

#设置自动化执行人
def test_executor():
    while True:
        test_executor = easygui.enterbox(msg='中文英文皆可',title='请输入自动化执行人姓名')
        if (test_executor == "") or (test_executor == None):
            easygui.msgbox('必须要输入自动化执行人姓名才能继续开始测试','请输入自动化执行人姓名')
            continue
        else:
            return test_executor


#设置开始时间
def start_time():
    YN = easygui.ccbox('是否立刻开始测试？','开始测试',choices=['是','设置开始时间'])
    if YN == 0:
        start_time = easygui.enterbox(msg='格式如：18:30',title='请输入自动化测试开始的时间')
        timing=time.strftime('%H:%M',time.localtime(time.time()))
        print ("目前时间是：%s\n开始测试时间是：%s"%(timing,start_time))
        #是否需要从Internet上下载固件后，然后再进行测试
        #########控制什么时间脚本执行######
        while True:
            timing=time.strftime('%H:%M',time.localtime(time.time()))
            if timing != start_time:
                time.sleep(30)
                print ("目前时间是：%s，请等待..."%timing)
            else:
                print ("开始执行自动化测试！")
                break

#是选择定时开始测试，还是选择需要检查Internet上有固件后才进行测试
def choose_timing_or_download_FW():
    download = easygui.ccbox('是否需要检查Internet上有固件后才进行测试？','检查并下载固件',choices=['否','是'])
    if download == 0:
        web_address = easygui.enterbox(msg='格式如：http://...',\
                                       title='请输入固件的网站地址')
        easygui.msgbox('点击OK开始测试','即将开始测试')
        while True:
            #首先删除先前的固件
            subprocess.call("rm -rf ~/FW/7610_FW/new/*",shell=True)
            result = subprocess.call("wget --http-user=guest --http-passwd=grandstream -O fw.bin %s"%web_address,shell=True)
            if result == 0:
                print ("Download FW successful!\nStart running auto test...")
                break
            else:
                print ("Download FW failed! Wait 20mins and go on...")
                time.sleep(1200)
    else:
        easygui.msgbox('点击OK去设置开始的时间','即将开始测试')
        start_time()



#设置每个用例集是否需要逐个测试并发送邮件
#输出：1：不需要;0：需要
def testcase_onebyone():
    msg='是否需要逐个测试并生成单独的测试报告'
    title='请确定每个用例集是否需要逐个测试并生成单独的测试报告'
    choice=["不需要","需要"]
    onebyone = easygui.ccbox(msg,title,choices=choice)
    return onebyone


__author__ = 'zeng'

