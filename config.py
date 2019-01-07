#!/usr/bin/env python
# -*- coding: UTF-8 -*-  

'''
{
"版权"] = "lqab工作室",
"author":{
0:"全体"
}
"初创时间:"2017年3月",
}
'''

# ----------------- 外部模块处理<<开始>>  -----------------

#-----系统必备模块引用 #-----
import sys # 操作系统模块1
import os # 操作系统模块

#-----通用功能模块引用 #-----

#-----特定功能模块引用 #-----
#from service.handler import * #导入web路由
# ----------------- 外部模块处理<<结束>>  -----------------

# ----------------- 内部模块处理<<开始>>  -----------------


# 本地主路径
path_self ="\\code"
path_main = os.path.abspath('')
path_main = path_main.replace(path_self,"\\")

dic_config = {} #定义主变量字典

###config_start###

# ---- 系统标准参数配置 ---
dic_config["ip"] = "127.0.0.1" #---web调试地址
dic_config["web_port"] = "8100" #---web服务端口
dic_config["default_web_file"] = "index.html" #---web默认主页
dic_config["charset_web"] = "utf-8" #---web编码
dic_config["name_soft"] = "丽华数据挖掘机" #---软件名称
dic_config["type_soft"] = "公开发行" #---软件版本名 品系
dic_config["vol_soft"] = "版本号：1.0" #---软件版本号
dic_config["authority_soft"] = "GPL-3.0" #---软件授权方式
dic_config["author_soft"] = "lqab工作室" #---软件开发方
dic_config["qq_group"] = "730422068" #---软件支持服务QQ群号
dic_config["tel_lqab"] = "15636176092" #---软件支持手机
dic_config["wechat_lqab"] = "15636176092" #---软件支持微信
dic_config["url_lqab"] = "www.lqab.net" #---软件支持网站

# ---- 前台应用参数配置 ---
dic_config["max_per_page"] = "6" #---默认分页数
dic_config["form_default"] = "script" #---表单默认提交
dic_config["numb_find"] = "8" #---最大匹配关键词队列数
dic_config["numb_limit"] = "6" #---匹配候选数

# ---- 主数据库参数配置 ---
dic_config["path_sqlite"] = "\\data\\sqlite\\main.db" #---主配置sqlitewen文件地址
dic_config["host_mysql"] = "127.0.0.1" #---mysql数据库地址
dic_config["user_mysql"] = "root" #---mysql管理员名
dic_config["pwd_mysql"] = "r4t5y6u7" #---mysql管理员密码
dic_config["name_mysql_after"] = "a" #---mysql数据库名的后缀代号
dic_config["port_mysql"] = "3306" #---mysql数据库端口号
dic_config["charset_mysql"] = "utf8" #---mysql数据库编码
dic_config["database_if"] = "0" #---是否使用数据库环境


# ---- 主数据库参数配置 ---


# ---- 权限管理参数配置 ---

# ---- 前台应用参数配置 ---

# ---- 加密解密参数配置 ---

# ---- 数据分析引擎参数配置 ---

# ---- 工程生产参数 ----

dic_config["path_main"] = "http://lqab.vicp.net:1977/" #---默认主绝对路径

# ---- 缓存参数 ----

###config_end###


# ----------------- 内部模块处理<<结束>>  -----------------

# ------------------ 主过程<<开始>>  -------------------#


def main():

    print("") # 防止代码外泄 只输出一个空字符

if __name__ == '__main__':
    main()
    
# ------------------ 主过程<<结束>>  -------------------#
 