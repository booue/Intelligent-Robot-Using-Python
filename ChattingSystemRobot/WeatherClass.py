# -*-coding = utf-8-*-

# Author:qyan.li
# Date:2022/5/12 18:30
# Topic:爬虫返回天气信息(class实现)

import urllib.request,urllib.error
from bs4 import BeautifulSoup
import re

class WeatherInfo():
    def __init__(self,cityName):
        self.city = cityName
        self.url = r'https://www.tianqi.com/' + str(cityName) + r'/'
        self.findTime = re.compile(r'<dd class="week">(.*?)</dd>')
        self.html = None
        self.WeatherInformation = ''


    def askURL(self):
        # 模拟浏览器头部信息(浏览器伪装，不会被设别为爬虫程序)
        # 用户代理，可以接受什么类型的返回文件
        head = {'User-Agent':  # 中间不能存在任何空格，包括大小写的相关问题
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0'
                }
        request = urllib.request.Request(self.url, headers=head)  # 携带头部信息访问url
        html = ''
        try:
            responseInfo = urllib.request.urlopen(request)  # responseInfo包含网页的基本信息
            html = responseInfo.read().decode('utf-8')  # 防止格式错误
            # print(html)
        except urllib.error.URLError as e:
            if hasattr(e, 'code'):
                print(e.code)
            if hasattr(e, 'reason'):
                print(e.reason)
        self.html = html


    def getData(self):
        soup = BeautifulSoup(self.html, 'lxml')
        item = soup.find('div', class_="left")
        # 分别获得'湿度','天气','空气'信息
        ShiDuItem = item.find('dd', class_='shidu')
        WeatherItem = item.find('dd', class_='weather')
        AirItem = item.find('dd', class_='kongqi')
        item = str(item)
        # 获得时间信息
        Time = str(re.findall(self.findTime, item)[0]).split('\u3000')[0]
        # print(Time)
        # 获得湿度信息
        ShiduInfo = ''
        for item in ShiDuItem.find_all('b'):
            ShiduInfo = ShiduInfo + str(item.string)
            ShiduInfo = ShiduInfo + ' '
        # 获得天气信息
        temperature = WeatherItem.find('p', class_='now').find('b').string + '摄氏度'
        condition = WeatherItem.find('span').find('b').string
        TempCondition = temperature + condition
        # 获得空气信息
        AirCondition = AirItem.find('h5').string
        PM = AirItem.find('h6').string
        AirPM = AirCondition + PM

        self.WeatherInformation = Time + ' '  + ShiduInfo + '温度' +TempCondition + AirPM

    def startWeather(self):
        self.askURL()
        self.getData()


if __name__ == '__main__':
    WeatherItem = WeatherInfo('beijing')
    WeatherItem.startWeather()
    print(WeatherItem.WeatherInformation)



