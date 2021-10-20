from sqlalchemy import Column, Integer, String
from . import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)

    username = Column(String(32), nullable=False)

    first_name = Column(String(35), nullable=False)

    last_name = Column(String(35), nullable=False)

    email = Column(String(320), unique=True, nullable=False)

    password_hash = Column(String(256), nullable=False)

    # 0: read only, 1: read/write
    permission_level = Column(Integer, nullable=False, default=1)

    def __repr__(self):
        return '<User username:{}, name:"{} {}">'.format(self.username, self.first_name, self.last_name)
