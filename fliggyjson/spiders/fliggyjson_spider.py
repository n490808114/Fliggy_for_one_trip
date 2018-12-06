import scrapy
import time  # time.sleep()
import re  # re.search()
import datetime  # 日期遍历
import codecs  # 存储response
import sys  # 重大错误退出
import urllib
import random
from ..items import FliggyjsonItem
from scrapy import Request
from scrapy import Selector
from .login import getCookies


class Fliggyjsonspider(scrapy.Spider):
    name = 'fliggyjson'
    allow_url = ['fliggy.com']

    # 接收起飞城市，抵达城市，开始日期，天数
    depCityCode = input("depCityCode?\n")
    arrCityCode = input("arrCityCode?\n")
    start_date = datetime.datetime.strptime(
        input("please input scrapy start date\n"), '%Y-%m-%d')
    times = int(input("how many days you want search?\n"))

    # 替换DEFAULT_REQUEST_HEADERS
    header = {
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0',
    }

    # 声明start_urls
    start_urls = []

    for i in range(times):

        # 处理网址ksTS和callback部分
        tt0 = str(time.time()*1000)
        a = tt0.split(".")[0]
        tt1 = random.randint(0, 9999)
        b = str(tt1)
        c = str(tt1 + 1)

        # 处理网址searchJourney部分
        date = (start_date + datetime.timedelta(days=i)).strftime('%Y-%m-%d')
        # searchJourney0 = f'%5B%7B%22arrCityCode%22%3A%22{arrCityCode}%22%2C%22depCityCode%22%3A%22{depCityCode}'
        # searchJourney1 = f'%22%2C%22depDate%22%3A%22{date}%22%2C%22selectedFlights%22%3A%5B%5D%7D%5D'
        # searchJourney = searchJourney0 + searchJourney1
        searchJourney0 = [{"arrCityCode": arrCityCode,
                           "depCityCode": depCityCode, "depDate": date, "selectedFlights": []}]
        searchJourney1 = urllib.parse.quote(str(searchJourney0))
        searchJourney = str(searchJourney0)
        start_url0 = f'https://sijipiao.fliggy.com/ie/flight_search_result_poller.do?_ksTS='
        start_url1 = f'{a}_{b}&callback=jsonp{c}&supportMultiTrip=true&searchBy=1281'
        start_url2 = f'&childPassengerNum=0&infantPassengerNum=0&searchJourney={searchJourney}'
        start_url3 = '&tripType=0&searchCabinType=0&agentId=-1&controller=1&searchMode=0&b2g=0&formNo=-1&cardId=&needMemberPrice='
        start_url = start_url0 + start_url1 + start_url2 + start_url3
        print(start_url)
        start_urls.append(start_url)
    print(start_urls)

    # 在url里面拿出来一个网址做登录测试
    cookies_list = str(input('Please input Cookies from internet!!!\n'))
    cookies = {}
    for line in cookies_list.split(';'):
        key, value = line.split('=', 1)
        cookies[key] = value
    #test_url = start_urls.pop(0)
    #response_test = Request(test_url, headers=header)
    # 如果得到的响应网址是login网址，那么就登录登录到网站上，获取cookie
    # 并用cookie再次获取响应，再次测试
    # 同时把cookie传给start_request()函数

    #cookies = getCookies()
    #cookies = "orderBy=undefined; __guid=74766352.1451806701806439200.1532330561021.38; _umdata=6DF8A7CF5CA7BAC2756318B76F0C18CBF3B143C2191B477D9ADC3C1AAC61DF48AC423B94F08E3504CD43AD3E795C914CAF29FA256100E0D3C340701FB36F69D7; hng=CN%7Czh-CN%7CCNY%7C156; lid=%E5%9B%9B%E5%B7%9D%E9%93%81%E8%88%AA%E5%95%86%E6%97%85; cna=NHPUExvnDkACAavd8fAcPWmV; t=2a22edebcf647cd89d97eac8d717026b; tracknick=%5Cu56DB%5Cu5DDD%5Cu94C1%5Cu822A%5Cu5546%5Cu65C5; _tb_token_=w9P8VO7Ds79kkdK9MqT8; cookie2=1d2c40bed781d6f3280bfbe0d3d7f787; dnk=%5Cu56DB%5Cu5DDD%5Cu94C1%5Cu822A%5Cu5546%5Cu65C5; sk=sai=UUjZelvO6U7stsCVwbFftg%3D%3D&n=qGxD%2FJkjMY5nzndI&sae=UUtO%2FV%2BJNKq8f6vDFdxC3h4%3D&agf=AHt%2BE4yWJ9vdW%2B3PG2H51AyjIfm77%2B3T1PCl1UVBPKI%3D&ss=Tmc%3D&fg=Vvj6Fvb8IA%3D%3D&agt=Ug%3D%3D&i=Vv7BmA%3D%3D&fn=qGxD%2FJkjMY4XrIJyKN%2BC20ZS6lobLAigB2M%3D&ln=qGxD%2FJkjMY5nzndI; tal=Vw%3D%3D; __guid=66414014.4475733110818210000.1540536894689.8647; uc1=cookie16=VFC%2FuZ9az08KUQ56dCrZDlbNdA%3D%3D&tmb=1&cookie21=UIHiLt3xSard&cookie15=UIHiLt3xD8xYTw%3D%3D&existShop=true&pas=0&cookie14=UoTYNcxtv7UJUw%3D%3D&tag=8&lng=zh_CN; csg=4b4b389a; ck=uid=UNJZJXuidSDLjQ%3D%3D; sty=2; enc=ac3moLzGNB8gKq7sZNJJxiNcxzhWuMhMt7wAdJnB8JVU1SQaW5jcA8A38Qi18Nq6kgsTjJ7DWv3PH%2BWpmN6N9Q%3D%3D; isg=BPHxpR4oCYSVd6LZxoE_UaEjAH0nznBToP23Z9MGz7jX-hFMGi8uID9bGM45Mv2I; monitor_count=50"

    # 替换DEFAULT_REQUEST_HEADERS

    def start_requests(self):

        for url in self.start_urls:
            yield Request(url,
                          headers=self.header,
                          cookies=self.cookies,
                          callback=self.parse,
                          )

    def parse(self, response):
        items = []
        item = FliggyjsonItem()

        # 打印一下response,检验
        # with codecs.open(f'{int(time.time()*1000)}.txt', 'wb', encoding='utf-8') as f:
        #    f.write(response.text)

        # 删除json1234()保留括号中间的字典字符串，然后把字符串转为字典
        site0 = re.search(r'{.*}', response.text).group()
        site1 = re.sub(r'{0:', r'{"0":', site0)
        site2 = re.sub(r'true', r'"true"', site1)
        site3 = re.sub(r'false', r'"false"', site2)
        site = eval(site3)

        # 打印一下格式,检验
        print(type(site))

        # 抓数据
        for i in range(len(site["data"]["flightItems"])):
            #校验用
            #print(site["data"]["flightItems"][i]
            #      ["flightInfo"][0]["airlineCodes"])
            if site["data"]["flightItems"][i]["flightInfo"][0]["airlineCodes"] == ["JQ"]:
                item["depcity"] = site["data"]["flightItems"][i]["flightInfo"][0]["flightSegments"][0]["depCityCode"]
                item["arrcity"] = site["data"]["flightItems"][i]["flightInfo"][0]["flightSegments"][0]["arrCityCode"]
                item["depdate"] = site["data"]["flightItems"][i]["flightInfo"][0]["flightSegments"][0]["depTimeStr"].split(" ")[
                    0]
                item["price"] = site["data"]["flightItems"][i]["cardTotalPrice"]
                print(item)
                break
        # 打印一下item 校验
        # print(item)
        if item != {}:
            items.append(item)
        else:
            print('{}没有你要找的航班'.format(re.findall(r'\d{4}-\d{2}-\d{2}',response.url)[0]))
        return items
