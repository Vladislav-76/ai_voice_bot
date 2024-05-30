import re
import requests
import telebot

# Замените 'YOUR_API_TOKEN' на ваш реальный API токен, который вы получили от BotFather
API_TOKEN = '7353258115:AAG9RF8MkHu6RS4GWrhByJ6XX-sC3RPOr40'
WEATHER_API_KEY = '6af807436ce282afb165cc47aed9f356'

# Создание экземпляра бота
bot = telebot.TeleBot(API_TOKEN)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать! Я ваш новый бот. Как я могу вам помочь?")


# Обработчик команды /help
@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = (
        "Я могу выполнять следующие команды:\n"
        "/start - Начать общение с ботом\n"
        "/help - Показать это сообщение помощи\n"
        "/reverse_string <текст> - Перевернуть указанный текст\n"
        "/upper_string <текст> - Преобразовать указанный текст в заглавные буквы\n"
        "/vowels_remover <текст> - Удалить все гласные буквы из указанного текста\n"
        "/url_check <текст> - Проверить корректность введенного URL\n"
        "/weather_city <город> - Показать погоду в указанном городе\n"
    )
    bot.reply_to(message, help_text)


# Обработчик команды /reverse_string
@bot.message_handler(commands=['reverse_string'])
def reverse_string(message):
    try:
        # Получаем текст, который нужно перевернуть
        text_to_reverse = message.text[len('/reverse_string '):]
        if text_to_reverse:
            reversed_text = text_to_reverse[::-1]
            bot.reply_to(message, reversed_text)
        else:
            bot.reply_to(message, "Пожалуйста, укажите текст для переворота.")
    except Exception as e:
        bot.reply_to(message, "Произошла ошибка: " + str(e))


# Обработчик команды /upper_string
@bot.message_handler(commands=['upper_string'])
def upper_string(message):
    try:
        # Получаем текст, который нужно преобразовать в заглавные буквы
        text_to_upper = message.text[len('/upper_string '):]
        if text_to_upper:
            upper_text = text_to_upper.upper()
            bot.reply_to(message, upper_text)
        else:
            bot.reply_to(message, "Пожалуйста, укажите текст для преобразования в заглавные буквы.")
    except Exception as e:
        bot.reply_to(message, "Произошла ошибка: " + str(e))


# Обработчик команды /vowels_remover
@bot.message_handler(commands=['vowels_remover'])
def vowels_remover(message):
    try:
        # Гласные буквы на русском и английском языках
        vowels = "АЕЁИОУЫЭЮЯаеёиоуыэюяAEIOUYaeiouy"

        # Получаем текст, из которого нужно удалить гласные
        text_to_process = message.text[len('/vowels_remover '):]
        if text_to_process:
            # Удаляем гласные буквы
            processed_text = ''.join([char for char in text_to_process if char not in vowels])
            bot.reply_to(message, processed_text)
        else:
            bot.reply_to(message, "Пожалуйста, укажите текст для удаления гласных.")
    except Exception as e:
        bot.reply_to(message, "Произошла ошибка: " + str(e))


# Регулярное выражение для проверки корректности URL
URL_PATTERN = re.compile(
    r'^(https?|ftp):\/\/'  # http://, https://, ftp://
    r'([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6}'  # доменное имя
    r'(:[0-9]{1,5})?'  # порт (необязательно)
    r'(\/\S*)?$'  # путь (необязательно)
)


# Обработчик команды /url_check
@bot.message_handler(commands=['url_check'])
def url_check(message):
    # Извлекаем URL, который идет после команды
    url = message.text[len('/url_check '):]
    if URL_PATTERN.match(url):
        bot.reply_to(message, "URL корректен.")
    else:
        bot.reply_to(message, "URL некорректен.")


# Обработчик команды /weather_city
@bot.message_handler(commands=['weather_city'])
def weather_city(message):
    try:
        # Получаем название города
        city_name = message.text[len('/weather_city '):]
        if city_name:
            # Делаем запрос к API погоды
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={WEATHER_API_KEY}&units=metric"
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200:
                # Извлекаем информацию о погоде из ответа API
                weather_description = data['weather'][0]['description']
                temperature = data['main']['temp']
                feels_like = data['main']['feels_like']
                humidity = data['main']['humidity']

                weather_info = (
                    f"Погода в городе {city_name}:\n"
                    f"Описание: {weather_description}\n"
                    f"Температура: {temperature}°C\n"
                    f"Ощущается как: {feels_like}°C\n"
                    f"Влажность: {humidity}%"
                )
                bot.reply_to(message, weather_info)
            else:
                bot.reply_to(
                    message,
                    f"Не удалось получить данные о погоде для города: {city_name}. Проверьте правильность названия."
                )
        else:
            bot.reply_to(message, "Пожалуйста, укажите название города для получения погоды.")
    except Exception as e:
        bot.reply_to(message, "Произошла ошибка: " + str(e))


# Запуск бота
bot.polling()
