import numpy as np
import pandas as pd
import datetime as dt
import dionysus as d
import matplotlib.pyplot as plt
import os
import math

# generate rips complex using dionysus

if __name__ == '__main__':
    #os.chdir(os.path.join(os.getcwd(), 'scripts'))
    # preprocessing
    print(os.getcwd())
    df = pd.read_csv('./raw/mpv-data.csv')
    ca = df[df.state=='CA'][['latitude', 'longitude']]
    # mi['date'] = pd.to_datetime(mi['date']).dt.year
    # yrs_tot = mi['date'].unique().tolist()
    # print(yrs_tot)
    dims = [0,1]

    coords = ca.to_numpy()
    print(type(coords))

    # generate rips complex
    filtration = d.fill_rips(coords, 2, 1)
    pd = d.homology_persistence(filtration)
    dgms = d.init_diagrams(pd, filtration)

    # save dimension, birth, and death in .txt file
    for dim in dims:
        f = open('./raw/CA/ca_persistence_dim'+ str(dim)+ '.txt', 'w')
        for i, dgm in enumerate(dgms):
            if i == dim:
                for pt in dgm:
                    f.write(str(i)+'\t'+ str(pt.birth) + '\t' +str(pt.death) + '\n')
        f.close()
    print('rips generation complete')




