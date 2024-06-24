import factory
from django.contrib.auth.hashers import make_password
from faker import Faker
from users.models import User

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    id = 1
    username = fake.name()
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    first_name = fake.name()
    last_name = fake.name()
    password = factory.LazyFunction(lambda: make_password("123456"))
