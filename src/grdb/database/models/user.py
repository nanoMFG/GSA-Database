from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.grdb.database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)

    email = Column(String(320), primary_key=True)

    password_hash = Column(String(256), nullable=False)

    # 0: read only, 1: read/write
    permission_level = Column(Integer, nullable=False, default=1)

    author_id = Column(Integer, ForeignKey('author.id'))

    author = relationship("Author", back_populates="user", uselist=False)
