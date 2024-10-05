from rest_framework.serializers import ModelSerializer
from users.models import User


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "phone",
            "city",
            "is_active",
            "tg_chat_id",
            "password",
        )


class AnotherUserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "email", "phone", "city", "is_active", "tg_chat_id")
