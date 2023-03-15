#ca_example.py

from persistence import *
import numpy as np
import datetime as dt
import os

def main():

    os.chdir('./scripts')
    print(os.getcwd())

    al0, al1= [],[]
    df = pd.read_csv('../raw/mpv-data.csv')
    print(df.shape)
    state = df.state.unique().tolist()
    ca = df[df['state']=='CA']
    ca['date'] = pd.to_datetime(ca['date']).dt.year
    ca = ca[['date', 'latitude', 'longitude']]
    print(ca.shape)
    yrs_tot = ca['date'].unique().tolist()
    print(yrs_tot)
    
    for idx, yr in enumerate(yrs_tot):
        sub = ca[ca['date']==yr]
        sub.drop(columns='date', inplace = True)
        coords = sub.values.tolist()

        # generate persistence diagrams (pd)
        atree = alpha_pd(coords, 'ca')
        #rtree = rips_pd(coords, 'ca')

        # from the pds, generate persistence landscapes
        alandscapes = pers_landscapes('ca', atree, 'alpha')
        al0.append(alandscapes[0])
        al1.append(alandscapes[1])
        # print(l0[0:5])

        plot_landscapes_year(al0[idx], 0, 'alpha', 'CA', '../output/pl/', yr)
        plot_landscapes_year(al1[idx], 1, 'alpha', 'CA', '../output/pl/', yr)

    alpha_avg0 = np.mean(np.array(al0), axis = 0)
    alpha_avg1 = np.mean(np.array(al1), axis = 0)
    
    plot_landscapes(alpha_avg0, 0, 'alpha', 'CA', '../output/avg_pl/')
    plot_landscapes(alpha_avg1, 1, 'alpha', 'CA', '../output/avg_pl/')

    # rtree = rips_pd(coords, 'ca')
    # land = pers_landscapes('ca', rtree, 'rips')

if __name__=='__main__':
    main()
    