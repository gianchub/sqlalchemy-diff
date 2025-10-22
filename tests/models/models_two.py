import datetime
import enum
from typing import Optional

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
    Unicode,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import Mapped, declarative_base, relationship
from sqlalchemy.orm.decl_api import DeclarativeMeta


Base: DeclarativeMeta = declarative_base()


class Title(enum.Enum):
    ENGINEER = "ENGINEER"
    DIRECTOR = "DIRECTOR"
    CEO = "CEO"
    VP = "VP"


class Employee(Base):
    __tablename__ = "employees"
    __table_args__ = (
        CheckConstraint("age > 0 AND age <= 90", name="check_age"),
        Index("idx_title_department", "title", "department"),
        UniqueConstraint("name", "age", name="unique_employee_name_age"),
    )

    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(Unicode(200), unique=True, index=False)
    age: Mapped[int] = Column(
        Integer,
        nullable=True,
        default=21,
        server_default=text("CAST(21 as int)"),
    )
    ssn: Mapped[str] = Column(Unicode(30), nullable=False, index=True)
    number_of_pets: Mapped[int] = Column(BigInteger, default=100, nullable=True)
    title: Mapped[Optional[Title]] = Column(Enum(Title, native_enum=True))
    department: Mapped[Optional[str]] = Column(
        Enum("Product", "Engineering", "Sales", native_enum=False)
    )

    company_id: Mapped[int] = Column(
        Integer,
        ForeignKey("companies.id", name="fk_employees_companies"),
        nullable=False,
    )
    role_id: Mapped[int] = Column(
        String(50), ForeignKey("roles.id", name="fk_employees_roles"), nullable=False
    )

    # Relationships
    company: Mapped["Company"] = relationship("Company", back_populates="employees")
    role: Mapped["Role"] = relationship("Role", back_populates="employees")
    skills: Mapped[list["Skill"]] = relationship("Skill", back_populates="employee_rel")
    mobile_numbers: Mapped[list["MobileNumber"]] = relationship(
        "MobileNumber", back_populates="owner_rel"
    )


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=False)
    name: Mapped[str] = Column(Unicode(200), unique=False)

    employees: Mapped[list["Employee"]] = relationship("Employee", back_populates="company")

    company_type: Mapped[Optional[str]] = Column(
        Enum("Public", "Private", "Sole Trader", name="company_type")
    )


class Role(Base):
    __tablename__ = "roles"
    __table_args__ = (CheckConstraint("LENGTH(name) > 5", name="check_name"),)

    id: Mapped[str] = Column(String(50), primary_key=True)
    name: Mapped[str] = Column(Unicode(50), nullable=False, index=True)

    employees: Mapped[list["Employee"]] = relationship("Employee", back_populates="role")

    role_type: Mapped[Optional[str]] = Column(Enum("Permanent", "Contractor", name="role_type"))


class Skill(Base):
    __tablename__ = "skills"
    __table_args__ = {
        "comment": "Skills are the skills of the employees",
    }

    slug: Mapped[str] = Column(String(50), primary_key=True)
    description: Mapped[Optional[str]] = Column(
        Unicode(100), nullable=False, default="Skill description", unique=True
    )

    person: Mapped[int] = Column(
        Integer, ForeignKey("employees.id", name="fk_skills_employees"), nullable=False
    )

    employee_rel: Mapped["Employee"] = relationship("Employee", back_populates="skills")


class MobileNumber(Base):
    __tablename__ = "mobile_numbers"
    __table_args__ = {
        "comment": "Mobile numbers are the phone numbers of the employees",
    }

    id: Mapped[int] = Column(Integer, comment="The ID of the mobile number")
    number: Mapped[str] = Column(String(50), primary_key=True)

    owner: Mapped[int] = Column(
        Integer,
        ForeignKey("employees.id", name="foreign_key_mobile_numbers_employees"),
        nullable=True,
    )

    owner_rel: Mapped["Employee"] = relationship("Employee", back_populates="mobile_numbers")


class Employment(Base):
    __tablename__ = "employments"
    __table_args__ = (
        CheckConstraint("end_date > start_date", name="check_end_date_after_start_date"),
    )

    employee_id: Mapped[int] = Column(
        Integer,
        ForeignKey("employees.id", name="fk_employments_employees"),
        primary_key=True,
    )
    company_id: Mapped[int] = Column(
        Integer,
        ForeignKey("companies.id", name="fk_employments_companies"),
        primary_key=True,
    )
    start_date: Mapped[datetime.date] = Column(DateTime(timezone=True), nullable=False)
    end_date: Mapped[datetime.date] = Column(DateTime(timezone=True), nullable=True)
