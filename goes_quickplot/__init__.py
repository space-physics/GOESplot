from datetime import datetime, timedelta
import urllib.request
import imageio
import numpy as np
from pathlib import Path
from typing import Tuple

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


def get_goes(t:datetime, outdir:Path, goes:int, mode:str):
    """download GOES file for this time
    https://www.ncdc.noaa.gov/gibbs/image/GOE-13/IR/2017-08-21-06
    """
    STEM = 'https://www.ncdc.noaa.gov/gibbs/image/GOE-'
    outdir = Path(outdir).expanduser()

    dgoes = f'{t.year}-{t.month:02d}-{t.day:02d}-{t.hour:02d}'

    fn = outdir / f"goes{goes:d}-{mode}-{dgoes}.jpg"

    if fn.is_file(): # no clobber
        return

    url = (f'{STEM}{goes}/{mode}/' + dgoes)

    print(fn, end='\r')
    urllib.request.urlretrieve(url, fn)


def loadgoes(fn:Path) -> np.ndarray:
    """
    loads and modifies GOES image for plotting
    """

    img = imageio.imread(str(fn))

    assert img.ndim==3 and img.shape[2] == 3,'unexpected GOES image format'

    return img
