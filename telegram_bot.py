
from parser_app import login, get_products, get_buskets, get_categories ,get_products_by_category
from decouple import config
import telebot
import requests
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import webbrowser

bot = telebot.TeleBot(config('BOT_API'))
URL = config('URL')

is_activate = False

email = ''
categories = [] 

@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup(row_width=2)
    login_but = InlineKeyboardButton('Войти в аккаунт', callback_data='login')
    product_but = InlineKeyboardButton('Смотреть продукты' , callback_data='products')
    buskets_but = InlineKeyboardButton('Моя корзина' , callback_data='buskets')
    markup.add(login_but, product_but , buskets_but)
    markup.row(InlineKeyboardButton('Продукты по категориям', callback_data='products_by_category'))
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} \n Выберите действие: ', reply_markup=markup)

@bot.message_handler(commands=['site', 'website'])
def site(message):
    webbrowser.open(URL + '/product/products/')

@bot.message_handler(commands=['exit'])
def exit_account(message):
    global is_activate
    is_activate = False
    bot.send_message(message.chat.id, 'Вы вышли из аккаунта')
@bot.message_handler(content_types=['text'])
def handle_login(message):
    global is_activate
    if is_activate == False:
        if len(message.text.split()) == 2:
            global email
            email = message.text.split()[0]
            req = login(URL, message.text.split()[0], message.text.split()[1])
            if req == None:
                bot.send_message(message.chat.id, 'Неверный логин или пароль')
            else:
                bot.send_message(message.chat.id, 'Вы вошли в аккаунт')
                is_activate = True
        else:
                bot.send_message(message.chat.id, 'Неверный логин или пароль')
    else :
                bot.send_message(message.chat.id, 'Вы уже вошли в аккаунт')

@bot.callback_query_handler(func=lambda call: True)
def request_login(call):
    if call.data == 'login':
        bot.send_message(call.message.chat.id, 'Введите логин и пароль через пробел:')
        global is_activate
        is_activate = False
    if call.data == 'products':
        products_info = get_products(URL)
        for product in products_info:
            image_url = requests.get(product.get("image")).url if product.get('image') is not None else 'https://img.freepik.com/premium-vector/no-image-vector-icon-no-photo-sign-isolated_118339-3177.jpg?size=626&ext=jpg&ga=GA1.1.471228807.1705195023&semt=ais'
            title = product.get('title')
            description = product.get('description')
            if image_url and title:
                try:
                    bot.send_message(call.message.chat.id, f'{image_url} \n Продукты: {title} \n Описание: {description}')
                except telebot.apihelper.ApiTelegramException as e:
                    print(f"Error sending HTML message: {e}")
            else:
                bot.send_message(call.message.chat.id, f'Невозможно получить информацию о продукте')
    if call.data == 'buskets':
         if is_activate == True:
            global email
            response = get_buskets(URL, email)
            for product in response:
                if product != []:
                        title = product.get('product')
                        quantity = product.get('quantity')
                        bot.send_message(call.message.chat.id, f'Название: {title} \n Количество: {quantity}')
                else: 
                    bot.send_message(call.message.chat.id, 'Ваша корзина пуста')
         else:
            bot.send_message(call.message.chat.id, 'Вы не вошли в аккаунт')
    if call.data == 'products_by_category':
        murkup = InlineKeyboardMarkup(row_width = 2)
        global categories
        categories = []
        for category in get_categories(URL):
            murkup.row(InlineKeyboardButton(category.get('title'), callback_data=category.get('slug')))
            categories.append(category.get('slug'))
        
        bot.send_message(call.message.chat.id, 'Выберите категорию:', reply_markup=murkup)

    if call.data in categories:
        products_info = get_products_by_category(URL , call.data)
        if products_info != None:
            for product in products_info:
                bot.send_message(call.message.chat.id, f'Название: {product.get("title")} \n Описание: {product.get("description")} \n Цена: {product.get("price")}')
        else:
            bot.send_message(call.message.chat.id, 'Нет продуктов')

bot.polling()



