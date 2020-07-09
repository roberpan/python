# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
import re
import math

class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['bj.lianjia.com']
    start_urls =[]
    file='gardeninfo.csv'
    ids=pd.read_csv(file).drop(['Unnamed: 0'],axis=1)['id']
    len=len(ids)
    for id in ids[1000:len]:
        #id=ids[0]
        url='https://bj.lianjia.com/ershoufang/c{}/'.format(id)
        start_urls.append(url)

    # 以下代码实现根据已掌握的8000多个小区实现对每个小区房源信息抓取
    def parse(self, response):
        count = int(response.css('h2.total.fl span::text').extract_first())
        page = math.ceil(count / 30)
        if page!=0:
            for i in range(page):
                new_url=response.url+'pg{}'.format(i+1)
                yield scrapy.Request(url=new_url,callback=self.page_parse)

    def page_parse(self,response):
        urls = []
        contents = response.css('div.info.clear')
        for content in contents:
            url = content.css('.title a::attr(href)').extract_first()
            urls.append(url)
        for el in urls:
            yield scrapy.Request(url=el, callback=self.house_parse)

    def house_parse(self,response):
        item = {}
        df = pd.DataFrame(
            columns=('total_price', 'unit_price', 'roomtype', 'height', 'direction', 'decorate', 'area', 'age'
                     , 'garden', 'district', 'id'))
        item['total_price'] = response.css('.total::text').extract_first() + '万'
        item['unit_price'] = response.css('span.unitPriceValue::text').extract_first()
        # 获取房屋信息，如房型、层高、朝向、装修情况、面积、楼龄
        item['roomtype'] = response.css('.mainInfo::text').extract()[0]
        item['height'] = response.css('.subInfo::text').extract()[0]
        item['direction'] = response.css('.mainInfo::text').extract()[1]
        item['decorate'] = response.css('.subInfo::text').extract()[1]
        item['area'] = response.css('.mainInfo::text').extract()[2]
        item['age'] = re.sub("\D", "", response.css('.subInfo::text').extract()[2])
        # 获取房源所在小区、地区、环线等信息
        item['garden'] = response.css('.info::text').extract()[0]
        item['district'] = response.css('.info a::text').extract()[0]
        # 获取房源编号
        item['id'] = re.sub("\D", "", response.css('.houseRecord span::text').extract()[1])  # 通过正则方式把字符串中的数字提取出来
        # 用append方法向DataFrame中添加字典数据，注意在未设置DataFrame列名的情况下不能直接添加字典数据，会报错
        df = df.append(item, ignore_index=True)
        df.to_csv('content1.csv', mode='a', header=False)

#以下代码实现对链家主页3000条数据抓取
'''def parse(self, response):
        urls=[]
        contents = response.css('div.info.clear')
        for content in contents:
            url = content.css('.title a::attr(href)').extract_first()
            urls.append(url)
        for el in urls:
            yield scrapy.Request(url=el, callback=self.new_parse)

    def new_parse(self,response):
        item = {}
        df=pd.DataFrame(columns=('total_price','unit_price','roomtype','height','direction','decorate','area','age'
                        ,'garden','district','id'))
        item['total_price'] = response.css('.total::text').extract_first() + '万'
        item['unit_price'] = response.css('span.unitPriceValue::text').extract_first()
        # 获取房屋信息，如房型、层高、朝向、装修情况、面积、楼龄
        item['roomtype'] = response.css('.mainInfo::text').extract()[0]
        item['height'] = response.css('.subInfo::text').extract()[0]
        item['direction'] = response.css('.mainInfo::text').extract()[1]
        item['decorate'] = response.css('.subInfo::text').extract()[1]
        item['area'] = response.css('.mainInfo::text').extract()[2]
        item['age'] = re.sub("\D", "", response.css('.subInfo::text').extract()[2])
        # 获取房源所在小区、地区、环线等信息
        item['garden'] = response.css('.info::text').extract()[0]
        item['district'] = response.css('.info a::text').extract()[0]
        # 获取房源编号
        item['id'] = re.sub("\D", "", response.css('.houseRecord span::text').extract()[1])  # 通过正则方式把字符串中的数字提取出来
        # 用append方法向DataFrame中添加字典数据，注意在未设置DataFrame列名的情况下不能直接添加字典数据，会报错
        df = df.append(item, ignore_index=True)
        df.to_csv('content1.csv',mode='a',header=False)'''


