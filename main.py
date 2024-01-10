import telebot
import csv
from datetime import datetime
import pytz

# Replace 'YOUR_BOT_TOKEN' with the token you received from BotFather
bot = telebot.TeleBot('6033648633:AAELkhz1NQSulWVTKjHDPXa12Y9Psa698ZU')


@bot.message_handler(commands=['start'])
def start(message):
    # Ask for the user's name
    bot.send_message(message.chat.id, "Привет, это Мухаммад-Абдурахмон, дай мне знать твое настоящее имя, если ты мне "
                                      "известен, я обязательно одобрю тебя!")
    bot.register_next_step_handler(message, process_name_step)

@bot.message_handler(commands=['chat'])
def chat(message):
    if message.chat.id == 1927099919:
        bot.send_message(1927099919, 'users id:')
        bot.register_next_step_handler(message, send_user_message)
    else:
        bot.send_message(message.chat.id, "Можете писать ответ!")
        bot.register_next_step_handler(message, process_decribe_step)


def process_name_step(message):
    # Store the user's name
    user_name = message.text

    # Get user information
    user_id = message.from_user.id
    user_first_name = message.from_user.first_name
    user_last_name = message.from_user.last_name
    user_username = message.from_user.username

    # Approve the user (replace 'YOUR_CHANNEL_ID' with your channel ID)
    # channel_id = 'https://t.me/+ulk4XZ5VkmxhM2Iy'
    bot.send_message(message.chat.id, f"{user_name} можете подать заявку, приму ваш запрос как буду "
                                      f"онлайн\n\nt.me/+5xjXtgRcA8tkNWI6")

    # Save user information to a CSV file
    tz = pytz.timezone('Asia/Tashkent')  # Use the appropriate time zone
    timestamp = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

    bot.send_message(1927099919, "New member approving: "
                                 f"{user_name, user_id, user_first_name, user_last_name, user_username, timestamp}")
    save_to_csv(user_id, user_first_name, user_last_name, user_username, user_name, timestamp)

def process_decribe_step(message):
    save_message_to_csv(message.from_user.id, message.text)

    bot.send_message(1927099919, f"Message from: {message.chat.id, message.text}")
    bot.send_message(message.chat.id, "Ваш ответ был отправлен, и скоро пересмотрен, спасибо!")

def send_user_message(message):
    with open('user_id.txt', 'w') as txt_file:
        txt_file.write(message.text)
    bot.send_message(1927099919, 'id was successfully saved, write your message to user')
    bot.register_next_step_handler(message, send_user_message_last_step)

def send_user_message_last_step(message):
    with open('user_id.txt', 'r') as txt_file:
        user_id = txt_file.read()
    bot.send_message(user_id, message.text)
    bot.send_message(1927099919, 'your message was successfully delivered')

def save_to_csv(user_id, user_first_name, user_last_name, user_username, user_name, timestamp):
    with open('user_data.csv', 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([user_id, user_first_name, user_last_name, user_username, user_name, timestamp])

def save_message_to_csv(user_id, message_text):
    with open('user_messages.csv', 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([user_id, message_text])

if __name__ == "__main__":
    bot.polling(none_stop=True)
