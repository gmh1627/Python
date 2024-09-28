import os
from ctypes import util

# 将 GTK 的 bin 目录添加到系统路径
gtk_bin_path = r'D:\GTK3-Runtime Win64\bin'
os.environ['PATH'] = gtk_bin_path + ';' + os.environ['PATH']

# 检查是否可以找到 pango-1.0-0 库
pango_lib_path = util.find_library('pango-1.0-0')
print(pango_lib_path)  # 打印加载库的路径
