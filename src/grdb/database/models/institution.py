from sqlalchemy import Column, String, Integer, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from grdb.database import Base


class Institution(Base):
    __tablename__ = 'institution'

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String(150))

    country = Column(String(50))
