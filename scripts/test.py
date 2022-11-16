# code adapted from: 

# need these for the data
import numpy as np
from sklearn import datasets
import pandas as pd

# need these for plotting
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection

# need this for persistence
import dionysus

df = pd.read_csv('raw/mpv-data.csv')
df = df[['longitude', 'latitude','state']]
df = df[df.state == 'MI']
df.drop(columns = 'state', inplace= True)
coords = np.array(df.values.tolist())

#X, l = datasets.make_circles(n_samples=(0,20), noise=0.1, random_state=1)
rips_complex = dionysus.fill_rips(coords, 2, 0.25)

edges = []
triangles = []

for i in range(0, len(rips_complex)):
    # look for points, don't need these
    if len(dionysus._dionysus.Filtration.__getitem__(rips_complex,i)) == 1:
        pass
    # look for 1-simplices, append to edges
    if len(dionysus._dionysus.Filtration.__getitem__(rips_complex,i)) == 2:
        edges.append([dionysus._dionysus.Filtration.__getitem__(rips_complex,i)[0],dionysus._dionysus.Filtration.__getitem__(rips_complex,i)[1]])
    # look for 2-simplices, append to triangles
    if len(dionysus._dionysus.Filtration.__getitem__(rips_complex,i)) == 3:
        triangles.append([dionysus._dionysus.Filtration.__getitem__(rips_complex,i)[0],dionysus._dionysus.Filtration.__getitem__(rips_complex,i)[1],dionysus._dionysus.Filtration.__getitem__(rips_complex,i)[2]])    

fig4 = plt.figure(figsize=(10,10))

ax = fig4.add_subplot()

# plot edges
for i in range(len(edges)):
    ax.plot(np.transpose(coords[edges[i],:])[0], np.transpose(coords[edges[i],:])[1], color = 'black')
 
# plot triangles
for i in range(len(triangles)):
    vtx = coords[triangles[i],:]
    tri = PolyCollection([vtx])
    ax.add_collection(tri)
plt.savefig('output/mi_rips_vis.png', bbox_inches = 'tight')