import pytest
from django.urls import reverse


@pytest.mark.parametrize(
    "data, status_code",
    [({"type": "priv"}, 400), ({"name": "room1", "type": "private"}, 201)],
)
@pytest.mark.django_db
def test_create_room(db, client, user1, token, data, status_code):
    """
    Check creating a room and validate response
    """
    url = reverse("room-list-create")
    res = client.post(
        url,
        data=data,
        headers={"Authorization": f"Token {token}"},
    )
    assert res.status_code == status_code
    # if creation successful verify returned a data
    if status_code == 201:
        room = res.data
        assert room["name"] == data["name"]
        assert room["type"] == data["type"]
        assert room["owner"]["username"] == user1.username
