import channels.layers
from asgiref.sync import async_to_sync
from chat.utils import subscribe_to_room
from rest_framework import serializers
from users.models import User, UserChannel

from .models import Message, Room


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = "__all__"
        read_only_fields = ["id", "updated_at", "created_at", "owner"]
        depth = 2

    def create(self, validated_data):
        owner = self.context["request"].user
        validated_data["owner"] = owner
        room = super().create(validated_data)
        # add owner to the room
        room.users.add(owner)
        subscribe_to_room(room=room, user=owner)
        return room

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class JoinRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["users"]

    def update(self, instance: Room, validated_data):
        users = validated_data["users"]
        room = instance
        for user in users:
            room.users.add(user)
            subscribe_to_room(room=room, user=user)

        return instance


class AddUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)

    def validate(self, data):
        username = data.get("username")
        if username:
            user = User.objects.filter(username=username).first()
            if user is None:
                raise serializers.ValidationError({"username": ["Username not found."]})
        else:
            raise serializers.ValidationError(
                {"non_field_errors": ["Must include username."]}
            )

        data["user"] = user
        return data


class JoinPrivateRoomSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)

    def validate(self, data):
        user_id = data.get("user_id")
        to_user = User.objects.get(id=user_id)
        data["to_user"] = to_user
        return data


class LeaveRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ["users"]

    def update(self, instance: Room, validated_data):
        users = validated_data["users"]
        room = instance
        for user in users:
            room.users.remove(user)
        return instance


class MessageSerializer(serializers.ModelSerializer):
    room_id = serializers.IntegerField()

    class Meta:
        model = Message
        fields = "__all__"
        read_only_fields = ["id", "updated_at", "created_at", "owner"]
        depth = 2

    def create(self, validated_data):
        room_id = validated_data["room_id"]
        room = Room.objects.get(id=room_id)
        validated_data["room"] = room
        owner = self.context["request"].user
        validated_data["owner"] = owner
        return super().create(validated_data)
