import os
import dotenv
import openai
import telebot

# Загрузка переменных окружения
dotenv.load_dotenv()
api_key = os.getenv("PROXY_API_KEY", "{PROXY_API_KEY}")
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN", "{YOUR_TELEGRAM_BOT_TOKEN}")

# Инициализация OpenAI и Telegram Bot API
client = openai.OpenAI(api_key=api_key, base_url="https://api.proxyapi.ru/openai/v1")
bot = telebot.TeleBot(telegram_token)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать в чат с нейросетью (GPT-3.5-turbo)!\nВведите 'exit' для завершения сессии.")


# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text

    if user_input.lower() == 'exit':
        bot.reply_to(message, "Завершение сессии. До свидания!")
        return

    messages = [
        {"role": "user", "content": user_input},
        {"role": "system", "content": "Нейросеть: "},
    ]

    try:
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )

        ai_response = chat_completion.choices[0].message.content
        bot.reply_to(message, f"Нейросеть: {ai_response}")

    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")


# Запуск бота
if __name__ == "__main__":
    bot.polling(none_stop=True)
