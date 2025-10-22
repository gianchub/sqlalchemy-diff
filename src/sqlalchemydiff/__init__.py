from importlib.metadata import PackageNotFoundError, version


def app_version():  # pragma: no cover
    try:
        return version("sqlalchemy-diff")
    except PackageNotFoundError:
        return "unknown"


__version__ = app_version()
