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
from gresq.database.models import EnvironmentConditions
from test.database.factories import EnvironmentConditionsFactory

RTOL = 1e-3

@pytest.fixture(scope="class")
def environment_conditions_query():
    sess = dal.Session()
    return sess.query(EnvironmentConditions).all()


class TestEnvironmentConditionsQueries:
    def test_simple(self, environment_conditions):
        for row in environment_conditions:
            print(f"id: {row.ambient_temperature}")