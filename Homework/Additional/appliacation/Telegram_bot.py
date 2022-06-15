import telebot
from telebot import types
import sqlite3

token = '5434418723:AAFTtQr4cr6MRO7naQ6XZLh5Fg1V7bJfGVg'
bot = telebot.TeleBot(token)
basket = []

# Connect to database and get user id if not exists
@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('Cafe.db')
    cursor = conn.cursor()

    cursor.execute(f'SELECT  ID FROM Member WHERE User_id = {message.chat.id}')
    data = cursor.fetchone()

    if data is None:
        cursor.execute('INSERT INTO Member(User_id, Name) VALUES (?,?)', (message.chat.id, message.from_user.first_name))
        conn.commit()
        bot.send_message(message.chat.id, text=f'Hello, {message.from_user.first_name}!')

    else:
        bot.send_message(message.chat.id, text=f'Hello, {message.from_user.first_name}!')

    conn.close()

# Making a markups for drinks
@bot.message_handler(commands=['drinks'])
def drinks_keyboard(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Americano', callback_data='1'))
    markup.add(types.InlineKeyboardButton(text='Latte', callback_data='2'))
    markup.add(types.InlineKeyboardButton(text='Cappuccino', callback_data='3'))
    markup.add(types.InlineKeyboardButton(text='Dark coffee', callback_data='4'))
    markup.add(types.InlineKeyboardButton(text='Apple juice', callback_data='5'))
    markup.add(types.InlineKeyboardButton(text='Orange juice', callback_data='6'))
    bot.send_message(message.chat.id, text='Drinks', reply_markup=markup)

# Making a markups for pizza
@bot.message_handler(commands=['pizza'])
def pizza_keyboard(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Margaritta', callback_data='7'))
    markup.add(types.InlineKeyboardButton(text='Hawaii', callback_data='8'))
    markup.add(types.InlineKeyboardButton(text='Vezuvii', callback_data='9'))
    bot.send_message(message.chat.id, text='Pizza', reply_markup=markup)

#Making a markups for deserts
@bot.message_handler(commands=['desert'])
def desert_keyboard(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Mint ice-cream', callback_data='10'))
    markup.add(types.InlineKeyboardButton(text='Chocolate ice-cream', callback_data='11'))
    markup.add(types.InlineKeyboardButton(text='Simple ice-cream', callback_data='12'))
    markup.add(types.InlineKeyboardButton(text='Ice-cream with berries', callback_data='13'))
    markup.add(types.InlineKeyboardButton(text='Muffin', callback_data='14'))
    markup.add(types.InlineKeyboardButton(text='Cake', callback_data='15'))
    markup.add(types.InlineKeyboardButton(text='Biscuit', callback_data='16'))
    markup.add(types.InlineKeyboardButton(text='Donut', callback_data='17'))
    bot.send_message(message.chat.id, text='Deserts', reply_markup=markup)

# Making a function for buy products
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == '1':
        basket.append([call.message.chat.id, 1])

    elif call.data == '2':
        basket.append([call.message.chat.id, 2])

    elif call.data == '3':
        basket.append([call.message.chat.id, 3])

    elif call.data == '4':
        basket.append([call.message.chat.id, 4])

    elif call.data == '5':
        basket.append([call.message.chat.id, 5])

    elif call.data == '6':
        basket.append([call.message.chat.id, 6])

    elif call.data == '7':
        basket.append([call.message.chat.id, 7])

    elif call.data == '8':
        basket.append([call.message.chat.id, 8])

    elif call.data == '9':
        basket.append([call.message.chat.id, 9])

    elif call.data == '10':
        basket.append([call.message.chat.id, 10])

    elif call.data == '11':
        basket.append([call.message.chat.id, 11])

    elif call.data == '12':
        basket.append([call.message.chat.id, 12])

    elif call.data == '13':
        basket.append([call.message.chat.id, 13])

    elif call.data == '14':
        basket.append([call.message.chat.id, 14])

    elif call.data == '15':
        basket.append([call.message.chat.id, 15])

    elif call.data == '16':
        basket.append([call.message.chat.id, 16])

    elif call.data == '17':
        basket.append([call.message.chat.id, 17])

# Clear basket if user make a mistake
@bot.message_handler(commands=['clearbasket'])
def clear_basket(message):
    basket.clear()
    bot.send_message(message.chat.id, text='Basket is cleared')

# Add order in database
@bot.message_handler(commands=['makeorder'])
def make_order(message):
    conn = sqlite3.connect('Cafe.db')
    cursor = conn.cursor()
    for product in basket:
        cursor.execute('INSERT INTO "Order"(User_id, Product_id) VALUES(?,?)', (product[0], product[1]))
        conn.commit()
    basket.clear()
    conn.close()

if __name__ == '__main__':
    bot.infinity_polling()
