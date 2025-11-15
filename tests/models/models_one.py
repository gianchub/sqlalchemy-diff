# ty: ignore[invalid-assignment]
import datetime
import enum

from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Unicode,
)
from sqlalchemy.orm import Mapped, declarative_base, relationship
from sqlalchemy.orm.decl_api import DeclarativeMeta


Base: DeclarativeMeta = declarative_base()


class Title(enum.Enum):
    ENGINEER = "ENGINEER"
    MANAGER = "MANAGER"
    DIRECTOR = "DIRECTOR"
    CEO = "CEO"


class Employee(Base):
    __tablename__ = "employees"
    __table_args__ = (CheckConstraint("age > 0 AND age <= 100", name="check_age"),)

    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(Unicode(200), unique=True, index=True)
    age: Mapped[int] = Column(Integer, nullable=False, default=21)
    ssn: Mapped[str] = Column(Unicode(30), nullable=False)
    number_of_pets: Mapped[int] = Column(Integer, default=1, nullable=False)
    title: Mapped[Title | None] = Column(Enum(Title, native_enum=True))
    department: Mapped[str | None] = Column(  # ty: ignore[invalid-assignment]
        Enum("Product", "Engineering", "Sales", native_enum=False)
    )

    company_id: Mapped[int] = Column(
        Integer,
        ForeignKey("companies.id", name="fk_employees_companies"),
        nullable=False,
    )
    role_id: Mapped[int] = Column(
        Integer, ForeignKey("roles.id", name="fk_employees_roles"), nullable=False
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

    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(Unicode(200), nullable=False, unique=True)

    employees: Mapped[list["Employee"]] = relationship("Employee", back_populates="company")


class Role(Base):
    __tablename__ = "roles"
    __table_args__ = (CheckConstraint("LENGTH(name) > 5", name="check_name"),)

    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(Unicode(50), nullable=False)

    employees: Mapped[list["Employee"]] = relationship("Employee", back_populates="role")

    role_type: Mapped[str | None] = Column(Enum("Permanent", "Contractor", name="role_type"))


class Skill(Base):
    __tablename__ = "skills"
    __table_args__ = {
        "comment": "Skills are the skills of the employees",
    }

    slug: Mapped[str] = Column(String(50), primary_key=True)
    description: Mapped[str | None] = Column(Unicode(100), nullable=True)

    employee: Mapped[int] = Column(
        Integer, ForeignKey("employees.id", name="fk_skills_employees"), nullable=False
    )

    employee_rel: Mapped["Employee"] = relationship("Employee", back_populates="skills")


class MobileNumber(Base):
    __tablename__ = "mobile_numbers"
    __table_args__ = {
        "comment": "Mobile numbers are the mobile numbers of the employees",
    }

    id: Mapped[int] = Column(Integer, primary_key=True)
    number: Mapped[str] = Column(String(40), nullable=False)

    owner: Mapped[int] = Column(Integer, ForeignKey("employees.id"), nullable=False)

    owner_rel: Mapped["Employee"] = relationship("Employee", back_populates="mobile_numbers")


class Tenure(Base):
    __tablename__ = "tenures"

    employee_id: Mapped[int] = Column(
        Integer,
        ForeignKey("employees.id", name="fk_tenures_employees"),
        primary_key=True,
    )
    company_id: Mapped[int] = Column(
        Integer,
        ForeignKey("companies.id", name="fk_tenures_companies"),
        primary_key=True,
    )
    start_date: Mapped[datetime.date] = Column(DateTime(timezone=True), nullable=False)
    end_date: Mapped[datetime.date] = Column(DateTime(timezone=True), nullable=True)
