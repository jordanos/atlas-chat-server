from common.options import ChatTypes
from django.db import models
from users.models import User


# room model
class Room(models.Model):
    name = models.CharField(max_length=25, blank=False, null=False, unique=True)
    users = models.ManyToManyField(to=User)
    type = models.CharField(
        max_length=25,
        blank=False,
        null=False,
        choices=[[t.value, t.value] for t in ChatTypes],
    )
    owner = models.ForeignKey(
        to=User, related_name="room_owners", on_delete=models.DO_NOTHING, null=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# message model
class Message(models.Model):
    text = models.TextField()
    owner = models.ForeignKey(
        to=User, related_name="owners", on_delete=models.DO_NOTHING, null=False
    )
    room = models.ForeignKey(
        to=Room, related_name="rooms", on_delete=models.CASCADE, null=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
