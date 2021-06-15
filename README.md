# amazon_mining
爬取亚马逊所有家具种类销售排行榜前100名的商品排名信息，包括排名、照片链接、商品链接、标题、星级、评论数、最低价格和最高价格
# 目标
亚马逊公司（Amazon），是美国最大的一家网络电子商务公司，位于华盛顿州的西雅图，是网络上最早开始经营电子商务的公司之一，现在已成为全球商品品种最多的网上零售商和全球第二大互联网企业。

本次目标是爬取亚马逊**所有家具种类**销售排行榜前100名的商品排名信息。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210613185349904.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3lvdV9qdXN0X2xvb2s=,size_16,color_FFFFFF,t_70)
[上一篇博客](https://blog.csdn.net/you_just_look/article/details/117856617)已经把所有家具种类，以及种类页面链接爬取出来

接下来是根据这些种类链接，分析页面HTML，得到该家具种类前100名商品的排名、照片链接、商品链接、标题、星级、评论数、最低价格和最高价格
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210614235150185.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3lvdV9qdXN0X2xvb2s=,size_16,color_FFFFFF,t_70)


```

## 代码简要解析

```python
def gethtml(url0,head)
```

> gethtml函数是为了得到静态页面HTML，有对页面反应超时的情况做了些延时处理



# 结果
得到所有家具种类前100名的商品信息

![在这里插入图片描述](https://img-blog.csdnimg.cn/20210615171453987.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3lvdV9qdXN0X2xvb2s=,size_16,color_FFFFFF,t_70)
