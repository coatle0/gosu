import requests
import os
import re
import csv
import pandas as pd

import collections
collections.Callable = collections.abc.Callable
from bs4 import BeautifulSoup                            # for html parser
from urllib.request import urlopen                       # for html request/respone
import pandas as pd                                      # for DataFrame
from html_table_parser import parser_functions as parser #for parsing
import webbrowser

#import OpenDartReader

def merge_list(*args, fill_value = None):
    max_length = max([len(lst) for lst in args])
    merged = []
    for i in range(max_length):
        merged.append([
        args[k][i] if i < len(args[k]) else fill_value for k in range(len(args))])
    return merged

def crawl_url(url):

#url = "http://dart.fss.or.kr/dsaf001/main.do?rcpNo=20210513000114"
#url= "http://dart.fss.or.kr/pdf/download/main.do?rcp_no=20210513000114&dcm_no=8065508"
    r = requests.get(url)
    #print (r.text)

    reg_link = re.compile('viewDoc\((.*)\);}')
    
    reg_link_dl = re.compile('Download\((.*)\);')
    
    reg_link_text = re.compile('node1\[\'text\'\] = (.*);')
    reg_link_rcpNo = re.compile('node1\[\'rcpNo\'\] = \"(.*)";')
    reg_link_dcmNo = re.compile('node1\[\'dcmNo\'\] = \"(.*)";')
    reg_link_eleId = re.compile('node1\[\'eleId\'\] = \"(.*)";')
    reg_link_offset = re.compile('node1\[\'offset\'\] = \"(.*)";')
    reg_link_length = re.compile('node1\[\'length\'\] = \"(.*)";')
    reg_link_dtd = re.compile('node1\[\'dtd\'\] = \"(.*)";')
    

    p_contents = re.compile(r'text:(.*?)\sid:\s"([0-9]{1,2})",', re.DOTALL)


    params = []
    
    matches_link_dl = reg_link_dl.findall(r.text)
    
    matches_link_text = reg_link_text.findall(r.text)
    matches_link_rcpNo = reg_link_rcpNo.findall(r.text)
    matches_link_dcmNo = reg_link_dcmNo.findall(r.text)
    matches_link_eleId = reg_link_eleId.findall(r.text)
    matches_link_offset = reg_link_offset.findall(r.text)
    matches_link_length = reg_link_length.findall(r.text)
    matches_link_dtd = reg_link_dtd.findall(r.text)
    
    merged_lst= merge_list(matches_link_rcpNo,matches_link_dcmNo,matches_link_eleId,matches_link_offset,matches_link_length,matches_link_dtd)
    
    matches_link_dl = matches_link_dl[0].replace("'", "").replace(" ", "").split(",")
    
    
    #print(merged_lst)



    doc_url_tmpl = "http://dart.fss.or.kr/report/viewer.do?rcpNo=%s&dcmNo=%s&eleId=%s&offset=%s&length=%s&dtd=%s"
    
    dl_url_tmpl = "http://dart.fss.or.kr/pdf/download/main.do?rcp_no=%s&dcm_no=%s"

    con_link =[]
    
    dl_url = dl_url_tmpl % tuple(matches_link_dl)
    
    dl_r = requests.get(dl_url)
    
    dl_link = []
    dl_fn = []
    
    soup = BeautifulSoup(dl_r.text,'html.parser')
    

    for j in soup.find_all('a',class_= 'btnFile'):        # parsing btnFile calss
        dl_link.append(j.get('href'))
    
    for k in soup.find_all('td',class_= 'tL'):
        dl_fn.append(k.get_text())
    dl_link = ['http://dart.fss.or.kr'+ s for s in dl_link] 
    
    for p,q in zip(merged_lst,matches_link_text):
        con_link.append([q,doc_url_tmpl % tuple(p)])


    #print(con_link)

    df = pd.DataFrame(con_link)
    #print(df)
    #df.to_csv("test.csv",header=None,index=None,encoding ='utf-8-sig')
    return [df,dl_link,dl_fn]

def crawl_url2(url):

#url = "http://dart.fss.or.kr/dsaf001/main.do?rcpNo=20210513000114"
#url= "http://dart.fss.or.kr/pdf/download/main.do?rcp_no=20210513000114&dcm_no=8065508"
    r = requests.get(url)
    #print (r.text)

    reg_link = re.compile('viewDoc\(\'(.*)\);')
    
    matches_link = reg_link.findall(r.text)
    matches_link = reg_link.findall(r.text)
    matches_link = matches_link[0].replace("'", "").replace(" ", "").split(",")
    
    doc_url_tmpl = "https://dart.fss.or.kr/report/viewer.do?rcpNo=%s&dcmNo=%s&eleId=%s&offset=%s&length=%s&dtd=%s"
    
    doc_url = doc_url_tmpl % tuple(matches_link[0:6])
    #print(doc_url)
    
    return [doc_url]

def pick_tbl_df(tgt_url,match_word):

    #tgt_url = "http://dart.fss.or.kr/report/viewer.do?rcpNo=20210517000067&dcmNo=8071040&eleId=11&offset=93068&length=98079&dtd=dart3.xsd"
    table_attribute = BeautifulSoup(urlopen(tgt_url).read(), 'html.parser')
    try:
        table_pr = pd.read_html(tgt_url, match = match_word, header=0, encoding='utf-8')
    except ValueError:
        table_pr = [pd.DataFrame(),pd.DataFrame()]
    #table_up = pd.read_html(tgt_url, match = '구체적용도', header=0, encoding='utf-8')

    return table_pr

def pick_tbl_df1(tgt_url,match_word):

    #tgt_url = "http://dart.fss.or.kr/report/viewer.do?rcpNo=20210517000067&dcmNo=8071040&eleId=11&offset=93068&length=98079&dtd=dart3.xsd"
    table_attribute = BeautifulSoup(urlopen(tgt_url).read(), 'html.parser')
    try:
        page = requests.get(tgt_url)
        table_pr = pd.read_html(page.text.replace('<BR/>',''), match = match_word, header=0, encoding='utf-8')
    except ValueError:
        table_pr = [pd.DataFrame(),pd.DataFrame()]
    #table_up = pd.read_html(tgt_url, match = '구체적용도', header=0, encoding='utf-8')

    return table_pr