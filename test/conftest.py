import pytest


@pytest.fixture(scope="session")
def db_uri(request):
    return request.config.getoption('TEST_DB_URL')


def pytest_addoption(parser):
    parser.addoption(
        '--test-db-url',
        action='store',
        dest='TEST_DB_URL',
        default=(
            'mysql+mysqlconnector://root:@localhost:3306/'
            'sqlalchemydiff'
        ),
        help=(
            'DB url for testing (e.g. '
            '"mysql+mysqlconnector://root:@localhost:3306/'
            'sqlalchemydiff''")'
        )
    )
