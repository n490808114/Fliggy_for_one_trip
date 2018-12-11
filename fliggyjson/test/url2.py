import datetime
import random
import urllib.parse
import time


start_urls = []
depCityCode = input("depCityCode?\n")
arrCityCode = input("arrCityCode?\n")
start_date = datetime.datetime.strptime(
    input("please input scrapy start date\n"), '%Y-%m-%d')


tt0 = str(time.time()*1000)
a = tt0.split(".")[0]
tt1 = random.randint(0, 9999)
b = str(tt1)
c = str(tt1 + 1)

date = (start_date + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

searchJourney = [{
    "depCityCode":depCityCode,
    "arrCityCode":arrCityCode,
    "depDate":date,
    "selectedFlights":[]
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
start_url_head = "https://sijipiao.fliggy.com/ie/flight_search_result_poller.do?"
print(type(urllib.parse.urlencode(data)))
start_url = start_url_head + urllib.parse.urlencode(data)
print(start_url)

