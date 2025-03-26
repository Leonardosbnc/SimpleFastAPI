import factory

from api import models


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.User
        sqlalchemy_session_persistence = "commit"

    email = factory.Faker("email")
    username = factory.Faker("first_name")
    password = factory.Faker("password")
    is_admin = False
