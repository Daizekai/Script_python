import numpy as np
from Model.const import g
def L_diff(u,v,f,dx,dy):  #空间差分算子L
    """空间差分算子
    math : \left [ \overline{\bar{u}^{x}()_{x}}^{x} + \overline{\bar{v}^{y}( )_{y} }^{y}  \right ] 
    Args:
        u (numpy.array): 纬向风场
        v (numpy.array): 经向风场
        f (numpy.array): 某个矢量场 
        dx (float): x方向分辨率
        dy (float): y方向分辨率

    Returns:
        Lu+Lv (numpy.array): 算子
    """

    Lu = u.copy()
    Lv = v.copy()
    Lu[1:-1,1:-1] = 1./(4.0*dx) * ( (u[1:-1,2:] + u[1:-1,1:-1])*( f[1:-1,2:] - f[1:-1,1:-1])+( u[1:-1,:-2] + u[1:-1,1:-1])*(f[1:-1,1:-1] - f[1:-1,:-2]) )
    Lv[1:-1,1:-1] = 1./(4.0*dy) * ( (v[2:,1:-1] + v[1:-1,1:-1])*( f[2:,1:-1] - f[1:-1,1:-1])+( v[:-2,1:-1] + v[1:-1,1:-1])*(f[1:-1,1:-1] - f[:-2,1:-1]) )

    return (Lu+Lv)[1:-1,1:-1]

def f_plus(maps,f,u,v,dx,dy): #空间差分算子f*
    """变换后的科氏算子
    math : f_{i,j} = u_{i,j}\overline{m_{x}}^{x} - v_{i,j}\overline{m_{y}}^{y}
    Args:
        maps (array): 放大系数
        f (array): 科氏参数
        u (numpy.array): 纬向风场
        v (numpy.array): 经向风场
        dx (float): x方向分辨率
        dy (float): y方向分辨率

    Returns:
        _type_: 变换后的科氏算子
    """

    m_y,m_x = np.gradient(maps,dy,axis=0)[1:-1,1:-1],np.gradient(maps,dx,axis=1)[1:-1,1:-1]
    return (f[1:-1,1:-1] + u[1:-1,1:-1]*m_y - m_x*v[1:-1,1:-1] )  

def adv(uu,vv,dx,dy): #空间差分算子
    """空间差分平流算子
    math : \overline{()_{x}}^{x}+\overline{()_{y}}^{y}
    Args:
        uu (numpy.array): 纬向风场
        vv (numpy.array): 经向风场
        dx (float): x方向分辨率
        dy (float): y方向分辨率

    Returns:
        _type_: 算子
    """
    return (np.gradient(uu,dx,axis=1)[1:-1,1:-1]+np.gradient(vv,dy,axis=0)[1:-1,1:-1])

def advection_equation_2(maps,f,dx,dy,uu,vv,hh):  
    """二次守恒平流格式

    Args:
        maps (array): 放大系数
        f (array): 科氏参数
        u (numpy.array): 纬向风场
        v (numpy.array): 经向风场
        dx (float): x方向分辨率
        dy (float): y方向分辨率
        hh (_type_): 高度场

    Returns:
        E,G,H (tuple): 趋势场
    """
    ############################  du/dt   ##################################################
    E = - maps[1:-1,1:-1]*( L_diff(uu,vv,uu,dx,dy)+g*(np.gradient(hh,dx,axis=1)[1:-1,1:-1]) )+ f_plus(maps,f,uu,vv,dx,dy)*vv[1:-1,1:-1]
    
    #############################  dv/vt  ##################################################
   
    G = - maps[1:-1,1:-1]*( L_diff(uu,vv,vv,dx,dy) + g*(np.gradient(hh,dy,axis=0)[1:-1,1:-1]) )-f_plus(maps,f,uu,vv,dx,dy)*uu[1:-1,1:-1]
    
    #############################  dh/dt  ##################################################
    H = - maps[1:-1,1:-1]**2*(L_diff(uu,vv,hh/maps,dx,dy)+hh[1:-1,1:-1]/maps[1:-1,1:-1]*adv(uu,vv,dx,dy))
    
    return E,G,H

