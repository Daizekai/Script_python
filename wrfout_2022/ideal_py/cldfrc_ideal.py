"""
Created on June 9 21:05 2022

@author: xianyun
"""

# Example script to produce dbz plots for a WRF ideal-data run
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
filename = r'C:\Users\dzk\Desktop\test10\delt3\wrfout_d01_0001_01_01_00_00_00'
ncfile = Dataset(filename)
savename  = 'CloudHeight'                                                # savename
if not os.path.exists(savename):
    os.mkdir(savename)
#------------------------------------------------------------------#
#------------------------------------------------------------------#
#Which times and how many time steps are in the data set?
times = extract_times(ncfile,timeidx=ALL_TIMES,do_xtime=True)      #get all times in the file
ntimes = times.shape[0]                                            #number of times in the file

#------------------------------------------------------------------#
#------------------------------------------------------------------#
def cal_cloudiness(QT):                                            #计算云量
    k,m,n = QT.shape                                               #获取垂直层,平面网格
    cloudiness = np.zeros((k,))
    for i in range(k):
        tmp = QT[i,...]
        tmp = tmp[QT[i,...]!=0]
        cloudiness[i] = tmp.shape[0]/(m*n)
    return cloudiness

def cal_top(QT,z):   #计算云顶高度
    k,m,n = QT.shape 
    # print(QT.shape)
    cld_tops = np.zeros((m,n))
    for i in range(m):
        for j in range(n):
            # print(i,j)
            if np.where(QT[::-1,i,j]>=1.e-6)[0].size : 
                cld_tops[i,j] = z[k - np.where(QT[::-1,i,j]>=1.e-6)[0][0]]
            else :
                cld_tops[i,j] = 0
    return cld_tops
#------------------------------------------------------------------#
#------------------------------------------------------------------#
cloudthres = 1.e-5                                                 #阈值，判断是否有云
#------------------------------------------------------------------#
Z = getvar(ncfile,'z').to_numpy()[:,1,1]
QC = getvar(ncfile,'QCLOUD',timeidx=ALL_TIMES).to_numpy()
QR = getvar(ncfile,'QRAIN',timeidx=ALL_TIMES).to_numpy()
QI = getvar(ncfile,'QICE',timeidx=ALL_TIMES).to_numpy()
QS = getvar(ncfile,'QSNOW',timeidx=ALL_TIMES).to_numpy()
QG = getvar(ncfile,'QGRAUP').to_numpy()
QT = QC+QR+QG
QT[QT<cloudthres] = 0.

#------------------------------------------------------------------#
#------------------------------------------------------------------#
###云量随时间变化
# 云量计算
cldfrc = np.zeros((QT.shape[0],QT.shape[1]))
for i in range(QT.shape[0]):
    cldfrc[i,:]=cal_cloudiness(QT[i,...])

t,z = np.meshgrid(range(ntimes),Z/1000.)

fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot()

sh=ax.contourf(t,z,cldfrc.T,cmap=cmaps.WhViBlGrYeOrRe)
name = 'CloudyFraction'
ax.set_title(name,fontsize = 20)
ax.tick_params(direction='out', length=8,labelsize=20)
ax.set_xlabel('Time/10min',fontsize=20)
ax.set_ylabel('Height/km',fontsize=20)
car = fig.colorbar(sh)

fig.savefig(f'{savename}/{name}.png',dpi=300)

#------------------------------------------------------------------#
#------------------------------------------------------------------#
#------------------------------------------------------------------#
###云顶高度

levels = np.arange(0,12.1,0.5)


for nt in range(ntimes):
    print(f"Working on time: {times[nt]}")
    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot()

    sh=ax.contourf(cal_top(QT[nt,...],Z/1000),levels=levels,cmap=cmaps.WhiteBlueGreenYellowRed)
    name = f'CloudHeight_{times[nt]}min'
    ax.set_title(name,fontsize = 20)
    ax.tick_params(direction='out', length=8,labelsize=20)

    car = fig.colorbar(sh)
    car.ax.set_title('Height(km)',fontsize = 15)

    fig.savefig(f'{savename}/{name}.png',dpi=300)
