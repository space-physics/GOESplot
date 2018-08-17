#!/usr/bin/env python
from pathlib import Path
from matplotlib.pyplot import show  # draw, pause,
from argparse import ArgumentParser
import goes_quickplot as gq
from goes_quickplot.plots import plotgoes


def main():

    p = ArgumentParser()
    p.add_argument('datadir', help='directory of GOES image data to read')
    p.add_argument('pat', help='file glob pattern  preview:*.jpg  hires:*.nc', nargs='?',
                   default=['*.jpg', '*.nc'])
    p.add_argument('-d', '--downsample', help='downsample factor', type=int)
    p.add_argument('-wld', help='.wld path', default='data/')
    p.add_argument('-v', '--verbose', action='store_true')
    p = p.parse_args()

    datadir = Path(p.datadir).expanduser()
    if datadir.is_file():
        flist = [datadir]
    else:
        flist = []
        for pat in p.pat:
            flist += sorted(datadir.glob(pat))

    if len(flist) == 0:
        raise FileNotFoundError(f'No {p.pat} files found in {datadir}')

    print(f'{len(flist)} files found in {datadir}')

    for fn in flist:
        img = gq.load(fn)
        plotgoes(img, p.downsample, p.verbose)

        show()


if __name__ == '__main__':
    main()
