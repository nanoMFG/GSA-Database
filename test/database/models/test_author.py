from grdb.database.models import Author

def test_authors_exist(grdb,session):
    authors = session.query(Author).all()
    assert len(authors) != 0
