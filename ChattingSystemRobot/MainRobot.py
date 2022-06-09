# -*-coding = utf-8-*-

# Author:qyan.li
# Date:2022/5/12 15:37
# Topic:借助于python构建智能机器人，完成人机交互功能
# Reference:https://zhuanlan.zhihu.com/p/302592540
#          :https://www.cnblogs.com/xp1315458571/p/13892205.html

## 增加import文件检索路径(添加自定义的class模块)
import sys
sys.path.insert(0,r'C:\Users\腻味\Desktop\ChattingSystem\ChattingSystemRobot')
## 相关模块引入
import pyaudio
import wave
from aip import AipSpeech
import pyttsx3
from selenium import webdriver
import time
import requests
import json
from AutoMessageClass import AutoMsg
from WeatherClass import WeatherInfo
from AutoMail import AutoEmailClass
from pywinauto.application import Application
import pyautogui
import time
import pyperclip
import jieba
from fuzzywuzzy import fuzz
from xpinyin import Pinyin
import numpy


## 百度识别编码
APP_ID = '26215596'
API_KEY = 'mKmzR3E2lGbY3dgDhkSIG4BN'
SECRET_KEY = 'WRGlvZ7pGGQAmSpIf9kc9YEzaHTCLAGH'


#声音录制设置
CHUNK = 1024
FORMAT = pyaudio.paInt16 # 16位深
CHANNELS = 1 #1是单声道，2是双声道。
RATE = 16000 # 采样率，调用API一般为8000或16000
RECORD_SECONDS = 10 # 录制时间10s


#录音文件保存路径
def save_wave_file(pa, filepath, data):
    wf = wave.open(filepath, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(pa.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(data))
    wf.close()


#录音主体文件
def write_audio(filepath,isstart):
    '''
    :param filepath:文件存储路径（'test.wav'） 
    :param isstart: 录音启动开关（0：关闭 1：开启）
    '''
    if isstart == 1:
        pa = pyaudio.PyAudio()
        stream = pa.open(format=FORMAT,
                         channels=CHANNELS,
                         rate=RATE,
                         input=True,
                         frames_per_buffer=CHUNK)

        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)  # 读取chunk个字节 保存到data中
            frames.append(data)  # 向列表frames中添加数据data

        stream.stop_stream()
        stream.close()  # 停止数据流
        pa.terminate()  # 关闭PyAudio

        #写入录音文件
        save_wave_file(pa, filepath, frames)
    elif isstart == 0:
        exit()


# 获取录音文件内容并进行识别
def GetAudioContent(fileName):
    '''
    :param fileName:录音文件路径 
    :return: sign-是否获得结果，result_out-返回录音内容
    '''
    # 读取录音文件内容
    with open(fileName,'rb') as f:
        content = f.read()
    # 调用Baidu-api实现语音识别
    sign = 1
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    result = client.asr(content, 'wav', 16000, {'dev_pid': 1537, })
    print(result)
    if 'result' not in result.keys():
        sign = 0
        result_out = None
    elif result['result'] == ['']:
        sign = 0
        result_out = None
    else:
        result_out = "".join(result['result'])
    return [sign, result_out]



client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
def listen():
    '''
    :return: 语音识别结果返回
    '''
    with open('./AudioFile.wav', 'rb') as f:
        audio_data = f.read()

    results = client.asr(audio_data, 'wav', 16000, {
        'dev_pid': 1537,
    })
    if 'result' in results:
        print("you said: " + results['result'][0])
        return results['result'][0]
    else:
        print("出现错误，错误代码：" , results['err_no'])


#语音播报函数
def speech_read(content):
    '''
    :param content:待播报的字符串 
    :return: None
    '''
    #模块初始化
    engine = pyttsx3.init()
    engine.say(content)
    # 等待语音播报完毕
    engine.runAndWait()

## 自动内容检索
def SearchInternet(ObjectContent):
    '''
    :param ObjectContent:待检索的目标内容 
    :return: None
    '''

    driver = webdriver.Firefox()
    url = 'http://www.baidu.com'
    driver.get(url)
    # 最大化窗口(方便后续定位搜索框)
    driver.maximize_window()

    '''不同的浏览器，此处的标签驱动不同(可从网页源码分析)'''
    # 输入框定位和内容输入
    shuru = driver.find_element_by_id('kw')
    shuru.send_keys(ObjectContent)
    time.sleep(2)

    # 内容检索
    sousuo = driver.find_element_by_id('su')
    sousuo.click()
    time.sleep(2)

## 自动发送微信，qq消息
def AutoMessage(msg,friend,key):
    '''
    :param msg: 待发送的消息
    :param friend: 目标发送的对象
    :param key: 使用微信或者qq发送,'w'-wechat,'z'-qq
    :return:None 
    '''
    Amsg = AutoMsg(msg,friend,key)
    Amsg.start()

## 自动获取天气信息
def GetWeatherInfo(cityName = 'chengdu'):
    '''
    :param cityName:待查询城市的名称 
    :return: 该城市的天气信息
    '''
    WeatherItem = WeatherInfo(cityName)
    WeatherItem.startWeather()
    return WeatherItem.WeatherInformation

## 自动播放歌曲
def AutoPlayMusic(MusicName,pause = 0):
    '''
    :param MusicName:待播放的音乐名称 
    :param pause:是否暂停音乐
    :return: None
    '''
    if pause == 0:
        # 开启音乐软件
        app = Application(backend="uia").start(r'C:\Program Files (x86)\Tencent\QQMusic\QQMusic.exe')
        # 移动鼠标至搜索框位置
        pyautogui.moveTo(516, 39)
        pyautogui.click(button='left')
        # 剪切清空搜索框
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'x')
        # 复制粘贴搜索指定歌曲
        pyperclip.copy(MusicName)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(2)
        # 点击播放按钮
        pyautogui.moveTo(750, 450)
        pyautogui.click(button='left')
    if pause == 1:
        pyautogui.click(button='left')

## 自动发送邮件
def AutoSendEmail(friendName,subject,content):
    '''
    :param friendName:发送对象的姓名 
    :param subject: 邮件主题
    :param content: 邮件主要内容
    :return: None
    '''
    AE = AutoEmailClass.AutoEmail(friendName)
    AE.start(subject, content)

#调用机器人
def robot(text = " "):
    '''
    :param text: 问询的文本
    :return: 机器人返回的内容
    '''
    url = 'http://api.qingyunke.com/api.php?key=free&appid=0&msg='+str(text)
    response = requests.get(url)
    responseText = response.text.split('"')[-2]
    return responseText

# 文本处理函数：jieba分词+去除停用词
def TextDealing(content):
    '''
    :param content:待处理的文本内容 
    :return:None 
    '''
    # 停用词内容读取
    with open('./stop_words.txt','r',encoding = 'utf-8') as f:
        stopWordsLst = f.readlines()
    stopWordsLst = [item.strip('\n') for item in stopWordsLst]

    jiebaText = jieba.cut(content)
    _jiebaStr = ''
    jiebaStr = ''
    for item in jiebaText:
        if item not in stopWordsLst:
            _jiebaStr += item + ' '
            jiebaStr += item
        else:
            continue
    return _jiebaStr,jiebaStr


# 模糊匹配函数
def FuzzComparsion(text,shift = 0):
    '''
    :param text:待匹配的文本 
    :param shift:取值1或0-待匹配的模板不同
    :return: 相似程度列表
    '''
    similarityLst = []
    stencilTextLst1 = ['给李其炎发消息，邮件告诉他我明天有事找他','今天的天气状况怎么样','播放一首炸雷','帮我查一下现在的俄乌局势'] # 匹配的模板文本
    stencilTextLst2 = ['QQ', '微信', '邮件']
    if shift == 0:
        stencilTextLst = stencilTextLst1
    if shift == 1:
        stencilTextLst = stencilTextLst2
    for item in stencilTextLst:
        similarity = fuzz.ratio(item,text)
        similarityLst.append(similarity)
    return similarityLst


def MsgDivision(content,key):
    '''模板：给***发消息告诉他***
    :param content:待处理的文本 
    :return: friendName发送对象和Msg发送内容
    '''
    if key == 'w':
        friendName = content.split('发微信')[0].strip('给')
    if key == 'z':
        friendName = content.split('发QQ')[0].strip('给')
    Msg = content.split('告诉他')[-1]
    return friendName,Msg


def MailMsgDivision(content):
    '''模板：给***发送邮件，主题是***，邮件内容是***
    :param content: 待处理文本
    :return: friendName-发送对象,subject-邮件主题,MailContent-邮件内容
    '''
    friendName = content.split('发送邮件')[0].strip('给')
    subject = content.split('主题是')[1].split('邮件内容是')[0]
    MailContent = content.split('邮件内容是')[-1].strip(',')
    return friendName,subject,MailContent


def Mainloop(text):
    '''
    :param text:待问询的文本 
    :return: None或者返回的内容
    '''
    similarityLst = FuzzComparsion(text)
    print(similarityLst)
    if max(similarityLst) < 30:
        # 调用free robot
        response = robot(text)
        print(response)
    else:
        max_index = similarityLst.index(max(similarityLst))
        if max_index == 0:
            # 调用wechat,QQ,Mail模块(模板:给**发**告诉他****)
            similarityLst = FuzzComparsion(text,1)
            index = similarityLst.index(max(similarityLst))
            if index == 0:
                # 调用QQ模块
                friendName , Msg = MsgDivision(text,'z')
                AutoMessage(Msg,friendName,'z')
            if index == 1:
                # 调用微信模块
                friendName, Msg = MsgDivision(text,'w')
                AutoMessage(Msg, friendName, 'w')
            if index == 2:
                # 调用邮件模块
                friendName,subject,Mailcontent = MailMsgDivision(text)
                AutoSendEmail(friendName,subject,Mailcontent)
                pass
        if max_index == 1:
            # 调用查询天气模块(模板：以城市名称开头，如成都今天天气怎么样?)
            content , _ = TextDealing(text)
            cityName = content.split(' ')[0]
            P = Pinyin()
            cityName_pinyin = P.get_pinyin(cityName,'')
            Weather = GetWeatherInfo(cityName_pinyin)
            print(Weather)
        if max_index == 2:
            # 调用音乐播放模块(模板：播放**)
            MusicName = text.strip('播放')
            AutoPlayMusic(MusicName)
        if max_index == 3:
            # 调用浏览器检索板块
            _ , SearchContent = TextDealing(text)
            SearchInternet(SearchContent)


def main():
    speech_read('有什么可以帮您的呢？')
    write_audio(filepath = './AudioFile.wav',isstart = 1)
    content = listen()
    speech_read(content)
    Mainloop(content)


if __name__ == '__main__':
    main()



