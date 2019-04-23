import telebot
from Credentials import bot_proxy, bot_token, mtproto

import bot_pipe
from datetime import datetime

bot = telebot.TeleBot(bot_token)
telebot.apihelper.proxy = {'https': bot_proxy}
telebot.apihelper.proxy = {'http': bot_proxy}


def log(message, answer):
    print("\n ---------")
    print(datetime.now())
    print(message.text)
    print(answer)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.from_user.id, 'Enter profile link in VK')


@bot.message_handler(content_types=['text'])
def handle_text(message):
    df = bot_pipe.main(message.text)
    answer = 'model0 - {0} \n model1 - {1} \n model2 - {2} \n ' \
             'model3 - {3} \n model4 - {4}'.format(df.loc[0, 'model0'], df.loc[0, 'model1'], df.loc[0, 'model2'],
                                                   df.loc[0, 'model3'], df.loc[0, 'model4'])
    bot.send_message(message.from_user.id, answer)
    log(message, answer)


bot.polling(none_stop=True, interval=0)
