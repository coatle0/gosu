library(mypkg)

pf_tbl <- read_asgs_sheet('portf')

assetman_tbl <- read_asgs_sheet('assetman')
assetman_tbl$date<- as.character(assetman_tbl$date)

today_str<-as.character(today())
asset_total <- as.integer(pf_tbl$ps_close[which(pf_tbl$jm=='Total')])
asset_top4 <- round(sum(na.omit(pf_tbl$pshare[pf_tbl$Top4=='top4'])),3)
asset_top8 <- round(sum(na.omit(pf_tbl$pshare[pf_tbl$Top4=='top8'])),3)
asset_top12 <- round(sum(na.omit(pf_tbl$pshare[pf_tbl$Top4=='top12'])),3)
asset_indy <- round(sum(na.omit(pf_tbl$pshare[pf_tbl$Top4=='indy'])),3)
asset_cash <- round(sum(na.omit(pf_tbl$pshare[pf_tbl$sector=='cash'])),3)

assetman_temp<-data.frame(today_str,asset_total,asset_top4,asset_top8,
                     asset_top12,asset_indy,asset_cash,round(asset_total/assetman_tbl$total[1],2))
colnames(assetman_temp)<- colnames(assetman_tbl)
assetman_tbl<-rbind(assetman_tbl,assetman_temp)

write_asgs_sheet(assetman_tbl,'assetman','A1')