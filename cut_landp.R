#initialize set up
library(telegram.bot)
bot=Bot(token="5824250303:AAF30nE1zYlP28DzS-Gd69yAegN-LgHU_ag")
chat_id <- 1278251780
setwd("~/tm_study")
tmenv <- new.env()

code<-code_get(fresh = TRUE)

#get my pf list
pf_tbl <- read_asgs_sheet('portf_rt')
nofkjm <- which(pf_tbl$jm=='US')-1
nofusjm <- which(pf_tbl$jm=='Renesas')-1

pfsmb_ary <- pf_tbl$jm[1:nofkjm]
pf_us_lst <- pf_tbl$jm[(nofkjm+2):nofusjm]

pf_smb_bb<-lapply(pfsmb_ary,function(x){tqk_code<-code[match(x,code$name),3]$code;

yahoo_code<-paste0(tqk_code,".KQ")
yahoo_code1<-paste0(tqk_code,".KS")

start_date<-today()-100
temp<-tryCatch(expr= tqk_get(tqk_code,from=start_date),
error = function(e) na.omit(tq_get(yahoo_code, get = "stock.prices", from = start_date)[,2:7]),
warning = function(e) na.omit(tq_get(yahoo_code1, get = "stock.prices", from = start_date)[,2:7]),
warning = function(e) print("wrong error code") )

temp_x<-xts(temp[,2:6],temp$date);


temp_bbl <- BBands(temp_x[,c("high","low","close")],n=20);
temp_bbs <- BBands(temp_x[,c("high","low","close")],n=8);

return(c(coredata(tail(temp_bbs$dn,n=1)$dn)*1.015,coredata(tail(temp_bbl$up,n=1)$up)*1.03,0))
}
)

names(pf_smb_bb)<-pfsmb_ary

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
    return(c(coredata(tail(temp_bbs$dn,n=1)$dn)*1.015,coredata(tail(temp_bbl$up,n=1)$up)*1.03,0))
    #return(temp_bbl)
}
)
names(pf_us_bb)<-t(pf_us_lst)

pf_us_exit <-data.frame(t(floor(bind_rows(pf_us_bb)*100)/100))
pf_smb_exit <-data.frame(t(floor(bind_rows(pf_smb_bb))))
pf_losscut_df<-rbind(pf_smb_exit,NA,pf_us_exit)
write_asgs_sheet(pf_losscut_df,'losscut','A1')


while(TRUE) {



volmon <- read.csv("~/volmon.csv")
temp_bb<-lapply(pfsmb_ary,function(x){ tgt_close = volmon[volmon$code_name==x,4];
  if(tgt_close < pf_smb_bb[[x]][1]){print(paste0(x,"loss cut",tgt_close,'@',pf_smb_bb[[x]][1])); 
    if( pf_smb_bb[[x]][3] ==0){
      mes<-bot$sendMessage(chat_id = chat_id, text = paste0(x,"loss cut",tgt_close,'@',as.integer(pf_smb_bb[[x]][1])));
      pf_smb_bb[[x]][3]<-mes$message_id
    }
    return(pf_smb_bb[[x]])
  }else if(tgt_close > pf_smb_bb[[x]][2]){print(paste0(x,"profit cut",tgt_close,'@',pf_smb_bb[[x]][2])); 
    if(pf_smb_bb[[x]][3] ==0){
      mes<-bot$sendMessage(chat_id = chat_id, text = paste0(x,"profit cut",tgt_close,'@',as.integer(pf_smb_bb[[x]][2])));
      pf_smb_bb[[x]][3]<-mes$message_id
    }
    return(pf_smb_bb[[x]])
    }else{
      return(pf_smb_bb[[x]])
    }

  }
)

names(temp_bb)<-pfsmb_ary
pf_smb_bb <- temp_bb

Sys.sleep(180)

}