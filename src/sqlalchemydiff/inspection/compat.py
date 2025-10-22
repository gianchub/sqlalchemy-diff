"""Compatibility layer for sqlalchemy."""

try:
    from sqlalchemy import Inspector
except ImportError:  # pragma: no cover
    from sqlalchemy.engine.reflection import Inspector


__all__ = ["Inspector"]
