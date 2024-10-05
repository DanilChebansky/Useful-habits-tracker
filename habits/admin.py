from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "owner",
        "action",
        "is_pleasant",
        "related_habit",
        "period",
        "award",
        "action_time",
        "is_published",
    )
