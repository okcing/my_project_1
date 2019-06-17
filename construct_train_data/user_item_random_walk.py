#coding=utf8
import time
import random
import cPickle as pickle
import ujson

start = time.time()

#加载邻居字典
with open('../data/construct_train_data/user_item_edgelist_10h_filter.json', 'r') as json_file:
    node_neighbors = ujson.load(json_file)
print time.time() - start
start = time.time()

#实现功能，在随机游走时，把user和item分开

#构建一个random_walk 的函数,这个函数可以在一个图上面进行random walk，最终再得到序列
def deepwalk_walk(walk_length, start_node):
    # print('walk_length', walk_length, 'start_node', start_node)
    #添加出事节点
    walk = [start_node]
    # print('walk', walk)
    while len(walk) < walk_length:
        #得到最后的节点
        cur = walk[-1]
        nei_node = random.choice(node_neighbors[cur])
        # print 'cur', cur
        #得到邻居节点，得到候选列表
        # cur_nbrs = list(node_neighbors[cur])
        #得到概率列表
        # probality = []
        # for nei in cur_nbrs:
        #     print nei, edge_probality[(cur, nei)]
            # probality.append(edge_probality[(cur, nei)])
        walk.append(nei_node)
    return walk

walks = []
nodes = node_neighbors.keys()
print(type(nodes))
nodes = list(nodes)

with open('../data/construct_train_data/user_item_random_walk_10h_filter.txt', 'w') as new_session:
    for i in range(2):
        random.shuffle(nodes)
        print 'epoch', i
        for index, v in enumerate(nodes):
            # print('v',v)
            #if index%10000==0:
            #    print 'index', index
            walks = deepwalk_walk(40, v)
            #这是一个cid，表示user的
            if len(v.split('-'))==2:
                for n, w in enumerate(walks):
                    # print w
                    if n%2==0:
                        new_session.write(w + '\t')
                new_session.write('\n')
            #nid
            else:
                for n, w in enumerate(walks):
                    # print w
                    if n%2!=0:
                        new_session.write(w + '\t')
                new_session.write('\n')
            # break

print time.time() - start
