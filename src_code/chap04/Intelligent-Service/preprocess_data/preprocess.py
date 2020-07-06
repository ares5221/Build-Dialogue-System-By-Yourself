#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import csv


def read_data():
    '''
    读取保险数据源文件数据，将其作为数组返回
    :return:
    '''
    # 源数据文件地址
    csv_dir = './baoxianzhidao_filter.csv'
    # 存储读取到的保险问题描述
    insurance_ques = []
    # 存储读取到的保险问题对应答案
    insurance_ans = []
    # 读取源数据
    with open(csv_dir, 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            # 选取源数据中答案为最优答案的问答数据
            if len(row) == 4 and row[3] == '1':
                #  若question字段非空，则将问题title字段与question字段拼接为问题描述
                #  若question字段为空，则将问题title字段作为问题描述
                if row[1]:
                    insurance_ques.append(row[0] + row[1])
                else:
                    insurance_ques.append(row[0])
                # 选取replay字段作为答案描述
                insurance_ans.append(row[2])
    return insurance_ques, insurance_ans


def save_data(insurance_ques, insurance_ans):
    '''
    存储保险问答数据
    :param insurance_ques:
    :param insurance_ans:
    :return:
    '''
    # 遍历存储问答数据为csv格式
    for idx in range(len(insurance_ans)):
        with open('insurance_data.csv', 'a', newline='', encoding='utf-8') as csvfile:
            spamwriter = csv.writer(csvfile)
            spamwriter.writerow([insurance_ques[idx], insurance_ans[idx]])


if __name__ == '__main__':
    insurance_ques, insurance_ans = read_data()
    save_data(insurance_ques, insurance_ans)
