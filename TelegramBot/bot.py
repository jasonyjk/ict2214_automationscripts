import telebot

BOT_TOKEN = 'BOT TOKEN HERE'
bot = telebot.TeleBot(BOT_TOKEN)

try:
    print("Bot Running...")
    @bot.message_handler(commands=['start', 'hello'])
    def send_welcome(message):
        bot.reply_to(message, "ITP Message Bot Activated, Polling For Messages...")

    @bot.message_handler(func=lambda msg: True)
    def echo_all(message):
        bot.reply_to(message, message.text)

    bot.infinity_polling()

    print("Bot Running...")
except Exception as e:
    print(e)