import factory
import random

from grdb.database.models import RamanAnalysis
from .common import test_db

LIST_SIZES = [1, 2, 3, 4, 5, 6]


class RamanAnalysisFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = RamanAnalysis
        sqlalchemy_session = test_db.Session
        sqlalchemy_session_persistence = "flush"

    # raman_file_id = None
    # raman_set = factory.RelatedFactory(
    #     "test.database.factories.RamanSetFactory",
    #     "raman_spectra"
    #     )
    # xcoord = factory.Faker("pyint", min_value=0, max_value=100)
    # ycoord = factory.Faker("pyint", min_value=0, max_value=100)
    percent = factory.Faker("pyfloat", positive=False, min_value=0.0, max_value=100.0)
    d_peak_shift = factory.Faker(
        "pyfloat", positive=False, min_value=0.0, max_value=100.0
    )
    d_peak_amplitude = factory.Faker(
        "pyfloat", positive=False, min_value=0.0, max_value=100.0
    )
    d_fwhm = factory.Faker("pyfloat", positive=False, min_value=0.0, max_value=100.0)
    g_peak_shift = factory.Faker(
        "pyfloat", positive=False, min_value=0.0, max_value=100.0
    )
    g_peak_amplitude = factory.Faker(
        "pyfloat", positive=False, min_value=0.0, max_value=100.0
    )
    g_fwhm = factory.Faker("pyfloat", positive=False, min_value=0.0, max_value=100.0)
    g_prime_peak_shift = factory.Faker(
        "pyfloat", positive=False, min_value=0.0, max_value=100.0
    )
    g_prime_peak_amplitude = factory.Faker(
        "pyfloat", positive=False, min_value=0.0, max_value=100.0
    )
    g_prime_fwhm = factory.Faker(
        "pyfloat", positive=False, min_value=0.0, max_value=100.0
    )
