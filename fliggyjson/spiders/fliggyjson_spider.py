import scrapy
import time  # time.sleep()
import re  # re.search()
import datetime  # 日期遍历
import codecs  # 存储response
import sys  # 重大错误退出
import urllib.parse  # unicode strings to chinese
import random  # ksTS数字随机产生
from ..items import FliggyjsonItem
from scrapy import Request
from scrapy import Selector
import requests
# from .login import getCookies #暂时没有使用自动获取cookies


class Fliggyjsonspider(scrapy.Spider):
    name = 'fliggyjson'
    allow_url = ['fliggy.com']

    header = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.00',
    }

    # 接收起飞城市，抵达城市，开始日期，天数
    depCityCode = input("起飞城市？\n")
    arrCityCode = input("到达城市？\n")
    airlineCode = input("航空公司代码？\n（如果不指定航空公司，将搜索所有的直飞航班）\n")
    start_date = input("开始查询的日期？\n（如果不指定日期，将从今天查起）\n")
    try:
        if start_date == '':
            start_date = datetime.datetime.now()
        else:
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    except:
        print("错误的日期，日期格式YYYY-MM-DD")
    times = int(input("查询多少天？\n"))

    # 声明start_urls
    start_urls = []
    start_url_head = "https://sijipiao.fliggy.com/ie/flight_search_result_poller.do?"
    for i in range(times):

        # 处理网址ksTS和callback部分
        tt0 = str(time.time()*1000)
        a = tt0.split(".")[0]
        tt1 = random.randint(0, 9999)
        b = str(tt1)
        c = str(tt1 + 1)

        # 处理网址searchJourney部分
        date = (start_date + datetime.timedelta(days=i)).strftime('%Y-%m-%d')
        searchJourney = [{
            "arrCityCode": arrCityCode,
            "depCityCode": depCityCode,
            "depDate": date,
            "selectedFlights": []
        }]

        data = {
            '_ksTS': f"{a}_{b}",
            'callback': f"jsonp{c}",
            'supportMultiTrip': True,
            'searchBy': 1281,
            'childPassengerNum': 0,
            'infantPassengerNum': 0,
            'searchJourney': str(searchJourney),
            'tripType': 0,
            'searchCabinType': 0,
            'agentId': -1,
            'controller': 1,
            'searchMode': 0,
            'b2g': 0,
            'formNo': -1,
            'cardId': None,
            'needMemberPrice': None,
        }
        start_url = start_url_head + urllib.parse.urlencode(data)
        start_urls.append(start_url)

    #cookies_list = str(input('Please input Cookies from internet!!!\n'))
    #cookies = {}
    #for line in cookies_list.split(';'):
    #    key, value = line.split('=', 1)
    #    cookies[key] = value

    def start_requests(self):
        for url in self.start_urls:
            befor_depdate = re.findall(r'\d{4}-\d{2}-\d{2}',url)[0]
            befor_url = f"https://sijipiao.fliggy.com/ie/flight_search_result.htm?searchBy=1280&tripType=0&depCity={self.depCityCode}&arrCity={self.arrCityCode}&depDate={befor_depdate}&arrDate="
            r = requests.get(befor_url,headers=self.header)
            print(r.status_code)
            yield Request(url,
                          cookies=r.cookies,
                          callback=self.parse,
                          )

    def parse(self, response):
        items = []
        item = FliggyjsonItem()
        # 删除json1234()保留括号中间的字典字符串，然后把字符串转为字典
        site0 = re.search(r'{.*}', response.text).group()
        site1 = re.sub(r'\n', r'', site0)
        site2 = re.sub(r'{0:', r'{"0":', site1)
        site3 = re.sub(r'true', r'"true"', site2)
        site4 = re.sub(r'false', r'"false"', site3)
        site = eval(site4)
        response_date = re.findall(
            r'\d{4}-\d{2}-\d{2}', response.url)[0]
        # 抓数据
        for i in range(len(site["data"]["flightItems"])):
            if (len(site["data"]["flightItems"][i]["flightInfo"][0]["flightSegments"]) == 1) and ((site["data"]["flightItems"][i]["flightInfo"][0]["airlineCodes"] == [self.airlineCode]) if self.airlineCode != '' else True):
                item["depcity"] = self.depCityCode
                item["arrcity"] = self.arrCityCode
                item["depdate"] = response_date
                item["airlineInfo"] = urllib.parse.unquote(
                    site["data"]["flightItems"][i]["flightInfo"][0]["airlineInfo"])
                item["depAirportName"] = urllib.parse.unquote(
                    site["data"]["flightItems"][i]["flightInfo"][0]["depAirportName"])
                item["arrAirportName"] = urllib.parse.unquote(
                    site["data"]["flightItems"][i]["flightInfo"][0]["arrAirportName"])
                item["depTimeStr"] = site["data"]["flightItems"][i]["flightInfo"][0]["depTimeStr"]
                item["arrTimeStr"] = site["data"]["flightItems"][i]["flightInfo"][0]["arrTimeStr"]
                item["price"] = site["data"]["flightItems"][i]["cardTotalPrice"]/100
                print(item)
                items.append(item)
        if item == {}:
            print(f'{response_date}没有你要找的航班')
        return items
