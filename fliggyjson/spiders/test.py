import time

def timecode():
    timecode = str(time.time()*1000)
    yield timecode[:13]
    yield timecode[14:]
    yield str(int(timecode[14:])+1)


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

# _ksTS={str(time.time()*1000)[:13]}_{str(time.time()*1000)[14:]}&callback=jsonp{str(int(str(time.time()*1000)[14:])+1)}
    
start_url = [f'https://sijipiao.fliggy.com/ie/flight_search_result_poller.do?&supportMultiTrip=true&searchBy=1280&childPassengerNum=0&infantPassengerNum=0&searchJourney={searchJourney}&tripType=0&searchCabinType=0&agentId=-1&controller=1&searchMode=0&b2g=0&formNo=-1&cardId=&needMemberPrice=']
print(start_url)