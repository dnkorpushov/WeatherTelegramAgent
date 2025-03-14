import requests
from dotenv import load_dotenv
import os


def get_weather(city, api_key):
    # Базовый URL для запросов к API
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    
    # Полный URL запроса с параметром локализации
    complete_url = base_url + "appid=" + api_key + "&q=" + city + "&units=metric&lang=ru"
    
    # Отправка GET-запроса
    response = requests.get(complete_url)
    
    # Получение данных в формате JSON
    data = response.json()
    
    if data["cod"] != "404":
        # Текущая температура (в градусах Цельсия), округляем до целого числа
        current_temperature = round(data["main"]["temp"])
        
        # Описание погоды на русском языке
        weather_description = data["weather"][0]["description"]
        
        # Сила ветра (в метрах в секунду)
        wind_speed = data["wind"]["speed"]
        
        # Направление ветра (в градусах)
        wind_direction_degrees = data["wind"]["deg"]
        
        # Преобразование градусов в понятное направление
        def degrees_to_cardinal(degrees):
            directions = ["северный", "северо-восточный", "восточный", "юго-восточный", "южный", "юго-западный", "западный", "северо-западный"]
            index = int((degrees + 22.5)/45)
            return directions[index % 8]
        
        wind_direction = degrees_to_cardinal(wind_direction_degrees)
        
        # print(f"Текущая температура в {city}: {current_temperature}°C")
        # print(f"Погодные условия: {weather_description}")
        # print(f"Ветер: {wind_speed} м/с, {wind_direction}")
        return f"Сейчас в г. {city} {weather_description}, температура {current_temperature}°C, ветер {wind_direction}, {wind_speed} м/с"
    else:
        return ""


def get_city_name_by_coords(lat, lon, api_key, lang='ru'):
    # Формируем URL для запроса к API
    url = f"http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit=1&appid={api_key}"
    
    # Отправляем GET-запрос
    response = requests.get(url)
    
    # Проверяем статус ответа
    if response.status_code == 200:
        # Парсим JSON ответ
        data = response.json()
        if data:
            city_data = data[0]
            # Проверяем, есть ли локализованное имя для указанного языка
            if 'local_names' in city_data and lang in city_data['local_names']:
                return city_data['local_names'][lang]
            else:
                # Если локализованного имени нет, возвращаем стандартное имя
                return city_data.get('name', "Название города не найдено")
        else:
            return "Город не найден"
    else:
        return f"Ошибка при запросе к API: {response.status_code}"
    

if __name__ == "__main__":
    # Координаты Санкт-Петербурга
    lat = 59.950845
    lon = 30.267091
    # Запрашиваем название города на русском языке
    lang = "ru"

    load_dotenv()
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")

    # Получаем название города на русском языке
    city_name = get_city_name_by_coords(lat, lon, api_key, lang)
    print(f"Название города: {city_name}")
    print(get_weather(city=city_name, api_key=api_key))
