#Genshinpi V1.0.0
#by paclab
import sys
import os
import genshin
import asyncio
import datetime
import math
import time
import logging
from PIL import Image, ImageDraw, ImageFont

icondir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'icon')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')

if os.path.exists(libdir):
    sys.path.append(libdir)
from waveshare_epd import epd2in13_V2

# Domain lists
weaponlist = ["破瓦","孤云","瑚枝","始龀","雾丹","御灵","枷锁","陨铁","面具"]
booklist=["自由","繁荣","浮世","抗争","勤劳","风雅","诗文","黄金","天光"]

#############
# Functions #
#############

async def FetchCookies():
    #Fetch Player Cookies with HOYOLAB Authentication
    cookies = {"ltuid": _uid, "ltoken": "_ltoken"}  #Dict type
    client = genshin.Client(cookies, lang="zh-cn")
    return(client)

async def FetchPartial(client):
    #Fetch partial player info(stats, characters, exploration, teapots)
    partial = await client.get_partial_genshin_user(client.uid)
    return(partial)

async def FetchNote(client):
    #Fetch note info (resin, realm, commissions, expeditions)
    note = await client.get_genshin_notes(client.uid)
    return(note)

async def FetchExpeditionStatus(inputnote):
    #Fetch Expedition Status from player note
    for len_ex in range(len(inputnote.expeditions)):
        print(inputnote.expeditions[len_ex].character.name, inputnote.expeditions[len_ex].status)

async def DisplayExpeditionStatus(inputnote):
    #Fetch and display Expedition Status
    exp_str = ""
    #Fetch Expedition Status from player note
    for len_ex in range(len(inputnote.expeditions)):
        if inputnote.expeditions[len_ex].status == "Ongoing":
            exp_str = exp_str + "⊗"
        if inputnote.expeditions[len_ex].status == "Finished":
            exp_str = exp_str + "✔"
    return exp_str

async def geetWeeklyDiscount(inputnote):
    #Fetch and display Weekly Discount Domains
    wdiscount_str = "周本: "
    if inputnote.remaining_resin_discounts == 0:
        wdiscount_str = wdiscount_str + "✔"
    else:
        wdiscount_str = wdiscount_str + "✘"
    return wdiscount_str

async def getDaily_Commission(inputnote):
    #Fetch and display Daily commissions
    dailycom_str = "每日: "
    if inputnote.claimed_commission_reward == True:
        dailycom_str = dailycom_str + "✔"
    else:
        dailycom_str = dailycom_str + "✘"
    return dailycom_str

def PrintCharacters(partial):
    #Fetch player characters from partial list
    for x in range(len(partial.characters)):
        char_name = partial.characters[x].name
        char_rarity = partial.characters[x].rarity
        char_lv = partial.characters[x].level
        char_cons = partial.characters[x].constellation
        print(f"{char_name:10}|{char_rarity} | {char_lv} | {char_cons}")

def convert_timedelta(duration):
    #Convert TimeDelta format into HH:MM
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    return hours, minutes

def getWeaponList(weekday):
    # Fetch daily weapon enhancement material as str
    day_ct = weekday
    weapon_str = ''
    if day_ct > 3:
        day_ct = day_ct - 3
    for day_ct in range(day_ct*3-3,day_ct*3):
        #print(weaponlist[day_ct])
        weapon_str = weapon_str + "  " + weaponlist[day_ct]
    return weapon_str

def getBookList(weekday):
    # Fetch daily characters enhancement material as str
    day_ct = weekday
    book_str = ''
    if day_ct > 3:
        day_ct = day_ct - 3
    for day_ct in range(day_ct*3-3,day_ct*3):
        #print(booklist[day_ct])
        book_str = book_str + "  " + booklist[day_ct]
    return book_str

##################
#    main func   #
##################

async def main():
    #Retrieve client data
    client = await FetchCookies()
    note = await FetchNote(client)      #Resin/Expedition status      
    partial = await FetchPartial(client) #Stats, Characters, Explorations
    try:
        epd = epd2in13_V2.EPD()
        epd.init(epd.FULL_UPDATE)   #Initial screen full-update
        epd.Clear(0xFF)

        ##### Drawing UI display image
        #Declear fonts
        font13 = ImageFont.truetype(os.path.join(icondir, 'Font.ttc'), 13)
        font19 = ImageFont.truetype(os.path.join(icondir, 'Font.ttc'), 19)
        font30 = ImageFont.truetype(os.path.join(icondir, 'Font.ttc'), 30)

        # Declear display image
        image = Image.new('1', (epd.height, epd.width), 255)     
        draw = ImageDraw.Draw(image)

        #Drawing ui framelines
        draw.rectangle([(0,0),(epd.height, epd.width)], outline = 0, width = 3)
        draw.line([(0,45),(180,45)], fill = 0, width = 2)
        draw.line([(110,0),(110,45)], fill = 0, width = 2)
        draw.line([(180,0),(180,epd.height)], fill = 0,width = 2)
        draw.line([(30,45),(30, epd.height)], fill = 0, width = 2)
        draw.text((120, 6), '恢复时间', font = font13, fill = 0)
        draw.text((188, 6), '探索派遣', font = font13, fill = 0)

        #Side decoration
        png = Image.open(os.path.join(icondir, 'GENSHIN.bmp'))
        image.paste(png, (5,47))

        #Render Resin status / recovery time
        bmp = Image.open(os.path.join(icondir, 'Resin.bmp'))
        image.paste(bmp, (8,13))
        draw.text((40,5),str(note.current_resin),font = font30, fill=0)
        resin_remain_time = note.remaining_resin_recovery_time
        hours, minutes = convert_timedelta(resin_remain_time)
        resin_remain_time_str = str('{}时{}分'.format(hours, minutes))
        draw.text((120,25),resin_remain_time_str,font = font13, fill=0)

        #Domains, Weekly Discount, Daily Commisions Status
        date = datetime.datetime.now()     #Get Actual server time
        game_date = date - datetime.timedelta(hours=4, minutes=0)
        weekday = game_date.isoweekday()
        wdiscount_str = await geetWeeklyDiscount(note)
        dailycom_str = await getDaily_Commission(note)
        draw.text((40, 50), wdiscount_str, font = font13, fill = 0) #Display Weekly Discount Domains
        draw.text((110, 50), dailycom_str, font = font13, fill = 0) #Display Weekly Discount Domains
        if weekday != 7:
            weaponstr = getWeaponList(weekday)
            bookstr = getBookList(weekday)
            draw.text((30, 70), weaponstr, font = font19, fill = 0)
            draw.text((30, 90), bookstr, font = font19, fill = 0)
        else:
            draw.text((47, 60), "全部开放", font = font30, fill = 0)

        ###Realms
        realm_current = note.current_realm_currency
        realm_max = note.max_realm_currency
        realm_renorm = realm_current / realm_max #renormalization of realm currency percentage

        ##Display Realm currency
        realm_str = str(realm_current)+"/"+str(realm_max)
        draw.text((185, 50), realm_str, font = font13, fill = 0) 
        #####Realm currency scheme
        draw.ellipse((190, 65, 240, 115), outline = 0)
        deg = 2*(math.asin(math.sqrt(realm_renorm))*180/math.pi)
        draw.chord((190, 65, 240, 115), 90-deg, 90+deg, fill = 0)

        if realm_renorm == 1:
            draw.text((196, 80), "已满", font = font19, fill = 1)  #Notify when full
        
        #Expeditions
        exp_str = await DisplayExpeditionStatus(note)
        draw.text((183, 25), exp_str, font = font13, fill = 0)  #Notify when full

        #Display with correct screen rotating direction
        image = image.rotate(180)
        epd.display(epd.getbuffer(image))
        time.sleep(2)

    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd2in13_V2.epdconfig.module_exit()
        exit()
    
asyncio.run(main())
