from django.urls import path

from .views import (
    AddUser,
    JoinPrivateRoom,
    JoinRoom,
    LeaveRoom,
    MessageDetail,
    MessageList,
    RoomDetail,
    RoomList,
    RoomUsers,
)

urlpatterns = [
    path("", MessageList.as_view(), name="message-list-create"),
    path("<int:pk>/", MessageDetail.as_view(), name="message-detail"),
    path("rooms/", RoomList.as_view(), name="room-list-create"),
    path("rooms/<int:pk>/", RoomDetail.as_view(), name="room-detail"),
    path("rooms/<int:pk>/join/", JoinRoom.as_view(), name="join-room"),
    path("rooms/<int:pk>/leave/", LeaveRoom.as_view(), name="leave-room"),
    path("rooms/<int:pk>/users/", RoomUsers.as_view(), name="room-users"),
    path("rooms/<int:pk>/add-user/", AddUser.as_view(), name="room-users"),
    path("rooms/join-private/", JoinPrivateRoom.as_view(), name="room-users"),
]
