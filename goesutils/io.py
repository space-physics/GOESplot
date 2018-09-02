from datetime import datetime, timedelta
import imageio
import numpy as np
from pathlib import Path
from typing import Tuple, Optional, List
import xarray
from time import sleep
from dateutil.parser import parse
import concurrent.futures
import requests
import ftplib
import logging
try:
    import netCDF4
except ImportError:
    netCDF4 = None

STEM = 'GOES_EAST_'  # FIXME: make auto per satellite

R = Path(__file__).resolve().parents[1] / 'data'


def datetimerange(start: datetime, stop: datetime, step: timedelta) -> List[datetime]:
    """
    generates range of datetime start,stop,step just like range() for datetime
    """
    return [start + i*step for i in range((stop-start) // step)]


def wld2mesh(wdir: Optional[Path], inst: str, nxy: tuple) -> Tuple[np.ndarray, np.ndarray]:
    """converts .wld to lat/lon mesh for Cartopy/Matplotlib plots
    assumes the .wld file is EPSG:4326 coordinates (WGS84)
    """
    wdir = R if wdir is None else Path(wdir).expanduser()

    fn = wdir / (STEM + inst + '.wld')

    wld = np.loadtxt(fn)

    ny, nx = nxy

    lat = np.arange(wld[5]-wld[3] + ny*wld[3], wld[5]-wld[3], -wld[3])
    lon = np.arange(wld[4], wld[4]+nx*wld[0], wld[0])

    return lat, lon


def load(fn: Path, downsample: int=None, wld: Path=None) -> xarray.DataArray:
    """ for now this is single file at a time, but is trivial to extend to multi-files"""
    if fn.suffix == '.jpg':
        img = loadpreview(fn, wld)
    elif fn.suffix == '.nc':
        img = loadhires(fn, downsample)
    else:
        raise ValueError(f'unknown data type {fn}')

    img.attrs['filename'] = fn.name

    return img


def loadpreview(fn: Path, wld: Path=None) -> xarray.DataArray:
    """
    loads and modifies GOES image
    """

    img = imageio.imread(fn)

    assert img.ndim == 3 and img.shape[2] == 3, 'unexpected GOES image format'

    lat, lon = wld2mesh(wld, fn.stem.split('-')[1].upper(), img.shape[:2])

    img = xarray.DataArray(img, dims=['lon', 'lat', 'color'],
                           coords={'lon': lon, 'lat': lat, 'color': ['R', 'G', 'B']})

    return img


def loadhires(fn: Path, downsample: int=None) -> xarray.DataArray:
    """
    loads and modifies GOES data
    """
    if netCDF4 is None:
        raise ImportError('netCDF4 needed for hires data.   pip install netcdf4')

    with netCDF4.Dataset(fn, 'r') as f:
        t = datetime.utcfromtimestamp(f['time'][:])
        lon = np.flipud(f['lon'][::downsample, ::downsample])
        lat = np.flipud(f['lat'][::downsample, ::downsample])

        mask = lon > 180

        img = xarray.DataArray(np.flipud(f['data'][0, ::downsample, ::downsample]),
                               dims=['x', 'y'],
                               coords={'lon': (['x', 'y'], lon),
                                       'lat': (['x', 'y'], lat)},
                               attrs={'time': t, 'mask': mask})

    return img


def get_hires(host: str, ftpdir: str, flist: List[str],
              odir: Path, clobber: bool=False):
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


def parse_email(txtfn: Path) -> Tuple[str, List[str]]:
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
    url = (f'{STEM}{goes}/{mode}/' + dgoes)

    urlretrieve(url, fn)


def urlretrieve(url: str, fn: Path, overwrite: bool=False):
    """
    the way urlretrieve should be with timeout
    """
    if not overwrite and fn.is_file() and fn.stat().st_size > 10000:
        print(f'SKIPPED {fn}')
        return
# %% prepare to download
    R = requests.head(url, allow_redirects=True, timeout=10)
    if R.status_code != 200:
        logging.error(f'{url} not found. \n HTTP ERROR {R.status_code}')
        return
# %% download
    print(f'downloading {int(R.headers["Content-Length"])//1000000} MBytes:  {fn.name}')
    R = requests.get(url, allow_redirects=True, timeout=10)
    with fn.open('wb') as f:
        f.write(R.content)
