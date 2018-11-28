import scrapy
import time
import re
from ..items import FliggyjsonItem
from scrapy import Request
from scrapy import Selector

class Fliggyjsonspider(scrapy.Spider):
    name='fliggyjson'
    allow_url = ['fliggy.com']

    cookie = {
        'cookie':'orderBy=totalPrice; t=bf9be5e2e8d27395fb8a938060285400; _tb_token_=coJbGLq8KgyL2pgTPzV0; cookie2=1ee6daec952a9da4888497507e3ec0fb; cna=ZqWFFApTJ1wCAatYLauO6+X7; isg=BGdnSaqL8IA9DHQMnnPxmQDB9ZLxREVP_0tVJznUtPYdKIfqQbiUH1shTuAT2xNG; hng=""; uc1=cookie16=VFC%2FuZ9az08KUQ56dCrZDlbNdA%3D%3D&cookie21=WqG3DMC9Fb5mPLIQo9kR&cookie15=W5iHLLyFOGW7aA%3D%3D&existShop=false&pas=0&cookie14=UoTYNc%2FjoMAejw%3D%3D&tag=8&lng=zh_CN; uc3=vt3=F8dByR1WS%2FkGAZSKw4g%3D&id2=UUBZFJ7tZScqxw%3D%3D&nk2=rt4ZDKM%2BEgA%3D&lg2=W5iHLLyFOGW7aA%3D%3D; tracknick=%5Cu7A81%5Cu98DE%5Cu70FD%5Cu4E91; _l_g_=Ug%3D%3D; ck1=""; unb=2815955626; lgc=%5Cu7A81%5Cu98DE%5Cu70FD%5Cu4E91; cookie1=VWfHkD1GJQFoMdWi6P3FU55YkUwsXeOgEn492IGYmgI%3D; login=true; cookie17=UUBZFJ7tZScqxw%3D%3D; _nk_=%5Cu7A81%5Cu98DE%5Cu70FD%5Cu4E91; uss=""; csg=21825861; skt=d83027a01de1d029; enc=ExPhEL%2FD5HqhtcCop3C5Vdjj7tvwxK7dcPFWEwMTaVpLbwCN71nG5xDjLeT0qONUUN%2F2CrPoic4G%2BIY6VkGeOQ%3D%3D'
        }
    
    depCityCode = input("depCityCode?")
    arrCityCode = input("arrCityCode?")
    depDate = input("depDate?")

    searchJourney=[
        {
            "depCityCode":depCityCode,
            "arrCityCode":arrCityCode,
            "depDate":depDate,
            "selectedFlights":[]
        }
        ]

    #_ksTS={str(time.time()*1000)[:13]}_{str(time.time()*1000)[14:]}&callback=jsonp{str(int(str(time.time()*1000)[14:])+1)}

    start_url = [f'https://sijipiao.fliggy.com/ie/flight_search_result_poller.do?_ksTS=1543432777709_726&callback=jsonp727&supportMultiTrip=true&searchBy=1280&childPassengerNum=0&infantPassengerNum=0&searchJourney={searchJourney}&tripType=0&searchCabinType=0&agentId=-1&controller=1&searchMode=0&b2g=0&formNo=-1&cardId=&needMemberPrice=']
    
    def start_requests(self):
        for url in self.start_urls:
            yield Request(
                url,
                callback=self.parse,
                cookies=self.cookie,
                )

    def parse(self,response):

        items = []
        item = FliggyjsonItem()
        site0 = list(re.split('jsonp(\d){,4}',response.text)[-1][1:-2])
        site1 = re.sub(r'{0:','{"1":',site0)
        site2 = re.sub(r'true','"true"',site1)
        site3 = re.sub(r'false','"false"',site2)
        site =eval(site3)
        for i in range(10):
            if site["data"]["flightItems"][i]["flightInfo"][0]["depAirlineCode"] == 'JQ':
                item["depcity"] = site["data"]["flightItems"][i]["flightInfo"][0]["flightSegments"][0]["depCityCode"]
                item["arrcity"] = site["data"]["flightItems"][i]["flightInfo"][0]["flightSegments"][0]["arrCityCode"]
                item["depdate"] = site["data"]["flightItems"][i]["flightInfo"][0]["flightSegments"][0]["depTimeStr"].split(" ")[0]
                item["price"] = site["data"]["flightItems"][i]["cardTotalPrice"]
                break
        print(item)
        items.append(item)