import factory

from grdb.database.models import SemFile
from .common import test_db

LIST_SIZES = [1, 2, 3]


class SemFileFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = SemFile
        sqlalchemy_session = test_db.Session
        sqlalchemy_session_persistence = "flush"

    # experiment_id = factory.Sequence(lambda n:n)
    #experiment_id = None
    filename = factory.Faker("file_name", extension="tif")
    url = factory.Faker("url")
    #default_analysis_id = None
