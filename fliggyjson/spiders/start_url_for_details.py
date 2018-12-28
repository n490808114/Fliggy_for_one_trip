import time
import random
import datetime
import urllib.parse

def get_start_url_for_details(depCityCode,arrCityCode,start_date,search_for_each_week,times):
    '''
    https://sijipiao.fliggy.com/ie/flight_search_result_poller.do?
    _ksTS=1545790243989_2504
    &callback=jsonp2505
    &supportMultiTrip=true
    &searchBy=1280
    &childPassengerNum=0
    &infantPassengerNum=0
    &searchJourney=
    [{
        "depCityCode":"CGO",
        "arrCityCode":"MEL",
        "depDate":"2019-01-09",
        "selectedFlights":
        [{
            "marketFlightNo":"JQ068",
            "operatFlightNo":"",
            "flightTime":"2019-01-09 23:05:00",
            "depCityCode":"CGO",
            "arrCityCode":"MEL",
            "depAirportCode":"CGO",
            "arrAirportCode":"MEL",
            "marketingAirlineCode":"JQ",
            "operatingAirlineCode":"",
            "codeShare":"false",
            "depTerm":"",
            "arrTerm":""
        }]
    }]
    &tripType=0
    &searchCabinType=0
    &agentId=-1
    &searchMode=2
    &controller=1
    &b2g=0
    &formNo=-1
    &cardId=
    &needMemberPrice=
    '''
    try:
        if start_date == '':
            start_date = datetime.datetime.now()
        else:
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    except:
        print("错误的日期，日期格式YYYY-MM-DD")

    FlightNo = input("请输入航班号：\n").upper()
    AirLineNo = FlightNo[0:2]
    flightTime = input("请输入起飞时间，格式如下23:05\n")
    start_urls = []
    start_url_head = "https://sijipiao.fliggy.com/ie/flight_search_result_poller.do?"

    for i in range(times):
        tt0 = str(time.time()*1000)
        a = tt0.split(".")[0]
        tt1 = random.randint(0, 9999)
        b = str(tt1)
        c = str(tt1 + 1)
        date = start_date + datetime.timedelta(days=i)
        if (search_for_each_week != '') and (str(date.weekday()+1) not in search_for_each_week):
            continue
        date = date.strftime('%Y-%m-%d')
        flightDateTime = date + " " + flightTime +":00"
        searchJourney = [{
            "depCityCode":depCityCode,
            "arrCityCode":arrCityCode,
            "depDate":date,
            "selectedFlights":
            [{
            "marketFlightNo":FlightNo,
            "operatFlightNo":"",
            "flightTime":flightDateTime,
            "depCityCode":depCityCode,
            "arrCityCode":arrCityCode,
            "depAirportCode":depCityCode,
            "arrAirportCode":arrCityCode,
            "marketingAirlineCode":AirLineNo,
            "operatingAirlineCode":"",
            "codeShare":"false",
            "depTerm":"",
            "arrTerm":""
        }]
        }]
        data = {
            "_ksTS" : f"{a}_{b}",
            "callback" : f"jsonp{c}",
            "supportMultiTrip" : "true",
            "searchBy" : 1280,
            "childPassengerNum" : 0,
            "infantPassengerNum" : 0,
            "searchJourney" : "searchJourneyForChange",
            "tripType" : 0,
            "searchCabinType" : 0,
            "agentId" : -1,
            "searchMode" : 2,
            "controller" : 1,
            "b2g" : 0,
            "formNo" : -1,
            "cardId" : None,
            "needMemberPrice" : None,
        }
        start_url = start_url_head + urllib.parse.urlencode(data).replace("searchJourneyForChange",str(searchJourney))
        start_urls.append(start_url)
    return start_urls
