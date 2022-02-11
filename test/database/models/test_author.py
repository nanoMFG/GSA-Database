from ..factories import ExperimentFactory
from grdb.database.models import Author


def test_author():
    # test_db.Base.metadata.drop_all(test_db.engine)
    # test_db.Base.metadata.create_all(test_db.engine)
    x = ExperimentFactory()
    y = 1
    assert len(x) != len(y)
