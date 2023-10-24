from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Clients(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    phone = Column(String(50), nullable=False, unique=True)
    document = Column(String(50), nullable=False, unique=True)
    address = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    zip_code = Column(String(50), nullable=False)
    birthday = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    bikes = relationship('Bikes', back_populates='clients')

class Bikes(Base):
    __tablename__ = 'bikes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    brand = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    year = Column(Integer, nullable=False)
    color = Column(String(50), nullable=False)
    serial_number = Column(String(50), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    client_id = Column(Integer, ForeignKey('clients.id'))
    clients = relationship('Clients', back_populates='bikes')
