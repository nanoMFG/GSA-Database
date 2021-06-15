import factory

from gresq.database.models import EnvironmentConditions
from gresq.database.dal import dal

LIST_SIZES = [1, 2, 3]


class EnvironmentConditionsFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = EnvironmentConditions
        sqlalchemy_session = dal.Session()
        sqlalchemy_session_persistence = "commit"

    experiments = factory.RelatedFactoryList(
        "test.database.factories.ExperimentFactory", "experiment", size=3
    )
    dew_point = factory.Faker('pyfloat', positive=False, min_value=-100, max_value=100)
    ambient_temperature = factory.Faker('pyfloat', positive=False, min_value=-100, max_value=100)