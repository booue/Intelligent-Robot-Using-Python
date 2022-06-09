# -*-coding = utf-8-*-

# Author:qyan.li
# Date:2022/5/13 9:35
# Topic:借助于python程序实现自动化邮件发送
# Reference:https://zhuanlan.zhihu.com/p/89868804


import smtplib
# 负责构造文本
from email.mime.text import MIMEText
# 负责将多个对象集合起来
from email.mime.multipart import MIMEMultipart
from email.header import Header


class AutoEmail():
    def __init__(self,MailReceiver,SendMail = '2691848674@qq.com'):
        self.MailSender = SendMail
        self.mm = MIMEMultipart('related')
        self.mail_host = "smtp.qq.com"
        self.mail_license = "tbhcprdhnghodcij"
        self.MailReceiver = MailReceiver
        self.ReceiverAddress = ''

    def Name2Mail(self,fileName):
        with open(fileName,'r',encoding = 'utf-8') as f:
            content = f.readlines()
        for item in content:
            if self.MailReceiver == item.split(' ')[0]:
                self.ReceiverAddress = item.split(' ')[1].strip('/n')
                return 1
            else:
                continue
        return -1

    def MailContent(self,subjectContent,bodyContent):
        # 邮件主题
        subject_content = subjectContent
        # 设置发送者,注意严格遵守格式,里面邮箱为发件人邮箱
        self.mm["From"] = "sender_name<" + self.MailSender + ">"
        # 设置接受者,注意严格遵守格式,里面邮箱为接受者邮箱
        self.mm["To"] = "receiver_1_name<" + self.ReceiverAddress + ">"
        # 设置邮件主题
        self.mm["Subject"] = Header(subject_content, 'utf-8')

        # 邮件正文内容
        body_content = bodyContent
        # 构造文本,参数1：正文内容，参数2：文本格式，参数3：编码方式
        message_text = MIMEText(body_content, "plain", "utf-8")
        # 向MIMEMultipart对象中添加文本对象
        self.mm.attach(message_text)

    def SendMail(self):
        mail_receivers = []
        mail_receivers.append(self.ReceiverAddress)
        # 发送邮件
        # 创建SMTP对象
        stp = smtplib.SMTP()
        # 设置发件人邮箱的域名和端口，端口地址为25
        stp.connect(self.mail_host, 25)
        # set_debuglevel(1)可以打印出和SMTP服务器交互的所有信息
        stp.set_debuglevel(1)
        # 登录邮箱，传递参数1：邮箱地址，参数2：邮箱授权码
        stp.login(self.MailSender, self.mail_license)
        # 发送邮件，传递参数1：发件人邮箱地址，参数2：收件人邮箱地址，参数3：把邮件内容格式改为str
        stp.sendmail(self.MailSender, mail_receivers, self.mm.as_string())
        print("邮件发送成功")
        # 关闭SMTP对象
        stp.quit()

    def start(self,subject,content):
        flag = self.Name2Mail(r'C:\Users\腻味\Desktop\ChattingSystem\ChattingSystemRobot\AutoMail\MailAddress.txt')
        if flag == -1:
            print('您的好友列表中查无此人')
            return
        else:
            self.MailContent(subject,content)
            self.SendMail()


if __name__ == '__main__':
    AE = AutoEmail('李其炎2')
    AE.start('垃圾邮件','写代码眼睛快瞎了')







