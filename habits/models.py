from django.db import models
from django.core.validators import MaxValueValidator
from users.models import User

NULLABLE = {"blank": True, "null": True}
# Create your models here.


class Habit(models.Model):
    owner = models.ForeignKey(
        User,
        **NULLABLE,
        on_delete=models.CASCADE,
        related_name="habits",
        verbose_name="Пользователь",
    )
    place = models.CharField(
        **NULLABLE,
        max_length=255,
        verbose_name="Место выполнения привычки",
        help_text="Укажите место выполнения привычки",
    )
    habit_time = models.TimeField(
        **NULLABLE,
        verbose_name="Время напоминания о выполнении привычки",
        help_text="Укажите время напоминания о выполнении привычки",
    )
    action = models.CharField(
        max_length=255,
        verbose_name="Действие",
        help_text="Укажите, в чем заключается привычка",
    )
    is_pleasant = models.BooleanField(
        verbose_name="Признак приятной привычки",
        help_text="Укажите, приятная ли привычка",
        default=False,
    )
    related_habit = models.ForeignKey(
        "self",
        **NULLABLE,
        on_delete=models.CASCADE,
        related_name="related_habits",
        verbose_name="Связанная привычка",
        help_text="Укажите связаную привычку",
    )
    period = models.PositiveIntegerField(
        **NULLABLE,
        validators=[MaxValueValidator(7)],
        verbose_name="Периодичность",
        help_text="Укажите, раз во сколько дней будет выполняться привычка",
    )
    award = models.CharField(
        **NULLABLE,
        max_length=255,
        verbose_name="Вознаграждение",
        help_text="Укажите, чем будете себя вознаграждать за выполнение",
    )
    action_time = models.PositiveIntegerField(
        **NULLABLE,
        validators=[MaxValueValidator(120)],
        verbose_name="Время на выполнение",
        help_text="Укажите время выполнения привычки в секундах",
    )
    is_published = models.BooleanField(
        verbose_name="Признак публичности",
        help_text="Укажите, доступна ли Ваша привычка, как пример для заполнения другими пользователями",
        default=False,
    )
    first_habit_date = models.DateTimeField(
        verbose_name='Дата и время первого выполнения привычки', auto_now_add=True
    )
    next_habit_date = models.DateTimeField(
        verbose_name='Дата и время следующего выполнения привычки',
        **NULLABLE
    )

    def __str__(self):
        # Строковое отображение объекта
        return f'Привычка {self.action} пользователя {self.owner}'

    class Meta:
        verbose_name = 'Привычка'  # Настройка для наименования одного объекта
        verbose_name_plural = 'Привычки'  # Настройка для наименования набора объектов
