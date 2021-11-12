from sqlalchemy import Column, String, Integer, ForeignKey, Date, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import select, func, text, and_
from sqlalchemy.sql import exists
from sqlalchemy.schema import Table
from sqlalchemy.dialects.postgresql import *

from src.grdb.database import Base, class_registry

ExperimentToAuthorAssociation = Table('EXP_TO_ATHR_ASSCTN', Base.metadata,
                                      Column('author_id', Integer, ForeignKey('author.id')),
                                      Column('experiment_id', Integer, ForeignKey('experiment.id'))
                                      )


class Author(Base):
    """[summary]
    
    Args:
        Base ([type]): [description]
    
    Returns:
        [type]: [description]
    """

    id = Column(Integer, primary_key=True, info={"verbose_name": "ID"})

    first_name = Column(
        String(64), info={"verbose_name": "First Name", "required": False}
    )
    last_name = Column(
        String(64), info={"verbose_name": "Last Name", "required": False}
    )
    institution = Column(
        String(64), info={"verbose_name": "Institution", "required": False}
    )
    nanohub_userid = Column(
        Integer, info={"verbose_name": "nanoHub Submitter User ID"}
    )
    # Collection of experiments submitted by this author
    submitted_experiments = relationship("Experiment")

    # Collection of experiments associated with this author 
    authored_experiments = relationship("Experiment", secondary="EXP_TO_ATHR_ASSCTN", back_populates="authors")

    user = relationship("User", back_populates="author", uselist=False)

    @hybrid_property
    def full_name_and_institution(self):
        return "%s, %s   (%s)" % (self.last_name, self.first_name, self.institution)

    def json_encodable(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "institution": self.institution,
        }
