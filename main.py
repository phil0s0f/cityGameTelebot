# main.py
import telebot
import os
from bot.CitiesGame import CitiesGame
from bot.llm_city import get_city_description
from bot.voice_processing import voice_to_text, text_to_voice

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TELEGRAM_TOKEN)

cities_game = CitiesGame()


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать в игру Города с GigaChat API!")


@bot.message_handler(commands=['history'])
def show_history(message):
    chat_id = message.chat.id
    history = cities_game.history(chat_id)
    print(f"Запрошена история для чата {chat_id}")
    bot.reply_to(message, f"Список городов использованных в игре: {history}")


@bot.message_handler(content_types=['text'])
def handle_message(message):
    if message.text.lower() in ('сдаюсь', 'сдаюсь!', 'сдаюсь.'):
        handle_give_up(message)
    else:
        handle_city(message)


def handle_give_up(message):
    chat_id = message.chat.id
    print(f"Пользователь {chat_id} сдался")
    history = cities_game.history(chat_id)
    cities_game.give_up(chat_id)
    bot.reply_to(message, f"Ха-ха! Я победил тебя, человечишка! \n{history}")
    return


def handle_city(message):
    chat_id = message.chat.id

    user_input = message.text.lower()

    next_city, is_city = cities_game.turn(chat_id, user_input)

    if is_city:
        kb = telebot.types.InlineKeyboardMarkup()
        kb.add(telebot.types.InlineKeyboardButton('Что это за город?', callback_data='city_info'))
        bot.reply_to(message, next_city, reply_markup=kb)
    else:
        bot.reply_to(message, next_city)


@bot.callback_query_handler(func=lambda x: 'city_info' in x.data)
def get_city_info(query: telebot.types.CallbackQuery):
    bot.edit_message_reply_markup(chat_id=query.message.chat.id,
                                  message_id=query.message.id,
                                  reply_markup=None)
    bot.reply_to(query.message,
                 text=get_city_description(query.message.text))


@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
    try:
        message_id = message.chat.id
        # Получение файла
        file_info = bot.get_file(message.voice.file_id)
        file_path = file_info.file_path

        # Загрузка файла
        downloaded_file = bot.download_file(file_path)

        # Сохранение файла локально
        input_file = f"{message.chat.id}_voice.ogg"
        with open(input_file, "wb") as f:
            f.write(downloaded_file)

        city = voice_to_text(message_id, input_file)
        next_city, is_city = cities_game.turn(message.chat.id, city)
        if is_city:
            output_voice_file = text_to_voice(message_id, next_city)
            with open(output_voice_file, "rb") as voice:
                bot.send_voice(message_id, voice)
            # os.remove(output_voice_file)
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")
        print(f"Ошибка: {e}")


bot.polling()
