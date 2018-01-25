"""
Adapt Enum across versions of SQLAlchemy.

SQLAlchemy supports PEP 435 Enum classes as of 1.1.
Prior versions supported only the values as strings.

Export a suitable column type for either case.
"""
import enum
import sqlalchemy


def Enum(*enums, **kw):
    if sqlalchemy.__version__ >= '1.1':
        return sqlalchemy.Enum(*enums, **kw)

    if len(enums) == 1 and issubclass(enums[0], enum.Enum):
        return sqlalchemy.Enum(*(v.name for v in enums[0]), **kw)

    return sqlalchemy.Enum(*enums, **kw)
