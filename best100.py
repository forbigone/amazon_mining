import requests
from lxml import etree
import pandas as pd
import time
import re
from pandas import DataFrame

def gethtml(url0,head):
    i = 0
    while i < 5:
        try:
            html = requests.get(url = url0, headers = head,timeout = (10, 20))
            repeat = 0
            while (html.status_code != 200):  # 错误响应码重试
                print('error: ', html.status_code)
                time.sleep(20 + repeat * 5)
                if (repeat < 5):
                    repeat += 1
                html = requests.get(url = url0, headers = head,timeout = (10, 20))
            return html
        except requests.exceptions.RequestException:
            print('超时重试次数: ', i + 1)
            time.sleep(1)
            i += 1
    raise Exception()


def get_link(url, hea):
    req = gethtml(url, hea)
    html = etree.HTML(req.text)
    type_link0 = html.xpath('//span[@class="zg_selected"]/../following-sibling::ul//a/@href')  # 排除上级
    type_text = html.xpath('//*[@id="zg_browseRoot"]//span/text()')
    end_link0 = html.xpath('//span[@class="zg_selected"]/../following-sibling::li[1]')  # 兄弟节点（之后）
    end_link1 = html.xpath('//span[@class="zg_selected"]/../preceding-sibling::li[1]')  # 兄弟节点（之前）
    if (len(end_link0) or len(end_link1)):
        end_link = 1
    else:
        end_link = 0
        if (len(type_link0) == 1):
            print('***********',type_text)
    time.sleep(10)
    return type_link0,type_text, end_link







url = 'https://www.amazon.com/-/zh/%E9%94%80%E5%94%AE%E6%8E%92%E8%A1%8C%E6%A6%9C-Home-Kitchen-%E5%AE%B6%E5%85%B7/zgbs/home-garden/1063306/ref=zg_bs_unv_hg_2_17873917011_3'

print(url)
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

type_link = []
type_text = []

type_link0,type_text0, end_link0 = get_link(url, hea)
if (end_link0 != 0):
    type_link.append(url)
    type_text.append(type_text0[0])
    print('新增：', type_text0[0])
else:
    for link1 in type_link0:  # 家具后 1 级-----卧室、客厅
        url = link1
        if (type_link0.index(link1) > 100):
            continue
        type_link1,type_text0, end_link0 = get_link(url, hea)
        print('第一级：', type_text0)
        if (end_link0 != 0):
            type_link.append(url)
            type_text.append(type_text0[0])
            print('新增：', type_text0[0])
            continue
        else:
            for link2 in type_link1:  # 家具后 2 级-----床、衣柜
                url = link2
                if (type_link1.index(link2) > 100):
                    continue
                type_link2,type_text0, end_link0 = get_link(url, hea)
                print('第二级：', type_text0)
                if (end_link0 != 0):
                    type_link.append(url)
                    type_text.append(type_text0[0])
                    print('新增：', type_text0[0])
                    continue
                else:
                    for link3 in type_link2:  # 家具后 3 级-----床头，床架
                        url = link3
                        if (type_link2.index(link3) > 100):
                            continue
                        type_link3,type_text0, end_link0 = get_link(url, hea)
                        print('第三级：', type_text0)
                        if (end_link0 != 0):
                            type_link.append(url)
                            type_text.append(type_text0[0])
                            print('新增：', type_text0[0])
                            continue
                        else:
                            for link4 in type_link3:  # 家具后 4 级-----Adjustable Bases、床板
                                url = link4
                                if (type_link3.index(link4) > 100):
                                    continue
                                type_link4,type_text0, end_link0 = get_link(url, hea)
                                print('第四级：', type_text0)
                                if (end_link0 != 0):
                                    type_link.append(url)
                                    type_text.append(type_text0[0])
                                    print('新增：', type_text0[0])
                                    continue
                                else:
                                    for link5 in type_link4:  # 家具后 5 级-----Adjustable Bases、床板
                                        url = link5
                                        if (type_link4.index(link5) > 100):
                                            continue
                                        type_link5,type_text0, end_link0 = get_link(url, hea)
                                        print('第五级：', type_text0)
                                        if (end_link0 != 0):
                                            type_link.append(url)
                                            type_text.append(type_text0[0])
                                            print('新增：', type_text0[0])
                                            continue
                                        else:
                                            for link6 in type_link5:  # 家具后 6 级-----Adjustable Bases、床板
                                                url = link6
                                                if (type_link5.index(link6) > 100):
                                                    continue
                                                type_link6,type_text0, end_link0 = get_link(url, hea)
                                                print('第六级：', type_text0)
                                                if (end_link0 != 0):
                                                    type_link.append(url)
                                                    type_text.append(type_text0[0])
                                                    print('新增：', type_text0[0])
                                                    continue







df = DataFrame({
    '类别': type_text,
    '链接': type_link    

})

path0 = 'C:/myfile/project/amazon_mining/data/排名链接.csv'
df.to_csv(path0, encoding='utf-8', index=False)  # 去掉index，保留头部
'''
type_list = []
type_link = []
num0 = 2
type_link0, type_text = get_link(url, hea, num0)
time.sleep(5)
a0 = re.findall(r".*www.amazon.com/(.*)/zgbs.*", type_link0[1])[0]

result =  end_link(a0, type_link0, type_text, hea, num0)
time.sleep(3)
if (result == 0):
    num0 += 1
    
    for link1 in type_link0:
        type_link1, type_text = get_link(link1, hea, num0)
        time.sleep(5)
        a0 = re.findall(r".*www.amazon.com/(.*)/zgbs.*", type_link0[1])[0]

        result = end_link(a0, type_link1, type_text, hea, num0)
        time.sleep(3)
        
        if (result == 0):
            num0 += 1
        else:
            type_list.extend(type_text)
            type_link.extend(type_link0)
            

else:
    type_list.extend(type_text)
    type_link.extend(type_link0)


print(type_list)
print(type_link)
'''

'''
url1 = 'https://www.amazon.com/-/zh/%E9%94%80%E5%94%AE%E6%8E%92%E8%A1%8C%E6%A6%9C-Home-Kitchen-%E5%AE%B6%E5%85%B7/zgbs/home-garden/1063306/ref=zg_bs_unv_hg_2_17873917011_3'
url2 = 'https://www.amazon.com/-/zh/%E9%94%80%E5%94%AE%E6%8E%92%E8%A1%8C%E6%A6%9C-Home-Kitchen-%E5%8D%A7%E5%AE%A4%E5%AE%B6%E5%85%B7/zgbs/home-garden/1063308/ref=zg_bs_nav_hg_2_1063306'
url3 = 'https://www.amazon.com/-/zh/%E9%94%80%E5%94%AE%E6%8E%92%E8%A1%8C%E6%A6%9C-Home-Kitchen-%E6%95%B4%E4%BD%93%E5%BA%8A%E5%8F%8A%E7%BB%84%E4%BB%B6/zgbs/home-garden/3733101/ref=zg_bs_nav_hg_3_1063308'
url4 = 'https://www.amazon.com/-/zh/%E9%94%80%E5%94%AE%E6%8E%92%E8%A1%8C%E6%A6%9C-Home-Kitchen-Bed-Bases-Foundations/zgbs/home-garden/17873917011/ref=zg_bs_nav_hg_4_3733101'
url5 = 'https://www.amazon.com/-/zh/%E9%94%80%E5%94%AE%E6%8E%92%E8%A1%8C%E6%A6%9C-Home-Kitchen-Adjustable-Bed-Bases/zgbs/home-garden/17873919011/ref=zg_bs_nav_hg_5_17873917011'

num = 0
req1,type_text1, end_link1 = get_link(url1, hea, num)
time.sleep(1)
num += 1
req2,type_text2, end_link2 = get_link(url2, hea, num)
time.sleep(1)
num += 1
req3,type_text3, end_link3 = get_link(url3, hea, num)
time.sleep(1)
num += 1
req4,type_text4, end_link4 = get_link(url4, hea, num)
time.sleep(1)
num += 1
req5,type_text5, end_link5 = get_link(url5, hea, num)
'''







