# __author:'Mr.Li'

# date:2018/8/3

from urllib import request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
import re
from lxml import etree
import os
import time

base_url = 'https://bj.lianjia.com/xiaoqu/?from=rec'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
    'cookie': 'lianjia_uuid=e7bfc193-9df7-4fee-99b9-12b849b92c58; _smt_uid=5ba1f1bf.a06aefa; UM_distinctid=165f09855722d3-0068ec0a87d8f3-36664c08-13c680-165f098557332c; _ga=GA1.2.526187921.1537339842; lianjia_token=2.0017a893276fc268b60605ba1644494a21; select_city=110000; _jzqckmp=1; _gid=GA1.2.201028289.1540289516; lianjia_ssid=942ca8f0-7245-4bbf-b10d-097ead309b96; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1539855259,1539858151,1540289514,1540343627; _jzqc=1; _jzqy=1.1537339840.1540343627.5.jzqsr=baidu|jzqct=%E9%93%BE%E5%AE%B6.jzqsr=baidu|jzqct=%E9%93%BE%E5%AE%B6; _jzqx=1.1539231190.1540347402.5.jzqsr=bj%2Elianjia%2Ecom|jzqct=/zufang/rs%e5%a4%a9%e5%a4%a9%e5%ae%b6%e5%9b%ad/.jzqsr=bj%2Elianjia%2Ecom|jzqct=/xiaoqu/; _jzqa=1.468389794993398800.1537339840.1540347402.1540357974.24; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1540359475; _jzqb=1.59.10.1540357974.1; _gat=1; _gat_past=1; _gat_global=1; _gat_new_global=1; _gat_dianpu_agent=1'
}

count = 1
req = request.Request(base_url, headers=headers)
response = request.urlopen(req)
html = response.read().decode('utf-8')
pattern = re.compile(r'class="page-box house-lst-page-box".*?"totalPage":(.*?),',re.S)
# 拿到一共有多少页的小区
page = pattern.findall(html)
# print(page)
if(page != []):
    page = int(page[0])
    for i in range(1,page+1,1):
        url = "https://bj.lianjia.com/xiaoqu/pg" + str(i) + "/"
        req = request.Request(url, headers=headers)
        response = request.urlopen(req)
        html = response.read().decode('utf-8')
        # print(html)
        html = etree.HTML(html)
        # 拿到每个小区的链接
        detailPageHtml = html.xpath('//a[@class="img"]/@href')
        # print(detailPageHtml)
        for detailUrl in detailPageHtml:
            req = request.Request(detailUrl, headers=headers)
            response = request.urlopen(req)
            html = response.read().decode('utf-8')
            # print(html)
            html = etree.HTML(html)
            # 拿到所有户型的链接
            allHuXing = html.xpath('//a[@class="btn-large"]/@href')
            # print(allHuXing)
            if(allHuXing != []):
                allHuXingUrl = allHuXing[0]
                # print(allHuXingUrl)
                req = request.Request(allHuXingUrl, headers=headers)
                response = request.urlopen(req)
                html = response.read().decode('utf-8')
                pattern = re.compile(r'class="page-box house-lst-page-box".*?"totalPage":(.*?),', re.S)
                # 拿到一个区一共有多少页的户型
                page = pattern.findall(html)
                # print(page)
                if(page != []):
                    page = int(page[0])
                    for i in range(1, page + 1, 1):
                        allHuXingUrlList = allHuXingUrl + 'pg' + str(i) + '/'
                        # print(allHuXingUrlList)
                        req = request.Request(allHuXingUrlList, headers=headers)
                        response = request.urlopen(req)
                        html = response.read().decode('utf-8')
                        # print(html)
                        html = etree.HTML(html)
                        # 拿到每个户型的路径
                        detailPageHtml = html.xpath('//div[@class="title"]/a[@target="_blank"]/@href')
                        # print(detailPageHtml)
                        for detailurl in detailPageHtml:
                            if (detailurl != []):
                                try:
                                    requ = request.Request(detailurl, headers=headers)
                                    response = request.urlopen(requ)
                                    html = response.read().decode('utf-8')
                                    # print(html)
                                    htmlName = etree.HTML(html)
                                    # 拿到小区的名字
                                    xiaoQuName = htmlName.xpath('//div[@class="wrapper"]/text()')
                                    # print(xiaoQuName)
                                    nameSplit = xiaoQuName[0].split(" ")
                                    # print(nameSplit)
                                    xiaoQuName = nameSplit[0]
                                    # 拿到户型图的链接
                                    huXingUrl = htmlName.xpath('//li[@data-desc="户型图"]/@data-src')
                                    # print(xiaoQuName,huXingUrl)
                                    if (huXingUrl != []):
                                        urlSplit = huXingUrl[0].split(".")
                                        if(urlSplit != []):
                                            # print(urlSplit)
                                            photoUrl = urlSplit[0] + '.' + urlSplit[1] + '.' + urlSplit[2] + '.' + urlSplit[
                                                3] + '.' + "2000x1500" + '.' + urlSplit[-1]
                                            img_name = photoUrl.split('/')
                                            count += 1
                                            print(count,xiaoQuName, photoUrl)
                                            path = os.path.join('./xinlianjia/', xiaoQuName)
                                            if not os.path.exists(path):
                                                os.mkdir(path)
                                            if photoUrl not in path:
                                                try:
                                                    request.urlretrieve(photoUrl, filename=os.path.join(path, img_name[-1]))
                                                    time.sleep(0.3)
                                                except:
                                                    print("找不到图")
                                except:
                                    print('没有图')