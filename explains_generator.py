import time

import numpy as np
from collections import defaultdict
import conndb
import numpy

class explains:
    def __init__(self):
        self.k=4
        self.d=2
        self.l=1
        self.prov_list=[]
        self.question_tuple=[]
        self.mark = 0
        self.agg_function = ""
        self.db=conndb.dboperate()
        self.cur=self.db.get_cur()
        self.attr_list = []
        self.agg_attr = ""
        self.attr_num = 0
        self.len_al=len(self.attr_list)
        self.len_pl=len(self.prov_list)
        self.len_qt = len(self.question_tuple)
        self.hash_attr = {}
        self.unuse_list=[]
        self.use_list=[]
        self.explain_len = 0
        self.weight_list = []
        self.final = 0
        self.max_weight = 0
        self.explains_dict = {}
        self.sumtime  = 0
        self.table_name = ""
        self.con_sql = ""
        # min number of attributes in summary
        self.min_attr = 2
        self.max_attr = 5
        self.prov_sum = 0
        self.prov_count = 0
        self.match_count = 0
        self.attr_list = []


        self.hash_test = {}
        self.hash_unuserule = {}
        self.hash_contri = {}
        self.final_explains={}
        self.coverage_dict = {}
        # test
        self.match_count = 0
    #    impact
        self.impact_list = []
    def generator(self , prov_list , question_tuple , mark , agg_function , attr_list , agg_attr , table_name , con_sql ,context):
        self.explain_len = 0
        self.question_tuple = question_tuple
        self.mark = mark
        self.agg_function = agg_function
        self.attr_list = attr_list
        self.agg_attr = agg_attr
        self.len_al=len(attr_list)
        self.len_pl=len(prov_list)
        self.len_qt = len(question_tuple)
        self.table_name = table_name
        self.con_sql = con_sql
        self.attr_list = attr_list
        explains_list = []




        for i in range(len(prov_list)):
            self.prov_list.append(prov_list[i][self.len_qt:])
        # print(self.prov_list)


        for i in range(self.len_al) :
            # print(self.attr_list[i][0] + "：" + self.agg_attr)
            if self.attr_list[i][0] == self.agg_attr :
                self.attr_num = i
                break
        # sensitivity analysis
        if agg_function == "avg" :
            self.prov_sum = 0
            for i in self.prov_list :
                self.prov_sum += float(i[self.attr_num])
        self.prov_count = len(self.prov_list)
            # print(self.prov_sum)

        # unuse attributes
        unuse_list=self.unuse_attr()

        # print(unuse_list)


        # get attr list
        attr_list = self.get_attr()

        # print(attr_list)
        print(unuse_list)

        # for i in range(len(attr_list)) :
        #     if len(attr_list[i]) == 1 :
        #         unuse_list[i] = 1

        # print(attr_list)
        # get weight
        self.weight_list = self.weight(attr_list , unuse_list)
        #print("weight list：")
       # print(self.weight_list)
        # print(unuse_list)
       # print(attr_list)

        explain_attrnum = 0
        for i in range(len(unuse_list)):
            if unuse_list[i] == 0:
                explain_attrnum += 1

        self.unuse_list = unuse_list
        self.use_list = attr_list
        # get length
        for i in range(len(self.unuse_list)) :
          if self.unuse_list[i] ==0 :
           self.explain_len +=1

        # print(self.prov_list)

        # find last 0 in unuse_list
        for i in range(len(self.use_list)):
            if self.unuse_list[i] == 0:
                self.final = i

        coverage = {}
        # generate summary
        for i in range(self.k) :
          # print(len(self.prov_list))
          self.explains_dict = {}
          self.hash_unuserule ={}
          self.match_count = 0
          self.generator_explains(1,{},0)
          if len(self.explains_dict) != 0:

             best_rule = max(self.explains_dict, key=lambda x: self.explains_dict[x])

             self.impact_list.append(self.hash_contri[best_rule])
             # print("---------------------------------------------------"+best_rule)
             # print("---------------------------------------------------"+str(self.coverage_dict[best_rule]))
             coverage[str(best_rule)] = self.coverage_dict[str(best_rule)]



             self.delete_abrule(str(best_rule).split())

             self.final_explains.update({best_rule: self.explains_dict[best_rule]})
        #  update  contribution
             self.update_hash_contri(str(best_rule).split())



        var = 0
        for rule in list(self.final_explains.keys()):

            explains_list.append([])
            list_rule = str(rule).split(' ')
            varcount1 = 0
            for i in range(len(self.unuse_list)) :
               # if self.unuse_list[i] == -1 :
               #     explains_list[var].append('*')

               if self.unuse_list[i] == 1 :
                   explains_list[var].append('*')

               if self.unuse_list[i] == 0 :
                   explains_list[var].append(list_rule[varcount1])
                   varcount1 += 1
            explains_list[var].append(self.final_explains[rule])
            var+=1

        # print(self.sumtime)
        print("-----------------------------------------summary：")
        cc = 0
        for i in coverage:
          print(str(i) + " Coverage: "+str(coverage[i])+"  Impact: "+str(self.impact_list[cc]))
          cc+=1
        return explains_list


    # get attr
    def get_attr(self):
        useattr_list = []

        # sum or avg
        if self.agg_function == "sum" or self.agg_function == "avg" :

            # print(self.prov_list)
            for i in range(len(self.attr_list)) :
                temp_list=[]
                if self.attr_num == i:
                    useattr_list.append(temp_list)
                    continue
                for j in range(len(self.prov_list)) :
                    if self.prov_list[j][i] not in temp_list :
                        temp_list.append(self.prov_list[j][i])
                useattr_list.append(temp_list)

            # for i in range(len(self.prov_list)) :
            #  print(self.prov_list[i])

        if self.agg_function == "count" or self.agg_function == "min" or self.agg_function == "max" :

          for i in range(len(self.attr_list)):
            temp_list = []
            if self.attr_num == i :
                useattr_list.append(temp_list)
                continue
            for j in range(len(self.prov_list)):
                  if self.prov_list[j][i] not in temp_list :
                    temp_list.append(self.prov_list[j][i])
            useattr_list.append(temp_list)

        # print(useattr_list)



        return useattr_list

    # attribute filter/MAF algorithm , You can specify a list of attributes, or directly use the filtered attributes
    # unuse_list  unuse attributes = 1 , aggrate attribute = -1 , normal attribute = 0
    def unuse_attr(self ):
        sql = "SELECT * FROM %s"%(self.table_name)
        self.cur.execute(sql)
        prov_list = self.cur.fetchall()
        # cur.execute(sql)
        # print(cur.fetchall())
        print("*************MAF*******************")


        #prov_list = self.prov_list

        attr_list = list(range(len(self.attr_list)))
        unuse_list = [0]*len(attr_list)
       # print(prov_list)
        # ************************dispersive attributes***************************************
        T_dispersive = min(50 , len(prov_list)-1)
        attr_value_counts = {}
        for tup in prov_list:
            for attr_index in attr_list:
                attr_value = tup[attr_index]
                if attr_index not in attr_value_counts:
                    attr_value_counts[attr_index] = set()
                attr_value_counts[attr_index].add(attr_value)


        attributes_with_over_n_values = []
        for attr_index, values_set in attr_value_counts.items():
            if len(values_set) > T_dispersive:
                attributes_with_over_n_values.append(attr_index)
                unuse_list[attr_index] = 1
        print(f"dispersive attributes", attributes_with_over_n_values)
        # ************************object attributes***************************************
        T_object = 0.9

        attr_value_counts = {}

        total_tuples = len(prov_list)


        for tup in prov_list:
            for attr_index in attr_list:
                attr_value = tup[attr_index]
                if attr_index not in attr_value_counts:
                    attr_value_counts[attr_index] = {}
                if attr_value not in attr_value_counts[attr_index]:
                    attr_value_counts[attr_index][attr_value] = 0
                attr_value_counts[attr_index][attr_value] += 1

        attributes_below_threshold = []
        for attr_index, value_counts in attr_value_counts.items():
            for value, count in value_counts.items():
                if count / total_tuples > T_object:
                    attributes_below_threshold.append((attr_index, value))
                    unuse_list[attr_index] = 1
        print(f"object attributes：", attributes_below_threshold)


        # ************************dependent attributes***************************************
        T_dependent = 0.95

        column_lists = [[] for _ in range(len(prov_list[0]))]

        for tuple_item in prov_list:
            for index, item in enumerate(tuple_item):
                column_lists[index].append(item)
       # print(column_lists)
        for i in range(len(column_lists)-1):
           for j in range(i+1 , len(column_lists)):
              if  unuse_list[i] ==0 and self.dependent(column_lists[i] , column_lists[j] , T_dependent):
                print(f"dependent attributes：" , attr_list[j])
                unuse_list[j] = 1
              if  unuse_list[j] ==0 and self.dependent(column_lists[j], column_lists[i], T_dependent):
                print(f"dependent attributes：", attr_list[i])
                unuse_list[i] = 1

        print("********************************")
        unuse_list[self.attr_num] = -1
        print(unuse_list)


        return unuse_list
        # census
       # return [0,-1,0,1,0,0,0,0,1,0]
        # movies
       # return [1,0,0,1,-1,1,0,0]
        # return [0, -1, 0, 0, 1, 1, 0, 0]


    #  dependent
    def dependent(self , list1 , list2 , rate):

        pair_count_dict = defaultdict(int)
        key_count_dict = defaultdict(int)


        for key, value in zip(list1, list2):
            pair_count_dict[(key, value)] += 1
            key_count_dict[key] += 1


        key_pair_ratio = defaultdict(dict)
        for (key, value), count in pair_count_dict.items():
            ratio = count / key_count_dict[key]
            key_pair_ratio[key][(key, value)] = ratio
           # print(f"Key: {key}, Value: {value}, Ratio: {ratio}")


        for key, ratios in key_pair_ratio.items():
            max_ratio = max(ratios.values())
            if max_ratio <= rate:
                return False
        return True

    # weight function
    def weight(self ,attr_list , unuse_list):
        weight_list  = []
        max = 0
        sum = 0.00

        # for i in range(self.len_al) :
        #     if unuse_list[i] == 1 or unuse_list[i] == -1 or len(attr_list[i]) == 1 :
        #         weight_list.append(-1.00)
        #         continue
        #     else :
        #         weight_list.append(len(attr_list[i])**0.5)
        #         sum+=len(attr_list[i])**0.5
        # for i in range(len(weight_list)) :
        #     if weight_list[i] !=-1.0 :
        #         weight_list[i]=round(weight_list[i]/sum,2)
        #     if weight_list[i] > max :
        #        max = weight_list[i]


        for i in range(self.len_al):
            if unuse_list[i] == 1 or unuse_list[i] == -1 or len(attr_list[i]) == 1 :
                weight_list.append(-1.00)
            else :
                weight_list.append(1.00)
        max=1


        self.max_weight = max
        return weight_list

    # generator
    def generator_explains(self, attrnum , current_list , current_max):

       create_rule = []
       current_list = current_list
       temp_list = {}



       t1 = time.clock()
       for i in range(self.explain_len) :
           create_rule.append('*')

       if attrnum == 1 :
           count = 0
           for i in range(len(self.use_list)) :
               if self.unuse_list[i] != 0 :
                   continue
               else :
                   for j in self.use_list[i] :
                     create_rule[count] = str(j)
                     # print(create_rule)
                     # print(self.explain_match(create_rule))
                     # temp_list[" ".join(create_rule)] = round(float(self.explain_match(create_rule , self.prov_list)) * float(self.weight_list[i]),2)
                     # print(self.hash_contri[" ".join(create_rule)])
                     if " ".join(create_rule) not in self.hash_contri or self.hash_contri[" ".join(create_rule)] == -1:
                         temp_list[" ".join(create_rule)] = float(self.explain_match(create_rule, self.prov_list)) * float(self.weight_list[i])
                     else :
                         temp_list[" ".join(create_rule)] = float(self.hash_contri[" ".join(create_rule)]) * float(self.weight_list[i])
                     if current_max < temp_list[" ".join(create_rule)] :
                         current_max = temp_list[" ".join(create_rule)]
                   create_rule[count] = '*'
                   count += 1
       else :
          for rule in  list(current_list.keys()) :
              count = 0
              list_rule=str(rule).split(' ')
              for i in range(len(self.use_list)):
                  if self.unuse_list[i] != 0:
                      continue
                  else :
                      if list_rule[count] == '*' :
                         for j in self.use_list[i] :

                             list_rule[count] = j
                             # print(" ".join('%s' %id for id in list_rule))

                             if  " ".join('%s' %id for id in list_rule) not in temp_list and " ".join('%s' %id for id in list_rule) not in self.hash_unuserule:
                                 # 查看是否满足剪枝的条件
                                 temp_count = 0
                                 weight_value = 0
                                 star_count = 0
                                 for k in range(len(self.use_list)):
                                     if self.unuse_list[k] != 0:
                                         continue
                                     else:
                                         if list_rule[temp_count] =='*' :
                                            star_count += 1
                                         else :
                                            weight_value += float(self.weight_list[k])
                                         temp_count +=1
                                 if " ".join('%s' %id for id in list_rule) not in self.hash_contri or self.hash_contri[" ".join('%s' %id for id in list_rule)]==-1:
                                     cont = float(self.explain_match(list_rule, self.prov_list))
                                 else :
                                     cont = float(self.hash_contri[" ".join('%s' % id for id in list_rule)])

                                 # print(cont * (temp_count * self.max_weight + weight_value))
                                 # print(current_max)
                                 # print(list_rule)
                                 # print("cont " + str(cont) + " weight " + str(weight_value))

                                 if cont * (temp_count * self.max_weight + weight_value) >= current_max:

                                   temp_list[" ".join('%s' % id for id in list_rule)] = cont * weight_value

                                   if current_max < temp_list[" ".join('%s' %id for id in list_rule)]:
                                       current_max = temp_list[" ".join('%s' %id for id in list_rule)]
                                 else :
                                    self.hash_unuserule[" ".join('%s' %id for id in list_rule)] = 1

                             list_rule[count] = '*'
                      count += 1

       # print(current_max)
       print("number of candidates："+str(len(temp_list)))

       print(temp_list)
       print(self.match_count)
       # for i in temp_list :
       #    if temp_list[i] == 0 :
       #        print(i)
       # 递归生成

       if attrnum >= 2 :
          self.explains_dict.update(temp_list)

       t2 = time.clock()
       print(t2-t1)

       if attrnum+1 <= self.explain_len :
         self.generator_explains( attrnum+1 , temp_list ,current_max)


       # return dict(sorted(self.explains_dict.items(), key=lambda x: x[1], reverse=True))


       return


    def explain_match(self , rule , object_list) :
       t1 = time.clock()
       con_sum = 0.00
       # print(final)
       sign_list = [0]*(len(object_list)+1)
       cover_count = 0
       # sign_list = np.full((len(object_list)), 0)


       count = 0
       for i in range(len(self.use_list)):
          if self.unuse_list[i] != 0:
              # print("***")
              continue
          else :
              for j in range(len(object_list)) :
                 if sign_list[j] == 1 :
                   continue
                 else:
                      # print(str(rule[count]) + " " + str(object_list[j][i]))
                      if str(rule[count]) != str(object_list[j][i]) and rule[count] != '*':
                          sign_list[j] = 1
                          continue
                      else :
                          if i == self.final and sign_list[j] == 0:
                              if self.agg_function == "sum" :
                                  con_sum += float(object_list[j][self.attr_num])
                                  # print(rule)
                                  # print(object_list[j][self.attr_num])
                              elif self.agg_function == "avg"  :
                                  con_sum += abs(self.prov_sum/self.prov_count - (self.prov_sum - float(object_list[j][self.attr_num]))/(self.prov_count-1))
                              else:
                                  con_sum += 1
                              cover_count +=1
              count += 1


       t2 = time.clock()
       # print(self.sumtime)
       self.sumtime+=t2-t1
       # if consum[0][0] == None :
       #     return 0.00
       # else :
       #     return consum[0][0]
       self.match_count+=1
       # print(" ".join('%s' %id for id in rule))
       self.coverage_dict[" ".join('%s' %id for id in rule)] = cover_count
       self.hash_contri[" ".join('%s' %id for id in rule)] = con_sum

       return con_sum

    # delete
    def delete_abrule(self , rule_list):

          item = 0
          while item < len(self.prov_list) :
            count = 0
            for i in range(len(self.unuse_list)) :
                  if self.unuse_list[i] == 0 :
                     # print(str(rule_list[count]) + "|"+str(self.prov_list[item][i]))
                     if rule_list[count] != '*' and str(self.prov_list[item][i]) != str(rule_list[count]) :
                        # print(str(rule_list[count]) + "|"+str(self.prov_list[item][i])+"删除")
                        break
                     count += 1

                  if i == len(self.unuse_list)-1 :
                      # print(self.prov_list[item])
                      del self.prov_list[item]
                      item -=1

            item += 1

    def update_hash_contri(self, rule):
        sign_dict=[]
        for i in range(len(rule)) :
            if rule[i] == '*':
                continue
            else:
                for j in self.hash_contri.keys() :

                    rule_list = str(j).split(" ")
                    if j not in sign_dict :
                        if rule_list[i] !='*' and rule[i] != rule_list[i]:
                            sign_dict.append(j)


        for j in self.hash_contri.keys():
             if j not in sign_dict:
                self.hash_contri[j] = -1


    def unuse_List_getter(self):
        return self.unuse_list