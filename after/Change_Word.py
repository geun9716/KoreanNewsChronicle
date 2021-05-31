import pandas as pd

f = open("C:/Users/ghdtk/Project_test/이형동의어.txt", encoding = 'utf-8')
words = []
for line in f:
    line = line.strip()
    words.append(line.split(", "))

df = pd.read_csv("C:/Users/ghdtk/Project_test/Data/2019_pre.csv", encoding = 'utf-8')

N_list = df['N_list']
after_tokens = []
for N in N_list:
    n_list = N.split(", ")
    tokens = []
    for n in n_list:
        n = n.strip("[]'")
        tokens.append(n)
        
    after_token = []
    for token in tokens:
        sw = 0
        for word in words:
            if token in word:
                after_token.append(word[0])
                sw = 1
                break
        
        if(sw == 0):
            after_token.append(token)
    after_tokens.append(after_token)
df['modified_N_list'] = pd.Series(after_tokens)
df.to_csv("2019_after.csv", encoding="utf-8")
