
<div align="center">

# Danmaku Reader
[![LICENSE](https://img.shields.io/badge/LICENSE-GPLv3+-red)][LICENSE]
[![Python](https://img.shields.io/badge/python-3.9+-blue)](https://www.python.org)
[![基于](https://img.shields.io/badge/基于-bilibili_api_python-green)][base]

**:warning: 注意：python版经过作者更详细的测试，会更加稳定; release版是pyinstaller打包完成的，只测试了可运行性**

</div>

--------

# 项目简介

**本项目源于作者学习python的过程中，十分希望与感谢各位对本项目的指导**

## 使用方法：（需要登录b站账号，请仔细阅读登录界面说明）

- 非打包方案
  - 通过要求文件安装必要支持`pip install -r requirements.txt`
  - 用3.9以上版本运行DanmakuReader.py

- release方案
  - 个人打包
    - 本项目给出了项目打包文件DanmakuReader.spec，只需安装`pip install pyinstaller`，并通过
      `pyinstaller DanmakuReader.spec`即可打包项目文件，打包好的程序位于 `./dist`文件夹中
  - release方案
    - 可以通过百度网盘
      > https://pan.baidu.com/s/1Xfv6NSY8QTdNOpDL7I-OBw?pwd=11my
    - 或者在GitHub页面获得最新包（GitHub一般会慢一点）


## 文件说明
- /files - 各类文件储存位置，第一次打开项目后自动创建
  * ban_words - 屏蔽词文件，json格式
  * settings - 非敏感设置信息文件，明文，json格式
  * INITIAL - 敏感信息文件（保存登录的cookie及账号密码），明文，json格式
  * temp - 临时标记文件，无内容，第一次初始化和重置时创建，打开程序后删除
- /logging - 日志文件夹
  * print_cmd_logging - 日志输出，包含项目文件输出，外部库logging的WARNING以下级别输出
  * sample_danmaku - 弹幕事件随机抽取，当打开debug后，随机抽取部分弹幕作为样例方便分析（抽取比20：1）  

## 机制说明
* 弹幕追赶机制
  * 机制保证在队列有50个以上词时，清空队列
  * 机制保证在队列有40个以上词时，每5个词只读1个词，并在保持40个以上词5次读取后清理10个词
  * 机制保证在队列有30个以上词时，每4个词只读1个词，并在保持30个以上词10次读取后清理10个词
  * 机制保证在队列有20个以上词时，每3个词只读1个词，并在保持20个以上词15次读取后清理10个词
  * 机制保证在队列有10个以上词时，每2个词只读1个词，并在保持10个以上词20次读取后清理5个词
  * 机制保证在队列有5个以上词时，每3个词只读2个词。


## 其他说明（Q&A）

* Q:为什么没有做重置弹幕机制？
  * A:已经有弹幕追赶机制了，不用重置也会一直保持在最新弹幕（追赶机制可以完全保证在大多数时间内在读最新弹幕）

* Q:我该怎么帮助作者？
  * A:你可以访问本项目的github页面提issue或者在b站联系：吾名喵喵之翼。作者只要闲着看到就会回复你（大概会在每天的23点后）
  * 仓库地址：https://github.com/MeowDWing/DanmakuReader


------

## 更新计划

+ alpha 1.3+ ： 日志方案等（预计11月底）
+ beta+ ： 更好的GUI界面（预计2024年中上）

[license]: https://github.com/MeowDWing/DanmakuReader/blob/main/LICENSE
[base]: https://github.com/Nemo2011/bilibili-api