
# import sys  
import tkinter
import os
from tkinter.messagebox import *
from datetime import datetime, date, timedelta
import json
import webbrowser

# import YEDDA-py3

time = ["1","2","3","4","5","6","7","8","9","0","-","+"]
idex = ["P","G","S","K","E","L","F","X","Q","M","C","Y"] 
# dict_mima = dict(zip(time,idex))
dict_jima = dict(zip(idex,time))

index = tkinter.Tk()  #创建主窗口
index.iconbitmap('./images/cy.ico')
index.attributes('-alpha',1)  #窗口背景透明化
index.title('“火星”实体关系文本标注软件V1.0-登录页面') #设置主窗口标题
index.geometry('400x650+500+10') #设置主窗口大小

#下面两行代码的作用是固定窗口大小，不可拉动调节
index.maxsize(400,650)
index.minsize(400,650)

#**************************************************
#                 添加组件

# 加载图片
canvas = tkinter.Canvas(index, width=400, height=650, bg=None)
image_file = tkinter.PhotoImage(file=r"./images/cybiaozhu.png")
image = canvas.create_image(200, 0, anchor='n', image=image_file)
canvas.pack()

#账号与密码文字标签
account_lable = tkinter.Label(index, text = '账号', bg='lightskyblue', fg='white', font=('Arial', 12), width=5, height=1)
account_lable.place(relx=0.23,rely=0.36)
pasw_lable = tkinter.Label(index, text = '密码', bg='lightskyblue', fg='white', font=('Arial', 12), width=5, height=1)
pasw_lable.place(relx=0.23,rely=0.46)

#账号与密码输入框
account = tkinter.Entry(index,width=24, highlightthickness = 1,highlightcolor = 'lightskyblue',relief='groove')  #账号输入框
account.place(relx=0.34,rely=0.36 )  #添加进主页面,relx和rely意思是与父元件的相对位置
password = tkinter.Entry(index,width=24, show='*',highlightthickness = 1,highlightcolor = 'lightskyblue',relief='groove')  #密码输入框
password.place(relx=0.34,rely=0.46) #添加进主页面

user = dict() #{"Chen":"123456"}  #定义一个字典来存储用户的信息(key :账号 , value：密码)

def readusers():
    try:
        with open("./utils/users.config", 'r') as fp:
            press_cmd = {k : v for k, v in json.load(fp).items()} #字典
            return press_cmd
    except:
        showinfo("配置信息","错误,请联系管理员")
        return {"roots":"123456"}
#登录按钮处理函数
def login():
    ac = account.get()
    ps = password.get()
    #账号密码信息读出json文件
    user = readusers()
    if (ac == "" or ps == ""):
        showinfo("用户登录", "请完整填写信息")  # messagebox的方法
    elif user.get(ac) != ps:
        account.delete(0,'end')  #清空文本框的内容
        password.delete(0,'end')  #清空文本框的内容
        showinfo("用户登录", "账号或者密码有误")   #messagebox的方法
    else:
        account.delete(0, 'end')  # 清空文本框的内容
        password.delete(0, 'end')  # 清空文本框的内容
        showinfo("用户登录", "登录成功,请确认")  # messagebox的方法
        
        os.system('biaozhu.py %s %s"' %(ac, ps))
        # os.close()

def jiema(strinput,dict_jima):
    strinput1 = strinput[:10]
    list_jiema = list(strinput1)
    list_jima = [dict_jima[i] for i in list_jiema]
    # list_jima2 = [dict_jima[i] for i in list_jiema]
    key = ''
    for i in list_jima:
        key += i
    # print(key)
    # key = '2022-04-15'
    oldtime = date(*map(int, key.split('-'))) 
    old_time = oldtime + timedelta(days=1) #凌晨之前
    # print('lodtime',oldtime)
    # print('lodtime',old_time)
    now_time = datetime.now()
    now_time_str = now_time.strftime('%Y-%m-%d')
    now_time = date(*map(int, now_time_str.split('-')))
    # print(now_time)
    # print(nwetime - oldtime)
    if  (now_time <=  old_time) and (now_time >=  oldtime) :
        return True
        # 存储字典到系统，并访问网站
    else:
        return False
        # print("请重新获取序列号")
        #错误，请重新设置账号密码
        #超时，请重新联系管理员
    # print(futuer_time_str )
    # return 

def writeusers(username, usermima):
    try:
        with open("./utils/users.config", 'r') as fp:
            press_cmd1 = {k :v for k, v in json.load(fp).items()} #字典
            press_cmd1[username] = usermima
        with open("./utils/users.config", 'w') as fp:    
            json.dump(press_cmd1,fp)
            showinfo("配置信息","成功写入")
    except:
        showinfo("配置信息","错误,请联系管理员")
        # return {"root":"123456"}
         
        
def reguesta():
    ac = account.get()
    ps = password.get()
    
    if (ac == "" or ps == ""):
        showinfo("用户注册", "请完整填写信息！")  # messagebox的方法
    elif len(ac) == 0:
        showinfo("用户注册","请输入密码")   #messagebox的方法
    elif len(ps) == 0:
        showinfo("用户注册","请输入账号")   #messagebox的方法
    else:
        if (len(ac) > 12) and (len(ps) > 12):
            strinput3 = ac[10:12]
            strinput2 = ac[12:]
            strinput31 = ps[10:12]
            strinput21 = ps[12:]
        else:
            showinfo("注册","无效信息")
            return False
        try :
            if (jiema(ac,dict_jima)==True) and (jiema(ps,dict_jima)==True) and (strinput3 == "Y#") and (strinput31 == "Y#") :
                username = strinput2
                usermima = strinput21
                # user[username] = usermima
                showinfo("注册信息","成功,跳转到标注界面?")  # messagebox的方法
                #账号密码信息存入json文件
                writeusers(username, usermima)
                os.system('biaozhu.py %s %s"' %(username, usermima))
            else:
                showinfo("注册","注册未通过")
        except:
            showinfo("注册","注册失败")
            
       
        
        
        # user[ac] = ps
        # account.delete(0, 'end')  # 清空文本框的内容
        # password.delete(0, 'end')  # 清空文本框的内容
        # showinfo("用户注册", "注册成功！")  # messagebox的方法
 
def openhtml():
    
    file = r'.\utils\火星实体关系文本标注软件教程.html'
    webbrowser.open(file, new=2)  


#登录与注册按钮
loginBtn = tkinter.Button(index,text='注册',font = ('楷体',12),width=6,height=1,bd=0.5,command=reguesta,relief='solid',bg='lightcyan')
loginBtn.place(relx=0.57,rely=0.57)
loginBtn = tkinter.Button(index,text='登录',font = ('楷体',12),width=6,height=1,command=login,relief='solid',bd = 0.5,bg='lightcyan')
loginBtn.place(relx=0.3,rely=0.57)

loginBtn = tkinter.Button(index,text='服务',font = ('宋体',12),width=6,height=1,command=openhtml,relief='solid',bd = 0.5,bg='blue')
loginBtn.place(relx=0.83,rely=0.94)



#**************************************************
index.mainloop() #使窗口不断刷新，应该放在代码最后一句



    # pramter = 'GMGGCMKCPKY#'
    # jiema(pramter,dict_jima)
    
