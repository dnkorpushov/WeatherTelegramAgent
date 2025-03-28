# WeatherTelegramAgent
Телеграм-бот "Погодный консультант" с ИИ-агентом на Gigachat.
Для работы нужны токены GigaChat, OpenWeatherMap и токен вашего телеграм-бота.

## Запуск
Скопируйте файл `sample.env`

```
cp sample.env .env
```

Укажите в файле `.env` все токены.
```
TELEGRAM_TOKEN=<токен вашего телеграм-бота>
GIGACHAT_TOKEN=<токен API Gigachat>
OPENWEATHERMAP_API_KEY=<API key OpenWeatherMap>
```

Запуск проекта:
```
python3 main.py
```

## Сборка и запуск в Docker
### Сборка контейнера
```
docker build -t weather-telegram-agent .
```

### Запуск контейнера 
```
docker run -it -d --env-file ./.env --restart unless-stopped weather-telegram-agent
```
