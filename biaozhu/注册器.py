from datetime import datetime
# 19 
def mima(dict_mima):
    now_time = datetime.now()
    now_time_str = now_time.strftime('%Y-%m-%d')
    # print(now_time_str )
    list_mima = list(now_time_str)
    show = [dict_mima[i] for i in list_mima]
    key = ''
    for i in show:
        key += i
    key += "Y#"
    return key


if __name__ == '__main__':
     time = ["1","2","3","4","5","6","7","8","9","0","-","+"]
     idex = ["P","G","S","K","E","L","F","X","Q","M","C","Y"]
     #
     # 2022-04-15
     dict_mima = dict(zip(time,idex)) #dict_jima = dict(zip(time,idex))
    
     # print(len(mima(dict_mima)))
     keya = mima(dict_mima) #有效期到下个凌晨,
     print("动态序列号为  "+keya+ "\n\n你需要在登录界面中输入序列号和账户信息\n例如你注册的账号为 chen 密码为 123456 "+"\n\n账号框  "+\
         keya+"Chen"+"\n密码框  "+keya+"123456" + "\n\n你可以在下个凌晨前用本序列号多次注册\n注册成功后，下一次只需要账号信息即可登录")
