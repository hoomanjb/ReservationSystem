from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text


from .database_base import Base

# we can use some relationship with this tables but we don't want to have add any complexity


class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    listing_id = Column(Integer, nullable=False, default=True)

    def __init__(self, name, listing_id):
        self.name = name
        self.listing_id = listing_id


class Reservation(Base):
    __tablename__ = 'reservation'
    id = Column(Integer, primary_key=True, nullable=False)
    room_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    start_time = Column(TIMESTAMP(timezone=True), nullable=True)
    end_time = Column(TIMESTAMP(timezone=True), nullable=True)
    user_id = Column(Integer, nullable=False)

    def __init__(self, room_id, name, start_time, end_time, user_id):
        self.room_id = room_id
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.user_id = user_id


class Listing(Base):
    __tablename__ = 'listing'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user_id = Column(Integer, nullable=False)

    def __init__(self, name, user_id, description):
        self.name = name
        self.user_id = user_id
        self.description = description


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    phone_number = Column(String)

    def __init__(self, email, password):
        self.email = email
        self.password = password
