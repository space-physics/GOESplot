#!/usr/bin/env python
"""parallel file downloading for Python 3"""
from datetime import timedelta
from dateutil.parser import parse
from pathlib import Path
import concurrent.futures
#
from goes_quickplot import datetimerange, get_goes


if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('goessat',help='number of GOES satellite e.g. 13',type=int)
    p.add_argument('goesmode',help='instrument [IR,WV,VS]')
    p.add_argument('start',help='time to start downloading data')
    p.add_argument('stop',help='time to stop downloading data')
    p.add_argument('outdir',help='directory to write data')
    p = p.parse_args()

    outdir = Path(p.outdir).expanduser()
    outdir.mkdir(parents=True,exist_ok=True)

    start, stop = parse(p.start), parse(p.stop)
# %% GOES 13
    tgoes = datetimerange(start, stop, timedelta(hours=3))
    print('downloading',len(tgoes),'files to',outdir)


    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as exe:
        future_file = {exe.submit(get_goes, t, outdir, p.goessat, p.goesmode): t for t in tgoes}
        for f in concurrent.futures.as_completed(future_file):
            t = future_file[f]

    print()
