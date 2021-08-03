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

RTOL = 1e-3

@pytest.fixture(scope="class")
def recipe_query():
    sess = dal.Session()
    return sess.query(Recipe).all()


class TestRecipeQueries:
    def test_simple(self, recipe):
        for row in recipe:
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
            assert isclose(r.maximum_temperature,fact[r.id].maximum_temperature, rel_tol=RTOL)

      
    def test_prop__maximum_pressure(self, recipe):
        """Test maximum_pressure hybrid property and expression behavior.

        Check basic functionality of attribute and its SQL expression

        Args:
            recipe [Recipe]: List of Recipes from factory engine
        """
        # From hybrid attribute of factory session
        print("\nFactory:")
        fact = {}
        for r in recipe:
            print(f"id: {r.id}, max press: {r.maximum_pressure}")
            fact[r.id] = r
        # Test query expression behavior
        sess = dal.Session()
        print("Query")
        for r in sess.query(Recipe.id, Recipe.maximum_pressure).filter(
            Recipe.id.in_([r.id for r in recipe])
        ):
            print(f"id: {r.id}, max press: {r.maximum_pressure}")
            assert isclose(r.maximum_pressure,fact[r.id].maximum_pressure, rel_tol=RTOL)


    def test_prop__average_carbon_flow_rate(self, recipe):
        """Test average_carbon_flow_rate hybrid property and expression behavior.

        Check basic functionality of attribute and its SQL expression

        Args:
            recipe [Recipe]: List of Recipes from factory engine
        """
        # From hybrid attribute of factory session
        print("\nFactory:")
        fact = {}
        for r in recipe:
            print(f"id: {r.id}, value: {r.average_carbon_flow_rate}")
            fact[r.id] = r
        # Test query expression behavior
        sess = dal.Session()
        print("Query")
        for r in sess.query(Recipe.id, Recipe.average_carbon_flow_rate).filter(
            Recipe.id.in_([r.id for r in recipe])
        ):
            print(f"id: {r.id}, value: {r.average_carbon_flow_rate}")
            assert isclose(r.average_carbon_flow_rate,fact[r.id].average_carbon_flow_rate, rel_tol=RTOL)

    
    def test_prop__carbon_source(self, recipe):
        """Test carbon_source hybrid property and expression behavior.

        Check basic functionality of attribute and its SQL expression

        Args:
            recipe [Recipe]: List of Recipes from factory engine
        """
        # From hybrid attribute of factory session
        print("\nFactory:")
        fact = {}
        for r in recipe:
            print(f"id: {r.id}, value: {r.carbon_source}")
            fact[r.id] = r
        # Test query expression behavior
        sess = dal.Session()
        print("Query")
        for r in sess.query(Recipe.id, Recipe.carbon_source).filter(
            Recipe.id.in_([r.id for r in recipe])
        ):
            print(f"id: {r.id}, value: {r.carbon_source}")
            assert(fact[r.id].carbon_source == r.carbon_source)

    def test_prop__uses_helium(self, recipe):
        """Test uses_helium hybrid property and expression behavior.

        Check basic functionality of attribute and its SQL expression

        Args:
            recipe [Recipe]: List of Recipes from factory engine
        """
        # From hybrid attribute of factory session
        print("\nFactory:")
        fact = {}
        for r in recipe:
            print(f"id: {r.id}, value: {r.uses_helium}")
            fact[r.id] = r
        # Test query expression behavior
        sess = dal.Session()
        print("Query")
        for r in sess.query(Recipe.id, Recipe.uses_helium).filter(
            Recipe.id.in_([r.id for r in recipe])
        ):
            print(f"id: {r.id}, value: {r.uses_helium}")
            assert(fact[r.id].uses_helium == r.uses_helium)

    def test_prop__uses_argon(self, recipe):
        """Test uses_argon hybrid property and expression behavior.

        Check basic functionality of attribute and its SQL expression

        Args:
            recipe [Recipe]: List of Recipes from factory engine
        """
        # From hybrid attribute of factory session
        print("\nFactory:")
        fact = {}
        for r in recipe:
            print(f"id: {r.id}, value: {r.uses_argon}")
            fact[r.id] = r
        # Test query expression behavior
        sess = dal.Session()
        print("Query")
        for r in sess.query(Recipe.id, Recipe.uses_argon).filter(
            Recipe.id.in_([r.id for r in recipe])
        ):
            print(f"id: {r.id}, value: {r.uses_argon}")
            assert(fact[r.id].uses_argon == r.uses_argon)

    def test_prop__uses_hydrogen(self, recipe):
        """Test uses_hydrogen hybrid property and expression behavior.

        Check basic functionality of attribute and its SQL expression

        Args:
            recipe [Recipe]: List of Recipes from factory engine
        """
        # From hybrid attribute of factory session
        print("\nFactory:")
        fact = {}
        for r in recipe:
            print(f"id: {r.id}, value: {r.uses_hydrogen}")
            fact[r.id] = r
        # Test query expression behavior
        sess = dal.Session()
        print("Query")
        for r in sess.query(Recipe.id, Recipe.uses_hydrogen).filter(
            Recipe.id.in_([r.id for r in recipe])
        ):
            print(f"id: {r.id}, value: {r.uses_hydrogen}")
            assert(fact[r.id].uses_hydrogen == r.uses_hydrogen)


    #def test__json_encodable(self, recipe):
    #    assert False
