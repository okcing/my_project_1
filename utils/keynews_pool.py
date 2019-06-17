#coding=utf8
'''
希望能够提供一个方法，可以获取要闻正排池中，新闻的oid-nid的字典
'''
import redis
from collections import defaultdict

class KeynewsPool(object):

    def __init__(self, host, port, password, db):
        '''
        :param host: redis的ip
        :param port: redis的端口
        :param password: redis的密码
        :return:
        '''
        self.host = host
        self.port = port
        self.password = password
        self.db = db

    def connect_db(self):
        pool = redis.ConnectionPool(host=self.host, port=self.port, password=self.password, decode_responses=True, db=self.db)
        r = redis.StrictRedis(connection_pool=pool)

        return r

    #s.t.d.redis.sohucs.com


    def get_data(self):
        r = self.connect_db()
        keys = r.keys()
        oid_nid_dict = defaultdict(str)
        xxxx=0
        for k in keys:
            try:
                if xxxx%10000==0:
                    print xxxx
                xxxx+=1
                json_info = r.hgetall(k)
                oid_nid_dict[json_info['oid']] = k
            except:
                pass

        return oid_nid_dict

    def get_nid_oid_dict(self):
        r = self.connect_db()
        keys = r.keys()
        nid_oid_dict = defaultdict(str)
        for k in keys:
            try:
                json_info = r.hgetall(k)
                nid_oid_dict[k] = json_info['oid']
            except:
                pass

        return nid_oid_dict

    def get_oid_set(self):
        r = self.connect_db()
        keys = r.keys()
        oid_set = set()

        for k in keys:
            try:
                json_info = r.hgetall(k)
                oid_set.add(json_info['oid'])
            except:
                pass
        return oid_set



    def get_nid_set(self):
        r = self.connect_db()
        nid = r.keys()
        return nid


    # def get_keynews_sample(self):
    #     r = self.connect_db()
    #     for nid in r.keys():
    #         key_news_sample = r.hgetall(nid)
    #         break
    #     return key_news_sample

