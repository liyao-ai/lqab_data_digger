#!/usr/bin/env python
# -*- coding: UTF-8 -*-  


#--------- 外部模块处理<<开始>> ---------#

#-----系统自带必备模块引用-----

import os
import time
import datetime

#-----系统外部需安装库模块引用-----


#-----DIY自定义库模块引用-----

import config
import diy.inc_sys as inc_sys # DIY系统模块
import inc_voice # 语音处理模块

#--------- 外部模块处理<<结束>> ---------#

#--------- 内部模块处理<<开始>> ---------#

# ---外部参变量处理

# ---全局变量处理

# ---本模块内部类或函数定义区


# 窗体功能
class Window_fun(object):

    # 执行结果展示
    def slotAdd(self,id_task=0,action=""):
        
        if (action == "测试"):
        
            self.id_task += 1
            
            for n in range(10):
                
                str_n = "任务" + str(id_task) + 'File index {0}'.format(n)
                self.run_show_main.addItem(str_n)
                #QApplication.processEvents()
            
                time.sleep(1)
    
    # 多线程驱动
    @staticmethod
    def thread_it(func, *args):
        t = threading.Thread(target=func, args=args) 
        t.setDaemon(True)   # 守护--就算主界面关闭，线程也会留守后台运行
        t.start()           # 启动
        # t.join()          # 阻塞--会卡死界面！

    # 脚本内嵌处理
    def script_run(self,script_name=""):
        result_p = ""
        if (script_name != ""):
            result_p = model.model_run(script_name=script_name)
        self.chat_main.append(result_p)
        
    # 标点符号变换处理
    def punctuation_change(self,txt_p=""):
        
        txt_p = txt_p.replace("标点句号","。")
        txt_p = txt_p.replace("标点逗号","，")
        txt_p = txt_p.replace("标点分号","；")
        txt_p = txt_p.replace("标点问号","？")
        txt_p = txt_p.replace("标点叹号","！")
        txt_p = txt_p.replace("标点冒号",":")
        txt_p = txt_p.replace("标点书扩号左","（")
        txt_p = txt_p.replace("标点书扩号右","）")
        txt_p = txt_p.replace("标点书名号左","《")
        txt_p = txt_p.replace("标点书名号右","》")
        txt_p = txt_p.replace("标点破折号","—")
        
        return txt_p
            
    # 语音识别并输入
    def voice_input(self):
        
        result_p = ""
        file_voice = str(datetime.datetime.now()).split(".")[0]
        file_voice = FILE_PATH + file_voice.replace("-","").replace(":","").replace(" ","") + ".wav"
        inc_voice.rec(file_name=file_voice) # 录音
        r = requests.post(URL, headers=self.buildHeader(), data=self.readFile(file_voice))
        dic_p = {}
        
        #txt = txt.Decode("utf-8")
        try:
            txt = r.content.decode()
            dic_p  = json.loads(txt)
            dic_p  = json.loads(r.content)
        except:
            pass
        if (dic_p):
            for x in dic_p["data"]:
                if ("text" in x):
                    result_p += self.punctuation_change(txt_p=x["text"])
                
        self.input_main.setText(result_p)
            
    # 朗读函数
    def read_it(self):
        voice = inc_voice.Voice() # 语音对象实例化
        voice.speak_voice(self.answer_last) # 朗读文本
        
    # 命令识别
    def order_recognise(self,txt_p=""):
    
        action_p = ""
        
        if ("爬虫" in txt_p or "crawler" in txt_p):
            return "crawler"
        
        if ("系统测试" in txt_p):
            return "test_sys"
            
        if ("系统信息" in txt_p):
            return "info_sys"
            
        return action_p
    
    # 系统内部处理
    def sys_do(self,**dic_args):
    
        if ("to_do" in dic_args):
            to_do = dic_args["to_do"]
        else:
            to_do = "n/a"
        result = self.show_second_windows(to_do=to_do)
        return result
        
    # 显示loading
    def loading_show(self,args=""):
        self.chat_main.setText("装载中...")
            
    # 通过爬虫获得webAPI接口答案
    def get_answer(self,args=""):
    
        q_p = self.input_main.text() #获取输入文本
        result = "" # 处理结果
        #QMessageBox.about(self, 'New',self.input_main.text()) # 调试用
        
        url_p = config.dic_config["ip"] + ":" + config.dic_config["web_port"] + "/api"
        values = {
                "action":"api",
                "q":q_p
                    }
        print(url_p,values) # 调试用

        try:
            result = inc_crawler.get_html_post(url_p,values)
            self.answer_last = result
            result = result.replace("\n","").replace("&nbsp"," ")
        except:
            pass
            
        return result
    
    # 对话历史资料获取
    def chat_old_get(self):
        
        list_t = []
        list_t2 = []
        list_last = []
        txt = ""
        result = ""
        with open("chat.html", 'r',encoding='UTF-8') as f:
            txt = f.read()
        if (txt != ""):
            list_t = txt.split("\n")
            if (list_t):
                list_last = sorted(list_t,reverse=True)
                for x in list_last:
                    list_t2 = x.split("</div><div>")
                    m = 0
                    for y in list_t2:
                        result += "<br>" +  y + "<br>"
                        m += 1

        return result
        

    # 重输操作
    def submit_clear_do(self):
    
        #QMessageBox.about(self, 'New','清除') # 调试用
        self.input_main.setText('')
        self.input_main.setFocus()
        
    def buildHeader(self):
    
        curTime = str(int(time.time()))
        param = "{\"result_level\":\""+RESULT_LEVEL+"\",\"auth_id\":\""+AUTH_ID+"\",\"data_type\":\""+DATA_TYPE+"\",\"sample_rate\":\""+SAMPLE_RATE+"\",\"scene\":\""+SCENE+"\",\"lat\":\""+LAT+"\",\"lng\":\""+LNG+"\"}"
        #使用个性化参数时参数格式如下：
        #param = "{\"result_level\":\""+RESULT_LEVEL+"\",\"auth_id\":\""+AUTH_ID+"\",\"data_type\":\""+DATA_TYPE+"\",\"sample_rate\":\""+SAMPLE_RATE+"\",\"scene\":\""+SCENE+"\",\"lat\":\""+LAT+"\",\"lng\":\""+LNG+"\",\"pers_param\":\""+PERS_PARAM+"\"}"
        paramBase64 = base64.b64encode(param.encode('utf-8'))
        paramBase64 = b'eyJhdWUiOiJyYXciLCJzYW1wbGVfcmF0ZSI6IjE2MDAwIiwiYXV0aF9pZCI6Ijk0MDk1ZDkwZjRmNTUyM2MxYTA3OTlhMzkzOWJjNmZjIiwiZGF0YV90eXBlIjoiYXVkaW8iLCJzY2VuZSI6Im1haW4ifQ=='

        m2 = hashlib.md5()
        m2.update(API_KEY.encode() + curTime.encode() + paramBase64)
        checkSum = m2.hexdigest()

        header = {
            'X-CurTime': curTime,
            'X-Param': paramBase64,
            'X-Appid': APPID,
            'X-CheckSum': checkSum,
        }
        return header

    def readFile(self,filePath):
    
        binfile = open(filePath, 'rb')
        data = binfile.read()
        return data
    
    # 附加cmd命令
    def cmd_run(self,file_c):
    
        os.system(file_c) #启动内嵌服务器程序
    
    # 一键处理
    def result_onekey(self,c):
    
        global runs_is
        runs_is += 1
        self.setCentralWidget(self.textedit)
        
        time_start = datetime.datetime.now() #赋值初始时间

        self.textedit.append("<h3> 编号：<font color=\"#ff0000\">" + str(runs_is) + "</font></h3>")
        self.textedit.append("<h4> 模式：<font color=\"#0000ff\">" + c + "</font></h4>")
        self.textedit.append("<h4> 初始时刻 >>> " + str(time_start) + "</h4>")
        
        result = inc_result.result() #一键处理实例化
        self.textedit.append("用户数据示例：")
        self.textedit.append(str(result.data_load_1()))
        self.textedit.append("<br>")
        self.textedit.append("银行数据示例：")
        self.textedit.append(str(result.data_load_2()))
        self.textedit.append("<br>")
        self.textedit.append("浏览行为示例：")
        self.textedit.append(str(result.data_load_3()))
        self.textedit.append("<br>")
        self.textedit.append("账单数据示例：")
        self.textedit.append(str(result.data_load_4()))
        self.textedit.append("<br>")
        self.textedit.append("贷款数据示例：")
        self.textedit.append(str(result.data_load_5()))
        self.textedit.append("<br>")
        self.textedit.append("数据补缺示例：")
        self.textedit.append(str(result.data_load_6()))
        self.textedit.append("<br>")
        self.textedit.append("训练数据示例：")
        self.textedit.append(str(result.data_load_7()))
        self.textedit.append("<br>")
        self.textedit.append("分析结果示例：")
        self.textedit.append(str(result.data_load_8()))
        self.textedit.append("<br>")
        self.textedit.append("最后生成结果文件 >>> " + str(result.data_result_last()))
        
        self.textedit.append("<br>")
        self.textedit.append(">>> " + c + "执行完毕！共耗时：<font color=\"#ff0000\">" + str("%.4f" % self.time_run(time_start)) + "</font> 秒")
        self.textedit.append("<br>------------------------------------------------------------")

    #数据装载
    def data_load(self,c):
    
        self.textedit.append("Hello world")
        
    def file_laod(self,file_name_c,args_c):
        self.setCentralWidget(self.textedit)
        self.textedit.append(">>> python " + runfile_name_c + " " + args_c)
        #os.system("python " + runfile_name_c + " " + args_c)
        os.system("main.pyw")
        
    #打开新窗口
    def window_manage(self,title_w,url_w):
        url_w += "&md5_user=" + md5_user #添加用户操作密钥 
        newWindow = window_message(title_w,url_w)
        newWindow.show()
        newWindow.exec_()
        
    #内嵌浏览器调用
    def browser_load(self,url_c):
        tmp = QWebView()
        tmp.load(QUrl(url_c))
        tmp.show()
        pass
            
    # textedit载入文本型文件
    def load_txt_textedit(self,file_name_c):
        
        self.textedit_main = QTextEdit()
        self.setCentralWidget(self.textedit_main)
    
    # 载入文本型文件
    def load_txt_textBrowser(self,file_name_c):
        
        Dialog_main=QtWidgets.QWidget()
        self.textBrowser_main = QtWidgets.QTextBrowser(Dialog_main)
        self.textBrowser_main.setGeometry(QtCore.QRect(180, 60, 256, 192))
        self.textBrowser_main.setObjectName("textBrowser_main")
        
        self.setCentralWidget(self.textBrowser_main)
    
    # windows系统web后台服务操作
    def web_server_windows(self,action_c):
        if (action_c == "load"):
            self.thread_it(os.system,"python Win_server.py install")
            self.thread_it(os.system,"python Win_server.py --startup auto install")
            self.thread_it(os.system,"python Win_server.py start")
        if (action_c == "unload"):
            self.thread_it(os.system,"python Win_server.py remove")
            self.thread_it(os.system,"python Win_server.py stop")
        if (action_c == "restart"):
            self.thread_it(os.system,"python Win_server.py restart")
            
    # 运行时间
    def time_run(self,starttime):
        endtime = datetime.datetime.now() #赋值结束时间
        endtime = endtime-starttime
        endtime = str(endtime)
        arr_1 = endtime.split(":")
        alltime = 3600*float(arr_1[0]) + 60*float(arr_1[1]) + float(arr_1[2])
        return alltime
        
    # 系统锁定
    def sofeware_lock(self,file_p="config.py",old_save_if=0,key_class=0):
        # 生成密钥
        key_p = "ldaeisok"
        
        if (key_class == 0):
            key_p = code_numb_rand()
        if (key_class == 1):
            key_p = code_char_rand()
        if (key_class == 2):
            if (md5_user != ""):
                key_p = md5_user
        
            
        # 添加锁定操作到加解密记录表
        sql = "INSERT INTO secret set "
        sql += "file_is='" + file_p + "'"
        sql += ",action='sys_lock'"
        sql += ",key_secret='" + key_p + "'"
        
        #print (sql) #调试用
        if (class_admin != ""):
            sql += ",admin_is='-" + class_admin + "-'"
        # 是否保留旧的关键文件
        if (old_save_if == 1):
        
            t = open(file_p, 'r', encoding="utf-8")
            text = t.read()
            #text = text.encode("utf-8")
            t.close()
            text = str(text)
            sql += ",text_old='" + text.replace("'","\\\'") + "'"
            
        else:
        
            sql += ",text_old='nothing'"
        #print (sql) # 调试用
        insert_if = rs_way_mysql.write_sql(sql)
        # 对关键文件进行加密操作
        Secret_base().secret_do(file_p,key_p,secret_if=1)
        
        # 回写操作成功记录到加解密表
        sql = "select last_insert_id() from secret"
        res, rows = rs_way_mysql.read_sql(sql)
        if res> 0:
            id = rows[0][0]
        else:
            id = 0
        sql = "update secret set v1=1  where id=" + str(id) + " and key_secret='" + key_p + "'"
        update_if = rs_way_mysql.write_sql(sql)
        # 后续处理
        QMessageBox.about(self, "系统锁定操作","系统已锁定，***解锁码： " + key_p + " ,请拍照或用纸笔记录,千万不要遗忘！\n解锁命令：python secret.py")
        sys.exit() #退出GUI
        
    @staticmethod
    def thread_it(func, *args):
        t = threading.Thread(target=func, args=args) 
        t.setDaemon(True)   # 守护--就算主界面关闭，线程也会留守后台运行
        t.start()           # 启动
        # t.join()          # 阻塞--会卡死界面！

# 系统信息类
class Info_sys(object):

# windows操作系统信息
    def info_windows(self):

        import psutil #系统信息模块

        import platform #系统平台模块
    
        txt = ""
        enter = "</font><br>"
        mark_1 ="<font style=\"font-size:15px;background:#f2753f;\" color=\"#FFFFFF\">"

        txt += " 开机时间: "+ mark_1  + str(datetime.datetime.fromtimestamp(psutil.boot_time ()).strftime("%Y-%m-%d %H: %M: %S") ) + enter

        txt += " 操作系统名称及版本号："+ mark_1 + platform.platform() + enter   
        txt += " 操作系统版本号:"+ mark_1  + platform.version() + enter
        txt += " 操作系统的位数:"+ mark_1  + str(platform.architecture()) + enter  
        txt += " 计算机类型:"+ mark_1  + platform.machine() + enter
        txt += " 计算机的网络名称:"+ mark_1  + platform.node()  + enter  
        txt += " 计算机处理器信息:"+ mark_1  + platform.processor() + enter


        txt += " cpu逻辑个数: "+ mark_1  + str(psutil.cpu_count()) + enter
        txt += " cpu物理个数: "+ mark_1  + str(psutil.cpu_count(logical=False)) + enter
        mem = psutil.virtual_memory()
        txt += " 内存总数: "+ mark_1  + str(mem.total) + enter
        txt += " 内存信息: "+ mark_1  + str(mem) + enter
        txt += " 网络信息: "+ mark_1  + str(psutil.net_io_counters(pernic=True)) + enter
        txt += " 系统进程ID: "+ mark_1  + str(psutil.pids()) + enter


        import socket #系统socket模块

        localIP = socket.gethostbyname(socket.gethostname())
        txt += " 本地IP:"+ mark_1  + localIP + enter
    
        ipList = socket.gethostbyname_ex(socket.gethostname())
        for i in ipList:
        # 过滤空序列、主机名和localIP（localIP不是业务地址发情况）
            if i and (not isinstance(i, str)) and (i != localIP):  

                for ip in i:
                    txt += " 并列IP:"+ mark_1  + ip + enter
        #MAC地址
        import uuid
        mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
        txt += " MAC地址:"+ mark_1 
        txt += " ".join([mac[e:e+2] for e in range(0,11,2)])
    
        txt += enter 
        txt += " Python的版本号："+ mark_1  + platform.python_version() + enter #显示当前python版本
        txt += ""+ mark_1  + str(platform.python_build()) + enter
        txt += ""+ mark_1  + platform.python_compiler() + enter
        txt += ""+ mark_1  + platform.python_branch() + enter
        txt += ""+ mark_1  + platform.python_implementation() + enter
        txt += ""+ mark_1  + platform.python_revision() + enter
        txt += ""+ mark_1  + str(platform.python_version_tuple()) + enter
    
        import cgi # 声明IIS调用方式
        enter = "<br>"
        for x in os.environ:
            txt += " " + x + ":<font style=\"font-size:15px;background:#f29f3f;\" color=\"#FFFFFF\">" + os.environ.get(x) + "</font>" + enter

        return txt
        
# 系统测试类
class Test_sys(object):

# windows操作系统信息
    def test_windows(self):
        txt = "<div>tensorflow测试</div>"
        
        import tensorflow as tf
        
        txt += "<div>版本：" + str(tf.__version__) + "</div>"
        txt += "<div>路径：" + str(tf.__path__) + "</div>"
        
        with tf.device('/cpu:0'):
            a = tf.constant([1.0,2.0,3.0],shape=[3],name='a')
            b = tf.constant([1.0,2.0,3.0],shape=[3],name='b')
        with tf.device('/gpu:1'):
            c = a+b
   
        #注意：allow_soft_placement=True表明：计算设备可自行选择，如果没有这个参数，会报错。
        #因为不是所有的操作都可以被放在GPU上，如果强行将无法放在GPU上的操作指定到GPU上，将会报错。
        sess = tf.Session(config=tf.ConfigProto(allow_soft_placement=True,log_device_placement=True))
        #sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
        sess.run(tf.global_variables_initializer())
        txt += "<div>GPU计算测试结果：[" 
        for x in sess.run(c):
            txt += str(x) + ","
        txt = txt[:-1]
        txt += "] //显示[2.0,4.0,6.0]是正确的。</div>"
        
        return txt

# 单机运行环境 dic_p 参数字典
def run_it(dic_p={}):
    pass
    
#--------- 内部模块处理<<结束>> ---------#

#---------- 主过程<<开始>> -----------#
# 说明字典
dic_note = {
"版权":["LQAB工作室"],
"作者":["集体","吉更"],
"初创时间":["2018年12月"],
"功能":["特定函数模块"],
}
def main():

    inc_sys.version(dic_p=dic_note) #打印版本
    #1 过程一
    run_it()
    #2 过程二
    #3 过程三
    
if __name__ == '__main__':
    main()
    
#---------- 主过程<<结束>> -----------#
