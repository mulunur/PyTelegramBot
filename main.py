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
    bot.register_next_step_handler(message, user_entering_name)


def user_entering_name(message):
    global name
    try:
        name = str(message.text)
        bot.send_message(message.chat.id, name + messages.ok_name)
        bot.register_next_step_handler(message, user_entering_time)
    except Exception as e:
        print(repr(e))
        bot.send_message(message.chat.id, messages.hello_error)
        bot.register_next_step_handler(message, user_entering_name)


def user_entering_time(message):
    global awake_hour
    try:
        if message.text.find(':') != -1:
            awake_hour = int(message.text[:message.text.find(':')])
        else:
            awake_hour = int(message.text)
        if awake_hour < 0 or awake_hour > 24:
            raise ValueError
        bot.send_message(message.chat.id, messages.num_hours)
        bot.register_next_step_handler(message, user_entering_hours)
    except Exception as e:
        print(repr(e))
        bot.send_message(message.chat.id, messages.num_error)
        bot.register_next_step_handler(message, user_entering_time)


def user_entering_hours(message):
    global time_hours
    try:
        time_hours = int(message.text)
        if time_hours < 3 or time_hours > 12:
            raise ValueError
        bot.send_message(message.chat.id, messages.ok_hours)
        calculate_alarm_clock(message)
    except Exception as e:
        print(repr(e))
        bot.send_message(message.chat.id, messages.num_error)
        bot.register_next_step_handler(message, user_entering_hours)


def calculate_alarm_clock(message):
    global name
    global time_hours
    global awake_hour

    try:
        prepare_to_sleep_time = 16  # в среднем человек засыпает за 16 минут
        sleep_minutes = int(time_hours) * 60 + prepare_to_sleep_time
        number_of_cycles = int(sleep_minutes / 90)
        sleep_time = (awake_hour - (number_of_cycles * 90 / 60)) % 24
        sleep_time_minutes = int(60 * (sleep_time % 1)) + 16
        sleep_time_hours = str(int(sleep_time))
        if sleep_time_minutes < 10:
            sleep_time_minutes = '0' + str(sleep_time_minutes)
        sleep_time_minutes = str(sleep_time_minutes)
        sleep_time_string = sleep_time_hours + ':' + sleep_time_minutes
        bot.send_message(message.chat.id, name + messages.sleep_time[0] +
                         str(awake_hour) + messages.sleep_time[2] +
                         sleep_time_string + messages.sleep_time[3])
        bot.send_message(message.chat.id, messages.process_commands)

    except Exception as e:
        print(repr(e))
        bot.send_message(message.chat.id, messages.calculation_error)
        bot.send_message(message.chat.id, name + messages.ok_name)
        bot.register_next_step_handler(message, user_entering_time)


@bot.message_handler(commands=['reg'])
def new_user(message):
    bot.send_message(message.chat.id, messages.hello_for_new)
    bot.register_next_step_handler(message, user_entering_name)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, messages.help_message[0])
    bot.send_message(message.chat.id, messages.help_message[1])
    bot.send_message(message.chat.id, messages.help_message[2])


bot.polling()
