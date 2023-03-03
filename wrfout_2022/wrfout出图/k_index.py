########################
#########################
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cmaps
import os
from cartopy.feature import NaturalEarthFeature
from metpy.calc import divergence 
from metpy.units import units
from metpy.calc import k_index
from wrf import (getvar, interplevel, to_np, latlon_coords, get_cartopy,
                 cartopy_xlim, cartopy_ylim,ALL_TIMES)
import warnings
warnings.filterwarnings("ignore")

###############读取数据########################
filename = f'D:\python_data\wrfout_d01_2022-05-09_12'
ncfile = Dataset(filename)

savename = 'k_index'                                        # savename 保存路径文价夹名字
if not os.path.exists(savename):
    os.mkdir(savename)
##############计算################################
p = getvar(ncfile, "pressure",timeidx= ALL_TIMES)
t = getvar(ncfile, "temp",timeidx= ALL_TIMES)
dewt = getvar(ncfile, "td",units='K',timeidx= ALL_TIMES)

p = p.metpy.quantify()
t=t.metpy.quantify()
dewt = dewt.metpy.quantify()
##################################################
print('数据提取完成')
ncfile.close()
##################################################
def replace(title):       ###储存路径格式化
    title = title.replace('-','_')
    return title.replace(':','_')
####设置经纬度#####################################
latmin= p["XLAT"].min().values
latmax= p["XLAT"].max().values
lonmin= p["XLONG"].min().values
lonmax= p["XLONG"].max().values
xloc = np.linspace(int(lonmin), int(lonmax), 5)
yloc = np.linspace(int(latmin), int(latmax), 5)
##############################################
# Plot the data
# The `get_cartopy` wrf function will automatically find and use the
# intended map projection for this dataset
lats, lons = latlon_coords(p)
cart_proj = get_cartopy(p)
klevels = np.arange(-50,50.2,5)
k_ind = np.zeros_like(p[:,1,:,:])

for ntime in range(p.shape[0]):
    times = np.datetime_as_string((p[ntime]["Time"].values + np.timedelta64(8,'h')).astype('datetime64[s]'))
    print(f'{times}')
    #cal k_index
    k_ind = np.array(k_index(p[ntime,:,:,:],t[ntime,:,:,:],dewt[ntime,:,:,:]))

    fig = plt.figure(figsize=(12, 12))
    ax = plt.axes(projection=cart_proj)

    # Add features to the projection
    states = NaturalEarthFeature(category="cultural",
                                    scale="50m",
                                    facecolor="none",
                                    name="admin_1_states_provinces")

    ax.add_feature(states, linewidth=0.5, edgecolor="black")
    ax.coastlines('50m', linewidth=0.8)

    # Add filled dew point temperature contours
    plt.contourf(   to_np(lons),
                    to_np(lats),
                    k_ind,
                    levels=klevels,
                    cmap = cmaps.cmocean_thermal_r,
                    transform=ccrs.PlateCarree())

    # Add a colorbar
    cbar = plt.colorbar(ax=ax,
                        extend = 'both',
                        drawedges=True,
                        ticks= klevels,
                        extendrect=True,
                        shrink=0.5,
                        aspect=30)
                        #                       
    
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
    gl.xlines = False  #是否打开经纬度网格
    gl.ylines = False

    # 增加珠海的位置
    plt.scatter([113.34], [22.17], s=35, c='r',transform=ccrs.PlateCarree())

    plt.title('(c)',loc='left',y=1.01, size=15)
    plt.savefig(f'{savename}\k_index_{replace(times)}',dpi=300)
    plt.close()


    