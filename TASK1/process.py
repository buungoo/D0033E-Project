
import numpy as np
import pandas as pd
 
import collections

dict1 = collections.defaultdict(list)

# using loadtxt()
train = np.loadtxt("test-final.csv", delimiter=",", dtype=str)
#test = np.loadtxt("test-sorted.csv", delimiter=",", dtype=str)


for item in train:
    data = item
    #data[-2] = item[-2][1:-1]
    dict1[item[-2]].append(data)
#print(dict1)

for i in dict1:
    df = pd.DataFrame(dict1[i])
    df.to_csv(f'out{i}.csv', index=None, header=None)

    
