from sqlalchemy import Column, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Person(Base):
    __tablename__ = "persons"

    passport = Column(String, primary_key=True)
    name = Column(String)
    last_name = Column(String)
    fullname = Column(String, index=True)
    email = Column(String)
    telfnumber = Column(String)
    sex = Column(String)

    IBAN = Column(String)
    salary = Column(String)

    company = Column(String)
    company_address = Column(String)
    company_email = Column(String)
    company_telfnumber = Column(String)
    job = Column(String)

    city = Column(String, index=True)
    address = Column(String)
    IPv4 = Column(String)
