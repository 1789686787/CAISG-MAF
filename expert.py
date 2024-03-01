import psycopg2
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="liuwudi",
    password="980416",
    database='test'
)
global cur
cur = conn.cursor()


filepath = '/home/liuwudi/postgres/census1.txt'

file = open(filepath , 'r')

for line in file.readlines() :
    str_list = line.split('\t')
    str_list[9] = str_list[9].replace("\n", "")

    print(str_list)
    sql = "insert into census values(%s);"%("\'"+"\',\'".join(str_list)+"\'")
    print(sql)
    cur.execute(sql)
    conn.commit()






