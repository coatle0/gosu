library(googlesheets4)
library(mypkg)
library(lubridate)
library(quantmod)
library(PerformanceAnalytics)
library(telegram.bot)
library(tidyquant)

bot=Bot(token="5824250303:AAF30nE1zYlP28DzS-Gd69yAegN-LgHU_ag")
chat_id <- 1278251780

code<-code_get(fresh = TRUE)
bb_win_szl <- 20
bb_win_szs <- 8

args=commandArgs(trailingOnly=TRUE)
market<-args[2]
x<-args[1]

tqk_code<-code[match(x,code$name),3]$code
yahoo_code<-paste0(tqk_code,".KQ")
yahoo_code1<-paste0(tqk_code,".KS")

start_date<-today()-100

if (market=='k'){
    temp<-tryCatch(expr= tqk_get(tqk_code,from=start_date),
    error = function(e) na.omit(tq_get(yahoo_code, get = "stock.prices", from = start_date)[,2:7]),
    warning = function(e) na.omit(tq_get(yahoo_code1, get = "stock.prices", from = start_date)[,2:7]),
    warning = function(e) {print("wrong error code"); chk<-bot$send_message(chat_id,"wrong jm name");bot$delete_message(chat_id,chk$message_id); quit()})
    chk<-bot$send_message(chat_id,"ready to draw")
    temp$nvol <- (temp$volume-mean(temp$volume))/sd(temp$volume)
    temp_x<-xts(temp[,2:7],temp$date)
}else{
    temp<-get(getSymbols(x,from=start_date))[,1:5]
    colnames(temp) <- c('open','high','low','close','volume')
    temp$nvol <- (temp$volume-mean(temp$volume))/sd(temp$volume)
    temp_x<-temp
    chk<-bot$send_message(chat_id,"ready to draw")
}

#bb long calculate
temp_bbl <- BBands(temp_x[,c("high","low","close")],n=bb_win_szl)
temp_atrl <- ATR(temp_x[,c("high","low","close")],n=bb_win_szl)

#bb short calculate
#bb long calculate
temp_bbs <- BBands(temp_x[,c("high","low","close")],n=bb_win_szs)
temp_atrs <- ATR(temp_x[,c("high","low","close")],n=bb_win_szs)



temp_bbl$close<-temp_x$close



temp_bbl<-tail(temp_bbl,n=150)
temp_atrl <- tail(temp_atrl,n=150)

temp_bbl<-temp_bbl[,-4]

temp_bbs<-tail(temp_bbs,n=150)
temp_atrs <- tail(temp_atrs,n=150)


temp_bbl$temp_low <- temp_atrl$trueLow
temp_bbl$dn <- temp_bbs$dn
temp_bbl$nvol<-temp_x$nvol

#temp_bbs$temp_low <- temp_atrs$trueLow

temp_bb.df<-cbind(index(temp_bbl),data.frame(coredata(temp_bbl)))

colnames(temp_bb.df)<-paste0(x,colnames(temp_bb.df))


gs4_auth(email = "coatle0@gmail.com")
ssid <- "1GWW0Q1RgMNAvSG7S4OyrbXSpcSHDnMSmd2uTsmZyJJE"
range_clear(ssid,sheet='jm_char')
bot$delete_message(chat_id,chk$message_id)
range_write(ssid,temp_bb.df,range="A1",col_names = TRUE,sheet = "jm_char")


