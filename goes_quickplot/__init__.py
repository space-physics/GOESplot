from datetime import datetime, timedelta
import urllib.request
import imageio
from pathlib import Path

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


