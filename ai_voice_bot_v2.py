import os
import dotenv
import openai
import telebot
from gtts import gTTS
import speech_recognition as sr
from pydub import AudioSegment

dotenv.load_dotenv()
api_key = os.getenv("PROXY_API_KEY", "your_openai_api_key")
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN", "your_telegram_bot_token")

# Initialize OpenAI API
client = openai.OpenAI(api_key=api_key, base_url="https://api.proxyapi.ru/openai/v1")

# Initialize the Telegram bot
bot = telebot.TeleBot(telegram_token)

# Initialize the speech recognizer
recognizer = sr.Recognizer()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать в чат с нейросетью (GPT-3.5-turbo)!\nВведите 'exit' для завершения сессии.")


@bot.message_handler(content_types=['text'])
def handle_text_message(message):
    user_input = message.text

    if user_input.lower() == 'exit':
        bot.reply_to(message, "Завершение сессии. До свидания!")
        return

    handle_ai_response(message, user_input)


@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
    try:
        # Download the voice message
        file_info = bot.get_file(message.voice.file_id)
        file = bot.download_file(file_info.file_path)

        # Save the voice message to a file
        with open("voice_message.ogg", 'wb') as f:
            f.write(file)

        # Convert OGG to WAV
        audio = AudioSegment.from_ogg("voice_message.ogg")
        audio.export("voice_message.wav", format="wav")

        # Convert the voice message to text
        with sr.AudioFile("voice_message.wav") as source:
            audio_data = recognizer.record(source)
            user_input = recognizer.recognize_google(audio_data, language='ru-RU')

        # Remove the temporary file
        os.remove("voice_message.ogg")

        handle_ai_response(message, user_input)

    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка при распознавании голоса: {e}")


def handle_ai_response(message, user_input):
    messages = [
        {"role": "user", "content": user_input},
    ]

    try:
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )

        ai_response = chat_completion.choices[0].message.content
        tts = gTTS(text=ai_response, lang='ru')
        tts.save("response.mp3")

        with open("response.mp3", "rb") as voice:
            bot.send_voice(message.chat.id, voice)

        os.remove("response.mp3")

    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")


if __name__ == "__main__":
    bot.polling(none_stop=True)
