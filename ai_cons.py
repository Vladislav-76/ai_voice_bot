import dotenv
import openai
import os

dotenv.load_dotenv()
# Замените {PROXY_API_KEY} на ваш реальный API ключ
api_key = os.getenv("PROXY_API_KEY", "{PROXY_API_KEY}")

# Инициализация клиента OpenAI
client = openai.OpenAI(api_key=api_key, base_url="https://api.proxyapi.ru/openai/v1")


def chat_with_ai():
    print("Добро пожаловать в консольный чат с нейросетью (GPT-3.5-turbo)!")
    print("Введите 'exit' для завершения сессии.\n")

    while True:
        user_input = input("Вы: ")
        messages = [
            {"role": "user", "content": user_input},
            {"role": "system", "content": "Нейросеть: "},
        ]

        if user_input.lower() == 'exit':
            print("Завершение сессии. До свидания!")
            break

        try:
            chat_completion = client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                messages=messages,
            )

            ai_response = chat_completion.choices[0].message.content
            print(f"Нейросеть: {ai_response}\n")

        except Exception as e:
            print(f"Произошла ошибка: {e}\n")


if __name__ == "__main__":
    chat_with_ai()
