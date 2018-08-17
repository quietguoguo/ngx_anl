# ngx_anl
目标是做一个在线编辑nginx配置文件，并实现在线检查的web界面<br>
使用了codemirror作为文本编辑器。<br>
<p>思路：<br>
1、从nginx.conf中读取include的配置文件，从各个配置文件中读取servername 和 upsteam 然后根据所在的文件名分类生成呈现在里一个list.html。<br>
2、在list.html中根据用户点选servername和upsteam ，从相应的配置文件中读取相应的配置。<br>
读取方式为： <br>
将配置文件读入一个list中，根据正则匹配找到对应的servername 或者upsteam 关键字。<br>
如果是servername则继续线上查找server关键字，并记录list的行数，然后向下继续读取，根据{}的个数配置判断代码段结束行数。<br>
如果是upsteam，则起始行数就是当前行，向下读取根据{}的个数配置判断代码段结束行数<br>
以上两种方式可以获取相应的代码段的起始结束位置。<br>
3、将第2步中的获取的代码段载入有codemirror的页面show.html中，由用户进行编辑。（不太会做前端的东西，这个页面超级丑）<br>
4、用户提交，由nginx进行检查（用户需要自己搭建nginx环境），如果正确，则写入，然后将整个配置文件显示出来；如果错误，则从备份还原，并显示nginx的报错信息。

<br>
目前做的就是这样子。<br>
