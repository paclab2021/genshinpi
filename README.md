# genshinpi
A lite Genshin player info viewer for Raspberry Pi with E-Ink display

This project shall be credited to thesadru's Genshin Hoyolab API (https://github.com/thesadru/genshin.py) which provided the foundational framework to retrieve players' real-time information in the Genshin game.

## Hardware requirement:
Raspberry Pi Zero W (Gen 1/2)

or Raspberry Pi (Gen 3/4)

Waveshare 2.13inch e-Paper HAT Display (Ver.2)

A neet chassis(Optional)

It is straightforward to install this software and get it running. 

## Before installation
To begin you need a Raspberry Pi with the e-Paper display assembled. You must also need to set up the SSH connection with the Pi and get it connected to the Internet.

## To install
Access your Pi with an SSH connection and download the software package to its Home directory
```
cd ~
git clone https://github.com/paclab2021/genshinpi.git
```
Install python libraries required by the software:
```
cd ~/genshinpi/
sudo pip3 install -r requirements.txt 
```
Verify if the SPI interface is enabled, otherwise, the E-Ink screen won't display anything.
```
sudo raspi-config
```
In the pop-up GUI menu, select **5.Interfacing Options -> P4.SPI -> Yes**

## How to use

Open the installed **genshinpi** directory and modify the cookie parameter (**ltuid** and **ltoken**) within FetchCookies()
```
cd ~/genshinpi/
nano main.py
```
Here is an example showing the correct format of **ltuid** and **ltoken** set up.

If you need help with getting your **ltuid** and **ltoken** you may have a look on Sadru's project Wiki (https://thesadru.github.io/genshin.py/authentication/)
```py
async def FetchCookies():
    #Fetch Player Cookies with HOYOLAB Authentication
    cookies = {"ltuid": 205879462, "ltoken": "6226f7cbe59e99a90b5cef6f94f966fd"}  #Dict type
    client = genshin.Client(cookies, lang="zh-cn")
    return(client)
```
Now you can get this **GenshinPi** running by:
```
sudo python3 main.py
```
If the screen light up and shows the correct info, congratulations! To be finished you need set up its auto fetching process, otherwise, the program won't automatically update the player status when leaving the Raspberry Pi idle.

A simple solution for auto-fetching display is to use the **Crontab**:
```
sudo pip3 install crontab
```
After it is installed, you may declare the auto-update time in **crontab**'s configuration file.

```
sudo crontab-e
```
Copy and paste this command to the commented last line:

(You may change the number if you want its update interval other than 2 minutes)
```
*/2 * * * * /usr/bin/python3 /home/pi/genshinpi/main.py
```

Save and close the configuration file, and the crontab will install fresh program auto-execution 
```
pi@raspberrypi:~/genshinpi $ sudo crontab -e
crontab: installing new crontab
```
