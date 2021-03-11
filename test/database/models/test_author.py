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
from gresq.database.models import Author
from test.database.factories import AuthorFactory

RTOL = 1e-3

@pytest.fixture(scope="class")
def author_query():
    sess = dal.Session()
    return sess.query(Author).all()


class TestAuthorQueries:
    def test_simple(self, author):
        sesh = dal.Session()
        qall = sesh.query(Author).all()
        for row in qall:
            print(f"id: {row.id}")
            for author in row.author:
                print(f"step: {author.institution}")