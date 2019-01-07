#!/usr/bin/env python
# -*- coding: UTF-8 -*-  

#--------- 外部模块处理<<开始>> ---------#

#-----系统自带必备模块引用-----
import sys # 处理系统模块
import os # 操作系统模块
import types # 数据类型
import time # 获得系统时间
import datetime # 获得日期
import random # 随机函数
import threading #多线程
import multiprocessing #多进程
import requests # web端到端
import hashlib # 哈希
import base64 # 加解密
import json # json模块
import platform

#-----系统外部需安装库模块引用-----

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QWidget

# 任务栏图标处理 
import ctypes
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")

#-----DIY自定义库模块引用-----
import time
import datetime
import config
import inc_crawler # 爬虫模块
import inc_fun # 特殊函数模块
import diy.inc_sys as inc_sys # DIY系统模块
import diy.inc_conn as inc_conn # 数据库连接系统
import inc_voice # 语音处理模块

#--------- 外部模块处理<<结束>> ---------#


#--------- 内部模块处理<<开始>> ---------#

# ---外部参变量处理

#-----重要系统全局类-----



#-----重要系统全局变量-----

title = config.dic_config["name_soft"] 
title += " " + config.dic_config["vol_soft"] 
title += "  QQ群：" + config.dic_config["qq_group"]
title += "  服务电话：" + config.dic_config["tel_lqab"] + "(9:00 - 16:30)"
title += "  微信：" + config.dic_config["wechat_lqab"]

runs_is = 0 #主窗口被调用模块ID
url_manage = "http://" + config.dic_config["ip"] + ":" + config.dic_config["web_port"]
class_admin = "" #管理员等级
md5_user ="" #登录校验后的用户密钥

URL = "http://openapi.xfyun.cn/v2/aiui"
APPID = "5b42bd46"
API_KEY = "dc10d88378c24f65bcf3cd855c0668c8"
AUE = "raw"
AUTH_ID = "94095d90f4f5523c1a0799a3939bc6fc"
DATA_TYPE = "audio"
SAMPLE_RATE = "16000"
SCENE = "main"
RESULT_LEVEL = "complete"
LAT = "39.938838"
LNG = "116.368624"
#个性化参数，注意需进行两层转义
PERS_PARAM = "{\\\\\\\"auth_id\\\\\\\":\\\\\\\"94095d90f4f5523c1a0799a3939bc6fc\\\\\\\"}"
FILE_PATH = "data\\voice\\"

# ---本模块内部类或函数定义区


# 窗体主类
class Window_main(QMainWindow,QWidget,inc_fun.Window_fun):

    def __init__(self,title_w="测试版xxx",path_icon="img\logo.ico",parent=None):
    
        super(Window_main, self).__init__(parent)
        
        self.id_task = 0 # 子任务初始id号
        self.windowList = [] # 窗口编号列表
        
        #super().__init__() # 调用父类初始化方法
        global runs_is # 执行模块调用次数
        global question_p # 单轮的问题
        global answer_p # 单轮的答案

        self.resize(818,525) # 设置窗口大小
        self.setWindowTitle(title_w) #设置窗口标题
        self.setWindowIcon(QIcon(path_icon))
        #self.setWindowOpacity(1.0) #设置窗体透明度
        self.setGeometry( 112, 88, 818, 525) # 初次打开相对位置
        
        self.createMenu() # 激活菜单
        
        self.createUI() # 激活主交互
        
        self.runUI() # 激活执行结果展示
        
        #首次调用对话主UI界面处理
        self.txt_old = "<br><br><br>==== 以下是人机对话历史记录 ====<hr><br>" + self.chat_old_get()
        self.answer_last = ""
        self.chatUI(self.txt_old) # 支持语音输入的对话框
        self.inputUI(txt="命令：") # 命令输入框
        
        
    def runUI(self,txt=""):
    
        from PyQt5.QtWidgets import QPushButton,QListWidget
        self.run_show_main = QListWidget(self)
        self.run_show_main.resize(538,88)
        self.run_show_main.move(150,103)
        self.run_show_main.addItem("-- 任务执行结果 --")

    def chatUI(self,txt):
        
        self.chat_main = QTextEdit(self)
        self.chat_main.setHtml(txt)
        self.chat_main.resize(538,219)
        self.chat_main.move(150,193)
        
    def inputUI(self,txt=""):
        
        # 提示标识
        self.l1=QLabel(self)
        self.l1.setText(txt)
        self.l1.move(168,423)
        
        # 主输入框
        self.input_main = QLineEdit(self)
        self.input_main.resize(168,28)
        self.input_main.move(210,423)
        
        # 确认按钮
        self.submit_main= QPushButton("确认",self)
        self.submit_main.resize(50,28)
        self.submit_main.move(398,423)
        
        # 重输按钮
        self.submit_clear= QPushButton("重输",self)
        self.submit_clear.resize(50,28)
        self.submit_clear.move(468,423)
        
        # 语音输入按钮
        self.submit_voice_input= QPushButton("语音输入",self)
        self.submit_voice_input.resize(58,28)
        self.submit_voice_input.move(538,423)
        
        # 朗读按钮
        self.submit_voice_out = QPushButton("朗读",self)
        self.submit_voice_out.resize(50,28)
        self.submit_voice_out.move(616,423)
        
        # 槽关系确定
        
        self.submit_clear.clicked.connect(self.submit_clear_do)
        self.submit_main.clicked.connect(self.input_do)
        self.submit_voice_input.clicked.connect(self.voice_input)
        self.submit_voice_out.clicked.connect(self.read_it)
    
    # 菜单栏
    def createMenu(self):
    
        dic_menu ={}
        #menubar = QMenuBar(self)
        rs_sqlite_file = inc_conn.Conn_sqlite3(config.path_main + config.dic_config["path_sqlite"],0) 
        sql = "select classify from menu_classify order by power "
        res,rows = rs_sqlite_file.read_sql(sql)
        
        for row in rows:
            dic_menu[row[0]] = {}
            sql = "select name_run,show_if from menu where classify='" + row[0] + "'"
            res_t,rows_t = rs_sqlite_file.read_sql(sql)
            for x in rows_t:
                dic_menu[row[0]][x[0]]=x[1]
            
        #print (dic_menu) # 调试用
        
        self.menubar = self.menuBar()
        
        # ----- 基础操作管理子菜单 -----
        
        if ("基础操作" in dic_menu):
            
            self.menu = self.menubar.addMenu("基础操作 ")
            
            if ("共享算力" in dic_menu["基础操作"]):
                if (dic_menu["基础操作"]["共享算力"] == 1):
                    #self.menu.addAction('&共享算力', lambda :self.f_do())
                    self.menu.addAction(QAction("共享算力", self, triggered=lambda :self.thread_it(self.slotAdd,self.id_task,"测试")))
                    
            if ("打开任务" in dic_menu["基础操作"]):
                if (dic_menu["基础操作"]["打开任务"] == 1):
                    self.menu.addAction('&打开任务', lambda :QMessageBox.about(self, 'New','内部测试中...'))
                    
            if ("保存任务" in dic_menu["基础操作"]):
                if (dic_menu["基础操作"]["保存任务"] == 1):
                    self.menu.addAction('&保存任务', lambda :QMessageBox.about(self, 'New','内部测试中...'))
                    
            if ("另存任务" in dic_menu["基础操作"]):
                if (dic_menu["基础操作"]["另存任务"] == 1):
                    self.menu.addAction('&另存任务', lambda :QMessageBox.about(self, 'New','内部测试中...'))
                    
            if ("导入数据库" in dic_menu["基础操作"]):
                if (dic_menu["基础操作"]["导入数据库"] == 1):
                    self.menu.addAction('&导入数据库', lambda :QMessageBox.about(self, 'New','内部测试中...'))
                    
            if ("导出数据库" in dic_menu["基础操作"]):
                if (dic_menu["基础操作"]["导出数据库"] == 1):
                    self.menu.addAction('&导出数据库', lambda :QMessageBox.about(self, 'New','内部测试中...'))
                    
            if ("登陆云平台" in dic_menu["基础操作"]):
                if (dic_menu["基础操作"]["登陆云平台"] == 1):
                    self.menu.addAction('&登陆云平台', lambda :QMessageBox.about(self, 'New','内部测试中...'))
                    
            if ("下载云任务" in dic_menu["基础操作"]):
                if (dic_menu["基础操作"]["下载云任务"] == 1):
                    self.menu.addAction('&下载云任务', lambda :QMessageBox.about(self, 'New','内部测试中...'))
                    
            if ("发布云任务" in dic_menu["基础操作"]):
                if (dic_menu["基础操作"]["发布云任务"] == 1):
                    self.menu.addAction('&发布云任务', lambda :QMessageBox.about(self, 'New','内部测试中...'))
                    
            if ("清空历史记录" in dic_menu["基础操作"]):
                if (dic_menu["基础操作"]["清空历史记录"] == 1):
                    self.menu.addAction('&清空历史记录', lambda :QMessageBox.about(self, 'New','内部测试中...'))
        
            self.menu.addSeparator()
        
            self.menu.addAction(QAction("&关闭", self, triggered=qApp.quit)) 
        
        # ----- 数据预处理管理子菜单 -----
        
        if ("数据预处理" in dic_menu):
            
            self.menu = self.menubar.addMenu("数据预处理 ")
            
            if ("数据清理" in dic_menu["数据预处理"]):
                if (dic_menu["数据预处理"]["数据清理"] == 1):
                    self.menu.addAction('&数据清理', lambda :QMessageBox.about(self, 'New','内部测试中...'))
                    
            if ("字典管理" in dic_menu["数据预处理"]):
                if (dic_menu["数据预处理"]["字典管理"] == 1):
                    self.menu.addAction('&字典管理', lambda :QMessageBox.about(self, 'New','内部测试中...'))
                    
            if ("中文分词" in dic_menu["数据预处理"]):
                if (dic_menu["数据预处理"]["中文分词"] == 1):
                    self.menu.addAction('&中文分词', lambda :QMessageBox.about(self, 'New','内部测试中...'))
                    
            if ("过滤停用词" in dic_menu["数据预处理"]):
                if (dic_menu["数据预处理"]["过滤停用词"] == 1):
                    self.menu.addAction('&过滤停用词', lambda :QMessageBox.about(self, 'New','内部测试中...'))
                    
            if ("文本纠错" in dic_menu["数据预处理"]):
                if (dic_menu["数据预处理"]["文本纠错"] == 1):
                    self.menu.addAction('&文本纠错', lambda :QMessageBox.about(self, 'New','内部测试中...'))
                    
            if ("新词发现" in dic_menu["数据预处理"]):
                if (dic_menu["数据预处理"]["新词发现"] == 1):
                    self.menu.addAction('&新词发现', lambda :QMessageBox.about(self, 'New','内部测试中...'))
            
            self.menu.addSeparator()
        
        # ----- 数据挖掘子菜单 -----
        if ("数据挖掘" in dic_menu):
            
            self.menu = self.menubar.addMenu("数据挖掘 ")
            
            if ("爬取数据" in dic_menu["数据挖掘"]):
                if (dic_menu["数据挖掘"]["爬取数据"] == 1):
                    self.menu.addAction('&爬取数据', lambda :self.dialog_open(to_do="爬虫处理"))
                    
            if ("数据抽取" in dic_menu["数据挖掘"]):
                if (dic_menu["数据挖掘"]["数据抽取"] == 1):
                    self.menu.addAction('&数据抽取', lambda :QMessageBox.about(self, 'New','内部测试中...'))
                    
            if ("回归分类" in dic_menu["数据挖掘"]):
                if (dic_menu["数据挖掘"]["回归分类"] == 1):
                    self.menu.addAction('&回归分类', lambda :QMessageBox.about(self, 'New','内部测试中...'))
                    
            if ("SVM分类" in dic_menu["数据挖掘"]):
                if (dic_menu["数据挖掘"]["SVM分类"] == 1):
                    self.menu.addAction('&SVM分类', lambda :QMessageBox.about(self, 'New','内部测试中...'))
                    
            if ("网络分类" in dic_menu["数据挖掘"]):
                if (dic_menu["数据挖掘"]["网络分类"] == 1):
                    self.menu.addAction('&网络分类', lambda :QMessageBox.about(self, 'New','内部测试中...'))
                    
            if ("强化学习" in dic_menu["数据挖掘"]):
                if (dic_menu["数据挖掘"]["强化学习"] == 1):
                    self.menu.addAction('&强化学习', lambda :QMessageBox.about(self, '对抗学习','内部测试中...'))
                    
            if ("对抗学习" in dic_menu["数据挖掘"]):
                if (dic_menu["数据挖掘"]["对抗学习"] == 1):
                    self.menu.addAction('&对抗学习', lambda :QMessageBox.about(self, '对抗学习','内部测试中...'))
                    
            if ("自定义处理" in dic_menu["数据挖掘"]):
                if (dic_menu["数据挖掘"]["自定义处理"] == 1):
                    self.menu.addAction('&自定义处理', lambda :QMessageBox.about(self, 'New','内部测试中...'))
            
            self.menu.addSeparator()
        
        # ----- 精品应用子菜单 -----
        if ("精品应用" in dic_menu):
            
            self.menu = self.menubar.addMenu("精品应用 ")
            
            if ("价格预测" in dic_menu["精品应用"]):
                if (dic_menu["精品应用"]["价格预测"] == 1):
                    self.menu.addAction('&价格预测', lambda :self.script_run(script_name="yes"))
                    
            if ("销量预测" in dic_menu["精品应用"]):
                if (dic_menu["精品应用"]["销量预测"] == 1):
                    self.menu.addAction('&销量预测', lambda :QMessageBox.about(self, 'New','内部测试中...'))
                    
            if ("用户画像" in dic_menu["精品应用"]):
                if (dic_menu["精品应用"]["用户画像"] == 1):
                    self.menu.addAction('&用户画像', lambda :QMessageBox.about(self, 'New','内部测试中...'))
                    
            if ("个性化推荐" in dic_menu["精品应用"]):
                if (dic_menu["精品应用"]["个性化推荐"] == 1):
                    self.menu.addAction('&个性化推荐', lambda :QMessageBox.about(self, 'New','内部测试中...'))
                    
            if ("客服问答" in dic_menu["精品应用"]):
                if (dic_menu["精品应用"]["客服问答"] == 1):
                    self.menu.addAction('&客服问答', lambda :QMessageBox.about(self, 'New','内部测试中...'))
                    
            if ("信用评估" in dic_menu["精品应用"]):
                if (dic_menu["精品应用"]["信用评估"] == 1):
                    self.menu.addAction('&信用评估', lambda :QMessageBox.about(self, 'New','内部测试中...'))
                    
            if ("自定义应用" in dic_menu["精品应用"]):
                if (dic_menu["精品应用"]["自定义应用"] == 1):
                    self.menu.addAction('&自定义应用', lambda :QMessageBox.about(self, 'New','内部测试中...'))
        
            self.menu.addSeparator()
        
        # ----- 运行状态子菜单 -----
        if ("运行状态" in dic_menu):
            
            self.menu = self.menubar.addMenu("运行状态 ")
            
            if ("系统信息" in dic_menu["运行状态"]):
                if (dic_menu["运行状态"]["系统信息"] == 1):
                    self.menu.addAction('&系统信息', lambda :self.sys_do(to_do="系统信息"))
                    
            if ("系统测试" in dic_menu["运行状态"]):
                if (dic_menu["运行状态"]["系统测试"] == 1):
                    self.menu.addAction('&系统测试', lambda :self.sys_do(to_do="系统测试"))
                    
            if ("本地批处理" in dic_menu["运行状态"]):
                if (dic_menu["运行状态"]["本地批处理"] == 1):
                    self.menu.addAction('&本地批处理', lambda :QMessageBox.about(self, 'New','内部测试中...'))
                    
            if ("远端批处理" in dic_menu["基础操作"]):
                if (dic_menu["基础操作"]["远端批处理"] == 1):
                    self.menu.addAction('&远端批处理', lambda :QMessageBox.about(self, 'New','内部测试中...'))
                    
            if ("GUI查询" in dic_menu["运行状态"]):
                if (dic_menu["运行状态"]["GUI查询"] == 1):
                    self.menu.addAction('&GUI查询', lambda :QMessageBox.about(self, 'New','内部测试中...'))
                    
            if ("WEB查询" in dic_menu["运行状态"]):
                if (dic_menu["运行状态"]["WEB查询"] == 1):
                    self.menu.addAction('&WEB查询', lambda :QMessageBox.about(self, 'New','内部测试中...'))
            
            self.menu.addSeparator()
        
        # ----- 参数调节子菜单 -----
        if ("参数调节" in dic_menu):
            
            self.menu = self.menubar.addMenu("参数调节 ")
            
            if ("回归模型" in dic_menu["参数调节"]):
                if (dic_menu["参数调节"]["回归模型"] == 1):
                    self.menu.addAction('&回归模型', lambda :QMessageBox.about(self, 'New','内部测试中...'))
                    
            if ("SVM模型" in dic_menu["参数调节"]):
                if (dic_menu["参数调节"]["SVM模型"] == 1):
                    self.menu.addAction('&SVM模型', lambda :QMessageBox.about(self, 'New','内部测试中...'))
                    
            if ("网络模型" in dic_menu["参数调节"]):
                if (dic_menu["参数调节"]["网络模型"] == 1):
                    self.menu.addAction('&网络模型', lambda :QMessageBox.about(self, 'New','内部测试中...'))
                    
            if ("强化模型" in dic_menu["参数调节"]):
                if (dic_menu["参数调节"]["强化模型"] == 1):
                    self.menu.addAction('&参数调节', lambda :QMessageBox.about(self, 'New','内部测试中...'))
                    
            if ("对抗模型" in dic_menu["参数调节"]):
                if (dic_menu["参数调节"]["对抗模型"] == 1):
                    self.menu.addAction('&对抗模型', lambda :QMessageBox.about(self, 'New','内部测试中...'))
                    
            if ("自定义模型" in dic_menu["参数调节"]):
                if (dic_menu["参数调节"]["自定义模型"] == 1):
                    self.menu.addAction('&自定义模型', lambda :QMessageBox.about(self, 'New','内部测试中...'))
        
            self.menu.addSeparator()
        
        # ----- 帮助子菜单 -----
        
        if ("帮助" in dic_menu):
        
            self.menu = self.menubar.addMenu("帮助 ")
            
            if ("爬取数据" in dic_menu["帮助"]):
                if (dic_menu["基础操作"]["帮助"] == 1):
                    self.menu.addAction(QAction("快速入门", self, triggered=lambda :os.system(os.path.abspath('') + "\\readme.md")))
                    
            if ("爬取数据" in dic_menu["帮助"]):
                if (dic_menu["基础操作"]["帮助"] == 1):
                    self.menu.addAction(QAction("官方主页", self, triggered=lambda :self.thread_it(self.result_onekey, "一键处理")))
                    
            if ("爬取数据" in dic_menu["帮助"]):
                if (dic_menu["基础操作"]["帮助"] == 1):
                    self.menu.addAction(QAction("在线支持", self, triggered=lambda :self.thread_it(self.test,"执行测试")))
                    
            if ("爬取数据" in dic_menu["帮助"]):
                if (dic_menu["基础操作"]["帮助"] == 1):
                    self.menu.addAction(QAction("版本说明", self, triggered=lambda :self.thread_it(self.test,"执行测试")))
                    
            if ("爬取数据" in dic_menu["帮助"]):
                if (dic_menu["基础操作"]["帮助"] == 1):
                    self.menu.addAction(QAction("友情资助", self, triggered=lambda :self.thread_it(self.test,"执行测试")))
        
            self.menu.addSeparator()
        
        rs_sqlite_file.close() # 关闭数据库连接
        
    # 读取对话

    # 主显示界面
    def createUI(self):
    
        txt = "" # 空白文本
        self.Dialog_thread = QtWidgets.QWidget()
        self.textBrowser_thread = QtWidgets.QTextBrowser(self.Dialog_thread)
        self.textBrowser_thread.setObjectName("textBrowser")
        with open("backgroud.html", "r",encoding="UTF-8") as f:
            txt = f.read(4194304)
        self.textBrowser_thread.setHtml(txt) #最多读取32M大小的历史记录文件
        
        if (runs_is == 0):
            self.setCentralWidget(self.textBrowser_thread)
    
    # 打开对话框
    def dialog_open(self,**dic_args):
        
        if ("to_do" in dic_args):
            to_do = dic_args["to_do"]
        else:
            to_do = "n/a"
            
        the_dialog = Dialog_main(to_do=to_do)
        if (the_dialog.exec_() == QDialog.Accepted):
            pass
            
        return to_do
        
    # 打开新界面
    def show_second_windows(self,**dic_args):
        
        if ("to_do" in dic_args):
            to_do = dic_args["to_do"]
        else:
            to_do = "n/a"
            
        the_window =SecondWindow(to_do=to_do)
        self.windowList.append(the_window)   ##注：没有这句，是不打开另一个主界面的！
        self.close()
        the_window.show()
        
        return to_do
        
    # 输入操作
    def input_do(self):
        
        self.txt_old = "<br><br><br>==== 以下是历史记录 ====<hr><br>" + self.chat_old_get()
        
        action_p = ""
        result = ""
        q_p = self.input_main.text().strip()
        try:
            action_p = self.order_recognise(txt_p=q_p)
        except:
            pass
        
        # 系统测试
        if (action_p == "info_sys"):
            result = self.sys_do(to_do="系统信息")
        
        # 系统测试
        if (action_p == "test_sys"):
            result = self.sys_do(to_do="系统测试")

        # 爬虫
        if (action_p == "crawler"):
            result = self.dialog_open(to_do="爬虫处理")
             # 调用对话框
            
        # 载入等待界面
        #self.thread_it(self.loading_show,"")
        # 获得问答结果
        #self.get_answer()
        content = "<div><div>" + str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())) + "</div>"
            
        # 写入对话日志
        if (result.strip() != ""):
        
            content += "<div>[ " +q_p + " ]</div><div>" + result + "</div>"
            
        else:
        
            content += "<div>[ " +q_p + " ]</div><div>" + "系统未能识别，请稍后再试......" + "</div>"
        
        content += "</div>\n" 
        with open("chat.html", "a+",encoding="utf-8") as f:
            f.write(content)
            
        
        self.chat_main.setHtml(content + self.txt_old)
        
            
    @staticmethod
    def thread_it(func, *args):
        t = threading.Thread(target=func, args=args) 
        t.setDaemon(True)   # 守护--就算主界面关闭，线程也会留守后台运行
        t.start()           # 启动
        # t.join()          # 阻塞--会卡死界面！
        
    def test(self, c):
        
        print ("hello")
    
class window_message(QMainWindow):
    
    def __init__(self,title_w,url_c):
    
        super().__init__() # 调用父类初始化方法
        global runs_is # 执行模块调用次数
        self.resize(800,600) # 设置窗口大小
        self.setWindowTitle(title_w) #设置窗口标题
        self.createUI(url_c)

       
    def createUI(self,url_c_2):
    
        bw = QWebView()
        bw.load(QUrl(url_c_2))
        bw.show()
        self.setCentralWidget(bw)
        
#启动登录菜单类

class LoginDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
    
        QDialog.__init__(self, parent)  
        self.setWindowTitle("<系统登录>" + config.dic_config["name_soft"] + "_" + config.dic_config["type_soft"] + "_" + config.dic_config["vol_soft"] ) 
        self.setWindowIcon(QIcon("..\\img\logo.ico"))
        self.resize(338,158)  
        self.setWindowOpacity(0.99) #设置窗体透明度
        self.leName = QLineEdit(self)  
        self.leName.setPlaceholderText(u'用户名')  
   
        self.lePassword = QLineEdit(self)  
        self.lePassword.setEchoMode(QLineEdit.Password)  
        self.lePassword.setPlaceholderText(u'密码')  
   
        self.pbLogin = QPushButton(u'登录',self)  
        self.pbCancel = QPushButton(u'取消',self)  
   
        self.pbLogin.clicked.connect(self.login)  
        self.pbCancel.clicked.connect(self.reject)  
   
        layout = QVBoxLayout()  
        layout.addWidget(self.leName)  
        layout.addWidget(self.lePassword)  
   
        # 放一个间隔对象美化布局  
        spacerItem = QSpacerItem(20,48,QSizePolicy.Minimum,QSizePolicy.Expanding)  
        layout.addItem(spacerItem)  
   
        # 按钮布局  
        buttonLayout = QHBoxLayout()  
        # 左侧放一个间隔  
        spancerItem2 = QSpacerItem(40,20,QSizePolicy.Expanding,QSizePolicy.Minimum)  
        buttonLayout.addItem(spancerItem2)  
        buttonLayout.addWidget(self.pbLogin)  
        buttonLayout.addWidget(self.pbCancel)  
   
        layout.addLayout(buttonLayout)  
   
        self.setLayout(layout)  
    
    # 登录校验
    def login(self):
    
        global class_admin # 管理员等级
        global md5_user # 管理员MD5值
        username = hash_make(hash_make(self.leName.text()))
        password = hash_make(hash_make(self.lePassword.text()))
        sql = "select roles from user_main where username='" + username + "' and password = '" + password + "' order by id desc limit 0,1"
        res,rows = rs_sqlite.read_sql(sql)
        #print (sql) #调试用
        if( res > 0 ):
            class_admin = rows[0][0]
            md5_user = password
            self.accept()# 关闭对话框并返回1  
        else:  
            QMessageBox.critical(self, u'错误', u'用户名或密码不匹配')  
            
#第二个主界面
class SecondWindow(QMainWindow):
    
    def __init__(self,**dic_args):
    
        super().__init__()
        
        if ("to_do" in dic_args):
            self.title_second_window = dic_args["to_do"]
            self.to_do = dic_args["to_do"]
        else:
            self.title_second_window = "n/a"
            self.to_do = dic_args["to_do"]
            
        self.setWindowTitle(self.title_second_window)
        
        if (self.to_do == "系统信息"):
            self.windows_sys_info()
        
        if (self.to_do == "系统测试"):
            self.windows_sys_test()
    
        # 操作系统信息
    
    # 系统信息窗体
    def windows_sys_info(self):
    
        def windows_info():
            
            txt = "n/a"
            
            info_sys = inc_fun.Info_sys()
            try:
                txt = info_sys.info_windows()
            except Exception as e:
                print (e)

            self.Dialog_thread = QtWidgets.QWidget()
            self.textBrowser_thread = QtWidgets.QTextBrowser(self.Dialog_thread)
            self.textBrowser_thread.setObjectName("textBrowser")
            self.textBrowser_thread.setHtml(txt) #最多读取32M大小的历史记录文件
            self.setCentralWidget(self.textBrowser_thread)

            # 设置状态栏
            self.statusBar().showMessage("当前状态：" + self.to_do)

            # 窗口最大化
            self.showMaximized()
    
        sysstr = platform.system()
        
        if(sysstr =="Windows"):
        
            print ("Call Windows info")
            windows_info()
            
        elif(sysstr == "Linux"):
            print ("Call Linux tasks")
        else:
            print ("Other System tasks")
    
    # 系统测试窗体
    def windows_sys_test(self):
    
        txt = ""
        
        test_sys = inc_fun.Test_sys()
        try:
            txt = test_sys.test_windows()
        except Exception as e:
            print (e)

        self.Dialog_thread = QtWidgets.QWidget()
        self.textBrowser_thread = QtWidgets.QTextBrowser(self.Dialog_thread)
        self.textBrowser_thread.setObjectName("textBrowser")
        self.textBrowser_thread.setHtml(txt) #最多读取32M大小的历史记录文件
        self.setCentralWidget(self.textBrowser_thread)

        # 设置状态栏
        self.statusBar().showMessage("当前状态：" + self.to_do)

        # 窗口最大化
        self.showMaximized()

    ###### 重写关闭事件，回到主界面
    
    def closeEvent(self, event):
        
        self.windowList = []
        window_main = Window_main(title)
        self.windowList.append(window_main)  #主界面调用装载
        window_main.show()
        event.accept()
        
#对话框
class Dialog_main(QDialog):
    
    def __init__(self,**dic_args):
    
        super().__init__()
        
        if ("to_do" in dic_args):
            self.title_dialog = dic_args["to_do"]
            self.to_do = dic_args["to_do"]
        else:
            self.title_dialog = "n/a"
            self.to_do = dic_args["to_do"]
            
        self.setWindowTitle(self.title_dialog) #设置对话框标题

        ### 设置对话框类型
        self.setWindowFlags(Qt.Tool)

# 说明字典
dic_note = {
"版权":["LQAB工作室"],
"作者":["集体","吉更"],
"初创时间":["2018年12月"],
"功能":["GUI模版"],
}
def run_it():

    print("") # 调试用

#--------- 内部模块处理<<结束>> ---------#

#---------- 主过程<<开始>> -----------#

def main():
    inc_sys.version(dic_p=dic_note) #打印版本
    #1 过程一
    run_it()
    #2 过程二
    #3 过程三
    
if __name__ == '__main__':
    main()
    
#---------- 主过程<<结束>> -----------#