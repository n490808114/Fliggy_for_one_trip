from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

cookies_list = str(input('Please input Cookies from internet!!!\n'))
cookies = {}
for line in cookies_list.split(';'):
    key, value = line.split('=', 1)
    cookies[key] = value
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get('https://sijipiao.fliggy.com/ie/flight_search.htm')
driver.add_cookie(cookies)
driver.get("https://sijipiao.fliggy.com/ie/flight_search_result.htm?searchBy=1278&b2g=0&formNo=-1&agentId=-1&needMemberPrice=true&searchJourney=%5B%7B%22depCityCode%22%3A%22MEL%22%2C%22arrCityCode%22%3A%22CGO%22%2C%22depCityName%22%3A%22%25E5%25A2%25A8%25E5%25B0%2594%25E6%259C%25AC%22%2C%22arrCityName%22%3A%22%25E9%2583%2591%25E5%25B7%259E%22%2C%22depDate%22%3A%222018-12-19%22%7D%2C%7B%22depCityCode%22%3A%22CGO%22%2C%22arrCityCode%22%3A%22MEL%22%2C%22depCityName%22%3A%22%25E9%2583%2591%25E5%25B7%259E%22%2C%22arrCityName%22%3A%22%25E5%25A2%25A8%25E5%25B0%2594%25E6%259C%25AC%22%2C%22depDate%22%3A%222018-12-26%22%7D%5D&childPassengerNum=0&infantPassengerNum=0&tripType=1&cardId=")
action = ActionChains(driver)
