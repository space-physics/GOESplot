# GOES Plot

![Actions Status](https://github.com/space-physics/goesplot/workflows/ci/badge.svg)
[![PyPi Download stats](http://pepy.tech/badge/goesplot)](http://pepy.tech/project/goesplot)

Quick Python script to download and plot GOES satellite preview and hi-resolution data by date/time.

![goes absorption](tests/goes13-IR-2017-07-13-12.jpg)


```sh
python -m pip install -e .
```

The scripts work with two types of data:

* [preview .jpg](https://www.ncdc.noaa.gov/gibbs/), 3 hour cadence
* [full fidelity NetCDF4](https://www.class.ncdc.noaa.gov/saa/products/welcome), 1 minute cadence

Full fidelity data:

Select data using GOES
[shopping cart](https://www.class.ncdc.noaa.gov/saa/products/shopping_cart_upd).
Search by date, geographic region.
Consider getting NetCDF format data unless you're familiar with the other options.
[Register](https://www.class.ncdc.noaa.gov/saa/products/user_profile)
for NOAA CLASS if needed.

It may take up to 48 hours to get access to your order.
NOAA CLASS emails you when data is ready.
Each 5-10 minute set of multi-band data is several hundred megabytes at full resolution.

Preview (3 hour cadence):

Get [GOES preview imagedata](https://www.ncdc.noaa.gov/gibbs/) with parallel download:

```sh
python get-goes-preview.py goesnum start stop outdir
```

example: download IR from GOES-13 2018-01-01 to 2018-01-02 to `~/data/goes13`:

```sh
python get-goes-preview.py 13 IR 2018-01-01T00 2018-01-03T00 ~/data/goes13
```

These are updated every 3 hours.
For science use, the
[full fidelity GOES data](https://www.class.ncdc.noaa.gov/saa/products/welcome)
are updated on minutely timescale.

Plot GOES IR data georegistered via Cartopy:

```sh
python plot-goes.py ~/data/goes13
```

Plot a specific file:

```sh
python plot-goes.py ~/data/goes13/2018-01-01T12:35:00.jpg
```
