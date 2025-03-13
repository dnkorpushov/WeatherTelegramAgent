import os
import sys

from langchain_gigachat.tools.giga_tool import giga_tool
from langchain_core.messages import HumanMessage
from langchain_gigachat import GigaChat
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

import telebot
from telebot import types
import signal

from dotenv import load_dotenv

from pydantic import BaseModel, Field
from typing import List

from utils import get_weather


system_prompt = """
Ты консультант по погоде.
Твои задачи:
1. Получи от пользователя название города.
2. Используй инструмент get_current_weather для получения информации погоде в данном городе.
3. Сообщи пользователю текущие погодные условия (температуру, облачность, скорость и направление ветра, наличие осадков).
4. Обязательно дай подробный совет, как одеться пользователю при выходе на улицу исходя из текущих погодных условий.

Отвечай только на вопросы о погоде и рекомендациях как одеться в такую погоду.
На другие вопросы отвечай, что не знаешь ответа.
"""

load_dotenv()

telegram_token = os.getenv("TELEGRAM_TOKEN")
gigachat_token = os.getenv("GIGACHAT_TOKEN")
openweathermap_api_key = os.getenv("OPENWEATHERMAP_API_KEY")

get_current_weather_examples = [
   {
       "request": "Какая сейчас погода в Хургаде",
       "params": {"city":"Хургада"},
   },
   {
       "request": "а какая погода в пхукете",
       "params": {"city":"Пхукет"},
   },
   {
       "request": "что там в каннах",
       "params": {"city":"Канны"},
   }
]


class GetCurrentWeatherResult(BaseModel):
   """
   Модель для хранения результатов текущей погоды.
   """
   weather: str = Field(description="Текущая погода")


@giga_tool(few_shot_examples=get_current_weather_examples)
def get_current_weather(city: str = Field(description="Название города")) -> GetCurrentWeatherResult:
   """
   Функция для получения текущей погоды в указанном городе.
   """
   result = get_weather(openweathermap_api_key, city)
   return  GetCurrentWeatherResult(weather=result)


bot = telebot.TeleBot(telegram_token)
model = GigaChat(
   credentials=gigachat_token,
   scope="GIGACHAT_API_PERS",
   model="GigaChat",
   verify_ssl_certs=False
)

tools = [get_current_weather]
model_with_functions = model.bind_functions(tools)
agent = create_react_agent(model_with_functions, tools=tools, checkpointer=MemorySaver(), state_modifier=system_prompt)

@bot.message_handler(commands=['start'])
def start_bot(message):
   """
   Обработчик команды /start.
   """
   markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
   repeat_button = types.KeyboardButton("Начать сначала")
   markup.add(repeat_button)

   first_message = f"{message.from_user.first_name}, привет!\nЯ погодный консультант, в каком городе находишся?"
   bot.send_message(message.chat.id, first_message, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Начать сначала")
def do_repeat(message):
   """
   Обработчик команды "Начать сначала".
   """
   start_bot(message)

@bot.message_handler(content_types=['text'])
def answer(message):
   """
   Обработчик текстовых сообщений.
   """
   config = {"configurable": {"thread_id": message.chat.id}}
   try:
       response = agent.invoke({"messages": [HumanMessage(content=message.text)]}, config)
       bot.send_message(message.chat.id, response["messages"][-1].content)
   except:
       bot.send_message(message.chat.id, "Что-то пошло не так :( Попробуй еще раз.")

def stop_bot(sig, frame):
   """
   Функция для остановки бота.
   """
   print("Агент завершил работу.")
   bot.stop_polling()
   sys.exit(0)


if __name__ == "__main__":
   signal.signal(signal.SIGINT, stop_bot)
   print("Агент готов. Ctrl-C для завершения работы.")
   bot.infinity_polling()
