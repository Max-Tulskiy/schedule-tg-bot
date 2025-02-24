import logging
import asyncio
import datetime
import pandas as pd
import pytz
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, CallbackContext
from config import (
    TOKEN,
    schedule_odd_name,
    schedule_even_name
)

def is_even_week():
    return datetime.datetime.now().isocalendar()[1] % 2 == 0


def load_schedule(file_path):
    try:
        df = pd.read_csv(file_path, encoding="utf-8-sig", skipinitialspace=True)

        expected_columns = {"День", "Пара", "Время", "Предмет"}
        if not expected_columns.issubset(set(df.columns)):
            raise ValueError(f"В файле {file_path} отсутствуют ожидаемые столбцы. Найдены: {df.columns.tolist()}")

        schedule = {}
        for _, row in df.iterrows():
            day = row["День"].strip() 
            pair_num = row["Пара"].strip()
            entry = f"{pair_num}: {row['Время']} {row['Предмет']}"
            
            if day in schedule:
                schedule[day].append(entry)
            else:
                schedule[day] = [entry]
        
        return schedule
    except Exception as e:
        logging.error(f"Ошибка загрузки файла {file_path}: {e}")
        return {}

even_schedule = load_schedule(schedule_even_name)
odd_schedule = load_schedule(schedule_odd_name)


def get_schedule():
    today = datetime.datetime.now(pytz.timezone("Europe/Moscow")).strftime("%A")
    today = {
        "Monday": "Понедельник",
        "Tuesday": "Вторник",
        "Wednesday": "Среда",
        "Thursday": "Четверг",
        "Friday": "Пятница",
        "Saturday": "Суббота",
        "Sunday": "Воскресенье"
    }.get(today, "Воскресенье")

    schedule = even_schedule if is_even_week() else odd_schedule    
    return schedule.get(today, ["Нет пар"])


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Привет! Я бот с расписанием! Напиши /today, чтобы узнать пары на сегодня.")


async def today(update: Update, context: CallbackContext) -> None:
    schedule = get_schedule()
    await update.message.reply_text("\n\n".join(schedule))


async def set_bot_commands(application: Application):
    commands = [
        BotCommand("start", "Запустить бота"),
        BotCommand("today", "Расписание на сегодня"),
    ]
    await application.bot.set_my_commands(commands)


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("today", today))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(set_bot_commands(app))

    app.run_polling()

if __name__ == '__main__':
    main()
