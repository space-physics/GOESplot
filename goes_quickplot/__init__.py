from datetime import datetime, timedelta
import urllib.request
import imageio
from pathlib import Path

def wld2mesh(fn:Path, nxy:tuple) -> np.ndarray:
    """converts .wld to lat/lon mesh for Cartopy/Matplotlib plots
    assumes the .wld file is EPSG:4326 coordinates (WGS84)
    """
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


def loadgoes(fn:Path):
    """
    loads and modifies GOES image for plotting
    """

    img = imageio.imread(str(fn))

    if downsample is not None:
        img = skimage.transform.resize(img, (img.shape[0], img.shape[1]),
                                   mode='constant',cval=255,
                                    preserve_range=True).astype(img.dtype)
    # make transparent (arbitrary)
    img[...,-1] = 128

    mask = img[...,:3].all(axis=2) == 0
    img[mask,:3] = 255  # make no signal be white

    return img
