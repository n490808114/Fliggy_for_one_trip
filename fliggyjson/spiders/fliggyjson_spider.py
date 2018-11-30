import scrapy
import time
import re
import datetime
import codecs
import json
import sys
import urllib
from ..items import FliggyjsonItem
from scrapy import Request
from scrapy import Selector
from scrapy.http.cookies import CookieJar


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
        tt = str(time.time()*1000)
        a, b, c = (tt.split(".")[0], tt.split(".")[1],
                   str(eval(tt.split(".")[1]+'+1')))

        # 处理网址searchJourney部分
        searchJourney = [{
            "depCityCode": depCityCode,
            "arrCityCode": arrCityCode,
            'depDate': (start_date + datetime.timedelta(days=i)).strftime('%Y-%m-%d'),
            'selectedFlights': []
        }]

        start_url0 = f'https://sijipiao.fliggy.com/ie/flight_search_result_poller.do?_ksTS='
        start_url1 = f'{a}_{b}&callback=jsonp{c}&supportMultiTrip=true&searchBy=1280'
        start_url2 = f'&childPassengerNum=0&infantPassengerNum=0&searchJourney={str(searchJourney)}'
        start_url3 = '&tripType=0&searchCabinType=0&agentId=-1&controller=1&searchMode=0&b2g=0&formNo=-1&cardId=&needMemberPrice='
        start_url = start_url0 + start_url1 + start_url2 + start_url3
        print(start_url)
        start_urls.append(start_url)
    print(start_urls)

    # 初始化CookieJar
    cookie_jar = CookieJar()
    # 在url里面拿出来一个网址做登录测试
    test_url = start_url.pop(0)
    response_test = Request(test_url, headers=header)

    # 如果得到的响应网址是login网址，那么就登录登录到网站上，获取cookie
    # 并用cookie再次获取响应，再次测试
    # 同时把cookie传给start_request()函数
    if "login" in response_test.url:
        check_login(login())
        start_url.append(test_url)
    else:
        parse(response_test)

    # 替换DEFAULT_REQUEST_HEADERS
    def start_requests(self):
        for url in self.start_urls:
            yield Request(url,
                          headers=self.header,
                          cookies=self.cookie_jar,
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

    # 登录动作
    def login(self):
        login_url = 'https://login.taobao.com/member/login.jhtml'
        login_header = ''
        login_post_data = urllib.parse.urlencode({
            'username': '490808114@qq.com',
            'password': 'Zzz8801668',
            # 'username': (str(input("Please input your taobao Username"))),
            # 'password': (str(input("Please input your taobao Password"))),
        })
        return scrapy.FormRequest(
            url=login_url,
            method='POST',
            headers=login_header,
            formdate=login_post_data,
            callback=self.check_login,
        )
    # 检查登录登录是否成功

    def check_login(self, response):
        if True:
            self.cookie_jar.extract_cookies(response, response.Request)
            with open('cookies.txt', 'w') as f:
                for cookie in self.cookie_jar:
                    f.write(str(cookie) + '\n')
