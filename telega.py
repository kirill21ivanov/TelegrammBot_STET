import telebot
import time
import json
import os
import config
from telebot import types
from datetime import datetime

try:
    bot = telebot.TeleBot(config.TOKEN)
    user_data = {}
    admin_data = {}
    user_states = {}
    NAME, SURNAME, PHONE, ADDRESS = range(4)
    


    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except telebot.apihelper.ApiTelegramException as e:
            print(f"Ошибка при удалении сообщения: {e}")
        old = types.InlineKeyboardMarkup(row_width=1)
        b1 = types.InlineKeyboardButton("Заполнить форму", callback_data="forma1")
        x = [types.InlineKeyboardButton("Контакты", url="https://stet-kazan.ru/contact.html"), types.InlineKeyboardButton("Услуги", url="https://stet-kazan.ru/uslugi.html")]
        old.add(b1).row(*x)
        bot.send_message(message.chat.id, "Привет!✌🏼")
        text = f"Это компания <b>СТЭТ</b> - мы помогаем взыскивать компенсацию с застройщика до 400 000 рублей за строительные недостатки в квартирах. <b>Заполняй форму</b> и мы с тобой свяжемся!"
        with open('img/Untitled.png', 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption=text, parse_mode="HTML", reply_markup=old)

    @bot.callback_query_handler(func=lambda call: call.data == "start2")
    def send_forma1(call):
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except telebot.apihelper.ApiTelegramException as e:
            print(f"Ошибка при удалении сообщения: {e}")
        old = types.InlineKeyboardMarkup(row_width=1)
        b1 = types.InlineKeyboardButton("Заполнить форму", callback_data="forma1")
        x = [types.InlineKeyboardButton("Контакты", url="https://stet-kazan.ru/contact.html"), types.InlineKeyboardButton("Услуги", url="https://stet-kazan.ru/uslugi.html")]
        old.add(b1).row(*x)
        text = "Привет! Это компания <b>СТЭТ</b> - мы помогаем взыскивать компенсацию с застройщика до 400 000 рублей за строительные недостатки в квартирах. <b>Заполняй форму</b> и мы с тобой свяжемся!"
        with open('img/Untitled.png', 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo, caption=text, parse_mode="HTML", reply_markup=old)
        

    @bot.callback_query_handler(func=lambda call: call.data == "forma1")
    def send_welcomes(call):
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except telebot.apihelper.ApiTelegramException as e:
                print(f"Ошибка при удалении сообщения: {e}")
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            user_id = call.message.chat.id
            user_file = f"users/{user_id}.json"
            if os.path.exists(user_file):
                print(2)
                welcome_message = f"Пожалуйста, выберите время записи на экспертизу и внести детали"
                but1 = types.InlineKeyboardButton("Начать запись", callback_data="forma2")
            else:
                print(3)
                welcome_message = f"Пожалуйста, заполните ваше имя и контакты"
                but1 = types.InlineKeyboardButton("Пройти регистрацию", callback_data="forma")
            user_data[user_id] = {}
            user_states[user_id] = NAME  # Set the initial state to NAME
            but2 = types.InlineKeyboardButton("Обратно", callback_data="start2")
            keyboard.add(but1, but2)
            user_id = call.message.chat.id
            global bot_users
            bot_users = bot.send_message(user_id, parse_mode="HTML", text=welcome_message, reply_markup=keyboard)
            
    @bot.callback_query_handler(func=lambda call: call.data == "forma2")
    def starts_call_data(call):
        user_id = call.message.chat.id
        try:
            bot.delete_message(user_id, call.message.message_id)
        except telebot.apihelper.ApiTelegramException as e:
            print(f"Ошибка при удалении сообщения: {e}")
        with open(f'users/{user_id}.json', 'r') as file:
            user_data = json.load(file)
            global report_check
            report_check = 0
            user_id = call.message.chat.id
            user_data[user_id] = {}
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton("Пропустить")
            keyboard.add(button1)
            bot.send_message(user_id, "<b>Пожалуйста, опишите, вашу проблему (прикрепите фото, если есть)</b>", parse_mode="HTML", reply_markup=keyboard)
            bot.register_next_step_handler(call.message, handle_user_response)
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except telebot.apihelper.ApiTelegramException as e:
                print(f"Ошибка при удалении сообщения: {e}")

    def handle_user_response(message):
            print(message.text)
            other_user_id = config.ADMIN
            try:
                bot.delete_message(message.chat.id, message.text)
            except telebot.apihelper.ApiTelegramException as e:
                print(f"Ошибка при удалении сообщения: {e}")
            bot.send_message(message.chat.id, "Спасибо!", reply_markup=types.ReplyKeyboardRemove())
            try:
                bot.delete_message(message.chat.id, message.message_id)
            except telebot.apihelper.ApiTelegramException as e:
                print(f"Ошибка при удалении сообщения: {e}")
            if report_check == 1:
                try:
                    bot.delete_message(message.chat.id, message.message_id)
                except telebot.apihelper.ApiTelegramException as e:
                    print(f"Ошибка при удалении сообщения: {e}")
                return 0
            else:
                user_id = message.chat.id
                response = message.text
                user_data[user_id]['response'] = response
                global admin_data_user_id
                admin_data_user_id = user_id
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                button1 = types.InlineKeyboardButton("Календарь", callback_data="button14")
                button2 = types.InlineKeyboardButton("На главную", callback_data="start2")
                keyboard.add(button1, button2)
                with open('img/121.png', 'rb') as photo:
                    text3 = "Выберите удобное время для записи и наши специалисты свяжутся с нами"
                    bot.send_photo(user_id, photo, caption=text3, parse_mode="HTML", reply_markup=keyboard)


    @bot.callback_query_handler(func=lambda call: call.data == "forma")
    def start_form(call):
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except telebot.apihelper.ApiTelegramException as e:
            print(f"Ошибка при удалении сообщения: {e}")
        user_id = call.message.chat.id
        user_file = f"users/{user_id}.json"
        if os.path.exists(user_file):
            bot.send_message(user_id, "Выбрать время для записи")
        else:
            user_data[user_id] = {}
            user_states[user_id] = NAME
            bot.send_message(user_id, "Регистрация Данных для обратной связи.\nВведите свое Имя:")

    @bot.message_handler(func=lambda message: message.chat.type == 'private')
    def handle_form_input(message):
        user_id = message.chat.id
        text = message.text
        current_step = user_states.get(user_id, NAME)
        if current_step == NAME:
            user_data[user_id]["name"] = text
            user_states[user_id] = SURNAME
            bot.send_message(user_id, "Теперь введите вашу фамилию:")
        elif current_step == SURNAME:
            user_data[user_id]["surname"] = text
            user_states[user_id] = PHONE
            bot.send_message(user_id, "Теперь введите ваш номер телефона:")
        elif current_step == PHONE:
            user_data[user_id]["phone"] = text
            user_states[user_id] = ADDRESS
            bot.send_message(user_id, "Теперь введите ваш адрес проживания:\nНапример - г.Казань ул.Амирхана д.1 кв. 221 ")
        elif current_step == ADDRESS:
            user_data[user_id]["address"] = text
            user_states.pop(user_id, None)
            save_user_data(user_id)

            keyboard = types.InlineKeyboardMarkup(row_width=1)
            but1 = types.InlineKeyboardButton("Дальше", callback_data="forma1")
            keyboard.add(but1)
            bot.send_message(user_id, "Отлично! Теперь Вы можете записаться на экспертизу!", reply_markup=keyboard)

    def save_user_data(user_id):
        if user_id in user_data:
            with open(f"users/{user_id}.json", "w") as json_file:
                json.dump(user_data[user_id], json_file, ensure_ascii=False, indent=4)
            del user_data[user_id]

    @bot.message_handler(func=lambda message: message.chat.type in ['group', 'supergroup'])
    def check_for_profanity(message):
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        text = message.text.lower()
        text2 = "Привет! Это компания <b>СТЭТ</b> - мы помогаем взыскивать компенсацию с застройщика до 400 000 рублей за строительные недостатки в квартирах. <b>Заполняй форму</b> и мы с тобой свяжемся!"
        x = [types.InlineKeyboardButton("Контакты", url="https://stet-kazan.ru/contact.html"), types.InlineKeyboardButton("Услуги", url="https://stet-kazan.ru/uslugi.html")]
        has_keyword = any(keyword in text for keyword in ["экспертизу", "проверить", "экспертиза", "стены", "не ровные стены", "экс"])
        with open('img/Untitled.png', 'rb') as photo:
            if has_keyword:
                try:
                    but19 = types.InlineKeyboardButton("Начать заполнять", callback_data="forma1")
                    keyboard.add(but19).row(*x)
                    bot.send_photo(message.from_user.id, photo, caption=text2, parse_mode="HTML", reply_markup=keyboard)
                except telebot.apihelper.ApiTelegramException as e:
                    print(f"Ошибка при удалении сообщения: {e}")
                    key = types.InlineKeyboardMarkup(row_width=1)
                    but1 = types.InlineKeyboardButton("Начать заполнять", url="http://t.me/build21_bot")
                    key.add(but1).row(*x)
                    bot.send_message(message.chat.id, text2, parse_mode="HTML", reply_markup=key)

    @bot.callback_query_handler(func=lambda call: call.data == "button14") # Кнопка Скрыть
    def block_user_by_id(call):
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except telebot.apihelper.ApiTelegramException as e:
            print(f"Ошибка при удалении сообщения: {e}")
        user_id = call.message.chat.id
        user_data[user_id] = {}
        # keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # button1 = types.KeyboardButton("Пропустить")
        # keyboard.add(button1)
        bot.send_message(user_id, "<b>Пожалуйста, напишите дату и время, когда Вы хотите записаться на экспертизу</b>", parse_mode="HTML")
        bot.register_next_step_handler(call.message, sdjgckasdhkldwhcklad)
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except telebot.apihelper.ApiTelegramException as e:
            print(f"Ошибка при удалении сообщения: {e}")

    def sdjgckasdhkldwhcklad(message):
            print(message.text)
            other_user_id = config.ADMIN
            try:
                bot.delete_message(message.chat.id, message.text)
            except telebot.apihelper.ApiTelegramException as e:
                print(f"Ошибка при удалении сообщения: {e}")
            # bot.send_message(message.chat.id, "Спасибо!", reply_markup=types.ReplyKeyboardRemove())
            try:
                bot.delete_message(message.chat.id, message.message_id)
            except telebot.apihelper.ApiTelegramException as e:
                print(f"Ошибка при удалении сообщения: {e}")
            if report_check == 1:
                try:
                    bot.delete_message(message.chat.id, message.message_id)
                except telebot.apihelper.ApiTelegramException as e:
                    print(f"Ошибка при удалении сообщения: {e}")
                return 0
            else:
                user_id = message.chat.id
                response = message.text
                # user_data[user_id]['response'] = response
                with open(f'users/{user_id}.json', 'r') as file:
                    user_data = json.load(file)
                    global admin_data_user_id
                    admin_data_user_id = user_id
                    keyboard = types.InlineKeyboardMarkup(row_width=1)
                    button2 = types.InlineKeyboardButton("На главную", callback_data="start2")
                    keyboard.add(button2)
                    bot.send_message(user_id, f"Спасибо! Мы вас записали! {message.text}", reply_markup=keyboard)
                    name =  user_data['name']
                    surname = user_data['surname']
                    phone = user_data['phone']
                    try:
                        bot.send_message(other_user_id, f"🔔Новое уведомление!🔔\nЕсть потанциальный клиент! Его данные: {name}, {surname}, {phone}, Дата: {message.text}")
                    except telebot.apihelper.ApiTelegramException as e:
                        print(f"Ошибка при удалении сообщения: {e}")
                    try:
                        bot.delete_message(user_id, message.message_id)
                    except telebot.apihelper.ApiTelegramException as e:
                        print(f"Ошибка при удалении сообщения: {e}")


    @bot.callback_query_handler(func=lambda call: call.data == "block") # Кнопка Скрыть
    def block_user_by_id(call):
        global report_check
        report_check = 1
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except telebot.apihelper.ApiTelegramException as e:
            print(f"Ошибка при удалении сообщения: {e}")

except telebot.apihelper.ApiTelegramException as e:
    if e.result.status_code == 429:
        print("Слишком много запросов. Подождите 5 секунд и повторите.")
        time.sleep(15)

if __name__ == "__main__":
    bot.polling()