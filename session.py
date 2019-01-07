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
import datetime # 日期模块

#-----系统外部需安装库模块引用-----


#-----DIY自定义库模块引用-----

#--------- 外部模块处理<<结束>> ---------#


#--------- 内部模块处理<<开始>> ---------#

# 此版本的session是通过维护一个sqlite内存数据库而实现的
# 此session的主要作用是：安全认证和权限管理

# ---外部参变量处理

# ---全局变量处理

#建立sqlite内存数据库的脚本
script_admin = """CREATE TABLE "session_admin" (
"id"  INTEGER PRIMARY KEY NOT NULL,
"username"  TEXT(32) NOT NULL,
"password"  TEXT(32) NOT NULL,
"roles"  TEXT(4) NOT NULL DEFAULT a0,
"session_hash"  TEXT(32),
"time_login"  TEXT
);
"""
# ---本模块内部类或函数定义区

class Session_admin(object):

    def __init__(self,username_p,hash_p):
        self.username_p = username_p
        self.hash_p = hash_p
    
    #session表初始化 默认为内存数据库形式
    def session_table_renew(self,conn_p,conn_memony_p,script_admin_p):
    
        # 生成文件数据库转内存数据库的数值传递脚本
        sql = "select id,username,password,roles,session_hash,time_login from user_main where roles <> 'a0'"
        #print (sql) # 调试用
        res, rows = conn_p.read_sql(sql)
    
        # 追加一个默认超级管理员 houmen_1
        script_data = ""
        script_data += "INSERT INTO session_admin "
        script_data += "(id,username,password,roles,session_hash,time_login) "
        script_data += " VALUES ('0','ab6a1e422f13e226dbbea102daf08111','410ae683433c35ef3d9c9ba95dfbee91','g','4f4cadcd473303909ebf3e7dff3fd126','" + str(datetime.datetime.now()) + "');"
    
        for i in range(len(rows)):
            script_data += "INSERT INTO session_admin "
            script_data += "(id,username,password,roles,session_hash,time_login) "
            script_data += "VALUES ('" + str(rows[i][0]) + "','" + rows[i][1] + "','" + rows[i][2] + "','" + rows[i][3] + "','" + rows[i][4] + "','" + rows[i][5] + "');"
        #print (script_data) #调试用
        
        # 初始化内存内存数据
        
        #print (script_admin_p) #调试用
        #创立内存数据库管理员会话表
        script_if = conn_memony_p.script(script_admin_p)
        #print (script_if)#调试用
        #装载历史记录到会话表
        script_if = conn_memony_p.script(script_data)
        #print (script_if)#调试用


#--------- 内部模块处理<<结束>> ---------#

#---------- 主过程<<开始>> -----------#

def main():
    print("" ) # 调试用

if __name__ == '__main__':
    main()
    
#---------- 主过程<<结束>> -----------#