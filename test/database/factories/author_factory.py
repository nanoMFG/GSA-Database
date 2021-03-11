import factory

from gresq.database.models import Author
from gresq.database.dal import dal

LIST_SIZES = [1, 2, 3]


class AuthorFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Author
        sqlalchemy_session = dal.Session()
        sqlalchemy_session_persistence = "commit"

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    institution = "University of Illinois"
    nanohub_userid = factory.Faker('user_name')