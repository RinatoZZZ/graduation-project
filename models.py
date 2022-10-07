from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean
from db import Base, engine


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    name = Column(String)
    date_time_registration = Column(DateTime)
    last_time_active = Column(DateTime)
    link_photo = Column(String)
    vector_photo = Column(JSON)
    check_photo = Column(Boolean)
    in_active = Column(Boolean)


    def __repr__(self):
        return f'<User {self.username} {self.name} {self.date_time_registration}>'


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
