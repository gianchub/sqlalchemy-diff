# -*- coding: utf-8 -*-
import enum

from sqlalchemy import Column, ForeignKey, Integer, String, Unicode
from sqlalchemy.ext.declarative import declarative_base

from .enumadaptor import Enum


Base = declarative_base()


class Polarity(enum.Enum):
    NEG = 'NEG'
    POS = 'POS'


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(200), unique=True, index=False)
    age = Column(Integer, nullable=False, default=21)
    ssn = Column(Unicode(30), nullable=False)
    number_of_pets = Column(Integer, default=1, nullable=False)
    polarity = Column(Enum(Polarity, native_enum=True))
    spin = Column(Enum('down', 'up', native_enum=False))

    company_id = Column(
        Integer,
        ForeignKey("companies.id", name="fk_emp_comp"),
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
    name = Column(Unicode(200), nullable=True, unique=False)


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(60), nullable=False)


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True)
    slug = Column(String(50))
    description = Column(Unicode(100), nullable=True)

    employee = Column(
        Integer,
        ForeignKey("employees.id", name="fk_skills_employees"),
        nullable=False
    )


class PhoneNumber(Base):
    __tablename__ = "phone_numbers"

    id = Column(Integer, primary_key=True)
    number = Column(String(40), nullable=False)

    owner = Column(
        Integer,
        ForeignKey("employees.id", name="fk_phone_numbers_employees"),
        nullable=False
    )
