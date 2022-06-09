### 基于python的智能聊天机器人



#### 一、文件结构：

1. ``MainRobot.py`` 主体代码

2. ``WeatherClass.py`` 天气查询板块``class``

3. ``AutoMessageClass.py`` 消息自动发送板块``class``

4. ``stop_words.txt`` 文本处理停用词文件

5. ```AudioFile.wav` 录音保存文件

6. ``AutoMail`` 自动发送邮件文件夹

   --- ``AutoEmailClass.py`` 自动发送邮件``class``

   --- ``MailAddress.py`` 姓名邮箱映射文件

#### 二、调用方式：

+ 前提：
  1. 进入文件夹目录
  2. 安装相关``python``模块
  3. 部分功能需要特殊配置：
     + 网页查询 --- 浏览器驱动
     + 自动发邮件 --- 邮箱授权码，配置姓名邮箱地址文件

+ 代码执行：

  运行``MainRobot.py``代码，待电脑麦克风调用后，语音输入，等待程序返回结果

