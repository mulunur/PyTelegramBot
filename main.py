import telebot

TOKEN = "1814314219:AAGGUNpYh279YU_Z7mP380ff9y91NU7SpPM"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "how are you doing?")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    if message.text == 'Привет':
        bot.reply_to(message, "Привет создатель")
    else:
        bot.reply_to(message, message.text)

bot.polling()