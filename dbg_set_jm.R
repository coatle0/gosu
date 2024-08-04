args=commandArgs(trailingOnly=TRUE)
tgt_jm<-args[1]
  
gs4_auth(email = "coatle0@gmail.com")
ssid <- "1GWW0Q1RgMNAvSG7S4OyrbXSpcSHDnMSmd2uTsmZyJJE"
range_clear(ssid,sheet='dbg_day',range='A2:B')
range_write(ssid,as.data.frame(tgt_jm),range="A2",col_names = FALSE,sheet = "dbg_day")
range_write(ssid,as.data.frame(100),range="B2",col_names = FALSE,sheet = "dbg_day")