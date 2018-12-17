import datetime  # 日期遍历
import random  # ksTS数字随机产生
import time
import urllib.parse


def get_start_urls(*args):
    # 接收起飞城市，抵达城市，开始日期，天数
    depCityCode,arrCityCode,start_date,search_for_each_week,times =args
    try:
        if start_date == '':
            start_date = datetime.datetime.now()
        else:
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    except:
        print("错误的日期，日期格式YYYY-MM-DD")
    

    # 声明start_urls
    start_urls = []
    start_url_head = "https://sijipiao.fliggy.com/ie/flight_search_result_poller.do?"
    for i in range(times):

        # 处理网址ksTS和callback部分
        tt0 = str(time.time()*1000)
        a = tt0.split(".")[0]
        tt1 = random.randint(0, 9999)
        b = str(tt1)
        c = str(tt1 + 1)

        # 处理网址searchJourney部分
        date = start_date + datetime.timedelta(days=i)
        if (search_for_each_week != '') and (str(date.weekday()+1) not in search_for_each_week):
            continue
        searchJourney = [{
            "arrCityCode": arrCityCode,
            "depCityCode": depCityCode,
            "depDate": date.strftime('%Y-%m-%d'),
            "selectedFlights": []
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
        start_url = start_url_head + urllib.parse.urlencode(data)
        start_urls.append(start_url)
    return start_urls
