
from fileinput import filename
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from numpy import dot
from numpy.linalg import  inv,lstsq
import matplotlib as mpl
from scipy.interpolate import interp2d
from metpy.calc import smooth_gaussian,smooth_n_point
from metpy.interpolate import inverse_distance_to_grid

filename    = r'./obsdata.txt'
col = r'./station.txt'
cols =pd.read_table(col)
#cols.set_index("区站号", inplace = True)
main_data = pd.read_csv(filename,sep='\s+',header=None)
main_data.columns = ["站号","年份","月份","日","时次","气压","海平面气压","最高气压","最低气压","最大风速","极大风速",
                    "极大风速的风向(角度) ","2分钟平均风向(角度)","2分钟平均风速 ","最大风速的风向(角度)","温度/气温",
                    "最高气温","最低气温","相对湿度","水汽压","最小相对湿度 ","降水量","水平能见度(人工)","现在天气",
                    "总云量","云量(低云或中云)","云底高度","低云量 ","风力","体感温度"]

# %% 提取三省站点数据
province=["江苏","浙江","上海"]
stn_data=pd.concat([cols[cols['省份']==i] for i in province])
stn=stn_data["区站号"]
lons,lats=stn_data["经度（度分）"]/100,stn_data["纬度（度分）"]/100
#%% 提取气象数据
main_data = main_data[["站号","年份","月份","日","时次","温度/气温"]]
a=main_data.set_index(["站号","年份","月份","日","时次"])
b=[a.loc[(i,2021,3,28,0)] for i in stn]
#%% 画图

lons = np.around(lons, 1)
lats = np.around(lats, 1)
lon_grid = np.arange(lons.min()-0.1, lons.max()+1, 0.05) 
lat_grid = np.arange(lats.min()-0.1, lats.max()+1, 0.05) 
lon_gridmesh, lat_gridmesh = np.meshgrid(lon_grid, lat_grid)
lt_grid = inverse_distance_to_grid(lons,lats,np.array(b),lon_gridmesh,lat_gridmesh,r=4,min_neighbors=5,kind = 'cressman' )
llt = smooth_n_point(lt_grid, n=9, passes=1)


#%%
fig = plt.figure(figsize=(8,6))
font = {'family': 'Time New Roman',
        'style': 'italic',   # 修改倾斜程度
        # 'weight': 'normal',  # 修改粗细
        'color': 'black',  # 颜色
        'size': 16,  # 字体大小
        }  # 设置xlabel、title、text等字体设置

#%%
ax = fig.add_subplot(1, 1, 1, projection=ccrs.LambertCylindrical())
sh=ax.contourf(lon_gridmesh, lat_gridmesh ,llt,transform=ccrs.LambertCylindrical(),cmap='bwr')
sh1 = ax.contour(lon_gridmesh, lat_gridmesh ,llt,10,colors="k", transform=ccrs.LambertCylindrical())
 #设置范围
ax.spines['left'].set_linewidth(5)
ax.spines['right'].set_linewidth(5)
ax.spines['top'].set_linewidth(5)
ax.spines['bottom'].set_linewidth(5) 
ax.set_extent([115,125,25,38], crs=ccrs.LambertCylindrical())
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.set_xticks(np.arange(115,125+1,2.5)) # np.arange(74.0, 134.0, 0.1) 
ax.set_yticks(np.arange(25,40+1,2.5))#(18.0, 54.0, 0.1) 
ax.tick_params(labelsize=8)
    # 等值线上标字
ax.clabel(sh1, fmt='%2.1f', fontsize=15, colors="k")
ax.set_title('changsanjiao',fontdict=font)

  
#position=fig.add_axes([0.15, 0.05, 0.7, 0.05])#位置[左,下,右,上]
cbar=fig.colorbar(sh)#,cax=position,orientation='horizontal')#方向
plt.show()
fig.savefig(r'./grid.png')

