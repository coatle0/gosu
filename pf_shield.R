ktickerData <- new.env()
utickerData <- new.env()
start_date <- '2023-05-26'
pf_tbl <- read_asgs_sheet('portf')
nofjm <- which(pf_tbl$jm=='현금')-1

usd_ex <- unlist(pf_tbl$Tiker[which(pf_tbl$jm=="usd")])
jpy_ex <- unlist(pf_tbl$Tiker[which(pf_tbl$jm=="jpy")])

pf_tbl_dut<-cbind(pf_tbl$jm[1:nofjm],do.call(rbind, str_split(pf_tbl$Tiker[1:nofjm], ':'))[,2],pf_tbl$ex[1:nofjm],as.integer(pf_tbl$nofs[1:nofjm]))
colnames(pf_tbl_dut) <- c("jm","ticker",'ex','nofs')
pf_tbl_dut <- as.data.frame(pf_tbl_dut)
#korean asset estimation
lapply(pf_tbl_dut$jm[pf_tbl_dut$ex=='KRW'],function(x){ tqk_code<-code[match(x,code$name),3]$code;yahoo_code<-paste0(tqk_code,".KQ");
temp<-tryCatch(expr= tqk_get(tqk_code,from=start_date),
               error = function(e) { print(paste0(x," new jm, using yahoo"));get_yahoo<-tq_get(yahoo_code, get = "stock.prices", from = start_date);return(get_yahoo[,2:7])},
               warning = function(e) print("Warning") );
assign(x,xts(temp[,2:6],temp$date),envir=ktickerData)})

kcl_lst <- lapply(pf_tbl_dut$jm[pf_tbl_dut$ex=='KRW'],function(x) Cl(get(x,envir = ktickerData)))

kcl_lst_mul<-Map('*',kcl_lst,as.integer(pf_tbl_dut$nofs[pf_tbl_dut$ex=='KRW']))
kcl_lst_lsum <- Reduce('+',kcl_lst_mul)

#us asset estimation

lapply(pf_tbl_dut$ticker[pf_tbl_dut$ex=='USD'],function(x) getSymbols(x,src='yahoo',env=utickerData,from=start_date))
ucl_lst <- lapply(pf_tbl_dut$ticker[pf_tbl_dut$ex=='USD'],function(x) Cl(get(x,envir = utickerData)))
ucl_lst_mul<-Map('*',ucl_lst,as.integer(pf_tbl_dut$nofs[pf_tbl_dut$ex=='USD']))
ucl_lst_lsum <- Reduce('+',ucl_lst_mul)
ucl_lst_lsum <- ucl_lst_lsum * usd_ex

#jpy asset estimation

lapply(pf_tbl_dut$ticker[pf_tbl_dut$ex=='JPY'],function(x) getSymbols.yahooj(paste0('YJ',x,'.T'),src='yahoo',env=utickerData,from=start_date))
jcl_lst <- lapply(pf_tbl_dut$ticker[pf_tbl_dut$ex=='JPY'],function(x) Cl(get(paste0('YJ',x,'.T'),envir = utickerData)))
jcl_lst_mul<-Map('*',jcl_lst,as.integer(pf_tbl_dut$nofs[pf_tbl_dut$ex=='JPY']))
jcl_lst_lsum <- Reduce('+',jcl_lst_mul)
jcl_lst_lsum <- jcl_lst_lsum * jpy_ex

pf_sum <- kcl_lst_lsum+ucl_lst_lsum+jcl_lst_lsum
