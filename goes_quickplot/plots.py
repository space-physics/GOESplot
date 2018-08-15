from pathlib import Path
from matplotlib.pyplot import figure
import cartopy
import xarray
# import skimage.transform
# import numpy as np
from numpy.ma import masked_where

# WGS84 is the default, just calling it out explicity so somene doesn't wonder.
GREF = cartopy.crs.PlateCarree()  # globe=cartopy.crs.Globe(ellipse='WGS84')


def plotgoes(img: xarray.DataArray, fn: Path, downsample: int=None, verbose: bool=False):
    """plot GOES data on map coordinates
    https://stackoverflow.com/questions/36228363/dealing-with-masked-coordinate-arrays-in-pcolormesh?rq=1
    """
    PTYPE = 'contour'

    # hsv = rgb_to_hsv(d)

    fg = figure(1, figsize=(15, 10))
    fg.clf()

    ax = fg.gca(projection=GREF)

    ax.set_title(fn.name)

    ax.add_feature(cartopy.feature.COASTLINE, linewidth=0.5, linestyle=':')
    ax.add_feature(cartopy.feature.NaturalEarthFeature('cultural', 'admin_1_states_provinces',
                                                       '50m',
                                                       linestyle=':', linewidth=0.5, edgecolor='grey', facecolor='none'))

    labels = [[-117.1625, 32.715, 'San Diego'],
              [-87.9073, 41.9742, 'KORD'],
              [-90.3755, 38.7503, 'KSUS'],
              [-97.040443, 32.897480, 'KDFW'],
              [-104.6731667, 39.8616667, 'KDEN'],
              [-111.1502604, 45.7772358, 'KBZN'],
              [-106.6082622, 35.0389316, 'KABQ']
              ]
    if 0:
        for l in labels:
            ax.plot(l[0], l[1], 'bo', markersize=7, transform=GREF)
            ax.annotate(l[2], xy=(l[0], l[1]), xytext=(3, 3), textcoords='offset points')

    lat = img.lat
    lon = img.lon

    if downsample:
        #        img = skimage.transform.resize(img.values,
        #                                (img.shape[0]//downsample, img.shape[1]//downsample),
        #                                 mode='constant',cval=255,
        #                                 preserve_range=True).astype(img.dtype)
        img = img[::downsample, ::downsample]
        lon = lon[::downsample, ::downsample]
        lat = lat[::downsample, ::downsample]
        mask = img.attrs['mask'][::downsample, ::downsample]

    h = ax.pcolor(masked_where(mask, lon),
                  masked_where(mask, lat),
                  masked_where(mask, img),
                  transform=GREF)
    fg.colorbar(h, ax=ax)
# %%
    if lon.ndim == 2 and verbose:
        fg = figure(2, figsize=(12, 8))
        fg.clf()

        ax = fg.subplots(1, 2)
        ax[0].set_title('latitude')
        ax[1].set_title('longitude')

        if PTYPE == 'pcolor':
            h = ax[0].pcolormesh(masked_where(mask, lat))
            fg.colorbar(h, ax=ax[0])
            h = ax[1].pcolormesh(masked_where(mask, lon))
            fg.colorbar(h, ax=ax[1])
        elif PTYPE == 'contour':
            h = ax[0].contour(masked_where(mask, lat))
            ax[0].clabel(h, fmt='%0.1f')
            h = ax[1].contour(masked_where(mask, lon))
            ax[1].clabel(h, fmt='%0.1f')

        fg.suptitle(fn)
