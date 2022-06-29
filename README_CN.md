# GenshinPi- Ver 1.0.0
### [English](README.md)  | 中文
基于树莓派与电子墨水屏的轻量化原神玩家信息实时显示器
本项目使用的数据接口来自于thesadru等编写的原神玩家信息API (https://github.com/thesadru/genshin.py)
，该项目提供了基于python的原神玩家信息API框架，相当实用。
## 硬件需求:
树莓派 Zero W (第1/2代皆可)

或 树莓派 (第3/4代)

微雪 2.13寸 e-Paper 电纸墨水屏显示器 (第二代)

好看可爱的外壳(可选)

根据以下步骤设置安装本程序相当简易，预计操作时间不超过10分钟。

## 安装之前
在安装本软件之前，请准备好一个已连接至微雪电子墨水屏的树莓派设备。
如果您是第一次设置树莓派，请务必根据第三方教程配置好设备的SSH连接与Wi-Fi互联网设置。该程序需要树莓派连接互联网方可使用。
## 安装步骤
使用SSH工具连接至树莓派，并通过Git下载本程序至树莓派的根目录：
```
cd ~
git clone https://github.com/paclab2021/genshinpi.git
```
程序下载完成后，需要下载安装运行相关的Python依赖库
```
sudo pip3 install -r requirements.txt 
```
点亮墨水屏需要打开树莓派的SPI接口，以开启树莓派主板与屏幕的通信协议

```
sudo raspi-config
```
在打开的设置窗口界面里, 依次选择 **5.Interfacing Options -> P4.SPI -> Yes**，确认打开树莓派硬件的SPI接口。

## 如何使用

打开已安装的 **genshinpi** 目录，通过文本编辑器访问main.py文件，找到FetchCookies()函数，将您米游社账户的**ltuid**与**ltoken**填入相关参数内：
```
cd ~/genshinpi/
nano main.py
```

下列实例代码显示了**ltuid**与**ltoken**在FetchCookies()函数的正确格式与填入方式（非真实，如果不想让别人看到您的玩家信息请注意私密保存），无需修改该函数外的其它代码。

如果您不明白如何获取自己游戏账户的**ltuid**与**ltoken**，请访问Sadru的Wiki获取详细解释与步骤(https://thesadru.github.io/genshin.py/authentication/)
```py
async def FetchCookies():
    #Fetch Player Cookies with HOYOLAB Authentication
    cookies = {"ltuid": 205879462, "ltoken": "6226f7cbe59e99a90b5cef6f94f966fd"}  #Dict type
    client = genshin.Client(cookies, lang="zh-cn")
    return(client)
```
上述步骤完成后，您可以开始测试**GenshinPi**的主程序是否正常工作了
```
sudo python3 main.py
```
如果墨水屏刷新点亮，且成功显示相关信息，恭喜！您已经成功一大半了，最后还需要配置程序的自动刷新脚本。否则，该程序只会在SSH中手动输入命令才会运行；
这里使用的是**Crontab**小工具，能让本程序自动定时运行，实现玩家信息实时刷新的功能。

```
sudo pip3 install crontab
```
成功安装**Crontab**后，编辑该程序的自动运行配置文件

```
sudo crontab-e
```
复制该行脚本至配置文件的底行便可实现自动运行。

这里的案例是令屏幕每2分钟刷新一次，如果您想改变程序自动刷新信息的周期，将数字改为您所需要的数字即可。
```
*/2 * * * * /usr/bin/python3 /home/pi/genshinpi/main.py
```

保存并关闭**Crontab**配置文件，程序便可按照设置的周期自动运行。
```
pi@raspberrypi:~/genshinpi $ sudo crontab -e
crontab: installing new crontab
```
