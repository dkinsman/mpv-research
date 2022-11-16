from persistence import *

def main():
    l0,l1 = [], []
    df = pd.read_csv('raw/mpv-data.csv')
    print(df.shape)
    df = df[['latitude', 'longitude', 'state']]
    df.dropna(subset = ['longitude'], axis = 0, how = 'all', inplace = True)
    df.dropna(subset = ['latitude'], axis = 0, how = 'all', inplace = True)
    state = df.state.unique().tolist()

    for s in state:
        print(s)
        st = df[df['state'] == s]
        sta = st.drop(columns='state')
        print(sta.shape)
        lat_long = sta.values.tolist()
        #rips = rips_pd(lat_long, s)
        alpha = alpha_pd(lat_long, s)
        L=pers_landscapes(s, alpha, 'alpha')
        l0.append(L[0])
        l1.append(L[1])

    avg0 = np.mean(np.array(l0), axis = 0)
    avg1 = np.mean(np.array(l1), axis = 0)
    
    plot_landscapes(avg0, 0, 'alpha')
    plot_landscapes(avg1, 1, 'alpha')
        


if __name__=='__main__':
    main()