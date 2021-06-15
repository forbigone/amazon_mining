import requests
from lxml import etree
import pandas as pd
from pandas import DataFrame
import time
import re


def gethtml(url0, head):
    i = 0
    while i < 5:
        try:
            html = requests.get(url=url0, headers=head, timeout=(10, 20))
            repeat = 0
            while (html.status_code != 200):  # 错误响应码重试
                print('error: ', html.status_code)
                time.sleep(20 + repeat * 5)
                if (repeat < 5):
                    repeat += 1
                html = requests.get(url=url0, headers=head, timeout=(10, 20))
            return html
        except requests.exceptions.RequestException:
            print('超时重试次数: ', i + 1)
            time.sleep(1)
            i += 1
    raise Exception()




hea = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'downlink': '8',
    'ect': '4g',
    'rtt': '250',
    'Cookie': "session-id=134-0636042-0633818; session-id-time=2082787201l; i18n-prefs=USD; lc-main=zh_CN; sp-cdn=\"L5Z9:HK\"; x-wl-uid=1+h+8IhdF3lb3loyXLwiMOfz3PH6woTCuzvYabJv1d81BUtVw5TivYIXiDZAsh9cD2nneHGwuI88=; ubid-main=131-3884934-2925229; session-token=ZK8ZbeTD4tYIbKhfb3ovzTNSyFhCCiVB11MxESFEcen0QcGOLJsPZyJGuYVXhbc8UHxlfxi3jlhqH2/Vi1r5e5JUC6VtDJ3SYr1BHKeJ/ojd1NXXiFPsvhS6vfu4DLGXTLXp09O74a2y6RJ819FBo+te0ipxQIzfDGe8Zl4AJR1vUO6i0dyTc+SaewPDubDb; csm-hit=tb:X1TAAK5TV6CYS0QH19GC+s-V75NP7RDRN9BM9MW71CX|1594957493721&t:1594957493721&adb:adblk_no",
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
}

hea_0 = {
    # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    # 'accept-encoding': 'gzip, deflate, br',
    # 'accept-language': 'zh-CN,zh;q=0.9',
    # 'cache-control': 'max-age=0',
    'downlink': '1.5',
    'ect': '3g',
    'rtt': '300',
    # 'Cookie': "session-id=141-3132077-2152004; session-id-time=2082787201l; i18n-prefs=USD; lc-main=zh_CN; sp-cdn=\"L5Z9:CN\"; x-wl-uid=10tVwZ45eSXqIpeD5HaRaEZWh15W7H+vfi+XqqFlEGrT7tDZnDY5T/tN95e+9xgX+MWXBse7hC5A=; ubid-main=134-3335690-9399343; session-token=2+RCbdp4M2oj5rIKbi4cUwACUf85OmSwpSfM6Ivx6nA2Bi4hINPvjwpQy2IQvZxkN/xqDCLmTyBDTXaZxBGrEWhyHTEkhFb4He197smVmXFqsEIhF8GoSsCyJNctIJZWR1SJkbd/liAdOpkdAUYV59W+4xnXcq/ZJMQ0RkCkmis8aFuu7JKH6VmFoZv9QeIA; csm-hit=tb:G2VNCYGMS99K5WSAF3WK+s-M9HQ7RS4JN5SAWD8M20Z|1594365538625&t:1594365538625&adb:adblk_no",
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.8 Safari/537.36'
}

df = DataFrame({
    '类别': {},
    '排名': {},
    '照片链接': {},
    '商品链接': {},
    '标题': {},
    '星级': {},
    '评论数': {},
    '低价格': {},
    '高价格': {},

})

path = 'C:/myfile/project/amazon_mining/data/排名链接.csv'
df_type = list(pd.read_csv(path)['类别'])
df_link = list(pd.read_csv(path)['链接'])

for link in range(0,len(df_link)):
    time.sleep(2)
    for j in range(1,3):
        url0 = df_link[link]
        url1 = url0.split('ref=', 2)[0]
        url2 = "ref=zg_bs_pg_%s?_encoding=UTF8&pg=%s" % (str(j), str(j))
        url = url1 + url2
        print(url)
        req = gethtml(url, hea)
        html = etree.HTML(req.text)
        time.sleep(10)
        
    
        for i in range(0,50):
            z = i + (j-1)*50 + link*100  # 调整序号
            df.loc[z, '类别'] = df_type[link]
            a1 = html.xpath('//li[@class="zg-item-immersion"][%s]//span[@class="zg-badge-text"]/text()' %str(i+1))  # 50个
            if (len(a1) == 0):
                df.loc[z, '排名'] = '***'  # 有的链接前100名中并没有100个商品
                continue
            a2 = html.xpath('//li[@class="zg-item-immersion"][%s]//div[@class="a-section a-spacing-small"]/img/@src' %str(i+1))
            a3 = html.xpath('//li[@class="zg-item-immersion"][%s]//div[@class="a-section a-spacing-small"]/img/@alt' %str(i+1))
            a7 = html.xpath('//li[@class="zg-item-immersion"][%s]/span/div/span/a/@href' %str(i+1))
            if (len(a2) == 0 and len(a3) == 0):
                df.loc[z, '照片链接'] = '###'   # 有的商品有排名，但已经不存在 --- This item is no longer available
                df.loc[z, '标题'] = '###'
                continue
            a4 = html.xpath('//li[@class="zg-item-immersion"][%s]//span[@class="a-icon-alt"]/text()' %str(i+1))
            a5 = html.xpath('//li[@class="zg-item-immersion"][%s]//a[@class="a-size-small a-link-normal"]/text()' %str(i+1))
            a6 = html.xpath('//li[@class="zg-item-immersion"][%s]//span[@class="p13n-sc-price"]/text()' %str(i+1))
            a7 = html.xpath('//li[@class="zg-item-immersion"][%s]/span/div/span/a/@href' %str(i+1)) # 商品链接
            
            
            df.loc[z, '排名'] = a1[0]
            df.loc[z, '照片链接'] = a2[0]
            df.loc[z, '标题'] = a3[0]
            df.loc[z, '商品链接'] = "https://www.amazon.com/" + a7[0]
            
            if (len(a4) == 0):
                df.loc[z, '星级'] = 0
            else:
                if ('star' in a4[0]):
                    x_star = a4[0].split(' out', 2)[0]  # 提取星级数--英文
                    df.loc[z, '星级'] = x_star
                if ('星' in a4[0]):
                    x_star = re.findall(r".*平均 (.*) 星.*", a4[0])[0]  # 提取星级数--中文
                    df.loc[z, '星级'] = x_star
            if (len(a5) == 0):
                df.loc[z, '评论数'] = 0
            else:
                df.loc[z, '评论数'] = a5[0].replace(',', '')
    
    
            if (len(a6) == 2):
                df.loc[z, '低价格'] = a6[0]
                df.loc[z, '高价格'] = a6[1]
            elif(len(a6) == 1):
                df.loc[z, '低价格'] = a6[0]
                df.loc[z, '高价格'] = 0
            elif(len(a6) == 0):
                df.loc[z, '低价格'] = 0
                df.loc[z, '高价格'] = 0


path0 = 'C:/myfile/project/amazon_mining/data/排名.csv'
df.to_csv(path0, encoding='utf-8', index=False)  # 去掉index，保留头部