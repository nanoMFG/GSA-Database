import factory

from grdb.database.models import Software
from .common import test_db


class SoftwareFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Software
        sqlalchemy_session = test_db.Session
        sqlalchemy_session_persistence = "flush"

    # sample = factory.SubFactory("test.database.factories.SampleFactory", authors=None)
    # raman_set = factory.SubFactory("test.database.factories.RamanSetFactory", setauthors=None)
    name = "fake_sw"
    version = "1.1.0"
    release_date = factory.Faker('date_object')
    branch = 'master'
    commitsh = factory.Faker("sha1")
    url = factory.Faker("url")
