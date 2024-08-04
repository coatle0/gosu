setwd('~')
ktickerData <- new.env()
code<-code_get(fresh = TRUE)

bb_win_szl <- 20
bb_win_szs <- 8

idx_gs_lst <- read_gs_idx('mybiz')
kweight_lst<-idx_gs_lst[[2]]
ksmb_lst<-idx_gs_lst[[1]]

df_tmp <- list()

for (i in 1:length(ksmb_lst)){

start_date<- as.character(kweight_lst[[i]]-days(32))
ref_date <- as.character(kweight_lst[[i]])


lapply(ksmb_lst[[i]],function(x){ tqk_code<-code[match(x,code$name),3]$code;yahoo_code<-paste0(tqk_code,".KQ");
                        temp<-tryCatch(expr= tqk_get(tqk_code,from=start_date),
                        error = function(e) { print(paste0(x," new jm, using yahoo"));get_yahoo<-tq_get(yahoo_code, get = "stock.prices", from = start_date);return(get_yahoo[,2:7])},
                        warning = function(e) print("Warning") );
                        assign(x,xts(temp[,2:6],temp$date),envir=ktickerData)})

ref_xts <- get(ksmb_lst[[i]][1],envir=ktickerData)


temp_bbl <- BBands(ref_xts[,c("high","low","close")],n=bb_win_szl)
temp_atrl <- ATR(ref_xts[,c("high","low","close")],n=bb_win_szl)

temp_bbs <- BBands(ref_xts[,c("high","low","close")],n=bb_win_szs)
temp_atrs <- ATR(ref_xts[,c("high","low","close")],n=bb_win_szs)


temp_bbl$atrl <- temp_atrl$trueLow
temp_bbl$dn <- temp_bbs$dn
temp_bbl <- temp_bbl[,-4]




ref_prices=do.call(cbind,lapply(ksmb_lst[[i]],function(x) coredata(Cl(get(x,envir=ktickerData)[ref_date]))))

prices_run=do.call(cbind,lapply(ksmb_lst[[i]],function(x){print(x); coredata(Cl(get(x,envir = ktickerData)))}))

prices_run_idx = sweep(prices_run,2,ref_prices,'/')*100



colnames(prices_run_idx) <- ksmb_lst[[i]]

prices_run_idx_sort<-prices_run_idx[,(order(colSums(tail(prices_run_idx[,-1])),decreasing = T)+1)[1:2]]

prices_run_idx_sort<- cbind(prices_run_idx[,1],prices_run_idx_sort)
colnames(prices_run_idx_sort)[1] <- ksmb_lst[[i]][1]
temp_bbl <- (temp_bbl/ref_prices[1])*100

xts_tmp <- cbind(temp_bbl,prices_run_idx_sort)

df_tmp[[i]] <- data.frame(date=index(xts_tmp),coredata(xts_tmp))
}




maxlen <- max(unlist(lapply(df_tmp,dim)))

tmp <-do.call(cbind,lapply(df_tmp,function(x){fillrow<-maxlen-nrow(x);if(fillrow != 0) x[(nrow(x)+1):(nrow(x)+fillrow),]<-NA;x}))

write_asgs_sheet(tmp,"shield","A1")