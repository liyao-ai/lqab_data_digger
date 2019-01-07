#!/usr/bin/env python
# -*- coding: UTF-8 -*-  
#--------- 模块处理<<开始>> ---------#

#-----系统自带必备模块引用-----
import sys # 处理系统模块
import os # 操作系统模块
import types # 数据类型
import time # 获得系统时间
import datetime # 获得日期
import random # 随机函数
import threading #多线程
import multiprocessing #多进程

#-----系统外部需安装库模块引用-----

#-----DIY自定义库模块引用-----
import diy.inc_sys as inc_sys #自定义系统级功能模块
import diy.inc_conn as inc_conn #自定义数据库功能模块
import config #系统配置参数
from inc_gui import * #自定义GUI处理模块

#--------- 模块处理<<结束>> ---------#

#--------- 辅助功能处理<<开始>> ---------#

#--------- 辅助功能处理<<结束>> ---------# 

#--------- 主处理功能<<开始>> ---------#


# ----主辅助函数定义区 ----


#--------- 主处理功能<<结束>> ---------# 

#--------- 主过程<<开始>> ---------#
def gui_main():
    
    #1 主窗体实例化
    app = QApplication(sys.argv)
    window_main = Window_main(title)
    
    #2 主窗体显示
    window_main.show()
    
    #3 结束处理
    sys.exit(app.exec_())

# 说明字典
dic_note = {
"版权":["LQAB工作室"],
"作者":["集体","吉更"],
"初创时间":["2018年12月"],
"功能":["数据挖掘机主程序"],
}
def main():

    inc_sys.version(dic_p=dic_note) # 打印版本
    gui_main()
    
if __name__ == "__main__":

    main()
    
#--------- 主过程<<结束>> ---------#