import pandas as pd

lists = []
for i in range(1, 7):
    path = "2019{0:02d}.csv".format(i)
    lists.append(pd.read_csv(path, encoding="utf-8-sig"))

df = pd.concat(lists)
df.to_csv("./2019/2019.csv", index=False)