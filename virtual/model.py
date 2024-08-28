from sqlalchemy import Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Integer, String, Double, Float, Date
from sqlalchemy.orm import relationship

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 

engine = create_engine('mysql+mysqlconnector://hostelpayment:abc123@localhost/hostel-payment')

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a Session
session = Session()

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    address = Column(String(100), nullable=False)  # Removed unique constraint
    phone_number = Column(String(20), nullable=False)  

class Booking(Base):
    __tablename__= 'bookings'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
    booking_date = Column(Date, nullable=False)
    duration = Column(Integer, nullable=False)
    total_cost = Column(Float, nullable=False)

    user = relationship('User')
    room = relationship('Room')

class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True)
    amount_to_pay = Column(Float, nullable=False)
    payment_Method = Column(String, nullable=False)
    Knockoff = Column(Integer, ForeignKey('bookings.id'), nullable=False)
    Remaining_balance = Column(Integer, ForeignKey('bookings.id'), nullable=False)


    booking = relationship('Booking')

class Invoice(Base):
    __tablename__ = 'invoices'
    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey('bookings.id'), nullable=False)
    invoice_date = Column(Date, nullable=False)
    amount_due = Column(Float, nullable=False)
    status = Column(String(50), nullable=False)
    booking = relationship('Booking')




   