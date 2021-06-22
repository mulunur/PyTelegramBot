import telebot
import messages
import config
import time
from telebot import types


bot = telebot.TeleBot(config.TOKEN)
name = ""
awake_hour = ""
time_hours = ""


@bot.message_handler(commands=['start'])
def command_start(message):
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(2)
    bot.send_message(message.chat.id, messages.help_message[0])
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(3)
    bot.send_message(message.chat.id, messages.help_message[1])
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(6)
    bot.send_message(message.chat.id, messages.help_message[2])
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(4)
    bot.send_message(message.chat.id, messages.hello_for_new)


@bot.message_handler(content_types=['text'])
def user_entering_name(message):
    if type (message.text) is str:
        global name
        name = message.text
        bot.send_message(message.chat.id, name + messages.ok_name)
        bot.register_next_step_handler(message, user_entering_time)
    else:
        bot.send_message(message.chat.id, messages.reset_hello)
        return


def user_entering_time(message):
    try:
        awake_hour = int(message.text)
        if awake_hour < 0 or awake_hour > 24:
            raise ValueError
        bot.send_message(message.chat.id, messages.num_hours)
        bot.register_next_step_handler(message, user_entering_hours)
    except Exception:
        bot.send_message(message.chat.id, messages.num_error)
        bot.register_next_step_handler(message, user_entering_time)


def user_entering_hours(message):
    try:
        time_hours = int(message.text)
        print(type (time_hours))
        if time_hours < 3 or time_hours > 12:
            raise ValueError
        bot.send_message(message.chat.id, messages.ok_hours)
        calculate_alarm_clock(message)
    except Exception:
        bot.send_message(message.chat.id, messages.num_error)
        bot.register_next_step_handler(message, user_entering_hours)


def calculate_alarm_clock(message):
    global name
    global time_hours
    global awake_hour

    sleep_minutes = int(time_hours) * 60
    number_of_cycles = sleep_minutes / 90
    sleep_time = awake_hour + (number_of_cycles * 90 / 60)
    bot.send_message(message.chat.id, '''name + messages.sleep_time[0] + awake_hour +
                     messages.sleep_time[1] + time_hours + messages.sleep_time[2] +
                     sleep_time + messages.sleep_time[3]''')


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, messages.help_message)


bot.polling()
