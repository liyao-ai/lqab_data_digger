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
import json # json控件

#-----系统外部需安装库模块引用-----


#-----DIY自定义库模块引用-----
from diy.inc_sys import * #自定义系统级功能模块 
from diy.inc_conn import * #自定义数据库功能模块

#--------- 外部模块处理<<结束>> ---------#


#--------- 内部模块处理<<开始>> ---------#

# ---外部参变量处理

# ---全局变量处理

import diy.inc_crawler_fast as inc_crawler_fast # 引入快速爬虫模块 用于API解析中间件

sys.path.append("..")

import config #系统配置参数

# ---本模块内部类或函数定义区
class Markbase(object):
    
    # 问题识别决策树法
    def question_if(self,str_p="",action_p="question_if"):
        
        result_p = 0
        
        str_t = ""
        dic_p = {}
        url_p = config.dic_config["url_api"] + "api"
        values = {
                "action":action_p,
                "q":str_p
                    }
        #print (url_p,values,inc_crawler_fast.get_html_post(url_p,values))# 调试用
        
        try:
            dic_p = json.loads(inc_crawler_fast.get_html_post(url_p,values))
        except:
            pass
        
        #print ("结果字典：",dic_p) # 调试用
        
        if (dic_p):
            if ("result" in dic_p):
                result_p = dic_p["result"]
            
        return result_p
        
    # 问主题词识别
    def theme_get(self,str_p="",action_p="mk"):
        
        result_p = 0
        
        str_t = ""
        dic_p = {}
        url_p = config.dic_config["url_api"] + "api"
        values = {
                "action":action_p,
                "q":str_p
                    }
        #print (url_p,values,inc_crawler_fast.get_html_post(url_p,values))# 调试用
        
        try:
            dic_p = json.loads(inc_crawler_fast.get_html_post(url_p,values))
        except:
            pass
        
        #print ("结果字典：",dic_p) # 调试用
        
        if (dic_p):
            result_p = dic_p
            
        return result_p
        
    # 问题意图识别
    def inner_get(self,str_p="",action_p="cf_cnn_bilstm"):
        
        result_p = 0
        
        str_t = ""
        dic_p = {}
        url_p = config.dic_config["url_api"] + "api"
        values = {
                "action":action_p,
                "q":str_p
                    }
        #print (url_p,values,inc_crawler_fast.get_html_post(url_p,values))# 调试用
        
        try:
            dic_p = json.loads(inc_crawler_fast.get_html_post(url_p,values))
        except:
            pass
        
        #print ("结果字典：",dic_p) # 调试用
        
        if (dic_p):
            result_p = dic_p
            
        return result_p

# 问题的标注
class Mark_question(Markbase):
    
    def __init__(self):
        pass
        
# 意图的标注
class Mark_intent(Markbase):
        
    def form_intent(self,i_p=0,j_p=0,c_p=0):
        
        txt = ""
        list_t = []
        
        if (j_p == 1):
        
            txt += "问题分类：<select name=\"intent_" + str(i_p) + "_" + str(j_p) + "\">"
            list_t = [
            "<option  value=\"0\" @X@>n/a</option>",
            "<option  value=\"1\" @X@>实质型</option>",
            "<option  value=\"2\" @X@>非实质型</option>"
            ]
            i = 0
            for x in list_t:
                if (c_p == i):
                    txt += x.replace("@X@","selected = \"selected\"")
                else:
                    txt += x.replace("@X@","")
                i += 1
            txt += "</select>"
            
        if (j_p == 2):
        
            txt += "非实质型分类：<select name=\"intent_" + str(i_p) + "_" + str(j_p) + "\">"
            list_t = [
            "<option  value=\"0\" @X@>n/a</option>",
            "<option  value=\"1\" @X@>礼貌语言</option>",
            "<option  value=\"2\" @X@>情感交流</option>"
            ]
            i = 0
            for x in list_t:
                if (c_p == i):
                    txt += x.replace("@X@","selected = \"selected\"")
                else:
                    txt += x.replace("@X@","")
                i += 1
            txt += "</select>"
            
        if (j_p == 3):
        
            txt += "疑问类型分类：<select name=\"intent_" + str(i_p) + "_" + str(j_p) + "\">"
            list_t = [
            "<option  value=\"0\" @X@>n/a</option>",
            "<option  value=\"1\" @X@>是否型</option>",
            "<option  value=\"2\" @X@>解答型</option>"
            ]
            i = 0
            for x in list_t:
                if (c_p == i):
                    txt += x.replace("@X@","selected = \"selected\"")
                else:
                    txt += x.replace("@X@","")
                i += 1
            txt += "</select>"
            
        if (j_p == 4):
        
            txt += "解答型分类：<select name=\"intent_" + str(i_p) + "_" + str(j_p) + "\">"
            list_t = [
            "<option  value=\"0\" @X@>n/a</option>",
            "<option  value=\"1\" @X@>是什么</option>",
            "<option  value=\"2\" @X@>为什么</option>",
            "<option  value=\"3\" @X@>怎么办</option>",
            "<option  value=\"4\" @X@>指令</option>"
            ]
            i = 0
            for x in list_t:
                if (c_p == i):
                    txt += x.replace("@X@","selected = \"selected\"")
                else:
                    txt += x.replace("@X@","")
                i += 1
            txt += "</select>"
            
        if (j_p == 5):
        
            txt += "知识领域分类：<select name=\"intent_" + str(i_p) + "_" + str(j_p) + "\">"
            list_t = [
            "<option  value=\"0\" @X@>n/a</option>",
            "<option  value=\"1\" @X@>常识</option>",
            "<option  value=\"2\" @X@>诊断</option>",
            "<option  value=\"3\" @X@>治疗</option>",
            "<option  value=\"4\" @X@>生存期</option>",
            "<option  value=\"5\" @X@>花费</option>",
            "<option  value=\"6\" @X@>其它</option>"
            ]
            i = 0
            for x in list_t:
                if (c_p == i):
                    txt += x.replace("@X@","selected = \"selected\"")
                else:
                    txt += x.replace("@X@","")
                i += 1
            txt += "</select>"
            
        return txt
        
# 主题的标注
class Mark_theme(Markbase):
    
    def __init__(self):
        pass
        
# 答案类
class Mark_answer(Markbase):
    
    # 答案抽取
    def extract(self,q_p="",a_p="",action_p="answer_extract_similar"):
        
        result_p = {}
        
        if (q_p.strip() == "" or q_p.strip() == ""):
            return result_p
        
        url_p = config.dic_config["url_api"] + "api"
        values = {
                "action":action_p,
                "q":q_p,
                "answer":a_p
                    }
        #print (url_p,values,inc_crawler_fast.get_html_post(url_p,values))# 调试用
        
        try:
            result_p = json.loads(inc_crawler_fast.get_html_post(url_p,values))
        except:
            pass
        
        #print ("结果字典：",result_p) # 调试用
            
        return result_p
        
# 相似度类
class Mark_similar(Markbase):
    
    # 关键词相似
    def similar_keyword(self,q_p="",a_p="",action_p="similar_shorttxt"):
        
        result_p = {}
        
        if (q_p.strip() == "" or q_p.strip() == ""):
            return result_p
        
        url_p = config.dic_config["url_api"] + "api"
        values = {
                "action":action_p,
                "q":q_p,
                "answer":a_p
                    }
        #print (url_p,values,inc_crawler_fast.get_html_post(url_p,values))# 调试用
        
        try:
            result_p = json.loads(inc_crawler_fast.get_html_post(url_p,values))
        except:
            pass
        
        #print ("结果字典：",result_p) # 调试用
            
        return result_p


def run_it():

    print("") # 调试用

#--------- 内部模块处理<<结束>> ---------#

#---------- 主过程<<开始>> -----------#

def main():

    #1 过程一
    run_it()
    #2 过程二
    #3 过程三
    
if __name__ == '__main__':
    main()
    
#---------- 主过程<<结束>> -----------#