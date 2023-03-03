
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
import cartopy.crs as crs
from cartopy.feature import NaturalEarthFeature
import cmaps
from wrf import (getvar, interplevel, to_np, latlon_coords, get_cartopy,
                 cartopy_xlim, cartopy_ylim,ALL_TIMES)

###############读取数据##########################################################################
filename =r'wrfout_d02_2022-05-09_21:00:00'   ######wrfout路径#########
ncfile = Dataset(filename)
flag = 1                 #是否循环出图[0,1]，默认1，循环出图
##############计算##############################################################################
time_inv = getvar(ncfile, "times",timeidx= ALL_TIMES)
time_inv = 2+int((time_inv[2] - time_inv[1]).values.astype('timedelta64[h]')/np.timedelta64(1, 'h')) #wrfout时间间隔,小时为单位

ter= getvar(ncfile, 'ter', timeidx=-1)  
print(ter.shape)
U10, V10 = getvar(ncfile, 'U10', timeidx=ALL_TIMES), getvar(ncfile, 'V10', timeidx=ALL_TIMES)  # 提取10m风速

######数据重新采样##############################################################################   
def resample(data,time_inv):
    if time_inv <=3 :
        k = 3 // time_inv
        data_3h = data[::k]
    else:
        print('wrfout输出时间间隔大于3小时')
    return data_3h    

def replace(title):       ###储存路径格式化
    title = title.replace('-','_')
    return title.replace(':','_')


################################################################################################
def draw_contourf(ax,var,level,cmap,title):  ####填色图
    lats, lons = latlon_coords(var)
    extents = list(np.array([var.coords['XLONG'].min(),var.coords['XLONG'].max(),var.coords['XLAT'].min(),var.coords['XLAT'].max()],dtype=np.int16))
    # print(extents)
    contours = plt.contourf(to_np(lons), to_np(lats), to_np(var),
                             levels = level,cmap=cmap,
                             transform=crs.PlateCarree())
    

    gl=ax.gridlines(ylocs=np.arange(extents[2], extents[3], 1), xlocs=np.arange(extents[0], extents[1], 3),x_inline=False, y_inline=False,
                            draw_labels=True,linestyle="--", linewidth=1, alpha=0.35)
    gl.top_labels = False
    gl.right_labels = False
    gl.rotate_labels = False
    #ax.set_title(title)
    return contours

def draw_barb(ax,u,v):      ###风场
    nd = 8
    lats, lons = latlon_coords(u)
    ax.barbs(to_np(lons[::nd,::nd]), to_np(lats[::nd,::nd]),
          to_np(u[::nd, ::nd]), to_np(v[::nd, ::nd]),
          transform=crs.PlateCarree(), length=4)


##############################################################
proj = get_cartopy(ter)              #####地图投影
# level = np.arange(0,25,5)              
levels =np.arange(-100,1000,100)#####色标范围
car = 'unit:'+ter.attrs['units']     #####色标单位
figname ='terrain' #####保存文件名字
####画图################################
for i in range(U10.shape[0]-1):
    fig = plt.figure(figsize=(6,6))
    time_start = str(U10.Time.values[i])[:16]
    title = f'{time_start}'
    print(title)
    ax = fig.add_subplot(1,1,1,projection=proj)
    cs=draw_contourf(ax,ter,levels,cmaps.MPL_terrain,title)
    draw_barb(ax,U10[i],V10[i])
    plt.subplots_adjust(wspace=0.12, hspace=0.02)
    cb = fig.colorbar(cs,orientation='horizontal',shrink=0.8)  # 方向
    cb.ax.tick_params(labelsize=10)  # 设置色标刻度字体大小
    cb.set_label(car,fontsize = 10)
    #fig.savefig(f'{figname}/{replace(title)}',dpi=300)
    fig.savefig(f'{figname}/{replace(title)}.png',dpi=300)
    #fig.close()
##############################################################################################
print('!'*20)
print('!'*5+'successful','!'*4)
print('!'*20)




