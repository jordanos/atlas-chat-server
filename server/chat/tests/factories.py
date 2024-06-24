import factory
from chat.models import Message, Room
from faker import Faker
from users.tests.factories import UserFactory

fake = Faker()


class RoomFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Room

    name = fake.unique.name()
    type = "private"
    owner = factory.SubFactory(UserFactory)

    @factory.post_generation
    def users(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for author in extracted:
                self.users.add(author)


class MessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Message

    text = fake.text()
    owner = factory.SubFactory(UserFactory)
    room = factory.SubFactory(RoomFactory)
