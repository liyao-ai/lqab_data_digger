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
import os # 操作系统模块
import sys # 操作系统模块1
import datetime # 系统时间模块1
import time # 系统时间模块2

#-----系统外部需安装库模块引用-----

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options


#-----DIY自定义库模块引用-----
sys.path.append("..")
import config #系统配置参数
import session #系统session模块
from diy.inc_sys import * #自定义系统级功能模块 
from diy.inc_conn import * #自定义数据库操作模块
from diy.inc_hash import * # 基本自定义hash模块
import diy.inc_file as inc_file # 基本自定义文件模块
 
#-----DIY自定义库模块引用-----

#--------- 外部模块处理<<结束>> ---------#


#--------- 内部模块处理<<开始>> ---------#

# ---外部参变量处理

# ---全局变量处理

# ---本模块内部类或函数定义区

# web服务基础模块
class BaseHandler(tornado.web.RequestHandler):

    # 获得浏览器传递参数
    def browser_argument(self,name_p=""):
        
        value_p = ""
        
        if (name_p != ""):
        
            try:
                if (name_p in self.request.arguments):
                    value_p = self.request.arguments[name_p][0].decode('utf-8')
            except:
                pass
                
        print ("输入参数名：",name_p,"返回参数值：",value_p)
        
        return value_p
        
    # 动态调用模块
    def import_do(self,file_p="",args_p=""):
        
        result = ""
        
        run_model =__import__(file_p)
        result = run_model.run_it(args_p)
        #try:
            #run_model =__import__(file_p)
            #result = run_model.run_it(args_p)
        #except:
            #result = "模块不存在或调用接口错误"
            
        return result
        
    # 用户权限标定
    def user_power_is(self,roles_p):

        result = "零"
        if (roles_p == 1):
            result = "一"
        elif(roles_p == 2):
            result = "二"
        elif(roles_p == 3):
            result = "三"
        elif(roles_p == 4):
            result = "四"
        elif(roles_p == 5):
            result = "五"
        elif(roles_p == 6):
            result = "六"
        elif(roles_p == 7):
            result = "七"
        elif(roles_p == 8):
            result = "八"
        elif(roles_p == 9):
            result = "九"
            
        return result

    # 用户登录处理
    def user_login_do(self,username_p="",password_p="",cookie_if=1):
    
        pass_if_p = False
        roles_p = ""
        dic_t = {}
        str_log = ""
        str_t = ""
        dic_t["username"] = username_p
        dic_t["password"] = password_p
        username_p = hash_make(hash_make(username_p)) #密文处理
        password_p = hash_make(hash_make(password_p)) #密文处理
        path_p = config.path_main + "data\\log\\user\\"
        
        #查询用户管理数据库
        
        rs_way_mysql = Conn_mysql(config.dic_config["host_mysql"],config.dic_config["user_mysql"],config.dic_config["pwd_mysql"], "lqab_way_" + config.dic_config["name_mysql_after"], int(config.dic_config["port_mysql"])) # 生成MYSQL数据库way方法实例
        sql = "select roles,id,coin from user where username='" + username_p + "' and password = '" + password_p + "' order by id desc limit 0,1"
        res_m, rows_m = rs_way_mysql.read_sql(sql)
        
        if (res_m > 0):
        
            roles_p = rows_m[0][0]
            dic_t["roles"] = rows_m[0][0]
            dic_t["id"] = rows_m[0][1]
            dic_t["coin"] = rows_m[0][2]
            dic_t["time_login"] = str_split(datetime.datetime.now())
            dic_t["ip"] = self.request.remote_ip
            str_log = str(dic_t)
            
            # 日志操作
            if (config.dic_config["log_if"] == "1"):
                path_p += "z_user_login_" + str(rows_m[0][1]) + ".csv"
                file_file = inc_file.File_file()
            
            # 加密session字典
            str_t = secret_lqab(str_log,key_p=config.dic_config["secret_key"],salt_p = config.dic_config["secret_salt"],secret_if="yes")
            pass_if_p = True
            
        if (pass_if_p == True):
        
            #print ("加密的session字典",str_t) # 调试用
            if (cookie_if == 1):
                self.set_secure_cookie("session_lqab_user",str_t)
                txt_log = ""
                # 将访问日志字典转化为csv格式
                if (dic_t):
                    txt_log = str(dic_t["id"]) + "," + dic_t["username"] + "," + dic_t["password"] + "," +  str(dic_t["roles"]) + "," + str(dic_t["coin"]) + "," + dic_t["time_login"] + "," + dic_t["ip"] +  "\n"
                try:
                    file_file.write_add(path_p=path_p,renew_if=0,content_p=txt_log)
                except:
                    pass
                
        rs_way_mysql.close_cur() #关闭数据游标
        rs_way_mysql.close() #关闭数据连接
        
        return pass_if_p,roles_p

    # 用户登录检查
    def user_login_check(self,time_alive_p=0):
        
        pass_if = False
        time_now_p = str_split(datetime.datetime.now()) #调试用
        time_now_p = time.mktime(time.strptime(time_now_p, '%Y-%m-%d %H:%M:%S'))
        time_login_p = ""
        roles_p = 0
        dic_login_p = {}
        str_t = ""
        
        try:
            
            str_t = self.get_secure_cookie("session_lqab_user")
            str_t = str_t.decode('utf-8')
            # 解密session字典
            str_t = secret_lqab(str_t,key_p=config.dic_config["secret_key"],salt_p = config.dic_config["secret_salt"],secret_if="no")
            dic_login_p = eval(str_t)
            
        except:
        
            pass
            
        if (dic_login_p):
            # 登录处理
            pass_if,roles_p= self.user_login_do(username_p=dic_login_p["username"],password_p=dic_login_p["password"],cookie_if=0)
            # 校验历史权限
            if (roles_p != dic_login_p["roles"]):
                pass_if = False
            # 登录时间比对
            time_login_p = dic_login_p["time_login"]
            time_login_p = time.mktime(time.strptime(time_login_p, '%Y-%m-%d %H:%M:%S'))
            print ("距上次登录时间：",time_now_p-time_login_p,"秒") # 调试用
            if ((time_now_p-time_login_p) > 3600.0*24.0 * time_alive_p):
                pass_if = False
            
        #print ("参数：",roles_p,str_t,dic_login_p) # 调试用
        
        # 权限检查
        return pass_if,dic_login_p
    
    # 管理员权限标定
    def admin_power_is(self,roles_p):

        for i in range(8):
            row = config.dic_config["power_" + str(i)]
            if (roles_p == row[0]):
                return row[1]
                
        return "n/a"
        
    # 管理员登录退出
    def sys_logout(self,list_p=["lqab"]):
            
        for x in list_p:
            self.clear_cookie(x) # 清空cookies

    # 管理员登录处理
    def admin_login_do(self,username_p="",password_p="",cookie_if=1):
    
        pass_if_p = False
        roles_p = ""
        dic_t = {}
        str_log = ""
        aid_p = 0 # 管理员ID
        str_t = ""
        dic_t["username"] = username_p
        dic_t["password"] = password_p
        username_p = hash_make(hash_make(username_p)) #密文处理
        password_p = hash_make(hash_make(password_p)) #密文处理
        path_p = config.path_main + "data\\log\\admin\\"
        
        #查询用户管理数据库
        
        rs_sqlite_file = Conn_sqlite3(config.path_main + config.dic_config["path_sqlite"],0) # 生成文件数据库实例
        sql = "select roles,id from user_main where username='" + username_p + "' and password = '" + password_p + "' order by id desc limit 0,1"
        res_m, rows_m = rs_sqlite_file.read_sql(sql)
        
        if (res_m > 0):
        
            roles_p = rows_m[0][0]
            dic_t["roles"] = rows_m[0][0]
            dic_t["id"] = rows_m[0][1]
            aid_p = rows_m[0][1]
            dic_t["time_login"] = str_split(datetime.datetime.now())
            dic_t["ip"] = self.request.remote_ip
            str_log = str(dic_t)
            
            # 日志操作
            if (config.dic_config["log_if"] == "1"):
                path_p += "z_admin_login_" + str(rows_m[0][1]) + ".csv"
                file_file = inc_file.File_file()
            
            # 加密session字典
            str_t = secret_lqab(str_log,key_p=config.dic_config["secret_key"],salt_p = config.dic_config["secret_salt"],secret_if="yes")
            pass_if_p = True
            
        if (pass_if_p == True):
        
            #print ("加密的session字典",str_t) # 调试用
            if (cookie_if == 1):
                self.set_secure_cookie("session_lqab_admin",str_t)
                txt_log = ""
                # 将访问日志字典转化为csv格式
                if (dic_t):
                    txt_log = str(dic_t["id"]) + "," + dic_t["username"] + "," + dic_t["password"] + "," +  dic_t["roles"] + "," + dic_t["time_login"] + "," + dic_t["ip"] +  "\n"
                try:
                    file_file.write_add(path_p=path_p,renew_if=0,content_p=txt_log)
                except:
                    pass
                
        rs_sqlite_file.close_cur() # 关闭数据库游标
        rs_sqlite_file.close() # 关闭数据库连接
        
        return pass_if_p,roles_p,aid_p

    # 管理员登录检查
    def admin_login_check(self,time_alive_p=0):
        
        pass_if = False
        time_now_p = str_split(datetime.datetime.now()) #调试用
        time_now_p = time.mktime(time.strptime(time_now_p, '%Y-%m-%d %H:%M:%S'))
        time_login_p = ""
        roles_p = "a0"
        dic_login_p = {}
        str_t = ""
        aid_p = 0 # 管理员ID
        
        try:
            
            str_t = self.get_secure_cookie("session_lqab_admin")
            str_t = str_t.decode('utf-8')
            # 解密session字典
            str_t = secret_lqab(str_t,key_p=config.dic_config["secret_key"],salt_p = config.dic_config["secret_salt"],secret_if="no")
            dic_login_p = eval(str_t)
            
        except:
        
            pass
            
        if (dic_login_p):
            # 登录处理
            pass_if,roles_p,aid_p= self.admin_login_do(username_p=dic_login_p["username"],password_p=dic_login_p["password"],cookie_if=0)
            dic_login_p["aid"] = aid_p # 获得管理员ID
            # 校验历史权限
            if (roles_p != dic_login_p["roles"]):
                pass_if = False
            # 登录时间比对
            time_login_p = dic_login_p["time_login"]
            time_login_p = time.mktime(time.strptime(time_login_p, '%Y-%m-%d %H:%M:%S'))
            print ("距上次登录时间：",time_now_p-time_login_p,"秒") # 调试用
            if ((time_now_p-time_login_p) > 3600.0*24.0 * time_alive_p):
                pass_if = False
            
        #print ("参数：",roles_p,str_t,dic_login_p) # 调试用
        
        # 权限检查
        return pass_if,dic_login_p

# 主页模块
class IndexHandler(tornado.web.RequestHandler):
    
    def get(self,*args):
        
        # 访问日志处理
        dic_login_p = {}
        dic_t = {}
        txt_log = "" # 日志的文本内容
        path_p = config.path_main + "data\\log\\z_log_web_index.csv"
        file_file = inc_file.File_file()
        dic_t["time_v"] = str_split(datetime.datetime.now()) # 访问时间
        dic_t["ip"] = self.request.remote_ip # 获得IP
        dic_t["id"] = 0
        # 获得用户cookie资料
        try:
            
            str_t = self.get_secure_cookie("session_lqab_user")
            str_t = str_t.decode('utf-8')
            # 解密session字典
            str_t = secret_lqab(str_t,key_p=config.dic_config["secret_key"],salt_p = config.dic_config["secret_salt"],secret_if="no")
            dic_login_p = eval(str_t)
            if ("id" in dic_login_p):
                dic_t["id"] = dic_login_p["id"]
            
        except:
        
            pass
        
        #print ("日志参数",path_p,dic_t) # 调试用
        
        # 将访问日志字典转化为csv格式
        if (dic_t):
            txt_log = str(dic_t["id"]) + "," + dic_t["ip"] + "," + dic_t["time_v"] + "\n"
            
        # 写入访问日志
        try:
            file_file.write_add(path_p=path_p,renew_if=0,content_p=txt_log)
        except:
            pass
            
        # 渲染首页
        self.render('index.html',
        name_soft=config.dic_config["name_soft"],
        type_soft=config.dic_config["type_soft"],
        vol_soft=config.dic_config["vol_soft"],
        authority_soft=config.dic_config["authority_soft"],
        author_soft=config.dic_config["author_soft"],
        qq_group=config.dic_config["qq_group"],
        tel_lqab=config.dic_config["tel_lqab"],
        url_lqab=config.dic_config["url_lqab"],
        sys_time=str(datetime.datetime.now())
        ) #渲染首页
        
# 前台用户模块
class UserHandler(BaseHandler):

    # 权限检查
    def user_roles_chk(self,file_p="",code_p="",roles_p=""):
        
        pass_if = False
        
        rs_way_mysql = Conn_mysql(config.dic_config["host_mysql"],config.dic_config["user_mysql"],config.dic_config["pwd_mysql"], "lqab_way_" + config.dic_config["name_mysql_after"], int(config.dic_config["port_mysql"])) # 生成MYSQL数据库way方法实例
        sql = "select id from menu_user "
        sql += "where file_name ='" + file_p + "' and parm ='" + code_p + "' "
        sql += "and roles <= " + str(roles_p)
        res, rows = rs_way_mysql.read_sql(sql)
        #print(sql) #调试用
        if (res > 0):
            pass_if = True
            
        rs_way_mysql.close_cur() #关闭数据游标
        rs_way_mysql.close() #关闭数据连接
            
        return pass_if
    
    # 动态执行内容获取
    def content_get(self,roles_p="",file_p="",code_p="",args_p=""):
        
        result = ""
        pass_if =  True
        #1 权限检查
        pass_if = self.user_roles_chk(file_p=file_p,code_p=code_p,roles_p=roles_p)
        if (pass_if is False):
            result = "用户操作权限不匹配或权限表故障"
            return result
        
        result = self.import_do(file_p=file_p,args_p=args_p) # 获得动态执行模块结果
        
        return result

    # 文件执行
    def file_do(self,roles_p=0):
    
        file_p = "" # 请求功能模块名
        code_p = "" # 请求功能模块名
        output = "" # 请求结果的输出方式
        time_now_p = str_split(datetime.datetime.now()) # 请求时间
        path_p = config.path_main + "data\\log\\"
        dic_t = {}
        str_log = ""
        args_p = {}
        result = "<center><br><br>N/A</center>"
        content = ""
        
        # 取得web端提交参数
        dic_t = self.request.arguments
        for x in dic_t:
            try:
                args_p[x]= dic_t[x][0].decode('utf-8')
            except:
                pass
            
        # 登录校验
        pass_if,dic_login_p = self.user_login_check(time_alive_p=config.dic_config["time_alive"])
        #print ("基础参数",pass_if,dic_login_p) # 调试用
        
        # 追加参数字典
        #print ("追加前的参数字典",args_p) # 调试用
        args_p.update(dic_login_p)
        
        if (pass_if is False):
            result = "没有权限或登录超时"
            return result
        
        try:
            file_p = self.browser_argument(name_p="file")
            code_p = self.browser_argument(name_p="code")
            output = self.browser_argument(name_p="output")
        except:
            pass
            
        #print ("脚本调用参数",roles_p,file_p,code_p,output) # 调试用
        
        # 业务处理
        args_p["roles"] = roles_p # 追加操作权限参数
        
        content = self.content_get(roles_p=roles_p,file_p=file_p,code_p=code_p,args_p=args_p)
        # print ("内容",content) # 调试用
        
        # 写入操作日志
        if (config.dic_config["log_if"] == "1"):
            path_p += "z_log_script.csv"
            args_p["time_run"] = str_split(datetime.datetime.now())
            file_file = inc_file.File_file()
            # 将访问日志字典转化为csv格式
            txt_log = ""
            if (args_p):
                txt_logo = args_p["file"] + "," + args_p["code"] + "," + args_p["output"] + "," + str(args_p["roles"]) + "," +  args_p["time_run"] +  "\n"
                try:
                    file_file.write_add(path_p=path_p,renew_if=0,content_p=txt_log)
                except:
                    pass
                    
        # 结果展示
        if (output == "html"):
            result =content # 调试用
            
        return result
    
    # 用户注册
    def reg_user(self):
    
        result = ""
        username_old = ""
        username_p = ""
        password_p = ""
        password2_p = ""
        connection_p = ""
        username_is = ""
        connection_is = ""
        sql_add = ""
        
        # 提交参数赋值
        
        try:
        
            username_p = self.browser_argument(name_p="username")
            password_p = self.browser_argument(name_p="password")
            password2_p = self.browser_argument(name_p="password2")
            connection_p = self.browser_argument(name_p="connection")
            username_old = username_p
            
        except:
        
            pass
            
        if (username_old == ""):
                result = "<center><br><br><font color=\"#ff0000\">账号名不能为空</font>，请返回重新填写"
                result += "[<a href=\"javascript:history.back();\">返回</a>]</center>"
                return result
                
        if (password_p != password2_p):
                result = "<center><br><br><font color=\"#ff0000\">两次密码不一致</font>，请返回重新填写"
                result += "[<a href=\"javascript:history.back();\">返回</a>]</center>"
                return result
                
        if (len(password_p) < 6):
                result = "<center><br><br><font color=\"#ff0000\">密码长度不能小于6</font>，请返回重新填写"
                result += "[<a href=\"javascript:history.back();\">返回</a>]</center>"
                return result
                
        print ("注册的基础数据：",username_p,password_p,connection_p)# 调试用
        
        if (username_p != ""):
            
            # 字符串识别
            username_is = str_is(username_old)
            connection_is = str_is(connection_p)
            # 尽可能添加可用信息
            if (connection_is == ""):
            
                if (username_is == "mp"):
                    sql_add = "tel='" + username_old + "'"
                elif (username_is == "email"):
                    sql_add = "email='" + username_old + "'"
                elif (username_is == "qq"):
                    sql_add = "qq='" + username_old + "'"
                elif (username_is == ""):
                    result = "<center><br><br>至少要填写<font color=\"#ff0000\">手机号,邮箱,QQ号</font>中的一种作为账号或联系方式，<br>请返回重新填写"
                    result += "[<a href=\"javascript:history.back();\">返回</a>]</center>"
                    return result
            else:
            
                if (connection_is == "mp"):
                    sql_add = "tel='" + connection_p + "'"
                elif (connection_is == "email"):
                    sql_add = "email='" + connection_p + "'"
                elif (connection_is == "qq"):
                    sql_add = "qq='" + connection_p + "'"
            
            #print ("用户注册明文",username_p,password_p) # 调试用
            username_p = hash_make(hash_make(username_p)) #密文处理
            password_p = hash_make(hash_make(password_p)) #密文处理
        
            rs_way_mysql = Conn_mysql(config.dic_config["host_mysql"],config.dic_config["user_mysql"],config.dic_config["pwd_mysql"], "lqab_way_" + config.dic_config["name_mysql_after"], int(config.dic_config["port_mysql"])) # 生成MYSQL数据库way方法实例
            
            sql = "select roles,id from user where username='" + username_p + "'"
            res_m, rows_m = rs_way_mysql.read_sql(sql)

            if (res_m > 0):
                result = "<center><br><br><font color=\"#ff0000\">用户名已经被注册</font>，请返回重新填写"
                result += "[<a href=\"javascript:history.back();\">返回</a>]</center>"
                return result
            else:
            # 插入新用户注册信息
                sql = "insert into user set "
                sql += "username='" + username_p + "',"
                sql += "password='" + password_p + "'"
                if (sql_add != ""):
                    sql += "," + sql_add
                #print ("新增用户操作",sql) # 调试用
                insert_if = rs_way_mysql.write_sql(sql)
                if (insert_if == True):
                    result = "<center><br><br>用户名 <font color=\"#ff0000\">" + username_old + "</font> 注册成功！3秒后跳转至下一页..."
                    result += "<meta http-equiv=\"refresh\" content=\"5;url=\"> </center>"
                print (sql,insert_if) # 调试用
                
            rs_way_mysql.close_cur() #关闭数据游标
            rs_way_mysql.close() #关闭数据连接
            
        return result
        
    # 主执行过程
    def do_it(self,*args):
        
        pass_if = ""
        time_alive = ""
        roles_p = ""
        do_is = ""
        username = ""
        password = ""
        time_login = str_split(datetime.datetime.now())
        dic_login_p = {}
        coin = 0
        username = "客人"
        result = ""
        
        # 业务逻辑开始
        # 基于cookies的自动登录
        pass_if,dic_login_p = self.user_login_check(time_alive_p=config.dic_config["time_alive"])
        #print (dic_login_p) # 调试用
        if (dic_login_p):
        
            roles_p = dic_login_p["roles"]
            coin = dic_login_p["coin"]
            username = dic_login_p["username"]
            
        try:
        
            do_is = self.browser_argument(name_p="do_is")
            username = self.browser_argument(name_p="username")
            password = self.browser_argument(name_p="password")
            print ("认证登录数据：",do_is,username,password)# 调试用
            
        except:
        
            pass
        
        # 账户找回
        if (do_is == "userback"):
            result = "<center><br><br>"
            result += """
            <a target="_blank" href="//shang.qq.com/wpa/qunwpa?idkey=d673c782e031974dbe72277ea033980d7a4a942fc533289b106e8fd11a7f6c1b"><img border="0" src="//pub.idqqimg.com/wpa/images/group.png" alt="丽华抗癌客服1群" title="丽华抗癌客服1群"></a>
            """
            result += "<br><br>请加QQ群 <font color=\"#ff0000\">694373542</font>，人工申诉找回账号。" 
            if (result != ""):
                self.write (result)
        # 登录处理
        if (do_is == "check_user_login"):
            pass_if,roles_p = self.user_login_do(username_p=username,password_p=password,cookie_if=1)
        # 注册处理
        if (do_is == "reg_user"):
            result = self.reg_user()
            if (result != ""):
                self.write (result)
        # 登录退出处理
        if (do_is == "logout"):
            self.sys_logout(list_p=["session_lqab_user"])
            pass_if = False
        # 执行性请求
        if (do_is == "file_do"):
            result = self.file_do(roles_p=roles_p)
            if (result != ""):
                self.write (result)
        
        
        #print ("是否为注册管理员：",pass_if,"权限：",roles_p) # 调试用
        
        # 重新登录
        if (pass_if is False and result == ""):
        
            result = "<meta http-equiv=\"refresh\" content=\"0;url=statics/web/user_login.html\">"
            self.write (result)
            
        # 进入后台管理
        if (pass_if is True and result == ""):
            
            self.render('user.html',
            name_soft=config.dic_config["name_soft"],
            type_soft=config.dic_config["type_soft"],
            vol_soft=config.dic_config["vol_soft"],
            authority_soft=config.dic_config["authority_soft"],
            author_soft=config.dic_config["author_soft"],
            qq_group=config.dic_config["qq_group"],
            tel_lqab=config.dic_config["tel_lqab"],
            url_lqab=config.dic_config["url_lqab"],
            user_roles=self.user_power_is(roles_p),
            logintime_last=time_login,
            username_p = username,
            coin_p = coin
            )
            
        return do_is
    
    # get方式登录
    def get(self):
        self.do_it()
    
    # post方式登录
    def post(self):
        self.do_it()
        
# 后台用户模块
class AdminHandler(BaseHandler):

    # 主执行过程
    def do_it(self,*args):
        
        pass_if = ""
        time_alive = ""
        roles_p = ""
        do_is = ""
        username = ""
        password = ""
        time_login = str_split(datetime.datetime.now())
        dic_login_p = {}
        aid_p = 0 # 管理员ID
        
        # 业务逻辑开始
        # 基于cookies的自动登录
        pass_if,dic_login_p = self.admin_login_check(time_alive_p=config.dic_config["time_alive"])
        
        print ("cookies字典",dic_login_p) # 调试用
        
        if (dic_login_p):
            roles_p = dic_login_p["roles"]
            username = dic_login_p["username"]
        
        try:
            do_is = self.browser_argument(name_p="do_is")
            if (self.browser_argument(name_p="username")):
                username = self.browser_argument(name_p="username")
            if (self.browser_argument(name_p="password")):
                password = self.browser_argument(name_p="password")
            print ("认证登录数据：",do_is,username,password)# 调试用
        except:
            pass
        
        # 登录处理
        if (do_is == "check_admin_login"):
            pass_if,roles_p,aid_p= self.admin_login_do(username_p=username,password_p=password,cookie_if=1)
            dic_login_p["aid"] = aid_p # 获得管理员ID
            
        if (do_is == "logout"):
            self.sys_logout(list_p=["session_lqab_admin"])
            pass_if = False
        
        print ("是否为注册管理员：",pass_if,"权限：",roles_p) # 调试用
        
        # 重新登录
        if (pass_if is False):
        
            self.render('login_admin.html',
            name_soft=config.dic_config["name_soft"],
            type_soft=config.dic_config["type_soft"],
            vol_soft=config.dic_config["vol_soft"],
            )
            
        # 进入后台管理
        else:
            
            self.render('admin.html',
            name_soft=config.dic_config["name_soft"],
            type_soft=config.dic_config["type_soft"],
            vol_soft=config.dic_config["vol_soft"],
            authority_soft=config.dic_config["authority_soft"],
            author_soft=config.dic_config["author_soft"],
            qq_group=config.dic_config["qq_group"],
            tel_lqab=config.dic_config["tel_lqab"],
            url_lqab=config.dic_config["url_lqab"],
            admin_roles=self.admin_power_is(roles_p),
            logintime_last=time_login,
            username=username
            )
            
        return do_is
    
    # get方式登录
    def get(self):
        self.do_it()
    
    # post方式登录
    def post(self):
        self.do_it()
        


#APi模块 强调速度 系统核心服务模块
class Api(BaseHandler):
    
    def do_it(self):
    
        file_p = ""
        result = ""
        
        try:
            file_p = self.browser_argument(name_p="file")
            #self.write (file) #调试用
        except:
            pass
        
        result = self.import_do(file_p=file_p,args_p=self.request.arguments) # 获得动态执行模块结果
        
        self.write(result)
        
    # get方式登录
    def get(self):
        self.do_it()
    
    # post方式登录
    def post(self):
        self.do_it()

# 寄生脚本处理 模仿文件型脚本调用调用
class ScriptHandler(BaseHandler):
    
    # 权限检查
    def roles_chk(self,file_p="",code_p="",roles_p=""):
        
        pass_if = False
        
        rs_sqlite_file = Conn_sqlite3(config.path_main + config.dic_config["path_sqlite"],0)
        sql = "select id from menu_list "
        sql += "where file_name ='" + file_p + "." + code_p + "' "
        sql += "and admin like '%-"+ roles_p + "-%' "
        res, rows = rs_sqlite_file.read_sql(sql)
        print("权限查询语句：",sql) #调试用
        if (res > 0):
            pass_if = True
            
        rs_sqlite_file.close_cur() # 关闭数据库游标
        rs_sqlite_file.close() # 关闭数据库连接
            
        return pass_if
    
    # 动态执行内容获取
    def content_get(self,roles_p="",file_p="",code_p="",args_p=""):
        
        result = ""
        pass_if =  True
        #1 权限检查
        pass_if = self.roles_chk(file_p=file_p,code_p=code_p,roles_p=roles_p)
        if (pass_if is False):
            result = "管理员操作权限不匹配或权限表故障"
            return result
        
        # 获得脚本文件名    
        try:
            file_p = self.browser_argument(name_p="file")
            #self.write (file) #调试用
        except:
            pass
        try:
            print ("脚本文件路径：",file_p,"参数字典：",args_p) # 调试用
        except:
            pass
            
        result = self.import_do(file_p=file_p,args_p=args_p) # 获得动态执行模块结果
            
        return result
        
    # 主执行过程
    def do_it(self,*args):
        
        roles_p = "" # 权限值初始化
        file_p = "" # 请求功能模块名
        code_p = "" # 请求功能模块名
        output = "" # 请求结果的输出方式
        time_now_p = str_split(datetime.datetime.now()) # 请求时间
        path_p = config.path_main + "data\\log\\"
        dic_t = {}
        str_log = ""
        args_p = {}
        
        # 取得web端提交参数
        dic_t = self.request.arguments
        for x in dic_t:
            try:
                args_p[x] = dic_t[x][0].decode('utf-8')
            except:
                pass
            
        
        # 登录校验
        pass_if,dic_login_p = self.admin_login_check(time_alive_p=config.dic_config["time_alive"])
        
        if (pass_if is False):
        
            self.render('login_admin.html',
            name_soft=config.dic_config["name_soft"],
            type_soft=config.dic_config["type_soft"],
            vol_soft=config.dic_config["vol_soft"],
            )
            
        # 参数处理
        
        roles_p = dic_login_p["roles"]
        try:
            file_p = self.browser_argument(name_p="file")
            code_p = self.browser_argument(name_p="code")
            output = self.browser_argument(name_p="output")
        except:
            pass
        print ("脚本调用参数",roles_p,file_p,code_p,output) # 调试用
        
        # 业务处理
        args_p["roles"] = roles_p # 追加操作权限参数
        if ("aid" in dic_login_p):
            args_p["aid"] = str(dic_login_p["aid"]) # 追加管理员ID
            
        content = self.content_get(roles_p=roles_p,file_p=file_p,code_p=code_p,args_p=args_p)
        
        # 写入操作日志
        if (config.dic_config["log_if"] == "1"):
        
            path_p += "z_log_script.csv"
            args_p["time_run"] = str_split(datetime.datetime.now()).encode('utf_8')
            file_file = inc_file.File_file()
            
            # 将访问日志字典转化为csv格式
            txt_log = ""
            
            #print ("基础参数字典",args_p) # 调试用
            print ("日志路径",path_p) # 调试用
            
            if (args_p):

                try:
                    txt_log = args_p["file"][0] + "," + args_p["code"][0] + "," + args_p["output"][0] + "," + args_p["roles"] + "," +  args_p["time_run"] +  "\n"
                    file_file.write_add(path_p=path_p,renew_if=0,content_p=txt_log)
                except:
                    pass
                    
        # 结果展示
        if (output == "html"):
            self.write(content) # 调试用
        
    def get(self,*args):
    
        self.do_it()
        
    def post(self,*args):

        self.do_it()
            
#内部数据调用模块
class Open(BaseHandler):

    def get_input(self):
        
        result = ""
        id = ""
        action = ""
        
        try:
            id = self.browser_argument(name_p="id")
        except:
            result = "Id is null!"
            
        try:
            action = self.browser_argument(name_p="action")
        except:
            action = "open_page" 
            
        #self.write (q) #调试用
        if (action == "open_page"):

            sql = "select title,content from page where id=" + id
            res,rows = rs_basedata_mysql.read_sql(sql)
            if (res < 1):
                return "数据不存在或数据库读取错误"
            else:
                result += "<h4>" + rows[0][0] + "</h4>" 
                result += "<div style=\"width:398px\">" + rows[0][1] + "</div>"
                
        return result
        
    def get(self):
        self.write(self.get_input())
        
    def post(self):
        self.write(self.get_input())

def main():
    print("")

if __name__ == "__main__":
    main()
