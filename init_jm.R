
library(googlesheets4)
library(tqk)
library(mypkg)
library(telegram.bot)
bot=Bot(token="5824250303:AAF30nE1zYlP28DzS-Gd69yAegN-LgHU_ag")
chat_id <- 1278251780

chk<-bot$send_message(chat_id,"starting jm code get")

setwd("~/tm_study")
#shell('get_tm.xlsm',wait = FALSE)
tmenv <- new.env()

code<-code_get()


#tm_stamp <- read.csv("tm_stamp_fm.csv")
#tm_idx <- read.csv("tm_idx_fm.csv")
#browseURL("https://docs.google.com/spreadsheets/d/1GWW0Q1RgMNAvSG7S4OyrbXSpcSHDnMSmd2uTsmZyJJE/edit#gid=292053813")
#get market index list
idx_fn <- 'kr_idx'
idx_gs_lst <- read_gs_idx(idx_fn)
kweight_lst<-idx_gs_lst[[2]]

ksmb_lst<-idx_gs_lst[[1]]

#get my pf list
pf_fn <- 'pf_idx'
pf_gs_lst <- read_rtgs_idx(pf_fn)
pfwt_lst<-pf_gs_lst[[2]]

pfsmb_lst<-pf_gs_lst[[1]]

#get every day focus jm list
focus_fn <- 'focus_idx'
fs_gs_lst <- read_rtgs_idx(focus_fn)
fswt_lst<-fs_gs_lst[[2]]

fssmb_lst<-fs_gs_lst[[1]]

smb_lst<-c(ksmb_lst,pfsmb_lst,fssmb_lst)

ksmb_code_lst <- lapply(smb_lst,function(x) lapply(x, function(x) paste0('A',code[match(x,code$name),3]$code)))
bot$delete_message(chat_id,chk$message_id)
ksmb_code_vt<-t(as.data.frame(ksmb_code_lst))
ksmb_code_vt_uq<-unique(ksmb_code_vt)
#write excel file for monitoring file list
writexl::write_xlsx(data.frame(ksmb_code_vt_uq), path = "c:/Users/coatle/Desktop/test_vq.xlsx")
write.csv(ksmb_code_vt_uq, file = "c:/Users/coatle/Desktop/test_vq.csv",row.names = FALSE)

# write code to gs to set up volmon VBA
gs4_auth(email = "coatle0@gmail.com")
ssid <- "1GWW0Q1RgMNAvSG7S4OyrbXSpcSHDnMSmd2uTsmZyJJE"
range_clear(ssid,sheet='ksmb_code')
chk<-bot$send_message(chat_id,"write to ksmb_code")
range_write(ssid,as.data.frame(ksmb_code_vt_uq),range="A1",col_names = TRUE,sheet = "ksmb_code")
bot$delete_message(chat_id,chk$message_id)

#cat("step1> copy jm list from googlesheet to excel volmon")
#cat("step2> press focus button to check jm list")
#cat("step3> press redo button to run continuous monitoring")

#sanity check
vsdfm_fl <- dir(pattern='vsdfm')
vsdfm_fl <- substr(vsdfm_fl,1,7)

ksmb_nd2get<-ksmb_code_vt_uq[!(ksmb_code_vt_uq[,1] %in% vsdfm_fl),1]
#print("jm list for gather ohlc min")
print(ksmb_nd2get)

write.csv(ksmb_nd2get, file = "~/ksmb_code.csv",row.names = FALSE)

#cat("run VBA get_tm to download ten minute OHLC and press enter")
#result <- scan("stdin", character(), n=1)

#gen_vsdfm(ksmb_nd2get)

#source("vmon_start.R")
