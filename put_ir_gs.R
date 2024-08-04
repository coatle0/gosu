library(readxl)
library(openxlsx)

IR_new <- read_excel("IR.xlsx")


ir_gs <-read_asgs_sheet('IR')
ir_rm<-ir_gs[which(ir_gs$check=='o'),]
ir_rm_ori <- read_excel("ir_rm.xlsx")
ir_rm_new<-rbind(ir_rm,ir_rm_ori)
write.xlsx(ir_rm_new,"ir_rm.xlsx",sheetName='IR',append=TRUE)
sc_ir<-anti_join(IR_new,ir_rm_new,by='rcept_no')
sc_ir$stock_code<-paste0('=',sc_ir$stock_code)
sc_ir$stock_code<-gs4_formula(sc_ir$stock_code)
sc_ir$hyperlink<-paste0('=',sc_ir$hyperlink)
sc_ir$hyperlink<-gs4_formula(sc_ir$hyperlink)

gs4_auth(email = "coatle0@gmail.com")
ssid_asset <- "1M0LjBg2tPZprA-BIvsOZXjNPyK_gKm4pY4Ns93gvgJo"
range_clear(ssid_asset,sheet='IR')
sheet_nm <- "IR"
range_write(ssid_asset,sc_ir,range="A1",col_names = TRUE,sheet = sheet_nm)
range_write(ssid_asset,data.frame('check'),range="I1",col_names = FALSE,sheet = sheet_nm)

