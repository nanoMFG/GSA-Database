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

from grdb.database.v1_1_0 import dal, Base
from grdb.database.v1_1_0.models import Author
from test.database.factories import AuthorFactory

RTOL = 1e-3

@pytest.fixture(scope="class")
def author_query():
    sess = dal.Session()
    return sess.query(Author).all()


class TestAuthorQueries:
    def test_simple(self, author):
        for row in author:
            print(f"nanahub user id: {row.nanohub_userid}")
