import pandas as pd
import gudhi as gd
import matplotlib.pyplot as plt

def alpha_pd(lat_long, state):
    stree = gd.AlphaComplex(points=lat_long).create_simplex_tree()
    dgm = stree.persistence(persistence_dim_max=True)
    plt.figure()
    gd.plot_persistence_diagram(dgm, legend=True)
    plt.title('Persistance diagram ' + state + ' (alpha)')
    plt.savefig('../output/pd_whole/' + state + 'alpha_pd.jpeg', bbox_inches='tight')

def main():
    df = pd.read_csv('../raw/mpv-data.csv')
    print(df.shape)
    df = df[['latitude', 'longitude', 'state']]
    state = df.state.unique().tolist()

    # mi = df[df['state']=='MI']
    # mi.drop(columns = 'state', inplace = True)
    # alpha_pd(mi.values.tolist(), 'MI')
    for s in state:
        print(s)
        st = df[df['state'] == s]
        sta = st.drop(columns='state')
        print(sta.shape)
        lat_long = sta.values.tolist()
        #rips_pd(lat_long, s)
        alpha_pd(lat_long, s)

if __name__=='__main__':
    main()