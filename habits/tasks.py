from celery import shared_task
import pytz
from datetime import timedelta

from config import settings
from django.utils.datetime_safe import datetime

from habits.models import Habit
from habits.services import send_telegram_message


@shared_task
def send_habit_reminder():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    # создание объекта с применением фильтра
    habits = Habit.objects.filter(first_habit_date__lte=current_datetime).filter(is_pleasant=False)

    for habit_item in habits:
        if habit_item.owner.tg_chat_id:
            if habit_item.next_habit_date is None:
                habit_item.next_habit_date = current_datetime
                habit_item.save()
            if habit_item.next_habit_date <= current_datetime and habit_item.next_habit_date:
                if habit_item.habit_time <= current_datetime.time():
                    message = f"Здравствуйте, {habit_item.owner.email}! Время выполнять привычку {habit_item.action}"
                    try:
                        send_telegram_message(chat_id=habit_item.owner.tg_chat_id, message=message)
                    except Exception as e:
                        print(str(e))
                    habit_item.next_habit_date += timedelta(days=habit_item.period)
                    habit_item.save()
        else:
            print(f"У пользователя {habit_item.owner.email} не указан айди телеграм-чата")
