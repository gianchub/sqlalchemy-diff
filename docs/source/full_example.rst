.. _full_example:

A full comparison PyTest Example
================================


Let's assume we have the following models:

``# models_left.py``

.. literalinclude:: ../testing/models_left.py

And these:

``# models_right.py``

.. literalinclude:: ../testing/models_right.py


This is how you could write a complete test suite for them:


.. literalinclude:: ../testing/test_example.py