from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


class DBConnectionFactory:
    """Create a SQLAlchemy engine."""

    @staticmethod
    def create_engine(uri: str, **params: Any) -> Engine:
        return create_engine(uri, **params)
