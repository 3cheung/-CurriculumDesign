import os,stat
import sys
import re
import time
import datetime
import shutil
#coding:utf-8
#利用python生成一个随机10位的字符串
import string
import random
import glob
#随机名字
def randName():
    #name=''
    list = [chr(i) for i in range(65,91)] + [chr(i) for i in range(97,123)] + [ str(i) for i in range(10)] #大写字母+小写字母+数字

    num = random.sample(list,15)
    stra=''
    value = stra.join(num) #将取出的十个随机数进行重新合并
    #if not value[0].isdigit():
    #    name = value
    return value

'''获取当前用户的主目录路径'''
#print (os.environ['HOME'])
#print (os.path.expandvars('$HOME'))
#print (os.path.expanduser('~'))

#判断不是文件 不是返回True ,是返回False
def isNotfile(path):
    if(os.path.isfile(path)):
        return False
    else:
        return True
def owner(path):
    stat_info = os.stat(path)
    uid = stat_info.st_uid  # 拥有者
    return uid
#权限输出 rwx
def permission(mode):
    a = ''
    rwx=''
    for x in mode:
        x= int(x)
        if x==0:
            rwx='---'
        elif x==1:
            rwx='--x'
        elif x==2:
            rwx='-w-'
        elif x==3:
            rwx='-wx'
        elif x==4:
            rwx='r--'
        elif x==5:
            rwx='r-x'
        elif x==6:
            rwx='rw-'
        elif x==7:
            rwx='rwx'
        a=a+rwx
    return a
#切换路径
def cd(path):
    if(re.match('^~(\/(\w+\/?)+)?$', path)):
        print(path,end='  a')
        '''os.path.expanduser('~')'''
        path = path.replace('~',os.path.expanduser('~'))
        print("代替后：",path)
    if(re.match('(\\.\\.)|(^\/?(\w+\/?)+$)',path)):
        if(isNotfile(path)):
            if(os.path.exists(path)):
                os.chdir(path)
            else:
                print('-bash: cd: ',path," :No such file or directory")

        else:
            print(path+"不是目录")
    else:
        print('-bash: cd: ', path, " :No such file or directory")
#路径
def pwd():
    #os.path.abspath(path)
    #print(os.getcwd())#pwd
    return os.getcwd()
def pwdp():
    #os.path.abspath(path)
    print(os.getcwd())#pwd
#查看目录下的文件
def ls():
    i = 0
    for file_name in os.listdir("."):
        if not file_name.startswith('.'):
            i = i+1
            if (os.path.isfile(file_name)):
                print('\033[1;32;40m' + file_name + '\033[0m', end="   ")
            else:
                print('\033[1;34;40m' + file_name + '\033[0m', end="   ")
    if(i!=0):
        print()
#查看详细信息
def ll():
    request_path = '.'
    for item in os.listdir(request_path):
        full_path = os.path.join(request_path, item)
        fsize = os.path.getsize(full_path)#大小
        fmtime = os.path.getmtime(full_path)#修改时间
        stat_info = os.stat(item)
        uid = stat_info.st_uid #拥有者
        gid = stat_info.st_gid #组
        mode = oct(stat_info.st_mode)[-3:]#权限
        rwx = permission(mode)
        if not item.startswith('.'):
            if (os.path.isfile(full_path)):
                print(rwx+'{:>5}{:>5}'.format(str(uid if uid !=0 else 'root'),str(gid if gid !=0 else 'root'))+'{:>10}{:>0}'.format(str(fsize),'KB')+time.strftime(" %b %d %H:%M",  time.localtime(fmtime))+'\033[1;32;40m' + full_path + '\033[0m')
                #print({'name': item, 'fsize': str(fsize) + 'KB', 'fmtime': fmtime})
            else:
                print(rwx + '{:>5}{:>5}'.format(str(uid if uid !=0 else 'root'),str(gid if gid !=0 else 'root')) + '{:>10}{:>0}'.format(str(fsize), 'KB') + time.strftime(" %b %d %H:%M",time.localtime(fmtime)) + '\033[1;34;40m' + full_path + '\033[0m')
#新建目录
def mkdir(path):
    if(bool(1-os.path.exists(path))):
        os.mkdir(path)
    else:
        print('mkdir: cannot create directory \''+path+'\': File exists')
#删除目录
def rmdir(*args):
    '''
    删除文件夹实例：
        rm - rf / var / log / httpd / access
    删除文件使用实例：
        rm -f /var/log/httpd/access.log
    rm -f 删除目录时：（报错）
        rm: cannot remove ‘aaa.txt’: Is a directory
    type:
        -i 删除前逐一询问确认。
        -f 即使原档案属性设为唯读，亦直接删除，无需逐一确认。
        -r 将目录及以下之档案亦逐一删除。
    '''
    path=args[0]
    type=''
    if(len(args)==2):
        path = args[1]
        type = args[0]
    if (type == ''):
        if (os.path.isfile(path)):
            y = input('rm: remove regular empty file ' + path + '?')
            if (re.match("Y|y|yes|YES", y)):
                os.remove(path)
        else:
            print("rm: cannot remove '" + path + "':  Is a directory")
    if (type == '-f'):
        if (os.path.isfile(path)):
            os.remove(path)
        else:
            print("rm: cannot remove '" + path + "': Is a directory")
    if(type=='-r'):
        if (os.path.exists(path)):
            if (os.path.isdir(path)):
                y = input('rm: remove directory '+path+'?')
                if(re.match("Y|y|yes|YES",y)):
                    shutil.rmtree(path)
            if (os.path.isfile(path)):
                y = input('rm: remove regular empty file ' + path + '?')
                if (re.match("Y|y|yes|YES", y)):
                    os.remove(path)
        else:
            print("rm: cannot remove '"+path+"': No such file or directory")
    if (type == '-rf'):
        if (os.path.exists(path)):
            if (os.path.isdir(path)):
                shutil.rmtree(path)
            if (os.path.isfile(path)):
               os.remove(path)
        else:
            print("rm: cannot remove '" + path + "': Is a directory")
def touch(filename):
    try:
        file = open(filename,'a')
        print(file)
    finally:
        file.close()
def exit():
    sys.exit(0)
#修改名字
def rename(oldPath,newPath):
    if(os.path.exists(oldPath)):
        if (os.path.exists(newPath)):
            y = input('mv: overwrite ‘'+newPath+'’?')
            if (re.match("Y|y|yes|YES", y)):
                shutil.move(oldPath,newPath)
        else:
            shutil.move(oldPath, newPath)
    else:
        print("mv: cannot stat ‘"+oldPath+"’: No such file or directory")
#复制文件
def copy(source,destination):
    if(os.path.isdir(source)):
        shutil.copytree(source,destination)
    if(os.path.isfile(source)):
        shutil.copy(source,destination)
#在指定的目录及其子目录下查找指定文件
def finddirfile(dir,filename):
    if(os.path.exists(dir)):
        for path in glob.glob(dir+'/'+'*'+filename+'*'):
            print(os.path.abspath(path))
    else:
        print("rm: cannot remove '" + dir + "': Is a directory")
dic = {'cd':cd,'pwd':pwdp,'ls':ls,'ll':ll,'mkdir':mkdir,'rm':rmdir,'touch':touch,'exit':exit,'mv':rename,'cp':copy,'find':finddirfile}
name = randName() #随机生成name
while(1):
    own = owner('.')
    own =own if own!=0 else 'root'
    path = pwd().replace('/root','')
    path = path if path!='' else '~'
    path = path.replace('/', '')
    index = input('\033[31m['+str(own)+'@'+name+' '+path+']#\033[0m')
    command = index.split(' ')
    a = dic.get(command[0])
    if(a):
        if(len(command)==2):
            try:
                a(command[1])
            except BaseException as e:
                print(e)
                print("Try '"+command[0]+" --help' for more information.")
        elif(len(command)==3):
            try:
                a(command[1],command[2])
            except BaseException as e:
                print(e)
                print("Try '" + command[0] + " --help' for more information.")
        else:
            try:
                a()
            except SystemExit as e:
                if str(e) == '0':
                    break
            except BaseException as e:
                print(e)
                print("Try '" + command[0] + " --help' for more information.")
    else:
        print('-bash: '+command[0]+': command not found')