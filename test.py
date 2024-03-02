import csv
import random

import psycopg2
import numpy as np
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="liuwudi",
    password="980416",
    database='test'
)
cur = conn.cursor()



# data = csv.reader(open('/home/liuwudi/postgres/TPC-H/TPC-H_Tools_v3.0.0/dbgen/lineitem.tbl', 'r', encoding='UTF-8'))
#
# k=0

#
# for d in data:
#
#     # print(d)
#     # d[0] = d[0].replace('|', "|")
#     # str1 = d[0].split('|')
#     # print(d)
#     if d[0][len(d[0])-1] =='|' :
#        d[0] = d[0][0:len(d[0])-2]
#     # print(d[0][len(d[0])-1])
#     # print(len(str1))
#     str = "insert into lineiddtem values(%s);"%('\''+d[0].replace('|' , "\',\'") + '\'')
#     # print(str)
#     cur.execute(str)
#     conn.commit()
#     k+=1
#     if k%100000 == 0 :
#         print(k)
sql = "select l_shipinstruct from q1_3m;"

sql1 = "update q1_3m set l_shipinstruct = 'NONE' where l_shipinstruct = 'NONE                     ';"

# cur.execute(sql)
# conn.commit()
# print(cur.fetchall())

# print(np.random.randint(1,100000,20))

# print(random.sample(range(0,34),1000000))

# 缩小数据库搜索空间
# sql2= "create table q1_100k as (select * from q1_3m order by random() limit 100000);"
#
# cur.execute(sql2)
# conn.commit()

sql2 = "select\
	l_orderkey,\
	sum(l_extendedprice * (1 - l_discount)) as revenue,\
	o_orderdate,\
	o_shippriority from customer,\
	orders,\
	lineitem where c_custkey = o_custkey\
	and l_orderkey = o_orderkey\
	and o_orderdate < l_shipdate group by\
	l_orderkey,\
	o_orderdate,\
	o_shippriority order by revenue desc,\
	o_orderdate;"
cur.execute(sql2)
print(len(cur.fetchall()))

print("successful!")





