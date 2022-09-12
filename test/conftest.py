"""Configuration module for pytest testing

Includes common test fixtures used for testing of database models_v_1_1_0.
   
"""
import pytest
"""UNCOMMECT TO TEST v.1_1_0
# from grdb.database.v1_1_0 import dal, Base
# from grdb.database.v1_1_0.models_v_1_1_0 import Recipe
# from test.database.factories import RecipeFactory, PreparationStepFactory, AuthorFactory, PropertiesFactory, FurnaceFactory, EnvironmentConditionsFactory, ExperimentFactory, SoftwareFactory, SubstrateFactory
"""
from grdb.database import dal, Base
from grdb.database.models import Recipe
from test.database.factories.common import dbSpec
from test.database.factories import RecipeFactory, PreparationStepFactory, AuthorFactory, PropertiesFactory, FurnaceFactory, EnvironmentConditionsFactory, ExperimentFactory, SoftwareFactory, SubstrateFactory

from grdb.server.app import create_app


# Make an option

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


@pytest.fixture(scope="session")
def persistdb(request):
    """fixture for adding the result of the "--persistdb" commandline option to a test when running pytest.

    Args:
        request

    Returns:
        Result of getoption.
    """
    return request.config.getoption("--persistdb")


@pytest.fixture(scope="session")
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
        if opt == "False":
            ret = False
    else:
        ret = False
    return ret
# dbSpec = {
#     "nSubstrates": 4,
#     "nAuthors": 12,
#     "nRecipes": 8,
#     "nExperiments": 10,
#     "listAuthorsPerExperiment": [1, 2, 1, 5, 1, 1, 3, 1, 1, 12],
#     "listRecipesPerExperiment": [1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
# }

# Call is testdb fixture
@pytest.fixture(scope="session")
def grdb(persistdb, dropdb):
    """Set up a set of recipes for testing using the factory boy factories.

    Yield the generates recipes and teardown afterwords.
    The ("--persistdb") option controls whether the test data are committed to the live
    test database.

    "-- persist commit" will commit test data to the session and leave the data in place.
    subsequent "--persist None" will scrub all test data.

    """
    # create_all is already in test/database__init__.py.
    #  I don't know why I have to call it here again, but I do.
    # Base.metadata.drop_all(bind=dal.engine)
    Base.metadata.create_all(bind=dal.engine)
    SubstrateFactory._meta.sqlalchemy_session_persistence = persistdb
    AuthorFactory._meta.sqlalchemy_session_persistence = persistdb
    RecipeFactory._meta.sqlalchemy_session_persistence = persistdb
    ExperimentFactory._meta.sqlalchemy_session_persistence = persistdb

    print("\n\nHere come some experiments!!\n")

    print("Creating substrates...")
    substrates = SubstrateFactory.create_batch(dbSpec["nSubstrates"])
    print("Creating authors...")
    authors = AuthorFactory.create_batch(dbSpec["nAuthors"])
    print("Creating recipes...")
    recipes = RecipeFactory.create_batch(dbSpec["nRecipes"])
    print("Creating furnaces...")
    furnaces = FurnaceFactory.create_batch(dbSpec["nFurnaces"])

    print("Creating experiments...")
    for n in range(dbSpec["nExperiments"]):
        recipeIdx = n%dbSpec['nRecipes']
        substrateIdx = n%dbSpec['nSubstrates']
        furnaceIdx = dbSpec["listFurnacesPerExperiment"][n] - 1
        #print(f"{n+1} Recipe num: {recipes[recipeIdx].id} Furnace num: {furnaces[furnaceIdx].id}")
        experiments = ExperimentFactory.create(
            authors=authors[:dbSpec["listAuthorsPerExperiment"][n]],
            recipe=[recipes[recipeIdx]],
            furnace=[furnaces[furnaceIdx]],
            substrate=[substrates[substrateIdx]],
            )
    sess = dal.Session()
    sess.commit()
    yield
    # Drop all tables
    if dropdb:
        print("Dropping tables")
        sess = dal.Session()
        sess.close()
        Base.metadata.drop_all(bind=dal.engine)

@pytest.fixture(scope="function")
def session():
    """Create a session for testing.

    Yield the session and teardown afterwords.
    """
    sess = dal.Session()
    yield sess
    print("Closing session")
    sess.rollback()
    dal.Session.remove()
    #sess.close()

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

# @pytest.fixture(scope="class")
# def furnace(persistdb, dropdb):
#     Base.metadata.create_all(bind=dal.engine)
#     ExperimentFactory._meta.sqlalchemy_session_persistence = persistdb
#     EnvironmentConditionsFactory._meta.sqlalchemy_session_persistence = persistdb
#     experiments = ExperimentFactory.create_batch(10)
#     FurnaceFactory._meta.sqlalchemy_session_persistence = persistdb
#     furnaces = FurnaceFactory.create_batch(5)
#     yield furnaces
#     if dropdb:
#         sess = dal.Session()
#         sess.close()
#         Base.metadata.drop_all(bind=dal.engine)

# @pytest.fixture(scope="class")
# def properties(persistdb, dropdb):
#     PropertiesFactory._meta.sqlalchemy_session_persistence = persistdb
#     properties = PropertiesFactory.create_batch(10)
#     yield properties
#     if dropdb:
#         sess = dal.Session()
#         sess.close()
#         Base.metadata.drop_all(bind=dal.engine)


# @pytest.fixture(scope="class")
# def environment_conditions(persistdb, dropdb):
#     ExperimentFactory._meta.sqlalchemy_session_persistence = persistdb
#     experiments = ExperimentFactory.create_batch(10)
#     EnvironmentConditionsFactory._meta.sqlalchemy_session_persistence = persistdb
#     environment_conditions = EnvironmentConditionsFactory.create_batch(10)
#     yield environment_conditions
#     if dropdb:
#         sess = dal.Session()
#         sess.close()
#         Base.metadata.drop_all(bind=dal.engine)

@pytest.fixture(scope="class")
def author(persistdb, dropdb):
    AuthorFactory._meta.sqlalchemy_session_persistence = persistdb
    print("Creating authors")
    authors = AuthorFactory.create_batch(10)
    yield authors
    if dropdb:
        sess = dal.Session()
        sess.close()
        Base.metadata.drop_all(bind=dal.engine)


# @pytest.fixture(scope="class")
# def software(persistdb, dropdb):
#     SoftwareFactory._meta.sqlalchemy_session_persistence = persistdb
#     softwares = SoftwareFactory.create_batch(10)
#     yield softwares
#     if dropdb:
#         sess = dal.Session()
#         sess.close()
#         Base.metadata.drop_all(bind=dal.engine)   

# @pytest.fixture(scope="class")
# def substrate(persistdb, dropdb):
#     SubstrateFactory._meta.sqlalchemy_session_persistence = persistdb
#     substrates = SubstrateFactory.create_batch(10)
#     yield substrates
#     if dropdb:
#         sess = dal.Session()
#         sess.close()
#         Base.metadata.drop_all(bind=dal.engine)

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client
