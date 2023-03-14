import numpy as np
# from sympy import Order
import os
import xarray as xr
def data_save(u,filename,outpath:str,flag = 1):
    """保存数据
    Args:
        u (numpy.array): 储存的文件
        flag (int, [1-5]): 想要储存文件的格式 Defaults to 1.
        flag = 1 : '.npy'
        flag = 2 : '.txt'
        flag = 3 : '.dat'
        flag = 4 : '.nc'
        flag = 5 : '.grib2'
    """
    os.chdir(outpath)
    if flag == 1:
        np.save(filename,u)

    # elif flag == 4 :
    #     lon,lat = np.meshgrid(np.arange(85,85+20*3.5,3.5),np.arange(32.5,32.5+16*2.5,2.5))
    #     ds = xr.Dataset(
    #         data_vars=dict(
    #             name = (["x","y"],u),
    #         ),
    #         coords = (
    #             lon = (["x","y"],lon),
    #             lat = (["x","y"],lat),
    #         ),
    #     )
    #     ds.to_netcdf(path=filename)

def read_meta(path = r'C:\Users\dzk\Desktop\Barotropic_primitive_equation_model\Input\za.dat'):
    data = np.fromfile(path,sep = ' ')
    return data.reshape((16,20),order='c')

