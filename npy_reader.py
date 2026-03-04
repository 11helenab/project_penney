import numpy as np

data= np.load('data/rawdeck_0.npy')

count = 0

for i in data: 
    print(i)
    print(count)
    count += 1