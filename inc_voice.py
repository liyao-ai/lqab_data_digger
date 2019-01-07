#!/usr/bin/env python
# -*- coding: UTF-8 -*-  


#--------- 外部模块处理<<开始>> ---------#

#-----系统自带必备模块引用-----

import os

#-----系统外部需安装库模块引用-----

from win32com.client import constants
import win32com.client
import pythoncom

# 语音录制
import pyaudio
import wave

#-----DIY自定义库模块引用-----
import config
import diy.inc_sys as inc_sys # DIY系统模块
#--------- 外部模块处理<<结束>> ---------#

#--------- 内部模块处理<<开始>> ---------#

# ---外部参变量处理

# ---全局变量处理

# ---本模块内部类或函数定义区


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 8000
RECORD_SECONDS = 5

def rec(file_name="data\\voice\\test.wav"):

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("开始录音......")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("......录音结束")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(file_name, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

# 语音合成类
class Voice(object):
    
    def __init__(self):
    
        self.speak_do = win32com.client.Dispatch("SAPI.SPVOICE")
    
    def speak_voice(self,txt_p):
        
        if (txt_p == ""):
            self.speak_do.Speak("系统没有反馈")
        else:
            self.speak_do.Speak(txt_p)
            
# 单机运行环境 dic_p 参数字典
def run_it(dic_p={}):
    pass
    
#--------- 内部模块处理<<结束>> ---------#

#---------- 主过程<<开始>> -----------#
dic_note = {
"版权":["LQAB工作室"],
"作者":["集体","吉更"],
"初创时间":["2018年12月"],
"功能":["语音处理模块"],
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
