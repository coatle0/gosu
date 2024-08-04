tmenv <- new.env()
args=commandArgs(trailingOnly=TRUE)
x<-args[1]
ksmb_code <- x

print("read csv for vsdfm")
gen_vsdfm(ksmb_code)