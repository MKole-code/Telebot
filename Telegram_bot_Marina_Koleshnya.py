from bs4 import BeautifulSoup
import requests
import time
import telebot
from telebot import types
import threading

token = "1864621609:AAGTulFpiowjam7_cVlCYnJxwNPD82HMuq4"

bot = telebot.TeleBot(token=token)

users = set()
print(users)
@bot.message_handler(commands=['start', 'help'])
def start(message):
    user_id = message.chat.id
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    bot.send_message(user_id, "Привет! Я бот, который познакомит тебя с афишей джазовых концертов в Москве на неделю.") #, reply_markup=keyboard)

    button1 = types.InlineKeyboardButton(text="Афиша концертов на неделю", callback_data="button1")
    button2 = types.InlineKeyboardButton(text="Подписка на рассылку раз в неделю", callback_data="button2")

    keyboard.add(button1)
    keyboard.add(button2)

    bot.send_message(message.chat.id, "Жми на кнопку!", reply_markup=keyboard)
    bot.send_message(user_id, "Чтобы отписаться, набери /unsubscribe")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "button1":
            bot.send_message(call.message.chat.id, answer)
        if call.data == "button2":

            bot.send_message(call.message.chat.id, "Заявка на еженедельную подписку принята!")
            users.add(call.message.chat.id)



url = 'https://www.afisha.ru/msk/schedule_concert/na-nedelyu/jazz/?sort=date&view=list/'
page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')
events = soup.findAll('li', class_='SlE6Y _1gSmu')


answer = ''
for i in events:
    event = i.find('section').find('h3').find('a').get_text()
    try:
        desc = i.find('section').find('div', class_='').get_text()
    except:
        desc = 'Нет описания'
    date = i.find('section').find('div', class_='_1Jo7v').get_text()
    answer += event + " "+ desc.replace("Нет описания", "") + " " + date + " " + '\n\n'

print(answer)


def mailing():
    while True:
        #print("start mailing", users)
        for user in users:
            bot.send_message(user, answer)
        #time.sleep(3600*24*7) # код для рассылки раз в неделю
        time.sleep(20) # код для отладки time.sleep()


@bot.message_handler(commands=['unsubscribe'])
def unsubscribe(message):
    try:
        users.discard(message.chat.id)
    except:
        pass


thread = threading.Thread(target=mailing)
thread.start()

bot.polling(none_stop=True)

