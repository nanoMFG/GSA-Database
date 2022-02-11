import factory

from grdb.database.models import Substrate
from .common import test_db


class SubstrateFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Substrate
        sqlalchemy_session = test_db.Session
        sqlalchemy_session_persistence = "flush"

    catalyst = factory.Iterator(Substrate.catalyst.info["choices"])
    thickness = factory.Faker(
        "pyfloat", positive=False, min_value=0.0, max_value=10.0
    )
    diameter = factory.Faker(
        "pyfloat", positive=False, min_value=0.0, max_value=10.0
    )
    length = factory.Faker(
        "pyfloat", positive=False, min_value=0.0, max_value=10.0
    )
    surface_area = factory.Faker(
        "pyfloat", positive=False, min_value=0.0, max_value=10.0
    )
