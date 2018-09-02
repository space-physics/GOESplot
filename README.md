[![Build Status](https://travis-ci.com/scivision/GOESutils.svg?branch=master)](https://travis-ci.com/scivision/GOESutils)
[![Coverage Status](https://coveralls.io/repos/github/scivision/GOESutils/badge.svg?branch=master)](https://coveralls.io/github/scivision/GOESutils?branch=master)
[![Build status](https://ci.appveyor.com/api/projects/status/ork0ny0prr1h8hen?svg=true)](https://ci.appveyor.com/project/scivision/goesutils)
[![PyPi version](https://img.shields.io/pypi/pyversions/goesutils.svg)](https://pypi.python.org/pypi/goesutils)
[![PyPi formats](https://img.shields.io/pypi/format/goesutils.svg)](https://pypi.python.org/pypi/goesutils)
[![PyPi Download stats](http://pepy.tech/badge/goesutils)](http://pepy.tech/project/goesutils)

# GOES Utilities

Quick Python script to download and plot GOES satellite preview and hi-resolution data by date/time.

![goesutils7 absorption](tests/goes13-IR-2017-07-13-12.jpg)

## Install

    python -m pip install -e .

## Usage

The scripts work with two types of data:
* [preview .jpg](https://www.ncdc.noaa.gov/gibbs/), 3 hour cadence
* [full fidelity NetCDF4](https://www.class.ncdc.noaa.gov/saa/products/welcome), 1 minute cadence

### Full fidelity data

Select data using GOES 
[shopping cart](https://www.class.ncdc.noaa.gov/saa/products/shopping_cart_upd).
Search by date, geographic region. 
Consider getting NetCDF format data unless you're familiar with the other options.
[Register](https://www.class.ncdc.noaa.gov/saa/products/user_profile)
for NOAA CLASS if needed. 

It may take up to 48 hours to get access to your order.
NOAA CLASS emails you when data is ready. 
Each 5-10 minute set of multi-band data is several hundred megabytes at full resolution.

### Preview (3 hour cadence)

1. Get [GOES preview imagedata](https://www.ncdc.noaa.gov/gibbs/) with parallel download:
   ```sh
   python get-goes-preview.py goesnum start stop outdir
   ```
   example: download IR from GOES-13 2018-01-01 to 2018-01-02 to `~/data/goes13`:
   ```sh
   python get-goes-preview.py 13 IR 2018-01-01T00 2018-01-03T00 ~/data/goes13
   ```
   These are updated every 3 hours. 
   For science use, you'll want the 
   [full fidelity GOES data](https://www.class.ncdc.noaa.gov/saa/products/welcome)
   updated on minutely timescale.
2. Plot GOES IR data georegistered via Cartopy:
   ```sh
   python plot-goes.py ~/data/goes13
   ```
   Plot a specific file:
   ```sh
   python plot-goes.py ~/data/goes13/2018-01-01T12:35:00.jpg
   ```
   

