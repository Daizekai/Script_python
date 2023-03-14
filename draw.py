
from turtle import position
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs  as ccrs
import cartopy.feature as cfeature

#########需要修改的量################################
title = '初始场'

###################################################
hgt = np.load('Output\h.npy')[1,...]
u_wind= np.load('Output\\u.npy')[1,...]
v_wind= np.load('Output\\v.npy')[1,...]

###初始场路径##########################
# path = r'C:\Users\dzk\Desktop\实习报告\Barotropic_primitive_equation_model\Input'
# hgt = np.fromfile(path+'\za.dat',sep = ' ').reshape((16,20),order='c')
# u_wind= np.fromfile(path+'\\ua.dat',sep = ' ').reshape((16,20),order='c')
# v_wind= np.fromfile(path+'\\va.dat',sep = ' ').reshape((16,20),order='c')


lon,lat = np.meshgrid(np.arange(85,155,3.5),np.arange(32.5,72.5,2.5))

fig = plt.figure(figsize=[8,6])
maps=ccrs.PlateCarree(central_longitude=105)
ax = fig.add_subplot(1,1,1, projection=maps)


plt.tick_params(labelsize=12)   #设置坐标轴字体大小
plt.rcParams['font.sans-serif']='SimHei'    #设置默认字体

ax.set_extent([85, 151,32.5, 67])
sh=ax.contour(lon,lat,hgt,np.arange(5100.,5900.,50.),colors='k',extend='both',transform=ccrs.PlateCarree())#cmap = 'RdBu_r')
sf=ax.contourf(sh,transform=ccrs.PlateCarree(),cmap = 'RdBu_r' )
ax.quiver(lon[1:-1,1:-1],lat[1:-1,1:-1],u_wind[1:-1,1:-1],v_wind[1:-1,1:-1],transform=ccrs.PlateCarree())
plt.clabel(sh, inline=True, fontsize=10)
ax.add_feature(cfeature.COASTLINE,lw=0.5) 
gl=ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False, color='gray', alpha=0.3, linestyle='--')
gl.top_labels = False
gl.right_labels = False
gl.rotate_labels = False
plt.colorbar(sf,shrink=0.8)
ax.set_title(title)
plt.savefig('Output\\'+title)
plt.show()
