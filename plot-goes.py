#!/usr/bin/env python
from pathlib import Path
from matplotlib.pyplot import draw,pause
#
import goes_quickplot as gq
from goes_quickplot.plots import plotgoes

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('datadir',help='directory of GOES image data to read')
    p.add_argument('pat',help='file glob pattern',nargs='?', default='*.jpg')
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

# %% each instrument type has unique coordinate registration in general
    for f in flist:
        img = gq.loadgoes(f)

        lat, lon = gq.wld2mesh(p.wld, f.stem.split('-')[1].upper(), img.shape[:2])

        plotgoes(img, f, lat, lon, 10)

        draw(); pause(0.2)