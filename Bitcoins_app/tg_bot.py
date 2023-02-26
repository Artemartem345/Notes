import telebot
import config
import pydantic_models

bot = telebot.TeleBot(config.bot_token)


@bot.message_handler(commands=['start'])
def start_message(message):
    # создаем объект для работы с кнопками (row_width - определяет количество кнопок по ширине)
    markup = telebot.types.ReplyKeyboardMarkup(
        row_width=2, resize_keyboard=True)

    # создаем каждую кнопку таким образом
    btn1 = telebot.types.KeyboardButton('Кошелек')
    btn2 = telebot.types.KeyboardButton('Перевести')
    btn3 = telebot.types.KeyboardButton('История')

    markup.add(btn1, btn2, btn3)

    text = f'Привет {message.from_user.full_name}, я твой бот-криптокошелек, \n' \
           'у меня ты можешь хранить и отправлять биткоины'

    # теперь добавляем объект с кнопками к отправляемому пользователю сообщению в аргумент "reply_markup"
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(regexp='Кошелек')
def wallet(message):
    markup = telebot.types.ReplyKeyboardMarkup(
        row_width=2, resize_keyboard=True)
    # мы создали ещё одну кнопку, которую надо обработать
    btn1 = telebot.types.KeyboardButton('Меню')
    markup.add(btn1)
    balance = 0  # сюда мы будем получать баланс через наш API
    text = f'Ваш баланс: {balance}'
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(regexp='Перевести')
def transaction(message):
    markup = telebot.types.ReplyKeyboardMarkup(
        row_width=2, resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('Меню')
    markup.add(btn1)
    text = f'Введите адрес кошелька куда хотите перевести: '
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(regexp='История')
def history(message):
    markup = telebot.types.ReplyKeyboardMarkup(
        row_width=2, resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('Меню')
    markup.add(btn1)
    transactions = ['1', '2', '3']  # сюда мы загрузим транзакции
    text = f'Ваши транзакции{transactions}'
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(regexp='Меню')
def menu(message):
    markup = telebot.types.ReplyKeyboardMarkup(
        row_width=2, resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('Кошелек')
    btn2 = telebot.types.KeyboardButton('Перевести')
    btn3 = telebot.types.KeyboardButton('История')
    markup.add(btn1, btn2, btn3)

    text = f'Главное меню'
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(regexp='Я в консоли')
def print_me(message):
    markup = telebot.types.ReplyKeyboardMarkup(
        row_width=2, resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('Меню')
    markup.add(btn1)
    print(message.from_user.to_dict())
    text = f'Ты: {message.from_user.to_dict()}'
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(func=lambda message: message.from_user.id == config.tg_admin_id and message.text == "Админка")
def admin_panel(message):
    markup = telebot.types.ReplyKeyboardMarkup(
        row_width=2, resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('Общий баланс')
    btn2 = telebot.types.KeyboardButton('Все юзеры')
    btn3 = telebot.types.KeyboardButton('Меню')
    markup.add(btn1, btn2, btn3)
    text = f'Админ-панель'
    bot.send_message(message.chat.id, text, reply_markup=markup)


users = config.fake_database['users']


# делаем проверку на админ ли боту пишет проверяем текст сообщения
@bot.message_handler(func=lambda message: message.from_user.id == config.tg_admin_id and message.text == "Все юзеры")
def all_users(message):
    text = f'Юзеры:'
    # создаем объект с инлайн-разметкой
    inline_markup = telebot.types.InlineKeyboardMarkup()
    for user in users:  # в цикле создаем 3 кнопки и добавляем их поочередно в нашу разметку
        inline_markup.add(telebot.types.InlineKeyboardButton(text=f'Юзер: {user["name"]}',
                                                             callback_data=f"user_{user['id']}"))
        # так как мы добавляем кнопки по одной, то у нас юзеры будут в 3 строчки
        # в коллбеке у нас будет текст, который содержит айди юзеров
    bot.send_message(message.chat.id, text,
                     reply_markup=inline_markup)  # прикрепляем нашу разметку к ответному сообщению


# в качестве условия для обработки принимает только лямбда-функции
# хендлер принимает объект Call
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    query_type = call.data.split('_')[0]  # получаем тип запроса
    if query_type == 'user':
        # получаем айди юзера из нашей строки
        user_id = call.data.split('_')[1]
        inline_markup = telebot.types.InlineKeyboardMarkup()
        for user in users:
            if str(user['id']) == user_id:
                inline_markup.add(telebot.types.InlineKeyboardButton(text="Назад", callback_data='users'),
                                  telebot.types.InlineKeyboardButton(text="Удалить юзера",
                                                                     callback_data=f'delete_user_{user_id}'))

                bot.edit_message_text(text=f'Данные по юзеру:\n'
                                           f'ID: {user["id"]}\n'
                                           f'Имя: {user["name"]}\n'
                                           f'Ник: {user["nick"]}\n'
                                           f'Баланс: {user["balance"]}',
                                      chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      reply_markup=inline_markup)
                print(f"Запрошен {user}")
                break

    if query_type == 'users':
        inline_markup = telebot.types.InlineKeyboardMarkup()
        for user in users:
            # к каждой кнопке прикручиваем в callback_data айди юзера, чтобы можно было идентифицировать нажатую кнопку
            inline_markup.add(telebot.types.InlineKeyboardButton(text=f'Юзер: {user["name"]}',
                                                                 callback_data=f"user_{user['id']}"))
        bot.edit_message_text(text="Юзеры:",
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=inline_markup)  # прикрепляем нашу разметку к ответному сообщению

    if query_type == 'delete' and call.data.split('_')[1] == 'user':
        # получаем и превращаем наш айди в число
        user_id = int(call.data.split('_')[2])
        for i, user in enumerate(users):
            if user['id'] == user_id:
                print(f'Удален Юзер: {users[i]}')
                users.pop(i)
        inline_markup = telebot.types.InlineKeyboardMarkup()
        for user in users:
            inline_markup.add(telebot.types.InlineKeyboardButton(text=f'Юзер: {user["name"]}',
                                                                 callback_data=f"user_{user['id']}"))
        bot.edit_message_text(text="Юзеры:",
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=inline_markup)  # прикрепляем нашу разметку к ответному сообщению


@bot.message_handler(func=lambda message: message.from_user.id == config.tg_admin_id and message.text == "Общий баланс")
def total_balance(message):
    markup = telebot.types.ReplyKeyboardMarkup(
        row_width=2, resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('Меню')
    btn2 = telebot.types.KeyboardButton('Админка')
    markup.add(btn1, btn2)
    balance = 0
    for user in users:
        balance += user['balance']
    text = f'Общий баланс: {balance}'
    bot.send_message(message.chat.id, text, reply_markup=markup)


# запускаем бота этой командой:
bot.infinity_polling()



