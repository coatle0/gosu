library(googlesheets4)
library(tqk)
library(mypkg)
library(lubridate)
library(quantmod)
library(PerformanceAnalytics)
library(telegram.bot)
library(tidyquant)


bot=Bot(token="5824250303:AAF30nE1zYlP28DzS-Gd69yAegN-LgHU_ag")
chat_id <- 1278251780

code<-code_get()
bb_win_szl <- 20
bb_win_szs <- 8

start_date<-today()-180

#get us pf list
#pf_us_sht <- "usport"
#pf_us_lst <- read_asgs_sheet(pf_us_sht)

#get jm new 23-12-25
pf_tbl <- read_asgs_sheet('portf_rt')
nofkjm <- which(pf_tbl$jm=='US')-1
nofusjm <- which(pf_tbl$jm=='Renesas')-1

pf_us_lst <- pf_tbl$jm[(nofkjm+2):nofusjm]

pf_us_bb<-lapply(t(pf_us_lst),function(x){print(x);

temp<-get(getSymbols(x,from=start_date))[,1:5];
    colnames(temp) <- c('open','high','low','close','volume');

    temp_x<-temp;

#bb long calculate
    temp_bbl <- BBands(temp_x[,c("high","low","close")],n=bb_win_szl)
    temp_atrl <- ATR(temp_x[,c("high","low","close")],n=bb_win_szl)

#bb short calculate
#bb long calculate
    temp_bbs <- BBands(temp_x[,c("high","low","close")],n=bb_win_szs)
    temp_atrs <- ATR(temp_x[,c("high","low","close")],n=bb_win_szs)

    temp_bbl$close<-temp_x$close



    temp_bbl<-tail(temp_bbl,n=120)
    temp_atrl <- tail(temp_atrl,n=120)

    temp_bbl<-temp_bbl[,-4]

    temp_bbs<-tail(temp_bbs,n=120)
    temp_atrs <- tail(temp_atrs,n=120)


    temp_bbl$atrl <- temp_atrl$trueLow
    temp_bbl$dn <- temp_bbs$dn
    temp_bbl$nvol<-temp_x$nvol

#colnames(temp_bbl)<-paste0(x,colnames(temp_bbl))
    return(temp_bbl)
}
)
names(pf_us_bb)<-t(pf_us_lst)

pf_us_bb.df <- do.call(cbind,lapply(pf_us_bb,function(x){data.frame(date=index(x),coredata(x))}))

write_asgs_sheet(pf_us_bb.df,"pf_us_bb","A1")

#get my kor pf list
#pf_fn <- 'pf_idx'
#pf_gs_lst <- read_rtgs_idx(pf_fn)
#pfwt_lst<-pf_gs_lst[[2]]

#pfsmb_lst<-pf_gs_lst[[1]]
#pfsmb_ary<-unlist(pfsmb_lst)

#get kor jm list 231225
pfsmb_ary <- pf_us_lst <- pf_tbl$jm[1:nofkjm]
pf_smb_bb<-lapply(pfsmb_ary,function(x){tqk_code<-code[match(x,code$name),3]$code;

yahoo_code<-paste0(tqk_code,".KQ")
yahoo_code1<-paste0(tqk_code,".KS")


temp<-tryCatch(expr= tqk_get(tqk_code,from=start_date),
error = function(e) na.omit(tq_get(yahoo_code, get = "stock.prices", from = start_date)[,2:7]),
warning = function(e) na.omit(tq_get(yahoo_code1, get = "stock.prices", from = start_date)[,2:7]),
warning = function(e) print("wrong error code") )

temp$nvol <- (temp$volume-mean(temp$volume))/sd(temp$volume)
temp_x<-xts(temp[,2:6],temp$date);

#bb long calculate
temp_bbl <- BBands(temp_x[,c("high","low","close")],n=bb_win_szl)
temp_atrl <- ATR(temp_x[,c("high","low","close")],n=bb_win_szl)

#bb short calculate
#bb long calculate
temp_bbs <- BBands(temp_x[,c("high","low","close")],n=bb_win_szs)
temp_atrs <- ATR(temp_x[,c("high","low","close")],n=bb_win_szs)



temp_bbl$close<-temp_x$close



temp_bbl<-tail(temp_bbl,n=120)
temp_atrl <- tail(temp_atrl,n=120)

temp_bbl<-temp_bbl[,-4]

temp_bbs<-tail(temp_bbs,n=120)
temp_atrs <- tail(temp_atrs,n=120)


temp_bbl$atrl <- temp_atrl$trueLow
temp_bbl$dn <- temp_bbs$dn
temp_bbl$nvol<-temp_x$nvol

#colnames(temp_bbl)<-paste0(x,colnames(temp_bbl))
return(temp_bbl)
}
)
names(pf_smb_bb)<-pfsmb_ary

chk<-bot$send_message(chat_id,"ready to draw")
row_min <- min(unlist(lapply(lapply(pf_smb_bb,dim),function(x) x[1])))
pf_smb_bb <-lapply(pf_smb_bb,function(x) tail(x,n=row_min))

pf_smb_bb.df <- do.call(cbind,lapply(pf_smb_bb,function(x){data.frame(date=index(x),coredata(x))}))

write_asgs_sheet(pf_smb_bb.df,"pf_kor_bb","A1")


