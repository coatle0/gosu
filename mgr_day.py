import xlwings as xw
import os
import openpyxl
import pandas as pd


ohlc_path ="C:/Users/coatle/Documents/tm_study/get_tm.xlsm"
volmon_path = "C:/Users/coatle/Desktop/volmon.xlsm"
jm_list_path = "c:/Users/coatle/Desktop/test_vq.csv"
jm_new_path = "C:/Users/coatle/Documents/ksmb_code.csv"

app = xw.App(visible=False)


#run rscript to get jm list and jm to get 5m data
os.system('rscript --vanilla init_jm.R')


#confused


jm_new = pd.read_csv(jm_new_path)

col_idx = 1
row_idx = 1

if jm_new.shape[0] != 0:
    wb_ohlc = xw.Book(ohlc_path)
    macro_run = wb_ohlc.macro("Button1_Click")
    sheet_ohlc = wb_ohlc.sheets[0]
    for jm in jm_new['x']:
        sheet_ohlc.range(row_idx,col_idx).value = jm
        macro_run()
        print(jm)
    
    print("get all new jm")    
    os.system('rscript gen_vsdfm.R')
print("ohlc update done")

app = xw.App(visible=True)
wb_volmon = xw.Book(volmon_path)
macro_focus = wb_volmon.macro("focusjm_Click")
sheet_volmon = wb_volmon.sheets[1]

jm_list = pd.read_csv(jm_list_path)

sheet_volmon.range('Q:Q').clear()
sheet_volmon.range('Q1').options(pd.DataFrame, index=False).value = jm_list

macro_focus()
test=sheet_volmon.range('A12').options(pd.DataFrame, index=False, header=True, expand='table').value