#!/usr/bin/env python
"""parallel file downloading for Python 3
GOES 3-hour cadence JPG previews are widely available, but have limited scientific application.
Once you know the time span of interest, request full-fidelity data from NOAA CLASS system,
which gives ~ 100 MB/minute of data!

This program is for downloading:
* 3-hour JPG low-resolution previews
"""
import goes_quickplot
from argparse import ArgumentParser


def main():
    p = ArgumentParser()
    p.add_argument('goessat', help='number of GOES satellite e.g. 13', type=int)
    p.add_argument('goesmode', help='instrument [IR,WV,VS]')
    p.add_argument('start', help='time to start downloading data')
    p.add_argument('stop', help='time to stop downloading data')
    p.add_argument('outdir', help='directory to write data')
    p = p.parse_args()

    goes_quickplot.get_preview(p.outdir, p.start, p.stop, p.goessat, p.goesmode)


if __name__ == '__main__':
    main()
