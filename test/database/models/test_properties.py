import pytest
from math import isclose

from gresq.database import dal, Base
from gresq.database.models import Properties
from test.database.factories import PropertiesFactory

RTOL = 1e-3

@pytest.fixture(scope="class")
def properties_query():
    sess = dal.Session()
    return sess.query(Properties).all()


class TestPropertiesQueries:
    def test_simple(self, properties):
        sesh = dal.Session()
        qall = sesh.query(Properties).all()
        for row in qall:
            print(f"id: {row.id}")
            print(f"layers: {row.number_of_layers}")
        sesh.close()