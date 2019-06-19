#coding=utf8
'''
首先得到当前正排中的所有文章（优质文章筛选？？？），回溯点击历史，得到"文章-用户"文件
'''
import sys
sys.path.append('/data/wangqianfa_online/my_project_1')
from utils.keynews_pool import KeynewsPool
import ujson
from collections import defaultdict
import os
import cPickle as pickle
from operator import itemgetter
import json
import faiss
import numpy as np
from sklearn.preprocessing import normalize
import time
import ujson
import sys
sys.path.append('/data/wangqianfa_online/my_project_1')


def load_item_embedding(embedding_file):
    index_dict = {}
    item_embeddings = []
    with open(embedding_file, 'r') as f:
        for index, line in enumerate(f):
            #the first line is the infomatation of the item embedding
            if index == 0:
                continue
            info = line.strip().split()
            embedding = np.array([float(i) for i in info[1:]]).astype('float32')
            item_embeddings.append(embedding)
            index_dict[index-1] = info[0]
    item_embeddings = np.array(item_embeddings).astype('float32')
    return item_embeddings, index_dict

def train_faiss(item_feature, D):
    '''
    use IndexFlatIP to get similar item
    '''
    #construct the index
    index = faiss.IndexFlatIP(D)
    index.add(item_feature)
    print index.ntotal
    D, I = index.search(item_feature, 200)
    return I

def get_nid_age(embedding_file):
    '''
    get item age from news redis and filter nid to ensure the nid in keynews redis
    :param embedding_file: filename
    :return: nid_age_dict
    '''

    #connect keynews redis
    keynewspool = KeynewsPool('sf.y.redis.sohucs.com', 25008, 'b83e99ea9a96b8377282ee0ec2d60311', 0)
    r = keynewspool.connect_db()

    all_nids = set()
    for key in r.scan_iter():
        # delete the key
        all_nids.add(key)

    keynewspool_all = KeynewsPool('s.t.d.redis.sohucs.com', 25060, 'b9583db58a5da3e871a006ef54d2d059', 0)
    r_all = keynewspool_all.connect_db()

    embedding_nids = set()
    with open(embedding_file, 'r') as f:
        for index, line in enumerate(f):
            if index == 0:
                continue
            nid = line.strip().split()[0]
            embedding_nids.add(nid)

    #filter
    filter_nids = set()
    for item in all_nids:
        ctime = r_all.hget(item, 'ctime')
        if ctime is not None:
            ctime = float(ctime) / 1000
        else:
            ctime = float(0)
        # item_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ctime))
        # print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        timedelta = time.time() - ctime
        # print sim_title
        if timedelta < 3600*8 and item in all_nids:
            # print timedelta
            filter_nids.add(item)
    return filter_nids

if __name__ == '__main__':

    s = time.time()
    filter_nids = get_nid_age('../model/deep_walk_item_10h_filter.model.txt')
    print time.time() - s

    item_embeddings, index_dict = load_item_embedding('../model/deep_walk_item_10h_filter.model.txt')
    #
    item_embeddings = normalize(item_embeddings, norm='l2')
    #
    similar_index = train_faiss(item_embeddings, D=32)

    all_sim_nids = set()
    #sim_item_dict
    cold_sim_nid = defaultdict(list)
    for ids, sim_items in enumerate(similar_index):
        sim_temp = []
        N = 0
        for ids_inner, item in enumerate(sim_items):
            if ids == item:
                continue
            if index_dict[item] in filter_nids:
                N += 1
                all_sim_nids.add(index_dict[item])
                sim_temp.append(index_dict[item])
                if N == 10:
                    break
        cold_sim_nid[index_dict[ids]] = sim_temp
    print len(all_sim_nids)
    with open('../data/get_similar_item/cold_sim_nid', 'w') as json_file:
        ujson.dump(cold_sim_nid, json_file)
    # pickle.dump(cold_sim_nid, open('cold_sim_nid', 'wb'), True)





