import scrapy
import time  # time.sleep()
import re  # re.search()
import datetime  # 日期遍历
import codecs  # 存储response
import sys  # 重大错误退出
from ..items import FliggyjsonItem
from scrapy import Request
from scrapy import Selector

#getcookie()
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


class Fliggyjsonspider(scrapy.Spider):
    name = 'fliggyjson'
    allow_url = ['fliggy.com']

    # 接收起飞城市，抵达城市，开始日期，天数
    depCityCode = input("depCityCode?")
    arrCityCode = input("arrCityCode?")
    start_date = datetime.datetime.strptime(
        input("please input scrapy start date"), '%Y-%m-%d')
    times = int(input("how many days you want search?"))

    # 替换DEFAULT_REQUEST_HEADERS
    header = {
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0',
    }

    # 声明start_urls
    start_urls = []

    for i in range(times):

        # 处理网址ksTS和callback部分
        tt = str(time.time()*1000)
        a, b, c = (tt.split(".")[0], tt.split(".")[1],
                    str(round(eval(tt+'%1'),4)+0.0001).split(".")[1])

        # 处理网址searchJourney部分
        searchJourney = [{
            "depCityCode": depCityCode,
            "arrCityCode": arrCityCode,
            'depDate': (start_date + datetime.timedelta(days=i)).strftime('%Y-%m-%d'),
            'selectedFlights': []
        }]

        start_url0 = f'https://sijipiao.fliggy.com/ie/flight_search_result_poller.do?_ksTS='
        start_url1 = f'{a}_{b}&callback=jsonp{c}&supportMultiTrip=true&searchBy=1280'
        start_url2 = f'&childPassengerNum=0&infantPassengerNum=0&searchJourney={str(searchJourney)}'
        start_url3 = '&tripType=0&searchCabinType=0&agentId=-1&controller=1&searchMode=0&b2g=0&formNo=-1&cardId=&needMemberPrice='
        start_url = start_url0 + start_url1 + start_url2 + start_url3
        print(start_url)
        start_urls.append(start_url)
    print(start_urls)

    # 在url里面拿出来一个网址做登录测试

    
    test_url = start_urls.pop(0)
    response_test = Request(test_url, headers=header)
    cookies = {}
    # 如果得到的响应网址是login网址，那么就登录登录到网站上，获取cookie
    # 并用cookie再次获取响应，再次测试
    # 同时把cookie传给start_request()函数
    if bytes("login",encoding='utf-8') in response_test.body:
        cookies = getCookies()
    else:
        print("不用获取Cookies")
        start_urls.append(test_url)

        

    # 替换DEFAULT_REQUEST_HEADERS
    def start_requests(self):

        for url in self.start_urls:
            yield Request(url,
                            headers=self.header,
                            cookies=self.cookies,
                            callback=self.parse,
                            )

    def parse(self, response):
        items = []
        item = FliggyjsonItem()

        # 打印一下response,检验
        with codecs.open(f'{int(time.time()*1000)}.txt', 'wb', encoding='utf-8') as f:
            f.write(response.text)

        # 删除json1234()保留括号中间的字典字符串，然后把字符串转为字典
        site0 = re.search(r'json\d{,4}\((.*)\)', response.text).group()
        site1 = re.sub(r'{0:', r'{"0":', site0)
        site = eval(site1)

        # 打印一下格式,检验
        print(type(site))

        # 抓数据
        for i in range(10):
            print(site["data"]["flightItems"][i]
                    ["flightInfo"][0]["depAirlineCode"])
            if site["data"]["flightItems"][i]["flightInfo"][0]["depAirlineCode"] == 'JQ':
                item["depcity"] = site["data"]["flightItems"][i]["flightInfo"][0]["flightSegments"][0]["depCityCode"]
                item["arrcity"] = site["data"]["flightItems"][i]["flightInfo"][0]["flightSegments"][0]["arrCityCode"]
                item["depdate"] = site["data"]["flightItems"][i]["flightInfo"][0]["flightSegments"][0]["depTimeStr"].split(" ")[
                    0]
                item["price"] = site["data"]["flightItems"][i]["cardTotalPrice"]
                print(item)
                break
        print(item)
        items.append(item)

    def getCookies(self):
        # chrome_options = Options()
        # chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(
            executable_path=r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver",
        )

        time.sleep(3)
        driver.get('https://login.taobao.com/member/login.jhtml')
        time.sleep(3)
        driver.find_element_by_class_name('login-switch').click()
        # driver.find_element_by_xpath(
        #    '//*[@id="J_QRCodeLogin"]/div[5]/a[1]').click()

        time.sleep(3)
        driver.find_element_by_xpath(
            '//*[@id="TPL_username_1"]').send_keys('490808114@qq.com')
        driver.find_element_by_xpath(
            '//*[@id="TPL_password_1"]').send_keys('Zzz8801668')

        move_button = driver.find_element_by_xpath('//*[@id="nc_1_n1t"]')

        # 初始化AtionChains()
        action = ActionChains(driver)
        # 鼠标移动到元素上，点击并hold
        action.move_to_element(move_button).click_and_hold().perform()
        # 移动鼠标(260,0)
        action.move_by_offset(300, 0).perform()
        # 释放鼠标
        action.release().perform()
        time.sleep(0.5)

        # action.click_and_hold(move_button).perform()
        # action.drag_and_drop_by_offset(move_button,260,0).perform()
        # 鼠标移动操作在测试环境中比较常用到的场景是需要获取某元素的 flyover/tips，
        # 实际应用中很多 flyover 只有当鼠标移动到这个元素之后才出现，
        # 所以这个时候通过执行 moveToElement(toElement) 操作，
        # 就能达到预期的效果。但是根据我个人的经验，这个方法对于某些特定产品的图标，图像之类的 flyover/tips 也不起作用，
        # 虽然在手动操作的时候移动鼠标到这些图标上面可以出现 flyover, 但是当使用 WebDriver 来模拟这一移动操作时，虽然方法成功执行了，
        # 但是 flyover 却出不来。所以在实际应用中，还需要对具体的产品页面做相应的处理。

        driver.find_element_by_xpath('//*[@id="J_SubmitStatic"]').click()

        time.sleep(2)

        cookie = {}
        driver.get("https://i.taobao.com/my_taobao.htm")
        if '我的' in driver.title:
            for elem in driver.get_cookies():
                cookie[elem['name']] = elem['value']
            if len(cookie) > 0:
                print("get Cookies Successful!!!")
            else:
                print("登陆失败")
                sys.exit()
        return cookie

        driver.close()
        driver.quit()
