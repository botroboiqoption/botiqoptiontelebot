import telebot
import time
from iqoptionapi.stable_api import IQ_Option
import json
from datetime import datetime
API = IQ_Option("email","senha")
API.connect()

bot = telebot.TeleBot('token')

@bot.message_handler(commands=['analitic'])
def analitic(session):
    trader = str(session.text).split()
    par = trader[1] # paridade
    timec = int(trader[2]) # time candle 1 5 15 min
    oscdif = 30
    msgid = 0
    while True:
        # Info Oscillators
        oscHold = 0 
        oscShell = 0
        oscBuy = 0
        # Info Moving Averages
        mavHold = 0 
        mavShell = 0
        mavBuy = 0
        indicators = API.get_technical_indicators(par)
        for data in indicators:                    
            if data['candle_size'] == (timec * 60):
                if data['group'] == 'OSCILLATORS':
                    oscHold = oscHold + str(data).count('hold')
                    oscShell = oscShell + str(data).count('sell')
                    oscBuy = oscBuy + str(data).count('buy')                    
                if data['group'] == 'MOVING AVERAGES':
                    mavHold = mavHold + str(data).count('hold')
                    mavShell = mavShell + str(data).count('sell')
                    mavBuy = mavBuy + str(data).count('buy')                    
        if oscdif != mavBuy:
            oscdif = mavBuy
            if msgid > 0: bot.delete_message(session.chat.id, msgid)
            message = bot.send_message(session.chat.id, '###### ANALITIC IQ OPTION ######\n\n           Hora da Atualização: '+str(((datetime.now()).strftime('%H:%M:%S')))+'\n\nMOVING AVERAGES\nCompra: '+str(mavBuy)+'\nVenda: '+str(mavShell)+'\nAguarda: '+str(mavHold)+'\n\nOSCILLATORS\nCompra: '+str(oscBuy)+'\nVenda: '+str(oscShell)+'\nAguarda: '+str(oscHold)+'\n\n##### PAR: '+str(par)+'| EXP: '+str(timec)+' Min #####')
            msgid = message.message_id
        time.sleep(1) 


bot.polling()
