from persistence import *
import os

def main():
    os.chdir('./scripts')
    print(os.getcwd())

    df = pd.read_csv('../raw/mpv-data.csv')
    print(df.shape)
    df = df[['latitude', 'longitude', 'state']]
    df.dropna(subset = ['longitude'], axis = 0, how = 'all', inplace = True)
    df.dropna(subset = ['latitude'], axis = 0, how = 'all', inplace = True)
    state = df.state.unique().tolist()
    #state = ['CA', 'TX'] 

    for s in state:
        print(s)
        st = df[df['state'] == s]
        sta = st.drop(columns='state')
        print(sta.shape)
        lat_long = sta.values.tolist()
        alpha = alpha_pd(lat_long, s)
        L=pers_landscapes(s, alpha, 'alpha')
        plot_landscapes(L[0], 0, 'alpha', s, '../output/pl_whole/')
        plot_landscapes(L[1], 1, 'alpha', s, '../output/pl_whole/')

        if (len(lat_long) <= 200):
            rips = rips_pd(lat_long, s)
            L=pers_landscapes(s, rips, 'rips')
            plot_landscapes(L[0], 0, 'rips', s, '../output/pl_whole/')
            plot_landscapes(L[1], 1, 'rips', s, '../output/pl_whole/')
        


if __name__=='__main__':
    main()