from matplotlib.pyplot import figure
import cartopy
import xarray
import numpy as np
from numpy.ma import masked_where

PC = cartopy.crs.PlateCarree()
GS = cartopy.crs.Geostationary(-75.)
labels = [[-117.1625, 32.715, 'San Diego'],
          [-87.9073, 41.9742, 'KORD'],
          [-90.3755, 38.7503, 'KSUS'],
          [-97.040443, 32.897480, 'KDFW'],
          [-104.6731667, 39.8616667, 'KDEN'],
          [-111.1502604, 45.7772358, 'KBZN'],
          [-106.6082622, 35.0389316, 'KABQ']
          ]


def plotgoes(img: xarray.DataArray, verbose: bool=False):
    """plot GOES data on map coordinates
    https://stackoverflow.com/questions/36228363/dealing-with-masked-coordinate-arrays-in-pcolormesh?rq=1
    """
    print(f'generating plot from {img.filename}')

    fg = figure(1, figsize=(15, 10))
    fg.clf()

    ax = fg.gca(projection=GS)

    ax.set_title(img.filename)

    ax.add_feature(cartopy.feature.COASTLINE, linewidth=0.5, linestyle=':')
    ax.add_feature(cartopy.feature.NaturalEarthFeature('cultural', 'admin_1_states_provinces',
                                                       '50m',
                                                       linestyle=':', linewidth=0.5,
                                                       edgecolor='grey', facecolor='none'))

    lat = masked_where(img.mask, img.lat)
    lon = masked_where(img.mask, img.lon)
    im = masked_where(img.mask, img)

    h = ax.pcolor(lon, lat, im, transform=PC)
    fg.colorbar(h, ax=ax)

    if False:
        for l in labels:
            ax.plot(l[0], l[1], 'bo', markersize=7, transform=PC)
            # only for rectangular systems
            ax.annotate(l[2], xy=(l[0], l[1]), xytext=(3, 3), textcoords='offset points', transform=PC)

        # only for rectangular systems
        ax.set_xticks(range(-140, -20, 20))
        ax.set_yticks(range(0, 60, 10))

    if verbose and lon.ndim == 2:
        plotlatlon(im, lat, lon, img.filename)


def plotlatlon(img: np.ndarray, lat: np.ndarray, lon: np.ndarray, fn: str):
    """ Lat / long grid plots """

    PTYPE = 'contour'

    fg = figure(figsize=(12, 8))

    ax = fg.subplots(1, 2)
    ax[0].set_title('latitude')
    ax[1].set_title('longitude')

    if PTYPE == 'pcolor':
        h = ax[0].pcolormesh(lat)
        fg.colorbar(h, ax=ax[0])

        h = ax[1].pcolormesh(lon)
        fg.colorbar(h, ax=ax[1])
    elif PTYPE == 'contour':
        h = ax[0].contour(lat)
        ax[0].clabel(h, fmt='%0.1f')

        h = ax[1].contour(lon)
        ax[1].clabel(h, fmt='%0.1f')

    fg.suptitle(fn)
