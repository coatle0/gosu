import xlwings as xw
import os
import openpyxl
import pandas as pd
import sys

app = xw.App(visible=False)
ohlc_path ="C:/Users/coatle/Documents/tm_study/get_tm.xlsm"

comp_code =  sys.argv[1]

wb_ohlc = xw.Book(ohlc_path)
macro_run = wb_ohlc.macro("Button1_Click")
sheet_ohlc = wb_ohlc.sheets[0]

col_idx = 1
row_idx = 1

sheet_ohlc.range(row_idx,col_idx).value = comp_code
macro_run()
print(comp_code + "from VBA"+os.getcwd())
wb_ohlc.close()

tgt_scr = 'rscript C:/Users/coatle/gen_vsdfm_arg.R '+comp_code
os.system(tgt_scr)
