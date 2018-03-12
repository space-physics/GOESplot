from datetime import datetime, timedelta
import imageio
import numpy as np
from pathlib import Path
from typing import Tuple
import xarray
from numpy.ma import masked_where # pcolormesh doesn't like NaN
try:
    import netCDF4
except ImportError:
    netCDF4 = None


stem = 'GOES_EAST_' # FIXME: make auto per satellite


def wld2mesh(wdir:Path, inst:str, nxy:tuple) -> Tuple[np.ndarray, np.ndarray]:
    """converts .wld to lat/lon mesh for Cartopy/Matplotlib plots
    assumes the .wld file is EPSG:4326 coordinates (WGS84)
    """
    wdir = Path(wdir).expanduser()

    fn = wdir / (stem + inst + '.wld')

    wld = np.loadtxt(fn)

    ny, nx = nxy

    lat = np.arange(wld[5]-wld[3] + ny*wld[3], wld[5]-wld[3], -wld[3])
    lon = np.arange(wld[4], wld[4]+nx*wld[0], wld[0])

    return lat, lon


def datetimerange(start:datetime, stop:datetime, step:timedelta) -> list:
    return [start + i*step for i in range((stop-start) // step)]


def loadgoes_preview(fn:Path, wld:Path) -> np.ndarray:
    """
    loads and modifies GOES image
    """

    img = imageio.imread(fn)

    assert img.ndim==3 and img.shape[2] == 3,'unexpected GOES image format'

    lat, lon = wld2mesh(wld, fn.stem.split('-')[1].upper(), img.shape[:2])

    img = xarray.DataArray(img, dims=['lon','lat'],
                           coords={'lon':lon, 'lat':lat})

    return img


def loadgoes_hires(fn:Path) -> np.ndarray:
    """
    loads and modifies GOES data
    """
    if netCDF4 is None:
        raise ImportError('netCDF4 needed for hires data.   pip install netcdf4')

    with netCDF4.Dataset(fn,'r') as f:
        t = datetime.utcfromtimestamp(f['time'][:])
        lon = np.flipud(f['lon'][:])
        lat = np.flipud(f['lat'][:])
#        lon = f['lon'][:]
#        lat = f['lat'][:]

        mask = lon>180

        img = xarray.DataArray(np.flipud(np.squeeze(f['data'])),
        #img = xarray.DataArray(np.squeeze(f['data']),
                               dims=['x','y'],
                               coords={'lon':(['x','y'], lon),
                                       'lat':(['x','y'], lat)},
                               attrs={'time':t, 'mask':mask})

    return img