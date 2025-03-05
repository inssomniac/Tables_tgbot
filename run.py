import csv
import requests
import asyncio
import logging
from os import getenv
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from model import db, Students as Table

load_dotenv()

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = getenv("BOT_TOKEN")
CSV_URL = getenv("CSV_URL")
ADMIN_ID = int(getenv("ADMIN_ID") or 0)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def fast_check():
    try:
        response = requests.get(CSV_URL)
        response.encoding = response.apparent_encoding
        data = response.text
        reader = csv.reader(data.splitlines())

        for row in reader:
            if len(row) < 4 or row[0] == 'Имя Фамилия' or row[3] == 'Баллы' or row[0] == '':
                continue

            student = db.query(Table).filter_by(student=row[0]).first()
            points = int(row[3]) if row[3].isdigit() else 0

            if student:
                if student.merge_request != row[2]:
                    student.merge_request = row[2]
                    db.commit()
                if student.points != points:
                    student.points = points
                    db.commit()
            else:
                db.add(Table(student=row[0], group=row[1], merge_request=row[2], points=points))
                db.commit()

    except Exception as e:
        logging.error(f"Ошибка при обновлении данных: {e}")

async def check_updates_periodically():
    while True:
        list_of_students = []
        try:
            response = requests.get(CSV_URL)
            response.encoding = response.apparent_encoding
            data = response.text
            reader = csv.reader(data.splitlines())

            for row in reader:
                if len(row) < 4 or row[0] == 'Имя Фамилия' or row[3] == 'Баллы' or row[0] == '':
                    continue

                student = db.query(Table).filter_by(student=row[0]).first()
                points = int(row[3]) if row[3].isdigit() else 0

                if student:
                    if student.merge_request != row[2]:
                        student.merge_request = row[2]
                        db.commit()
                        list_of_students.append(
                            f'Новый merge-request!\n{row[0]} с баллами {points}\nСсылка: {row[2]}'
                        )
                    elif student.points != points:
                        student.points = points
                        db.commit()
                else:
                    db.add(Table(student=row[0], group=row[1], merge_request=row[2], points=points))
                    db.commit()
                    list_of_students.append(
                        f'Новый merge-request!\n{row[0]} с баллами {points}\nСсылка: {row[2]}'
                    )

        except Exception as e:
            logging.error(f"Ошибка при обновлении данных: {e}")

        if list_of_students:
            message = '\n\n'.join(list_of_students)
            await bot.send_message(chat_id=ADMIN_ID, text=message)

        logging.info("Проверка обновлений завершена")
        await asyncio.sleep(600)

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Помощь", callback_data="help_info")]
    ])
    await message.answer("Привет! Я бот уведомлений о новых мердж реквестах.\nВыберите действие:", reply_markup=keyboard)

@dp.message(Command("help"))
async def help_cmd(message: types.Message):
    help_text = (
        "Доступные команды:\n"
        "/start — запустить бота и показать меню\n"
        "/help — получить справочную информацию\n"
        "/find — найти мерж-реквест по фамилии\n\n"
        "Также вы можете использовать кнопки для быстрого доступа к функциям."
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Закрыть", callback_data="close_help")]
    ])
    await message.answer(help_text, reply_markup=keyboard)

@dp.callback_query(F.data == "help_info")
async def help_info_callback(callback: types.CallbackQuery):
    help_text = (
        "Доступные команды:\n"
        "/start — запустить бота и показать меню\n"
        "/help — получить справочную информацию\n"
        "/find — найти мерж-реквест\n\n"
        "Также вы можете использовать кнопки для быстрого доступа к функциям."
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Закрыть", callback_data="close_help")]
    ])
    await callback.message.edit_text(help_text, reply_markup=keyboard)
    await callback.answer()

@dp.callback_query(F.data == "close_help")
async def close_help_callback(callback: types.CallbackQuery):
    await callback.message.edit_text("Привет! Я бот уведомлений о новых мердж реквестах.\nВыберите действие:")
    await callback.answer()

@dp.message(Command("find"))
async def find_merge_request(message: types.Message):
    await message.answer("Введите фамилию или имя студента для поиска мерж-реквеста:")

@dp.message()
async def search_student_merge_request(message: types.Message):
    student_name = message.text.strip()
    fast_check()
    student = db.query(Table).filter(Table.student.ilike(f"%{student_name}%")).first()

    if student:
        response = (
            f"{student.student}\nСсылка: {student.merge_request}\n"
            f"Баллы: {student.points}"
        )
    else:
        response = f"Студент с фамилией {student_name} не найден."

    await message.answer(response)

async def main():
    asyncio.create_task(check_updates_periodically())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
