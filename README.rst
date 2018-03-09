==================
GOES-quickplot
==================
Quick Python script to download and plot GOES satellite PNGs by date/time

Install
=======
::

    python -m pip install -e .


Usage
=====

Full fidelity data
------------------

1. Select data using GOES `shopping cart <https://www.class.ncdc.noaa.gov/saa/products/shopping_cart_upd>`_.
   Search by date, geographic region. Consider getting NetCDF format data unless you're familiar with the other options.
   `Register <https://www.class.ncdc.noaa.gov/saa/products/user_profile>`_ for NOAA CLASS if needed.
   It may take up to 48 hours to get access to your order, NOAA CLASS emails you when data is ready.
   Each 5-10 minute set of multi-band data is several hundred megabytes at full resolution.



Preview (3 hour cadence)
------------------------

1. Get `GOES preview imagedata <https://www.ncdc.noaa.gov/gibbs/>`_ with parallel download::

        python get-goes-preview.py goesnum start stop outdir

   example: download IR from GOES-13 2018-01-01 to 2018-01-02 to ``~/data/goes13``::

        python get-goes-preview.py 13 IR 2018-01-01T00 2018-01-03T00 ~/data/goes13

These are updated every 3 hours.
For science use, you'll want the `full fidelity GOES data <https://www.class.ncdc.noaa.gov/saa/products/welcome>`_ updated on minutely timescale.

2. Plot GOES IR data georegistered via Cartopy::

        python plot-goes.py ~/data/goes13

   Plot a specific file::

        python plot-goes.py ~/data/goes13/2018-01-01T12:35:00.png



Notes
=====



