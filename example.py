"""
Example script for testing the Azure ttk theme
Author: rdbende
License: MIT license
Source: https://github.com/rdbende/ttk-widget-factory
"""
import os
import time
import tkinter as tk
from tkinter import ttk
import conndb
import explains_generator


class App(ttk.Frame):


    def __init__(self, parent):
        ttk.Frame.__init__(self)
        # Make the app responsive
        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

        #
        self.db=conndb.dboperate()
        self.cur=self.db.get_cur()
        self.query_sql=""
        self.tablename_list=self.db.tablename_getter()
        self.table_attr_list=[]
        # print(self.tablename_list)


        # Create value lists
        self.agg_list = ["sum", "count", "avg", "min", "max"]

        self.k_context = 1
        self.k_value = 4
        self.d_value = 0
        self.l_value = 0
        self.ununse_list = []
        # Create widgets :)
        self.setup_widgets()


    def setup_widgets(self):

        self.aggquery_frame = ttk.Frame(self)
        self.aggquery_frame.place(x=0,y=0,width=800,height=600)

        self.widgets_frame = ttk.LabelFrame(self.aggquery_frame,text="aggrate query")
        self.widgets_frame.place(x=10,y=0,width=780,height=210)
        # self.widgets_frame.columnconfigure(index=0, weight=1)

        #
        ttk.Label(self.widgets_frame, text="Table").place(x=10, y=10)

        self.tablename_combo = ttk.Combobox(
            self.widgets_frame, state="readonly", values=self.tablename_list
        )
        self.tablename_combo.place(x=80, y=5)

        self.tablename_combo.bind('<<ComboboxSelected>>', self.get_table_attr)
        # select
        ttk.Label(self.widgets_frame, text="select").place(x=10, y=45)

        self.select_attr1 = ttk.Label(
            self.widgets_frame,
            justify="center",
        )
        self.select_attr1.place(x=80, y=45)

        self.select_attr2 = ttk.Label(
            self.widgets_frame,
            justify="center",
        )
        self.select_attr2.place(x=160, y=45)

        self.select_attr3 = ttk.Label(
            self.widgets_frame,
            justify="center",
        )
        self.select_attr3.place(x=240, y=45)

        self.select_attr4 = ttk.Label(
            self.widgets_frame,
            justify="center",
        )
        self.select_attr4.place(x=320, y=45)



        self.agg_combo = ttk.Combobox(
            self.widgets_frame, state="readonly", values=self.agg_list
        )
        self.agg_combo.current(0)
        self.agg_combo.place(x=400, y=45 , width=80,height=30)


        self.label = ttk.Label(
            self.widgets_frame,
            text="（",
            justify="center",
        )
        self.label.place(x=490, y=45)

        self.agg_attr_Combo = ttk.Combobox(
            self.widgets_frame, state="readonly"
        )
        self.agg_attr_Combo.place(x=515, y=45,width=100,height=30)

        self.label = ttk.Label(
            self.widgets_frame,
            text="）",
            justify="center",
        )
        self.label.place(x=620, y=45)

        # as
        ttk.Label(self.widgets_frame, text="as").place(x=630, y=45)
        self.as_entry = ttk.Entry(self.widgets_frame)

        self.as_entry.place(x=660, y=45,width=100)
        # from
        ttk.Label(self.widgets_frame, text="from").place(x=10, y=75)
        self.from_tablename = ttk.Label(
            self.widgets_frame,
            justify="center",
        )
        self.from_tablename.place(x=80, y=75)
        # group by
        ttk.Label(self.widgets_frame, text="group by").place(x=10, y=110)
        self.gb_attr_Combo1 = ttk.Combobox(
            self.widgets_frame, state="readonly"
        )
        self.gb_attr_Combo1.place(x=80, y=110,width=75)
        self.gb_attr_Combo1.bind('<<ComboboxSelected>>', self.get_gbvalue1)


        self.gb_attr_Combo2 = ttk.Combobox(
            self.widgets_frame, state="readonly"
        )
        self.gb_attr_Combo2.place(x=160, y=110,width=75)
        self.gb_attr_Combo2.bind('<<ComboboxSelected>>', self.get_gbvalue2)

        self.gb_attr_Combo3 = ttk.Combobox(
            self.widgets_frame, state="readonly"
        )
        self.gb_attr_Combo3.place(x=240, y=110,width=75)
        self.gb_attr_Combo3.bind('<<ComboboxSelected>>', self.get_gbvalue3)

        self.gb_attr_Combo4 = ttk.Combobox(
            self.widgets_frame, state="readonly"
        )
        self.gb_attr_Combo4.place(x=320, y=110,width=75)
        self.gb_attr_Combo4.bind('<<ComboboxSelected>>', self.get_gbvalue4)

        self.select_button = ttk.Button(self.widgets_frame,text="execute query",command=self.start_query)
        self.select_button.place(x=300, y=150,height=35)
        # self.select_button.bind('<<ButtonRelease-1>>', self.start_query())



        # Create a Frame for the Radiobuttons
        self.radio_frame = ttk.LabelFrame(self.aggquery_frame, text="query result")
        self.radio_frame.place(x=10,y=210,width=680,height=380)

        self.result_view_bar = ttk.Scrollbar(self.radio_frame)
        self.result_view_bar.pack(side="right", fill="y")

        self.result_view = ttk.Treeview(self.radio_frame,
                                        columns=(1,2,3,4,5),
                                        show='headings',
                                        yscrollcommand=self.result_view_bar.set)
        self.result_view.column(1, anchor="center", width=120)
        self.result_view.column(2, anchor="center", width=120)
        self.result_view.column(3, anchor="center", width=120)
        self.result_view.column(4, anchor="center", width=120)
        self.result_view.column(5, anchor="center", width=120)
        self.result_view.pack(expand=True, fill="both")
        self.result_view_bar.config(command=self.result_view.yview)


        self.question_frame = ttk.Frame(self.aggquery_frame)
        self.question_frame.place(x=700,y=210,width=100,height=390)

        self.prov_button = ttk.Button(self.question_frame,text="provenance",command=self.provenance)
        self.prov_button.place(rely=0.1)

        self.summarize_button = ttk.Button(self.question_frame,text="summary",command=self.question)
        self.summarize_button.place(rely=0.3)





        self.explain_frame = ttk.LabelFrame(self,text="解释")
        self.explain_frame.place(x=800,y=0,width=790,height=590)

        self.explain_view_bar = ttk.Scrollbar(self.explain_frame )
        self.explain_view_bar.pack(side="right", fill="y")

        self.explain_view_xbar = ttk.Scrollbar(self.explain_frame, orient="horizontal")
        self.explain_view_xbar.pack(side="bottom", fill="x")

        self.explain_view = ttk.Treeview(self.explain_frame,
                                        columns=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20),
                                        show='headings',
                                        yscrollcommand=self.explain_view_bar.set ,
                                        xscrollcommand=self.explain_view_xbar.set
                                         )
        self.explain_view.column(1, anchor="center", width=98)
        self.explain_view.column(2, anchor="center", width=98)
        self.explain_view.column(3, anchor="center", width=98)
        self.explain_view.column(4, anchor="center", width=98)
        self.explain_view.column(5, anchor="center", width=98)
        self.explain_view.column(6, anchor="center", width=98)
        self.explain_view.column(7, anchor="center", width=98)
        self.explain_view.column(8, anchor="center", width=98)
        self.explain_view.column(9, anchor="center", width=98)
        self.explain_view.column(10, anchor="center", width=98)
        self.explain_view.column(11, anchor="center", width=98)
        self.explain_view.column(12, anchor="center", width=98)
        self.explain_view.column(13, anchor="center", width=98)
        self.explain_view.column(14, anchor="center", width=98)
        self.explain_view.column(15, anchor="center", width=98)
        self.explain_view.column(16, anchor="center", width=98)
        self.explain_view.column(17, anchor="center", width=98)
        self.explain_view.column(18, anchor="center", width=98)
        self.explain_view.column(19, anchor="center", width=98)
        self.explain_view.column(20, anchor="center", width=98)
        self.explain_view.pack(expand=True, fill="both")
        self.explain_view_bar.config(command=self.explain_view.yview)
        self.explain_view_xbar.config(command=self.explain_view.xview)


    def get_table_attr(self,event):
        self.from_tablename['text']=self.tablename_combo.get()
        self.db.tableattr_getter(self.tablename_combo.get())
        self.table_attr_list=self.db.tableattr_getter(self.tablename_combo.get())
        # print(self.table_attr_list)
        self.agg_attr_Combo['values']=self.table_attr_list
        tup=("",)

        self.gb_attr_Combo1['values'] = self.table_attr_list
        self.gb_attr_Combo1['values'] = tup+self.gb_attr_Combo1['values']

        self.gb_attr_Combo2['values'] = self.table_attr_list
        self.gb_attr_Combo2['values'] = tup+self.gb_attr_Combo2['values']

        self.gb_attr_Combo3['values'] = self.table_attr_list
        self.gb_attr_Combo3['values'] = tup+self.gb_attr_Combo3['values']

        self.gb_attr_Combo4['values'] = self.table_attr_list
        self.gb_attr_Combo4['values'] = tup+self.gb_attr_Combo4['values']


    def start_query(self):
        for k in range(6) :
         self.result_view.heading(k,text="")

        for child in self.result_view.get_children():
            self.result_view.delete(child)

        # 加载属性
        i = 1
        if len(self.gb_attr_Combo1.get())!=0 :
          self.result_view.heading(i,text=self.gb_attr_Combo1.get())
          i+=1
        if len(self.gb_attr_Combo2.get())!=0 :
          self.result_view.heading(i,text=self.gb_attr_Combo2.get())
          i+=1
        if len(self.gb_attr_Combo3.get())!=0 :
          self.result_view.heading(i,text=self.gb_attr_Combo3.get())
          i+=1
        if len(self.gb_attr_Combo4.get())!=0 :
          self.result_view.heading(i,text=self.gb_attr_Combo4.get())
          i+=1
        self.result_view.heading(i,text=self.as_entry.get())


        self.query_sql="select "+self.gbvalue()+","+self.agg_combo.get()+"("+ self.agg_attr_Combo.get() +") as " + self.as_entry.get() + " from " +self.tablename_combo.get() + " group by " +self.gbvalue()+ " order by "+ self.as_entry.get()+" desc;"

        self.cur.execute(self.query_sql)

        agg_result=self.cur.fetchall()
        for result_index in range(len(agg_result)) :
            self.result_view.insert('','end',value=agg_result[result_index] )


    def gbvalue(self):
        gbstr=""
        if len(self.gb_attr_Combo1.get())!=0 :
          if len(gbstr)!=0 : gbstr+=","
          gbstr+=self.gb_attr_Combo1.get()
        if len(self.gb_attr_Combo2.get())!=0 :
          if len(gbstr)!=0 : gbstr+=","
          gbstr+=self.gb_attr_Combo2.get()
        if len(self.gb_attr_Combo3.get())!=0 :
          if len(gbstr)!=0 : gbstr+=","
          gbstr+=self.gb_attr_Combo3.get()
        if len(self.gb_attr_Combo4.get())!=0 :
          if len(gbstr)!=0 : gbstr+=","
          gbstr+=self.gb_attr_Combo4.get()
        return gbstr

    def where_value(self):

        result_List=self.result_view.item(self.result_view.selection(), "value")
        i = 0
        where_str = ""
        if len(self.gb_attr_Combo1.get())!=0 :
          if len(where_str)!=0 : where_str+=" and "
          where_str+=self.gb_attr_Combo1.get() + "= '" + result_List[i] + '\''
          i += 1
        if len(self.gb_attr_Combo2.get())!=0 :
          if len(where_str)!=0 : where_str+=" and "
          where_str+=self.gb_attr_Combo2.get() + "= '" + result_List[i] + '\''
          i += 1
        if len(self.gb_attr_Combo3.get())!=0 :
          if len(where_str)!=0 : where_str+=" and "
          where_str+=self.gb_attr_Combo3.get() + "= '" + result_List[i] + '\''
          i += 1
        if len(self.gb_attr_Combo4.get())!=0 :
          if len(where_str)!=0 : where_str+=" and "
          where_str+=self.gb_attr_Combo4.get() + "= '" + result_List[i] + '\''
          i += 1

        # print(where_str)
        return where_str


    def get_gbvalue1(self,event):
        self.select_attr1['text'] = self.gb_attr_Combo1.get()+" ,"
    def get_gbvalue2(self,event):
        self.select_attr2['text'] = self.gb_attr_Combo2.get()+" ,"
    def get_gbvalue3(self, event):
        self.select_attr3['text'] = self.gb_attr_Combo3.get()+" ,"
    def get_gbvalue4(self, event):
        self.select_attr4['text'] = self.gb_attr_Combo4.get()+" ,"


    def provenance(self):

        for k in range(21) :
         self.explain_view.heading(k,text="")

        for child in self.explain_view.get_children():
            self.explain_view.delete(child)


        for i in range(1,len(self.table_attr_list)+1) :
            self.explain_view.heading(i,text=self.table_attr_list[i-1])




        # sql_prov = "select " +" provenance " + self.gbvalue() + "," \
        #              + self.agg_combo.get() + "(" + self.agg_attr_Combo.get() + ") as " + self.as_entry.get() \
        #              + " from " + self.tablename_combo.get() \
        #              + " where " + self.where_value()\
        #              + " group by " + self.gbvalue() \
        #              + ";"
        # # print(sql_prov)
        # self.cur.execute(sql_prov)
        #
        # provlist = self.cur.fetchall()

        provlist = self.get_provenance()


        attr_num = self.gbvalue().count(',', 0, len(self.gbvalue()))+2


        # print(provlist)
        # print(self.gbvalue())
        for result_index in range(len(provlist)):
            self.explain_view.insert('', 'end', value=provlist[result_index][attr_num:])



    def get_provenance(self):
        sql_prov = "select " +" provenance " + self.gbvalue() + "," \
                     + self.agg_combo.get() + "(" + self.agg_attr_Combo.get() + ") as " + self.as_entry.get() \
                     + " from " + self.tablename_combo.get() \
                     + " where " + self.where_value()\
                     + " group by " + self.gbvalue() \
                     + ";"
        # print(sql_prov)
        self.cur.execute(sql_prov)

        provlist = self.cur.fetchall()
        return provlist

    def get_attrlist(self):
        return self.table_attr_list


    def question(self):
        global max_rule
        t1 = time.clock()

        sql_prov = "select " +" provenance " + self.gbvalue() + "," \
                     + self.agg_combo.get() + "(" + self.agg_attr_Combo.get() + ") as " + self.as_entry.get() \
                     + " from " + self.tablename_combo.get() \
                     + " where " + self.where_value()\
                     + " group by " + self.gbvalue() \
                     + ";"

        sql_context = "select " +" provenance " + self.gbvalue() + "," \
                     + self.agg_combo.get() + "(" + self.agg_attr_Combo.get() + ") as " + self.as_entry.get() \
                     + " from " + self.tablename_combo.get() \
                     + " where not(" + self.where_value()\
                     + ") group by " + self.gbvalue() \
                     + ";"



        self.cur.execute(sql_prov)
        prov_list=self.cur.fetchall()

        prov_list = self.delete_space(prov_list)


        self.cur.execute(sql_context)
        context_list = self.cur.fetchall()
        context_list = self.delete_space(context_list)


        # prov_list = self.insertsign(prov_list)
        # print(self.result_view.item(self.result_view.selection(),"value"))
        # print(self.agg_combo.get())
        # print(self.cur.fetchall())

        # explains
        explain = explains_generator.explains()

        #
        explain_list = explain.generator(prov_list ,
                                         self.result_view.item(self.result_view.selection(),"value") , 1 ,
                                         self.agg_combo.get(), self.table_attr_list , self.agg_attr_Combo.get() ,
                                         self.tablename_combo.get() , self.get_contribution_sql(0),False)

        self.ununse_list = explain.unuse_List_getter()
        del explain

        t22=time.clock()
        # with MAF algorithm
        print("provenance cost："+str(t22-t1))

        print("-----------------------------------------------------------context summary------------------------------------------------------")
        explain = explains_generator.explains()

        explain_context_list = explain.generator(context_list,
                                              self.result_view.item(self.result_view.selection(), "value"), 1,
                                              self.agg_combo.get(), self.table_attr_list, self.agg_attr_Combo.get(),
                                              self.tablename_combo.get(), self.get_contribution_sql(1),True)

        for i in explain_list:
          i.append("")
        for j in explain_context_list:
          j.append("")
        for rule in explain_list:
          for crule in explain_context_list:
            for index in range(len(crule)-2):
               if (crule[index] == "*" and rule[index] !="*") or (rule[index] !="*" and crule[index] !="*" and rule[index] != crule[index]) :
                   break
               if(index == len(crule)-3) :
                   rule[len(crule)-1] = "public"
                   crule[len(crule) - 1] = "public"
        for rule in explain_list:
            if rule[len(rule)-1] != "public" :
               rule[len(rule) - 1] = "private"
        for crule in explain_context_list:
            if crule[len(crule)-1] != "public" :
               crule[len(crule) - 1] = "private"

    #context replace
        for k in range(self.k_context):
            max_rule = []
            min_rule = []
            min_rule_id = 0
            for crule in explain_context_list :
                if crule[len(crule)-1] == "private" and crule[len(crule)-2] != 0 :
                   max_rule = crule
                   break
            if max_rule == [] :
                break
            for i in range(len(explain_list)) :
                rule = explain_list[i]
               # print(rule[len(rule)-2])
               # print(max_rule[len(max_rule)-2])
                if rule[len(rule) - 1] != "context":
                   min_rule_id = i
                   min_rule = explain_list[min_rule_id]
            if min_rule == []:
               break
            if min_rule[len(min_rule)-1] != "context" and min_rule[len(min_rule)-2] < max_rule[len(max_rule)-2]:
                   explain_list[min_rule_id] = list(max_rule)
                   explain_list[min_rule_id][len(min_rule)-1] = "context"
                   max_rule[len(min_rule)-2] = 0
                   max_rule[len(min_rule)-1] = "context"


        print("-----------------------------------------provenance summary：")
        for i in explain_list:
          print(i)
        print("-----------------------------------------context summary：")
        for i in explain_context_list:
          print(i)




        del explain

        t2 = time.clock()
        print("total cost：" + str(t2 - t1))






        for k in range(21) :
         self.explain_view.heading(k,text="")

        for child in self.explain_view.get_children():
            self.explain_view.delete(child)

        count_a = 1




        for i in range(1,len(self.table_attr_list)+1) :
          if self.ununse_list[i-1] != -1 :
            self.explain_view.heading(count_a,text=self.table_attr_list[i-1])
            count_a +=1



        self.explain_view.heading(len(self.table_attr_list), text="score")
        self.explain_view.heading(len(self.table_attr_list)+1, text="Type")

        for i in range(1 , len(explain_list)+1) :
            self.explain_view.insert('', 'end', value = explain_list[i-1])

        self.explain_view.insert('', 'end', value = ['---','---','---','---','---','---','---','---','---','---'])

        for i in range(1 , len(explain_context_list)+1) :
            self.explain_view.insert('', 'end', value=explain_context_list[i - 1])





        return explain_list

    def low_question(self):
        explain_list = []

        sql_prov = "select " +" provenance " + self.gbvalue() + "," \
                     + self.agg_combo.get() + "(" + self.agg_attr_Combo.get() + ") as " + self.as_entry.get() \
                     + " from " + self.tablename_combo.get() \
                     + " where " + self.where_value()\
                     + " group by " + self.gbvalue() \
                     + ";"

        # print(prov_query)

        self.cur.execute(sql_prov)

        # print(self.result_view.item(self.result_view.selection(),"value"))
        # print(self.agg_combo.get())
        # print(self.cur.fetchall())
        # explain.generator(self.cur.fetchall() , self.result_view.item(self.result_view.selection(),"value") , 0 , self.agg_combo.get() , self.table_attr_list,self.agg_attr_Combo.get())

        return explain_list

    def get_contribution_sql(self , sign):
        count = 0
        con_sql=""
        if len(self.gb_attr_Combo1.get())!=0 :
          if len(con_sql)!=0 : con_sql+=" and "
          con_sql+=str(self.gb_attr_Combo1.get())+"=\'"+self.result_view.item(self.result_view.selection(),"value")[count]+"\'"
          count += 1
        if len(self.gb_attr_Combo2.get())!=0 :
          if len(con_sql)!=0 : con_sql+=" and "
          con_sql+=str(self.gb_attr_Combo2.get())+"=\'"+self.result_view.item(self.result_view.selection(),"value")[count]+"\'"
          count += 1
        if len(self.gb_attr_Combo3.get())!=0 :
          if len(con_sql)!=0 : con_sql+=" and "
          con_sql+=str(self.gb_attr_Combo3.get())+"=\'"+self.result_view.item(self.result_view.selection(),"value")[count]+"\'"
          count += 1
        if len(self.gb_attr_Combo4.get())!=0 :
          if len(con_sql)!=0 : con_sql+=" and "
          con_sql+=str(self.gb_attr_Combo4.get())+"=\'"+self.result_view.item(self.result_view.selection(),"value")[count]+"\'"
          count +=1

        if sign == 0 :
            if self.agg_combo.get()=="sum" or self.agg_combo.get()=="avg":
                sql = "select sum("+self.agg_attr_Combo.get()+") from "+self.tablename_combo.get() + "_test where "+con_sql
            else :
                sql = "select count(" + self.agg_attr_Combo.get() + ") from " + self.tablename_combo.get() + "_test where " + con_sql
        else :
            if self.agg_combo.get() == "sum" or self.agg_combo.get() == "avg":
                sql = "select sum(" + self.agg_attr_Combo.get() + ") from " + self.tablename_combo.get() + "_context where not(" + con_sql+")"
            else:
                sql = "select count(" + self.agg_attr_Combo.get() + ") from " + self.tablename_combo.get() + "_context where not(" + con_sql+")"
        return sql


    def delete_space(self , orgin_list):
        fin_list=[]
        for i in orgin_list :
            x=[]
            for j in range(len(i)):

                if isinstance(i[j],str) == True:
                    x.append(i[j].replace(' ',''))
                else:
                    x.append(i[j])
            fin_list.append(tuple(x))
        return fin_list

if __name__ == "__main__":


    root = tk.Tk()
    root.title("query explain system")

    # Simply set the theme
    root.tk.call("source", "azure.tcl")
    root.tk.call("set_theme", "light")

    app = App(root)
    app.pack(fill="both", expand=True)

    # Set a minsize for the window, and place it in the middle
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    # root.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))
    root.geometry('1600x600+100+100')
    root.mainloop()

    # root1 = tk.Tk()
    # root1.geometry('1300x600+100+100')
    # root1.mainloop()