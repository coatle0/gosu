library(telegram.bot)
bot=Bot(token="5824250303:AAF30nE1zYlP28DzS-Gd69yAegN-LgHU_ag")
chat_id <- 1278251780

bot_gosu = Bot(token = "7297044765:AAHxCAZ_ETjoG3lyDTkvggM3i4drCL_5Y4g")

args=commandArgs(trailingOnly=TRUE)

msg_text <- args[1]


bot$sendMessage(chat_id = chat_id, text =msg_text)

bot_gosu$sendMessage(chat_id = chat_id, text =msg_text)



