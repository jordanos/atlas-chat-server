import json

import pytest
from django.urls import reverse
from users.models import User
from users.tests.utils import verify_user_api_response


@pytest.mark.django_db
def test_user1(db, user1):
    """
    Check if user1 exists and password is hashed
    """
    users = User.objects.filter(username="user1")
    assert users.exists()
    user1 = users.first()
    # test if password is hashed
    assert user1.password != "123456"


@pytest.mark.django_db
def test_get_users(user1, client):
    """
    Check users count to be 1 and existing username to be user1
    """
    url = reverse(viewname="user-list-create")
    res = client.get(url)
    assert res.status_code == 200
    # check structure of res
    assert "page_metadata" in res.data
    assert "results" in res.data
    page_metadata = res.data["page_metadata"]
    results = res.data["results"]
    # check user count = 1
    assert page_metadata["count"] == 1
    # check result length is 1, user dict data and contains username = user1
    assert isinstance(results, list)
    assert len(results) == 1
    user = results[0]
    assert verify_user_api_response(user)
    assert user["username"] == "user1"


@pytest.mark.parametrize(
    "data, status_code",
    [({"username": "abel"}, 400), ({"username": "abel", "password": "123456"}, 201)],
)
@pytest.mark.django_db
def test_create_user(db, client, data, status_code):
    """
    Check creating a user with various payloads
    """
    url = reverse(viewname="user-list-create")
    res = client.post(url, data=data)
    assert res.status_code == status_code
    # check user exists in db
    if status_code == 201:
        assert User.objects.filter(username=data["username"]).exists()


@pytest.mark.django_db
def test_user_detail(client, user1, token):
    """
    Check getting user detail and authentication
    """
    url = reverse(viewname="user-detail", args=[1])
    res = client.get(url)
    # token must be supplied
    assert res.status_code == 401
    # send request with token in header
    res = client.get(url, headers={"Authorization": f"Token {token}"})
    assert res.status_code == 200
    # verify data
    user = res.data
    assert verify_user_api_response(user)
    # check username
    assert user["username"] == "user1"


@pytest.mark.django_db
def test_update_user(client, user1, token):
    """
    Update user detail and check updated data
    """
    new_username = "john"
    payload = {"username": new_username}
    url = reverse(viewname="user-detail", args=[1])
    res = client.patch(url, data=payload)
    # token must be supplied
    assert res.status_code == 401
    # send request with token in header
    res = client.patch(
        url,
        data=json.dumps(payload),
        headers={"Authorization": f"Token {token}", "Content-Type": "application/json"},
    )
    assert res.status_code == 200
    assert res.data["username"] == new_username
    # send get user detail request and validate username
    res = client.get(url, headers={"Authorization": f"Token {token}"})
    assert res.data["username"] == new_username
