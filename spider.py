# -*- codeing = utf-8 -*-
# @Time : 2022/3/13 21:43
# @Author : zhangxianglong
# @File : spider.py
# @Software : PyCharm

from bs4 import  BeautifulSoup     #网页解析,获取数据
import re       #正则表达式，进行文字匹配
import urllib.request,urllib.error      #制定URL，获取网页数据
import xlwt     #进行excel操作
import sqlite3  #进行SQLite数据库操作

def main():
    baseurl = "https://movie.douban.com/top250?start="
    #1.爬取网页
    datalist = getData(baseurl)
    savepath = "豆瓣电影Top250.xls"
    #3.保存数据
    saveData(datalist,savepath)

#链接的正则表达式
findLink = re.compile(r'<a href="(.*?)">')
#图片的正则表达式
findImgSrc = re.compile(r'<img.*src="(.*?)"',re.S)  #re.S 让换行符包含在字符中
#片名的正则表达式
findTitle = re.compile(r'<span class="title">(.*)</span>')
#评分的正则表达式
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
#评价人数的正则表达式
findJudge = re.compile(r'<span>(\d*)人评价</span>')
#简介的正则表达式
findInq = re.compile(r'<span class="inq">(.*)</span>')
#具体内容的正则表达式
findBd = re.compile(r'<p class="">(.*?)</p>',re.S)

def getData(baseurl):
    datalist = []
    for i in range(0,10):#调用获取页面信息的函数
        url = baseurl + str(i*25)
        html = askURL(url)#保存获取的网页
        #2.逐一解析数据
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div',class_="item"):     #查找符合要求的字符串，形成列表
            #print(item)#测试
            data = []#保存一部电影的所有信息
            item = str(item)
            #影片详情的链接
            link = re.findall(findLink,item)[0]
            data.append(link)
            #图片
            imgSrc = re.findall(findImgSrc,item)[0]
            data.append(imgSrc)
            #电影名
            titles = re.findall(findTitle,item)
            if(len(titles) == 2):
                ctitle = titles[0]
                data.append(ctitle)
                otitle = titles[1].replace("/","")
                data.append(otitle)
            else:
                data.append(titles[0])
                data.append(' ')#留空
            #评分
            rating = re.findall(findRating,item)[0]
            data.append(rating)
            #评价人数
            judgeNum = re.findall(findJudge,item)[0]
            data.append(judgeNum)
            #简介
            inq = re.findall(findInq,item)
            if len(inq) != 0:
                inq = inq[0].replace("。","")#去掉句号
                data.append(inq)
            else:
                data.append(" ")#留空
            # 具体内容
            bd = re.findall(findBd,item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?'," ",bd)     #去掉<br/>
            bd = re.sub('/'," ",bd)                     #去掉/
            data.append(bd.strip())                     ##去掉空格
            datalist.append(data)

    return datalist

#得到一个指定的URL的网页内容
def askURL(url):
    head = {    #模拟头部信息
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
    }
    request = urllib.request.Request(url,headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        #print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html




#保存数据
def saveData(datalist,savepath):
    book = xlwt.Workbook(encoding="utf-8",style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet('豆瓣电影Top250',cell_overwrite_ok=True)  # 创建工作表
    col = ("电影详情链接","图片链接","影片中文名","影片外国名","评分","评价人数","概况","相关信息")
    for i in range(0,8):
        sheet.write(0,i,col[i])#列名
    for i in range(0,250):
        print("第%d条"%(i+1))
        data = datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])
    book.save(savepath)  # 保存数据表


if __name__ == "__main__":#当程序执行时
    #调用函数
    main()
    print("爬取完毕！")