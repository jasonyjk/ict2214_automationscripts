import telebot

BOT_TOKEN = '6920332421:AAFSc27xb_6AEKgXywTqdm7yoFHNzt8RvnE'
bot = telebot.TeleBot(BOT_TOKEN)

#def send_automated_messages():
#    chat_id = '6920332421'  # Replace with the chat ID where you want to send messages
#    while True:
#        try:
#            bot.send_message(chat_id, "/start")
#            time.sleep(10)  # Adjust the interval as needed
#        except Exception as e:
#            print(e)
#            time.sleep(10)

try:
    print("Bot Running...")
    @bot.message_handler(commands=['start', 'hello'])
    def send_welcome(message):
        bot.reply_to(message, "ITP Message Bot Activated, Polling For Messages...")

    @bot.message_handler(func=lambda msg: True)
    def echo_all(message):
        bot.reply_to(message, message.text)

    #@bot.message_handler(commands=['get_chat_id'])
    #def get_chat_id(message):
    #    chat_id = message.chat.id
    #    bot.reply_to(message, f"Your chat ID is: {chat_id}")

    # Start the automated messaging in a separate thread
    #automated_message_thread = threading.Thread(target=send_automated_messages)
    #automated_message_thread.daemon = True
    #automated_message_thread.start()

    bot.infinity_polling()

    print("Bot Running...")
except Exception as e:
    print(e)