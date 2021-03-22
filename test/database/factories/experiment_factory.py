import factory
import datetime

from gresq.database.models import Experiment
from gresq.database.dal import dal

LIST_SIZES = [1, 2, 3]


class ExperimentFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Experiment
        sqlalchemy_session = dal.Session()
        sqlalchemy_session_persistence = "commit"

    recipe_id = factory.Faker('pyint')
    environment_conditions_id = factory.Faker('pyint')
    substrate_id = factory.Faker('pyint')
    furnace_id = factory.Faker('pyint')
    primary_sem_file_id = factory.Faker('pyint')
    # The user/author that submitted this experiment
    submitted_by = factory.Faker('pyint')
    # The date the experiment was conducted
    experiment_date = factory.Faker('date_between_dates',
        date_start=datetime.date(2020, 1, 1),
        date_end=datetime.date(2020, 5, 31),
    )
    # The material grown
    material_name = 'Graphene'
    # Status of experiment valdation
    validated = False
    # The authors that conducted the experiment
    # authors = factory.SubFactory(
    #     "test.database.factories.AuthorFactory"
    # )
    properties = factory.SubFactory(
        "test.database.factories.PropertiesFactory", experiments=[]
    )
    # # MANY-TO-ONE: experiments->recipe
    recipe = factory.SubFactory(
        "test.database.factories.RecipeFactory", experiments=[]
    )

    # # MANY-TO-ONE: experiments->environment_conditions
    environment_conditions  = factory.SubFactory(
        "test.database.factories.EnvironmentConditionsFactory", experiments=[]
    )

    # # MANY-TO-ONE: experiments->substrate
    substrate  = factory.SubFactory(
        "test.database.factories.SubstrateFactory", experiments=[]
    )

    # # MANY-TO-ONE: experiments->furnace
    furnace  = factory.SubFactory(
        "test.database.factories.FurnaceFactory", experiments=[]
    )

    # # ONE-TO-MANY: experiment -> raman_files
    raman_files = factory.RelatedFactoryList(
        "test.database.factories.RamanFileFactory", "experiment", size=3
    )

    # # ONE-TO-MANY: experiment -> sem_files
    sem_files = factory.RelatedFactoryList(
        "test.database.factories.SemFileFactory", "experiment", size=3
    )
    primary_sem_file = factory.RelatedFactory(
        "test.database.factories.SemFileFactory", "experiment"
    )
   