import factory

from gresq.database.models import Furnace
from gresq.database.dal import dal

LIST_SIZES = [1, 2, 3]


class FurnaceFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Furnace
        sqlalchemy_session = dal.Session()
        sqlalchemy_session_persistence = "commit"

    experiments = factory.SubFactory(
        "test.database.factories.ExperimentFactory", furnace=None
    )
    tube_diameter = factory.Faker('pyfloat', positive=False, min_value=-100, max_value=100)
    cross_sectional_area = factory.Faker('pyfloat', positive=False, min_value=-100, max_value=100)
    tube_length = factory.Faker('pyfloat', positive=False, min_value=-100, max_value=100)
    length_of_heated_region = factory.Faker('pyfloat', positive=False, min_value=-100, max_value=100)