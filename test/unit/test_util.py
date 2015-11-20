# -*- coding: utf-8 -*-
import json
import os
import uuid

import pytest

from sqlalchemydiff.util import CompareResult, InspectorFactory
from mock import Mock, patch, call


class TestCompareResult(object):

    def test___init__(self):
        info, errors = Mock(), Mock()

        result = CompareResult(info, errors)

        assert info == result.info
        assert errors == result.errors

    def test_is_match(self):
        info, errors = {}, {}
        result = CompareResult(info, errors)

        assert True == result.is_match

        result.errors = {1: 1}
        assert False == result.is_match

    def test_dump_info(self):
        info = {'some': 'info'}
        filename = '{}.txt'.format(uuid.uuid4())
        result = CompareResult(info, {})

        result.dump_info(filename=filename)

        with open(filename, 'rU') as stream:
            assert info == json.loads(stream.read())

        os.unlink(filename)

    def test_dump_errors(self):
        errors = {'some': 'errors'}
        filename = '{}.txt'.format(uuid.uuid4())
        result = CompareResult({}, errors)

        result.dump_errors(filename=filename)

        with open(filename, 'rU') as stream:
            assert errors == json.loads(stream.read())

        os.unlink(filename)


class TestInspectorFactory(object):

    @pytest.yield_fixture
    def create_engine_mock(self):
        with patch('sqlalchemydiff.util.create_engine') as m:
            yield m

    @pytest.yield_fixture
    def inspect_mock(self):
        with patch('sqlalchemydiff.util.inspect') as m:
            yield m

    def test_from_uri(self, inspect_mock, create_engine_mock):
        uri = 'some-db-uri/some-db-name'
        inspector = InspectorFactory.from_uri(uri)

        create_engine_mock.assert_called_once_with(uri)
        inspect_mock.assert_called_once_with(create_engine_mock.return_value)

        assert inspect_mock.return_value == inspector
