from sqlalchemy import Column, String, Integer

from fastapiproject.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __repr__(self):
        return f"<User(id={self.id}, " \
               f"name=\"{self.name})>"
