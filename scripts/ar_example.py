from persistence import *
import numpy as np
import datetime as dt
import os
import warnings
#warnings.filterwarnings("ignore")

def main():

    os.chdir('./scripts')
    print(os.getcwd())

    al0, al1, rl0, rl1 = [],[], [], []
    df = pd.read_csv('../raw/mpv-data.csv')
    print(df.shape)
    state = df.state.unique().tolist()
    ar = df[df['state']=='AR']
    ar['date'] = pd.to_datetime(ar['date']).dt.year
    ar = ar[['date', 'latitude', 'longitude']]
    print(ar.shape)
    yrs_tot = ar['date'].unique().tolist()
    print(yrs_tot)
    
    for idx, yr in enumerate(yrs_tot):
        sub = ar[ar['date']==yr]
        sub.drop(columns='date', inplace = True)
        coords = sub.values.tolist()

        # generate persistence diagrams (pd)
        atree = alpha_pd_yr(coords, 'AR', yr)
        rtree = rips_pd_yr(coords, 'AR', yr)

        # from the pds, generate persistence landscapes
        alandscapes = pers_landscapes('AR', atree, 'alpha')
        rlandscapes = pers_landscapes('AR', rtree, 'rips')
        rl0.append(rlandscapes[0])
        rl1.append(rlandscapes[1])
        al0.append(alandscapes[0])
        al1.append(alandscapes[1])
        # print(l0[0:5])

        plot_landscapes_year(al0[idx], 0, 'alpha', 'AR', '../output/pl/', yr)
        plot_landscapes_year(al1[idx], 1, 'alpha', 'AR', '../output/pl/', yr)

    alpha_avg0 = np.mean(np.array(al0), axis = 0)
    alpha_avg1 = np.mean(np.array(al1), axis = 0)
    rips_avg0 = np.mean(np.array(rl0), axis = 0)
    rips_avg1 = np.mean(np.array(rl1), axis = 0)
    
    plot_landscapes(alpha_avg0, 0, 'alpha', 'AR', '../output/avg_pl/')
    plot_landscapes(alpha_avg1, 1, 'alpha', 'AR', '../output/avg_pl/')
    plot_landscapes(rips_avg0, 0, 'rips', 'AR', '../output/avg_pl/')
    plot_landscapes(rips_avg1, 1, 'rips', 'AR', '../output/avg_pl/')

    # rtree = rips_pd(coords, 'AR')
    # land = pers_landscapes('AR', rtree, 'rips')

if __name__=='__main__':
    main()