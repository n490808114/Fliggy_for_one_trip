import scrapy
import re  # re.search()
import urllib.parse  # unicode strings to chinese
from ..items import FliggyjsonItem
from scrapy import Request
from scrapy import Selector
from .start_urls import get_start_urls
# from .login import getCookies #暂时没有使用自动获取cookies

class Fliggyjsonspider(scrapy.Spider):
    name = 'fliggyjson'
    allow_url = ['fliggy.com']



    depCityCode = input("起飞城市？\n")
    arrCityCode = input("到达城市？\n")
    airlineCode = input("航空公司代码？\n（如果不指定航空公司，将搜索所有的直飞航班）\n")
    start_date = input("开始查询的日期？\n（如果不指定日期，将从今天查起）\n")
    search_for_each_week = input("请输入航班周期:\n(周一请输入1，周二请输入2.......周日请输入7.\n如果不限制航班周期，什么都不要输入)")
    times = int(input("查询多少天？\n"))

    start_urls = get_start_urls(depCityCode,arrCityCode,start_date,search_for_each_week,times)

    cookies_list = str(input('Please input Cookies from internet!!!\n'))
    cookies = {}
    for line in cookies_list.split(';'):
        key, value = line.split('=', 1)
        cookies[key] = value

    def start_requests(self):
        for url in self.start_urls:
            #befor_depdate = re.findall(r'\d{4}-\d{2}-\d{2}',url)[0]
            #befor_url = f"https://sijipiao.fliggy.com/ie/flight_search_result.htm?searchBy=1280&tripType=0&depCity={self.depCityCode}&arrCity={self.arrCityCode}&depDate={befor_depdate}&arrDate="
            #r = requests.get(befor_url,headers=self.header)
            #print(r.status_code)
            header = {
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.00',
                'referer':re.sub(r'http(.*)searchby','https://sijipiao.fliggy.com/ie/flight_search_result.htm?searchBy',url)
            }
            yield Request(url,
                        headers=header,
                        cookies=self.cookies,
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
                #print(item)
                items.append(item)
                item = {}
        #if item == {}:
        #    print(f'{response_date}没有你要找的航班')
        return items
