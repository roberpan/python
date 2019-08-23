# -*- coding: utf-8 -*
#显示要查询城市的天气情况
import json
import requests
with open('citycode.txt') as file:
    line=file.readlines()
    citycode=eval(line[0])
cityname=input("你想查哪个城市的天气？")
if cityname in citycode:
    code = citycode[cityname]
    url='http://wthrcdn.etouch.cn/weather_mini?citykey='+code
    r=requests.get(url)
    info=json.loads(r.text)
    info_today=info['data']['forecast'][0]
    print("今天日期：",info_today['date'])
    print("最高温度：",info_today['high'])
    print("最低温度：",info_today['low'])
    print("风向：", info_today['fengxiang'])
    print("天气：", info_today['type'])
    print("")

    info_tomorrow=info['data']['forecast'][1]
    print("明天日期：", info_tomorrow['date'])
    print("明日最高温度：", info_tomorrow['high'])
    print("明日最低温度：", info_tomorrow['low'])
    print("明日风向：", info_tomorrow['fengxiang'])
    print("明日天气：", info_tomorrow['type'])
    print("")

    info_after_tomorrow = info['data']['forecast'][2]
    print("后天日期：", info_after_tomorrow['date'])
    print("后日最高温度：", info_after_tomorrow['high'])
    print("后日最低温度：", info_after_tomorrow['low'])
    print("后日风向：", info_after_tomorrow['fengxiang'])
    print("后日天气：", info_after_tomorrow['type'])
else:
    print("城市不存在!")