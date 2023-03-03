from time import time
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cmaps
import os
from cartopy.feature import NaturalEarthFeature

from wrf import (getvar, interplevel, to_np, latlon_coords, get_cartopy,
                 cartopy_xlim, cartopy_ylim,ALL_TIMES,smooth2d,geo_bounds)


###############读取数据########################
filename = f'D:\python_data\wrfout_d01_2022-05-09_12'
wrfin = Dataset(filename)

savename = 'hgt'                                        # savename 保存路径文价夹名字
if not os.path.exists(savename):
    os.mkdir(savename)
##############计算############################
p = getvar(wrfin, "pressure",timeidx= ALL_TIMES)
z = getvar(wrfin, "z",timeidx= ALL_TIMES)
ua = getvar(wrfin, "ua", units="m s-1",timeidx=ALL_TIMES)
va = getvar(wrfin, "va", units="m s-1",timeidx=ALL_TIMES)
wspd_wdir = getvar(wrfin, "uvmet_wspd_wdir", units="m s-1",timeidx=ALL_TIMES)[0]
print('数据提取完成')

##############################################
# Interpolate geopotential height, u, and v winds to N hPa
N = 500   #插值的气压
hgt = interplevel(z, p, N)
u = interplevel(ua, p, N)
v = interplevel(va, p, N)
wspd = interplevel(wspd_wdir, p, N)
print('数据插值完成')

#平滑
smooth_hgt = smooth2d(hgt, 3, cenweight=4)
##############################################

def draw_barb(ax,u,v):      ###风场
    nd = 7
    lats, lons = latlon_coords(u)
    ax.barbs(to_np(lons[::nd,::nd]), 
            to_np(lats[::nd,::nd]),
            to_np(u[::nd, ::nd]), 
            to_np(v[::nd, ::nd]),
            transform=ccrs.PlateCarree(), 
            color = '#1382f1',
            length= 5 )

def replace(title):       ###储存路径格式化
    title = title.replace('-','_')
    return title.replace(':','_')
####设置经纬度#####################################
latmin= geo_bounds(wrfin = wrfin).bottom_left.lat
latmax= geo_bounds(wrfin = wrfin).top_right.lat
lonmin= geo_bounds(wrfin = wrfin).bottom_left.lon
lonmax= geo_bounds(wrfin = wrfin).top_right.lon
xloc = np.linspace(int(lonmin), int(lonmax), 4)
yloc = np.linspace(int(latmin), int(latmax), 4)
wrfin.close()
##############################################
# Plot the data
# The `get_cartopy` wrf function will automatically find and use the
# intended map projection for this dataset
lats, lons = latlon_coords(p)
cart_proj = get_cartopy(p)
wspdlevels = np.arange(20,36.2,2)
hgtlevels = np.arange(568,592,2)

for ntime in range(u.shape[0]):
    times = np.datetime_as_string((smooth_hgt[ntime,:,:]["Time"].values + np.timedelta64(8,'h')).astype('datetime64[s]'))
    print(f'{times}')
    fig = plt.figure(figsize=(12, 12))
    ax = plt.axes(projection=cart_proj)

    # Add features to the projection
    states = NaturalEarthFeature(category="cultural",
                                    scale="50m",
                                    facecolor="none",
                                    name="admin_1_states_provinces")

    ax.add_feature(states, linewidth=0.5, edgecolor="black")
    ax.coastlines('50m', linewidth=0.8)

    con = plt.contour(   to_np(lons),
                    to_np(lats),
                    to_np(smooth_hgt[ntime,:,:]/10),
                    levels = hgtlevels,
                    colors = 'k',
                    transform=ccrs.PlateCarree())
    plt.clabel(con)
    # Add filled dew point temperature contours
    plt.contourf(   to_np(lons),
                    to_np(lats),
                    to_np(wspd[ntime,:,:]),
                    levels=wspdlevels,
                    cmap = cmaps.MPL_YlGnBu,
                    transform=ccrs.PlateCarree())
    # Add a colorbar
    cbar = plt.colorbar(ax=ax,
                        ticks= wspdlevels,
                        extend = 'both',
                        drawedges=True,
                        extendrect=True,
                        shrink=0.5,
                        aspect=30)
    #Draw barb
    draw_barb(ax,u[ntime],v[ntime])

    # Draw gridlines
    gl = ax.gridlines(crs=ccrs.PlateCarree(),
                        xlocs=xloc, 
                        ylocs=yloc, 
                        draw_labels=True,
                        dms=False,
                        x_inline=False,
                        y_inline=False,
                        linewidth=1,
                        color="k",
                        alpha=0.25)

    # Manipulate latitude and longitude gridline numbers and spacing
    gl.top_labels = False
    gl.right_labels = False
    gl.xpadding = 15   #刻度标签和图的位置
    gl.ypadding = 10
    gl.xlabel_style = {"rotation": 0, "size": 15 }
    gl.ylabel_style = {"rotation": 0, "size": 15}
    # gl.xlines = False  #是否打开经纬度网格
    # gl.ylines = False


    # 增加珠海的位置
    plt.scatter([113.34], [22.17], s=35, c='r',transform=ccrs.PlateCarree())

    plt.title('(a)',loc='left',y=1.01, size=15)
    plt.savefig(f'{savename}\hgt_{replace(times)}',dpi=300)
    plt.close()


    