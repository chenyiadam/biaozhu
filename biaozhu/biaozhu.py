# -*- coding: utf-8 -*-
"""
2022/4/16
CHENYI | YNU
"""

#调用第三方库部分
from ast import Pass
import tkinter as tk
import platform
from tkinter import font, filedialog, ttk, Button
from collections import deque
import os.path
from utils import auto_tagging, init_logger
import json
from utils.colors import color_mapping #提前定义的颜色
from utils.colors_1 import color_mapping_1 #提前定义的颜色
import re
from time import sleep
from tkinter.ttk import Style
from PIL import ImageTk
from PIL import Image
import webbrowser
from  tkinter import messagebox
import os
import sys
from datetime import datetime
# import ttkthemes

logger = init_logger()


#主类
class MyFrame(tk.Frame):
    
    #定义的类参
    def __init__(self, parent):
        super().__init__(parent)
        
        # os.system("python file_B.py " + para_A)
        try:
            self.title = "“火星”实体关系文本标注软件 V1.0-标注界面      管理员:%s   权限:%s" %(sys.argv[1],sys.argv[2])
##            self.title = "“火星”实体关系文本标注软件 V1.0-标注界面      管理员:%s   权限:%s" %("user","123456") 
        except:
            self.title = "“火星”实体关系文本标注软件 V1.0-标注界面      noneuser"
        self._os = platform.system().lower() #小写
        self.parent = parent
        self.file_name = ""
        self.auto_tag = False
        self.history = deque(maxlen=10000000)  # 存储操作历史，最多存储步数
        self.content = ''
        self.no_sel_text = False
        
        self.relationlist = dict()
        # self.relationlist = {k:1 for k,v in self.press_cmd_1.items()}
        self.relationlist["sumlink"] = 0
        
        self.p = r'.\images\guifan.png'
        # self.p1 = r'.\images\jiaochen.png'
        self.url = r'.\utils\火星实体关系文本标注软件教程.html'
        self.url1 = r'.\utils\Brat标注规范.html'
        self.url2 = r'.\utils\KG规范.html'
        
        # 初始的"按键-指令"映射关系
        self.press_cmd = {} # 初始的"实体按键-指令"映射关系
        self.press_cmd_1 = {} # 初始的"关系按键-指令"映射关系
        
        # self.all_keys = "abcdefghijklmnopqrstuvwxyz"
        self.all_keys = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.all_tagged_strings = {}  # 存储所有标注的文本的索引，及其对应的快捷键
        
        # 存储解释快捷键对应含义的Entry的List
        self.entry_list = [] # 存储解释快捷键对应含义的Entry的List
        self.entry_list_1 = [] # 存储解释快捷键对应含义的relation的List
        
        # self.colorlist = list()
        # 存储快捷键名称的Label的List
        self.label_list = [] #存储快捷名
        self.label_list_1 = [] #存储快捷名
        
        # ShortCuts Label
        self.sc_lbl = None
        self.sc_lbl_1 = None
        
        # 显示配置文件名称的下拉列表控件
        self.config_box = None
        self.config_box_1 = None
        # C:\Users\AdamCY\Desktop\yedda-py3-main\ceshi_result.txt
        self.mytxtfile = r"C:\Users\AdamCY\Desktop\yedda-py3-main\ceshi_result.txt"
        #颜色
        self.key_color_mapping = {}
        
        self.key_color_mapping_1 = {}
        self.frame_rows = 20  # 固定行数-整个面板
        self.frame_cols = 8  # 固定列数-整个面板
        self.schema = "BIESO"  # 默认的标注模式，默认有“O” -还可以设置BI；需要其他方式则解码部分需要增加
        
        
        self.config_file = "选实体"#"configs/default.config"
        self.former_cfg_file = self.config_file
        
        self.config_file_1 = "选关系"#"configs/default.config"
        self.former_cfg_file_1 = self.config_file_1
        
        # self.i = 1
        self.rep = r'\[<.*?\⊙'  # 标注后的词语的正则表达式,这个是同来解码匹配的
        
        #--这里修改代码，用来修改添加关系后的情况
        
        self.entity_re = r'\[<.*?\⊙'
        
        # self.entity_re_1 = r'◎\||.*?\||◎(?!|←◎)' # 标注后的关系的正则表达式
        
        
        
        # configure color
        self.select_color = 'light salmon' #'black'   # 光标选中后的文本颜色
        self.word_style = "楷体"  # 待标注文本的字体类型 仿宋
        self.word_size = 12  # 待标注文本的字体大小
        self.weight = "normal"  # 待标注文本的字体不必加粗

        self.parent.title(self.title) #软件显示名称
        self.pack(fill=tk.BOTH, expand=True)

        #构造字典，用来显示
        self.zh = ['病名','病症','其它','药名','诊断方案','治疗方案', "取消标注",'包含','治疗','危险因素','辅助诊断','特征','并发','别名','作用','条件','诊断',"zz1","pp1","ww1"]
        self.en = ['dis','hyp','oth','med','dia','cur',"none", 'Incl','Trea','Risk','Auxi','Char','Conc','Alia','Acti','Cond','Diag',"zzz", "ppp", "www"]
        self.ti = ["A","B","C","D","E","F","Q","I","T","K","U","M","N","L","J","Y","G","Z", "P", "W"]
        self.dic1 = dict(zip(self.ti, self.zh)) 
        self.dic2 = dict(zip(self.en,self.ti ))

#----------------------------------设计视图---------------------------------        


        for idx in range(self.frame_cols): #遍历面板列数
            self.columnconfigure(idx, weight=2)
        self.columnconfigure(self.frame_cols, weight=1)
        self.columnconfigure(self.frame_cols + 1, weight=1)
        for idx in range(self.frame_rows):
            self.rowconfigure(idx, weight=1)
        
        
        # 文档提示信息
        self.lbl = tk.Label(self, text="点按右侧「打开文件」按钮导入文件")
        self.lbl.grid(row=0, column=0, rowspan=1, sticky=tk.W, pady=4, padx=10)
        
        # self.set_shortcuts_layout_relation() ##更新快捷键布局，
        # self.set_shortcuts_layout() ##更新快捷键布局，
        
        # 文档显示设置  #这里更改的字号 self.rest_4()
        self.fnt = font.Font(family=self.word_style, size= self.word_size, weight=self.weight, underline=0)
        self.text = tk.Text(self, font=self.fnt, selectbackground= self.select_color, #"pink", #selectbackground= self.select_color ,
                            bg= 'white' , borderwidth=10,insertbackground = 'red',insertwidth=3, selectforeground='red') #'#F2F2F2'//white #F2F2F2,bg背景颜色，selectbackground-选中颜色
        self.text.insert('1.0', '\n\n\n\n\n\n\n\t\t\t欢迎使用"火星"文本实体标注软件') #, selectforeground='black'
        self.text.grid(row=1, column=0, columnspan=self.frame_cols, #self.frame_cols固定的行数
                       rowspan= self.frame_rows, #控制视图为整列
                       padx=10,
                       sticky=tk.E + tk.W + tk.S + tk.N)
       
        # 为文档显示区添加纵向滚动条
        self.sb = tk.Scrollbar(self)
        self.sb.grid(row=1, column=self.frame_cols, rowspan=self.frame_rows, padx=1,
                     sticky=tk.E + tk.W + tk.S + tk.N)
        self.text['yscrollcommand'] = self.sb.set
        self.sb['command'] = self.text.yview
        # self.save_to_history(text)


#----------------------------------设计功能区---------------------------------  
        #设计标签-相当于显示器
        # lbl = tk.Label(self, text='功能区', foreground="blue", font=(self.word_style, 20, "bold")) # 
        # lbl.grid(row=1, column=self.frame_cols + 1, sticky='w')

        #功能说明
        btn = Button(self, text="标注教程",bg = 'lightskyblue' , command=self.open_jiaochen, width=16) 
        btn.grid(row=1, column=self.frame_cols + 1) #视图最大列的下一列

        #设计按钮-相当于遥控器-点下按钮后，执行open_file功能
        
        btn = Button(self, text="打开文件", bg='red',command=self.open_file, width=16)
        btn.grid(row=2, column=self.frame_cols + 1) #视图最大列的下一列

        #设计格式化内容-format功能-去除多余的换行符-并非是标注取消
        self.format_btn = Button(self, text="格式化",bg = 'lightskyblue' ,command=self.format, width=16)
        self.format_btn.grid(row=2, column=self.frame_cols + 3, pady=4) 

        # #导出文件，即标注好的文件，执行export函数 self.export #原始的方法
        # btn = Button(self, text="导出", bg='red',command=self.export, width=16)
        # btn.grid(row=3, column=self.frame_cols + 3, pady=4)

        #导出文件，即标注好的文件，执行export函数 self.export  #新方法将整个文档导出
        btn = Button(self, text="导出", bg='red',command=self.export_new, width=16)
        btn.grid(row=3, column=self.frame_cols + 3, pady=4)
        
        # #退出程序，这里执行quit文件，系统自带的程序退出，无函数定义 #原始的方法
        # btn = Button(self, text="导出 并退出系统",bg = 'lightskyblue' ,  command=self.tuichu, width=16)
        # btn.grid(row=4, column=self.frame_cols + 3, pady=4)

        #退出程序，这里执行quit文件，系统自带的程序退出，无函数定义 #新方法将整个文档导出
        btn = Button(self, text="导出 并退出系统",bg = 'lightskyblue' ,  command=self.tuichu_new, width=16)
        btn.grid(row=4, column=self.frame_cols + 3, pady=4)
        
        #撤销函数的定义操作
        if len(self.history) < 2:
            self.undo_btn = Button(self, text="撤销",bg = 'lightskyblue' , command=self.undo, width=16, state='disabled')
        else:
            self.undo_btn = Button(self, text="撤销",bg = 'lightskyblue' , command=self.undo, width=16)
        self.undo_btn.grid(row=3, column=self.frame_cols + 1, pady=4)

        #取消标注---该功尚未添加完成--原理，选中内容删除标注还原标注内容，取消高亮,command=self.quxiaobz
        btn = Button(self, text="标注规范",command=self.open_jiaochen2,bg = 'lightskyblue', width=16) #等待添加-------功能待完善！！！
        btn.grid(row=4, column=self.frame_cols + 1, pady=4)
        
        # 弹出图片,标注规范
        btn = Button(self, text="KG规范",bg = 'lightskyblue' ,command=self.open_jiaochen1, width=16) #等待添加-------功能待完善！！！
        btn.grid(row=1, column=self.frame_cols + 3, pady=4)
        
        # # 一键标注，待完善！
        # btn = Button(self, text="一键标注",command=self.tanchu, width=10) #等待添加-------功能待完善！！！
        # btn.grid(row=6, column=self.frame_cols + 3, pady=4)

        # self.word_size = 15  # 待标注文本的字体大小
        # self.les = tk.StringVar()
        # # # 字号
        # translation1 = 15
        # self.entrya = tk.Entry(self, font='仿宋',width=4, textvariable= self.les)
        # self.entrya.grid(row=5, column= self.frame_cols + 2)
        # self.les.set(translation1)
        
        # #,command= self.rest_4 
        # btn = Button(self, text="默认字号",bg = 'lightskyblue' , width=6) #等待添加-------功能待完善！！！
        # btn.grid(row=5, column=self.frame_cols + 3, pady=4)
        
        
# -------------------------------光标位置信息 -------------------------------

        # 展示光标位置信息（cursor position）
        self.cr_info = tk.Label(self, text=("段落:{0:<4}位置:{1:<3}".format(1, 0)),
                                font=(self.word_style, 10, "bold"))
        self.cr_info.grid(row=0, column=self.frame_cols + 3, pady=4) #设置光标位置信息显示在面板上的位置
        
        # 光标当前位置
        self.cr_psn = '1.0'
        # self.last_cr_psn = list()
        self.msg_lbl = tk.Label(self, text="", anchor='w')
        self.msg_lbl.grid(row=0, column=self.frame_cols+1, sticky=tk.E + tk.W + tk.S + tk.N, pady=4, padx=10)
        #self.frame_rows \ 0
        
# -------------------------------标注操作 -------------------------------        
        # 在Text控件中按下不同的键，绑定对应的操作
        for press_key in self.all_keys: #遍历26个字母
            # 按下时，就进行标注
            self.text.bind(press_key, self.press_key_action) #按钮
            # 标注完成后，需要在释放所按键时删除输入的所按键的字符
            release = "<KeyRelease-" + press_key + ">"
            self.text.bind(release, self.release_key_action) #释放键入的字母
            
        # release = "<KeyRelease-Q>"
        # self.text.bind(release, self.release_key_action) #释放键入的字母
        # if self._os == 'darwin':
        #     self.text.bind('<Control-Key-z>', self.fallback_and_render)
        #     self.text.bind('<Control-Key-u>', self.undo)
        # else:
        #     self.text.bind('<Control-z>', self.fallback_and_render)
        #     self.text.bind('<Control-u>', self.undo)
        
        self.text.bind('<ButtonRelease-1>', self.button_release_1) #bind指代点击
        #鼠标单击后触发函数，触发获取光标位置的函数，每次点击都会触发！

        
        self.set_shortcuts_layout_relation() ##更新快捷键布局，
        self.set_shortcuts_layout() ##更新快捷键布局，
        
#----------------------类参到此结束，代码开始传递到布局部分---------------------- 
#----------------------类参到此结束，代码开始传递到布局部分----------------------       
    
    # def rest_4(self):
    #         content = self.entrya.get()
    #         logger.info(content)
    #         logger.info("输入字号:"+str(content))
    #         # print(content)
    #         path0 = content
    #         try:
    #             if type(int(path0)) == type(2022): 
    #                 self.word_size = int(path0)
    #                 logger.info("1:"+str(self.word_size))
    #                 return int(path0)
    #             else:
    #                 self.word_size = 12
    #                 logger.info("2:"+str(self.word_size))
    #                 return 15
    #         except:
    #             self.word_size = 13
    #             logger.info("3:"+str(self.word_size))
    #             return 15
    
    def tuichu(self): #保存并退出
        try:
            self.export()
            quit()
        except:
            try:
                self.export()
                exit()
            except:
                try:
                    quit()
                except:
                    exit()
    
    def tuichu_new(self): #保存并退出
        try:
            self.export_new()
            quit()
        except:
            try:
                self.export_new()
                exit()
            except:
                try:
                    quit()
                except:
                    exit()
   
#----------------------单击鼠标左键更新位置--------------------
    def button_release_1(self, event):
        """单击鼠标左键的操作"""
        self.cr_psn = self.text.index(tk.INSERT) #tk.INSERT指的是光标所在的位置
        self.last_cr_psn= self.cr_psn
        logger.info(f"更新光标位置:{self.cr_psn}")
        index = self.cr_psn.split('.')
        self.cr_info.config(text=("段落:{0:<4}位置:{1:<3}".format(index[0], index[1])))
        # self.last_cr_psn= self.cr_psn
        # self.last_cr_psn.append(self.cr_psn)

    
#----------------------打开文本文件函数--------------------
    def open_file(self):
        
        logger.info('选择文件')
        ftps = [('all files', '.*'), ('text files', '.txt'), ('ann files', '.ann')]
        dlg = filedialog.Open(self, filetypes=ftps)
        fl = dlg.show()
        logger.info(f'文件名称:{fl}')
        
        if fl:
            # 删除text控件中的内容
            self.text.delete("1.0", tk.END) #如果不写呢？
            # 读取内容并插入text控件
            
            text = self.read_file(fl) #读取内容函数，本函数的下一个函数
            try:
                self.text.insert(tk.END, text)  #在文本框中插入文本
            except:
                self.text.insert('1.0', '') #粘贴文本 或 打开文件
            # 更新显示的文件路径
            try:
                self.set_label("文件位置：" + fl+"\t →→ 点击键盘CapsLock键：英文大写状态 ←←") #更新视图上方的提示，提示内容为路径
            except:
                self.set_label("文件位置：" + "粘贴文本") #更新视图上方的提示，提示内容为路径
            # 更新变量
            self.history = deque(maxlen=10000000)
            self.content = ''
            self.no_sel_text = False
            
            # 初始的"按键-指令"映射关系
            self.press_cmd = {} #存储的按钮，也是英文小写字母 a:dis
            self.press_cmd_1 = {} #
            
            self.all_tagged_strings = {}  # 存储所有标注的文本的索引，及其对应的快捷键
            self.entry_list = []  # 存储解释快捷键对应含义的Entry的List
            self.label_list = []  # 存储快捷键名称的Label的List
            
            self.entry_list_1 = []  # 存储解释快捷键对应含义的Entry的List
            self.label_list_1 = []  # 存储快捷键名称的Label的List
            self.mytxtfile = r"C:\Users\AdamCY\Desktop\yedda-py3-main\ceshi_result.txt"
            self.p = r'.\images\guifan.png'
            # self.p1 = r'./images/jiaochen.png'
            self.url = r'.\utils\火星实体关系文本标注软件教程.html'
            self.url1 = r'.\utils\Brat标注规范.html'
            self.url2 = r'.\utils\KG规范.html'
            # ShortCuts Label
            self.sc_lbl = None
            self.sc_lbl_1 = None
            # self.relationlist = {k:1 for k,v in self.press_cmd_1.items()}
            # self.relationlist = dict()
            # self.relationlist["sumlink"] = 0
            # 显示配置文件名称的下拉列表控件
            self.config_box = None
            self.config_box_1 = None
            
            self.key_color_mapping = {}
            self.key_color_mapping_1 = {}
            self.save_to_history(text)
            
            #插入这里
            # self.set_shortcuts_layout_relation() ##更新快捷键布局，
            # self.set_shortcuts_layout() ##更新快捷键布局，
        #支线任务
        # row = 5
        # self.config_file = "选实体"#"configs/default.config"
        # self.former_cfg_file = self.config_file
        # self.config_file_1 = "选关系"#"configs/default.config"
        # self.former_cfg_file_1 = self.config_file_1
        
        # self.config_box = ttk.Combobox(self,width=5, values=get_cfg_files(), state='readonly') #设置下拉列表的长度
        # self.config_box.grid(row=row + 2, column=self.frame_cols + 2, sticky='w', padx=(0, 6))    
        # self.config_box.set(self.config_file.split(os.sep)[-1])# 默认的配置文件设置
        # self.config_box.bind('<<ComboboxSelected>>', self.on_select)
        
        # self.config_box_1 = ttk.Combobox(self,width=5, values=get_cfg_files1(), state='readonly') #设置下拉列表的长度 #自增
        # self.config_box_1.grid(row=row + 2, column=self.frame_cols + 4, sticky='w', padx=(0, 6)) #自增
        # self.config_box_1.set(self.config_file_1.split(os.sep)[-1]) #自增
        # self.config_box_1.bind('<<ComboboxSelected>>', self.on_select_1) #自增
        
        

    def open_jiaochen(self):
        self.msg_lbl.config(text='稍等,正在打开网址')
        # sleep(2)
        webbrowser.open(self.url, new=2)  # open in new tab
        # self.msg_lbl.config(text='稍等,正在打开网址')
        # sleep(5)
        self.msg_lbl.config(text='打开网址了吗？')
        # p = self.p1
        # image = Image.open(p)
        # image.show()
        # image.close()
    def open_jiaochen2(self):
        self.msg_lbl.config(text='稍等,正在打开网址')
        # sleep(2)
        webbrowser.open(self.url1, new=2)  # open in new tab
        # self.msg_lbl.config(text='稍等,正在打开网址')
        # sleep(5)
        self.msg_lbl.config(text='打开网址了吗？')

    def open_jiaochen1(self):
        self.msg_lbl.config(text='稍等,正在打开网址')
        # sleep(2)
        webbrowser.open(self.url2, new=2)  # open in new tab
        # self.msg_lbl.config(text='稍等,正在打开网址')
        # sleep(5)
        self.msg_lbl.config(text='打开网址了吗？')

#----------------------读取txt文本----------------------
    def read_file(self, file_name):
        try:
            f = open(file_name, "r",encoding="utf-8")
            text = f.read()
            self.file_name = file_name
            self.msg_lbl.config(text='导入成功') 
            return text
        except:
            return ""

#----------------------更新视图上方的提示，提示内容为路径----------------------
    def set_label(self, new_file):
        """更新Label控件的显示内容"""
        try:
            self.lbl.config(text=new_file)
        except:
            self.lbl.config(text="粘贴文本")

#----------------------更新显示的光标位置信息----------------------
    def update_cr_psn(self, cr_psn):
        """更新显示的光标位置信息"""
        psn = cr_psn.split('.')
        cursor_text = ("段落: %s位置: %s" % (psn[0], psn[-1]))
        self.cr_info.config(text=cursor_text)

#----------------------按下一个按键并释放后」的操作----------------------
    def press_then_release(self, event):
        """定义「按下一个按键并释放后」的操作 todo"""
        self.press_key_action(event)

#----------------------按下按钮对应操作----------------------
    def press_key_action(self, event): #传入的是英文字母
        """按下一个键位时，对应的操作"""
        if event.char not in "abcdefghijklmnopqrstuvwxyz":
            press_key = event.char.upper() #转大写
            # print(press_key)
            logger.info(f'捕获按键：{press_key}')
            if (press_key not in self.press_cmd) and (press_key not in self.press_cmd_1) : #如果未定义，就显示是无效的
                self.msg_lbl.config(text=f'无效的快捷键{press_key}')
                logger.info(f'无效的快捷键{press_key}') #下一步，撤销按钮
                # self.text.see("33.48")
                content, all_tagged_strings = self.fallback_action(act_msg=f'撤销键入{press_key}', delete_last=False)
                self.render_text(content, self.cr_psn) # "33.48"  
            # if  press_key == "Q"  :
            #     self.quxiaobz()
            
                return
            content, sel_last, all_tagged_strings = self.tag_text(press_key)
            if not content:
                return
            self.content = content
            self.all_tagged_strings = all_tagged_strings
            # 此时暂不渲染，因为按下键时，已经在最后插入了一个字符
            # 因此，再定义一个后续释放键的操作，用于删除那个新增的字符
        else:
            self.msg_lbl.config(text='请切换到大写状态')
        

 #------------释放按钮操作---------------
    def release_key_action(self, event):
        """定义释放按键的操作，即：删除添加到文本最后的cmd_str"""
        # if event.char  in "abcdefghijklmnopqrstuvwxyz":
        #     return 
        press_key = event.char.upper()
        
        # if press_key == "Q":
        #     self.quxiaobz()
        #     self.save_to_history(self.content, self.all_tagged_strings)
        #     #  press_key
        #     #  press_key = event.char.upper()
            
        if (press_key not in self.press_cmd) and (press_key not in self.press_cmd_1):
            if self.content:  # 说明不是一开始就按错了键
                self.render_text(self.content, all_tagged_strings=self.all_tagged_strings)
            else:  # 如果是一开始就按错了，那就从历史队列中取值
                content, all_tagged_strs = self.fallback_action()
                self.render_text(content)
        else:
            if self.no_sel_text:  # 没有选择文本
                content, all_tagged_strs = self.fallback_action(delete_last=False)
                self.render_text(content, all_tagged_strings=self.all_tagged_strings)
            else:
                self.render_text(self.content, all_tagged_strings=self.all_tagged_strings)
                self.save_to_history(self.content, self.all_tagged_strings)
    

#------------下一个函数的任务之一---------------
    def fallback_action(self, event=None, act_msg=None, delete_last=True,
                        undo=False):
        """回退上一步的操作

        :param event:
        :param act_msg:
        :param delete_last: 是否删除上一步操作
        :param undo: 是否为撤销操作，如果为撤销，则进行两次pop
        :return:
        """
        if event:
            logger.info(event.char)
        if act_msg:
            logger.info(f'{act_msg}')
        if undo:  # 能点击撤销操作按钮，则len(self.history)>2
            self.history.pop()
            content, all_tagged_strings = self.history[-1]
            logger.info(f'历史队列长度：{len(self.history)}')
            return content, all_tagged_strings
        if len(self.history) == 1:
            # 历史队列中只有一个元素，回退后需要将该元素重新填入队列
            # 即，保证历史队列中总有一个元素
            content, all_tagged_strings = self.history[-1]
            logger.info(f'历史队列长度：{len(self.history)}')
            return content, all_tagged_strings
        elif len(self.history) > 1:
            if not delete_last:
                content, all_tagged_strings = self.history[-1]
            else:
                content, all_tagged_strings = self.history.pop()
            logger.info(f'历史队列长度：{len(self.history)}')
            return content, all_tagged_strings
        else:
            logger.error('历史队列为空！')
            raise


#------------返回上一步，撤回功能---------------
    def undo(self):
        # self.i += 1 
        # self.text.see(self.last_cr_psn[-self.i])
        """撤销操作"""
        logger.info("撤销操作")
        content, all_tagged_strings = self.fallback_action(undo=True)
        self.render_text(content, all_tagged_strings=all_tagged_strings)
        self.update_undo_btn()
        


#------------获取文本，格式化任务之一---------------
    def get_text(self):
        """获取Text控件中的所有文本"""
        text = self.text.get("1.0", "end-1c")
        return text

    # def rereplace(self):
    #     # press_key = event.char.upper()
    #     print("写入替换的内容")
    #     pass
    
    # def quxiaobz(self):
    #     # {'bg': '#FFFFFF','fg': 'black'},
    #     print(1111111111111)
    #     try:
    #         # print(SEL_FIRST,SEL_LAST)
    #         print(self.text.index("sel.first"),self.text.index("sel.last")) #background
    #         self.text.tag_config('#FFFFFF',background= "#F5F5DC" )  # 再为标签进行设置 #background=self.select_color
    #             #===============注意要先删除其他的标签. '#FFFFFF',
            
    #         self.text.tag_add("#FFFFFF", self.text.index("sel.first"),self.text.index("sel.last"))
    #         #继续在这里插入函数，字符串替换
    #         # self.save_to_history(self.text)
    #         # save_to_history
    #         self.rereplace()
    #         # for i in colorlist:
    #             # text.tag_add(color, text.index("sel.first"),text.index("sel.last"))
    #             # print(i)
    #             # self.text.tag_remove(i,self.text.index("sel.first"), self.text.index("sel.last"))  # =======变色
    #         # if color !='white':#======white实际上是不进行背景色标注!这样效果最好!!!!!!a trick
    #         #     text.tag_add(color, text.index("sel.first"),text.index("sel.last")) #=======变色
    #         # if color !='#F2F2F2':#======white实际上是不进行背景色标注!这样效果最好
    #         #     text.tag_add("#F2F2F2", text.index("sel.first"),text.index("sel.last"))
    #         # print(text.tag_ranges(color))
    #         # print(11111111111)
    #     except:
    #         print("取消失败")
    
#------------按下按钮，进行标注---------------
    def tag_text(self, command): #传入的是英文字母
        # if command
        """根据键入的命令，对文本进行标注"""
        logger.info('开始标注')
        try:
            sel_first = self.text.index(tk.SEL_FIRST)  # 选定文本的开始位置
            sel_last = self.text.index(tk.SEL_LAST)  # 选定文本的结束位置
            self.no_sel_text = False
            
        except tk.TclError:
            logger.warning('未选择文本，无法进行标注')
            self.msg_lbl.config(text="未选中文本")
            self.no_sel_text = True
            return None, None, None
        former_text = self.text.get('1.0', sel_first)  # 从开始到sel_first的文本
        latter_text = self.text.get(sel_first, "end-1c")  # 从sel_first到最后的文本
        selected_string = self.text.selection_get()  # 选中的文本
        latter_text2 = latter_text[len(selected_string):]
        tagged_str, sel_last = self.tag_and_replace(selected_string, selected_string, command,
                                                    sel_last)
        all_tagged_strs = self.update_all_tagged_strs(command, sel_first, sel_last)
        former_text += tagged_str
        if self.auto_tag:
            logger.info('自动标注后续相同文本')
            content = former_text + auto_tagging(tagged_str, latter_text2)
        else:
            content = former_text + latter_text2
        logger.info('标注完成')
        return content, sel_last, all_tagged_strs


#------------更新索引位置等---------------
    def update_all_tagged_strs(self, key, start_index, end_index):
        # print(key)
        if (key in self.press_cmd) and( key != "Q"):
            """更新all_tagged_strs"""
            
            logger.info('更新已标注索引')
            tagged_str_index = self.history[-1][1].copy()
            tagged_str_index[start_index + '-' + end_index] = key
            # 并把所有的位于此标记后面的、同段落的索引位置全部更新
            new_all_tagged_strs = {}
            label = self.press_cmd[key]
            line_no = start_index.split('.')[0]
            for k in tagged_str_index:
                if k == start_index + '-' + end_index:
                    new_all_tagged_strs[k] = tagged_str_index[k]
                    continue
                if k.startswith(line_no):  # 处于同一行的
                    _s, _e = k.split('-')
                    # 且位于刚刚标记的位置的后面
                    if int(_s.split('.')[1]) > int(start_index.split('.')[1]): #在这里调整实体，后面有关系
                        s = line_no + '.' + str(int(_s.split('.')[1]) + len(label) + 4) #这里也是加,可以调试是len(key)
                        e = line_no + '.' + str(int(_e.split('.')[1]) + len(label) + 4) #这里调整实体
                        new_all_tagged_strs[s + '-' + e] = tagged_str_index[k]
                    else:
                        new_all_tagged_strs[k] = tagged_str_index[k]
                else:
                    new_all_tagged_strs[k] = tagged_str_index[k]
            logger.info('更新完成')
            return new_all_tagged_strs
        
        #调整实体中的取消标注
        if key == "Q":
            """更新all_tagged_strs"""
            
            logger.info('更新已标注索引')
            tagged_str_index = self.history[-1][1].copy()
            tagged_str_index[start_index + '-' + end_index] = key
            # 并把所有的位于此标记后面的、同段落的索引位置全部更新
            new_all_tagged_strs = {}
            label = self.press_cmd[key]
            line_no = start_index.split('.')[0]
            for k in tagged_str_index:
                if k == start_index + '-' + end_index:
                    new_all_tagged_strs[k] = tagged_str_index[k]
                    continue
                if k.startswith(line_no):  # 处于同一行的
                    _s, _e = k.split('-')
                    # 且位于刚刚标记的位置的后面
                    if int(_s.split('.')[1]) > int(start_index.split('.')[1]): #在这里调整实体，后面有关系
                        s = line_no + '.' + str(int(_s.split('.')[1])) #这里，分成两种情况，两种匹配，进行取消
                        e = line_no + '.' + str(int(_e.split('.')[1])) #这里调整取消标注后的序号，先调试颜色，再用正则
                        new_all_tagged_strs[s + '-' + e] = tagged_str_index[k]
                    else:
                        new_all_tagged_strs[k] = tagged_str_index[k]
                else:
                    new_all_tagged_strs[k] = tagged_str_index[k]
            logger.info('更新完成')
            return new_all_tagged_strs
        
        if key in self.press_cmd_1:
            logger.info('更新已标注索引')
            tagged_str_index = self.history[-1][1].copy()
            tagged_str_index[start_index + '-' + end_index] = key
            # 并把所有的位于此标记后面的、同段落的索引位置全部更新
            new_all_tagged_strs = {}
            label_1 = self.press_cmd_1[key]
            line_no = start_index.split('.')[0]
            for k in tagged_str_index:
                if k == start_index + '-' + end_index:
                    new_all_tagged_strs[k] = tagged_str_index[k]
                    continue
                if k.startswith(line_no):  # 处于同一行的
                    _s, _e = k.split('-')
                    # 且位于刚刚标记的位置的后面
                    if int(_s.split('.')[1]) > int(start_index.split('.')[1]):
                        #当本段中后面的文本已经标注时，在前面插入文本，要调整的长度
                        # aak = len(self.relation(self.dic2[label_1]))
                        aak = len(self.result) ##会不会写错了？
                        
                        # 定义一个全局的变量，用来存储长度，就不需要重新调用长度！
                        s = line_no + '.' + str(int(_s.split('.')[1]) + aak + 1)  #在这里调整关系
                        e = line_no + '.' + str(int(_e.split('.')[1]) + aak + 1)  #在这里调整关系
                        new_all_tagged_strs[s + '-' + e] = tagged_str_index[k]
                    else:
                        new_all_tagged_strs[k] = tagged_str_index[k]
                else:
                    new_all_tagged_strs[k] = tagged_str_index[k]
            logger.info('更新完成')
            return new_all_tagged_strs
        
        
        # if  press_key == "Q":
        #     print( press_key)
        #     logger.info('更新已标注索引了吗？？？')
        #     # tagged_str_index = self.history[-1][1].copy()
            # tagged_str_index[start_index + '-' + end_index] = key
            # # 并把所有的位于此标记后面的、同段落的索引位置全部更新
            # new_all_tagged_strs = {}
            # label_1 = self.press_cmd_1[key]
            # line_no = start_index.split('.')[0]
            # for k in tagged_str_index:
            #     if k == start_index + '-' + end_index:
            #         new_all_tagged_strs[k] = tagged_str_index[k]
            #         continue
            #     if k.startswith(line_no):  # 处于同一行的
            #         _s, _e = k.split('-')
            #         # 且位于刚刚标记的位置的后面
            #         if int(_s.split('.')[1]) > int(start_index.split('.')[1]):
            #             #当本段中后面的文本已经标注时，在前面插入文本，要调整的长度
            #             aak = len(self.relation(self.dic2[label_1]))
            #             s = line_no + '.' + str(int(_s.split('.')[1]) + aak + 6)  #在这里调整关系
            #             e = line_no + '.' + str(int(_e.split('.')[1]) + aak + 6)  #在这里调整关系
            #             new_all_tagged_strs[s + '-' + e] = tagged_str_index[k]
            #         else:
            #             new_all_tagged_strs[k] = tagged_str_index[k]
            #     else:
            #         new_all_tagged_strs[k] = tagged_str_index[k]
            # logger.info('更新完成')
        

    def get_replace(self, string, rep):#核心看这里解码
        para = string.strip('\n') #去除两端换行
        ent_list = re.findall(rep, string) #匹配查找，
    
        # print("ent_list",ent_list)
        # print("ok")
    
        para_len = len(para) #看整个句子的长度
        chunk_list = []  # 存储标注过的实体及相关信息
        end_pos = 0
        if not ent_list: #没有找到
            # chunk_list.append([para, 0, para_len, False])
            self.msg_lbl.config(text='匹配失败') 
            return string, 0
        else: #找到了
            for pattern in ent_list:
                start_pos = end_pos + para[end_pos:].find(pattern)
                # print(start_pos)
                end_pos = start_pos + len(pattern)
                chunk_list.append([pattern, start_pos, end_pos, True])

        full_list = []  # 将整个para存储进来，并添加标识（是否为标注的实体）
        for idx in range(len(chunk_list)):
            if idx == 0:  # 对于第一个实体，要处理实体之前的文本
                if chunk_list[idx][1] > 0:  # 说明实体不是从该para的第一个字符开始的,则将前面的无关紧要的加起来
                    full_list.append([para[0:chunk_list[idx][1]], 0, chunk_list[idx][1], False])
                    full_list.append(chunk_list[idx])
                else:
                    full_list.append(chunk_list[idx])
            else:  # 对于后续的实体
                if chunk_list[idx][1] == chunk_list[idx - 1][2]:
                    # 说明两个实体是相连的，直接将后一个实体添加进来
                    full_list.append(chunk_list[idx])
                elif chunk_list[idx][1] < chunk_list[idx - 1][2]:
                    # 不应该出现后面实体的开始位置比前面实体的结束位置还靠前的情况
                    pass
                else:
                    # 先将两个实体之间的文本添加进来
                    full_list.append([para[chunk_list[idx - 1][2]:chunk_list[idx][1]],
                                  chunk_list[idx - 1][2], chunk_list[idx][1],
                                  False])
                    # 再将下一个实体添加进来
                    full_list.append(chunk_list[idx])

            if idx == len(chunk_list) - 1:  # 处理最后一个实体
                if chunk_list[idx][2] > para_len:
                    # 最后一个实体的终止位置超过了段落长度，不应该出现这种情况
                    pass
                elif chunk_list[idx][2] < para_len:
                    # 将最后一个实体后面的文本添加进来
                    full_list.append([para[chunk_list[idx][2]:para_len], chunk_list[idx][2], para_len, False])
                else:
                    # 最后一个实体已经达到段落结尾，不作任何处理
                    pass
                    # print(full_list)
        # print(full_list)
        newstring = ''
        for slist in full_list:
            if slist[3]:
                ent_and_lab = slist[0].strip('[<$\⊙').split('→')
                ent, label = ent_and_lab
                newstring +=  '  '+ent
                for ii in range(len(label)+2):
                    newstring += ' '
            else:
                newstring += slist[0]
        #changelong = len(newstring)
        return newstring #, para_len, changelong
    


    def relation(self, cmd_key):#(关系 关系编号 头尾实体)
        # print(cmd_key)
        # print(self.relationlist)
        # logger.info(str(self.relationlist))
        # logger.info(str(cmd_key))
        self.relationlist[cmd_key] += 1
        self.relationlist["sumlink"] += 1
    
        jisuan = self.relationlist[cmd_key] % 2 +1
        if jisuan == 1 :
            kk =  int(self.relationlist["sumlink"]/2+1)
        else:
            kk =  int(self.relationlist["sumlink"]/2)
            
        logger.info("R"+str(kk)+"_"+cmd_key+str(jisuan))
        return( "R"+str(kk)+"_"+cmd_key+str(jisuan))
            
    def relation_hou(self, cmd_key):#(关系 关系编号 头尾实体)
        # print(cmd_key)
        # print(self.relationlist)
        # logger.info(str(self.relationlist))
        # logger.info(str(cmd_key))
        self.relationlist[cmd_key] += 1
        self.relationlist["sumlink"] += 1
    
        jisuan = self.relationlist[cmd_key] % 2 +1
        if jisuan == 1 :
            kk =  int(self.relationlist["sumlink"]/2+1)
        else:
            kk =  int(self.relationlist["sumlink"]/2)
            
        logger.info("R"+str(kk)+"_"+cmd_key+str(jisuan))
        return( "R"+str(kk)+"_"+cmd_key+str(jisuan))  
        


#------------ 高亮标注文本增加固定格式------------
    def tag_and_replace(self, content, string, cmd_key, index):
        """将content中的string进行标记，并返回最新的content和索引

        :param content: 包含标注内容的字符串，也可以和string相等
        :param string: 标注内容的字符串
        :param cmd_key: 键入的命令
        :param index: string最后一个字符所在的位置
        :return:
        """
        
        if (cmd_key in self.press_cmd) or (cmd_key in self.press_cmd_1):
            # 对文本进行标注
            try: #这里是标注实体
                self.press_cmd[cmd_key]
                if cmd_key == "Q":
                    if ("[<" not in string) or ("⊙" not in string) or (">]" not in string):
                        self.msg_lbl.config(text='未选中实体') 
                    elif (string[0] !="[") or  (string[-1] !="⊙"):
                        self.msg_lbl.config(text='请选择正确区间')   
                    else:
                        #高亮部分 ,开始位置+选中的字符串长度+插入的实体关系名称+插入的固定符号=结束位置,结束位置-1表示最后一个不标注，6-1 = 5
                        colorlist = ["#00FF00",'#3399ff','#00FFFF','#ffff1a','#FF1493','#FF8C00','#cc33ff', '#f5f5dc','#ffff1a','#3399ff','#4dff4d','#ff3300','#ff3399','#cc33ff','#6600ff','#66a3ff','#0086b3','#4da6ff','#4da6ff']
                        for i in colorlist:
                            self.text.tag_remove( i,self.text.index("sel.first"), self.text.index("sel.last"))  # =======变色
                            #print()
                        # if color !='white':#======white实际上是不进行背景色标注!这样效果最好!!!!!!a trick
                        #     # print(text.index("sel.first"),text.index("sel.last"))
                        #     text.tag_add(color, text.index("sel.first"),text.index("sel.last"))
                        
                        newstring = self.get_replace(string, self.rep) #,para_len,changelong
                        # new_string = string
                        new_string = newstring  #在这里匹配正则
                        new_index = index.split('.')[0] + "." + str(int(index.split('.')[1])) 
                        self.last_cr_psn =new_index
                else:
                    if ("→" in string) or ("@" in string) or ("⊙" in string) or ("[<" in string) or (">]" in string):
                        self.msg_lbl.config(text='不允许重叠')
                    else:
                        # new_string = "[<" + string + "→" + self.press_cmd[cmd_key] + ">]◎"
                        new_string = "[<" + string + "→" + cmd_key + ">]⊙"
                        #高亮部分 ,开始位置+选中的字符串长度+插入的实体关系名称+插入的固定符号=结束位置,结束位置-1表示最后一个不标注，6-1 = 5
                        new_index = index.split('.')[0] + "." + str(int(index.split('.')[1]) + len(cmd_key) + 5) 
                        self.last_cr_psn =new_index
            except: #这里是标注关系
                # print(self.relation(self.dic2[self.press_cmd_1[cmd_key]]))
                # logger.info(str(self.relation(self.dic2(self.press_cmd_1[cmd_key]))))
                if string == "⊙": #将relation函数的内容放在这里，不以函数的方式存在，可以解决掉标注的问题
                    
                    # ---------------函数恰入
                    cmd_key = self.dic2[self.press_cmd_1[cmd_key]]
                    self.relationlist[cmd_key] += 1
                    self.relationlist["sumlink"] += 1
                    jisuan = self.relationlist[cmd_key] % 2 +1
                    if jisuan == 1 :
                        kk =  int(self.relationlist["sumlink"]/2+1)
                    else:
                        kk =  int(self.relationlist["sumlink"]/2)
                        logger.info("R"+str(kk)+"_"+cmd_key+str(jisuan))
                    self.result =  "R"+str(kk)+"_"+cmd_key+str(jisuan)
                    # ---------------函数恰入
                    
                    # shubia = self.relation(self.dic2[self.press_cmd_1[cmd_key]])
                    shubia = self.result
                    # if string != "⊙":
                    new_string = "@"+ shubia + string #改为函数
                    new_index = index.split('.')[0] + "." + str(int(index.split('.')[1]) + len(shubia) )  #高亮部分 # + 2
                    self.last_cr_psn = new_index
                else:
                    self.msg_lbl.config(text='请选中⊙标注关系') 
                    # pass
                    # self.undo()
                #(关系 关系编号 头尾实体)
                # new_string = string + "("+cmd_key+self.relation(cmd_key)+ ")◎"  #更改标注格式！！！可以把key改为self.press_cmd_1[cmd_key]
                # new_index = index.split('.')[0] + "." + str(int(index.split('.')[1]) + len(self.press_cmd_1[cmd_key]) + 3) #高亮部分
                # except
            # 更新索引，行索引不变，列索引加上对应的字符数
            
        else:
            logger.warning(f'无效的快捷键{cmd_key}')
            return content, index
        if content == string:
            return new_string, new_index
        else:
            content = content.replace(string, new_string, 1)
            return content, new_index


#------------ 将当前的Text控件的内容存储历史------------
    def save_to_history(self, content='', all_tagged_strings=None):
        """将当前的Text控件的内容存储历史"""
        if all_tagged_strings is None:
            all_tagged_strings = {}
        logger.info(f'写入历史队列')
        self.history.append([content, all_tagged_strings])
        logger.info(f'历史队列元素数量：{len(self.history)}')
        self.update_undo_btn()
        if len(self.history) > 1:
            self.format_btn.config(state='disabled')
        else:
            self.format_btn.config(state='normal')

#------------ 更新undo_btn控件------------
    def update_undo_btn(self):
        """更新undo_btn控件的状态，目前控件一共包括："""
        if len(self.history) < 2:
            self.undo_btn.config(state='disabled')
        else:
            self.undo_btn.config(state='normal')



##------------定义快捷键1布局--------------------
    def set_shortcuts_layout(self):
        """规划「快捷键」的布局"""
        
        #以下是实体的配备标签
        if os.path.isfile(self.config_file): #提示选实体文件，
            try:
                with open(self.config_file, 'r') as fp:
                    self.press_cmd = {k.upper(): v for k, v in json.load(fp).items()} #字典
 
            except Exception:
                self.msg_lbl.config(text='强制配置！')
                logger.critical('配置文件非法')
                logger.info('回退上个配置文件')
                self.config_file = self.former_cfg_file #即重新选择文件
                self.on_select() #重新布局
                # raise InvalidShortcut("非法的配置文件格式")
                
        for k in self.press_cmd: #遍历每一个字母（键）
            if len(k) > 1: #要求快捷键只能是一个字母
                self.msg_lbl.config(text=f"错误！！`{k}:{self.press_cmd[k]}`错误，多个字符")
                logger.critical(f"`{k}:{self.press_cmd[k]}`错误，多个字符")
                logger.info('回退至上一个配置文件')
                self.config_file = self.former_cfg_file
                self.on_select() #重新布局
                # raise InvalidShortcut(f"{k}错误，自定义的快捷键只能是一个字符")
                # logger.critical(f"`{k}:{self.press_cmd[k]}`错误，多个字符")
        
        
        # 因为固定了行数，实体快捷键最多只能展示前10个
        # if len(self.press_cmd) > 10: #self.press_cmd中目前，暂时是所有的实体、关系；看懂后，再配置单独的关系
        #     logger.warning("最多只能展示前10个快捷键")
        
        row = 5
        
        
        # 快捷键提示文本
        map_label = tk.Label(self, text="快键",
                             foreground="#3399ff", font=(self.word_style, 12, "bold"))
        map_label.grid(row=row + 3, column=self.frame_cols + 1, columnspan=2, sticky='w', padx=5)
        
        map_label1 = tk.Label(self, text="实体",
                             foreground="#3399ff", font=(self.word_style, 12, "bold"))
        map_label1.grid(row=row + 3, column=self.frame_cols + 2, columnspan=2, sticky='w', padx=5)
        
        map_label2 = tk.Label(self, text="快键",
                             foreground="#3399ff", font=(self.word_style, 12, "bold"))
        map_label2.grid(row=row + 3, column=self.frame_cols + 3, columnspan=2, sticky='w', padx=5)
        
        map_label2 = tk.Label(self, text="关系",
                             foreground="#3399ff", font=(self.word_style, 12, "bold"))
        map_label2.grid(row=row + 3, column=self.frame_cols + 4, columnspan=2, sticky='w', padx=5)
        # map_label.grid(row=row + 3, column=self.frame_cols + 2, columnspan=2, sticky='w', padx=4)#自增
        
        
        # 销毁已有的控件(Entry和Label)
        if self.entry_list is not None:
            for x in self.entry_list:
                x.destroy()
        if self.label_list is not None:
            for x in self.label_list:
                x.destroy()
        self.entry_list = []
        self.label_list = []
        self.key_color_mapping_1 = {}
        # 更新控件
        
        
        #以下是实体列框构造
        row = 9  # 从第10行开始（索引是9）
        count = 1
        for key in sorted(self.press_cmd): #先将快键字母排序，再遍历
            if count > 11:
                break
            color = color_mapping_1[count - 1]
            # self.colorlist.append(color)
            # todo
            # 给每一种快捷键添加上对应的背景色与前景色
            self.text.tag_config(f'ent-{key}', background=color['bg']) #, foreground=color['fg']
            self.key_color_mapping_1[key] = count - 1 #用作标注时，字体背景色的颜色
            
            #这是实体标签处
            label = tk.Label(self, text=key.upper()+ ":"+ self.dic1[str(key.upper())] , foreground="green", anchor='e',font=(self.word_style, 10,"bold")) #self.word_style,
            label.grid(row=row, column=self.frame_cols+1, columnspan=1, rowspan=2, padx=8) #
            
            self.label_list.append(label)

            #这是实体提示框
            entry = tk.Entry(self,width=4, fg=color['fg'], bg=color['bg'], font=(self.word_style, 8, "bold"))
            entry.insert(0, '') #后面这个参数，可以让实体框有英文字 self.press_cmd[key] 
            entry.grid(row=row, column=self.frame_cols + 2, columnspan=1, rowspan=2)
            self.entry_list.append(entry)
            
            count += 1
            row += 1
        
        while count < 11: #在这里修改  这里其实是未选择文件时的布局
            
            label = tk.Label(self, text=" ", foreground="grey", anchor='e',
                             font=(self.word_style, 10, "bold"))
            label.grid(row=row, column=self.frame_cols+1, columnspan=1, rowspan=2, padx=8)
            self.label_list.append(label)
            
            entry = tk.Entry(self, width=4, fg="black", bg='#a6a6a6', font=(self.word_style, 8,), textvariable=tk.StringVar(value='无'))
            entry.grid(row=row, column=self.frame_cols + 2, columnspan=1, rowspan=2)
            self.entry_list.append(entry)
            
            count += 1
            row += 1
        self.set_combobox()
     
#----------------------关系列布局--------------------------------       
    def set_shortcuts_layout_relation(self):    
        #重复内容
        # zh = ['病名','病症','其它','药名','诊断方案','治疗方案', '包含','治疗','危险因素','辅助诊断','特征','并发','别名','作用','条件','诊断']
        # en = ['dis','hyp','oth','med','dia','cur', 'Incl','Trea','Risk','Auxi','Char','Conc','Alia','Acti','Cond','Diag']
        # ti = ["s","p","h", "d", "a", "r","i", "t", "k", "u", "m", "n", "l", "j", "y", "g"]
        # dic1 = dict(zip(ti,zh)) # + ":"+dic1[str(key)]
        
        if os.path.isfile(self.config_file_1):
            try:
                with open(self.config_file_1, 'r') as fp1:    
                    self.press_cmd_1 = {k.upper(): v for k, v in json.load(fp1).items()}  
                    self.relationlist = {k:1 for k,v in self.press_cmd_1.items()}  
                    self.relationlist["sumlink"] = 0
                    logger.info(str(self.relationlist))
            except Exception:
                self.msg_lbl.config(text='错误！！')
                logger.critical('文件非法')
                logger.info('回退上个配置文件')
                self.config_file_1 = self.former_cfg_file_1
                self.on_select_1()
                # raise InvalidShortcut("非法的配置文件格式")
                
        for k in self.press_cmd_1:
            if len(k) > 1:
                self.msg_lbl.config(text=f"错误！！`{k}:{self.press_cmd_1[k]}`错误，多字符")
                logger.critical(f"`{k}:{self.press_cmd_1[k]}`错误，多字符")
                logger.info('回退上个配置文件')
                self.config_file_1 = self.former_cfg_file_1
                self.on_select_1()
                # raise InvalidShortcut(f"{k}错误，自定义的快捷键只能是一个字符")
                
        # 销毁已有的控件(Entry和Label)
        if self.entry_list_1 is not None:
            for x in self.entry_list_1:
                x.destroy()
        if self.label_list_1 is not None:
            for x in self.label_list_1:
                x.destroy()
        self.entry_list_1 = []
        self.label_list_1 = []
        self.key_color_mapping = {}
        # self.save_to_history(self.text)
        # 更新控件
        
        #以下是关系列
        row = 9  # 从第10行开始（索引是9）
        count = 1
        for key in sorted(self.press_cmd_1):
            if count > 11:
                break
            color = color_mapping[count - 1]
            # self.colorlist.append(color)
            # todo
            # 给每一种快捷键添加上对应的背景色与前景色
            
            self.text.tag_config(f'ent-{key}', background=color['bg']) #, foreground=color['fg']
            self.key_color_mapping[key] = count - 1
            
            #添加关系列
            label1 = tk.Label(self, text=key.upper() + ":" + self.dic1[str(key.upper())], foreground="blue", anchor='e',font=(self.word_style, 10, "bold")) #'Times New Roman'
            label1.grid(row=row, column=self.frame_cols+3, columnspan=1, rowspan=1, padx=8) #
            self.label_list_1.append(label1)
            
            entry1 = tk.Entry(self,width=4, fg=color['fg'], bg=color['bg'], font=(self.word_style, 8, "bold"))
            entry1.insert(0, '') #后面这个参数可以让关系框有英文字 self.press_cmd_1[key]
            entry1.grid(row=row, column=self.frame_cols + 4, columnspan=1, rowspan=1)
            self.entry_list_1.append(entry1)
            
            count += 1
            row += 1
            
        while count < 11:
            label1 = tk.Label(self, text="", foreground="grey", anchor='e',
                             font=(self.word_style, 10, "bold"))
            label1.grid(row=row, column=self.frame_cols + 1, columnspan=1, rowspan=1, padx=8)
            self.label_list_1.append(label1)
            entry1 = tk.Entry(self, width=5, fg="black", bg='#a6a6a6', font=(self.word_style, 8,), textvariable=tk.StringVar(value='无'))
            entry1.grid(row=row, column=self.frame_cols + 4, columnspan=1, rowspan=1)
            self.entry_list_1.append(entry1)
            count += 1
            row += 1
        self.set_combobox_relation()
        
        
        
        
#------------设置下拉实体列表的动作------------
    def set_combobox(self):
        """设置下拉实体列表的动作"""
        row = 5
        if self.sc_lbl is not None:
            self.sc_lbl.destroy()
        if self.config_box is not None:
            self.config_box.destroy()
        # lbl = tk.Label(self, text='快捷键', anchor='w', width=8, foreground="blue", font=(self.word_style, 10, "bold"))
        # lbl.grid(row=row + 1, column=self.frame_cols + 1, sticky='w')
        
        # b=ttk.Separator(root,orient='horizontal')
        # b.pack(fill=tk.X)
        
        self.sc_lbl = tk.Label(self, text="选择模板：", foreground="#3399ff",
                               font=(self.word_style, 12, "bold"), padx=6)
        self.sc_lbl.grid(row=row + 2, column=self.frame_cols + 1, sticky='w')
        
        # 下拉列表控件1-实体
        self.config_box = ttk.Combobox(self,width=5, values=get_cfg_files(), state='readonly') #设置下拉列表的长度
        self.config_box.grid(row=row + 2, column=self.frame_cols + 2, sticky='w', padx=(0, 6))    
        
        # 默认的配置文件设置
        self.config_box.set(self.config_file.split(os.sep)[-1])
        self.config_box.bind('<<ComboboxSelected>>', self.on_select)
        


#------------设置下拉关系列表的动作------------
    def set_combobox_relation(self):
        """设置下拉关系列表的动作"""
        row = 5
        if self.sc_lbl_1 is not None:
            self.sc_lbl_1.destroy()
        if self.config_box_1 is not None:
            self.config_box_1.destroy()
        # lbl = tk.Label(self, text='快捷键', anchor='w', width=8, foreground="blue", font=(self.word_style, 10, "bold"))
        # lbl.grid(row=row + 1, column=self.frame_cols + 1, sticky='w')
        
        # self.sc_lbl_1 = tk.Label(self, text="选择模板：", foreground="#3399ff",
        #                        font=(self.word_style, 10, "bold"), padx=6)
        # self.sc_lbl_1.grid(row=row + 2, column=self.frame_cols + 1, sticky='w')
        
        # 下拉列表控件2-关系
        self.config_box_1 = ttk.Combobox(self,width=5, values=get_cfg_files1(), state='readonly') #设置下拉列表的长度 #自增
        self.config_box_1.grid(row=row + 2, column=self.frame_cols + 4, sticky='w', padx=(0, 6)) #自增
        
        self.config_box_1.set(self.config_file_1.split(os.sep)[-1]) #自增
        self.config_box_1.bind('<<ComboboxSelected>>', self.on_select_1) #自增

#------------设置下拉关系一键全标的动作------------
    def set_combobox_quanbiao(self):
        """设置下拉关系列表的动作"""
        row = 5
        # 下拉列表控件3-一键全标
        pass


#-----------配置文件后，更新实体----------
    def on_select(self, event=None):
        """选择了配置文件后，更新布局"""
        if event:
            logger.info(f"从{event.widget.get()}获取快捷键设置")
            self.former_cfg_file = self.config_file
            self.config_file = os.path.join("configs", event.widget.get())
        else:
            logger.info(f'从{self.config_file}获取配置文件')
        self.set_shortcuts_layout() #更新快捷键布局

#-----------配置文件后，更新布局----------        
    def on_select_1(self, event1=None):
        """选择了配置文件后，更新布局"""
        if event1:
            logger.info(f"从{event1.widget.get()}获取快捷键设置")
            self.former_cfg_file_1 = self.config_file_1
            self.config_file_1 = os.path.join("configs", event1.widget.get())
        else:
            logger.info(f'从{self.config_file_1}获取配置文件')
        self.set_shortcuts_layout_relation() #更新快捷键布局

#--------导出文件按钮执行的内容--------

    def export_1(self): #新的写入方法
        # self.text.window_create("insert", window=self.btn)
        # self.text.insert('end', '\n')
        text_paras, tagged_strings = self.history[-1] #存储的操作历史步数
        text_paras = text_paras.split('\n')
        
        now_time = datetime.now().strftime('%m-%d-%H-%M-%S')
        try:
            new_filename = self.file_name.split('.txt')[0]+'-'+sys.argv[1]+'-'+ now_time + '.anns'
        except:
            try:
                new_filename = self.file_name.split('.txt')[0]+ "-noneuser-" +now_time +'.anns'
            except:
                new_filename = "粘贴文本"+ "-noneuser-" +now_time +'.anns'
        content = self.get_text()
        h = open(new_filename, 'w', encoding='utf-8') #a+
        h.write(content + '\n') #添加到文件夹中的txt
        h.close()
        self.msg_lbl.config(text='结果导出成功')
        # pass
        
    
    def export(self):
        # 按照换行符进行分割，此时仍有空白行，再按段落遍历时去除，此处需要改进，插入特殊符号，以特殊符号切割
        text_paras, tagged_strings = self.history[-1] #存储的操作历史步数
        text_paras = text_paras.split('\n')
        
        now_time = datetime.now().strftime('%m-%d-%H-%M-%S')
        try:
            new_filename = self.file_name.split('.txt')[0]+'-'+sys.argv[1]+'-'+ now_time + '.anns'
        except:
            try:
                new_filename = self.file_name.split('.txt')[0]+ "-noneuser-" +now_time +'.anns'
            except:
                new_filename = "粘贴文本"+ "-noneuser-" +now_time +'.anns'
            
        
        f = open(new_filename, 'w', encoding="utf-8")
        for i in range(len(text_paras)):
            p = text_paras[i]
            p = p.strip()
            if not p:
                continue
            else:
                tagged_words = get_tagged_pairs(p, self.schema, self.entity_re)
                for w in tagged_words:
                    f.write(w)
                if i != len(text_paras) - 1:
                    f.write('\n')
        f.close()
        ent_count = {}
        for i in tagged_strings:
            key = tagged_strings[i]
            if key in ent_count:
                ent_count[key] += 1
            else:
                ent_count[key] = 1
        logger.info(f'实体标注情况：{ent_count}')
        self.msg_lbl.config(text='导出成功')
    
    def export_new(self):
        # 按照换行符进行分割，此时仍有空白行，再按段落遍历时去除，此处需要改进，插入特殊符号，以特殊符号切割
        text_paras, tagged_strings = self.history[-1] #存储的操作历史步数
        # text_paras = text_paras.split('\n')
        
        now_time = datetime.now().strftime('%m-%d-%H-%M-%S')
        try:
            new_filename = self.file_name.split('.txt')[0]+'-'+sys.argv[1]+'-'+ now_time + '.anns'
        except:
            try:
                new_filename = self.file_name.split('.txt')[0]+ "-noneuser-" +now_time +'.anns'
            except:
                new_filename = "粘贴文本"+ "-noneuser-" +now_time +'.anns'
            
        
        f = open(new_filename, 'w', encoding="utf-8")
        # for i in range(len(text_paras)):
        #     p = text_paras[i]
            # p = p.strip()
            # if not p:
            #     continue
            # else:
            #     tagged_words = get_tagged_pairs(p, self.schema, self.entity_re)
            #     for w in tagged_words:
            #         f.write(w)
            #     if i != len(text_paras) - 1:
            #         f.write('\n')
            # f.write(p)
        f.write(text_paras)
        # print(text_paras)
        f.close()
        
        ent_count = {}
        for i in tagged_strings:
            key = tagged_strings[i]
            if key in ent_count:
                ent_count[key] += 1
            else:
                ent_count[key] = 1
        logger.info(f'实体标注情况：{ent_count}')
        self.msg_lbl.config(text='导出成功')

#--------格式化按钮执行的内容--------
    def format(self):
        """格式化文本，去除多余的换行符"""
        content = self.get_text() #获取文本
        text = '\n'.join([i for i in content.split('\n') if i])
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, text)
        self.render_color()

#--------弹出照片--------
    def tanchu(self):
        p = self.p
        image = Image.open(p)
        image.show()
        # image.close()


#----------------渲染1---------------- 
    def render_color(self, all_tagged_strings=None):
        
        """渲染标注过的文本的颜色"""
        if all_tagged_strings is None:
            all_tagged_strings = {}
        for idx in all_tagged_strings:
            s, e = idx.split('-')
            key = all_tagged_strings[idx]
            self.text.tag_add(f'ent-{key}', s, e)

#----------------渲染2---------------- 
    def render_text(self, content, cr_psn=None, all_tagged_strings=None):
        # self.i = 1
        """渲染Text控件，包括文本的重新加载和颜色的渲染"""
        if all_tagged_strings is None:
            all_tagged_strings = {}
        logger.info('重新加载文本')
        self.text.delete("1.0", tk.END)
        self.text.insert("end-1c", content)
        # self.text.index(tk.INSERT)
        self.text.see(self.last_cr_psn)
        # self.text.see(self.text.index(tk.INSERT))
        ''''
        获取鼠标开始的位置
        '''
        # self.text.see(self.last_cr_psn[-1]) #在这里写入上一次光标的位置，获取每次光标的信息，存储在字典中，然后获取最后一个元素，或者通过不断赋值
        
        if cr_psn:
            self.text.mark_set(tk.INSERT, cr_psn)
            self.text.see(cr_psn)
            self.update_cr_psn(cr_psn)
        
        # if cr_psn:
        #     self.text.mark_set(tk.INSERT, "33.2")
        #     self.text.see(cr_psn)
        #     self.update_cr_psn(cr_psn)
            
        logger.info('渲染颜色')
        self.render_color(all_tagged_strings)



# ---------------------------------------------下拉框找文件---------------------------------------------
# ---------------------------------------------下拉框找文件---------------------------------------------
# ---------------------------------------------下拉框找文件---------------------------------------------

#下拉框找实体文件
def get_cfg_files():
    """获取目标路径下所有的配置文件名"""
    file_names = os.listdir("./configs")
    return sorted([x for x in file_names if (not x.startswith('.')) and x.endswith('.config')])

# 下拉框找关系文件
def get_cfg_files1():
    """获取目标路径下所有的配置文件名"""
    file_names1 = os.listdir("./configs")
    return sorted([y for y in file_names1 if (not y.startswith('.')) and y.endswith('.config')])




#---------------------------------------------解码阶段———————————————————————————————————————————————
#---------------------------------------------解码阶段———————————————————————————————————————————————
#---------------------------------------------解码阶段———————————————————————————————————————————————
#打标住
# get_tagged_pairs(para, schema="BIES", rep=r'\[<.*?→.*?>\]◎')
# def get_tagged_pairs_1(para, schema="BIESO", rep=r'\[<.*?\⊙'):#核心看这里解码
#     pass

def get_tagged_pairs(para, schema="BIESO", rep=r'\[<.*?\⊙'):#核心看这里解码
    """对一个段落中的所有文本进行标注
    
    :param para: 段落文本
    :param schema: 标注方法
    :param rep: 匹配标注的文本的正则表达式
    :return:
    """
    para = para.strip('\n') #去除两端换行
    ent_list = re.findall(rep, para) #匹配查找，
    
    # print("ent_list",ent_list)
    # print("ok")
    
    para_len = len(para) #看整个句子的长度
    chunk_list = []  # 存储标注过的实体及相关信息
    end_pos = 0
    if not ent_list: #没有找到
        chunk_list.append([para, 0, para_len, False])
    else: #找到了
        for pattern in ent_list:
            start_pos = end_pos + para[end_pos:].find(pattern)
            # print(start_pos)
            end_pos = start_pos + len(pattern)
            chunk_list.append([pattern, start_pos, end_pos, True])

    full_list = []  # 将整个para存储进来，并添加标识（是否为标注的实体）
    for idx in range(len(chunk_list)):
        if idx == 0:  # 对于第一个实体，要处理实体之前的文本
            if chunk_list[idx][1] > 0:  # 说明实体不是从该para的第一个字符开始的,则将前面的无关紧要的加起来
                full_list.append([para[0:chunk_list[idx][1]], 0, chunk_list[idx][1], False])
                full_list.append(chunk_list[idx])
            else:
                full_list.append(chunk_list[idx])
        else:  # 对于后续的实体
            if chunk_list[idx][1] == chunk_list[idx - 1][2]:
                # 说明两个实体是相连的，直接将后一个实体添加进来
                full_list.append(chunk_list[idx])
            elif chunk_list[idx][1] < chunk_list[idx - 1][2]:
                # 不应该出现后面实体的开始位置比前面实体的结束位置还靠前的情况
                pass
            else:
                # 先将两个实体之间的文本添加进来
                full_list.append([para[chunk_list[idx - 1][2]:chunk_list[idx][1]],
                                  chunk_list[idx - 1][2], chunk_list[idx][1],
                                  False])
                # 再将下一个实体添加进来
                full_list.append(chunk_list[idx])

        if idx == len(chunk_list) - 1:  # 处理最后一个实体
            if chunk_list[idx][2] > para_len:
                # 最后一个实体的终止位置超过了段落长度，不应该出现这种情况
                pass
            elif chunk_list[idx][2] < para_len:
                # 将最后一个实体后面的文本添加进来
                full_list.append([para[chunk_list[idx][2]:para_len], chunk_list[idx][2], para_len, False])
            else:
                # 最后一个实体已经达到段落结尾，不作任何处理
                pass
    #print("full_list",full_list)
    return tag_para(full_list, schema)

#打标注
def tag_para(seg_list, schema="BIESO"):
    """将段落中所有的字进行标注。

    :param seg_list: 由标注的实体词元素列表组成的列表
    :param schema: 标注方法
    :return:
    """
    pair_list = []
    for sub_list in seg_list:
        if sub_list[3]:  # 是标注的实体
            ent_and_lab = sub_list[0].strip('[<$\⊙').split('→')
            ent, label = ent_and_lab
            label = label.replace(">]","")
            ent = list(ent) #将实体转换成字符串
            tagged_txt = tag_entity(ent, label, schema)
            for i in tagged_txt:
                pair_list.append(i)
        else:  # 不是实体
            txt = sub_list[0]
            txt = list(txt)
            for idx in range(len(txt)):
                word = txt[idx]
                if word == ' ': #空字符不标注
                    continue
                pair = word + ' ' + 'O\n'
                pair_list.append(pair)
    return pair_list

#打标签
def tag_entity(word_list, label: str, schema: str = "BIESO"):
    """将实体字列表（word_list）中的每个字按照给定的模式（schema）打上
    对应的标签（label）

    :param word_list: 将实体词拆成单字组成的列表
    :param label: 实体对应的标签
    :param schema: 标注方法
    :return:
    """
    assert schema in ['BIESO', 'BIO'], f"不支持的标注模式{schema}"
    output_list = []
    list_len = len(word_list)
    if list_len == 1: #单字符
        if schema == 'BIESO':
            return word_list[0] + ' ' + 'S-' + label + '\n'
        else:  #'BI'
            return word_list[0] + ' ' + 'B-' + label + '\n'
    else:
        if schema == 'BIESO':
            for idx in range(list_len):
                if idx == 0:
                    pair = word_list[idx] + ' ' + 'B-' + label + '\n'
                elif idx == list_len - 1:
                    pair = word_list[idx] + ' ' + 'E-' + label + '\n'
                else:
                    pair = word_list[idx] + ' ' + 'I-' + label + '\n'
                output_list.append(pair)

        else: #'BI'
            for idx in range(list_len):
                if idx == 0:
                    pair = word_list[idx] + ' ' + 'B-' + label + '\n'
                else:
                    pair = word_list[idx] + ' ' + 'I-' + label + '\n'
                output_list.append(pair)
        return output_list
    


# def get_tagged_pairs(para, schema="BIES", rep=r'\[<.*?→.*?>\]◎'):#核心看这里解码
#     """对一个段落中的所有文本进行标注
    
#     :param para: 段落文本
#     :param schema: 标注方法
#     :param rep: 匹配标注的文本的正则表达式
#     :return:
#     """
#     para = para.strip('\n')
#     ent_list = re.findall(rep, para)
#     para_len = len(para)
#     chunk_list = []  # 存储标注过的实体及相关信息
#     end_pos = 0
#     if not ent_list:
#         chunk_list.append([para, 0, para_len, False])
#     else:
#         for pattern in ent_list:
#             start_pos = end_pos + para[end_pos:].find(pattern)
#             end_pos = start_pos + len(pattern)
#             chunk_list.append([pattern, start_pos, end_pos, True])

#     full_list = []  # 将整个para存储进来，并添加标识（是否为标注的实体）
#     for idx in range(len(chunk_list)):
#         if idx == 0:  # 对于第一个实体，要处理实体之前的文本
#             if chunk_list[idx][1] > 0:  # 说明实体不是从该para的第一个字符开始的
#                 full_list.append([para[0:chunk_list[idx][1]], 0, chunk_list[idx][1], False])
#                 full_list.append(chunk_list[idx])
#             else:
#                 full_list.append(chunk_list[idx])
#         else:  # 对于后续的实体
#             if chunk_list[idx][1] == chunk_list[idx - 1][2]:
#                 # 说明两个实体是相连的，直接将后一个实体添加进来
#                 full_list.append(chunk_list[idx])
#             elif chunk_list[idx][1] < chunk_list[idx - 1][2]:
#                 # 不应该出现后面实体的开始位置比前面实体的结束位置还靠前的情况
#                 pass
#             else:
#                 # 先将两个实体之间的文本添加进来
#                 full_list.append([para[chunk_list[idx - 1][2]:chunk_list[idx][1]],
#                                   chunk_list[idx - 1][2], chunk_list[idx][1],
#                                   False])
#                 # 再将下一个实体添加进来
#                 full_list.append(chunk_list[idx])

#         if idx == len(chunk_list) - 1:  # 处理最后一个实体
#             if chunk_list[idx][2] > para_len:
#                 # 最后一个实体的终止位置超过了段落长度，不应该出现这种情况
#                 pass
#             elif chunk_list[idx][2] < para_len:
#                 # 将最后一个实体后面的文本添加进来
#                 full_list.append([para[chunk_list[idx][2]:para_len], chunk_list[idx][2], para_len, False])
#             else:
#                 # 最后一个实体已经达到段落结尾，不作任何处理
#                 pass
#     return tag_para(full_list, schema)

# #打标注
# def tag_para(seg_list, schema="BIES"):
#     """将段落中所有的字进行标注。

#     :param seg_list: 由标注的实体词元素列表组成的列表
#     :param schema: 标注方法
#     :return:
#     """
#     pair_list = []
#     for sub_list in seg_list:
#         if sub_list[3]:  # 是标注的实体
#             ent_and_lab = sub_list[0].strip('[<$>]◎').split('→')
#             ent, label = ent_and_lab
#             ent = list(ent)
#             tagged_txt = tag_entity(ent, label, schema)
#             for i in tagged_txt:
#                 pair_list.append(i)
#         else:  # 不是实体
#             txt = sub_list[0]
#             txt = list(txt)
#             for idx in range(len(txt)):
#                 word = txt[idx]
#                 if word == ' ':
#                     continue
#                 pair = word + ' ' + 'O\n'
#                 pair_list.append(pair)
#     return pair_list

# #打标签
# def tag_entity(word_list, label: str, schema: str = "BIES"):
#     """将实体字列表（word_list）中的每个字按照给定的模式（schema）打上
#     对应的标签（label）

#     :param word_list: 将实体词拆成单字组成的列表
#     :param label: 实体对应的标签
#     :param schema: 标注方法
#     :return:
#     """
#     assert schema in ['BIES', 'BI'], f"不支持的标注模式{schema}"
#     output_list = []
#     list_len = len(word_list)
#     if list_len == 1:
#         if schema == 'BIES':
#             return word_list[0] + ' ' + 'S-' + label + '\n'
#         else:
#             return word_list[0] + ' ' + 'B-' + label + '\n'
#     else:
#         if schema == 'BIES':
#             for idx in range(list_len):
#                 if idx == 0:
#                     pair = word_list[idx] + ' ' + 'B-' + label + '\n'
#                 elif idx == list_len - 1:
#                     pair = word_list[idx] + ' ' + 'E-' + label + '\n'
#                 else:
#                     pair = word_list[idx] + ' ' + 'I-' + label + '\n'
#                 output_list.append(pair)

#         else:
#             for idx in range(list_len):
#                 if idx == 0:
#                     pair = word_list[idx] + ' ' + 'B-' + label + '\n'
#                 else:
#                     pair = word_list[idx] + ' ' + 'I-' + label + '\n'
#                 output_list.append(pair)
#         return output_list

# 打开图片
def get_img(filename): #, width, height
    im = Image.open(filename)#.resize((width, height))
    im = ImageTk.PhotoImage(im)
    return im

# import tkinter
#---------------------------------------------主函数阶段———————————————————————————————————————————————
#系统提示
def main():
    logger.info(f'当前操作系统：{platform.system()}')
    root = tk.Tk()
    root.iconbitmap('./images/cy.ico')
##    root.resizable(False, False)
    root.geometry("1300x700+20+1")# 页面整体大小1300x700;页面向右移动20,向下移动1


    # root.attributes('-alpha',1)  #窗口背景透明化
    # canvas = tkinter.Canvas(root, width=1300, height=700, bg=None)
    # image_file = tkinter.PhotoImage(file=r"./images/jiaochen.png")
    # image = canvas.create_image(650, 0, anchor='n', image=image_file)
    # canvas.pack()
    # # canvas.pack_forget()

    
    _ = MyFrame(root)
    logger.info('标注软件已经启动')

    
    
    # 当点击右上角退出时，执行的程序
    def on_closing():
        if messagebox.askokcancel("注意提前导出文件", "确认退出吗?"):
            root.destroy()
            quit()
    root.protocol('WM_DELETE_WINDOW', on_closing)
    root.mainloop()
    logger.info('标注软件已经关闭')

#先不管
class InvalidShortcut(Exception):
    pass



#主函数
if __name__ == '__main__':
    main()

    

