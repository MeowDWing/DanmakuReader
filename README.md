# DanmakuReader

--------

**本项目有如下功能及特点：**
* **读取弹幕本直播间有粉丝牌的粉丝弹幕**
* **设置屏蔽词（完全匹配）**
* 参照b站up资深小狐狸直播时的需要设计
* 语音目前基于百度语音合成api

****
**使用方法：**
* py文件
  * 直接运行main.py即可根据提示操作
* release
  * 你需要下载main.exe 与 reader.exe，并放入同一个文件夹
  * 直接运行main.exe即可根据提示操作
* API配置
  * 第一次运行程序会自动初始化，你需要在百度语音合成项目里创建自己的工程文件
  * https://ai.baidu.com/tech/speech/tts?track=b6d7c141cb9ed59bcbbc91553767924a67ea39bae9988258
  * 注册后，领取‘短文本在线合成’项目（个人有5w次调用次数），并创建你的应用
  * ![image](https://github.com/MeowDWing/DanmakuReader/assets/67000868/3301f9d0-4e56-4149-ac74-a15543322b9f)
  * 之后，将对应的APIkey与secretkey复制到./files/settings.txt的预留位置即可
