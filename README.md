# Auto Publisher для Telegram-канала

Скрипт для автоматической публикации фотографий в Telegram-канал с заданным интервалом.

## Как установить

1. Установите зависимости:

```bash
pip install python-telegram-bot python-dotenv
```

2. Создайте файл .env в той же папке и добавьте:

```text
TG_TOKEN=ваш_токен_бота
PUBLISH_DELAY_HOURS=4
API_KEY_NASA=ваш_ключ_nasa_api
TG_CHAT_ID=ваш_телеграм_канал
```

Описание переменных окружения:
TG_TOKEN - токен вашего Telegram бота (получить у @BotFather)  
PUBLISH_DELAY_HOURS - задержка между публикациями в часах (по умолчанию 4)  
API_KEY_NASA - API ключ для доступа к NASA API (получить на api.nasa.gov)  
TG_CHAT_ID - ID вашего Telegram канала (например, @all_ab_sp)

## Как использовать

Запустите скрипт из папки с фотографиями:

```bash
python auto_publisher.py
```

## Настройка задержки

1. Через аргумент командной строки:

```bash
python auto_publisher.py --delay 6  # публикация каждые 6 часов
```

2. Через переменную окружения (в файле .env):

```text
PUBLISH_DELAY_HOURS=8
```

## Как работает

1. Скрипт ищет все `.jpg`, `.png`, `.jpeg` файлы во всех подпапках

2. Перемешивает их случайным образом

3. Публикует по одной фотографии в канал `@all_ab_sp`

4. Ждет заданное количество часов

5. Повторяет бесконечно

## Пример работы скрипта

После запуска скрипт начинает публиковать фотографии. В консоли вы увидите сообщения об ошибках, если они возникнут:

```bash
$ python auto_publisher.py
Ошибка при публикации ./images/space1.jpg: [детали ошибки]
```

Если фотографий нет в папке:

```bash
Нет фотографий для публикации.
```

При успешной публикации в консоль ничего не выводится, только при ошибках. Проверяйте публикации в самом Telegram-канале @all_ab_sp.

## Как скачать фотографии для публикации

1. Из NASA API и SpaceX API

```bash
python fetch_nasa_apod.py
```

```bash
python fetch_nasa_epic.py
```

```bash
python fetch_spacex_images.py
```

2. Скачать готовые изображения
   Поместите фотографии в формате .jpg, .png, .jpeg в папку images/ рядом со скриптом.
   Структура папки:

```text
tg_space_channel/
├── auto_publisher.py
├── .env
├── requirements.txt
├── README.md
└── images/ # ваши фотографии здесь
    ├── space1.jpg
    ├── space2.png
    └── more/ # или в подпапках
        └── space3.jpeg
```
