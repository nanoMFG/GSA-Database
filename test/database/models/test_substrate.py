import pytest
from math import isclose

from grdb.database.v1_1_0 import dal, Base
from grdb.database.v1_1_0.models import Substrate
from test.database.factories import SubstrateFactory

RTOL = 1e-3

@pytest.fixture(scope="class")
def substrate_query():
    sess = dal.Session()
    return sess.query(Substrate).all()


class TestSoftwareQueries:
    def test_simple(self, substrate):
        for row in substrate:
            print(f"id: {row.id}")