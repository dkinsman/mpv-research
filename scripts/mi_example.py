from persistence import *
import numpy as np

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
    land = pers_landscapes(coords, 'MI', rtree)
    lands= np.array([land[0], land[1]])
    land_avg = np.mean(lands, axis = 0)
    landscape = plt.figure()
    plt.plot(land_avg[0][:100], label = "Landscape 1" )
    plt.plot(land_avg[0][100:200], label = "Landscape 2")
    plt.plot(land_avg[0][200:300], label = "Landscape 3")
    plt.plot(land_avg[0][300:400], label = "Landscape 4")
    plt.plot(land_avg[0][400:500], label = "Landscape 5")
    plt.plot(land_avg[0][500:600], label = "Landscape 6")
    plt.plot(land_avg[0][600:700], label = "Landscape 7")
    plt.plot(land_avg[0][700:800], label = "Landscape 8")
    plt.plot(land_avg[0][800:900], label = "Landscape 9")
    plt.plot(land_avg[0][900:1000], label = "Landscape 10")
    plt.legend()
    plt.title(state + 'Landscapes (dimension 1, rips)')
    landscape.savefig('output/avg_land.jpeg', bbox_inches = 'tight')
    plt.close()

if __name__=='__main__':
    main()