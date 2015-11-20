# -*- coding: utf-8 -*-
from unittest import TestCase

import six


if six.PY2:

    class TestCasePatch(TestCase):
        """Provide the assert_items_equal method for testing. """
        def runTest(self, *a, **kwa):  # Hack needed only in Python 2
            pass
    assert_items_equal = TestCasePatch().assertItemsEqual

else:

    assert_items_equal = TestCase().assertCountEqual
