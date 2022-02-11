import factory

from grdb.database.models import Furnace
from .common import test_db

LIST_SIZES = [1, 2, 3]


class FurnaceFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Furnace
        sqlalchemy_session = test_db.Session
        sqlalchemy_session_persistence = "flush"

    tube_diameter = factory.Faker('pyfloat', positive=False, min_value=-100, max_value=100)
    cross_sectional_area = factory.Faker('pyfloat', positive=False, min_value=-100, max_value=100)
    tube_length = factory.Faker('pyfloat', positive=False, min_value=-100, max_value=100)
    length_of_heated_region = factory.Faker('pyfloat', positive=False, min_value=-100, max_value=100)
