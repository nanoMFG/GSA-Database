import factory

from grdb.database.models import Author
from .common import test_db

LIST_SIZES = [1, 2, 3]


class AuthorFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Author
        sqlalchemy_session = test_db.Session
        sqlalchemy_session_persistence = "flush"

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    institution = "University of Illinois"
    nanohub_userid = factory.Faker('pyint')