#coding=utf-8
import linecache
import re

class search_servername:

    def __init__(self,servername='peixun.abc.com', file='example.conf',type='server'):
        self.servername = servername.replace('*','\*') #少量域名有*号。*号在正则中有特殊意义，做转义替换来处理；一些其他符号比如+/还没处理
        self.type=type                                          #server 或者 upstream
#        print self.type
        if self.type=='server':
            self.regstr = '\s*server_name.*'+ '\s' + self.servername + '\s*'#0到多个空格 server_name 任意字符 至少一个空格 域名 0到多个空格
        elif self.type=='upstream':
            self.regstr = '\s*upstream.*' + '\s' + self.servername + '\s*'
        self.file = file
        self.str = linecache.getlines(self.file)                #将整个文件读入一个str类型的list中
        self.num = 0                                            #servername的行号
        self.start = 0                                          #要处理的block的起始行号
        self.end = 0                                            #要处理的block的结束行号
        self.result = []


#根据searvername 查找所在行号
    def get_num(self):
        pattern = re.compile(self.regstr)
        for i in self.str:
            j=i.split('#',1)                    #按#拆分，前半部分就是未被注释的内容即j[0]
            match = re.match(pattern,j[0])      #正则匹配未被注释的部分，用mactch，而非search
            if match:                           #re.match只匹配字符串的开始，如果字符串开始不符合正则表达式，则匹配失败，函数返回None；而re.search匹配整个字符串，直到找到一个匹配。
                self.num = self.str.index(i)    #匹配到的话则返回行号。
                print self.num
                return self.num

#根据servername所在行，逐行递减查找这个server块的起始行号 ，按照正则r'\s*server\s*' 来匹配
    def get_start(self):
        j=self.num
        while True:
            if self.type=='server':
                pattern = re.compile(r'\s*server\s*')
                print 'server'
            elif self.type=='upstream':
                print 'upsteam'
                pattern = re.compile(r'\s*upstream\s*')
            j = j - 1
            k = self.str[j].split('#',1)
            match = re.match(pattern,k[0])
            if match:
                self.start = j
                print self.start
                return self.start

#根据server块起始行，查找这个server块的结尾行号。
    def get_end(self):
        count=0
        k=self.start
        while True:
            t=self.str[k].split('#',1)     #以下三行用来计数。排除注释内容中的{}个数，遇到{计数加一；遇到}计数减一
            count=count+t[0].count('{')
            count=count-t[0].count('}')
            if count == 0:                 #一旦计数为0 ，则认为{}完全成对，此块完结，当前行数即为结尾行数。
                self.end = k
                print self.end
                return self.end
            k = k + 1

    def show_block(self):                   #直接显示出来
        l = self.start
        while l <= self.end:
            print self.str[l],
            l = l + 1

    def get_result(self):                   #将结果赋值给到一个list中
        m = self.start
        while m <= self.end:
            self.result.append(self.str[m])
            m = m +1

        return self.result

if __name__ == '__main__':

    ss = search_servername('linglang.com','conf/abc.conf')
    print ss.get_num()
    print ss.get_start()
    print ss.get_end()
    ss.show_block()

'''
遇到的一些问题
最初的想法是将整个配置文件通过 linecache.getlines 方法读入到一个str的列表中，
然后通过正则匹配表达式 \s*server_name.*'+name+'\s*; 来match到str列表中的元素，然后通过元素获得该行号（要考虑注释的问题）
在通过该行号，递减行号，匹配 server { 同样通过正则来匹配，这样就确定了整个seaver的起始
获得起始行号后，递增行号， 初始一个计数变量count，通过匹配 花括号{}，遇到{ 计数count加1，遇到}计数count减1
考虑到注释中可能会出现花括号，正则写成了这个样子
    regstr_left  = '[^#]*{.*'
    regstr_right = '[^#]*}.*'
一般的文本都可以匹配，但是遇到下面的文本可能会有问题。
        echo 'jquery_get_time_ver1({"result":{"time":$unix_time},"status":{"code":1001,"msg":"success"})';

新的想法，将str中的元素按照#来拆分成两段，第一段是有效文本；第二段就是注释文本，不需要考虑
理论上来讲，ngx配置文件中的花括号{}，不管是本身包含作为分隔符的，还是上文中类似json串中的，都一定是成对出现的，
上文匹配{}的思路是基于一行只有一个的想法。新的想法是吧#（注释）前面文本中的{}全部用来计数，直到计数变为0 用字符串的count方法。
'''

'''def get_end(num):
    print num
    regstr_left  = '[^#]*{.*'
    regstr_right = '[^#]*}.*'

    pattern_left = re.compile(regstr_left)
    pattern_right = re.compile(regstr_right)
    count=0
    while True:
        match = re.match(pattern_left,str[num])
        if match:
            count=count+1
            print str[num]
        match = re.match(pattern_right,str[num])
        if match:
            count=count-1
            print str[num]
        if count == 0:
            end=num
            return end
        num=num+1
    ##{ 与 } 正则表示
'''