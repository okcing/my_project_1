#coding=utf8
'''
将得到的召回结果，推荐给每个用户
'''
import cPickle as pickle
import numpy as np
from sklearn.preprocessing import normalize
import time
from collections import defaultdict
import redis
from redis_shard.shard import RedisShardAPI
import ujson
from multiprocessing import Process,Pool, cpu_count
import datetime


redis_info = {
        'host': 'mb.y.redis.sohucs.com',
        'port': '22812',
        'password': 'e0857d376c81b53b3e7007465144b1da',
        'db': '0'
    }
redis_info_2 = {
    'host': 'mb.y.redis.sohucs.com',
    'port': '22829',
    'password': 'a4785f18b764896edcfe630326f3bbbd',
    'db': '0'
}
servers = [
    {'name': 'server1', 'host': 'mb.y.redis.sohucs.com', 'port': 22812, 'db': 0,
     'password': 'e0857d376c81b53b3e7007465144b1da'},
    {'name': 'server2', 'host': 'mb.y.redis.sohucs.com', 'port': 22829, 'db': 0,
     'password': 'a4785f18b764896edcfe630326f3bbbd'}
    ]
client = RedisShardAPI(servers, hash_method='md5')

def connect_db(host, port, password, db):
    pool = redis.ConnectionPool(host=host, port=port, password=password, decode_responses=True, db=db)
    r = redis.StrictRedis(connection_pool=pool)
    return r


def recommend(clk_cid):
    # 得到点击历史
    clk_his = user_clk_his[clk_cid]
    # 建立召回列表
    recall_list = []
    # 召回集合去重
    recall_set = set()

    # 遍历点击历史
    for index, item_nid in enumerate(clk_his):
        # 获取相似文章
        # 最近一次，获取5个
        if index == 0:
            for index_count, sim_temp in enumerate(sim_item_ge[item_nid]):
                if sim_temp in recall_set:
                    continue
                recall_list.append(sim_temp)
                recall_set.add(sim_temp)
                if index_count == 6:
                    break
        elif index == 1:
            for index_count, sim_temp in enumerate(sim_item_ge[item_nid]):
                if sim_temp in recall_set:
                    continue
                recall_list.append(sim_temp)
                recall_set.add(sim_temp)
                if index_count == 6:
                    break
        elif index == 2:
            for index_count, sim_temp in enumerate(sim_item_ge[item_nid]):
                if sim_temp in recall_set:
                    continue
                recall_list.append(sim_temp)
                recall_set.add(sim_temp)
                if index_count == 5:
                    break
        elif index == 3:
            for index_count, sim_temp in enumerate(sim_item_ge[item_nid]):
                if sim_temp in recall_set:
                    continue
                recall_list.append(sim_temp)
                recall_set.add(sim_temp)
                if index_count == 5:
                    break

        elif index > 3:
            for index_count, sim_temp in enumerate(sim_item_ge[item_nid]):
                if sim_temp in recall_set:
                    continue
                recall_list.append(sim_temp)
                recall_set.add(sim_temp)
                if index_count == 4:
                    break
            if index > 15:
                break

    # 查看召回列表长度
    # break
    temp_dict = {}
    temp = []
    temp_dict["art_lst"] = temp
    temp_dict["uid"] = clk_cid

    for recall_index, recall_item in enumerate(recall_list):
        data = [recall_item, 100 - recall_index]
        temp.append(data)
    temp_json = ujson.dumps(temp_dict)
    # break
    client.hset('GraphEm_{0}'.format(clk_cid), 'ge_main_cold', temp_json)
    client.expire('GraphEm_{0}'.format(clk_cid), 3600 * 48)

if __name__ == '__main__':
    #加载用户点击历史字典
    load_start = time.time()
    with open('../data/get_user_click_history/click_his/click_his.json', 'r') as f:
        user_clk_his = ujson.load(f)
    print '加载点击历史字典', time.time()-load_start

    #加载相似item字典
    load_start = time.time()
    with open('../data/get_similar_item/cold_sim/cold_sim_nid', 'r') as f:
        sim_item_ge = ujson.load(f)
    print '加载相似用户字典', time.time()-load_start

    print '所有用户个数', len(user_clk_his)

    t2 = time.time()
    pool = Pool(30)

    #遍历所有用户
    for cid_index, clk_cid in enumerate(user_clk_his):

        pool.apply_async(recommend, (clk_cid,))
    pool.close()
    pool.join()
    print('多个进程执行完毕')
    print datetime.datetime.now()
    print time.time() - t2
    print '========================================================================='

        #这里插入到redis中