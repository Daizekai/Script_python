"""
NCL_WRF_zoom_1_2.py
===================
This script illustrates the following concepts:
    - Plotting WRF data on native grid
    - Subsetting data to 'zoom in' on an area
    - Plotting data using wrf python functions
    - Following best practices when choosing a colormap

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/wrf_zoom_1.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/wrf_zoom_1_2_lg.png
"""

from time import time
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
from cartopy.feature import NaturalEarthFeature
import os
import cmaps
from wrf import (getvar, to_np, latlon_coords, get_cartopy,ALL_TIMES,extract_times)
from cartopy.mpl.ticker import (LongitudeFormatter, LatitudeFormatter,
                                LatitudeLocator, LongitudeLocator)




# Read in the data
filename = r"D:\python_data\wrfout_d01_2022-05-09_12"
wrfin = Dataset(filename)
# savename = 'precip'                                        # savename 保存路径文价夹名字
# if not os.path.exists(savename):
#     os.mkdir(savename) 

# read data
RAINC = getvar(wrfin,'RAINC',timeidx=ALL_TIMES)    #
RAINNC = getvar(wrfin,'RAINNC',timeidx=ALL_TIMES)
RAIN_SUM = RAINC + RAINNC  

# Set attributes for creating plot titles later
we = getattr(wrfin, 'WEST-EAST_GRID_DIMENSION')
sn = getattr(wrfin, 'SOUTH-NORTH_GRID_DIMENSION')
lvl = getattr(wrfin, 'BOTTOM-TOP_GRID_DIMENSION')
dis = getattr(wrfin, 'DY') / 1000  # Divide by 1000 to go from m to km
phys = getattr(wrfin, 'MP_PHYSICS')
pbl = getattr(wrfin, 'BL_PBL_PHYSICS')
cu = getattr(wrfin, 'CU_PHYSICS')
s_date = getattr(wrfin, 'START_DATE')
str_format = "WE={}; SN={}; Levels={}; Dis={}km; Phys Opt={}; PBL Opt={}; Cu Opt={}"
sd_frmt = "Init: {}"
titles=getattr(wrfin, 'TITLE')
                                            
levels = [0, 0.1, 3, 10, 20, 50, 70, 120]      #####色标范围
colors = ['#FFFFFF', '#90EE90', '#008000', '#00BFFF', '#0000FF', '#FF00FF', '#800000']

lats, lons = latlon_coords(RAINC)
cart_proj = get_cartopy(RAINC)

##设置显示的经纬度
# print("lat.min,lat.max,lon.min,lon.max")
print([RAINC["XLAT"].min(),RAINC["XLAT"].max(),RAINC["XLONG"].min(),RAINC["XLONG"].max()])
latmin= input("latmin:")
latmax= input("latmax:")
lonmin= input("lonmin:")
lonmax= input("lonmax:")
xloc = np.linspace(int(lonmin), int(lonmax), 4)
yloc = np.linspace(int(latmin), int(latmax), 4)

 ###修改初始时间###
nt_str = 28            ###!!!!!!!!修改初始时间!!!!!!!!###
nt_end = nt_str+12
s_str = np.datetime_as_string((RAIN_SUM[nt_str,:,:]["Time"].values + np.timedelta64(8,'h')).astype('datetime64[s]')) #转换为BJT北京时间
s_end = np.datetime_as_string((RAIN_SUM[nt_end,:,:]["Time"].values + np.timedelta64(8,'h')).astype('datetime64[s]'))
print(type(s_str))
data = to_np(RAIN_SUM[nt_end,:,:]-RAIN_SUM[nt_str,:,:])

# Plot the data
# The `get_cartopy` wrf function will automatically find and use the
# intended map projection for this dataset
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
                data,
                levels=levels,
                colors=colors,
                transform=ccrs.PlateCarree())
# Add a colorbar
cbar = plt.colorbar(ax=ax,
                    orientation="horizontal",
                    ticks= levels,
                    drawedges=True,
                    extendrect=True,
                    pad=0.08,
                    shrink=0.75,
                    aspect=30)

# Format location of colorbar text to look like NCL version
cbar.ax.text(0.5,
            1.5,
            'Precipitation Tendency(mm)',
            horizontalalignment='center',
            verticalalignment='center',
            transform=cbar.ax.transAxes)
cbar.ax.tick_params(labelsize=15)
cbar.ax.get_xaxis().labelpad = -48

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

# 墨卡托投影下 ncl风格
# ax.set_xticks(np.arange(80, 141, 10))#指定要显示的经纬度                      
# ax.set_yticks(np.arange(10, 41, 10))                  
# ax.xaxis.set_major_formatter(LongitudeFormatter())#刻度格式转换为经纬度样式                       
# ax.yaxis.set_major_formatter(LatitudeFormatter())                        
# ax.tick_params(axis='both',which='major',labelsize=15,direction='out',length=15,width=1,pad=0.2,top=True,right=True)
# ax.xaxis.set_minor_locator(mticker.MultipleLocator(1))#刻度格式转换为经纬度样式                       
# ax.yaxis.set_minor_locator(mticker.MultipleLocator(1))  
# ax.tick_params(axis='both',which='minor',direction='out',length=5,width=1,top=True,right=True)
# ax.spines['geo'].set_linewidth(1.5)#调节边框粗细
# ax.grid(alpha=0.3)

# Add titles to the plot
plt.title("Zoomed in plot", loc='center', x=.13, y=1.1, size=15)
plt.title(sd_frmt.format(s_date), loc='right', y=1.1, size=10)

# Add lower text using attributes from the dataset
# fig.text(0.704, 0.93,sd_frmt.format(s_date), size=10)
fig.text(0.18, 0.90,f"(10CST)Precipitation Tendency from {s_str} to {s_end}(mm)", size=12)
# fig.text(0.75, 0.90,"mm", size=12)
fig.text(0.25, 0.1, titles, size=15)
fig.text(0.252,
        0.08,
        str_format.format(we, sn, lvl, dis, phys, pbl, cu),
        size=12)

def replace(title):       ###储存路径格式化
    title = title.replace('-','_')
    return title.replace(':','_')

fig.savefig(f'{replace(s_str)}',dpi=300)