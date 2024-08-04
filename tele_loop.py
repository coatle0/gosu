from telethon import TelegramClient,events
from telethon import functions, types
from telethon.tl.types import MessageEntityTextUrl
import asyncio
import nest_asyncio
import openpyxl
import pandas as pd

from PIL import Image, ImageDraw, ImageFont
import os
import time
from os import path

import OpenDartReader
import requests
import re
import csv
#from fd_dart_mod import crawl_url
import datetime
import sys

import shutil
import os

import mypkg



focusjm_fn = "focusjm.xls" 
api_id = '26890695'
api_hash = '37fabab3680ade31f959c9c7f7241d71'
bot_id = 5824250303
awake_id = 1066938528
my_bot_ch = 'https://t.me/coatle_gosu_bot'
awake_ch = 'https://t.me/darthacking'
puzzle_ch = 'https://t.me/investment_puzzle'
pub_botch = 'https://t.me/+UXk5Hg2zqF84Y2Nl'


#dart api key
api_key = '61b268a6147bf74f5b549a99bff5ea2974e011b2'

start_date = '20230101'



dart_url = 'http://dart.fss.or.kr/dsaf001/main.do?rcpNo='
naver_url = 'https://finance.naver.com/item/fchart.naver?code='



global awake_entity
focusjm_list = pd.read_excel(focusjm_fn,dtype=str)

kwd_comp = ' '+focusjm_list['corp_name']
kwd_comp = kwd_comp.to_list()


client = TelegramClient('session_file', api_id, api_hash)

perf_df = pd.DataFrame([])
perf_df_tmp = pd.DataFrame([])

async def Run_Telethon():
    global awake_entity   
    global kwd_df 
    await client.start()
    
    #me = await client.get_me()
    #me = await client.get_entity(my_bot_ch)
    #print(me)

    
    awake_entity = await client.get_entity(awake_ch)
    await client.send_message(my_bot_ch,'Bot is ready')
    print('bot is ready!')
    await client.send_message(pub_botch,'Bot is ready')

    #print(my_channel)
    
   
    await client.run_until_disconnected()

kwd_prop = '최근 실적'

kwd4event = ['무상증자결정','유상증자결정','투자판단관련']

@client.on(events.NewMessage(chats=awake_ch))
async def handler(event):
    for i in kwd_comp:
        #실적발표시즌용
        #kwd_tgt_pool=[i,kwd_prop]
        kwd_tgt_pool="기업명:"+i
        #print(i)
        #if all(kwd_tgt in event.message.message for kwd_tgt in kwd_tgt_pool) :
        if kwd_tgt_pool in event.message.message:
            #print(i)          
            await client.forward_messages(my_bot_ch,event.message)
            await client.send_message(my_bot_ch,kwd_tgt_pool)
            #await event.reply(i)
            #print(msg.message)
            #focusjm_list.loc[focusjm_list['corp_name']==i.strip(),'awake']=msg.message
    
    for kwd4df_pick in kwd4event:
        if kwd4df_pick in event.message.message:
        #kwd_df_tmp.loc[0,kwd4df] = msg.message
        #kwd_df = pd.concat([kwd_df,kwd_df_tmp])
            await client.forward_messages(my_bot_ch,event.message)
            await client.send_message(my_bot_ch,'#'+kwd4df_pick)



@client.on(events.NewMessage(chats=my_bot_ch))
async def handler(event):
    txt_buf =""
    kwd_df = pd.DataFrame([])
    kwd_df_tmp = pd.DataFrame([])

    perf_df = pd.DataFrame([])
    perf_df_tmp = pd.DataFrame([])

    kwd4df = '기업설명회'
    await client.get_dialogs()
    date_of_post = datetime.datetime.today()-datetime.timedelta(days=1)
    #msgs=str(event)
    #print(event.message.message)
    escape = 0
    
    #await event.reply('안녕!')
    #async for msg in client.iter_messages(awake_entity,3000):

    if '/test' in event.message.message:
        buyorsell = event.message.message.split(' ')[1]

    if '/runkw' in event.message.message:
        os.system('python test_kiwoom.py')
        await client.send_message(my_bot_ch, "kw ready")

    if '/shield' in event.message.message:
        await event.message.delete()
        os.system('rscript shield.R')
        os.system('rscript shield_us.R')
        await client.send_message(my_bot_ch, "https://docs.google.com/spreadsheets/d/1M0LjBg2tPZprA-BIvsOZXjNPyK_gKm4pY4Ns93gvgJo/edit#gid=1794360922")

    if '/pfbb' in event.message.message:
        await event.message.delete()
        os.system('rscript bb_pf.R')

    if '/dbg' in event.message.message:
        #jm_name = event.message.message.split('_')[1]
        tgt_date = event.message.message.split(' ')[1]
        #count_msg = 0
        os.system('rscript dbg_day_run.R '+tgt_date)
        mes = await client.send_message(my_bot_ch, "done!")
        time.sleep(1.5)
        await mes.delete()
    
    if '/dbl' in event.message.message:
        jm_name = event.message.message.split(' ')[1]
        tgt_date = event.message.message.split(' ')[2]
        #count_msg = 0
        os.system('rscript dbg_set_jm.R '+jm_name)
        os.system('rscript dbg_day_run.R '+tgt_date)
        mes = await client.send_message(my_bot_ch, "done!")
        time.sleep(1.5)
        await mes.delete()
    
    if '/live' in event.message.message:
        await event.message.delete()



    if '/init_jm' in event.message.message:
        #jm_name = event.message.message.split('_')[1]
        #await client.forward_messages(my_bot_ch,event.message)
        mes=await client.send_message(my_bot_ch,"init gs jm")
        time.sleep(1.5)
        await mes.delete()
        #print('python dart_freport_name_arg.py '+jm_name)
        os.system('python mgr_day.py')
        mes = await client.send_message(my_bot_ch, "done!")
        time.sleep(1.5)
        await mes.delete()

    if '/quit' in event.message.message:
        await event.message.delete()
        async for msg in client.iter_messages(my_bot_ch,offset_date=date_of_post,reverse=True):
            if "Bot is ready" in msg.message:
                await msg.delete()
        sys.exit()
 
    
    if '/br' in event.message.message:
        jm_name = event.message.message.split(' ')[1]
        comp_name = jm_name
        print(jm_name)
        #await client.forward_messages(my_bot_ch,event.message)
        await event.message.delete()
        print('python dart_freport_name_arg.py '+jm_name)
        tgt_date = datetime.datetime.today().strftime("%Y%m%d")
        
        #os.system('python dart_freport_name_arg.py '+jm_name)
        dart = OpenDartReader(api_key)
        # get stock code
        df_corp_codes = dart.corp_codes
        chkcorp = df_corp_codes['corp_name'] == comp_name
        chknnull = df_corp_codes['stock_code'] != ' '
        comp_code = df_corp_codes[chkcorp & chknnull]['stock_code']
        report_list=dart.list(corp=comp_code.iloc[0],start=start_date,end=tgt_date,kind='A',final=False)
        test = report_list.query('report_nm.str.contains("보고서")')
        test = test[~test.report_nm.str.contains("기재정정")]
        test = test[~test.report_nm.str.contains("첨부추가")]
        test = test[~test.report_nm.str.contains("첨부정정")]
        #print(test)
        #remove '=' for compatibility issue btw xlsx and R read_xl
        header_url = dart_url+test['rcept_no']
        test['url'] = header_url
        test['hyperlink'] = 'HYPERLINK("'+header_url+'",'+'"사업보고서"'+')'
        test['stock_code']=naver_url+test['stock_code']
        test['stock_code']='HYPERLINK("'+test['stock_code']+'",'+'"chart link"'+')'

        df_index = test.columns.tolist()
        df_index.remove('corp_name')
        df_index.remove('report_nm')
        df_index.remove('rcept_dt')
        df_index.remove('hyperlink')
        df_index.remove('stock_code')
        dart_br_fn = 'dart_br.xlsx'
        test=test.drop(df_index,axis=1)
        str2send = test['stock_code'].iloc[0]+' '+test['hyperlink'].iloc[0] +" #"+comp_name
        print(str2send)
        await client.send_message(my_bot_ch,str2send)

        count_msg = 0

        report_df = pd.DataFrame([])
        report_df_tmp = pd.DataFrame([])
        
        async for msg in client.iter_messages(puzzle_ch,search="#"+jm_name):
            print(msg.id)
            await client.send_message(my_bot_ch,puzzle_ch+'/'+str(msg.id)+" #"+comp_name)
            test.loc[count_msg,'report'] = 'HYPERLINK("'+puzzle_ch+'/'+str(msg.id)+'")'
            count_msg = count_msg + 1
            if count_msg == 3:
                break



        awake_entity = await client.get_entity(awake_ch)
        #print(my_channel)
        kwd_df = pd.DataFrame([])
        kwd_df_tmp = pd.DataFrame([])


    
        
        comp_kwd = '최근 실적'
        #date_of_post = datetime.datetime(2023, 8, 1)
        date_of_post=datetime.datetime.today()-datetime.timedelta(days=1)
       
    
        async for msg in client.iter_messages(awake_entity,offset_date=date_of_post,search=comp_name):
           if comp_kwd in msg.message:
                    #print(msg.message)
                kwd_df_tmp.loc[0,kwd4df] = msg.message
                kwd_df = pd.concat([kwd_df,kwd_df_tmp])

        kwd_df=kwd_df.reset_index(drop=True)
        test['실적'] = kwd_df.iloc[0:4,0]
        await client.send_message(my_bot_ch,test['실적'][0]+" #"+comp_name)
        test.to_excel(excel_writer=dart_br_fn,index=False)
        sheet_nm = "IR2"

        ''' rpy2 sub pc windows 7 issue
        r_df = pandas2ri.py2rpy(test)

        robjects.globalenv["r_df"] = r_df

        robjects.r( multi line comments
            library(googlesheets4)
                  
            r_df$stock_code <- gs4_formula(r_df$stock_code)
            r_df$hyperlink<-gs4_formula(r_df$hyperlink)
                   
            
            gs4_auth(email = "coatle0@gmail.com")
            ssid_asset <- "1M0LjBg2tPZprA-BIvsOZXjNPyK_gKm4pY4Ns93gvgJo"
            range_clear(ssid_asset,sheet="IR2")
            range_write(ssid_asset,r_df,range="A1",col_names = TRUE,sheet = "IR2")

        multi line comments)
        '''
        
        
        #os.system('rscript --vanilla xls2gs.R '+dart_br_fn+" "+sheet_nm+" br")
        #print(jm_name)
        #await client.forward_messages(my_bot_ch,event.message)
        #await event.message.delete()
        print('rscript --vanilla run_jm.R '+jm_name+" k")
        os.system('rscript --vanilla run_jm.R '+jm_name+" k")
        await client.send_message(my_bot_ch,"https://docs.google.com/spreadsheets/d/1GWW0Q1RgMNAvSG7S4OyrbXSpcSHDnMSmd2uTsmZyJJE/edit#gid=1026403975")


    
    #bollinger band 
    if '/bb' in event.message.message:
        jm_name = event.message.message.split(' ')[1]
        market = event.message.message.split(' ')[2]
        #print(jm_name)
        #await client.forward_messages(my_bot_ch,event.message)
        await event.message.delete()
        print('rscript --vanilla run_jm.R '+jm_name+" "+market)
        os.system('rscript --vanilla run_jm.R '+jm_name+" "+market)
        await client.send_message(my_bot_ch,"https://docs.google.com/spreadsheets/d/1GWW0Q1RgMNAvSG7S4OyrbXSpcSHDnMSmd2uTsmZyJJE/edit#gid=1026403975")

    
    if event.message.message == '/deepl':
        start_buf = 0
        async for msg in client.iter_messages(my_bot_ch,reverse=True,offset_date=date_of_post):
            if "/st" in msg.message:
                txt_fn = msg.message.split(' ')[1]+'_'+msg.message.split(' ')[2]
                await msg.delete()
                #print("start reached")
                #await client.send_message(my_bot_ch,"start of txt")
                start_buf = 1
                txt_buf = ""
                #await client.send_message(my_bot_ch,txt_buf)
            elif '/deepl' in msg.message:
                print("end message")
                await msg.delete()
                #print(txt_buf)
                output_fn = txt_fn+'.txt'
                with open(output_fn, 'w',encoding='UTF-8') as modified: modified.write(txt_buf)
               

                tgt_fn = txt_fn 
                epub_title = "% " + tgt_fn + "\n"
                epub_fn = tgt_fn+'.epub'

                cover_nm = tgt_fn+'.png'
                fnt=font=ImageFont.truetype("arial.ttf",1200)
                image = Image.new(mode = "RGB", size = (6000,3000), color = "blue")
                draw = ImageDraw.Draw(image)
                draw.text((10,200), tgt_fn, font=fnt, fill=(255,255,0))
                new_img = image.rotate(-90,expand=True)
                new_img.save(cover_nm)

                with open(output_fn, 'r',encoding='UTF-8') as original: data = original.read()
                with open(output_fn, 'w',encoding='UTF-8') as modified: modified.write(epub_title+"# chapter one" + "\n"+ data)
        
                 

                pandoc_str='pandoc '+ output_fn+ " --epub-cover-image="+cover_nm + ' -o '+ epub_fn
                os.popen(pandoc_str)
                while not os.path.isfile(epub_fn):
                    print('waiting epub')
                    mes = await client.send_message(my_bot_ch, "waiting epub")
                    time.sleep(1.5)
                    await mes.delete()


                await client.send_file(my_bot_ch,epub_fn,caption='#'+tgt_fn)
                print("epub sent")
                mes = await client.send_message(my_bot_ch, "epub sent")
                time.sleep(2.5)
                await mes.delete()
                break

            else:
                #gather txt to translate to epub
                if start_buf:
                    txt_buf= txt_buf+msg.message
                    #print(txt_buf)

                if not '#' in msg.message:
                    await msg.delete()
    
    if event.message.message == '!perform':

        st_date = datetime.datetime(2023, 10, 1)
        awake_entity = await client.get_entity(awake_ch)

        async for msg in client.iter_messages(awake_entity,reverse=True,offset_date=st_date):
            for i in kwd_comp:
                kwd_tgt_pool=[i,kwd_prop]
                #print(i)
                if all(kwd_tgt in msg.message for kwd_tgt in kwd_tgt_pool) :
                #print(i)          
                #await client.forward_messages(my_bot_ch,msg)
                #await event.reply(i)
                #print(msg.message)
                    focusjm_list.loc[focusjm_list['corp_name']==i.strip(),'awake']=msg.message
            if kwd4df in msg.message:
                kwd_df_tmp.loc[0,kwd4df] = msg.message
                kwd_df = pd.concat([kwd_df,kwd_df_tmp])
            
            if '(잠정)실적' in msg.message:
                perf_df_tmp.loc[0,'timestamp'] = msg.message.splitlines()[0]
                corp_name = ((msg.message.splitlines()[1]).split(' ')[1]).split('(')[0]
                perf_df_tmp.loc[0,'corp'] = corp_name
                perf_df_tmp.loc[0,'rev'] = msg.message.splitlines()[4]
                perf_df_tmp.loc[0,'op'] = msg.message.splitlines()[5]

                
                perf_df_tmp.loc[0,'link'] = '=HYPERLINK("'+naver_url+mypkg.get_code(corp_name)+'",'+'"chart link"'+')'
                perf_df_tmp.loc[0,'stockfu'] = mypkg.issf(corp_name)
        
                perf_df = pd.concat([perf_df,perf_df_tmp])

        fn = 'focusjm_awake.xlsx'
    #test.to_csv(fn,encoding='euc-kr')
        focusjm_list.to_excel(excel_writer=fn)
        kwd_df.to_excel(excel_writer='kwd_awak'+kwd4df+'.xlsx')
        perf_df.to_excel(excel_writer='perf_awak_3q23.xlsx')
        print('performance update done')


@client.on(events.NewMessage(chats=pub_botch))
async def handler(event):
    txt_buf =""
    kwd_df = pd.DataFrame([])
    kwd_df_tmp = pd.DataFrame([])
    kwd4df = '기업설명회'
    await client.get_dialogs()
    date_of_post = datetime.datetime.today()-datetime.timedelta(days=1)
    #msgs=str(event)
    print(event.message.message)
    escape = 0
    
    #await event.reply('안녕!')
    #async for msg in client.iter_messages(awake_entity,3000):

    if '/help' in event.message.message:
        help_scr = (
                "'/live' bot 살아있는지 확인, 살아있으면 메시지 지워짐\n" 
                "'/br 종목명' 종목명 표시 종목 관련 Naver link, 사업보고서, 최신 리포트, 실적및" 
                    "rt_signal의 jm_char sheet에 볼린져밴드표시\n"
                "'/bb 종목명' 종목명 표시종목 볼린져밴드를 rt_signal의 jm_char sheet에 표시"
                )

        await client.send_message(pub_botch,help_scr)

    if '/test' in event.message.message:
        jm_name = event.message.message.split('_')[1]
        count_msg = 0
        
        async for msg in client.iter_messages(puzzle_ch,search="#"+jm_name):
            print(msg.id)
            await client.send_message(pub_botch,puzzle_ch+'/'+str(msg.id)+ ' #test')
            count_msg = count_msg + 1
            if count_msg == 3:
                break
    if '/live' in event.message.message:
        await event.message.delete()



    if '/init_jm' in event.message.message:
        #jm_name = event.message.message.split('_')[1]
        #await client.forward_messages(my_bot_ch,event.message)
        await client.send_message(pub_botch,"init gs jm")
        await event.message.delete()
        #print('python dart_freport_name_arg.py '+jm_name)
        os.system('rscript init_jm.R')
    if '/quit' in event.message.message:
        await event.message.delete()
        async for msg in client.iter_messages(pub_botch,offset_date=date_of_post,reverse=True):
            if "Bot is ready" in msg.message:
                await msg.delete()
        sys.exit()
 
    
    if '/br' in event.message.message:
        tgt_date = datetime.datetime.today().strftime("%Y%m%d")
        jm_name = event.message.message.split(' ')[1]
        comp_name = jm_name
        print(jm_name)
        #await client.forward_messages(pub_botch,event.message)
        await event.message.delete()
        print('python dart_freport_name_arg.py '+jm_name)
        
        #os.system('python dart_freport_name_arg.py '+jm_name)
        dart = OpenDartReader(api_key)
        # get stock code
        df_corp_codes = dart.corp_codes
        chkcorp = df_corp_codes['corp_name'] == comp_name
        chknnull = df_corp_codes['stock_code'] != ' '
        comp_code = df_corp_codes[chkcorp & chknnull]['stock_code']
        report_list=dart.list(corp=comp_code.iloc[0],start=start_date,end=tgt_date,kind='A',final=False)
        test = report_list.query('report_nm.str.contains("보고서")')
        test = test[~test.report_nm.str.contains("기재정정")]
        test = test[~test.report_nm.str.contains("첨부추가")]
        test = test[~test.report_nm.str.contains("첨부정정")]
        #print(test)
        #remove '=' for compatibility issue btw xlsx and R read_xl
        header_url = dart_url+test['rcept_no']
        test['url'] = header_url
        test['hyperlink'] = 'HYPERLINK("'+header_url+'",'+'"사업보고서"'+')'
        test['stock_code']=naver_url+test['stock_code']
        test['stock_code']='HYPERLINK("'+test['stock_code']+'",'+'"chart link"'+')'

        df_index = test.columns.tolist()
        df_index.remove('corp_name')
        df_index.remove('report_nm')
        df_index.remove('rcept_dt')
        df_index.remove('hyperlink')
        df_index.remove('stock_code')
        dart_br_fn = 'dart_br.xlsx'
        test=test.drop(df_index,axis=1)

        await client.send_message(pub_botch,test['stock_code'][0]+' '+test['hyperlink'][0] +" #"+comp_name)

        count_msg = 0

        report_df = pd.DataFrame([])
        report_df_tmp = pd.DataFrame([])
        
        async for msg in client.iter_messages(puzzle_ch,search="#"+jm_name):
            print(msg.id)
            await client.send_message(pub_botch,puzzle_ch+'/'+str(msg.id)+" #"+comp_name)
            test.loc[count_msg,'report'] = 'HYPERLINK("'+puzzle_ch+'/'+str(msg.id)+'")'
            count_msg = count_msg + 1
            if count_msg == 3:
                break



        awake_entity = await client.get_entity(awake_ch)
        #print(my_channel)
        kwd_df = pd.DataFrame([])
        kwd_df_tmp = pd.DataFrame([])

            
        comp_kwd = '최근 실적'
        #date_of_post = datetime.datetime(2023, 8, 1)
        date_of_post=datetime.datetime.today()-datetime.timedelta(days=1)
       
    
        async for msg in client.iter_messages(awake_entity,offset_date=date_of_post,search=comp_name):
           if comp_kwd in msg.message:
                    #print(msg.message)
                kwd_df_tmp.loc[0,kwd4df] = msg.message
                kwd_df = pd.concat([kwd_df,kwd_df_tmp])

        kwd_df=kwd_df.reset_index(drop=True)
        test['실적'] = kwd_df.iloc[0:4,0]
        await client.send_message(pub_botch,test['실적'][0]+" #"+comp_name)
        test.to_excel(excel_writer=dart_br_fn,index=False)
        sheet_nm = "IR2"

        ''' rpy2 sub pc windows 7 issue
        r_df = pandas2ri.py2rpy(test)

        robjects.globalenv["r_df"] = r_df

        robjects.r( multi line comments
            library(googlesheets4)
                  
            r_df$stock_code <- gs4_formula(r_df$stock_code)
            r_df$hyperlink<-gs4_formula(r_df$hyperlink)
                   
            
            gs4_auth(email = "coatle0@gmail.com")
            ssid_asset <- "1M0LjBg2tPZprA-BIvsOZXjNPyK_gKm4pY4Ns93gvgJo"
            range_clear(ssid_asset,sheet="IR2")
            range_write(ssid_asset,r_df,range="A1",col_names = TRUE,sheet = "IR2")

        multi line comments)
        '''
        
        
        os.system('rscript --vanilla xls2gs.R '+dart_br_fn+" "+sheet_nm+" br")
        #print(jm_name)
        #await client.forward_messages(my_bot_ch,event.message)
        #await event.message.delete()
        print('rscript run_jm.R '+jm_name+" KQ")
        os.system('rscript run_jm.R '+jm_name+" KQ")


    
    #bollinger band 
    if '/bb' in event.message.message:
        jm_name = event.message.message.split(' ')[1]
        market = event.message.message.split(' ')[2]
        
        #print(jm_name)
        #await client.forward_messages(my_bot_ch,event.message)
        await event.message.delete()
        print('rscript run_jm.R '+jm_name+" "+market)
        os.system('rscript --vanilla run_jm.R '+jm_name+" "+market)
        await client.forward_messages(pub_botch,'bbnd done')

    
    if event.message.message == '/deepl':
        start_buf = 0
        async for msg in client.iter_messages(pub_botch,reverse=True,offset_date=date_of_post):
            if "/st_" in msg.message:
                txt_fn = msg.message.split(' ')[1]+'_'+msg.message.split(' ')[2]
                await msg.delete()
                #print("start reached")
                #await client.send_message(my_bot_ch,"start of txt")
                start_buf = 1
                txt_buf = ""
                #await client.send_message(my_bot_ch,txt_buf)
            elif '/deepl' in msg.message:
                print("end message")
                await msg.delete()
                #print(txt_buf)
                output_fn = txt_fn+'.txt'
                with open(output_fn, 'w',encoding='UTF-8') as modified: modified.write(txt_buf)
               

                tgt_fn = txt_fn 
                epub_title = "% " + tgt_fn + "\n"
                epub_fn = tgt_fn+'.epub'

                cover_nm = tgt_fn+'.png'
                fnt=font=ImageFont.truetype("arial.ttf",1200)
                image = Image.new(mode = "RGB", size = (6000,3000), color = "blue")
                draw = ImageDraw.Draw(image)
                draw.text((10,200), tgt_fn, font=fnt, fill=(255,255,0))
                new_img = image.rotate(-90,expand=True)
                new_img.save(cover_nm)

                with open(output_fn, 'r',encoding='UTF-8') as original: data = original.read()
                with open(output_fn, 'w',encoding='UTF-8') as modified: modified.write(epub_title+"# chapter one" + "\n"+ data)
        
                 

                pandoc_str='pandoc '+ output_fn+ " --epub-cover-image="+cover_nm + ' -o '+ epub_fn
                os.popen(pandoc_str)
                while not os.path.isfile(epub_fn):
                    time.sleep(2.5)
                    print('waiting epub')


                await client.send_file(pub_botch,epub_fn,caption='#'+tgt_fn)
                print("epub sent")
                break

            else:
                #gather txt to translate to epub
                if start_buf:
                    txt_buf= txt_buf+msg.message
                    #print(txt_buf)

                if not '#' in msg.message:
                    await msg.delete()
    
    if event.message.message == '!perform':

        async for msg in client.iter_messages(awake_entity,reverse=True,offset_date=date_of_post):
            for i in kwd_comp:
                kwd_tgt_pool=[i,kwd_prop]
                #print(i)
                if all(kwd_tgt in msg.message for kwd_tgt in kwd_tgt_pool) :
                #print(i)          
                #await client.forward_messages(my_bot_ch,msg)
                #await event.reply(i)
                #print(msg.message)
                    focusjm_list.loc[focusjm_list['corp_name']==i.strip(),'awake']=msg.message
            if kwd4df in msg.message:
                kwd_df_tmp.loc[0,kwd4df] = msg.message
                kwd_df = pd.concat([kwd_df,kwd_df_tmp])

        fn = 'focusjm_awake.xlsx'
    #test.to_csv(fn,encoding='euc-kr')
        focusjm_list.to_excel(excel_writer=fn)
        kwd_df.to_excel(excel_writer='kwd_awak'+kwd4df+'.xlsx')


nest_asyncio.apply()
asyncio.run(Run_Telethon())
