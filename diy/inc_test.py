#!/usr/bin/env python
# -*- coding: UTF-8 -*-  

'''
{
"版权":"LQAB工作室",
"author":{
"1":"集体",
}
"初创时间:"2017年3月",
}
'''

#--------- 外部模块处理<<开始>> ---------#

#-----系统自带必备模块引用-----

import sys # 操作系统模块1
import os # 操作系统模块2
import types # 数据类型
import time # 时间模块
import datetime # 日期模块
import re # 正则模块

#-----系统外部需安装库模块引用-----


#-----DIY自定义库模块引用-----
sys.path.append("..")
import config #系统配置参数
import diy.inc_sys as inc_sys #自定义基础组件

#--------- 外部模块处理<<结束>> ---------#


#--------- 内部模块处理<<开始>> ---------#

# ---外部参变量处理

# ---全局变量处理


# ---本模块内部类或函数定义区

#继承字符扩展对象
class Regular_base(object):

    # 获取参数的当前路径
    def exist_if(self,re_p,txt_p):
        pattern = re.compile(re_p)
        return (pattern.search(str_p))

#--------- 内部模块处理<<结束>> ---------#

#---------- 主过程<<开始>> -----------#

def main():

    print ("") #调试用
    
if __name__ == '__main__':
    
    main()
    
#---------- 主过程<<结束>> -----------#