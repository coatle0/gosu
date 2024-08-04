#use open Dart reader

import OpenDartReader
from datetime import datetime,timedelta,date
import pandas as pd
import openpyxl
import os
from fd_dart_mod import crawl_url2
import time
import re
import mypkg
import requests

# ==== 0. 객체 생성 ====
# 객체 생성 (API KEY 지정)
api_key = '61b268a6147bf74f5b549a99bff5ea2974e011b2'

dart = OpenDartReader(api_key)

#start_date = input("input start date:")
tgt_date = datetime.today().strftime("%Y%m%d")
#tgt_date = input("input end date:")
start_date = date.today() - timedelta(5)
start_date = start_date.strftime("%Y%m%d")
list=dart.list(start=start_date,end=tgt_date,kind='I')
list1= dart.list(start=start_date,end=tgt_date,kind='A')


dart_url = 'https://dart.fss.or.kr/dsaf001/main.do?rcpNo='
naver_url = 'https://finance.naver.com/item/fchart.naver?code='
#test = list.query('report_nm.str.contains("잠정")')
test=list.query('report_nm.str.contains("기업설명회|결산실적")')
#test=test[test.report_nm.str.contains("IR")]

tgt_url = dart_url+test['rcept_no']
test['flr_nm'] = tgt_url
#test['hyperlink'] = tgt_url
#test['hyperlink'] = '=HYPERLINK("'+tgt_url+'")'
test['hyperlink'] = 'HYPERLINK("'+tgt_url+'","IR")'


test['stock_code']=naver_url+test['stock_code']
test['stock_code']='HYPERLINK("'+test['stock_code']+'",'+'"chart link"'+')'

df_index = test.columns.tolist()
df_index.remove('corp_name')
df_index.remove('rcept_no')
df_index.remove('report_nm')
df_index.remove('rcept_dt')
df_index.remove('hyperlink')
df_index.remove('stock_code')
df_index.remove('flr_nm')

test=test.drop(df_index,axis=1)
test['stockfu']='True'

rlt_df = pd.DataFrame()
rtl_df = test

fn = "IR.xlsx"
fn_csv="IR.csv"
#test.to_csv(fn,encoding='euc-kr')
rtl_df.to_excel(excel_writer=fn,index=False)

#pattern to search


for i in range (0,test.shape[0]):
#for i in range (0,5):
    #url = tgt_url.iloc[i]
    test['stockfu'].iloc[i] = mypkg.issf(test['corp_name'].iloc[i])
    
    rcp_no = test['rcept_no'].iloc[i]
    pt= "\t\tviewDoc\(\""+rcp_no+"\", \""+"\d+\""
    r = requests.get(f'http://dart.fss.or.kr/dsaf001/main.do?rcpNo={rcp_no}')
    matches = re.findall(pt, r.text)
    matches_list=matches[0].split('"')
    params = f'rcpNo={rcp_no}&dcmNo={matches_list[3]}&eleId=0&offset=0&length=0&dtd=HTML'
    doc_url = f'http://dart.fss.or.kr/report/viewer.do?{params}'
    print(i)
    print(test['corp_name'].iloc[i])

    if (test['corp_name'].iloc[i] != '라피치') and (test['corp_name'].iloc[i] != '루트락'):
        try:
            table2 = pd.read_html(doc_url, match = '시작일', header=0,encoding='euc-kr')
            txt_buf=table2[0][0:4].to_string()
            test['flr_nm'].iloc[i] = txt_buf
        except ValueError:
            table2 = pd.read_html(doc_url, match = '일시', header=0,encoding='euc-kr')
            txt_buf=table2[0][0:4].to_string()
            test['flr_nm'].iloc[i] = txt_buf
        except ValueError:
            table2 = pd.read_html(doc_url, match = '결정일자', header=0,encoding='euc-kr')
            txt_buf=table2[0][0:4].to_string()
            test['flr_nm'].iloc[i] = txt_buf    
        except ValueError:
            table2 = pd.read_html(doc_url, match = '해당기간', header=0,encoding='euc-kr')
            txt_buf=table2[0][0:4].to_string()
            test['flr_nm'].iloc[i] = txt_buf     
        except ValueError:
            print(test.iloc[i,])
    
    time.sleep(3)

test.to_excel(excel_writer=fn,index=False)
os.system('rscript put_ir_gs.R')

