from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import warnings


class Database:
    """
    Class that is used to access database in webapp.
    """

    def __init__(self, base=None):
        """
        Args:
            base (): declarative base
        """
        self.engine = None
        self.Session = None
        self.Base = base if base else None

    def init(self, db_url: str, enable_model_query: bool = True):
        """
        Args:
            db_url (str): Database url to access the database.
                This initializes the engine and
            enable_model_query (bool): enable Model.query.xxx to query the database.
        """
        self.engine = create_engine(db_url, pool_pre_ping=True)
        self.Session = scoped_session(sessionmaker(autocommit=False,
                                                   autoflush=False,
                                                   bind=self.engine))
        if enable_model_query and self.Base:
            self.Base.query = self.Session.query_property()
        elif enable_model_query:
            warnings.warn("Model query enabled but no declarative base passed.")
