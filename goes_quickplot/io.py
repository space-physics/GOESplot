from time import sleep
from pathlib import Path
from dateutil.parser import parse
import concurrent.futures
import urllib.request
import ftplib
from datetime import datetime, timedelta
try:
    import netCDF4
except ImportError:
    netCDF4 = None
#
from . import datetimerange


def get_hires(host: str, ftpdir: str, flist: list, odir: Path, clobber: bool=False):
    """download hi-res GOES data over FTP"""

    odir = Path(odir).expanduser()
    print('writing', len(flist), 'files to', odir)

    with ftplib.FTP(host, 'anonymous', 'guest', timeout=15) as F:
        F.cwd(ftpdir)

        for i, f in enumerate(flist):
            parts = f.split('/')
            rpath = parts[-2]
            rfn = parts[-1]
            if F.pwd().split('/')[-1] != rpath:
                F.cwd(rpath)

            ofn = odir / f
            if not clobber:  # check NetCDF4 files to see if we can read them or if they are corrupted by aborted download.
                if ofn.is_file() and ofn.suffix == '.nc':
                    try:
                        if netCDF4:
                            with netCDF4.Dataset(ofn, 'r') as n:
                                if n.variables:
                                    continue
                    except Exception:
                        pass

            print(f'{i/len(flist)*100:.1f} %  {ofn}')
            ofn.parent.mkdir(parents=True, exist_ok=True)
            with ofn.open('wb') as h:
                F.retrbinary(f'RETR {rfn}', h.write)

            sleep(0.5)  # anti-leech


def parse_email(txtfn: Path):
    """Parse GOES hi-res file list from email"""
    txtfn = Path(txtfn).expanduser()

    flist = []
    with txtfn.open('r') as f:
        for line in f:
            L = line.strip()
            if L.startswith('get'):
                flist.append(L.split(' ')[-1])
                continue
            if L.startswith('cd'):
                ftpdir = L.split(' ')[-1]

    return ftpdir, flist
# %% preview


def get_preview(odir: Path, start: datetime, stop: datetime, goessat: int, goesmode: str):
    odir = Path(odir).expanduser()
    odir.mkdir(parents=True, exist_ok=True)

    if isinstance(start, str):
        start = parse(start)
    if isinstance(stop, str):
        stop = parse(stop)
# %% GOES 3-hour previews
    tgoes = datetimerange(start, stop, timedelta(hours=3))
    print('downloading', len(tgoes), 'files to', odir)

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as exe:
        future_file = {exe.submit(dl_goes, t, odir, goessat, goesmode): t for t in tgoes}
        for f in concurrent.futures.as_completed(future_file):
            future_file[f]

    print()


def dl_goes(t: datetime, outdir: Path, goes: int, mode: str):
    """download GOES file for this time
    https://www.ncdc.noaa.gov/gibbs/image/GOE-13/IR/2017-08-21-06
    """
    STEM = 'https://www.ncdc.noaa.gov/gibbs/image/GOE-'
    outdir = Path(outdir).expanduser()

    dgoes = f'{t.year}-{t.month:02d}-{t.day:02d}-{t.hour:02d}'

    fn = outdir / f"goes{goes:d}-{mode}-{dgoes}.jpg"

    if fn.is_file():  # no clobber
        return

    url = (f'{STEM}{goes}/{mode}/' + dgoes)

    print(fn, end='\r')
    urllib.request.urlretrieve(url, fn)
