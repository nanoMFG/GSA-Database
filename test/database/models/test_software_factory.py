import pytest
from math import isclose

from grdb.database.v1_1_0 import dal, Base
from grdb.database.v1_1_0.models import Software
from test.database.factories import SoftwareFactory

RTOL = 1e-3

@pytest.fixture(scope="class")
def software_query():
    sess = dal.Session()
    return sess.query(Software).all()


class TestSoftwareQueries:
    def test_simple(self, software):
        for row in software:
            print(f"id: {row.id}")