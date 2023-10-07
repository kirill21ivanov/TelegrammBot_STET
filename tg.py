import telebot
import config


bot = telebot.TeleBot(config.TOKEN)

second_text_name = None

try:
    user_chat = bot.get_chat(870978960)
    if user_chat.username:
        second_text_name = "@" + user_chat.username
        bot.send_message(870163214, second_text_name)
    else:
        second_text_name = user_chat.first_name
except telebot.apihelper.ApiTelegramException as e:
    print(f"Error while fetching user's chat information: {e}")


