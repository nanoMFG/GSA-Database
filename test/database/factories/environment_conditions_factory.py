import factory

from grdb.database.models import EnvironmentConditions
from .common import test_db

LIST_SIZES = [1, 2, 3]


class EnvironmentConditionsFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = EnvironmentConditions
        sqlalchemy_session = test_db.Session
        sqlalchemy_session_persistence = "flush"

    dew_point = factory.Faker('pyfloat', positive=False, min_value=-100, max_value=100)
    ambient_temperature = factory.Faker('pyfloat', positive=False, min_value=-100, max_value=100)