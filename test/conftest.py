"""Configuration module for pytest testing

Includes common test fixtures used for testing of database models.
   
"""
import pytest

from gresq.database import dal, Base
from gresq.database.models import Recipe
from test.database.factories import RecipeFactory, PreparationStepFactory, AuthorFactory, PropertiesFactory, FurnaceFactory, EnvironmentConditionsFactory, ExperimentFactory

#Make an option

def pytest_addoption(parser):
    """pytest command line option definition for "--persistdb"

    Args:
        parser
    """
    parser.addoption(
        "--persistdb",
        action="store",
        default="commit",
        help="persistdb: session behavior for test factories: none, commit or flush",
    )
    parser.addoption(
        "--dropdb",
        action="store",
        default=True,
        help="dropdb: Teardown database when finished: True, False",
    )

@pytest.fixture(scope="module")
def persistdb(request):
    """fixture for adding the result of the "--persistdb" commandline option to a test when running pytest.

    Args:
        request

    Returns:
        Result of getoption.
    """
    return request.config.getoption("--persistdb")

@pytest.fixture(scope="module")
def dropdb(request):
    """fixture for adding the result of the "--dropdb" commandline option to a test
    when running pytest.

    Args:
        request

    Returns:
        Result of getoption.
    """
    opt = request.config.getoption("--dropdb")
    ret = True
    if opt:
        if opt=="False":
            ret = False
    else:
        ret = False
    return ret

#Call is testdb fixture
@pytest.fixture(scope="class")
def recipe(persistdb, dropdb):
    """Set up a set of recipes for testing using the factory boy factories.

    Yield the generates recipes and teardown afterwords.
    The ("--persistdb") option controls whether the test data are committed to the live
    test database.

    "-- persist commit" will commit test data to the session and leave the data in place.
    subsequent "--persist None" will scrub all test data.

    """
    # create_all is already in test/database__init__.py.
    #  I don't know why I have to call it here again, but I do.
    #Base.metadata.drop_all(bind=dal.engine)
    Base.metadata.create_all(bind=dal.engine)
    print("Hey, here come some recipes...")
    # Set persistance for test data
    ExperimentFactory._meta.sqlalchemy_session_persistence = persistdb
    experiments = ExperimentFactory.create_batch(10)
    RecipeFactory._meta.sqlalchemy_session_persistence = persistdb
    PreparationStepFactory._meta.sqlalchemy_session_persistence = persistdb
    # Add a batch of recipes
    recipes = RecipeFactory.create_batch(5)
    yield recipes
    # Drop all tables
    if dropdb:
        sess = dal.Session()
        sess.close()
        Base.metadata.drop_all(bind=dal.engine)


@pytest.fixture(scope="class")
def author(persistdb, dropdb):
    AuthorFactory._meta.sqlalchemy_session_persistence = persistdb
    authors = AuthorFactory.create_batch(10)
    yield authors
    if dropdb:
        sess = dal.Session()
        sess.close()
        Base.metadata.drop_all(bind=dal.engine)

# @pytest.fixture(scope="class")
# def experiment(persistdb, dropdb):
#     Base.metadata.drop_all(bind=dal.engine)
#     Base.metadata.create_all(bind=dal.engine)
#     ExperimentFactory._meta.sqlalchemy_session_persistence = persistdb
#     EnvironmentConditionsFactory._meta.sqlalchemy_session_persistence = persistdb
#     experiments = ExperimentFactory.create_batch(10)
#     yield experiments
#     if dropdb:
#         sess = dal.Session()
#         sess.close()
#         Base.metadata.drop_all(bind=dal.engine)

@pytest.fixture(scope="class")
def furnace(persistdb, dropdb):
    Base.metadata.create_all(bind=dal.engine)
    ExperimentFactory._meta.sqlalchemy_session_persistence = persistdb
    EnvironmentConditionsFactory._meta.sqlalchemy_session_persistence = persistdb
    experiments = ExperimentFactory.create_batch(10)
    FurnaceFactory._meta.sqlalchemy_session_persistence = persistdb
    furnaces = FurnaceFactory.create_batch(5)
    yield furnaces
    if dropdb:
        sess = dal.Session()
        sess.close()
        Base.metadata.drop_all(bind=dal.engine)

@pytest.fixture(scope="class")
def properties(persistdb, dropdb):
    # RecipeFactory._meta.sqlalchemy_session_persistence = persistdb
    # PreparationStepFactory._meta.sqlalchemy_session_persistence = persistdb
    # recipes = RecipeFactory.create_batch(5)
    # ExperimentFactory._meta.sqlalchemy_session_persistence = persistdb
    # experiments = ExperimentFactory.create_batch(10)
    PropertiesFactory._meta.sqlalchemy_session_persistence = persistdb
    properties = PropertiesFactory.create()
    yield properties
    if dropdb:
        sess = dal.Session()
        sess.close()
        Base.metadata.drop_all(bind=dal.engine)
