#!/usr/bin/env python
import goes_quickplot as gq
import pytest


def test_import():
    assert gq is not None


if __name__ == '__main__':
    pytest.main(['-x', __file__])
