#得到点击数据
#sh get_exp_clk_data_from_kafka.sh

#数据筛选，并且得到edgelist
#python get_user_edge_list.py

#得到邻居节点
#/data/wangqianfa/anaconda2/bin/python get_neighbors.py

#随机游走生成序列
#python user_item_random_walk.py

#训练word2vec
python train_deepwalk.py

#保存每个nid的相似nid
#python get_cold_sim_nid.py
/data/wangqianfa/anaconda2/bin/python get_cold_sim_nid_faiss.py

/data/wangqianfa/anaconda2/bin/python get_sim_nid_faiss.py

#生成之后移入文件夹
mv ../data/get_similar_item/cold_sim_nid ../data/get_similar_item/cold_sim
mv ../data/get_similar_item/sim_nid ../data/get_similar_item/cold_sim
#打印出来观察标题相似
#python visual_title_sim.py
