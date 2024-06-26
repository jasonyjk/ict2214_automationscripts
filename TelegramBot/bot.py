import telebot

# Set bot token here
BOT_TOKEN = 'BOT TOKEN HERE'
bot = telebot.TeleBot(BOT_TOKEN)

try:
    print("Bot Running...")

    # Bot only accepts /start and /hello
    @bot.message_handler(commands=['start', 'hello'])
    def send_welcome(message):
        bot.reply_to(message, "ITP Message Bot Activated, Polling For Messages...")

    # Bot replies to your message
    @bot.message_handler(func=lambda msg: True)
    def echo_all(message):
        bot.reply_to(message, message.text)

    # Bot always listens for your command message 
    bot.infinity_polling()

# Handle errors by printing out.
except Exception as e:
    print(e)