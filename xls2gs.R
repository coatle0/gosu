print('vanilla')
library(googlesheets4)
library(readxl)
library(openxlsx)

args=commandArgs(trailingOnly=TRUE)
print(args[2])
sheet_nm = args[2]
special_opt = args[3]
xlsx_fn<-args[1]

tgt_df <- read_excel(xlsx_fn)
#print(tgt_df)

if(special_opt=='br'){
    tgt_df$stock_code <- gs4_formula(paste0('=',tgt_df$stock_code))
    tgt_df$hyperlink<-gs4_formula(paste0('=',tgt_df$hyperlink))
    tgt_df$report<-gs4_formula(paste0('=',tgt_df$report))
    print('processing gs command')
}

gs4_auth(email = "coatle0@gmail.com")
ssid_asset <- "1M0LjBg2tPZprA-BIvsOZXjNPyK_gKm4pY4Ns93gvgJo"
range_clear(ssid_asset,sheet=sheet_nm)
range_write(ssid_asset,tgt_df,range="A1",col_names = TRUE,sheet = sheet_nm)
