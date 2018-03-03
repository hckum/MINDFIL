 #! /usr/bin/python
# encoding=utf-8

import logging
import copy
import data_model as dm


def parse_user_data(user_data):
    if not user_data:
        return []
    user_data_list = user_data.split(';')
    ret = list()
    for i in range(len(user_data_list)):
        data = user_data_list[i].strip().rstrip('\n').rstrip(';')
        if data:
            data_dict = dict()
            kv_pairs = data.split(',')
            for kv in kv_pairs:
                if len(kv.split(':')) == 2:
                    k = kv.split(':')[0].strip()
                    v = kv.split(':')[1].strip()
                    data_dict[k] = v
            if len(data_dict) > 0:
                ret.append(data_dict)
    return ret


def grade_final_answer(data, data_pair_list):
    size = data_pair_list.size()
    correct = 0
    for d in data:
        if 'type' not in d or d['type'] != 'final_answer':
            continue
        if 'url' not in d or d['url'] not in ['/record_linkage', '/section2']:
            continue

        answer_id = d['id']
        answer_id = answer_id.lstrip('p')
        pair_num = int(answer_id.split('a')[0])
        answer = int(answer_id.split('a')[1])

        dp = data_pair_list.get_data_pair(pair_num)
        if dp != None and dp.grade(answer):
            correct += 1

    return [correct, size]