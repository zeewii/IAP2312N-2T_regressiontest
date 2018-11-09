#coding=utf-8
#描述:本模块用来调用数据，方便测试用例来调用
#作者：曾祥卫
#时间：2018.09.17

import csv
import xlrd,xlwt
from xlutils.copy import copy
import os
dirname = os.path.dirname(__file__)
PATH = os.path.join(dirname, "data.xlsx")
#PATH = './data/data.xlsx'






def data_basic():
    """
    描述：读取data目录下/data/data.xlsx-basic_conf
    输入：None
    输出：以字典的形式输出basic中数据
    """
    try:
        #定义一个字典
        basic = {}
        #打开文件的工作空间
        xlsFile = xlrd.open_workbook(PATH)
        #获取对应的表-basic_conf
        table = xlsFile.sheet_by_name('basic_conf')
        #获取AP的管理ip
        basic['DUT_ip'] = table.cell_value(2,1)
        #获取AP的管理web
        basic['DUT_web'] = "http://{}".format(basic['DUT_ip'])
        #获取AP的eth1的mac地址
        basic['ap_brlan_mac'] = table.cell_value(2,2)
        #获取AP的wlan0的mac地址
        basic['ap_wlan0_mac'] = table.cell_value(2,3)
        #获取管理员用户名
        basic['superUser'] = table.cell_value(3,1)
        #管理员默认密码
        basic['super_defalut_pwd'] = table.cell_value(4,1)
        #一般用户名
        basic['user'] = table.cell_value(5,1)
        #测试ap的ssh用户名
        basic['ssh_user'] = table.cell_value(7,1)
        #测试ap的ssh密码
        basic['ssh_pwd'] = table.cell_value(7,2)
        #测试主机IP
        basic['PC_ip'] = table.cell_value(8,1)
        #测试主机IP
        basic['static_PC_ip'] = table.cell_value(8,2)
        #测试主机密码
        basic['PC_pwd'] = table.cell_value(9,1)
        #测试主机无线网卡接口名
        basic['wlan_pc'] = table.cell_value(10,1)
        #测试主机有线网卡接口名
        basic['lan_pc'] = table.cell_value(11,1)
        #测试ap新版本号
        basic['new_version']= table.cell_value(12,1)
        #测试ap旧版本号
        basic['old_version']= table.cell_value(12,2)
        #测试ap新版本的链接地址
        basic['new_version_http']= table.cell_value(13,1)
        #测试ap旧版本的链接地址
        basic['old_version_http']= table.cell_value(13,2)

        #com口log和用例集log存放的scp地址
        basic['scp_server'] = table.cell_value(14,1)
        #syslog，com口log和core file存放的ftp路径
        basic['scp_dir'] = table.cell_value(14,2)
        #syslog，com口log和core file存放的ftp的用户名
        basic['scp_name'] = table.cell_value(14,3)
        #syslog，com口log和core file存放的ftp的密码
        basic['scp_pwd'] = table.cell_value(14,4)

        #运行iperf3服务器的ip
        basic['iperf_ip'] = table.cell_value(15,1)

        # #radius服务器的地址
        # basic['radius_addr'] = table.cell_value(15,1)
        # #radius服务器的密钥
        # basic['radius_secrect'] = table.cell_value(15,2)
        # #radius服务器的用户名
        # basic['radius_usename'] = table.cell_value(15,3)
        # #radius服务器的密码
        # basic['radius_password'] = table.cell_value(15,4)
        # #radius服务器中带VID的用户名
        # basic['radius_VID_usename'] = table.cell_value(16,1)
        # #radius服务器中带VID的密码
        # basic['radius_VID_password'] = table.cell_value(16,2)
        # #http服务器新固件地址
        # basic['http_new_addr'] = table.cell_value(17,1)
        # #http服务器旧固件地址
        # basic['http_old_addr'] = table.cell_value(17,2)
        # #https服务器新固件地址
        # basic['https_new_addr'] = table.cell_value(18,1)
        # #https服务器旧固件地址
        # basic['https_old_addr'] = table.cell_value(18,2)
        # #tftp服务器新固件地址
        # basic['tftp_new_addr'] = table.cell_value(19,1)
        # #tftp服务器旧固件地址
        # basic['tftp_old_addr'] = table.cell_value(19,2)
        # #iperf服务器地址
        # basic['iperf_ip'] = table.cell_value(20,1)
        #

        # #给无线网卡设置的固定ip
        # basic['client_ip'] = table.cell_value(22,1)
        # #子网掩码
        # basic['mask'] = table.cell_value(23,1)
        # #ntp服务
        # basic['ntp'] = table.cell_value(24,1)

        #######################################
        # #测试专用的firefox的profile路径
        # basic['firefox_profile'] = table.cell_value(36,1)
        return basic
    except IOError as e:
        print("文件信息错误,具体信息：\n%s"%e)


def data_login():
    """
    描述：读取data目录下/data/data.xlsx-login_conf
    输入：None
    输出：以字典的形式输出login中数据
    """
    try:
        #定义一个字典
        data = {}
        #打开文件的工作空间
        xlsFile = xlrd.open_workbook(PATH)
        #获取对应的表-login_conf
        table = xlsFile.sheet_by_name('login_conf')
        #获取数字密码
        data['digital_pwd'] = table.cell_value(2,1)
        #获取字母密码
        data['letter_pwd'] = table.cell_value(3,1)
        #获取asii密码
        data['asii_pwd'] = table.cell_value(4,1)
        #数字字母混合
        data['digital_letter'] = table.cell_value(5,1)
        #数字和ASII码混合
        data['digital_asii'] = table.cell_value(6,1)
        #字母和ASII码混合
        data['letter_asii'] = table.cell_value(7,1)
        #数字字母asii混合
        data['all'] = table.cell_value(8,1)
        #空
        data['blank'] = table.cell_value(20,1)
        #中文
        data['chineses'] = table.cell_value(21,1)
        return data
    except IOError as e:
        print("文件信息错误,具体信息：\n%s"%e)

def data_lan():
    """
    描述：读取data目录下/data/data.xlsx-lan_conf
    输入：None
    输出：以字典的形式输出lan中数据
    """
    try:
        #定义一个字典
        data = {}
        #打开文件的工作空间
        xlsFile = xlrd.open_workbook(PATH)
        #获取对应的表-lan_conf
        table = xlsFile.sheet_by_name('lan_conf')
        #获取静态ip地址1
        data['ap_test_IP1'] = table.cell_value(2,1)
        #获取静态ip地址2
        data['ap_test_IP2'] = table.cell_value(2,2)
        #获取静态ip地址3
        data['ap_test_IP3'] = table.cell_value(2,3)
        #获取子网掩码1
        data['netmask1'] = table.cell_value(3,1)
        #获取子网掩码2
        data['netmask2'] = table.cell_value(3,2)
        #获取子网掩码3
        data['netmask3'] = table.cell_value(3,3)
        #获取自定义子网掩码1
        data['custom_netmask1'] = table.cell_value(4,1)
        #获取自定义子网掩码2
        data['custom_netmask2'] = table.cell_value(4,2)
        #获取自定义子网掩码3
        data['custom_netmask3'] = table.cell_value(4,3)

        return data
    except IOError as e:
        print("文件信息错误,具体信息：\n%s"%e)

def data_wan():
    """
    描述：读取data目录下/data/data.xlsx-wan_conf
    输入：None
    输出：以字典的形式输出wan中数据
    """
    try:
        #定义一个字典
        data = {}
        #打开文件的工作空间
        xlsFile = xlrd.open_workbook(PATH)
        #获取对应的表-wan_conf
        table = xlsFile.sheet_by_name('wan_conf')
        #获取静态ip地址
        data['static_IP'] = table.cell_value(2,1)
        #获取wan口IP的字符串
        data['wan_str'] = table.cell_value(2,2)
        #获取子网掩码
        data['netmask'] = table.cell_value(3,1)
        #获取网关地址
        data['gateway'] = table.cell_value(4,1)
        #获取DNS
        data['DNS'] = table.cell_value(5,1)
        #获取pppoe的用户名
        data['pppoe_user'] = table.cell_value(6,1)
        #获取pppoe的密码
        data['pppoe_password'] = table.cell_value(6,2)

        return data
    except IOError as e:
        print("文件信息错误,具体信息：\n%s"%e)



def data_wireless():
    """
    描述：读取data目录下/data/data.xlsx-wireless_conf
    输入：None
    输出：以字典的形式输出wireless中数据
    """
    try:
        #定义一个字典
        data = {}
        #打开文件的工作空间
        xlsFile = xlrd.open_workbook(PATH)
        #获取对应的表-wireless_conf
        table = xlsFile.sheet_by_name('Wireless_conf')
        #获取全数字ssid
        data['digital_ssid'] = table.cell_value(2,1)
        #获取字母ssid
        data['letter_ssid'] = table.cell_value(3,1)
        #data['letter_ssid'] = data['letter_ssid_part']+master_last_6mac()
        #数字字母asii混合
        data['all_ssid_part'] = table.cell_value(4,1)
        data['all_ssid'] = data['all_ssid_part']+master_last_6mac()
        #额外ssid-数字字母asii混合
        data['add_ssid_part'] = table.cell_value(4,2)
        data['add_ssid'] = data['add_ssid_part']+master_last_6mac()
        #ASCII码
        data['ascii_ssid'] = table.cell_value(5,1)
        #数字和字母混合
        data['digital_letter_ssid'] = table.cell_value(6,1)
        #最短ssid
        data['short_ssid'] = table.cell_value(7,1)
        #最长ssid
        data['long_ssid'] = table.cell_value(8,1)
        #中文SSID
        data['CN_ssid'] = table.cell_value(9,1)
        #wep64加密
        data['wep64'] = table.cell_value(10,1)
        #wep64加密-10
        data['wep64-10'] = table.cell_value(10,2)
        #wep128加密
        data['wep128'] = table.cell_value(11,1)
        #wep128加密-26
        data['wep128-26'] = table.cell_value(11,2)
        #异常wep密码1
        data['abnormal1_wep'] = table.cell_value(10,3)
        #异常wep密码2
        data['abnormal2_wep'] = table.cell_value(11,3)
        #wpa最短加密
        data['short_wpa'] = table.cell_value(12,1)
        #wpa各种字符串密码
        data['all_wpa'] = table.cell_value(12,2)
        #错误的WPA密码
        #data['error_wpa'] = table.cell_value(12,3)
        #wpa最长加密
        data['long_wpa'] = table.cell_value(13,1)
        #特殊符号SSID
        data['special_ssid'] = table.cell_value(14,1)
        #radius服务器的用户名，密码，key
        data['radius_usename'] = table.cell_value(15,1)
        data['radius_password'] = table.cell_value(15,2)
        data['radius_key'] = table.cell_value(15,2)
        #桥接的essid, bssid，加密方式，密码
        data['bridge_essid'] = table.cell_value(16,1)
        data['bridge_bssid'] = table.cell_value(16,2)
        data['bridge_encryption'] = table.cell_value(16,3)
        data['bridge_pwd'] = table.cell_value(16,4)
        data['bridge_ip'] = table.cell_value(16,5)
        #PC需要访问桥接的无线路由所指定的静态IP地址
        data['bridge_static_ip'] = table.cell_value(16,6)

        #客户端限制数量输入字母
        data['limit_letter'] = table.cell_value(17,1)
        #客户端限制数量输入特殊符号
        data['limit_ascii'] = table.cell_value(18,1)
        #客户端限制数量上限值
        data['limit_max'] = table.cell_value(19,1)
        #客户端限制数量下限值
        data['limit_min'] = table.cell_value(20,1)
        #客户端限制数量大于上限值
        data['limit_more_max'] = table.cell_value(21,1)
        #客户端限制数量小于下限值
        data['limit_less_min'] = table.cell_value(22,1)
        #客户端限制数量
        data['client_limit'] = table.cell_value(23,1)
        #客户端数量限制测试值
        data['client_limit_test'] = table.cell_value(24,1)
        return data
    except IOError as e:
        print("文件信息错误,具体信息：\n%s"%e)

def master_last_6mac():
    """
    取得ap的无线的mac地址的后6位mac地址
    """
    basic = data_basic()
    master_ap = basic['ap_wlan0_mac']
    #小写转换为大写
    Master_ap = master_ap.upper()
    #按：号分成列表
    tmp1 = Master_ap.split(":")
    #取第4个元素到最后一个元素
    tmp2 = tmp1[3:]
    #组合成字符串
    tmp3 = ''.join(tmp2)
    return tmp3

#设置excel表的单元格样式
#输入：bold:是否粗写
def set_style(bold=False):
    style = xlwt.XFStyle() # 初始化样式
    font = xlwt.Font() # 为样式创建字体
    font.name = 'Times New Roman' # 'Times New Roman'
    font.bold = bold
    font.color_index = 4
    font.height = 220
    style.font = font
    return style

#创建excel
#输入：excel_name:excel表格名称;row_m:第m次要输入的结果（为列表）
def create_excel(excel_name,row0):
    #创建工作簿
    f = xlwt.Workbook()
    #创建sheet1
    sheet1 = f.add_sheet('sheet1',cell_overwrite_ok=True)
    #生成第一行
    for i in range(len(row0)):
        sheet1.write(0,i,row0[i],set_style(True))
    # row0 = [u'次数',u'配对',u'解除配对']
    f.save('%s.xls'%excel_name) #保存文件
    print ("create excel successfully!")

#创建一个空的excel
#创建excel
#输入：excel_name:excel表格名称;
def create_excel_black(excel_name,sheet_name):
    #创建工作簿
    f = xlwt.Workbook()
    #创建sheet1
    sheet1 = f.add_sheet(sheet_name,cell_overwrite_ok=True)
    f.save('%s.xls'%excel_name) #保存文件
    print ("create excel successfully!")


#追加写excel-增加一行
#输入：excel_name:excel表格名称;row_m:第m次要输入的结果（为列表）
def add_excel_row(excel_name,row_m):
    #用xlrd提供的方法打开文件的工作空间
    f = xlrd.open_workbook('%s.xls'%excel_name)
    #用xlrd提供的方法获得现在已有的行数
    rows = f.sheets()[0].nrows
    #用xlutils提供的copy方法将xlrd的对象转化为xlwt的对象
    excel = copy(f)
    #用xlwt对象的方法获得要操作的sheet
    table = excel.get_sheet(0)
    #生成第m行
    table.write(rows,0,rows,set_style())
    for i in range(len(row_m)):
        table.write(rows,i,row_m[i],set_style())

    excel.save('%s.xls'%excel_name) #保存文件
    print ("add to write excel successfully!")

#追加写excel-增加一行,并将前面加一个空行
#输入：excel_name:excel表格名称;row_m:第m次要输入的结果（为列表）
def add_excel_row_add(excel_name,row_m):
    #用xlrd提供的方法打开文件的工作空间
    f = xlrd.open_workbook('%s.xls'%excel_name)
    #用xlrd提供的方法获得现在已有的行数
    row = f.sheets()[0].nrows
    rows = row+1
    #用xlutils提供的copy方法将xlrd的对象转化为xlwt的对象
    excel = copy(f)
    #用xlwt对象的方法获得要操作的sheet
    table = excel.get_sheet(0)
    #生成第m行
    table.write(rows,0,rows,set_style())
    for i in range(len(row_m)):
        table.write(rows,i,row_m[i],set_style())

    excel.save('%s.xls'%excel_name) #保存文件
    print ("add to write excel successfully!")

#追加写excel-增加一行,并将前面加一个空行
#输入：excel_name:excel表格名称;row_m:第m次要输入的结果（为列表）
def add_excel_row_add_backup(excel_name,row_m):
    #用xlrd提供的方法打开文件的工作空间
    f = xlrd.open_workbook('%s.xls'%excel_name)
    #用xlrd提供的方法获得现在已有的行数
    rows = f.sheets()[0].nrows
    #用xlutils提供的copy方法将xlrd的对象转化为xlwt的对象
    excel = copy(f)
    #用xlwt对象的方法获得要操作的sheet
    table = excel.get_sheet(0)
    #生成第m行
    table.write(rows,0,rows,set_style())
    for i in range(len(row_m)):
        table.write(rows,i,row_m[i],set_style())

    excel.save('%s.xls'%excel_name) #保存文件
    print ("add to write excel successfully!")

#追加写excel-增加某个坐标的内容
#输入：excel_name:excel表格名称;row_n:写入第几行;column_n:写入第几列;content:写入的内容(字符串)
def add_excel_content(excel_name,row_n,column_n,content):
    #用xlrd提供的方法打开文件的工作空间
    f = xlrd.open_workbook('%s.xls'%excel_name)
    #用xlutils提供的copy方法将xlrd的对象转化为xlwt的对象
    excel = copy(f)
    #用xlwt对象的方法获得要操作的sheet
    table = excel.get_sheet(0)
    #生成第n行
    table.write(row_n,column_n,content,set_style())
    excel.save('%s.xls'%excel_name) #保存文件
    print ("add to write excel successfully!")

def csv_to_xlsx(csv_name,sheet_name):
    with open(csv_name,'r') as f:
        read = csv.reader(f)
        work = xlwt.Workbook()
        sheet = work.add_sheet(sheet_name)
        l=0
        for line in read:
            print(line)
            r =0
            for i in line:
                print(i)
                sheet.write(l,r,i)#一个一个将单元格数据写入
                r = r+1
            l = l+1
        work.save('./data/tmp.xls')

def csv_to_xlsx_back1(i,sheet_name):
    with open('～/tftp/csv/memdatadigital%s.csv'%i,'r') as f:
        read = csv.reader(f)
        work = xlwt.Workbook()
        sheet = work.add_sheet(sheet_name)
        l=0
        for line in read:
            print(line)
            r =0
            for i in line:
                print(i)
                sheet.write(l,r,i)#一个一个将单元格数据写入
                r = r+1
            l = l+1
        work.save('./data/tmp.xls')

def csv_to_xlsx_back2(csv_name,sheet_name):
    with open('～/tftp/csv/memdataletter%s.csv'%csv_name,'r') as f:
        read = csv.reader(f)
        work = xlwt.Workbook()
        sheet = work.add_sheet(sheet_name)
        l=0
        for line in read:
            print(line)
            r =0
            for i in line:
                print(i)
                sheet.write(l,r,i)#一个一个将单元格数据写入
                r = r+1
            l = l+1
        work.save('./data/tmp.xls')

#从excel中读取一行数据，这里的path写绝对路径
def read_excel_content(excel_name,sheet_name):
    #用xlrd提供的方法打开文件的工作空间
    f = xlrd.open_workbook('%s.xls'%excel_name)
    #获取对应的表-basic_conf
    table = f.sheet_by_name(sheet_name)
    print (sheet_name)
    print (table)
    print (table.nrows)
    result = table.row_values(0)
    print (result)
    return result

#从excel中读取一行数据，这里的path写绝对路径
def read_excel_content_add(excel_name,sheet_name):
    #用xlrd提供的方法打开文件的工作空间
    f = xlrd.open_workbook('%s.xls'%excel_name)
    #获取对应的表-basic_conf
    table = f.sheet_by_name(sheet_name)
    result = table.row_values(1)
    return result

#从excel中读取一行数据，这里的path写绝对路径
def read_excel_content_add2(excel_name,sheet_name):
    #用xlrd提供的方法打开文件的工作空间
    f = xlrd.open_workbook('%s.xls'%excel_name)
    #获取对应的表-basic_conf
    table = f.sheet_by_name(sheet_name)
    result = table.row_values(2)
    return result







