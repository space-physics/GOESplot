#!/usr/bin/env python
"""
Hi-res data
./plot-goes.py -d 8 ~/data/goes/goes13.2017.233.080017.BAND_02.nc

preview .jpg data
./plot-goes.py ~/data/goes13/goes13-IR-2017-07-13-15.jpg
"""
from pathlib import Path
from matplotlib.pyplot import show  # draw, pause,
from argparse import ArgumentParser

import goesplot as gq
from goesplot.plots import plotgoes


def main():

    p = ArgumentParser()
    p.add_argument("datadir", help="directory of GOES image data to read")
    p.add_argument("pat", help="file glob pattern  preview:*.jpg  hires:*.nc", nargs="?", default=["*.jpg", "*.nc"])
    p.add_argument("-d", "--downsample", help="downsample factor", type=int, default=8)
    p.add_argument("-wld", help=".wld path")
    p.add_argument("-v", "--verbose", action="store_true")
    p = p.parse_args()

    datadir = Path(p.datadir).expanduser()

    flist = [datadir] if datadir.is_file() else [sorted(datadir.glob(pat)) for pat in p.pat]

    if len(flist) == 0:
        raise FileNotFoundError(f"No {p.pat} files found in {datadir}")
    if len(flist) > 1:
        print(f"{len(flist)} files found in {datadir}")

    for fn in flist:
        img = gq.load(fn, p.downsample, p.wld)

        plotgoes(img, p.verbose)

        show()


if __name__ == "__main__":
    main()
