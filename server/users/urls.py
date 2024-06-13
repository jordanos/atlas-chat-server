from django.urls import path

from .views import UserDetail, UserList

urlpatterns = [
    path("", UserList.as_view(), name="user-list-create"),
    path("<int:pk>/", UserDetail.as_view(), name="user-detail"),
]
