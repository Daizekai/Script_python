import numpy as np
from Model.time_diff import *
from Model.smooth import *
from Model.geo import *
from Model.file_io import data_save
def run():  # sourcery skip: for-index-underscore
    """运行文件
    """
    #### 读取namelist，获得程序需要的参数
    dt = 600 # unit['secend'] time_step
    ref_lon = 51
    grids = [16,20]
    path = r'C:\Users\dzk\Desktop\实习报告\Barotropic_primitive_equation_model\Input\za.dat'
    outpath = r'C:\Users\dzk\Desktop\实习报告\Barotropic_primitive_equation_model\Output'
    dx = dy = 3e5
    t_sum = 48  #模拟时长 unit=['hour]
    #######################################################################

    time_control = np.array([1,6,12,24],dtype=np.float32)*6  # 时间控制参数 ，[unit = 'hour']这里规定 6h 做一次时间平滑，12h做空间平滑，24h结束积分
    time_num = int(time_control[-1]*3600/dt)    # 需要积分的时间步数
    #########计算地图放大系数和科氏参数######################################
    map,f = cmf(ref_lon,grids,dx,outpath)
    
    ##########初始化风场###################################################

    h_0,ua_0,va_0 = geo_init(map,f,path,dx,dy,outpath,flag=2)
 
    ###########初始化#####################################################
    #######这里将数组设置为(时间，经度，纬度)三维数据 (3,n,m)################
    #######这里直接默认赋固定边界值，因为后续操作都是内点(u[1:-1,1:-1])操作###
    #####################################################################
    u = np.tile(ua_0,(3,1,1))
    v = np.tile(va_0,(3,1,1))
    h = np.tile(h_0,(3,1,1))
    print('----------初始化成功------------\n')
    ##########积分#######################################################
    Na = 0
    while Na < t_sum/12 :
        for i in range(int(time_control[-2])):
            #######前一小时 欧拉-后差#######################################
            if i < time_control[0]:
                u,v,h=Eula_past_diff(u,v,h,map,f,dx,dy,dt)

            elif i == time_control[0] :
                u,v,h= three_step(u,v,h,map,f,dx,dy,dt)
                i = i+1  #总的是消耗两步

            else :
                u,v,h=Central_diff(u,v,h,map,f,dx,dy,dt)

            if not ((i+1) % 6):
                u[1,...]=N_point_smooth(u[1,...],N = 5,flag = 1)
                v[1,...]=N_point_smooth(v[1,...],N = 5,flag = 1)
                h[1,...]=N_point_smooth(h[1,...],N = 5,flag = 1)
                print('--------------------已积分到第{0:f}小时---------------------------'.format((i+1)/6))
            if i*dt == 6*3600 : 
                pass       
                # #############时间平滑#######################    
                # u[1,1:-1,1:-1]=time_smooth(u,flag = 1)
                # v[1,1:-1,1:-1]=time_smooth(v,flag = 1)
                # h[1,1:-1,1:-1]=time_smooth(h,flag = 1)
    #############12h空间平滑################################################
        u[1,...]=N_point_smooth(u[1,...],N = 9)
        v[1,...]=N_point_smooth(v[1,...],N = 9)
        h[1,...]=N_point_smooth(h[1,...],N = 9) 
        Na +=1
    #############保存文件###################################################
    data_save(u,'u',outpath)
    data_save(v,'v',outpath)
    data_save(h,'h',outpath)
    #############预报结束###################################################