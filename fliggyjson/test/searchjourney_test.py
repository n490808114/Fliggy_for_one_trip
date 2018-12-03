'''
https://sijipiao.fliggy.com/ie/flight_search_result_poller.do?_ksTS=1543470153276_758
&callback=jsonp759&supportMultiTrip=true&searchBy=1281&childPassengerNum=0&infantPassengerNum=0&searchJourney=
[{"depCityCode":"CTU",
"arrCityCode":"ZRH",
"depCityName":"%E6%88%90%E9%83%BD",
"arrCityName":"%E8%8B%8F%E9%BB%8E%E4%B8%96",
"depDate":"2018-12-12",
"selectedFlights":[]}]
&tripType=1&searchCabinType=0&agentId=-1&controller=1&searchMode=0&b2g=0&formNo=-1&cardId=&needMemberPrice=
'''
'''
https://sijipiao.fliggy.com/ie/flight_search_result_poller.do?_ksTS=1543801573274_754
&callback=jsonp755&supportMultiTrip=true&searchBy=1281&childPassengerNum=0&infantPassengerNum=0&searchJourney=
%5B%7B%22arrCityCode%22%3A%22MEL%22%2C%22depCityCode%22%3A%22CGO%22%2C%22depDate%22%3A%222018-12-12%22%2C%22selectedFlights%22%3A%5B%5D%7D%5D
&tripType=0&searchCabinType=0&agentId=-1&controller=1&searchMode=0&b2g=0&formNo=-1&cardId=&needMemberPrice=true
'''
'''
https://sijipiao.fliggy.com/ie/flight_search_result_poller.do?_ksTS=1543799496113_9998
&callback=jsonp9999&supportMultiTrip=true&searchBy=1280&childPassengerNum=0&infantPassengerNum=0&searchJourney=
[%7B'depCityCode':%20'CGO',%20'arrCityCode':%20'MEL',%20'depDate':%20'2018-12-20',%20'selectedFlights':%20[]%7D]&tripType=0&searchCabinType=0&agentId=-1&controller=1&searchMode=0&b2g=0&formNo=-1&cardId=&needMemberPrice=
'''
import datetime
import urllib.parse

depCityCode = input("depCityCode?")
arrCityCode = input("arrCityCode?")
start_date = datetime.datetime.strptime(
    input("please input scrapy start date"), '%Y-%m-%d')
#times = int(input("how many days you want search?"))
date = (start_date + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
searchJourney0  =[{"arrCityCode":"{arrCityCode}","depCityCode":"{depCityCode}","depDate":"{date}","selectedFlights":[]}]
searchJourney = [{"depCityCode": depCityCode,
                    "arrCityCode": arrCityCode,
                    'depDate': (start_date + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
                    'selectedFlights':[]}]
print(urllib.parse.quote(f'result={searchJourney}'))
print(searchJourney0)
print(urllib.parse.quote(str(searchJourney0)))