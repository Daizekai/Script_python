from __future__ import print_function

from netCDF4 import Dataset
from wrf import getvar, ALL_TIMES

# 创建文件序列
wrflist = [Dataset("wrfout_d01_2016-10-07_00_00_00"),
           Dataset("wrfout_d01_2016-10-07_01_00_00"),
           Dataset("wrfout_d01_2016-10-07_02_00_00")]

# 提取所有时刻的P变量
p_cat = getvar(wrflist, "P", timeidx=ALL_TIMES, method="cat")

print(p_cat)