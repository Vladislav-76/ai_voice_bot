import dotenv
import os
import telebot
from gtts import gTTS

dotenv.load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


# Обработчик команды /start
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать! Отправьте мне сообщение, и я его озвучу.")


# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text

    try:
        # Создание аудиофайла с озвучкой текста
        tts = gTTS(user_text, lang='ru')
        audio_file = "audio.mp3"
        tts.save(audio_file)

        # Отправка аудиофайла обратно пользователю
        with open(audio_file, 'rb') as audio:
            bot.send_voice(message.chat.id, audio)

        # Удаление временного аудиофайла
        os.remove(audio_file)

    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")


# Запуск бота
if __name__ == "__main__":
    bot.polling(none_stop=True)
