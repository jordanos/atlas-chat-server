import pytest
from django.urls import reverse


@pytest.mark.parametrize(
    "data, status_code",
    [({"text": "helloooo"}, 400), ({"text": "hello", "room_id": 1}, 201)],
)
@pytest.mark.django_db
def test_create_message(db, client, user1, token, room_factory, data, status_code):
    """
    Check creating a message and validate response
    """
    room_factory.create(
        id=1, name="room_pvt", type="private", owner=user1, users=[user1]
    )
    url = reverse("message-list-create")
    res = client.post(
        url,
        data=data,
        headers={"Authorization": f"Token {token}"},
    )
    assert res.status_code == status_code
    # if creation successful verify returned a data
    if status_code == 201:
        message = res.data
        assert message["text"] == data["text"]
        assert message["room"]["id"] == data["room_id"]
        assert message["owner"]["username"] == user1.username
