import itertools
import numpy as np
from Model.file_io import data_save
from Model.file_io import read_meta
from Model.const import le,f0,k,a,g
# np.random.seed(99) 测试数据
def cmf(theta:float,grids:list,dx:float,outpath): #计算地图放大系数和科氏参数
    """计算地图放大系数和科氏参数

    Args:
        theta (float): 研究区域中心纬度
        grids (list): 网格点数，第一个参数为纬向
        dx (float)  : 网格距离,经纬方向一致 [unit:'m']
        outpath (str): 保存计算的放大系数和科氏参数

    Returns:
        rm,f (tuple): 前一个为放大系数，后一个为科氏参数

    """        
    
    ###############计算模式中心到北极的距离rl########################
    theta = theta*np.pi/180
    th = 30*np.pi/180
    t = np.tan(theta/2)/np.tan(th/2)
    rcent = a*np.sin(th)/k*t**k
    n,m = grids
    #########确定网格坐标原点在地图坐标系中的位置#####################
    xi0 = -(m-1)/2.0
    yj0 = -(rcent / dx + (n-1)/2.0)
    rm = np.empty((n,m))
    f = np.empty((n,m))
    ##求各格点至北极点的距离rl,(xj,yi)为模式各格点在地图坐标系中的位置#
    for i, j in itertools.product(range(m), range(n)):
        xi = xi0+i
        yj = yj0+j
        rl = dx*np.sqrt(xi**2+yj**2)

    ########## 求放大系数rm和柯氏参数f##############################
        sin_xy = (le**(2.0/k)-rl**(2.0/k))/(le**(2.0/k)+rl**(2.0/k))
        cos_xy = np.sqrt(1-sin_xy**2)
        rm[j,i] = k*rl/(a*cos_xy)
        f[j,i] = 2*f0*sin_xy
    
    #################保存数据######################################
    data_save(rm,'maps_Factor',outpath)
    data_save(f,'Coriolis',outpath)

    return rm,f

def geo_init(maps,f,path,dx,dy,outpath,flag=2):    #计算地转风初值

    """计算地转风初值
    maps :放大系数
	f:科氏参数
    path : 原始数据路径
    dx,dy :分辨率 unit['m']
    gradient ：函数,差分代替微分
    flag : 差分格式 1:后差 2:中央差
    """
    #############读文件##############################################
    geo_meta = read_meta(path)              #测试数据 n*m 16*20    

    #############计算初值############################################
    if flag == 2: #中央差
        ua_0 = -maps*g/f*np.gradient(geo_meta,dy,axis=0,edge_order=1)
        va_0 = maps*g/f*np.gradient(geo_meta,dx,axis=1,edge_order=1) #axis=1,dz/dx
    elif flag == 1: #前差
        df_dy_end = geo_meta[-1,:] - geo_meta[-2,:] # 1*20
        df_dy_0 =  geo_meta[1:,:] - geo_meta[:-1,:] # 15*20
        df_dy = np.vstack((df_dy_0,df_dy_end))/dx
        df_dx_end = geo_meta[:,-1] - geo_meta[:,-2] # 16*1
        df_dx_0  = geo_meta[:,1:] - geo_meta[:,:-1] # 16*19

        df_dx = np.hstack((df_dx_0,df_dx_end.reshape(-1,1)))/dx
        ###########################################################
        ua_0 = -maps*g/f*df_dy
        va_0 =  maps*g/f*df_dx
    #############存文件#############################################  
    data_save(ua_0,'ua_0',outpath)
    data_save(va_0,'va_0',outpath)

    return geo_meta,ua_0,va_0
