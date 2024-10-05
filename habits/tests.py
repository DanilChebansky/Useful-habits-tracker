from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="testcase@ya.ru")
        self.habit = Habit.objects.create(
            place="At home1",
            habit_time="11:00:00",
            action="1Washing dishes",
            is_pleasant=False,
            period=1,
            award="Eat cookies",
            action_time=120,
            is_published=False,
            owner=self.user,
            related_habit=None,
        )
        self.client.force_authenticate(user=self.user)

    def test_habit_retrieve(self):
        url = reverse("habits:habits_retrieve", args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), self.habit.action)

    def test_habit_create(self):
        url = reverse("habits:habits_create")
        data = {
            "action": "1Reading books",
            "is_pleasant": True,
            "is_published": True,
            "owner": self.user.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_habit_update(self):
        url = reverse("habits:habits_update", args=(self.habit.pk,))
        data = {
            "place": "At home1",
            "habit_time": "11:00:00",
            "action": "1Cooking lunch",
            "is_pleasant": False,
            "period": 1,
            "award": "Eat lunch",
            "action_time": 120,
            "is_published": False,
            "owner": self.user.pk,
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), "1Cooking lunch")
        self.assertEqual(data.get("award"), "Eat lunch")

    def test_habit_delete(self):
        url = reverse("habits:habits_delete", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)

    def test_owner_habit_list(self):
        url = reverse("habits:owner_habits_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.habit.pk,
                    "place": self.habit.place,
                    "habit_time": self.habit.habit_time,
                    "action": self.habit.action,
                    "is_pleasant": self.habit.is_pleasant,
                    "period": self.habit.period,
                    "award": self.habit.award,
                    "action_time": self.habit.action_time,
                    "is_published": self.habit.is_published,
                    "owner": self.user.pk,
                    "related_habit": self.habit.related_habit,
                },
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_published_habit_list(self):
        url = reverse("habits:published_habits_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 0,
            "next": None,
            "previous": None,
            "results": [],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
