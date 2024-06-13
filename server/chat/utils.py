import channels.layers
from asgiref.sync import async_to_sync
from chat.models import Room
from users.models import User, UserChannel


def subscribe_to_room(room: Room, user: User) -> None:
    """
    Lets the channel of users websocket subscribe to room
    """
    # ws subscribe to room channel
    # add current user channel to group
    try:
        channel = UserChannel.objects.get(owner=user)
        if channel.is_active:
            channel_layer = channels.layers.get_channel_layer()
            async_to_sync(channel_layer.group_add)(
                f"room_{room.id}",
                channel.channel_name,
            )
    except UserChannel.DoesNotExist:
        pass
