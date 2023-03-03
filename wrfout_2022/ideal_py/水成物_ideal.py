"""
Created on June 9 23:28 2022

@author: xianyun
"""

# Example script to produce dbz plots for a WRF ideal-data run     ##参考ncl脚本
from fileinput import filename
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
from wrf import getvar, ALL_TIMES,extract_times
import cmaps
import os

#begin--------------------------------------------------------------#
# The WRF ARW input file.  
# This needs to have a ".nc" appended, so just do it.
# a = addfile("../wrfout_d01_2000-01-24_12:00:00.nc","r")
filename = r'C:\Users\dzk\Desktop\test10\delt1\wrfout_d01_0001_01_01_00_00_00'
ncfile = Dataset(filename)
savename = 'hydrometeor_delt1'                                                  # savename 保存路径文价夹名字
if not os.path.exists(savename):
    os.mkdir(savename) 
#------------------------------------------------------------------#
#------------------------------------------------------------------#
#Which times and how many time steps are in the data set?
times = extract_times(ncfile,timeidx=ALL_TIMES,do_xtime=True)      #get all times in the file
ntimes = times.shape[0]                                            #number of times in the file

#------------------------------------------------------------------#
#------------------------------------------------------------------#
def cal_cloudiness(QT):                                            #计算云量函数
    k,m,n = QT.shape                                               #获取垂直层,平面网格
    cloudiness = np.zeros((k,))
    for i in range(k):
        tmp = QT[i,...]
        tmp = tmp[QT[i,...]!=0]
        cloudiness[i] = tmp.shape[0]/(m*n)
    return cloudiness

#------------------------------------------------------------------#
#------------------------------------------------------------------#
cloudthres = 1.e-5   #阈值，判断是否有云
#------------------------------------------------------------------#
###高度
Z = getvar(ncfile,'z').to_numpy()[:,1,1]
###水成物
QC = getvar(ncfile,'QCLOUD',timeidx=ALL_TIMES).to_numpy()*1000     #convert g/kg
QR = getvar(ncfile,'QRAIN',timeidx=ALL_TIMES).to_numpy()*1000      #convert g/kg
QI = getvar(ncfile,'QICE',timeidx=ALL_TIMES).to_numpy()*1000       #convert g/kg
QS = getvar(ncfile,'QSNOW',timeidx=ALL_TIMES).to_numpy()*1000      #convert g/kg
QG = getvar(ncfile,'QGRAUP').to_numpy()   #三维？？？（40，41，41）
QT = QC+QR+QG
QT[QT<cloudthres] = 0.
###垂直风
W = getvar(ncfile,'W',timeidx=ALL_TIMES).to_numpy()
W = (W[:,:-1,:,:]+W[:,1:,:,:])/2                                   #插值为标量
#------------------------------------------------------------------#
#------------------------------------------------------------------#
#画图 云水+冰晶
_,l,n,m =  QC.shape
levels = np.arange(0,2.5,0.5)
x,z= np.meshgrid(range(m),Z/1000.)
for nt in range(ntimes):
    print(f"Working on time: {times[nt]}")
    fig = plt.figure(figsize=(9,8))
    ax = fig.add_subplot()
    # plt.rcParams['font.family'] = 'YaHei Consolas Hybrid'
    cl1=ax.contour(x[::3,::3],z[::3,::3],QC[nt,::3,20,::3],levels=levels,linewidths = 1.25,colors='b')
    plt.clabel(cl1 ,  fmt='%.2f',inline=True, fontsize=10)
    cl2=ax.contour(x[::3,::3],z[::3,::3],QI[nt,::3,20,::3],levels=levels,linewidths = 1.25,colors='k',linestyles = "dashdot")
    plt.clabel(cl2 , fmt='%.2f', inline=True, fontsize=10)
    sh=ax.contourf(x,z,W[nt,:,20,:],levels= np.arange(-15,35,4),cmap = cmaps.cmp_b2r)

    car = fig.colorbar(sh)
    car.ax.set_ylabel('velocity(m/s)',fontsize = 20)

    ax.set_xlabel('Times(min)',fontsize = 20)
    ax.set_ylabel('Height(km)',fontsize = 20)

    bwith = 2                                                      #画布边框粗细
    ax.spines['bottom'].set_linewidth(bwith)
    ax.spines['left'].set_linewidth(bwith)
    ax.spines['top'].set_linewidth(bwith)
    ax.spines['right'].set_linewidth(bwith)

    name = f'QQ_{times[nt]}min'
    ax.set_title(name,fontsize = 20)
    ax.tick_params(direction='out', length=8,labelsize=20)

    fig.savefig(f'{savename}/{name}.png',dpi=300)

#------------------------------------------------------------------#
#------------------------------------------------------------------#
# #雨水混合+雪
print(QG.shape)
print(QT.shape)
_,l,n,m =  QC.shape
x,z= np.meshgrid(range(m),Z/1000.)
for nt in range(ntimes):
    print(f"Working on time: {times[nt]}")
    fig = plt.figure(figsize=(9,8))
    ax = fig.add_subplot()
    # plt.rcParams['font.family'] = 'YaHei Consolas Hybrid'
    cl1=ax.contour(x[::3,::3],z[::3,::3],QR[nt,::3,20,::3],levels=3,linewidths = 1,colors='b')
    plt.clabel(cl1 ,  fmt='%.2f',inline=True, fontsize=10)
    cl2=ax.contour(x[::3,::3],z[::3,::3],QS[nt,::3,20,::3],levels=3,linewidths = 1,colors='k',linestyles = "dashdot")
    plt.clabel(cl2 , fmt='%.2f', inline=True, fontsize=10)
    # sh=ax.contourf(QG[nt,:,20,:],cmap = cmaps.precip4_11lev)

    # car = fig.colorbar(sh)
    # car.ax.set_ylabel('(g/kg)',fontsize = 20)
    ax.set_xlabel('Times(min)',fontsize = 20)
    ax.set_ylabel('Height(km)',fontsize = 20)

    bwith = 2 
    ax.spines['bottom'].set_linewidth(bwith)
    ax.spines['left'].set_linewidth(bwith)
    ax.spines['top'].set_linewidth(bwith)
    ax.spines['right'].set_linewidth(bwith)

    name = f'QR_QS_{times[nt]}min'
    ax.set_title(name,fontsize = 20)
    ax.tick_params(direction='out', length=8,labelsize=20)

    fig.savefig(f'{savename}/{name}.png',dpi=300)
#------------------------------------------------------------------#
#------------------------------------------------------------------#

#最大水凝物混合比时间序列
fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot()

ax.plot(times,QC.max(axis=-1).max(axis=-1).max(axis=-1),marker='.',c='r',lw=1.5,label='cloud')
ax.plot(times,QI.max(axis=-1).max(axis=-1).max(axis=-1),marker='*',c='b',lw=1.5,label='ice')
ax.plot(times,QR.max(axis=-1).max(axis=-1).max(axis=-1),marker='^',c='g',lw=1.5,label='rain')
ax.plot(times,QS.max(axis=-1).max(axis=-1).max(axis=-1),marker='s',c='y',lw=1.5,label='snow')
plt.legend()

ax.set_xlabel('Times(min)',fontsize = 20)
ax.set_ylabel('MixRadio(g/kg)',fontsize = 20)
ax.tick_params(direction='out', length=8,labelsize=15)
fig.savefig(f'{savename}/MixRadio.png',dpi=300)

#------------------------------------------------------------------#
#------------------------------------------------------------------#
# 水凝物随高度变化

for nt in range(ntimes):
    print(f"Working on time: {times[nt]}")
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot()

    ax.plot(QC[nt,...].mean(axis=-1).mean(axis=-1),Z/1000,c='r',lw=1.5,label='QC')
    ax.plot(QI[nt,...].mean(axis=-1).mean(axis=-1),Z/1000,c='b',lw=1.5,label='QI')
    ax.plot(QR[nt,...].mean(axis=-1).mean(axis=-1),Z/1000,c='g',lw=1.5,label='QR')
    ax.plot(QS[nt,...].mean(axis=-1).mean(axis=-1),Z/1000,c='y',lw=1.5,label='QS')
    plt.legend()
    # ax.set_xlim(0,12)
    # ax.set_xlabel('Wind Speed(m/s)',fontsize = 20)
    # ax.set_ylabel('Height(km)',fontsize = 20)
    name = f'Q_Height_{times[nt]}min'
    ax.set_title(name,fontsize = 15)
    ax.tick_params(direction='out', length=8,labelsize=20)

    fig.savefig(f'{savename}/{name}.png',dpi=300)

