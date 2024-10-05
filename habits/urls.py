from django.urls import path

from habits.apps import HabitsConfig
from habits.views import (
    HabitOwnerListAPIView,
    HabitPublishedListAPIView,
    HabitCreateAPIView,
    HabitUpdateAPIView,
    HabitDestroyAPIView,
    HabitRetrieveAPIView,
)

app_name = HabitsConfig.name

urlpatterns = [
    path("", HabitOwnerListAPIView.as_view(), name="owner_habits_list"),
    path(
        "published/", HabitPublishedListAPIView.as_view(), name="published_habits_list"
    ),
    path("<int:pk>/", HabitRetrieveAPIView.as_view(), name="habits_retrieve"),
    path("<int:pk>/update/", HabitUpdateAPIView.as_view(), name="habits_update"),
    path("<int:pk>/delete/", HabitDestroyAPIView.as_view(), name="habits_delete"),
    path("create/", HabitCreateAPIView.as_view(), name="habits_create"),
]
