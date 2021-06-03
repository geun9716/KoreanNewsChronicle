import pandas as pd

lists = []
for i in range(1, 7):
    path = "../Topic_Abstract/2021_new/2019{0:02d}_LDA_topic3.csv".format(i)
    lists.append(pd.read_csv(path, encoding="utf-8-sig"))

df = pd.concat(lists)
df.to_csv("./2019/2019_LDA.csv", index=False)