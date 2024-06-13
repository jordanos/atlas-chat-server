from chat.utils import subscribe_to_room
from common.permissions import IsOwner
from django_filters import rest_framework as filters
from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import User
from users.serializers import UserSerializer

from .models import Message, Room
from .serializers import (
    AddUserSerializer,
    JoinPrivateRoomSerializer,
    JoinRoomSerializer,
    LeaveRoomSerializer,
    MessageSerializer,
    RoomSerializer,
)


class RoomList(generics.ListCreateAPIView):
    queryset = Room.objects.all().order_by("-id")
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        self.queryset = self.queryset.filter(users__in=[user])
        return super().get_queryset()


class RoomDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]


class RoomUsers(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        room = Room.objects.get(pk=pk)
        # TODO: if room not found raise 404 exception
        self.queryset = room.users.order_by("-is_online")
        return super().get(request, *args, **kwargs)


class JoinRoom(generics.UpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = JoinRoomSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class AddUser(generics.CreateAPIView):
    serializer_class = AddUserSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data["user"]
            room = Room.objects.get(pk=pk)
            if room.type == "private" and room.users.count() >= 2:
                raise serializers.ValidationError(
                    {
                        "non_field_errors": [
                            "Room max user limit(2) reached, Create a public room if you want to chat with more users."
                        ]
                    }
                )
            room.users.add(user)
            # ws of new added user subscribe
            subscribe_to_room(room=room, user=user)
        return Response(
            RoomSerializer(room).data,
            status=201,
        )


class JoinPrivateRoom(generics.CreateAPIView):
    serializer_class = JoinPrivateRoomSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            to_user = serializer.validated_data["to_user"]
            from_user = self.request.user
            room = (
                Room.objects.filter(type="private", users__in=[from_user])
                .filter(users__in=[to_user])
                .first()
            )
            if room is None:
                room = Room.objects.create(
                    name=f"{from_user.username}_{to_user.username}",
                    type="private",
                    owner=from_user,
                )
                room.users.add(from_user)
                room.users.add(to_user)
                # subscribe ws for new room creation
                subscribe_to_room(room=room, user=from_user)
                subscribe_to_room(room=room, user=to_user)
        return Response(
            RoomSerializer(room).data,
            status=201,
        )


class LeaveRoom(generics.UpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = LeaveRoomSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class MessagesFilter(filters.FilterSet):
    class Meta:
        model = Message
        fields = ["room"]


class MessageList(generics.ListCreateAPIView):
    queryset = Message.objects.all().order_by("-id")
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = MessagesFilter

    def get_queryset(self):
        user = self.request.user
        # TODO: filter messages based on current user
        return super().get_queryset()


class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsOwner]
