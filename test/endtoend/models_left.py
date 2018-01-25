# -*- coding: utf-8 -*-
import enum

from sqlalchemy import Column, ForeignKey, Integer, String, Unicode
from sqlalchemy.ext.declarative import declarative_base

from .enumadaptor import Enum


Base = declarative_base()


class Polarity(enum.Enum):
    NEGATIVE = 'NEGATIVE'
    POSITIVE = 'POSITIVE'


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(200), unique=True, index=True)
    age = Column(Integer, nullable=False, default=21)
    ssn = Column(Unicode(30), nullable=False)
    number_of_pets = Column(Integer, default=1, nullable=False)
    polarity = Column(Enum(Polarity, native_enum=True))
    spin = Column(Enum('spin_down', 'spin_up', native_enum=False))

    company_id = Column(
        Integer,
        ForeignKey("companies.id", name="fk_employees_companies"),
        nullable=False
    )

    role_id = Column(
        Integer,
        ForeignKey("roles.id", name="fk_employees_roles"),
        nullable=False
    )


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(200), nullable=False, unique=True)


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(50), nullable=False)


class Skill(Base):
    __tablename__ = "skills"

    slug = Column(String(50), primary_key=True)
    description = Column(Unicode(100), nullable=True)

    employee = Column(
        Integer,
        ForeignKey("employees.id", name="fk_skills_employees"),
        nullable=False
    )


class MobileNumber(Base):
    __tablename__ = "mobile_numbers"

    id = Column(Integer, primary_key=True)
    number = Column(String(40), nullable=False)

    owner = Column(
        Integer,
        ForeignKey("employees.id", name="fk_mobile_numbers_employees"),
        nullable=False
    )
