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
    depCityCode = input("depCityCode?")
    arrCityCode = input("arrCityCode?")
    start_date = datetime.datetime.strptime(
        input("please input scrapy start date"), '%Y-%m-%d')
    times = int(input("how many days you want search?"))

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
        tt1 = random.randint(0,9999)
        b = str(tt1)
        c = str(tt1 + 1)


        # 处理网址searchJourney部分
        date = (start_date + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        # searchJourney0 = f'%5B%7B%22arrCityCode%22%3A%22{arrCityCode}%22%2C%22depCityCode%22%3A%22{depCityCode}'
        # searchJourney1 = f'%22%2C%22depDate%22%3A%22{date}%22%2C%22selectedFlights%22%3A%5B%5D%7D%5D'
        # searchJourney = searchJourney0 + searchJourney1
        searchJourney0  =[{"arrCityCode":arrCityCode,"depCityCode":depCityCode,"depDate":date,"selectedFlights":[]}]
        searchJourney1 = urllib.parse.quote(str(searchJourney0))
        searchJourney = str(searchJourney0)
        start_url0 = f'https://sijipiao.fliggy.com/ie/flight_search_result_poller.do?_ksTS='
        start_url1 = f'{a}_{b}&callback=jsonp{c}&supportMultiTrip=true&searchBy=1281'
        start_url2 = f'&childPassengerNum=0&infantPassengerNum=0&searchJourney={searchJourney}'
        start_url3 = '&tripType=0&searchCabinType=0&agentId=-1&controller=1&searchMode=0&b2g=0&formNo=-1&cardId=&needMemberPrice='
        start_url =  start_url0 + start_url1 + start_url2 + start_url3
        print(start_url)
        start_urls.append(start_url)
    print(start_urls)

    # 在url里面拿出来一个网址做登录测试

    
    test_url = start_urls.pop(0)
    response_test = Request(test_url, headers=header)
    # 如果得到的响应网址是login网址，那么就登录登录到网站上，获取cookie
    # 并用cookie再次获取响应，再次测试
    # 同时把cookie传给start_request()函数

    cookies = getCookies()
        

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
        with codecs.open(f'{int(time.time()*1000)}.txt', 'wb', encoding='utf-8') as f:
            f.write(response.text)

        # 删除json1234()保留括号中间的字典字符串，然后把字符串转为字典
        site0 = re.search(r'json\d{,4}\((.*)\)', response.text).group()
        site1 = re.sub(r'{0:', r'{"0":', site0)
        site = eval(site1)

        # 打印一下格式,检验
        print(type(site))

        # 抓数据
        for i in range(10):
            print(site["data"]["flightItems"][i]
                    ["flightInfo"][0]["depAirlineCode"])
            if site["data"]["flightItems"][i]["flightInfo"][0]["depAirlineCode"] == 'JQ':
                item["depcity"] = site["data"]["flightItems"][i]["flightInfo"][0]["flightSegments"][0]["depCityCode"]
                item["arrcity"] = site["data"]["flightItems"][i]["flightInfo"][0]["flightSegments"][0]["arrCityCode"]
                item["depdate"] = site["data"]["flightItems"][i]["flightInfo"][0]["flightSegments"][0]["depTimeStr"].split(" ")[
                    0]
                item["price"] = site["data"]["flightItems"][i]["cardTotalPrice"]
                print(item)
                break
        print(item)
        items.append(item)


