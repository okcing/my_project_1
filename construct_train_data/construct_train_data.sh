#得到点击数据
sh get_exp_clk_data_from_kafka.sh

#数据筛选，并且得到edgelist
python get_user_edge_list.py

#得到邻居节点
/data/wangqianfa/anaconda2/bin/python get_neighbors.py

#随机游走生成序列
python user_item_random_walk.py

#将随机游走的序列移入文件夹
mv ../data/construct_train_data/user_item_random_walk_10h_filter.txt ../data/construct_train_data/train_data/user_item_random_walk_10h_filter.txt
