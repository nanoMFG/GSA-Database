"""UNCOMMECT TO TEST v.1_1_0
import pytest
from math import isclose

from grdb.database.v1_1_0 import dal, Base
from grdb.database.v1_1_0.models_v_1_1_0 import Properties
from test.database.factories import PropertiesFactory

RTOL = 1e-3

@pytest.fixture(scope="class")
def properties_query():
    sess = dal.Session()
    return sess.query(Properties).all()

class TestPropertiesQueries:
    def test_simple(self, properties):
        for row in properties:
            print(f"id: {row.id}")
            print(f"layers: {row.number_of_layers}")
"""