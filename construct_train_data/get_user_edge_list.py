#coding:utf8
'''
得到用户-新闻对，构成edgelist
策略：
1。点击量大的用户,要去掉，因为他们的兴趣面太广泛了,暂定前100
2。对于点击很多的item，要去掉，但不能去掉太多，暂定3个
2。仅有过N次点击的item，要去掉，无法准确计算，而且没必要计算这个，暂定5个，因为10小时才被点击了5次，说明不是什么好新闻
3。仅有过一次点击的用户，要去点，因为这个不能带来序列的信息，这个不要去掉太多
'''
import ujson
from collections import defaultdict
from operator import itemgetter
import time

start = time.time()

#用户计数
user_count = defaultdict(int)
#item计数
item_count = defaultdict(int)


#在每一行中，提取用户和点击新闻，并写入文件
with open('clk_10_hour', 'r') as clkic_file:
    for index, item in enumerate(clkic_file):
        #if index%100000==0:
        #    print index
        try:
            info = ujson.loads(item)
            # nid = info['nid']文章
            # cid = info['cid']用户
            if info["channelid"] != "1":
                continue
            user_count[info['cid']]+=1
            item_count[info['nid']]+=1
        except Exception as e:
            pass

# user_count_file = open('user_count_10_h', 'w')
sorted_user = sorted(user_count.iteritems(), key=itemgetter(1), reverse=True)
# for i in sorted_user:
#     user_count_file.write(str(i)+'\n')

sorted_item = sorted(item_count.iteritems(), key=itemgetter(1), reverse=True)
#for i in sorted_item:
#    print i
#打开文件

#设定用户和item黑名单
black_user = set()
for index, i in enumerate(sorted_user):
    if index<100 or i[1]==1:
        # print i
        black_user.add(i[0])

black_item = set()
for index, i in enumerate(sorted_item):
    if index<3 or i[1]<=10:
        # print i,'item'
        #print type(i[1])
        black_item.add(i[0])

print '黑名单user数量', len(black_user)
print '黑名单item数量', len(black_item)


#打开edgelist文件
user_item_edgelist = open('../data/construct_train_data/user_item_edgelist_10h_filter', 'w')

#在每一行中，提取用户和点击新闻，并写入文件
with open('clk_10_hour', 'r') as click_file:
    for index, item in enumerate(click_file):
        #if index%100000==0:
        #    print index
        try:
            info = ujson.loads(item)
            # nid = info['nid']文章
            # cid = info['cid']用户
            if info["channelid"] != "1":
                continue
            if info['nid'] in black_item or info['cid'] in black_user:
                continue
            user_item_edgelist.write(info['cid']+'\t'+info['nid']+'\n')
        except Exception as e:
            pass

user_item_edgelist.close()

print time.time() - start