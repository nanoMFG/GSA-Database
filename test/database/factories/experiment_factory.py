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
    authors = None
    
    furnace_id = 5
    properties = factory.RelatedFactory(
        "test.database.factories.PropertiesFactory", "experiment"
    )
    # # MANY-TO-ONE: experiments->recipe
    # recipe = None

    # # MANY-TO-ONE: experiments->environment_conditions
    # environment_conditions = None

    # # MANY-TO-ONE: experiments->substrate
    # substrate = None

    # # MANY-TO-ONE: experiments->furnace
    # furnace = None

    # # ONE-TO-MANY: experiment -> raman_files
    # raman_files = None

    # # ONE-TO-MANY: experiment -> sem_files
    # sem_files = None

    # primary_sem_file = None
   