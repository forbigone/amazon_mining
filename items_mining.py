import requests
from lxml import etree
import pandas as pd
import time
import re

import openpyxl
from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def gethtml(url0,head):
    i = 0
    while i < 5:
        try:
            html = requests.get(url = url0, headers = head,timeout = (10, 20))
            repeat = 0
            while (html.status_code != 200):  # 错误响应码重试
                print('error: ', html.status_code)
                time.sleep(20 + repeat * 5)
                repeat += 1
                html = requests.get(url = url0, headers = head,timeout = (10, 20))
                if (html.status_code != 200 and repeat == 2):
                    return html,repeat
            return html,repeat
        except requests.exceptions.RequestException:
            print('超时重试次数: ', i + 1)
            i += 1
    raise Exception()


def get_x_follow_link(url_follow,head):
    req, repeat = gethtml(url_follow, head)
    #req.encoding='UTF-8'
    html = etree.HTML(req.text)
    x_follow_link = ''
    x_follow_link0 = html.xpath('//*[@id="olpOfferList"]//div/h3/span/a')  # 文本
    x_follow_link1 = html.xpath('//*[@id="olpOfferList"]//div/h3/a/img')  # 图片
    for photo in x_follow_link1:
        x_follow_link += 'Amazon'
        x_follow_link += '-'
    for link in x_follow_link0:
        x_follow_link += link.text
        x_follow_link += '-'
    x_follow_link = x_follow_link[0:-1]
    return x_follow_link


def get_price(html):
    x_price = html.xpath('//span[@id="priceblock_saleprice"]/text()')  # 价格
    if (len(x_price) == 0):
        x_price0 = html.xpath('//span[@id="priceblock_ourprice"]/text()')  # 美国价格
        if (len(x_price0) == 0):
            x_price = 0
        else:
            x_price = x_price0[0]
    else:
        x_price = x_price[0]
    x_price = str(x_price)
    x_price = x_price.replace(',', '.')  # 部分价格有逗号,
    return x_price


def change_address(postal):
    while True:
        try:
            driver.find_element_by_id('glow-ingress-line1').click()
            # driver.find_element_by_id('nav-global-location-slot').click()
            time.sleep(2)
        except Exception as e:
            driver.refresh()
            time.sleep(10)
            continue
        try:
            driver.find_element_by_id("GLUXChangePostalCodeLink").click()
            time.sleep(2)
        except:
            pass
        try:
            driver.find_element_by_id('GLUXZipUpdateInput').send_keys(postal)
            time.sleep(1)
            break
        except Exception as NoSuchElementException:
            try:
                driver.find_element_by_id('GLUXZipUpdateInput_0').send_keys(postal.split('-')[0])
                time.sleep(1)
                driver.find_element_by_id('GLUXZipUpdateInput_1').send_keys(postal.split('-')[1])
                time.sleep(1)
                break
            except Exception as NoSuchElementException:
                driver.refresh()
                time.sleep(10)
                continue
        print("重新选择地址")
    driver.find_element_by_id('GLUXZipUpdate').click()
    time.sleep(1)
    driver.refresh()
    time.sleep(3)


def get_items(req, hea, hea_0):
    if (type(req) == str):
        html = etree.HTML(req)  # 美国返回文本html
    else:
        html = etree.HTML(req.text)
    
    
    local = html.xpath('//a[@class="nav-a nav-a-2 a-popover-trigger a-declarative"]//span[@class="nav-line-2"]/text()')
    print('收件地址: ', local)
    x_price = get_price(html)
    print('价格: ', x_price)
    if ('￥' in x_price):
        z_price = re.sub("\D", "", x_price)  # 日本价格存在小数点
    else:
        z_price = re.findall(r"\d+\.?\d*", x_price)[0]  # 只保留数字和小数点
    print('处理后的价格： ', z_price)

    if ('USD' in x_price or 'GBP' in x_price):  # 根据返回价格情况，调用不同的header
        print('----------USD and GBP------------')
        req0, repeat = gethtml(url, hea_0)
        html = etree.HTML(req0.text)
        x_price = get_price(html)
    try:
        x_star0 = html.xpath('//div[@id="averageCustomerReviews_feature_div"]//span[@id="acrPopover"]/@title')[0]  # 星级
    except:
        x_text0 = html.xpath('//div[@id="featurebullets_feature_div"]//ul//span[@class="a-list-item"]/text()')  # 利用都有的五点描述来区分出某些没评论的商品
        x_text = int(bool(len(x_text0)))
        print('五点描述: ', x_text)
        if (x_text):
            x_star = 0
            x_rate = 0
            print('星级: ', x_star)
            print('评论总数: ', x_rate)
            x_follow0 = html.xpath('//div[@id="olp_feature_div"]//a[@class="a-link-normal"]/text()')  # 跟卖检查
            if (len(x_follow0)):
                x_follow_url = url.split('/dp/', 2)[0] + \
                               html.xpath('//div[@id="olp_feature_div"]//a[@class="a-link-normal"]/@href')[0]
                x_follow = get_x_follow_link(x_follow_url, hea)
            else:
                x_follow = 0
            print('跟卖检查: ', x_follow)
            x_a0 = html.xpath('//div[@id="aplus3p_feature_div"]//div[@class="aplus-v2 desktop celwidget"]')  # A+页是否存在
            x_a = int(bool(len(x_a0)))
            print('A+页是否存在: ', x_a)
            # 大小类排名
            rank_big0 = html.xpath('//div[@id="product-details-grid_feature_div"]//td[contains(text(),"(")]')  # 英文
            if (len(rank_big0) > 0):
                rank_len = len(rank_big0)
                rank_del = []
                for rank_i in range(0, rank_len):
                    if ('g' in rank_big0[rank_i].text or 'unset' in rank_big0[rank_i].text):  # 排除重量Kg后也有括号
                        rank_del.append(rank_i)
                for del0 in rank_del:
                    del rank_big0[del0]
                rank_big1 = html.xpath(
                    '//div[@id="product-details-grid_feature_div"]//span[contains(text(),"(")]')  # 中文
                if (len(rank_big0) == 0 and len(rank_big1) == 0):
                    rank_big0 = 0
                else:
                    if (len(rank_big1) == 0):
                        rank_big0 = rank_big0[-1].text  # 排除unset
                    else:
                        rank_big0 = rank_big1[-1].text
            else:
                rank_big0 = html.xpath(
                    '//div[@id="product-details-grid_feature_div"]//span[contains(text(),"(")]')  # 中文
                if (len(rank_big0) == 0):
                    rank_big1 = html.xpath(
                        '//div[@id="detail-bullets_feature_div"]//li[@id="SalesRank"]/text()[2]')  # 西班牙文--情况1
                    if (len(rank_big1) == 0):
                        rank_big1 = html.xpath(
                            '//div[@class="wrapper ESlocale"]//td[contains(text(),"(")]')  # 西班牙文--情况2
                        if (len(rank_big1) == 0):
                            rank_big1 = html.xpath('//div[@style="overflow:hidden;"]//td[contains(text(),"(")]')  # 加拿大
                            if (len(rank_big1) != 0 and 'unset' in rank_big1[0].text):  # 排除重量Kg后也有括号
                                del rank_big1[0]
                            if (len(rank_big1) == 0):
                                rank_big1 = html.xpath(
                                    '//div[@id="detail_bullets_id"]//li[@id="SalesRank"]/text()[2]')  # 日本(与西班牙1类似)
                                if (len(rank_big1) == 0):
                                    rank_big1 = html.xpath(
                                        '//div[@id="productDetails_feature_div"]//span[contains(text(),"(")]')  # 美国
                                    if (len(rank_big1) == 0):
                                        rank_big0 = 0
                                    else:
                                        rank_big0 = rank_big1[0].text
                                else:
                                    rank_big0 = str(rank_big1[0])  # 这不需要加text
                            else:
                                rank_big0 = rank_big1[0].text
                        else:
                            rank_big0 = rank_big1[0].text
                    else:
                        rank_big0 = str(rank_big1[0])  # 这不需要加text
                    if (len(rank_big1) == 0):
                        rank_big0 = 0
                else:
                    rank_big0 = rank_big0[0].text
            if (rank_big0 == 0):  # 有部分商品没有排名
                rank_big_num = 0
                rank_big_type = 0
            else:
                rank_big_num = re.sub("\D", "", rank_big0)  # 提取数字
                rank_big_type = re.findall(r".*in (.*) \(.*", rank_big0) + re.findall(r".*名(.*) \(.*", rank_big0) + re.findall(r".*en (.*) \(.*", rank_big0) + re.findall(r".*\n(.*) -.*", rank_big0)  # 英文括号需要转义\，中文匹配和英文匹配相加
            print('排名: ', rank_big_num)
            print('排名类型: ', rank_big_type[0])
            x_bad = 0
            print('主页是否有差评: ', x_bad)
            return (x_star, x_rate, x_price, x_follow, x_text, x_a, rank_big_num, rank_big_type, x_bad)
        else:
            return ('', '', '', '', '', '', '', '', '')
    if ('颗星' in x_star0):
        x_star = x_star0.split(' 颗星', 2)[0]  # 提取星级数--中文
    if ('star' in x_star0):
        x_star = x_star0.split(' out', 2)[0]  # 提取星级数--英文
    if ('von' in x_star0):
        x_star = x_star0.split(' von', 2)[0].replace(',', '.')  # 提取星级数--德文
    if ('sur' in x_star0):
        x_star = x_star0.split(' sur', 2)[0].replace(',', '.')  # 提取星级数--法文
    if ('su' in x_star0):
        x_star = x_star0.split(' su', 2)[0].replace(',', '.')  # 提取星级数--意大利文
    if ('de' in x_star0):
        x_star = x_star0.split(' de', 2)[0].replace(',', '.')  # 提取星级数--西班牙文
    if ('つ星' in x_star0):
        x_star = x_star0.split('うち', 2)[1]  # 提取星级数--日文
    # 法文中逗号代表点
    print('星级: ', x_star)
    x_rate0 = html.xpath('//div[@id="averageCustomerReviews_feature_div"]//span[@id="acrCustomerReviewText"]/text()')[0]  # 评论总数
    x_rate = re.sub("\D", "", x_rate0)
    print('评论总数: ', x_rate)

    x_follow0 = html.xpath('//div[@id="olp_feature_div"]//a[@class="a-link-normal"]/text()')  # 跟卖检查
    if (len(x_follow0)):
        x_follow_url = url.split('/dp/', 2)[0] + \
                       html.xpath('//div[@id="olp_feature_div"]//a[@class="a-link-normal"]/@href')[0]
        x_follow = get_x_follow_link(x_follow_url, hea)
    else:
        x_follow = 0
    print('跟卖检查: ', x_follow)
    x_text0 = html.xpath('//div[@id="featurebullets_feature_div"]//ul//span[@class="a-list-item"]/text()')  # 五点描述
    x_text = int(bool(len(x_text0)))
    print('五点描述: ', x_text) # 0表示缺失
    x_a0 = html.xpath('//div[@id="aplus3p_feature_div"]//div[@class="aplus-v2 desktop celwidget"]')  # A+页是否存在
    x_a = int(bool(len(x_a0)))
    print('A+页是否存在: ', x_a) # 0表示缺失
    # 大小类排名
    rank_big0 = html.xpath('//div[@id="product-details-grid_feature_div"]//td[contains(text(),"(")]')  # 英文
    if (len(rank_big0) > 0):
        rank_len = len(rank_big0)
        rank_del = []
        for rank_i in range(0, rank_len):
            if ('g' in rank_big0[rank_i].text or 'unset' in rank_big0[rank_i].text):  # 排除重量Kg后也有括号
                rank_del.append(rank_i)
        for del0 in rank_del:
            del rank_big0[del0]
        rank_big1 = html.xpath('//div[@id="product-details-grid_feature_div"]//span[contains(text(),"(")]')  # 中文
        if (len(rank_big0) == 0 and len(rank_big1) == 0):
            rank_big0 = 0
        else:
            if (len(rank_big1) == 0):
                rank_big0 = rank_big0[-1].text  # 排除unset
            else:
                rank_big0 = rank_big1[-1].text
    else:
        rank_big0 = html.xpath('//div[@id="product-details-grid_feature_div"]//span[contains(text(),"(")]')  # 中文
        if (len(rank_big0) == 0):
            rank_big1 = html.xpath('//div[@id="detail-bullets_feature_div"]//li[@id="SalesRank"]/text()[2]')  # 西班牙文--情况1
            if (len(rank_big1) == 0):
                rank_big1 = html.xpath('//div[@class="wrapper ESlocale"]//td[contains(text(),"(")]')  # 西班牙文--情况2
                if (len(rank_big1) == 0):
                    rank_big1 = html.xpath('//div[@style="overflow:hidden;"]//td[contains(text(),"(")]')  # 加拿大
                    if (len(rank_big1) != 0 and 'unset' in rank_big1[0].text):  # 排除重量Kg后也有括号
                        del rank_big1[0]
                    if (len(rank_big1) == 0):
                        rank_big1 = html.xpath('//div[@id="detail_bullets_id"]//li[@id="SalesRank"]/text()[2]')  # 日本(与西班牙1类似)
                        if (len(rank_big1) == 0):
                            rank_big1 = html.xpath('//div[@id="productDetails_feature_div"]//span[contains(text(),"(")]')  # 美国
                            if (len(rank_big1) == 0):
                                rank_big0 = 0
                            else:
                                print('------美国------')
                                rank_big0 = rank_big1[0].text
                        else:
                            print('------ 日本(与西班牙1类似)------')
                            rank_big0 = str(rank_big1[0])  # 这不需要加text
                    else:
                        print('------ 加拿大------')
                        rank_big0 = rank_big1[0].text
                else:
                    print('------ 西班牙文--情况2------')
                    rank_big0 = rank_big1[0].text
            else:
                print('------ 西班牙文--情况1------')
                rank_big0 = str(rank_big1[0])  # 这不需要加text
            if (len(rank_big1) == 0):
                rank_big0 = 0
        else:
            print('------ 中文------')
            rank_big0 = rank_big0[0].text
    if (rank_big0 == 0):  # 有部分商品没有排名
        rank_big_num = 0
        rank_big_type = 0
    else:
        rank_big_num = re.sub("\D", "", rank_big0)  # 提取数字
        rank_big_type = re.findall(r".*in (.*) \(.*", rank_big0) + re.findall(r".*名(.*) \(.*", rank_big0) + re.findall(
            r".*en (.*) \(.*", rank_big0) + re.findall(r".*\n(.*) -.*", rank_big0)  # 英文括号需要转义\，中文匹配和英文匹配相加
    print('排名: ', rank_big_num)
    if (type(rank_big_type) == list):
        print('排名类型: ', rank_big_type[0])
    else:
        print('排名类型: ', rank_big_type)
   

    x_bad0 = html.xpath('//div[@class="a-section global-reviews-content celwidget"]//span[@class="a-icon-alt"]/text()')  # 主页是否有差评，存在小于5星
    x_bad0_top = html.xpath('//div[@class="a-section review aok-relative"]//span[@class="a-icon-alt"]/text()')  # 主页是否有差评，存在小于5星
    if (len(x_bad0_top) > 8):  # 部分商品有top评价，主页面最多显示8个
        x_bad0.extend(x_bad0_top[0:8])
    elif (len(x_bad0_top) <= 8 and len(x_bad0_top) > 0):
        x_bad0.extend(x_bad0_top)
    x_bad_list = ['']
    for i in x_bad0:
        if ('颗星' in i):
            x_bad_list.append(i.split(' 颗星', 2)[0])  # 提取星级数
        if ('star' in i):
            x_bad_list.append(i.split(' out', 2)[0])  # 提取星级数
        if ('von' in i):
            x_bad_list.append(i.split(' von', 2)[0].replace(',', '.'))  # 提取星级数
        if ('su' in i):
            x_bad_list.append(i.split(' su', 2)[0].replace(',', '.'))  # 提取星级数
        if ('de' in i):
            x_bad_list.append(i.split(' de', 2)[0].replace(',', '.'))  # 提取星级数
        if ('つ星' in i):
            x_bad_list.append(i.split('うち', 2)[1].replace(',', '.'))  # 提取星级数
    x_bad_list = [x for x in x_bad_list if x != '']  # 去除空值
    x_bad = 0
    for i in x_bad_list:
        if (i != '5.0'):  # 出现不为5星的都视为差评
            x_bad += 1
    x_bad = str(x_bad)
    print('主页是否有差评: ', x_bad) # 0表示缺失

    return (x_star, x_rate, x_price, x_follow, x_text, x_a, rank_big_num, rank_big_type, x_bad)



# 数据导入
url_list = ['http://www.amazon.com/dp/B07ZV21JVK?ref=myi_title_dp',  # 美国
            'http://www.amazon.co.uk/dp/B0774JBR84?ref=myi_title_dp',  # 英国
            'http://www.amazon.de/dp/B07ZQ2DGND?ref=myi_title_dp',  # 德国
            'http://www.amazon.fr/dp/B077DVM4LH?ref=myi_title_dp',  # 法国
            'http://www.amazon.it/dp/B07DJ43SM1?ref=myi_title_dp',  # 意大利
            'http://www.amazon.es/dp/B07ZQ1BWJP?ref=myi_title_dp',  # 西班牙
            #'http://www.amazon.co.jp/dp/B07PYRY8V3?ref=myi_title_dp', # 日本
            ]
# url = 'http://www.amazon.co.jp/dp/B07DZWTQJM?ref=myi_title_dp'



hea = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'downlink': '8',
    'ect': '4g',
    'rtt': '250',
    'Cookie': "session-id=257-3500989-3695223; i18n-prefs=GBP; ubid-acbuk=257-5950834-2508848; x-wl-uid=1bEcLG2b03/1tAwPJNyfuRH+U7J9ZaPYejSBR4HXKuYQPJtLhQbDYyO/GOMypGKXqZrG7qBkS0ng=; session-token=x04EF8doE84tE+6CXYubsjmyob/3M6fdmsQuqzD0jwl/qGdO5aRc2eyhGiwoD0TFzK1rR/yziHsDS4v6cdqT2DySFXFZ9I5OHEtgufqBMEyrA0/Scr87KKA+GWOjfVmKRuPCqOGaixZQ6AIjU3e2iFOdM+3v90NeXFI3cazZcd6x9TYCy9b5u9V8zR7ePbdP; session-id-time=2082758401l; csm-hit=tb:MAA188S1G57TNTH6HQCZ+s-T9EGT4C8FC8J74X5T7CY|1594212767446&t:1594212767446&adb:adblk_no",
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}

hea_0 = {
        #'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        #'accept-encoding': 'gzip, deflate, br',
        #'accept-language': 'zh-CN,zh;q=0.9',
        #'cache-control': 'max-age=0',
        'downlink': '1.5',
        'ect': '3g',
        'rtt': '300',
        #'Cookie': "session-id=141-3132077-2152004; session-id-time=2082787201l; i18n-prefs=USD; lc-main=zh_CN; sp-cdn=\"L5Z9:CN\"; x-wl-uid=10tVwZ45eSXqIpeD5HaRaEZWh15W7H+vfi+XqqFlEGrT7tDZnDY5T/tN95e+9xgX+MWXBse7hC5A=; ubid-main=134-3335690-9399343; session-token=2+RCbdp4M2oj5rIKbi4cUwACUf85OmSwpSfM6Ivx6nA2Bi4hINPvjwpQy2IQvZxkN/xqDCLmTyBDTXaZxBGrEWhyHTEkhFb4He197smVmXFqsEIhF8GoSsCyJNctIJZWR1SJkbd/liAdOpkdAUYV59W+4xnXcq/ZJMQ0RkCkmis8aFuu7JKH6VmFoZv9QeIA; csm-hit=tb:G2VNCYGMS99K5WSAF3WK+s-M9HQ7RS4JN5SAWD8M20Z|1594365538625&t:1594365538625&adb:adblk_no",
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.8 Safari/537.36'
    }




# 启动并初始化webdriver
options = webdriver.ChromeOptions()  # 初始化Chrome
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument("disable-web-security")
options.add_argument('disable-infobars')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
#driver = webdriver.Chrome(executable_path = '/home/spider2/chromedriver', chrome_options=options)
driver = webdriver.Chrome(chrome_options=options)
wait = WebDriverWait(driver, 20)

driver.maximize_window()
row = 2

search_page_url = 'https://www.amazon.com/s?k=basketball'
postal = "20237"  # 华盛顿
print("正在爬取初始页面", search_page_url)
try:
    driver.get(search_page_url)
except Exception as e:
	driver.quit()
	print (e)
	raise  # raise语句也可以不带参数，此时按原错误信息抛出。//raise MyError('invalid value: %s' % s)    
time.sleep(2)

change_address(postal)  # 更改邮寄地址

wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-result-list")))


for url in url_list:
    print(url)
    time.sleep(5)
    if('.com' in url):  # 用selenium 浏览器爬取
        
        js = 'window.open("' + url + '&language=en_US");'
        driver.execute_script(js)
    
        # 网页窗口句柄集
        handles = driver.window_handles
        # 进行网页窗口切换
        driver.switch_to.window(handles[-1])
    
        page_source = driver.page_source
        y_star, y_rate, y_price, y_follow, y_text, y_a, y_rank_big_num, y_rank_big_type, y_bad = get_items(driver.page_source, hea, hea_0)
        time.sleep(1)
    
        driver.close()
        driver.switch_to.window(handles[0])
    else:
        req, error = gethtml(url, hea)  # 默认header
        #req.encoding='UTF-8'
        y_star, y_rate, y_price, y_follow, y_text, y_a, y_rank_big_num, y_rank_big_type, y_bad = get_items(req, hea, hea_0)


driver.quit()  # 关闭浏览器


