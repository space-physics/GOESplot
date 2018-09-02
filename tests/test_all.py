#!/usr/bin/env python
import goesutils as gq
import pytest
from pathlib import Path

R = Path(__file__).parent


def test_load_preview():
    img = gq.load(R / 'goes13-IR-2017-07-13-12.jpg')

    assert img.shape == (1200, 1200, 3)


def test_load_hires():
    pytest.importorskip('netCDF4')
    img = gq.load(R / 'goes13.2017.233.080017.BAND_02.nc')

    assert img.shape == (1100, 2500)


if __name__ == '__main__':
    pytest.main(['-xrsv', __file__])
