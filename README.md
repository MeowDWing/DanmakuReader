# DanmakuReader

--------

**本项目有如下功能及特点：**

* **读取弹幕本直播间有粉丝牌的粉丝弹幕**


* **设置屏蔽词（完全匹配）**


* 参照b站up资深小狐狸直播时的需要设计
  * 自动追赶机制：帮助你直击最新弹幕（PUSH4 发布后）
  * 绝对的排外政策：可调节读取所需要的牌子等级（默认1级），只要不是自己直播间的牌子多少级都不读（PUSH4 发布后）
  * 没有阀门制度：跳过弹幕时不看等级，一视同仁（PUSH5 发布后）
  * 预设屏蔽词：符合狐宝直播需要，包含 。/ 赞 / ？ 和所有个位数字（PUSH5 发布后）
  * 当消息仅包含中英文常用符号时，拒绝加入消息队列（PUSH5发布后）
  * 自动储存字符长度3以下的字符串（PUSH5发布后）


* 基于pyttsx3


* 注意：python版经过作者更详细的测试，会更加稳定；release版是pyinstaller打包完成的，只测试了可运行性


* 打开项目后，可在对应直播间依次输入以下内容进行测试（注意直播间粉丝牌等级，没有粉丝牌或等级不足会拒绝加入队列）：
  * 好好好 > reader界面应出现：好好好 准备读取
  * 好好好 > 本次好好好不会读出来，因为相邻弹幕一致会拒绝读取
  * 。。。 > reader界面应出现：检测到。。。中仅包含符号，拒绝加入队列
  * 狐宝新婚快乐 > reader界面应出现：狐宝新婚快乐 准备读取
  * 好好好 > reader界面应出现：好好好 准备读取
  * 赞 > 本次赞因为在屏蔽词中，所以不会加入队列也不会读出来
  * 以上测试全部通过后，即可说明程序基本功能正常运行，如果有任何错误，请联系作者。
  * 错误信息可以如下形式保留：
    * 1,在项目文件夹右键打开cmd/windows terminal
    * 2,在cmd中，python请运行python main.py / release运行main.exe
    * 3,配置完成后，在主界面输入b启动程序，并关闭自动打开的reader界面
    * 4,以打开main同样的方式打开reader.py / reader.exe
    * 5,复现错误并将错误信息发送给作者，我会十分感谢您的错误报告


****
**使用方法：**
* py文件
  * 直接运行main.py即可根据提示操作
  * 由于未知bug，需要在启动后手动启动reader.py
* release
  * 直接运行main.exe即可根据提示操作，如果reader没有自动打开，可以手动启动

