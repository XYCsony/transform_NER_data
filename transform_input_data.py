# -*- coding: utf-8 -*-
# @Time    : 2020/9/23 10:39
# @Author  : ycxu
# @Email  : 773188396@qq.com

'''
实体标注文件格式转换
'''
import codecs
import os
import re

class TransformInputData:
    def __init__(self):
        pass

    def ann_2_bio(self, txt_data, ann_data):
        '''brat格式转bio'''
        txt = list(txt_data)
        label = ['O' for item in range(len(txt_data))]
        ann_labels = []
        for item in ann_data:
            t = re.split('[\t ]',item)
            ann_labels.append((eval(t[2]), eval(t[3]), t[1]))
        for (start, end, tag) in ann_labels:
            try:
                new_bio = ['I-'+tag for i in range(start, end)]
                new_bio[0] = 'B-'+tag
                label[start:end] = new_bio
            except:
                print('这条数据标注有问题:\n txt_data:{}\n ann_data:{}'.format(txt_data,ann_data))
                continue
        return txt, label

    def bio_2_bioes(self, txt_data, label_data):
        '''bio格式转bioes'''
        seq_len = len(label_data)

        for index, label in enumerate(label_data[:]):
            # 有两种情况抛异常（个人喜欢用 try 代替 if）
            #   1: O无法split
            #   2: 最后一位越界【即使越界了，结合下面第二个try的里面的if，我们把它设为O，个人思想。也可用其他办法】
            try:
                next_tag = label_data[index + 1].split('-')[0]
            except:
                next_tag = 'O'

            try:
                current_tag, = label.split('-')[0]
                if index < seq_len:
                    if (current_tag == 'B' and next_tag != 'I'):  # B之后无I, 改成S
                        label_data[index] = 'S' + '-' + label.split('-')[-1]
                    elif (current_tag == 'I' and next_tag != 'I'):  # I之后无I, I改成E
                        label_data[index] = 'E' + '-' + label.split('-')[-1]
            except:
                pass

        return txt_data, label_data
    def dict_2_bio(self,dict_data):
        '''dict格式转bio'''
        txt = list(dict_data['text'])
        label = ['O' for item in range(len(txt))]
        ann_labels = dict_data['labels']
        for (start, end, tag) in ann_labels:
            try:
                new_bio = ['I-' + tag for i in range(start, end)]
                new_bio[0] = 'B-' + tag
                label[start:end] = new_bio
            except:
                print('这条数据标注有问题:\n txt_data:{}\n ann_data:{}'.format(txt_data, ann_data))
                continue
        return txt, label

if __name__ == '__main__':
    dict_data = {"id": 2708,
                 "text": " 补气养血、调经止带，用于月经不调、经期腹痛  ",
                 "labels": [[1, 5, "DRUG_EFFICACY"], [6, 7, "SYMPTOM"], [18, 22, "SYMPTOM"]]}
    txt_data = ' 补气养血、调经止带，用于月经不调、经期腹痛  '
    ann_data = ['T1	DRUG_EFFICACY 1 5	补气养血', 'T2	SYMPTOM 18 22	经期腹痛', 'T3	SYMPTOM 6 7	调']
    T = TransformInputData()
    bio_data,bio_label = T.ann_2_bio(txt_data=txt_data, ann_data=ann_data)
    print(bio_data)
    print(bio_label)
    print('*'*200)
    bioes_data, bioes_label = T.bio_2_bioes(txt_data=bio_data,label_data=bio_label)
    print(bioes_data)
    print(bioes_label)
    print('*' * 200)
    bio_data,bio_label  = T.dict_2_bio(dict_data=dict_data)
    print(bio_data)
    print(bio_label)
    print('*' * 200)


