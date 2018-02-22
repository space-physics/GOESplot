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

1. Get `GOES data <hhttps://www.ncdc.noaa.gov/gibbs//>`_ with parallel download::

        python download-goes.py goesnum start stop outdir

   example: download IR from GOES-13 2018-01-01 to 2018-01-02 to ``~/data/goes13``::

        python download-goes.py 13 IR 2018-01-01T00 2018-01-03T00 ~/data/goes13

2. Plot GOES IR data georegistered via Cartopy::

        python plot-goes.py ~/data/goes13

   Plot a specific file::

        python plot-goes.py ~/data/nexrad/2018-01-01T12:35:00.png


