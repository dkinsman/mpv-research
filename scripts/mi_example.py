from persistence import *
import numpy as np
import pickle

def main():
    df = pd.read_csv('raw/mpv-data.csv')
    print(df.shape)
    df = df[['latitude', 'longitude', 'state']]
    state = df.state.unique().tolist()

    mi = df[df['state']=='MI']
    mi.drop(columns = 'state', inplace = True)
    coords = mi.values.tolist()
    atree = alpha_pd(coords, 'MI')
    rtree = rips_pd(coords, 'MI')
    rjson = pickle.dumps(rtree)
    print(rjson)
    land = pers_landscapes(coords, 'MI', rtree)

if __name__=='__main__':
    main()