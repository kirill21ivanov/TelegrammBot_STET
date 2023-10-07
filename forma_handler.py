# import telebot
# import json
# import config

# user_data = {}
# bot = telebot.TeleBot(config.TOKEN)

# @bot.callback_query_handler(func=lambda call: call.data == "forma")
# def handle_form_callback(call):
#     print(2)
#     try:
#         bot.delete_message(call.message.chat.id, call.message.message_id)
#     except telebot.apihelper.ApiTelegramException as e:
#         print(f"Ошибка при удалении сообщения: {e}")

#     user_id = call.message.chat.id
#     if user_id not in user_data:
#         user_data[user_id] = {}
#         bot.send_message(user_id, "Добро пожаловать! Для начала, введите ваше имя:")
#     else:
#         data = user_data[user_id]  # Get user data dictionary
#         if 'name' not in data:
#             data['name'] = call.message.text
#             bot.send_message(user_id, "Теперь введите вашу фамилию:")
#         elif 'surname' not in data:
#             data['surname'] = call.message.text
#             bot.send_message(user_id, "Теперь введите ваш номер телефона:")
#         elif 'phone' not in data:
#             data['phone'] = call.message.text
#             bot.send_message(user_id, "Теперь введите ваш адрес проживания:")
#         elif 'address' not in data:
#             data['address'] = call.message.text
#             # Save the data to a JSON file
#             save_user_data(user_id)
#             bot.send_message(user_id, "Ваши данные сохранены в файле.")
#         else:
#             bot.send_message(user_id, "Все данные уже введены и сохранены в файле.")

# def save_user_data(user_id):
#     if user_id in user_data:
#         with open(f"user_{user_id}.json", "w") as json_file:
#             json.dump(user_data[user_id], json_file, ensure_ascii=False, indent=4)
#         del user_data[user_id]