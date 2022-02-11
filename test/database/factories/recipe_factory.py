import factory

from grdb.database.models import Recipe
from .common import test_db

LIST_SIZES = [1, 2, 3, 4, 5, 6]


class RecipeFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Recipe
        sqlalchemy_session = test_db.Session
        sqlalchemy_session_persistence = "flush"

    carbon_source = factory.Iterator(Recipe.carbon_source.info["choices"])

    base_pressure = factory.Faker(
        "pyfloat", positive=True, min_value=80.0, max_value=100.0
    )

    # preparation_steps = factory.RelatedFactoryList(
    #     'database.factories.PreparationStepFactory', 'recipe_id', size=3
    # )
