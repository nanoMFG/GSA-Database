""" Tests for the Recipe model

Test relationships, properties and delete cascade behavior.  Testing at the model level
is intended to provide basic sanity checks, NOT to rewrite every bit of model logic and
 test it.

Application level testing should be developed to test expected behavior of application
logic when interacting with the database.

Conventions:

  test naming:
    test_rel__arelationship: 
    test_prop__aproperty:
    

"""
import pytest
from math import isclose

from gresq.database import dal, Base
from gresq.database.models import Recipe
from test.database.factories import RecipeFactory, PreparationStepFactory


@pytest.fixture(scope="class")
def recipe_query():
    sess = dal.Session()
    return sess.query(Recipe).all()


class TestRecipeQueries:
    def test_simple(self, recipe):
        sesh = dal.Session()
        qall = sesh.query(Recipe).all()
        for row in qall:
            print(f"id: {row.id}")
            for step in row.preparation_steps:
                print(f"step: {step.name}")

    # def test_rel__preparation_steps(self, sample, all_sample_query):
    #     pass

    def test_prop__maximum_temperature(self, recipe):
        """Test maximum_temperature hybrid property and expression behavior.

        Check basic functionality of attribute and its SQL expression

        Args:
            recipe [Recipe]: List of Recipes from factory engine
        """
        # From hybrid attribute of factory session
        print("\nFactory:")
        fact = {}
        for r in recipe:
            print(f"id: {r.id}, max temp: {r.maximum_temperature}")
            fact[r.id] = r
        # Test query expression behavior
        sess = dal.Session()
        print("Query")
        for r in sess.query(Recipe.id, Recipe.maximum_temperature).filter(
            Recipe.id.in_([r.id for r in recipe])
        ):
            print(f"id: {r.id}, max temp: {r.maximum_temperature}")
            assert isclose(r.maximum_temperature,fact[r.id].maximum_temperature)

      
    def test_prop__maximum_pressure(self, recipe):
        assert False

    def test_prop__average_carbon_flow_rate(self, recipe):
        assert False
    
    def test_prop__carbon_source(self, recipe):
        assert False

    def test_prop__uses_helium(self, recipe):
        assert False

    def test_prop__uses_argon(self, recipe):
        assert False

    def test_prop__uses_hydrogen(self, recipe):
        assert False

    def test__json_encodable(self, recipe):
        assert False
