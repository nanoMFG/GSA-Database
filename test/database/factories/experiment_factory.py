import factory
import datetime

from grdb.database.models import Experiment
from .common import test_db, dbSpec
from . import AuthorFactory

LIST_SIZES = [1, 2, 3]


class ExperimentFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Experiment
        sqlalchemy_session = test_db.Session
        sqlalchemy_session_persistence = "commit"

    #recipe_id = factory.LazyAttribute(lambda obj: obj.recipe.id)
    environment_conditions_id = factory.Faker('pyint')
    #substrate_id = factory.Faker('pyint')
    #furnace_id = factory.Faker('pyint')
    primary_sem_file_id = None
    # The user/author that submitted this experiment
    #submitted_by = factory.LazyAttribute(lambda obj: AuthorFactory().id)
    # The date the experiment was conducted
    #primary_sem_file_id = factory.LazyAttribute(lambda obj: obj.sem_files[0].id)
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
    properties = factory.RelatedFactoryList(
        "test.database.factories.PropertiesFactory", "experiment", size=1
    )
    # # MANY-TO-ONE: experiments->recipe
    # recipe = factory.SubFactory(
    #     "test.database.factories.RecipeFactory", experiments=[]
    # )

    # # MANY-TO-ONE: experiments->environment_conditions
    environment_conditions = factory.SubFactory(
        "test.database.factories.EnvironmentConditionsFactory", experiments=[]
    )

    # # MANY-TO-ONE: experiments->substrate
    substrate = factory.SubFactory(
        "test.database.factories.SubstrateFactory", experiments=[]
    )

    # # # MANY-TO-ONE: experiments->furnace
    # furnace = factory.SubFactory(
    #     "test.database.factories.FurnaceFactory", experiments=[]
    # )
    sem_files = factory.RelatedFactoryList(
        "test.database.factories.SemFileFactory", "experiment", size=3
    )
    # # ONE-TO-MANY: experiment -> raman_files
    raman_files = factory.RelatedFactoryList(
        "test.database.factories.RamanFileFactory", "experiment", size=3
    )

    @factory.post_generation
    def authors(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of authors were passed in, use them
            self.submitted_by = extracted[0].id
            for author in extracted:
                self.authors.append(author)

    @factory.post_generation
    def recipe(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            for recipe in extracted:
                self.recipe_id = recipe.id

    @factory.post_generation
    def furnace(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            for furnace in extracted:
                self.furnace_id = furnace.id

    @factory.post_generation
    def substrate(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            for substrate in extracted:
                self.substrate_id = substrate.id
