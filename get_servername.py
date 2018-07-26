#coding=utf-8
import os,re;
class get_servername:

    def __init__(self,main_file):
        self.main_file = main_file
        self.include_list = []
        self.listDomain = {}
        self.listUpsteam = {}
#从给的主配置文件中获取所有includ
    def IncludeFileList (self):
        fp = open(self.main_file);
        rf = re.compile(r'\s*include\s+(.*);');                 #正则要考虑手抖多打了一些空格的情况
        for line in fp.readlines():
            l = line.split('#',1)
            matchtext=rf.search(l[0]);                          #之前这里写的不严谨,有可能出现注释行的情况
                                                                #现在将当前行按照#拆分，抛弃注释掉的部分，会更严谨
            if matchtext:
                self.include_list.append(matchtext.group(1))
        fp.close()
        return self.include_list
#从include的文件获取所有servername 和 upsteam 。返回两个字典第一个是servername第二个是upstream字典
    def GetDomainandUpsteam(self):
        pathname = os.path.dirname(self.main_file)
        for filename in self.include_list:
            conf_file =pathname+'/'+filename
            if os.path.isfile(conf_file):
                fp = open(conf_file)
                re_domain = re.compile(r'\s*server_name\s+(.*);')
                re_upsteam = re.compile(r'\s*upstream\s+(.*)\s')

                for line in fp.readlines():
                    l = line.split('#',1)
                    match_domain = re_domain.match(l[0])
                    if match_domain:
                        domain = match_domain.group(1)
                        if domain:
                            if self.listDomain.has_key(filename):
                                for i in domain.split(' '):
                                    self.listDomain[filename].append(i)
                            else:
                                self.listDomain[filename] = []
                                for i in domain.split(' '):
                                    self.listDomain[filename].append(i)

                    match_upsteam = re_upsteam.match(l[0])
                    if match_upsteam:
                        upsteam = match_upsteam.group(1).split('{',1)[0]
                        if upsteam:
                            if self.listUpsteam.has_key(filename):
                                self.listUpsteam[filename].append(upsteam)
                            else:
                                self.listUpsteam[filename] = []
                                self.listUpsteam[filename].append(upsteam)
                fp.close();
        return self.listDomain,self.listUpsteam



if __name__ == '__main__':
    gs = get_servername("conf/nginx.conf")
    I = gs.IncludeFileList()
    LD,LU=gs.GetDomainandUpsteam()
    for key in LU:
        print LU[key]

'''
def GetUpstream(filename,listUpsteam):
    if os.path.isfile(filename):
        fp = open(filename);
        re_upsteam = re.compile(r'\s*upstream\s{1,}(.*);');
        for line in fp.readlines():
            match_upsteam = re_upsteam.match(line);
            if match_upsteam:
                upsteam = match_upsteam.group(1);
                if domain:
                    if listUpsteam.has_key(filename):
                        listUpsteam[filename] = listUpsteam[filename] + ';' + upsteam;
                    else:
                        listUpsteam[filename] = upsteam;
        fp.close();
'''

'''

    filelist = []
    mainfile = "conf/nginx.conf"
    listDomain = {}
    listUpsteam = {}
    if os.path.isfile(mainfile):
        IncludeFileList(mainfile,filelist);
        pathname = os.path.dirname(mainfile);
        for name in filelist:
            fname =pathname+os.path.sep+name;
            GetDomainandUpsteam(fname,listDomain,listUpsteam);
    for i in listDomain:
        print i
        print listDomain[i]

    for i in listUpsteam:
        print i
        print listUpsteam[i]
'''
