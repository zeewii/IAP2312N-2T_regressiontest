#coding=utf-8
#作者：曾祥卫
#时间：2019.09.17
#描述：ssh登录

import pexpect, subprocess, codecs
import datetime, time, os

dirname = os.path.dirname(os.path.dirname(__file__))
ssh_log_PATH = os.path.join(dirname, "data", "testresultdata", "ssh_log.txt")


class SSH:

    #自己SSH类的属性:host-远程登录主机名，pwd-密码
    def __init__(self, host, pwd):
        self.host = host
        self.pwd = pwd

    #描述:首先使用 ssh host -l user  cmd登录ssh,在确定是否是首次登录，再输出结果
    #输入：user-登录用户名,cmd-命令
    #输出:命令返回的结果，同时将结果存放在同目录的log.txt文件中
    def ssh_cmd(self, user, cmd):
        """
        首先使用 ssh host -l user  cmd登录ssh,在确定是否是首次登录，再输出结果
        """
        try:
            # #删除先前的ssh的key
            subprocess.call("rm -rf ~/.ssh",shell=True)
            #远程主机输入后出现的字符串
            ssh_newkey = "Are you sure you want to continue connecting (yes/no)?"
            # 为 ssh 命令生成一个 spawn 类的子程序对象.
            child = pexpect.spawn('ssh %s -l %s %s'%(self.host, user, cmd), timeout=8)
            i = child.expect([pexpect.TIMEOUT, ssh_newkey, 'password: '])
            # 如果登录超时，打印出错信息，并退出.
            if i == 0:
                print("错误，ssh 登录超时:")
                print(child.before, child.after)
                return None
            # 如果 ssh 没有 public key，接受它.
            if i == 1: # ssh does not have the public key. Just accept it.
                child.sendline ('yes')
                i = child.expect([pexpect.TIMEOUT, 'password: '])
                if i == 0:
                    print("错误，ssh 登录超时:")
                    print(child.before, child.after)
                    return None
            # 输入密码.
            child.sendline(self.pwd)

            # 列出输入密码后期望出现的字符串，'password',EOF，超时
            i = child.expect(['password: ', pexpect.EOF, pexpect.TIMEOUT])
            # 匹配到字符'password: '，打印密码错误
            if i == 0:
                print(u'用户名密码输入错误！')
            # 匹配到了EOF，打印ssh登录成功，并输入命令后成功退出
            elif i == 1:
                print(u'恭喜,ssh登录输入%s命令成功！' %cmd)
            # 匹配到了超时，打印超时
            else:
                print(u'输入命令后等待超时！')

            # 将执行命令的时间和结果以追加的形式保存到log.txt文件中备份文件
            f = codecs.open(ssh_log_PATH, 'a',encoding='utf-8')
            str1 = str(datetime.datetime.now()) + ' command:' + cmd
            f.writelines(str1 + child.before.decode('utf-8'))
            f.close()

            result = child.before.decode('utf-8')
            print (result)
            return result
        except Exception as e:
            print("ssh连接失败，正在重启进程")
            result2 = subprocess.call("rm -rf ~/.ssh", shell=True)
            print (result2)

            time.sleep(10)
            print("delete ssh")
            print (e)


    def ssh_pc_cmd(self, user, cmd):
        """ssh登录PC，输入命令，并返回结果"""
        try:
            #远程主机登录后出现的字符串
            finish = "[#$>] "
            #远程主机输入后出现的字符串
            ssh_newkey = "Are you sure you want to continue connecting (yes/no)?"
            # 为ssh命令生成一个spawn类的子程序对象
            child = pexpect.spawn("ssh %s@%s"%(user, self.host), timeout=8)
            #列出期望出现的字符串，'password',EOF,超时
            i = child.expect([ssh_newkey, "(?i)password: ", pexpect.TIMEOUT])

            #如果匹配EOF,超时,打印信息并退出
            if i == 2:
                print("ssh登录失败，由于输入密码时超时")
                print(child.before, child.after)
                #强制退出
                child.close(force=True)
            if i == 0:
                child.sendline ('yes')
                i = child.expect([pexpect.TIMEOUT, 'password: '])
                if i == 0:
                    print("ssh登录失败，由于输入密码时超时")
                    print(child.before, child.after)
                    return None

            #匹配到了password，输入password
            child.sendline(self.pwd)
            #期待远程主机的命令提示符出现
            child.expect(finish)
            child.sendline(cmd)
            child.expect(finish)
            time.sleep(5)
            print(u'恭喜,ssh登录pc输入%s命令成功！' %cmd)
            result = child.before.decode('utf-8')
            print(result)
            #退出telent子程序
            child.close(force=True)
            return result
        #异常打印原因
        except pexpect as e:
            print("ssh连接失败，正在重启进程")
            result2 = subprocess.call("rm -rf ~/.ssh", shell=True)
            print (result2)
            time.sleep(5)
            print("delete ssh")
            print (e)

# ssh_pc_cmd("192.168.5.250", "test","test","wget http://192.168.5.100/test_http")
# ssh_pc_cmd("192.168.5.250", "test","test","md5sum test_http")
# ssh_pc_cmd("192.168.5.250", "test","test","rm -rf test_http")