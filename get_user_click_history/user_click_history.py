#coding=utf8
import ujson as json
import os
from collections import defaultdict
import time
import datetime
import logging

PATH = '/data/wangqianfa_offline/my_project_1'


if __name__ == '__main__':
    start = time.time()

    clkic_file_path = '/data/wangqianfa/Get_Clk_data_newsfrom6/'

    all_file = os.listdir(clkic_file_path)

    #get clk dir name
    dir_file = []
    for i in all_file:
        if os.path.isdir(clkic_file_path + i):
            dir_file.append(clkic_file_path + i)

    #sort by date
    dir_file.sort()

    #user click his
    user_click_his = defaultdict(list)

    #file path
    path1 = dir_file[-1]
    path2 = dir_file[-2]

    all_file_1 = os.listdir(path1)
    # logging.INFO('all_file_1: %s', 'hhhh')

    all_file_1.sort(reverse=True)
    # logger.INFO('after sorted, all_file_1: %s', all_file_1)

    for f in all_file_1:
        # logger.INFO('path+filename', path1 + '/' + f)
        data_path = path1 + '/' + f
        clk_data = open(data_path, 'r').readlines()

        #new click
        clk_data = reversed(clk_data)
        for data in clk_data:
            try:
                info = data.strip().split('\1')
                # click_time = datetime.datetime.strptime(info[1], '%Y-%m-%d %H:%M:%S')
                # timedelta = ((time_now - click_time).seconds) / 3600
                # if timedelta > 10:
                #     print data, '大于10'
                #     break
                if len(user_click_his[info[2]])<10:
                    # user_click_his[info[2]].append([info[0], info[1]])
                    user_click_his[info[2]].append(info[0])
            except Exception as e:
                pass
                # logging.warn('Exception %s', e)

    all_file_2 = os.listdir(path2)

    all_file_2.sort(reverse=True)

    for f in all_file_2:
        # logger.INFO('path+filename', path1 + '/' + f)
        data_path = path2 + '/' + f
        clk_data = open(data_path, 'r').readlines()

        # new click
        clk_data = reversed(clk_data)
        for data in clk_data:
            try:
                info = data.strip().split('\1')
                # click_time = datetime.datetime.strptime(info[1], '%Y-%m-%d %H:%M:%S')
                # timedelta = ((time_now - click_time).seconds) / 3600
                # if timedelta > 10:
                #     print data, '大于10'
                #     break
                if len(user_click_his[info[2]])<10:
                    # user_click_his[info[2]].append([info[0], info[1]])
                    user_click_his[info[2]].append(info[0])
            except Exception as e:
                pass

    print time.time() - start
    start = time.time()
    with open('{0}/data/get_user_click_history/click_his.json', 'w') as json_file:
        json.dump(user_click_his, json_file)
    print time.time() - start



