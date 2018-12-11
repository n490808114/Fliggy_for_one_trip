import urllib.parse
import re
str0 = 'https://sijipiao.fliggy.com/ie/flight_search_result_poller.do?_ksTS=1544506579892_2201&callback=jsonp2202&supportMultiTrip=True&searchBy=1281&childPassengerNum=0&infantPassengerNum=0&searchJourney=%5B%7B%27arrCityCode%27%3A+%27MEL%27%2C+%27depCityCode%27%3A+%27CGO%27%2C+%27depDate%27%3A+%272018-12-21%27%2C+%27selectedFlights%27%3A+%5B%5D%7D%5D&tripType=0&searchCabinType=0&agentId=-1&controller=1&searchMode=0&b2g=0&formNo=-1&cardId=None&needMemberPrice=None'
r = re.search(r"depCityCode%27%3A\+%27(\w{3})%27%2C",str0).group(1)
print(r)