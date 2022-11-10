# -*- coding: utf-8 -*-
"""
2022/8/31 更新
CHEN | YNU
"""

#-----只需在这里修改文件地址即可↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

file_name = r'C:\Users\DELL\Desktop\biaozhu - 副本\zhuquanqin\6.anns'

#-----只需在这里修改文件地址即可↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑




import re
from datetime import datetime

def get_tagged_pairs(para, schema="BIEO", rep=r'\[<.*?\⊙'):#核心看这里解码
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
def tag_para(seg_list, schema="BIEO"):
    """将段落中所有的字进行标注。

    :param seg_list: 由标注的实体词元素列表组成的列表
    :param schema: 标注方法
    :return:
    """
    pair_list = []
    for sub_list in seg_list:
        # print(sub_list)
        if sub_list[3]:  # 是标注的实体
            ent_and_lab = sub_list[0].strip('[<$\⊙').split('→')
            ent, label = ent_and_lab[:2]
            

            label = label.replace(">]","")
            # print(ent, label) 
            #--------------------------------------实体与标签
            i = ent + ' ' + label
            pair_list.append(i)
            pair_list_entity.append(i)
            #--------------------------------------实体与标签


            # ent = list(ent) #将实体转换成字符串
            # tagged_txt = tag_entity(ent, label, schema)
            # # print(tagged_txt)
            # for i in tagged_txt:
            #     pair_list.append(i)


        else:  # 不是实体


            # txt = sub_list[0]
            # txt = list(txt)
            # for idx in range(len(txt)):
            #     word = txt[idx]
            #     if word == ' ': #空字符不标注
            #         continue
            #     pair = word + ' ' + 'O\n'
            #     pair_list.append(pair)

            #-----------------------------------插入---------
            txt = sub_list[0]
            i = txt + ' ' + "O"
            pair_list.append(i)
            #-----------------------------------插入---------


    return pair_list

#打标签
def tag_entity(word_list, label: str, schema: str = "BIEO"):
    """将实体字列表（word_list）中的每个字按照给定的模式（schema）打上
    对应的标签（label）

    :param word_list: 将实体词拆成单字组成的列表
    :param label: 实体对应的标签
    :param schema: 标注方法
    :return:
    """
    assert schema in ['BIEO', 'BIO'], f"不支持的标注模式{schema}"
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

def export(file):
    # 按照换行符进行分割，此时仍有空白行，再按段落遍历时去除，此处需要改进，插入特殊符号，以特殊符号切割
    
    text_paras = open(file,"r",encoding='utf-8').readlines()
    # print(text_paras)
        
    now_time = datetime.now().strftime('%m-%d-%H-%M-%S')
    new_filename = file[:-5] + '_分段_' +now_time +'.anns'

    f = open(new_filename, 'w', encoding="utf-8")
    for i in range(len(text_paras)):
        p = text_paras[i]
        # print(p)
        p = p.strip()
        if not p:
            continue
        else:
            schema = "BIEO"
            entity_re = r'\[<.*?\⊙'
            tagged_words = get_tagged_pairs(p, schema, entity_re)
            for w in tagged_words:
                f.write(w+'\n')
            if i != len(text_paras) - 1:
                f.write('\n')
    f.close()

    print('导出成功')


if __name__ == "__main__":
    pair_list_entity = []
    file = file_name #读取标注软件导出的文件
    export(file)
    
    # print(pair_list_entity)
