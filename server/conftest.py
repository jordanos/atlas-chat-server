import pytest
from pytest_factoryboy import register
from rest_framework.authtoken.models import Token
from users.tests.factories import UserFactory

register(UserFactory)


@pytest.fixture
def user1(user_factory):
    # Create user with username=user1
    user1 = user_factory.create(username="user1")
    # To use custom password, use the password kwarg and makepassword function from django
    # user1 = user_factory.create(username="user1", make_password("custom_pass"))
    return user1


@pytest.fixture
def token(db, user1):
    # Create token for user1
    token, created = Token.objects.get_or_create(user=user1)
    return token.key
