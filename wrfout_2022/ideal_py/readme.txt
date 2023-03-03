1、改代码前面路径就行，代码在ideal_py文件夹下，把数据从服务器下载下来用本地的python环境跑，服务器上有bug！！！
依赖的库
#====================#
conda install numpy
conda install matplotlib
conda install -c conda-forge netcdf4
conda install -c conda-forge xarray
conda install -c conda-forge wrf-python
conda install -c conda-forge cmaps
#====================#
上面的命令时下载库的命令，复制粘贴就可以安装了
#====================#

2、要是觉得麻烦，那就直接用我的图把，反正跑出来的是一样，挑几张分析分析

#====================#  云量
CloudHeight_delt*
|--CloudHeight_10.0min.png  ： 10分钟云顶高度图
|--CloudyFraction.png ：云量随时间变化图
#---------------------------------# 水凝物
hydrometeor_delt*  文件夹
|-MixRadio.png   ：水凝物最大混合比随时间变化图
|-Q_Height_10min.png ：10分钟水凝物粒子随高度变化图  QC 云，QR 雨滴 QI 冰晶 QS 雪
|-QQ_20.0min.png    :20分钟云水混合比（蓝实线）和冰晶混合比（黑虚线）随高度分布 填色图时垂直速度
#---------------------------------# 水汽
vapor_delt*   文件夹
|-QVAPOR_20.min  ：20分钟水汽随高度变化，填色图时垂直速度
#---------------------------------# 垂直速度
\Vertical_delt*
|-W_SpeedHeight_0.0min ：0分钟垂直速度对高度变化
|-Maximum.png  :最大垂直速度随时间变化

#---------------------------------# 降水
rainintencity.png ：雨强
降水量.png  ：不用我还说了把


