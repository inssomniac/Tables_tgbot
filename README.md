# Telegram бот для уведомлений о новых мердж-запросах

Этот бот создан для уведомления преподавателя по программированию о новых мерж-запросах, которые добавляют студенты. Он
автоматически отслеживает изменения в гугл таблице с мерж-запросами и сообщает преподавателю о новых запросах для
проверки.

## Функции бота

- Уведомление о новых мерж-запросах с баллами студентов.
- Поиск мерж-запросов по фамилии студента.
- Отображение справочной информации о работе бота.
- Поддержка команд и кнопок для удобного взаимодействия.

## Требования

Для запуска бота понадобится следующее:

- Python 3.8 или выше
- Библиотеки:
    - `aiogram 3.18` — для взаимодействия с Telegram API.
    - `requests 2.32` — для запросов к гугл таблице.
    - `sqlalchemy 2.0` — для работы с базой данных.
    - `python-dotenv` — для работы с переменными окружения.
    - `aiohttp 3.11` — для асинхронных запросов.

- Ссылка на Google таблицу, информацию из которой необходимо собирать (столбцы в нём должны быть организованы определённым образом)
- Токен бота (можно получить в Telegram с помощью `@BotFather`)
- Свой айди в телеграм (можно получить в Telegram с помощью `@getmyid_bot`)

## Структура файлов

- `run.py` — основной файл для запуска бота.
- `model.py` — файл с моделью базы данных для хранения информации о студентах и их мерж-запросах.
- `.env` — файл для хранения конфиденциальных данных, таких как токен бота, адреса таблицы и ID администратора. В `.env` файл необходимо написать следующее:
  - `BOT_TOKEN = "{ваш токен}"`
  - `ADMIN_ID = "{ваш айди}"`
  - `CSV_URL = "{ваша ссылка на Google таблицу}" `

## Используемые команды

- `/start` — запускает бота и выводит меню с кнопками.
- `/help` — выводит справочную информацию о работе бота.
- `/find` — запускает поиск мерж-запроса по фамилии студента.

## Примечания

- Бот преобразует данные из Google таблицы в csv файл для получения данных о мерж-запросах. Он автоматически обновляет
  информацию и уведомляет администратора о новых запросах.
- Бот работает с базой данных SQLite для хранения информации о студентах.

