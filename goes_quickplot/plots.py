from pathlib import Path
from matplotlib.pyplot import figure
import cartopy
import numpy as np

# WGS84 is the default, just calling it out explicity so somene doesn't wonder.
GREF = cartopy.crs.PlateCarree()#globe=cartopy.crs.Globe(ellipse='WGS84')

def plotgoes(img:np.ndarray, fn:Path, lat:list, lon:list, fignum:int=None):
    """plot GOES data on map coordinates"""
    #hsv = rgb_to_hsv(d)

    if fignum:
        figure(fignum).clf()

    ax = figure(fignum, figsize=(15,10)).gca(projection=GREF)

    ax.set_title(fn.name)

    ax.add_feature(cartopy.feature.COASTLINE, linewidth=0.5, linestyle=':')
    ax.add_feature(cartopy.feature.NaturalEarthFeature('cultural', 'admin_1_states_provinces',
                                  '50m',
                                  linestyle=':',linewidth=0.5, edgecolor='grey', facecolor='none'))

    labels = [[-117.1625, 32.715, 'San Diego'],
              [-87.9073, 41.9742, 'KORD' ],
              [-90.3755, 38.7503,'KSUS'],
              [-97.040443,32.897480,'KDFW'],
              [-104.6731667,39.8616667,'KDEN'],
              [ -111.1502604,45.7772358,'KBZN'],
              [ -106.6082622,35.0389316,'KABQ']
              ]
    if 0:
      for l in labels:
        ax.plot(l[0], l[1], 'bo', markersize=7, transform=GREF)
        ax.annotate(l[2], xy = (l[0], l[1]), xytext = (3, 3), textcoords = 'offset points')

    ax.imshow(img, origin='upper',
              extent=[lon[0],lon[-1],lat[0],lat[-1]],
              transform=GREF)