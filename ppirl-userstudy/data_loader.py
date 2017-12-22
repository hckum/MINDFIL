#! /usr/bin/python
# encoding=utf-8

import json


def load_data_from_csv(filename):
    data = list()
    filein = open(filename, 'r')
    for line in filein:
        record = line.split(',')
        data.append(record)
    return data


def save_data_to_json(filename, data):
    fileout = open(filename, 'w+')
    fileout.write(json.dumps(data, ensure_ascii=False))
    fileout.close()


def get_data_filename_by_url(url):
    if 'base_mode' in url:
        return 'practice_base_mode.csv'
    elif 'full_mode' in url:
        return 'practice_full_mode.csv'
    elif 'masked_mode' in url:
        return 'practice_masked_mode.csv'
    elif 'minimum_mode' in url:
        return 'practice_minimum_mode.csv'
    elif 'moderate_mode' in url:
        return 'practice_moderate_mode.csv'
