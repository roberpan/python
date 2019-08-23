import tkinter
import json
import requests

class Weather(object):
    def __init__(self):
        self.root=tkinter.Tk()
        self.root.title('天气查询')
        self.city_input=tkinter.Entry(self.root,width=30)
        self.display_info=tkinter.Listbox(self.root,width=50)
        self.result_button=tkinter.Button(self.root,command=self.weather,text='查询')

    def gui_arrang(self):
        self.city_input.pack()
        self.display_info.pack()
        self.result_button.pack()

    def weather(self):
        self.cityname=self.city_input.get()
        weather_info=[]
        try:
            with open('citycode.txt',encoding='ANSI') as file:
                line = file.readlines()
                citycode = eval(line[0])
            if self.cityname in citycode:
                code = citycode[self.cityname]
                url = 'http://wthrcdn.etouch.cn/weather_mini?citykey=' + code
                r = requests.get(url)
                info = json.loads(r.text)
                info_today = info['data']['forecast'][0]
                date_today=info_today['date']
                hightemp_today=info_today['high']
                lowtemp_today = info_today['low']
                wind_today=info_today['fe ngxiang']
                type_today=info_today['type']

                info_tomorrow = info['data']['forecast'][1]
                date_tomorrow = info_tomorrow['date']
                hightemp_tomorrow = info_tomorrow['high']
                lowtemp_tomorrow = info_tomorrow['low']
                wind_tomorrow = info_tomorrow['fengxiang']
                type_tomorrow = info_tomorrow['type']

                '''
                info_after_tomorrow = info['data']['forecast'][2]
                date_after_tomorrow = info_after_tomorrow['date']
                hightemp_after_tomorrow = info_after_tomorrow['high']
                lowtemp_after_tomorrow = info_after_tomorrow['low']
                wind_after_tomorrow = info_after_tomorrow['fengxiang']
                type_after_tomorrow = info_after_tomorrow['type']
                '''
                weather_info = [str(lowtemp_tomorrow), str(hightemp_tomorrow),
                                "风向 " + str(wind_tomorrow), "天气 " + str(type_tomorrow), "日期 " + str(date_tomorrow),"\n",
                    str(lowtemp_today), str(hightemp_today),
                                "风向 " + str(wind_today), "天气 " + str(type_today), "日期 " + str(date_today)]
        except:
            weather_info=["城市不存在!"]
            print("{},城市不存在!".format(self.cityname))

        for item in range(10):
            self.display_info.insert(0,"")

        for item in weather_info:
            self.display_info.insert(0,item)

        return weather_info

def main():
    weather=Weather()
    weather.gui_arrang()
    tkinter.mainloop()
    pass

if __name__=="__main__":
    main()