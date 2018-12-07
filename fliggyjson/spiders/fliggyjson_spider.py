import scrapy
import time  # time.sleep()
import re  # re.search()
import datetime  # 日期遍历
import codecs  # 存储response
import sys  # 重大错误退出
import urllib  # unicode strings to chinese
import random # ksTS数字随机产生
from ..items import FliggyjsonItem
from scrapy import Request
from scrapy import Selector
# from .login import getCookies #暂时没有使用自动获取cookies

class Fliggyjsonspider(scrapy.Spider):
    name = 'fliggyjson'
    allow_url = ['fliggy.com']

    # 接收起飞城市，抵达城市，开始日期，天数
    depCityCode = input("depCityCode?\n")
    arrCityCode = input("arrCityCode?\n")
    airlineCode = input("airlineCode?\n")
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
        searchJourney0 = [{"arrCityCode": arrCityCode,
                           "depCityCode": depCityCode, "depDate": date, "selectedFlights": []}]
        searchJourney1 = urllib.parse.quote(str(searchJourney0))
        searchJourney = str(searchJourney0)
        #拼接网址
        start_url0 = f'https://sijipiao.fliggy.com/ie/flight_search_result_poller.do?_ksTS='
        start_url1 = f'{a}_{b}&callback=jsonp{c}&supportMultiTrip=true&searchBy=1281'
        start_url2 = f'&childPassengerNum=0&infantPassengerNum=0&searchJourney={searchJourney}'
        start_url3 = '&tripType=0&searchCabinType=0&agentId=-1&controller=1&searchMode=0&b2g=0&formNo=-1&cardId=&needMemberPrice='
        start_url = start_url0 + start_url1 + start_url2 + start_url3
        print(start_url)
        start_urls.append(start_url)

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

        # 删除json1234()保留括号中间的字典字符串，然后把字符串转为字典
        site0 = re.search(r'{.*}', response.text).group()
        site1 = re.sub(r'{0:', r'{"0":', site0)
        site2 = re.sub(r'true', r'"true"', site1)
        site3 = re.sub(r'false', r'"false"', site2)
        site = eval(site3)

        # 抓数据
        for i in range(len(site["data"]["flightItems"])):
            # 校验用
            # print(site["data"]["flightItems"][i]
            #      ["flightInfo"][0]["airlineCodes"])
            if site["data"]["flightItems"][i]["flightInfo"][0]["airlineCodes"] == [self.airlineCode]:
                item["depcity"] = re.search(
                    r"depCityCode':%20'(\w{3})'", response.url).group(1)
                item["arrcity"] = re.search(
                    r"arrCityCode':%20'(\w{3})'", response.url).group(1)
                item["depdate"] = re.findall(
                    r'\d{4}-\d{2}-\d{2}', response.url)[0]
                item["airlineInfo"] = urllib.parse.unquote(
                    site["data"]["flightItems"][i]["flightInfo"][0]["airlineInfo"])
                item["depAirportName"] = urllib.parse.unquote(
                    site["data"]["flightItems"][i]["flightInfo"][0]["depAirportName"])
                item["arrAirportName"] = urllib.parse.unquote(
                    site["data"]["flightItems"][i]["flightInfo"][0]["arrAirportName"])
                item["depTimeStr"] = site["data"]["flightItems"][i]["flightInfo"][0]["depTimeStr"]
                item["arrTimeStr"] = site["data"]["flightItems"][i]["flightInfo"][0]["arrTimeStr"]
                item["price"] = site["data"]["flightItems"][i]["cardTotalPrice"]/100
                if item != {}:
                    items.append(item)
                item = {}
        else:
            print('{}没有你要找的航班'.format(re.findall(
                r'\d{4}-\d{2}-\d{2}', response.url)[0]))
        return items
