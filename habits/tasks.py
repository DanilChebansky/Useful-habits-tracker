import smtplib
from celery import shared_task
import pytz
from datetime import timedelta

from config import settings
from django.utils.datetime_safe import datetime
from django.core.mail import send_mail

from habits.models import Habit


@shared_task
def send_habit_reminder():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    # создание объекта с применением фильтра
    habits = Habit.objects.filter(first_habit_date__lte=current_datetime).filter(is_pleasnt=False)

    for habit_item in habits:
        if habit_item.owner.tg_chat_id:
            if habit_item.next_habit_date is None:
                habit_item.next_habit_date = current_datetime
                habit_item.save()
            if habit_item.next_habit_date <= current_datetime and habit_item.next_habit_date:
                if habit_item.habit_time <= current_datetime.time:

                    try:
                        send_mail(subject=habit_item.place,
                                  message=habit_item.action,
                                  from_email=settings.EMAIL_HOST_USER,
                                  recipient_list="dan14n97@yandex.ru",
                                  fail_silently=False)
                    except smtplib.SMTPException as e:
                        print(str(e))
                    habit_item.next_habit_date += timedelta(minutes=habit_item.period)
                    habit_item.save()
        else:
            print(f"У пользователя {habit_item.owner.email} не указан айди телеграм-чата")
