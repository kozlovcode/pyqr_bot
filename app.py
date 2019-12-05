import os
import qrcode
import telebot

# Указываем токен бота
bot = telebot.TeleBot('YOU BOT TOKEN')

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

# Запускаем бота
bot.polling()