from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from users.serializers import UserSerializer, AnotherUserSerializer
from users.permissions import IsSelfUser
from users.models import User


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [AllowAny]
        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        elif self.action in ["update", "partial_update"]:
            self.permission_classes = [IsAuthenticated, IsSelfUser]
        return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):

        if self.action in ["create", "update", "partial_update"]:
            self.serializer_class = UserSerializer
        elif self.action == "retrieve" and self.request.user == super().get_object():
            self.serializer_class = UserSerializer
        else:
            self.serializer_class = AnotherUserSerializer
        return self.serializer_class
