# -*- coding=utf-8 -*-
import linecache
import sys,os
from flask import Flask, render_template
from flask import request
from ldap3 import Server, Connection

from get_servername import get_servername
from search_servername import search_servername

import ngx_check

reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__,static_url_path='')
path='conf'


@app.route('/list',methods=['GET', 'POST'])
def list():
    gs = get_servername("conf/nginx.conf")
    I = gs.IncludeFileList()
    LD,LU=gs.GetDomainandUpsteam()
    return render_template('list.html',servernames=LD,upsteamnames=LU)

@app.route('/show',methods=['GET', 'POST'])
def show():
    if request.args.get('file'):
        file=request.args.get('file')
    else:
        return 'Worng agres'
    if request.args.get('name'):
        name=request.args.get('name')
    else:
        return 'Worng agres'
    if request.args.get('type'):
        type=request.args.get('type')
    else:
        return 'Worng agres'
    file=os.path.join(path,file)

    ss = search_servername (name,file,type)             #文件路径有修改，根据部署环境不同，这部分可能会有变化。会带到下一个页面
    ss.get_num ( )
    ss.get_start ( )
    ss.get_end ( )
    result=''
    result=result.join(ss.get_result())#把整个list，整合成一个字符串。之前用轮询list的方式，出了很多多余的回车。

    return render_template('show.html',results=result,name=name,file=file)

@app.route('/edit',methods=['GET','POST'])
def edit():
    name=request.form.get('name')
    file=request.form.get('file')
    ngxconf=request.form.get('code')
    # 加入check
    ngxconf_str = ngxconf.encode('utf8').split('\n')                #将unicode转换为utf8,将得到的str按照换行分隔成list,方便后续处理
    '''
    l_count=0                                           #左{ 计数
    r_count=0                                           #右} 计数
    for i in ngxconf_str_list:                          #轮询list
        j=i.split('#')                                  #分隔注释
        l_count = l_count + j[0].count('{')             #计数左{
        r_count = r_count + j[0].count('}')             #计数右}
    if l_count != r_count:
        return '左右{}不匹配，严重错误'
    '''

    ss = search_servername (name,file)
    print id(ss)
    num = ss.get_num()              #没用到
    start = ss.get_start()
    end = ss.get_end()

    str = linecache.getlines(file)  #原文
    str_copy = str[:]         #创建一个副本。先将改动写入配置文件，如果nginx检查没问题，保留新配置；如果有问题，就用原始副本写回配置文件
    i = end
    while i>=start:                 #删除原有servername
        str.pop(i)                  #list的remove方法是针对值，list中可以有相同值，如果用remove会吧所有相同值都去掉。pop针对下标
        i=i-1
    for i in ngxconf_str:             #把上一个页面中的testare中的配置信息分段导入，之前出现了^M 换行符，解决方方式从右边切割，然后加一个换行符
        str.append(i.replace('\r','\n'))             #把编辑后的servername追加上
    f=open(file,'wb')               #写入文件
    print file
    for i in str:
        f.write(i)
    f.close()

    check = 'Ngx check Success :)'
    if check == 'Ngx check Success :)' :
        str = linecache.getlines (file)
        result = ''
        result = result.join (str)
        return render_template('result.html',results=result,file=file)
    else:
        f = open (file, 'wb')
        print file
        for i in str_copy:
            f.write (i)
        f.close ( )
        return check



app.run(host='0.0.0.0',port=8080)

'''
2018-06-27
'''

