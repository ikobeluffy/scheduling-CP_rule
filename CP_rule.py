# -*-coding:utf-8-*-
import numpy as np
import pandas as pd

#机器数量
print '请输入机器数量：'
M=int(raw_input())
#执行时间
pro_time={}
df=pd.read_csv('pro_time.csv')
for i in range(0,len(df)):
    pro_time[str(i+1)]=df.loc[i].p
# pro_time = {'1':8,'2':10,'3':10,'4':12,'5':11,'6':15,'7':12,'8':12,'9':10,'10':19,'11':10,'12':10}
#约束条件—用一个字典表示
cons={}
df=pd.read_csv('file_cons.csv')
for i in range(0, len(df)):
    cons[str(df.loc[i].pri)] = df.loc[i].next.split()

# cons = {'1':['2'],'2':['3'],'4':['3','6'],'5':['3','6'],'3':['7'],'6':['8'],
#         '7':['10','11'],'8':['10','11','12'],'9':['10','11','12']}

#计算起始点和最终点
number_p=len(pro_time)
all_point=list([str(x) for x in range(1,number_p+1)])
l=cons.keys()
g=[]
start_point=[]
end_point=[]
for i in l:
    g=g+cons[i]
g=list(set(g))
for i in l:
    if i not in g:
        start_point.append(i)
for i in g:
    if i not in l:
        end_point.append(i)

# print start_point
# print end_point


#开始时间，结束时间初始化
start_time={}
end_time={}
for i in all_point:
    start_time[i]=0
    end_time[i]=0
for i in all_point:
    end_time[i]=start_time[i]+pro_time[i]

def update_time():
    for i in cons:
        for j in cons[i]:
            if end_time[i]>start_time[j]:
                start_time[j]=end_time[i]
                end_time[j]=start_time[j]+pro_time[j]
    return 0

def find_all_paths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if not graph.has_key(start):
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = find_all_paths(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths

#计算每条路的权重
def weight(path,pro_time):
    if len(path)!=0:
        tot=0
        for i in path:
            tot=tot+pro_time[i]
    else:
        return None
    return tot

#计算每个点的权重
def max_weight(point,end_point):
    max_w=[]
    for i in end_point:
        for k in find_all_paths(cons, point,i, path=[]):
            max_w.append(weight(k,pro_time))
    return max(max_w)

L_weight={}
for i in all_point:
    L_weight[i]=max_weight(i,end_point)

S=pd.Series(L_weight)
Sorted_p=S.sort_values(ascending=False)

list_byweight=Sorted_p.index
print '每个作业流的总权重'

print Sorted_p
#机器初始化
Machine=[]
for i in range(M):
    dirc={}
    dirc['num']=i+1
    dirc['work']=[]
    dirc['span_time']=0
    Machine.append(dirc)
Machine_df=pd.DataFrame(Machine)

def put_into(work):
    l=list(Machine_df['span_time'])
    k=l.index(min(l))
    Machine_df['work'][k].append(work)
    a=Machine_df.loc[k,'span_time']
    Machine_df.loc[k,'span_time']=a+pro_time[work]
    return a

#将一项作业插入到机器中
def put_into2(work):
    l=list(Machine_df['span_time'])
    k=l.index(min(l))
    a=Machine_df.loc[k,'span_time']
    if start_time[work]>a:
        a=start_time[work]
        Machine_df['work'][k].append('0')
    Machine_df['work'][k].append(work)
    Machine_df.loc[k,'span_time']=a+pro_time[work]
    end_time[work]=Machine_df.loc[k,'span_time']
    update_time()
    return 0

for i in list_byweight:
    put_into2(i)


print '排程结果（0代表机器空闲）：'
print Machine_df
print '   '
print '总完工时间为：'
print max(list(Machine_df['span_time']))
print '   '
print '每项作业开始时间：'
for i in all_point:
    print i,':',start_time[i]

print '   '
print '每项作业的完成时间：'
for i in all_point:
    print i,':',end_time[i]