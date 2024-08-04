library(telegram.bot)
bot=Bot(token="5824250303:AAF30nE1zYlP28DzS-Gd69yAegN-LgHU_ag")
chat_id <- 1278251780


#command to execute
#Yearly update
setwd('~')
tickerData <- new.env()


args=commandArgs(trailingOnly=TRUE)

qtr_ref_date <- args[1]
week_ref_date <- args[2]
idx_fn <- 'us_idx'
update_myuidx(qtr_ref_date,week_ref_date,idx_fn)

kidx_start = 5
ktickerData <- new.env()
data_start = "2022-12-05"
qtr_start = qtr_ref_date
week_start = week_ref_date
code<-code_get()

update_myidx(kidx_start,data_start,qtr_start,week_start)

#bot$sendMessage(chat_id = chat_id, text = 'index_updated')
#send_link<-"https://docs.google.com/spreadsheets/d/1Edz1EPV6hqBM2tMKSkA3zNmysmugMrAg1u2H3fheXaM/edit#gid=1183146127"
#bot$sendMessage(chat_id = chat_id, text = send_link)
