#!/usr/bin/env python
from pathlib import Path
from matplotlib.pyplot import draw, pause, show
from argparse import ArgumentParser
import goes_quickplot as gq
from goes_quickplot.plots import plotgoes


def main():

    p = ArgumentParser()
    p.add_argument('datadir', help='directory of GOES image data to read')
    p.add_argument('pat', help='file glob pattern  preview:*.jpg  hires:*.nc', nargs='?', default='*.jpg')
    p.add_argument('-d', '--downsample', help='downsample factor', type=int)
    p.add_argument('-wld', help='.wld path', default='data/')
    p.add_argument('-v', '--verbose', action='store_true')
    p = p.parse_args()

    datadir = Path(p.datadir).expanduser()
    if datadir.is_file():
        flist = [datadir]
    else:
        flist = sorted(datadir.glob(p.pat))

    if len(flist) == 0:
        raise FileNotFoundError(f'No {p.pat} files found in {datadir}')

    print(f'{len(flist)} files found in {datadir}')

    if p.pat == '*.jpg':
        plotpreview(flist, p.wld)
    elif p.pat == '*.nc':
        plothires(flist, p.downsample, p.verbose)
    else:
        raise ValueError(f'unknown data type {p.pat}')


def plotpreview(flist: list, wld: Path):
    """each instrument type has unique coordinate registration in general
    """
    for f in flist:
        img = gq.loadgoes_preview(f, wld)

        plotgoes(img, f, 10)

        draw()
        pause(0.2)


def plothires(flist: list, downsample: int, verbose: bool=False):
    """plot hi resoliution data"""
    for f in flist:
        img = gq.loadgoes_hires(f)

        plotgoes(img, f, downsample, verbose)

        show()


if __name__ == '__main__':
    main()
