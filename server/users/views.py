from rest_framework import generics
from rest_framework.permissions import BasePermission, IsAuthenticated

from .models import User
from .serializers import UserSerializer


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all().order_by("-id")
    serializer_class = UserSerializer
    permission_classes: list[BasePermission] = []

    def get_queryset(self):
        order_by = self.request.GET.get("order_by", None)
        if order_by is not None:
            self.queryset = self.queryset.order_by(order_by)
        return super().get_queryset()


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
