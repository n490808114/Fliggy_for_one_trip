from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import logging
from selenium.common.exceptions import UnexpectedAlertPresentException


def getCookies():
    cookies = []
    driver = webdriver.Chrome(
        executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver")

    time.sleep(3)
    driver.get('https://login.taobao.com/member/login.jhtml')
    time.sleep(3)
    driver.find_element_by_xpath(
        '//*[@id="J_QRCodeLogin"]/div[5]/a[1]').click()

    time.sleep(3)
    user = driver.find_element_by_xpath('//*[@id="TPL_username_1"]')
    user.send_keys('490808114@qq.com')
    password = driver.find_element_by_xpath('//*[@id="TPL_password_1"]')
    password.send_keys('Zzz8801668')

    move_button = driver.find_element_by_xpath('//*[@id="nc_1_n1z"]')
    
    # 初始化AtionChains()
    action = ActionChains(driver)
    # 鼠标移动到元素上，点击并hold
    action.move_to_element(move_button).click_and_hold().perform()
    # 移动鼠标(260,0)
    action.move_by_offset(260, 0).perform()
    # 释放鼠标
    action.release().perform()

    # action.click_and_hold(move_button).perform()
    # action.drag_and_drop_by_offset(move_button,260,0).perform()
    # 鼠标移动操作在测试环境中比较常用到的场景是需要获取某元素的 flyover/tips，
    # 实际应用中很多 flyover 只有当鼠标移动到这个元素之后才出现，
    # 所以这个时候通过执行 moveToElement(toElement) 操作，
    # 就能达到预期的效果。但是根据我个人的经验，这个方法对于某些特定产品的图标，图像之类的 flyover/tips 也不起作用，
    # 虽然在手动操作的时候移动鼠标到这些图标上面可以出现 flyover, 但是当使用 WebDriver 来模拟这一移动操作时，虽然方法成功执行了，
    # 但是 flyover 却出不来。所以在实际应用中，还需要对具体的产品页面做相应的处理。

    time.sleep(3)
    commit = driver.find_element_by_xpath('//*[@id="J_SubmitStatic"]')

    commit.click()
    time.sleep(3)

    cookie = {}
    if '我的' in driver.title:
        for elem in driver.get_cookies():
            cookie[elem['name']] = elem['value']
#        if len(cookie) >0:
#            logger = logging.getLogger(__name__)
#            logger.warning(f"get Cookies Successful:{user}")
    return cookies
    driver.close()
    driver.quit()


cookies = getCookies()
print(cookies)
