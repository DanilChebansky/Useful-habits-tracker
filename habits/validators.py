from rest_framework.serializers import ValidationError
from habits.models import Habit


class HabitValidator:

    def __init__(
        self, is_pleasant, award, related_habit, place, habit_time, period, action_time
    ):
        self.is_pleasant = is_pleasant
        self.award = award
        self.related_habit = related_habit
        self.habits = Habit.objects.all()
        self.place = place
        self.habit_time = habit_time
        self.period = period
        self.action_time = action_time

    def __call__(self, value):
        tmp_val1 = dict(value).get(self.is_pleasant)
        tmp_val2 = dict(value).get(self.award)
        tmp_val3 = dict(value).get(self.related_habit)
        tmp_val4 = dict(value).get(self.place)
        tmp_val5 = dict(value).get(self.habit_time)
        tmp_val6 = dict(value).get(self.period)
        tmp_val7 = dict(value).get(self.action_time)
        if tmp_val1:
            if tmp_val2 is not None or tmp_val3 is not None:
                raise ValidationError(
                    "Pleasant habit can't have award or related habit"
                )
        else:
            if (
                tmp_val4 is None or tmp_val5 is None or tmp_val6 is None or tmp_val7 is None
            ):
                raise ValidationError("Useful habit have to have all parameters")
            elif tmp_val2 is None and tmp_val3 is None:
                raise ValidationError(
                    "Habit have to be pleasant or to have award or related habit"
                )
            elif tmp_val2 is not None and tmp_val3 is not None:
                raise ValidationError(
                    "Habit have to have either award or related habit"
                )
            else:
                if tmp_val2 is None:
                    if self.habits.filter(pk=tmp_val3.id).first().is_pleasant is False:
                        raise ValidationError("Related habit have to be pleasant")
