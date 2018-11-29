import scrapy
import time
import re
import datetime
import codecs
import json
from ..items import FliggyjsonItem
from scrapy import Request
from scrapy import Selector

class Fliggyjsonspider(scrapy.Spider):
    name='fliggyjson'
    allow_url = ['fliggy.com']

    cookie = {
        'cookie':'orderBy=undefined; __guid=74766352.1451806701806439200.1532330561021.38; _umdata=6DF8A7CF5CA7BAC2756318B76F0C18CBF3B143C2191B477D9ADC3C1AAC61DF48AC423B94F08E3504CD43AD3E795C914CAF29FA256100E0D3C340701FB36F69D7; enc=sOVscSZ6cTGBauwU%2Bg3V5DdGuwiEr8ePoQLv2Wat5MJ9rhr5Cezn976IJnEyKs30qwugz9GEF%2BxqYy%2FU6t8qww%3D%3D; UM_distinctid=1674ea76872d-0cb9737524ac9f-454c092b-140000-1674ea7687355e; hng=CN%7Czh-CN%7CCNY%7C156; lid=%E5%9B%9B%E5%B7%9D%E9%93%81%E8%88%AA%E5%95%86%E6%97%85; cna=NHPUExvnDkACAavd8fAcPWmV; t=2a22edebcf647cd89d97eac8d717026b; tracknick=%5Cu56DB%5Cu5DDD%5Cu94C1%5Cu822A%5Cu5546%5Cu65C5; _tb_token_=HzxKmazPt5PUvrW9vU18; cookie2=1173ff590376e609a83582ac8bc59ef0; dnk=%5Cu56DB%5Cu5DDD%5Cu94C1%5Cu822A%5Cu5546%5Cu65C5; sk=sai=UUjZelvO6U7stsCVwbFftg%3D%3D&n=qGxD%2FJkjMY5nzndI&sae=UUtO%2FV%2BJNKq8f6vDFdxC3h4%3D&agf=WvWtM3kwAWiQHvVcjPFNbVPv91yf%2FeacJbCKQ%2FO9Fks%3D&ss=Tmc%3D&fg=Vvj6Fvb8IA%3D%3D&agt=Ug%3D%3D&i=Vv7BmA%3D%3D&fn=qGxD%2FJkjMY4XrIJyKN%2BC20ZS6lobLAigB2M%3D&ln=qGxD%2FJkjMY5nzndI; tal=Vw%3D%3D; l=aB8lElnGHIFLOFoXkManmSp2yOqxjgfLPpJW1MwP-Tx40AIhDYjkcdrbR_zINlIeSqOyu02V505j0; __guid=66414014.4475733110818210000.1540536894689.8647; sg=%E6%97%858a; _nk_=%5Cu56DB%5Cu5DDD%5Cu94C1%5Cu822A%5Cu5546%5Cu65C5; uc1=cookie16=UIHiLt3xCS3yM2h4eKHS9lpEOw%3D%3D&tmb=1&cookie21=U%2BGCWk%2F7oPGl&cookie15=Vq8l%2BKCLz3%2F65A%3D%3D&existShop=true&pas=0&cookie14=UoTYNc%2FnTOZKEQ%3D%3D&tag=8&lng=zh_CN; _l_g_=Ug%3D%3D; csg=05b5dd07; cookie1=AQGq2PB8ic%2FwnzXT6Eo4wxZvkgsM%2BUL%2BgMIehzviOHg%3D; unb=3286044998; cookie17=UNJZJXuidSDLjQ%3D%3D; ck=uid=UNJZJXuidSDLjQ%3D%3D; login=true; sty=2; monitor_count=33; isg=BKKiHfzeDQLLdRFsmZycPBam8yio47MO91gkMuw7zpXAv0I51IP2HSg567vmrx6l'
        }
    
    # 接收起飞城市，抵达城市，开始日期，天数
    depCityCode = input("depCityCode?")
    arrCityCode = input("arrCityCode?")
    start_date = datetime.datetime.strptime(input("please input scrapy start date"),'%Y-%m-%d')
    times = int(input("how many days you want search?"))

    # 替换DEFAULT_REQUEST_HEADERS
    header = {
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0',
    }
    # 声明start_urls
    start_urls = []

    for i in range(times):

        # 处理网址ksTS和callback部分
        tt = str(time.time()*1000)
        a ,b ,c = (tt.split(".")[0],tt.split(".")[1],str(eval(tt.split(".")[1]+'+1')))
        
        # 处理网址searchJourney部分
        searchJourney=[{
            "depCityCode":depCityCode,
                "arrCityCode":arrCityCode,
                'depDate':(start_date + datetime.timedelta(days=i)).strftime('%Y-%m-%d'),
                'selectedFlights':[]
                }]
        
        start_url0 = f'https://sijipiao.fliggy.com/ie/flight_search_result_poller.do?_ksTS='
        start_url1 = f'{a}_{b}&callback=jsonp{c}&supportMultiTrip=true&searchBy=1280'
        start_url2 = f'&childPassengerNum=0&infantPassengerNum=0&searchJourney={str(searchJourney)}'
        start_url3 = '&tripType=0&searchCabinType=0&agentId=-1&controller=1&searchMode=0&b2g=0&formNo=-1&cardId=&needMemberPrice=' 
        start_url = start_url0 + start_url1 + start_url2 + start_url3
        print(start_url)
        start_urls.append(start_url)
    print(start_urls)

    # 替换DEFAULT_REQUEST_HEADERS
    def start_requests(self):
        for url in self.start_urls:
            yield Request(url,headers=self.header,callback=self.parse)

    def parse(self,response):
        items = []
        item = FliggyjsonItem()
        with codecs.open(f'{int(time.time()*1000)}.txt','wb',encoding='utf-8') as f:
            f.write(response.text)
        site0 = list(re.split(r'jsonp(\d){,4}',response.text)[-1][1:-2])
        site1 = re.sub(r'{0:',r'{"1":',site0)
        site2 = re.sub(r'true','"true"',site1)
        site3 = re.sub(r'false','"false"',site2)
        site =eval(site3)
        #site = eval(response.text)
        print(type(site))
        print(response.text.count('a'))
        for i in range(10):
            print(site["data"]["flightItems"][i]["flightInfo"][0]["depAirlineCode"])
            if site["data"]["flightItems"][i]["flightInfo"][0]["depAirlineCode"] == 'JQ':
                item["depcity"] = site["data"]["flightItems"][i]["flightInfo"][0]["flightSegments"][0]["depCityCode"]
                item["arrcity"] = site["data"]["flightItems"][i]["flightInfo"][0]["flightSegments"][0]["arrCityCode"]
                item["depdate"] = site["data"]["flightItems"][i]["flightInfo"][0]["flightSegments"][0]["depTimeStr"].split(" ")[0]
                item["price"] = site["data"]["flightItems"][i]["cardTotalPrice"]
                print(item)
                break
        print(item)
        items.append(item)