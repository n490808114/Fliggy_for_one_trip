import datetime
import random
import urllib.parse
import time

start_urls = []
depCityCode = input("depCityCode?\n")
arrCityCode = input("arrCityCode?\n")
airlineCode = input("airlineCode?\n")
start_date = datetime.datetime.strptime(
    input("please input scrapy start date\n"), '%Y-%m-%d')
times = int(input("how many days you want search?\n"))
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