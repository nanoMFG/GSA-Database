from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class DataBase:
    """
    Class that is used to access database in webapp.
    """

    def __init__(self, base=None):
        """
        Args:
            base (): declarative base
        """
        self.engine = None
        self.session = None
        self.base = base if base else None

    def init(self, db_url: str, enable_model_query=True):
        """
        Args:
            db_url (str): Database url to access the database.
                This initializes the engine and
        """
        self.engine = create_engine(db_url)
        self.session = scoped_session(sessionmaker(autocommit=False,
                                                   autoflush=False,
                                                   bind=self.engine))
        if enable_model_query and self.base:
            self.base.query = self.session.query_property()
