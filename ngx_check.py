# -*- coding: UTF-8 -*-
import os
import commands
#这个脚本的目的是测试ngx配置文件是否正确。

def ngx_check(ngx_path,ngx_conf):
    ngx_conf=os.path.join(os.getcwd(),ngx_conf)
    cmd0 = ngx_path + ' -t -c '+ngx_conf
    print cmd0
    (status0, output0) = commands.getstatusoutput(cmd0)

    if status0 == 0 :
        return 'Ngx check Success :)'
    else :
        return output0
