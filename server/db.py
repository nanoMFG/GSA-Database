from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from src.grdb.database import Base


class DataBase:
    """
    Class that is used to access database in webapp.
    """

    def __init__(self):
        self.engine = None
        self.session = None

    def init(self, db_url: str):
        """
        Args:
            db_url (str): Database url to access the database.
                This initializes the engine and
        """
        self.engine = create_engine(db_url)
        self.session = scoped_session(sessionmaker(autocommit=False,
                                                   autoflush=False,
                                                   bind=self.engine))
        Base.query = self.session.query_property()
