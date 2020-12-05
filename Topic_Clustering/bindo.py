import pandas as pd
from collections import Counter

#필요없는 것을 먼저 제거후 돌리기

filename = "201901_clustered_500.csv"
file = pd.read_csv(filename,encoding='unicode_escape')

index=file['cluster_number']
print(type(index))

def frequency_sort(data):
	rt_data = []
	for d, c in Counter(data).most_common():
		for i in range(c):
			rt_data.append(d)
	return rt_data

list_sorted=frequency_sort(index);  

#중복 제거
def OrderedSet(list):
    my_set = set()
    res = []
    for e in list:
        if e not in my_set:
            res.append(e)
            my_set.add(e)

    return res

my_list = list(OrderedSet(list_sorted))

for i in range(0,9):
    print(my_list[i]) 
