import factory

from grdb.database.models import RamanFile
from .common import test_db

LIST_SIZES = [1, 2, 3]


class RamanFileFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = RamanFile
        sqlalchemy_session = test_db.Session
        sqlalchemy_session_persistence = "flush"

    experiment = factory.SubFactory(
        "database.factories.ExperimentFactory", raman_files=None
    )

    filename = factory.Faker("file_name", extension="tif")
    url = factory.Faker("url")
    wavelength = factory.Faker("pyfloat", positive=False, min_value=0.0, max_value=800.0)
