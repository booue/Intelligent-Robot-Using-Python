# -*-coding = utf-8-*-

# Author:qyan.li
# Date:2022/5/12 19:17
# Topic:实现QQ和Wechat自动发送消息
# Reference:https://blog.csdn.net/qq_42761569/article/details/119150096

import pyautogui
import pyperclip
import time

class AutoMsg():
    '''后期内部可以添加key以决定使用Wechat或者QQ'''
    def __init__(self,msg,friendName,key):
        self.msg = msg
        self.name = friendName
        self.key = key

    def sendMsg(self):
        # Ctrl + alt + w 打开微信
        # Ctrl + alt + z 打开QQ
        if self.key == 'w':
            pyautogui.hotkey('ctrl', 'alt', 'w')
        if self.key == 'z':
            pyautogui.hotkey('ctrl', 'alt', 'z')
        # 搜索好友
        pyautogui.hotkey('ctrl', 'f')
        # 复制好友昵称到粘贴板
        pyperclip.copy(self.name)
        # 模拟键盘 ctrl + v 粘贴
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)
        # 回车进入好友消息界面
        pyautogui.press('enter')

    def send(self):
        pyperclip.copy(self.msg)
        # 模拟键盘 ctrl + v 粘贴内容
        pyautogui.hotkey('ctrl', 'v')
        # 发送消息
        pyautogui.press('enter')

    def start(self):
        self.sendMsg()
        self.send()


if __name__ == '__main__':
    MsgClass = AutoMsg('你今天晚上吃饭吗?','我的iPhone','z')
    MsgClass.start()



