import factory
import random

from gresq.database.models import Recipe
from gresq.database.dal import dal

LIST_SIZES = [1, 2, 3, 4, 5, 6]


class RecipeFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Recipe
        sqlalchemy_session = dal.Session()
        sqlalchemy_session_persistence = None

    preparation_steps = factory.RelatedFactoryList(
        "test.database.factories.PreparationStepFactory", "recipe", size=3
    )
