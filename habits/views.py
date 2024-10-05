from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)

from habits.models import Habit
from habits.paginators import CustomPagination
from habits.serializers import HabitSerializer
from users.permissions import IsOwner


class HabitCreateAPIView(CreateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer

    def perform_create(self, serializer):
        habit = serializer.save()
        habit.owner = self.request.user
        habit.save()


class HabitOwnerListAPIView(ListAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwner]
    pagination_class = CustomPagination

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset().filter(owner=self.request.user)
        return queryset


class HabitPublishedListAPIView(ListAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = CustomPagination

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset().filter(is_published=True)
        return queryset


class HabitRetrieveAPIView(RetrieveAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwner]


class HabitUpdateAPIView(UpdateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwner]


class HabitDestroyAPIView(DestroyAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwner]
