import psycopg2
import example

class dboperate:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            port=5432,
            user="liuwudi",
            password="980416",
            database='test'
                           )
        self.cur = self.conn.cursor()




    def get_cur(self):
        return self.cur

    def tablename_getter(self):
            tablename_list=[]
            sql = "select tablename from pg_tables where schemaname='public'"
            self.cur.execute(sql)
            tablename_list=self.cur.fetchall()

            # for i in range(len(tablename_list)) :
            #  print(tablename_list[i])

            return tablename_list

    def tableattr_getter(self,tablename):
            attr_list=[]
            sql = "select COLUMN_NAME from information_schema.COLUMNS where table_name = '%s'"%(tablename)
            self.cur.execute(sql)
            tablename_list=self.cur.fetchall()
            # print(tablename_list)
            return tablename_list

    def contribution(self ,  rule , unuse_list , table_name , con_sql):
        sql = con_sql
        count =0
        table_attr = self.tableattr_getter(table_name)
        # print(table_attr)
        # print(rule)
        for i in range(len(unuse_list)) :
            if unuse_list[i] ==0 :
               if rule[count] != '*' :
                  sql +=" and "+ ''.join(table_attr[i]) + "=\'"+str(rule[count])+"\'"
               count +=1
        sql +=";"
        # print(sql)
        self.cur.execute(sql)
        contribute = self.cur.fetchall()
        # print(contribute)
        return contribute

    def create_table(self , tablename):
        sql_drop = "drop table if exists "+tablename+"_test;"
        self.cur.execute(sql_drop)
        self.conn.commit()
        sql_create = "create table "+tablename+"_test as select * from "+tablename
        self.cur.execute(sql_create)
        self.conn.commit()
    def create_context_table(self , tablename):
        sql_drop = "drop table if exists "+tablename+"_context;"
        self.cur.execute(sql_drop)
        self.conn.commit()
        sql_create = "create table "+tablename+"_context as select * from "+tablename
        self.cur.execute(sql_create)
        self.conn.commit()
    def drop_table(self, tablename):
        sql_drop = "drop table "+tablename+"_test;"
        self.cur.execute(sql_drop)
        self.conn.commit()
    def drop_context_table(self, tablename):
        sql_drop = "drop table "+tablename+"_context;"
        self.cur.execute(sql_drop)
        self.conn.commit()

    def delete_table(self , rule , tablename , unuse_list ):
        # print(rule)
        table_attr = self.tableattr_getter(tablename)
        count = 0
        count_first=0
        sql = "delete from "+tablename+"_test where "
        for i in range(len(unuse_list)) :
            if unuse_list[i] ==0 :
               if rule[count] != '*' :
                 if count_first==0 :
                     count_first=1
                 else :
                     sql += " and "
                 sql +=''.join(table_attr[i]) + "=\'"+str(rule[count])+"\'"
               count +=1
        sql +=";"
        self.cur.execute(sql)
        self.conn.commit()

    def delete_context_table(self , rule , tablename , unuse_list ):
        table_attr = self.tableattr_getter(tablename)
        count = 0
        count_first=0
        sql = "delete from "+tablename+"_context where "
        for i in range(len(unuse_list)) :
            if unuse_list[i] ==0 :
               if rule[count] != '*' :
                 if count_first==0 :
                     count_first=1
                 else :
                     sql += " and "
                 sql +=''.join(table_attr[i]) + "=\'"+str(rule[count])+"\'"
               count +=1
        sql +=";"
        self.cur.execute(sql)
        self.conn.commit()
if __name__ == "__main__":

    test1=dboperate()
    # test1.tablename_getter()
    # test1.tableattr_getter('publish')