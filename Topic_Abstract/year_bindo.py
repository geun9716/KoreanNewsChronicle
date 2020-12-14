import csv
import pandas as pd
import sys
from collections import Counter

df = pd.read_csv("2019.csv", encoding="utf-8")
topics = []

hot_topic_index = Counter(df['cnt']).most_common()
hot_topic = dict(hot_topic_index)

print(hot_topic)
print(len(hot_topic))