import telebot
from telebot import  types
import sqlite3
import random
act_category = ''
act_id=0
captcha_list = ["яблоко", "арбуз", "банан", "виноград", "морковь", "кукуруза"] # это название всех элементов с капчи, можете поставить что угодно
# ================
cp1 = "🍏"  # смайлики в капче.
cp2 = "🍉"
cp3 = "🍌"
cp4 = "🍇"
cp5 = "🥕"
cp6 = "🌽"
# ================
completecaptcga = [999]

bot_token = ""
admin = 
category = ['💳 Проблема пополнения', '❓ Вопрос по работе программы','💛 Сотрудничество', '💚 Предложения']
rules = 'Пишите уважительно, придерживаясь норм морали. В противном случае вы можете быть заблокированным'
bot=telebot.TeleBot(bot_token)

connect = sqlite3.connect('users.db')
cursor= connect.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tg_id INTEGER,
    activate INTEGER,
    try INTEGER,
    block INTEGER,
    support INTEGER,
    supportText TEXT
)""")

connect.commit()

@bot.message_handler()
def start(message):
    connect = sqlite3.connect('users.db')
    cursor= connect.cursor()
    people_id=message.chat.id
    cursor.execute(f'SELECT activate FROM users WHERE tg_id={people_id}') 
    data=cursor.fetchone()
    cursor.execute(f'SELECT block FROM users WHERE tg_id={people_id}') 
    bb=cursor.fetchone()
    global emoji
    global dostup
    if (data is None or data[0]==0):
        info=[message.chat.id, 0, 3, 0, 0]
        if data is None:
            cursor.execute('INSERT INTO users(tg_id, activate, try, block, support) VALUES (?, ?, ?, ?, ?);', info)
            connect.commit()
            cu(message) 
        else:
            if bb[0]==1:
                bot.send_message(message.chat.id, 'Вы заблокированы')
            else:
                cu(message)
    else:
        if bb[0]==1:
            bot.send_message(message.chat.id, 'Вы заблокированы')
        else:
            me(message)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "cpt1":
            ms = call.message.chat.id
            
            check = captcha_list[0:1]
            check = check[0]
            if emoji == check:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=' Проверка пройдена успешно!')
                connect  = sqlite3.connect('users.db')
                cursor = connect.cursor()
                cursor.execute("UPDATE users SET activate = (?) WHERE tg_id = (?)",(1,call.message.chat.id,))
                connect.commit()
                message=call.message
                me(message)
                completecaptcga.append(call.message.chat.id)

            else: 
                connect  = sqlite3.connect('users.db')
                cursor = connect.cursor()
                cursor.execute("SELECT try FROM users WHERE tg_id=(?)",(call.message.chat.id,))
                
                tr=cursor.fetchall()[0][0]
                if tr==3:
                    bot.send_message(call.message.chat.id,f'Вы неверно решили капчу. У вас осталось 2 попытки')
                    cursor.execute(f"UPDATE users SET try=? WHERE tg_id=(?)",(tr-1, call.message.chat.id))
                    message=call.message
                    cu(message)
                elif tr==2:
                    bot.send_message(call.message.chat.id,f'Вы неверно решили капчу. У вас осталось 1 попытка')
                    cursor.execute(f"UPDATE users SET try=? WHERE tg_id=(?)",(tr-1, call.message.chat.id))
                    message=call.message
                    cu(message)
                else:
                    bot.send_message(call.message.chat.id,f'Вы неверно решили капчу 3 раза, за что получаете блокировку!')
                    cursor.execute(f"UPDATE users SET try=? WHERE tg_id=(?)",(tr-1, call.message.chat.id))
                    cursor.execute(f"UPDATE users SET block=? WHERE tg_id=(?)",(1, call.message.chat.id))
                connect.commit()

        if call.data == "cpt2":
            ms = call.message.chat.id
            
            check = captcha_list[1:2]
            check = check[0]
            if emoji == check:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=' Проверка пройдена успешно!')
                connect  = sqlite3.connect('users.db')
                cursor = connect.cursor()
                cursor.execute("UPDATE users SET activate = (?) WHERE tg_id = (?)",(1,call.message.chat.id,))
                connect.commit()
                message=call.message
                me(message)
                completecaptcga.append(call.message.chat.id)
            if emoji != check:
                
                connect  = sqlite3.connect('users.db')
                cursor = connect.cursor()
                cursor.execute("SELECT try FROM users WHERE tg_id=(?)",(call.message.chat.id,))
                tr=cursor.fetchall()[0][0]
                if tr==3:
                    bot.send_message(call.message.chat.id,f'Вы неверно решили капчу. У вас осталось 2 попытки')
                    cursor.execute(f"UPDATE users SET try=? WHERE tg_id=(?)",(tr-1, call.message.chat.id))
                    message=call.message
                    cu(message)
                elif tr==2:
                    bot.send_message(call.message.chat.id,f'Вы неверно решили капчу. У вас осталось 1 попытка')
                    cursor.execute(f"UPDATE users SET try=? WHERE tg_id=(?)",(tr-1, call.message.chat.id))
                    message=call.message
                    cu(message)
                else:
                    bot.send_message(call.message.chat.id,f'Вы неверно решили капчу 3 раза, за что получаете блокировку!')
                    cursor.execute(f"UPDATE users SET try=? WHERE tg_id=(?)",(tr-1, call.message.chat.id))
                    cursor.execute(f"UPDATE users SET block=? WHERE tg_id=(?)",(1, call.message.chat.id))
                connect.commit()
        if call.data == "cpt3":
            ms = call.message.chat.id
            
            check = captcha_list[2:3]
            check = check[0]
            if emoji == check:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=' Проверка пройдена успешно!')
                connect  = sqlite3.connect('users.db')
                cursor = connect.cursor()
                cursor.execute("UPDATE users SET activate = (?) WHERE tg_id = (?)",(1,call.message.chat.id,))
                connect.commit()
                message=call.message
                me(message)
                completecaptcga.append(call.message.chat.id)
            if emoji != check:
                
                connect  = sqlite3.connect('users.db')
                cursor = connect.cursor()
                cursor.execute("SELECT try FROM users WHERE tg_id=(?)",(call.message.chat.id,))
                tr=cursor.fetchall()[0][0]
                if tr==3:
                    bot.send_message(call.message.chat.id,f'Вы неверно решили капчу. У вас осталось 2 попытки')
                    cursor.execute(f"UPDATE users SET try=? WHERE tg_id=(?)",(tr-1, call.message.chat.id))
                    message=call.message
                    cu(message)
                elif tr==2:
                    bot.send_message(call.message.chat.id,f'Вы неверно решили капчу. У вас осталось 1 попытка')
                    cursor.execute(f"UPDATE users SET try=? WHERE tg_id=(?)",(tr-1, call.message.chat.id))
                    message=call.message
                    cu(message)
                else:
                    bot.send_message(call.message.chat.id,f'Вы неверно решили капчу 3 раза, за что получаете блокировку!')
                    cursor.execute(f"UPDATE users SET try=? WHERE tg_id=(?)",(tr-1, call.message.chat.id))
                    cursor.execute(f"UPDATE users SET block=? WHERE tg_id=(?)",(1, call.message.chat.id))
                connect.commit()
        if call.data == "cpt4":
            ms = call.message.chat.id
            
            check = captcha_list[3:4]
            check = check[0]
            if emoji == check:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=' Проверка пройдена успешно!')
                connect  = sqlite3.connect('users.db')
                cursor = connect.cursor()
                cursor.execute("UPDATE users SET activate = (?) WHERE tg_id = (?)",(1,call.message.chat.id,))
                connect.commit()
                message=call.message
                me(message)
                completecaptcga.append(call.message.chat.id)
            if emoji != check:
                
                connect  = sqlite3.connect('users.db')
                cursor = connect.cursor()
                cursor.execute("SELECT try FROM users WHERE tg_id=(?)",(call.message.chat.id,))
                tr=cursor.fetchall()[0][0]
                if tr==3:
                    bot.send_message(call.message.chat.id,f'Вы неверно решили капчу. У вас осталось 2 попытки')
                    cursor.execute(f"UPDATE users SET try=? WHERE tg_id=(?)",(tr-1, call.message.chat.id))
                    message=call.message
                    cu(message)
                elif tr==2:
                    bot.send_message(call.message.chat.id,f'Вы неверно решили капчу. У вас осталось 1 попытка')
                    cursor.execute(f"UPDATE users SET try=? WHERE tg_id=(?)",(tr-1, call.message.chat.id))
                    message=call.message
                    cu(message)
                else:
                    bot.send_message(call.message.chat.id,f'Вы неверно решили капчу 3 раза, за что получаете блокировку!')
                    cursor.execute(f"UPDATE users SET try=? WHERE tg_id=(?)",(tr-1, call.message.chat.id))
                    cursor.execute(f"UPDATE users SET block=? WHERE tg_id=(?)",(1, call.message.chat.id))
                connect.commit()
        if call.data == "cpt5":
            ms = call.message.chat.id
            
            check = captcha_list[4:5]
            check = check[0]
            if emoji == check:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=' Проверка пройдена успешно!')
                connect  = sqlite3.connect('users.db')
                cursor = connect.cursor()
                cursor.execute("UPDATE users SET activate = (?) WHERE tg_id = (?)",(1,call.message.chat.id,))
                connect.commit()
                message=call.message
                me(message)
                completecaptcga.append(call.message.chat.id)
            if emoji != check:
                
                connect  = sqlite3.connect('users.db')
                cursor = connect.cursor()
                cursor.execute("SELECT try FROM users WHERE tg_id=(?)",(call.message.chat.id,))
                tr=cursor.fetchall()[0][0]
                if tr==3:
                    bot.send_message(call.message.chat.id,f'Вы неверно решили капчу. У вас осталось 2 попытки')
                    cursor.execute(f"UPDATE users SET try=? WHERE tg_id=(?)",(tr-1, call.message.chat.id))
                    message=call.message
                    cu(message)
                elif tr==2:
                    bot.send_message(call.message.chat.id,f'Вы неверно решили капчу. У вас осталось 1 попытка')
                    cursor.execute(f"UPDATE users SET try=? WHERE tg_id=(?)",(tr-1, call.message.chat.id))
                    message=call.message
                    cu(message)
                else:
                    bot.send_message(call.message.chat.id,f'Вы неверно решили капчу 3 раза, за что получаете блокировку!')
                    cursor.execute(f"UPDATE users SET try=? WHERE tg_id=(?)",(tr-1, call.message.chat.id))
                    cursor.execute(f"UPDATE users SET block=? WHERE tg_id=(?)",(1, call.message.chat.id))
                connect.commit()
        if call.data == "cpt6":
            ms = call.message.chat.id
        
            check = captcha_list[5:6]
            check = check[0]
            if emoji == check:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=' Проверка пройдена успешно!')
                connect  = sqlite3.connect('users.db')
                cursor = connect.cursor()
                cursor.execute("UPDATE users SET activate = (?) WHERE tg_id = (?)",(1,call.message.chat.id,))
                connect.commit()
                message=call.message
                me(message)
                completecaptcga.append(call.message.chat.id)
            if emoji != check:
                
                connect  = sqlite3.connect('users.db')
                cursor = connect.cursor()
                cursor.execute("SELECT try FROM users WHERE tg_id=(?)",(call.message.chat.id,))
                tr=cursor.fetchall()[0][0]
                if tr==3:
                    bot.send_message(call.message.chat.id,f'Вы неверно решили капчу. У вас осталось 2 попытки')
                    cursor.execute(f"UPDATE users SET try=? WHERE tg_id=(?)",(tr-1, call.message.chat.id))
                    message=call.message
                    cu(message)
                elif tr==2:
                    bot.send_message(call.message.chat.id,f'Вы неверно решили капчу. У вас осталось 1 попытка')
                    cursor.execute(f"UPDATE users SET try=? WHERE tg_id=(?)",(tr-1, call.message.chat.id))
                    message=call.message
                    cu(message)
                else:
                    bot.send_message(call.message.chat.id,f'Вы неверно решили капчу 3 раза, за что получаете блокировку!')
                    cursor.execute(f"UPDATE users SET try=? WHERE tg_id=(?)",(tr-1, call.message.chat.id))
                    cursor.execute(f"UPDATE users SET block=? WHERE tg_id=(?)",(1, call.message.chat.id))
                connect.commit()
                
def cu(message):
    ms = message
    # Это внутреняя клавиатура, которая содержит в себе символы, на которые нажимает человек.
    keyboard = types.InlineKeyboardMarkup()
    cpt1 = types.InlineKeyboardButton(text=cp1, callback_data="cpt1")
    cpt2 = types.InlineKeyboardButton(text=cp2, callback_data="cpt2")
    cpt3 = types.InlineKeyboardButton(text=cp3, callback_data="cpt3")
    keyboard.add(cpt1, cpt2, cpt3)
    cpt1 = types.InlineKeyboardButton(text=cp4, callback_data="cpt4")
    cpt2 = types.InlineKeyboardButton(text=cp5, callback_data="cpt5")
    cpt3 = types.InlineKeyboardButton(text=cp6, callback_data="cpt6")
    keyboard.add(cpt1, cpt2, cpt3)
    markdown = """
    *bold text*
    _italic text_
    [text](URL)
    """
    global emoji
    emoji = random.choice(captcha_list)
    global dostup
    dostup = 0
    # само сообщение с капчей.
    bot.send_message(message.chat.id, ' Чтобы продолжить пользоваться ботом, выберите на клавиатуре ' + '*' + emoji + '*', parse_mode="Markdown", reply_markup=keyboard)


def me(message):
    try:
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        cursor.execute(f'SELECT support FROM users WHERE tg_id={message.chat.id}')
        connect.commit()

        if message.chat.id != admin:
            if message.text == '⌨️ Обращение':
                if cursor.fetchall()[0][0] == 0:
                    klava = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                    for i in category:
                        klava.add(i)
                    bot.send_message(message.chat.id, f'Для создания обращения выберите категорию:', reply_markup=klava)
                else:
                    bot.send_sticker(message.chat.id, 'CAACAgQAAxkBAAEK0aBlYpe4pzREnPYyJeWqEohENxcuzAACCBYAAqbxcR6k_-nxPI03gTME')
                    bot.send_message(message.chat.id, 'Вы уже подали запрос, ожидайте ответа на него')
            elif message.text == category[0] or message.text == category[1] or message.text == category[2] or message.text == category[3]:
                if cursor.fetchall()[0][0] == 0:
                    global act_category
                    act_category = message.text
                    klava = types.ReplyKeyboardRemove()
                    answer = bot.send_message(message.chat.id, '📔 Теперь введите текст обращения:\n\nПожалуйста, помните, что вы можете отправить только одно сообщение! Постарайтесь уместить всю суть.\n\nЕсли хотите прикрепить скриншот, то загрузите на imgur.com, бот не принимает медиа.', reply_markup=klava)
                    bot.register_next_step_handler(answer, answer_f)
                else:
                    bot.send_message(message.chat.id, 'Вы уже подали запрос, ожидайте ответа на него')
            else:
                klava = types.ReplyKeyboardMarkup(resize_keyboard=True)
                button1 = '⌨️ Обращение'
                klava.add(button1)
                bot.send_sticker(message.chat.id, 'CAACAgQAAxkBAAEK0Z5lYpdo9QokCzd2sct_dbVPE5KNgwACDA8AAqbxcR4C181RIl_-BDME')
                bot.send_message(message.chat.id, 'Здравствуйте! Если вы хотите связаться со службой поддержки InsightEye, вы можете написать обращение по кнопке ниже.', reply_markup=klava)
        else:
            global act_id
            if message.text == '📭 Обращения':
                connect = sqlite3.connect('users.db')
                cursor = connect.cursor()
                cursor.execute(f'SELECT COUNT (id) FROM users')
                connect.commit()
                max_count = cursor.fetchall()[0][0]
                i = 1
                for i in range(max_count):
                    connect = sqlite3.connect('users.db')
                    cursor = connect.cursor()
                    cursor.execute(f'SELECT support FROM users WHERE id={i + 1}')
                    connect.commit()
                    a = cursor.fetchall()[0][0]
                    if a == 1:
                        connect = sqlite3.connect('users.db')
                        cursor = connect.cursor()
                        cursor.execute(f'SELECT supportText FROM users WHERE id={i + 1}')
                        connect.commit()
                        mes = cursor.fetchall()[0][0]
                        connect = sqlite3.connect('users.db')
                        cursor = connect.cursor()
                        cursor.execute(f'SELECT tg_id FROM users WHERE id={i + 1}')
                        connect.commit()
                        act_id = cursor.fetchall()[0][0]
                        klava = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        button1 = '✅ Ответить'
                        button2 = '❌ Забанить'
                        klava.add(button1, button2)
                        bot.send_message(message.chat.id, mes, reply_markup=klava, parse_mode='Markdown')
                        break
                    if i + 1 == max_count:
                        bot.send_message(message.chat.id, 'Больше обращений нет')
                        message.text = 'asdaAERGAERGsadfoagpoj'
                        me(message)
            elif message.text == '🫶 Разбан':
                klava = types.ReplyKeyboardRemove()
                unban = bot.send_message(message.chat.id, 'Введи id человека для разблокировки:')
                bot.register_next_step_handler(unban, unban_f)
            elif message.text == '⌨️ Сообщение':
                klava = types.ReplyKeyboardRemove()
                mess = bot.send_message(message.chat.id, 'Введи id получетеля сообщения:')
                bot.register_next_step_handler(mess, mess_f)
            elif message.text == '❌ Забанить':
                connect = sqlite3.connect('users.db')
                cursor = connect.cursor()
                cursor.execute(f"UPDATE users SET block=? WHERE tg_id=(?)", (1, act_id))
                connect.commit()
                bot.send_message(message.chat.id, f'{act_id} был заблокирован!')
                try:
                    bot.send_message(act_id, 'Администратор заблокировал вас!')
                except telebot.apihelper.ApiTelegramException as e:
                    if e.result_json['description'] == "Forbidden: bot was blocked by the user":
                        print(f"User {act_id} has blocked the bot.")
                    else:
                        print(f"Error sending message: {e}")
                message.text = 'asdASFGAWEFasdfiawefDF'
                connect = sqlite3.connect('users.db')
                cursor = connect.cursor()
                cursor.execute("UPDATE users SET support = (?) WHERE tg_id = (?)", (0, act_id,))
                connect.commit()
                me(message)
            elif message.text == '✅ Ответить':
                klava = types.ReplyKeyboardRemove()
                answer_for_s = bot.send_message(message.chat.id, f'Введите ответ для {act_id}:', reply_markup=klava)
                bot.register_next_step_handler(answer_for_s, answer_for_s_f)
            elif message.text == '✍️ Рассылка':
                connect = sqlite3.connect('users.db')
                cursor = connect.cursor()
                cursor.execute(f'SELECT COUNT (id) FROM users')
                connect.commit()
                klava = types.ReplyKeyboardMarkup(resize_keyboard=True)
                button1 = '☑️ Создаем'
                button2 = '⬅️ Вернуться'
                klava.add(button1, button2)
                bot.send_message(message.chat.id, f'В вашем боте `{cursor.fetchall()[0][0]}` пользователей. Хотите создать рассылку?', parse_mode='Markdown', reply_markup=klava)
            elif message.text == '☑️ Создаем' and message.chat.id == admin:
                klava = types.ReplyKeyboardRemove()
                ads = bot.send_message(message.chat.id, '✏️ Введи текст своей рассылки. Если хочешь, чтобы у рассылки была фотография - отправь фотографию, добавив к ней текст (одним сообщением)', reply_markup=klava)
                bot.register_next_step_handler(ads, ads_f)
            elif message.text == '⬅️ Вернуться':
                message.text = 'asdasdweafarfg'
                me(message)
            elif message.text == '✅ Создаем':
                message.text = 'asdasdweafarfg'
                ads_yf(message)
            else:
                klava = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                button1 = '📭 Обращения'
                button2 = '⌨️ Сообщение'
                button3 = '🫶 Разбан'
                button4 = '✍️ Рассылка'
                klava.add(button1, button2, button3, button4)
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEKxbFlV-GGO6htHe4Hi75YS3kFfIF8fAACvRwAArck-UlFx0Lq0J6bKDME')
                bot.send_message(message.chat.id, 'Меню админа:', reply_markup=klava)

    except telebot.apihelper.ApiTelegramException as e:
        if e.result_json['description'] == "Forbidden: bot was blocked by the user":
            print(f"User {message.chat.id} has blocked the bot.")
        else:
            print(f"Error in the 'me' function: {e}")


def ads_f(message):
    global photo_status
    global photo_id
    global description
    if message.content_type=='photo':
        bot.send_photo(message.chat.id, message.photo[0].file_id, message.caption)
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1='✅ Создаем'
        button2='⬅️ Вернуться'
        klava.add(button1,button2)
        photo_status=1
        description=message.caption
        photo_id=message.photo[0].file_id
        ads_y=bot.send_message(message.chat.id,'Вот так будет выглядеть рассылка. Проверь и подтверди старт рекламы', reply_markup=klava)
        bot.register_next_step_handler(ads_y,ads_yf)
    else:
        bot.send_message(message.chat.id, message.text)
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1='✅ Создаем'
        button2='⬅️ Вернуться'
        klava.add(button1,button2)
        photo_status=0
        description=message.text
        ads_y=bot.send_message(message.chat.id,'Вот так будет выглядеть рассылка. Проверь и подтверди старт рекламы', reply_markup=klava)
        

def ads_yf(message):
    global photo_status
    global photo_id
    global description

    connect  = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute(f'SELECT id FROM users ORDER BY id DESC LIMIT 1')
    connect.commit()
    i=1
    i2=int((cursor.fetchall())[0][0])
    try_false=0
    try_true=0
    for i in range(i2+1):
        connect  = sqlite3.connect('users.db')
        cursor = connect.cursor()
        cursor.execute(f'SELECT tg_id FROM users WHERE id = ?', (i,))
        connect.commit()
        if photo_status==1:
            try_true=try_true+1
            try:
                bot.send_photo(cursor.fetchall()[0][0],photo_id,description)
            except Exception as error:
                try_false=try_false+1

        else:
            try_true=try_true+1
            try:
                bot.send_message(cursor.fetchall()[0][0],description)
            except Exception as error:
                try_false=try_false+1
    
    text=f'📭 Рассылка была отправлена `{try_true-1}` пользователям!\n✅ Успешно доставлено: `{try_true-try_false}`\n❌ Не дошло: `{try_false-1}`'
    bot.send_message(message.chat.id, text, parse_mode='Markdown')
    me(message)

def unban_f(message):
    if (message.text).isdigit():
        connect = sqlite3.connect('users.db')
        cursor= connect.cursor()
        people_id=message.chat.id
        cursor.execute(f'SELECT block FROM users WHERE tg_id={message.text}') 
        data=cursor.fetchone()
        connect.commit()
        print(data)
        if data is None:
            bot.send_message(message.chat.id,'Пользователь  не найден в бд')
        elif data[0]==0:
            bot.send_message(message.chat.id, 'Пользователь не в бане')
            me(message)
        else:
            connect  = sqlite3.connect('users.db')
            cursor = connect.cursor()
            cursor.execute(f"UPDATE users SET block=? WHERE tg_id=(?)",(0, message.text))
            connect.commit()
            bot.send_message(message.chat.id, '💀 Юзер был разбанен!')
            bot.send_message(message.text,'Вы были разблокированы!')
            me(message)
    else:
        bot.send_message(message.chat.id,'Айди должно быть числом')
        me(message)

def mess2_f(message):
    global act_id
    bot.send_message(act_id, message.text)
    bot.send_message(message.chat.id,'Сообщение было отправлено')
    me(message)
def mess_f(message):
    if (message.text).isdigit():
        connect = sqlite3.connect('users.db')
        cursor= connect.cursor()
        people_id=message.chat.id
        cursor.execute(f'SELECT block FROM users WHERE tg_id={message.text}') 
        data=cursor.fetchone()
        connect.commit()
        print(data)
        if data is None:
            bot.send_message(message.chat.id,'Пользователь  не найден в бд')
            me(message)
        else:
            global act_id
            act_id=message.text
            mess=bot.send_message(message.chat.id, 'Введи сообщение для юзера:')
            bot.register_next_step_handler(mess,mess2_f)
    else:
        bot.send_message(message.chat.id,'Айди должно быть числом')
        me(message)
        
def answer_for_s_f(message):
    global act_id
    bot.send_message(act_id,'Вы получили ответ на свой запрос:\n\n'+message.text)
    bot.send_message(message.chat.id,'Пользователь  получил ответ!')
    connect  = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute("UPDATE users SET support = (?) WHERE tg_id = (?)",(0,act_id,))
    connect.commit()
    me(message)

def answer_f(message):
    global act_category

    # Проверяем, есть ли в сообщении медиа-файл
    if message.photo or message.document or message.audio or message.video or message.voice or message.sticker:
        bot.send_message(message.chat.id, 'Пожалуйста, загрузите фото на imgur.com и отправьте ссылку.')
        klava = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = '⌨️ Обращение'
        klava.add(button1)
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEKKntk7nn9Thz0XzQCqB2pArbAWmRKuwACeicAAn7IuUpa8TCgjo3IOzAE')
        bot.send_message(message.chat.id, 'Меню юзера:', reply_markup=klava)
    else:
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        cursor.execute("UPDATE users SET support = (?) WHERE tg_id = (?)", (1, message.chat.id,))
        text = f'Тема: {act_category}\nОбращение: {message.text}\nId Юзера: `{message.chat.id}`\nЮзернейм: @{message.from_user.username}'
        cursor.execute("UPDATE users SET supportText = (?) WHERE tg_id = (?)", (text, message.chat.id,))
        connect.commit()
        bot.send_message(message.chat.id, 'Обращение было отправлено, ожидайте ответа!')
        bot.send_message(admin, 'Вы получили новый запрос!')
        me(message)

bot.polling()