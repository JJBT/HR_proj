import telebot
from Credentials import bot_proxy, bot_token

import bot_pipe
from datetime import datetime

bot = telebot.TeleBot(bot_token)
# telebot.apihelper.proxy = {'https': bot_proxy}
# telebot.apihelper.proxy = {'http': bot_proxy}


def log(message, answer):
    output = '\n'.join(['\n----------', str(datetime.now()), message.text, answer])
    print(output)
    log_to_file(output)


def log_to_file(output):
    with open('log_file.txt', 'a') as log_file:
        log_file.write(output)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.from_user.id, 'Enter profile link in VK')


@bot.message_handler(content_types=['text'])
def handle_text(message):
    df = bot_pipe.main(message.text)
    if type(df) == bool and not df:
        answer = 'Account is private or blocked'
    else:
        answer = 'model0 - {0}'.format(df.loc[0, "model0"])

    bot.send_message(message.from_user.id, answer)
    log(message, answer)


bot.polling(none_stop=True, interval=0)
