import csv
import pandas as pd
import sys
from collections import Counter

df = pd.read_csv("./Data/201901.csv", encoding="utf-8")
topics = []

df.dropna()

for topic in df['topics']:
    if type(topic) == str:
        topics.extend(topic.split(','))

hot_topic_index = Counter(topics).most_common(20)
hot_topic = dict(hot_topic_index)

print(hot_topic)