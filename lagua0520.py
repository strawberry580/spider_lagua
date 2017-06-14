__author__ = 'wanglicai'
#coding:utf-8
#文件名  : lagua.py
#版权所有: 北京启明星辰信息安全技术有限公司

#作者    : 王立才
#生成日期: 2017-04-07
#功能描述：抓取拉呱节目视频信息

import urllib
import urllib2
import re
import codecs
import os
import socket

class Spider:

    def __init__(self):
        self.siteURL = 'http://v.iqilu.com/qlpd/l0/'
        #http://v.iqilu.com/qlpd/l0/index_1.html

##下载网页
    def getHtml(self,strname,strurl):
       print strurl
       try:
         request = urllib2.Request(strurl)
         response = urllib2.urlopen(request)
         strhtml = response.read().decode('utf-8')
         f = codecs.open(strname, "w", "utf-8")
         txt = unicode("campeon\n", "utf-8")
         if f:
            f.write(txt)
            f.write(strhtml)
            f.close()
       except urllib2.HTTPError, e:
            strhtml = ""
       except urllib2.URLError, e:
            strhtml = ""

       if f:
          f.close()
       return strhtml

##下载文件
    def auto_downfile(self,url,filename):
       try:
          urllib.urlretrieve(url,filename)
       except urllib.ContentTooShortError:
         print 'XXXXXXXXXXXX  Network conditions is not good.Reloading.'


##解析html页面
    def getContents(self,pageindex):

        if pageindex==0:
           strhtmlURL = self.siteURL
        else:
           strhtmlURL = self.siteURL + "index_" + str(pageindex) + ".html"
        strHtmlName = str(pageindex) + ".html"
        homehtml = self.getHtml(strHtmlName,strhtmlURL)
        pattern = re.compile('<dl>.*?<dt>.*?<a href="(.*?)".*? title="(.*?)".*? target="_blank"><img src="(.*?)"',re.S)
        items = re.findall(pattern,homehtml)
            ## 1链接 2标题 3图片
        for item in items:
            ##print item[0],' ',item[1],' ',item[2]
            strname = "HtmlFiles\\" + item[1] + ".html"
            strurl = item[0]
            strmp4html = self.getHtml(strname,strurl)
            if strmp4html.strip():
               strname = "Mp4Files\\" + item[1] + ".mp4"
               isExists = os.path.exists(strname)
               if not isExists:
                  print strname,' download from '
                  self.getMp4(strname,strmp4html)
            #else:
            #   print strname,' Exists\n'

##解析MP4html页面
    def getMp4(self,strName,strMp4html):
        items = re.findall(r"\"(http:.*?.mp4)\"", strMp4html)
        ## mp4链接
        for item in items:
             print item
             self.auto_downfile(item,strName)
             break


#创建新目录
    def mkdir(self,path):
        path = path.strip()
        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists=os.path.exists(path)
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(path)
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            return False

strinfo =  "\n/================================================================/"
strinfo += "\n/============  [下载拉呱节目视频]  ==============================/"
strinfo += "\n/============  [视频存放在mp4files文件夹下]  ====================/"
strinfo += "\n/============  [该程序仅供个人娱乐使用]  ========================/"
strinfo += "\n/============  [视频版权齐鲁电视台所有]  ========================/"
strinfo += "\n/============  [__author__ 青苹果 2017/05/20 ]  =================/"
strinfo += "\n/================================================================/"
print strinfo.decode('utf-8').encode('cp936')

spider = Spider()
spider.mkdir("HtmlFiles")
spider.mkdir("Mp4Files")
socket.setdefaulttimeout(600)#10分钟超时
for i in range(0,10):
      print "\n/======================== [",i,"] ========================/"
      spider.getContents(i)#venus2011
