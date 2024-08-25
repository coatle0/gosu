setwd('~')
tickerData <- new.env()


args=commandArgs(trailingOnly=TRUE)

#shell('rscript tele_single.R update_index',wait = TRUE)
qtr_ref_date <- args[1]
week_ref_date <- args[2]
idx_fn <- 'us_idx'
update_myuidx(qtr_ref_date,week_ref_date,idx_fn)
