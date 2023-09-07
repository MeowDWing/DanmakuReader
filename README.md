# DanmakuReader

--------

**本项目有如下功能及特点：**

* **读取弹幕本直播间有粉丝牌的粉丝弹幕**


* **设置屏蔽词**

* <font color=#00FFFF>参照b站up资深小狐狸直播时的需要设计
  * 自动追赶机制：帮助你直击最新弹幕（PUSH4 发布后）
  * 绝对的排外政策：可调节读取所需要的牌子等级（默认1级）
  * 极端的亲外决议：当读取所需等级设为0时，会读取所有弹幕（只要他能读出来）（PUSH8发布后）
  * 没有阀门制度：跳过弹幕时不看等级，一视同仁（PUSH5 发布后）
  * 预设屏蔽词：符合狐宝直播需要，包含 。/ 赞 和所有个位数字（PUSH5 发布后）
  * 当消息仅包含中英文常用符号时，拒绝加入消息队列（PUSH5发布后）
  * 正则表达式匹配（PUSH7 发布后）</font>


* <font color=#FFFF00>基于pyttsx3（PUSH6 发布后）</font>


* <font color=coffee>采用多进程编写（PUSH8 发布后）</font>


* **注意：python版经过作者更详细的测试，会更加稳定；release版是pyinstaller打包完成的，只测试了可运行性**


* <font color=#00FACB>打开项目后，可在对应直播间依次输入以下内容进行测试（注意直播间粉丝牌等级，没有粉丝牌或等级不足会拒绝加入队列）：
  * 好好好 > 界面应出现：好好好 准备读取
  * 好好好 > 本次好好好不会读出来，因为相邻弹幕一致会拒绝读取
  * 。。。 > 界面应出现：检测到。。。中仅包含符号，拒绝加入队列
  * 狐宝新婚快乐 > 界面应出现：狐宝新婚快乐 准备读取
  * 好好好 > 界面应出现：好好好 准备读取
  * 赞 > 本次赞因为在屏蔽词中，所以不会加入队列也不会读出来
  * 以上测试全部通过后，即可说明程序基本功能正常运行，如果有任何错误，请联系作者。
  * 错误信息可以如下形式保留：
    * 1,在项目文件夹右键打开cmd/windows terminal
    * 2,在cmd中，python请运行python main.py / release运行main.exe
    * 3,配置完成后，在主界面输入b启动程序
    * 4,复现错误并将错误信息发送给作者，我会十分感谢您的错误报告
</font>

****
**使用方法：**
* py文件（推荐）（需要库：bilibili-api-python、pyttsx3）
  * 你可以通过`pip install bilibili-api-python pyttsx3` 直接安装
  * 直接运行main.py即可根据提示操作

* release
  * 直接运行main.exe即可根据提示操作


*****
**配置说明**
* 打开main文件后，选择c.查看可以看到ban文件和settigns文件，选择即可打开文件，之后保存并关闭文件即可进一步操作


* ban_words：
  * 你可以在文件后面添加词或句子以达到匹配屏蔽
  * '$'(美元)符号开头的句子被认为是注释
  * '-'开头的句子被认为是匹配词（注意-后不要有空格，除非你需要空格加入匹配词）


* settings
  * 目前包含rid和min_level选项
  * rid代表接入直播间的直播间id， minlevel表示读取弹幕所需的最小本直播间粉丝牌等级
  * 由于api问题（没有牌子的直播徽章返回值是None而不是0），所以没有专门做所有人可阅读的设置，如有需要联系作者（github或b站均可）

* INITIAL
  * 本文件标记是否初始化并记录登录信息，**记录内容均为敏感内容且明文保存，请注意妥善保管**

* login
  * 本文件为自动登录标记文件，为空


*****
**机制说明**
* 弹幕追赶机制
  * 机制保证在队列有50个以上词时，清空队列
  * 机制保证在队列有40个以上词时，每5个词只读1个词，并在保持40个以上词5次读取后清理10个词
  * 机制保证在队列有30个以上词时，每4个词只读1个词，并在保持30个以上词10次读取后清理10个词
  * 机制保证在队列有20个以上词时，每3个词只读1个词，并在保持20个以上词15次读取后清理10个词
  * 机制保证在队列有10个以上词时，每2个词只读1个词，并在保持10个以上词20次读取后清理5个词
  * 机制保证在队列有5个以上词时，每3个词只读2个词。


*****
**其他说明（Q&A）**

* Q:为什么没有做重置弹幕机制？
  * A:已经有弹幕追赶机制了，不用重置也会一直保持在最新弹幕（追赶机制可以完全保证在大多数时间内在读最新弹幕）


* Q:我该怎么知道这些机制都正常运行了？
  * A:在reader界面，每个机制的每次运行都会发送运行消息，该界面是重要的调试界面，如果你无意调试，可以无视这个界面的输出。


* Q:为什么没有做界面？
  * A:很简单，因为作者不会，没学过。


* Q:作者怎么连这么简单的东西都不会？
  * A:因为这是计算机的活，作者是做通信的，不会很正常。


* Q:我该怎么帮助狐宝或者作者？
  * A:你可以访问本项目的github页面提issue或者在b站联系：吾名喵喵之翼。作者只要闲着看到就会回复你（大概会在每天的23点后）
  * 仓库地址：https://github.com/MeowDWing/DanmakuReader