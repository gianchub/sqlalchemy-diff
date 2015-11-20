# -*- coding: utf-8 -*-
import pytest


@pytest.fixture(scope="module")
def db_uri():
    return "mysql+mysqlconnector://root:@localhost/sqlalchemydiff"
