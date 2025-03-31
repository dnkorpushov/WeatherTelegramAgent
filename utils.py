import requests
from dotenv import load_dotenv
import os


def get_weather(city, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}appid={api_key}&q={city}&units=metric&lang=ru"
    
    response = requests.get(complete_url)
    
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
            directions = ["северный", 
                          "северо-восточный", 
                          "восточный",
                          "юго-восточный",
                          "южный",
                          "юго-западный",
                          "западный",
                          "северо-западный"]
            index = int((degrees + 22.5)/45)
            return directions[index % 8]
        
        wind_direction = degrees_to_cardinal(wind_direction_degrees)
        
        return (f"Сейчас в г. {city} {weather_description}, "
                f"температура {current_temperature}°C, ветер {wind_direction}, "
                f"{wind_speed} м/с")
    else:
        return ""


def get_city_name_by_coords(lat, lon, api_key, lang='ru'):
    base_url = "http://api.openweathermap.org/geo/1.0/reverse?"
    url = f"{base_url}lat={lat}&lon={lon}&limit=1&appid={api_key}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
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
    lang = "ru"

    load_dotenv()
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")

    city_name = get_city_name_by_coords(lat, lon, api_key, lang)
    print(f"Город: {city_name}")
    print(get_weather(city=city_name, api_key=api_key))
