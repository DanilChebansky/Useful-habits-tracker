from rest_framework import serializers
from habits.models import Habit
from habits.validators import HabitValidator


class HabitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit
        fields = "__all__"
        validators = [
            HabitValidator(
                is_pleasant="is_pleasant",
                award="award",
                related_habit="related_habit",
                place="place",
                habit_time="habit_time",
                period="period",
                action_time="action_time",
            )
        ]
