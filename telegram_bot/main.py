import logging
import requests
import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! What's your name?")
    name = (update.message.text).capitalize()
    reply = "How can i help you {}?".format(name)
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply)

def commands(update, context):
    reply = "/covid - for covid statistics global and by country "
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply)

def summary(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Enter which country or global for world statistics")
    dispatcher.add_handler(MessageHandler(Filters.text, summary_validation))

def summary_validation(update, context):
    reply = (update.message.text).capitalize()
    if(reply == "Global"):
        response = requests.get('https://api.covid19api.com/summary')
        data = response.json()
        if(response.status_code==200): #If everything went well
            if(data[reply]):
                global_reply = "Global Cases\n"
                for keys, i in data[reply].items():
                    global_reply += keys + ": " + str(i) + "\n"
                context.bot.send_message(chat_id=update.effective_chat.id, text=global_reply)
        else: #something went wrong
            context.bot.send_message(chat_id=update.effective_chat.id, text="Error, something went wrong.")
    else:
        response = requests.get('https://api.covid19api.com/total/country/'+reply)
        data = response.json()
        print(list(data)[-1])
        if(response.status_code==200):
            for keys, i in list(data)[-1].items():
                if keys == 'Confirmed':
                    confirmed = i
                if keys == 'Deaths':
                    deaths = i
                if keys == 'Recovered':
                    recovered = i 
                if keys == 'Active':
                    active = i
                if keys == 'Date':
                    date = i
            
            reply_text = reply + "\nCases Confirmed: " + str(confirmed) + "\nDeaths: " + str(deaths) + "\nRecovered: " + str(recovered) + "\nActive: " + str(active)
                
            context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)
        else: #something went wrong
            context.bot.send_message(chat_id=update.effective_chat.id, text="Error, something went wrong.")

updater = Updater(token='1788619740:AAHY3kWDnqntunZlBIgFJuLHI5LOnFttzAE', use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

covid_summary_handler = CommandHandler('covid', summary)
dispatcher.add_handler(covid_summary_handler)

commands_handler= CommandHandler('commands', commands)
dispatcher.add_handler(commands_handler)

updater.start_polling()
