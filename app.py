import os
import qrcode
import telebot
from flask import Flask, request

# Указываем токен бота
bot = telebot.TeleBot(os.environ['TOKEN'])

# Создаем flask сервер
server = Flask(__name__)

# Обрабатываем комманду /start
@bot.message_handler(commands=['start'])
def startfunc(message):
	bot.send_message(message.from_user.id, 'Отправь мне сообщение, а я сделаю из него QRCode')

# Обрабатываем входящие сообщения
@bot.message_handler(content_types=['text'])
def qrfunc(message):
	# Сохраняем ID чата
	chatid = message.from_user.id
	# Генерируем qrcode из входящени сообщения
	img = qrcode.make(message.text)
	# Сохраняем qrcode в png. В качестве имени используем ID чата
	# чтобы не было проблем при одновременном обращении разных пользователей
	img.save(f'{chatid}.png')
	# Открываем файл qrcode на чтение
	img = open(f'{chatid}.png', 'rb')
	# Отправляем открытый на чтение файл
	bot.send_photo(chatid, img)
	# Закрываем файл
	img.close()
	# Удаляем файл
	os.remove(f'{chatid}.png')

# Принимаем все запросы на корневой адрес / и передаем их боту
@server.route('/', methods=['POST'])
def getMessage():
	bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
	return "!", 200

# Запускаем flask сервер
if __name__ == "__main__":
	server.run()
