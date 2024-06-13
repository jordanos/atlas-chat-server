import pytest
from django.urls import reverse
from users.models import User


@pytest.mark.django_db
def test_user_create():
    User.objects.create(
        username="john",
        email="lennon@thebeatles.com",
        password="johnpassword",
    )
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_users_get(client):
    User.objects.create(
        username="john",
        email="lennon@thebeatles.com",
        password="johnpassword",
    )
    url = reverse(viewname="user-list-create")
    response = client.get(url)
    assert "page_metadata" in response.data
    assert "results" in response.data
