import factory

from grdb.database.models import SemAnalysis
from .common import test_db

LIST_SIZES = [1, 2, 3]


class SemAnalysisFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = SemAnalysis
        sqlalchemy_session = test_db.Session
        sqlalchemy_session_persistence = "flush"

    # sem_file = factory.SubFactory(
    #     "database.factories.SemFileFactory", analyses=None
    # )

    # sem_file_id = factory.Faker('pyint',max_value=100)
    software_name = 'fake_sw'
    software_version = '1.1.0'
