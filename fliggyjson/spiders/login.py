from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import sys


def getCookies():
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome()
        #executable_path=r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver",
    driver.get()
    time.sleep(3)
    driver.get('https://login.taobao.com/member/login.jhtml')
    time.sleep(3)
    #driver.find_element_by_class_name('login-switch').click()
    # driver.find_element_by_xpath(
    #    '//*[@id="J_QRCodeLogin"]/div[5]/a[1]').click()
    #time.sleep(3)
    #driver.find_element_by_xpath(
    #    '//*[@id="TPL_username_1"]').send_keys('490808114@qq.com')
    #driver.find_element_by_xpath(
    #    '//*[@id="TPL_password_1"]').send_keys('Zzz8801668')
    #
    #
    #move_button = driver.find_element_by_xpath('//*[@id="nc_1_n1t"]')
    #
    #try:
    #    driver.find_element_by_xpath('//*[@id="nocaptcha"]').get_attribute('style')
    #except:
    #    print('不需要滑动模块')
    #    time.sleep(5)
    #else:
    #    print('需要滑动模块')
    #    # 初始化AtionChains()
    #    action = ActionChains(driver)
    #    # 鼠标移动到元素上，点击并hold
    #    action.move_to_element(move_button).click_and_hold().perform()
    #    # 移动鼠标(260,0)
    #    for i in range(1,300):
    #        action.move_by_offset(1, 0).perform()
    #        time.sleep(round(((round(i/300,4)**3)+round(i/150)),4))
    #    #action.move_by_offset(300, 0).perform()
    #
    #    time.sleep(1)
    #    # 释放鼠标
    #    action.release().perform()
    #    time.sleep(20)
    #finally:
    #    driver.find_element_by_xpath('//*[@id="J_SubmitStatic"]').click()
    #    time.sleep(2)
    # action.click_and_hold(move_button).perform()
    # action.drag_and_drop_by_offset(move_button,260,0).perform()
    # 鼠标移动操作在测试环境中比较常用到的场景是需要获取某元素的 flyover/tips，
    # 实际应用中很多 flyover 只有当鼠标移动到这个元素之后才出现，
    # 所以这个时候通过执行 moveToElement(toElement) 操作，
    # 就能达到预期的效果。但是根据我个人的经验，这个方法对于某些特定产品的图标，图像之类的 flyover/tips 也不起作用，
    # 虽然在手动操作的时候移动鼠标到这些图标上面可以出现 flyover, 但是当使用 WebDriver 来模拟这一移动操作时，虽然方法成功执行了，
    # 但是 flyover 却出不来。所以在实际应用中，还需要对具体的产品页面做相应的处理。

    time.sleep(20)

    
    
    cookies = {}
    #driver.get("https://i.taobao.com/my_taobao.htm")
    for elem in driver.get_cookies():
        cookies[elem['name']] = elem['value']
    if len(cookies) > 0:
        print("get Cookies Successful!!!")
    else:
        print("登陆失败")
        sys.exit()
    driver.close()
    driver.quit()
    return cookies
