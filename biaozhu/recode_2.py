# -*- coding: utf-8 -*-
"""
2022/9/1 更新
CHEN | YNU
"""

#-----只需在这里修改文件地址即可↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

filea = r'C:\Users\DELL\Desktop\标注数据\删除了很多o的分段数据\zhuquanqing.txt'

#-----只需在这里修改文件地址即可↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑



import re
from datetime import datetime



def sanyuanzu1(entuty_list): #5元素元组
    entity_dict = {}
    entity_lists = []
    i = 0
    for entii in entuty_list:
        if ("O" not in entii) and (len(entii) > 2): #带有关系的实体行
            
            i += 1
            if len(entii) > 4: #多个关系
                entii.insert(0, i)
                j = -1
                # print(2)
                while True:
                    # print(1)
                    try:
                        j += 2
                        lin = entii[:3]
                        m = 2+j
                        mm = 4+j
                        entii[m]
                        lin.extend(entii[m: mm])
                        entity_lists.append(lin)
                    except:
                        break
            elif len(entii) == 4: #一个关系
                entii.insert(0, i)
                entity_lists.append(entii)   
            else:
                # print(entii)
                pass
    # for i in entity_lists:
    #     print(i) 
    return  wordtoch(sanyuanzu2(entity_lists))


def sanyuanzu2(entity_lists):
    entitysan_list = []
    for index, relation in  enumerate(entity_lists):
        for relation2 in entity_lists[index+1:]:
            # print(index, relation2)
            if relation[3] == relation2[3]:
                # print(relation[3])
                # pass
                if "1" in relation[-1]:
                    entitysan_list.append([relation[1],relation[2],relation[-1],relation2[2],relation2[1]])
                else:
                    entitysan_list.append([relation2[1],relation2[2],relation2[-1],relation[2],relation[1]])
                break #break 帮助在打标签时，能够断断续续多次标注。|匹配到最近的一对实体后，不再继续寻找。
    return entitysan_list


def wordtoch(words):
    zh = ['病名','病症','其它','药名','诊断方案','治疗方案', "取消标注",'包含','治疗','危险因素','辅助诊断','特征','并发','别名','作用','条件','诊断']
    en = ['dis','hyp','oth','med','dia','cur',"none", 'Incl','Trea','Risk','Auxi','Char','Conc','Alia','Acti','Cond','Diag']
    ti = ["A","B","C","D","E","F","Q","I","T","K","U","M","N","L","J","Y","G"]
    dic1 = dict(zip(ti, zh)) 
    # dic2 = dict(zip(en,ti ))
    dic3 = dict(zip(ti,en))
    # print(len(zh))
    # print(len(en))
    # print(len(ti))
    
    for word in words:
        try:
            word[1] = dic1[word[1]]
            word[2] = dic1[word[2][0]]
            word[3] = dic1[word[3]]
        except:
            continue

    now_time = datetime.now().strftime('%m-%d-%H-%M-%S')
    new_filename = file_name[:-5] + '_五元组_' +now_time +'.csv'
    filew = f = open(new_filename, 'w', encoding="utf-8")
    for word in words:
        filew.write(str(word).strip('[').strip(']') +'\n')
    filew.close()
    print('文件导出！')
    return words




def readfile(file):
    f = open(file, "r", encoding='utf-8').readlines()
    entuty_list = []
    for i in f:
        # print(i.strip('\n'))
        j = i.strip('\n')
        # print(j)
        j = re.split(" |@|_", j)
        # print(j)
        entuty_list.append(j)
    return entuty_list




#打标签
def tag_entity(word_list, label, schema='BIEO' ):
    """将实体字列表（word_list）中的每个字按照给定的模式（schema）打上
    对应的标签（label）

    :param word_list: 将实体词拆成单字组成的列表
    :param label: 实体对应的标签
    :param schema: 标注方法
    :return:
    """
    output_list = []
    list_len = len(word_list)
    if list_len == 1: #单字符
        if schema == 'BIEO':
            return word_list[0] + ' ' + 'B-' + label + '\n'
        else:  #'BI' 
            return word_list[0] + ' ' + 'B-' + label + '\n'
    else:
        if schema == 'BIEO':
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

def biaoqian(file_list):
    zh = ['病名','病症','其它','药名','诊断方案','治疗方案', "取消标注",'包含','治疗','危险因素','辅助诊断','特征','并发','别名','作用','条件','诊断']
    en = ['dis','hyp','oth','med','dia','cur',"none", 'Incl','Trea','Risk','Auxi','Char','Conc','Alia','Acti','Cond','Diag']
    ti = ["A","B","C","D","E","F","Q","I","T","K","U","M","N","L","J","Y","G"]
    dic1 = dict(zip(ti, zh)) 
    # dic2 = dict(zip(en,ti ))
    dic3 = dict(zip(ti,en))

    for entii in file_list:
        if ("O" in entii) or (("O" not in entii) and (len(entii) == 2)) :
            klist = [k+' '+'O\n' for k in entii[0]]
            ms_list.append(klist) #存储字符和标签
        elif ("O" not in entii) and (len(entii) > 2):
            if len(entii) == 4:
                word_list = list(entii[0])
                label = dic3[entii[-1][0]] + '-' + entii[-1][-1]
                ms_list.append(tag_entity(word_list, label))
            elif len(entii) > 4:
                word_list = list(entii[0])
                label = "main-1"
                ms_list.append(tag_entity(word_list, label))
            else:
                pass
        else:
            pass
    

def writefile(ms_list):
    now_time = datetime.now().strftime('%m-%d-%H-%M-%S')
    new_filename = file_name[:-5] + '_分段_' +now_time +'.anns'
    f = open(new_filename, 'w', encoding='utf-8')
    for i in ms_list:
        for j in i:
            if '。' in j:
                f.write(j+'\n')
            else:
                f.write(j)
    f.close()
    print("输出！")
    
    

if __name__ == "__main__":
    '''
    file_list = readfile(file_name)

    sanyuanzu1(file_list) #输出三元组-五元组文件
    '''
    schema="BIEO" 
    rep=r'\[<.*?\⊙'
    file_name = filea

    ms_list = []
    file_list = readfile(file_name)
    file_wlist = readfile(file_name)
    # print(file_list)
    

    #----------------------------------------------------------------
    # sanyuanzu1(file_list) #输出三元组-五元组文件

    #----------------上下代码，可以执行二选一！----------------------------

    biaoqian(file_wlist) # 付式 输出标签文件
    writefile(ms_list)
    #----------------------------------------------------------------

