from persistence import *

def main():
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
        rips = rips_pd(lat_long, s)
        #alpha_pd(lat_long, s)
        rips_landscapes(lat_long, s, rips)


if __name__=='__main__':
    main()