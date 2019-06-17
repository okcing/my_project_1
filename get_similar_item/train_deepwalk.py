#coding:utf8
from gensim.test.utils import datapath
from gensim.models import word2vec
import time
import gensim

start = time.time()

sentences = word2vec.LineSentence(datapath('/data/wangqianfa_offline/my_project_1/data/construct_train_data/train_data/user_item_random_walk_10h_filter.txt'))


model = word2vec.Word2Vec(sentences, size=32,window=5,min_count=0,workers=32,sg=1,hs=0, negative=5)

model.save("../model/deep_walk_item_10h_filter.model")   #保存模型
model.wv.save_word2vec_format('../model/deep_walk_item_10h_filter.model.txt','../model/vocab_deep_walk_item_10h_filter.txt',binary=False)
print time.time()-start


