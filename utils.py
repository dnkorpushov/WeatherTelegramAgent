import requests

def get_weather(api_key, city):
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
        return "Город не найден."

if __name__ == "__main__":
    # Вызов функции для Санкт-Петербурга
    print(get_weather("Санкт-Петербург"))
