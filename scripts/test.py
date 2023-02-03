import os
from ripser import ripser
from persim.landscapes import (
    PersLandscapeApprox,
    average_approx,
    snap_pl,
    plot_landscape,
    plot_landscape_simple
)
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt

if __name__ == '__main__':
    print(os.getcwd())
    os.chdir('scripts')
    print(os.getcwd())

    rl0, rl1= [],[]
    df = pd.read_csv('../raw/mpv-data.csv')
    print(df.shape)
    state = df.state.unique().tolist()
    mi = df[df['state']=='MI']
    mi['date'] = pd.to_datetime(mi['date']).dt.year
    mi = mi[['date', 'latitude', 'longitude']]
    print(mi.shape)
    yrs_tot = mi['date'].unique().tolist()
    print(yrs_tot)
    
    for idx, yr in enumerate(yrs_tot):
        sub = mi[mi['date']==yr]
        sub.drop(columns='date', inplace = True)
        #coords = sub.values.tolist()

        # generate persistence diagrams (pd)
        rtree = ripser(sub, maxdim = 2)['dgms']
        print(rtree)

        rl0.append(PersLandscapeApprox(dgms = rtree, hom_deg = 0))
        #print(rl0)
        rl1.append(PersLandscapeApprox(dgms = rtree, hom_deg = 1)) 
    
    avg0 = average_approx(rl0)
    #avg1 = average_approx(rl1)
    #[snap_avg0, snap_avg1] = snap_pl([avg0, avg1])

    plt.figure()
    plot_landscape_simple(avg0, title = 'Rips Avg. PL degree 0')
    #plot_landscape_simple(avg1, title='Rips Avg. PL degree 1')
    plt.savefig('../output/avg_pl/avgplMI0.png')