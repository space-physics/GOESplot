#!/usr/bin/env python
from pathlib import Path
from matplotlib.pyplot import draw,pause,show
#
import goes_quickplot as gq
from goes_quickplot.plots import plotgoes

def plotpreview(flist:list, wld:Path):
    """each instrument type has unique coordinate registration in general
    """
    for f in flist:
        img = gq.loadgoes_preview(f, wld)

        plotgoes(img, f, 10)

        draw(); pause(0.2)


def plothires(flist:list):
    """plot hi resoliution data"""
    for f in flist:
        img = gq.loadgoes_hires(f)

        plotgoes(img, f, downsample=8)

        show()

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('datadir',help='directory of GOES image data to read')
    p.add_argument('pat',help='file glob pattern  preview:*.jpg  hires:*.nc',nargs='?', default='*.jpg')
    p.add_argument('-wld',help='.wld path',default='data/')
    p = p.parse_args()

    datadir = Path(p.datadir).expanduser()
    if datadir.is_file():
        flist = [datadir]
    else:
        flist = sorted(datadir.glob(p.pat))

    if len(flist) == 0:
        raise FileNotFoundError(f'No {p.pat} files found in {datadir}')

    print(f'{len(flist)} files found in {datadir}')

    if p.pat=='*.jpg':
        plotpreview(flist, p.wld)
    elif p.pat=='*.nc':
        plothires(flist)
    else:
        raise ValueError(f'unknown data type {p.pat}')