import telebot
from telebot import types
from db import DatabaseHandler

bot = telebot.TeleBot('')
db_handler = DatabaseHandler()

class User:
    def __init__(self, user_id):
        self.id = user_id
        self.lvl, self.exp, self.wbd_lvl, self.wbd_exp = db_handler.get_user_data(user_id)

users = {}

@bot.message_handler(commands=['start'])
def welcome(message):
    
    user_id = message.from_user.id
    users[user_id] = User(user_id)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("👤 Stats")
    item2 = types.KeyboardButton("📜 Quests")
    item3 = types.KeyboardButton("🥷 Skills")
    markup.add(item1, item2, item3)

    bot.send_message(
        message.chat.id,
        f"Твой id: {message.from_user.id}\n Game: <b>{message.from_user.first_name}</b> \n Let's go for it",
        parse_mode='html',
        reply_markup=markup
    )


@bot.message_handler(content_types=['text'])
def buttons(message):
    user_id = message.from_user.id  # Сначала получаем user_id из сообщения
    if user_id in users:
        user = users[user_id]
    else:
        user = User(user_id)
        users[user_id] = user

    if message.chat.type == 'private':

        if message.text == '👤 Stats':
            if user.exp >= 0 and user.exp < 1000:
                user.lvl = 1
            elif user.exp >= 2000 and user.exp < 3000:
                user.lvl = 2
            bot.send_message(message.chat.id, f"Player level: {user.lvl}")

        elif message.text == '📜 Quests':
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Dailies", callback_data='quest1')
            item2 = types.InlineKeyboardButton("Weeklies", callback_data='quest2')
            item3 = types.InlineKeyboardButton("Monthly", callback_data='quest3')
            item4 = types.InlineKeyboardButton("Annually", callback_data='quest4')
            item5 = types.InlineKeyboardButton("Routine", callback_data='quest5')
            item6 = types.InlineKeyboardButton("Skills", callback_data='quest6')
            item7 = types.InlineKeyboardButton("Achievements", callback_data='quest7')
            markup.add(item1, item2, item3, item4, item5, item6, item7)
            bot.send_message(message.chat.id, "______________________________", reply_markup=markup)

        elif message.text == '🥷 Skills':
            if user.wbd_exp >= 0 and user.wbd_exp < 3000:
                user.wbd_lvl = 1
            elif user.wbd_exp >= 30000 and user.wbd_exp < 35000:
                user.wbd_lvl = 11
            # Добавьте остальные условия для уровней

            bot.send_message(message.chat.id, f"Skill - Web Design: {user.wbd_lvl} lvl")

        else:
            bot.send_message(message.chat.id, 'VR MMO RPG')

        db_handler.update_user_data(user_id, user.exp, user.lvl, user.wbd_exp, user.wbd_lvl)


@bot.callback_query_handler(func=lambda call: True)
def buttons_handle(call):
    
    user_id = call.from_user.id
    user = users[user_id]

    if call.data == 'quest1':
        handle_markup = types.InlineKeyboardMarkup()
        completed = types.InlineKeyboardButton("🟢 Completed", callback_data='completed')
        incompleted = types.InlineKeyboardButton("🔴 Incompleted", callback_data='incompleted')
        handle_markup.add(completed, incompleted)
        bot.send_message(
            call.message.chat.id,
            "<b>Make a website layout</b> \n  Rewards - \n    Player exp: 2 500 exp\n    Skill - Web Design: 30 00 exp",
            reply_markup=handle_markup,
            parse_mode="HTML"
        )
        bot.edit_message_text("\n.\n\n\n Refreshes in 20:39:14 \n\n\n.\n ", call.message.chat.id, call.message.message_id, reply_markup=None)

    elif call.data == 'completed':
        bot.send_message(call.message.chat.id, "Congratulations \n Rewards are already in your bag")
        user.exp += 2500
        user.wbd_exp += 30000

        lvl, exp, wbd_lvl, wbd_exp = db_handler.get_user_data(user_id)
        user.lvl, user.wbd_lvl = lvl, wbd_lvl

        bot.edit_message_text("Make a website layout", call.message.chat.id, call.message.message_id, reply_markup=None)

    elif call.data == 'incompleted':
        bot.send_message(call.message.chat.id, 'Бывает 😢')

    db_handler.update_user_data(user_id, user.exp, user.lvl, user.wbd_exp, user.wbd_lvl)

# RUN
bot.polling(none_stop=True)
