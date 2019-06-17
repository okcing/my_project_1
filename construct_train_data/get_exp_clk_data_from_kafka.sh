#取48小时
ssh root@10.18.96.21 "cd /data/amj/News/script;sh log_push.sh 150 deepwalk"
ssh root@10.18.96.21 "cd /data/amj/News/data/log/tmp/deepwalk;cat clk"> clk_10_hour
#ssh root@10.18.96.21 "cd /data/amj/News/data/log/tmp/cov_main;cat exp"> exp
#ssh root@10.18.96.81 "cd /data/amj/News/script;sh non_expand_push.sh 20 wangqianfa"
#ssh root@10.18.96.81 "cd /data/amj/News/data/log/tmp/wangqianfa;cat clk"> clk_1h
#ssh root@10.18.96.81 "cd /data/amj/News/data/log/tmp/wangqianfa;cat exp"> exp_1h



#重写文本,去除推荐频道
#python filter.py


#if [ ! -s filtered_clk ]; then
#    echo '文件内容为空'
#    exit 1
#else
#    echo "ok"
#fi


#cp filtered_clk clk_data/clk
#cd clk_data/
#chmod 777 clk
