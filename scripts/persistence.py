import pandas as pd
import gudhi as gd
import matplotlib.pyplot as plt
import gudhi.representations
import numpy as np

def alpha_pd(lat_long, state):
    stree = gd.AlphaComplex(points=lat_long).create_simplex_tree()
    dgm = stree.persistence(persistence_dim_max=True)
    plt.figure()
    gd.plot_persistence_diagram(dgm, legend=True)
    plt.title('Persistance diagram ' + state + ' (alpha)')
    plt.savefig('../output/pd_whole/' + state + 'alpha_pd.jpeg', bbox_inches='tight')
    plt.close()
    return stree

def rips_pd(lat_long, state):
    path = '../output/pd_whole/' + state + 'rips_pd.jpeg'
    stree = gd.RipsComplex(points=lat_long).create_simplex_tree(max_dimension = 2)
    dgm = stree.persistence()
    plt.figure()
    gd.plot_persistence_diagram(dgm, legend=True)
    plt.title('Persistance diagram ' + state + ' (rips)')
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    return stree

def alpha_pd_yr(lat_long, state, yr):
    path = '../output/pd/' + state + '/'+str(yr) +'alpha_pd.jpeg'
    stree = gd.AlphaComplex(points=lat_long).create_simplex_tree()
    dgm = stree.persistence(persistence_dim_max=True)
    plt.figure()
    gd.plot_persistence_diagram(dgm, legend=True)
    plt.title('Persistance diagram ' + state + ' '+str(yr) +' (alpha)')
    plt.savefig(path, bbox_inches='tight')
    print(path)
    plt.close()
    return stree

def rips_pd_yr(lat_long, state, yr):
    path = '../output/pd/' + state + '/'+str(yr) + 'rips_pd.jpeg'
    stree = gd.RipsComplex(points=lat_long).create_simplex_tree(max_dimension = 2)
    dgm = stree.persistence()
    plt.figure()
    gd.plot_persistence_diagram(dgm, legend=True)
    plt.title('Persistance diagram ' + state +' '+str(yr) + ' (rips)')
    plt.savefig(path, bbox_inches='tight')
    #print(path)
    plt.close()
    return stree

def pers_landscapes(state, complex, sc):
    landscapes = []
    DS = gd.representations.DiagramSelector(use=True, limit=np.inf, point_type='finite')
    dim0int_without_infinity = DS.fit_transform([complex.persistence_intervals_in_dimension(0)] )
    #print(dim0int_without_infinity)

    #next, we look at 1-dimensional persistence intervals, however, 
    # all 1-d intervals (blue) persist to infinity and will be removed to create the persistence landscapes
    #dgms=[complex.persistence_intervals_in_dimension(1)]
    #print(dgms2)
    dim1int_without_infinity = DS.fit_transform([complex.persistence_intervals_in_dimension(1)])
    #print(dim1int_without_infinity)
    
    L=gd.representations.Landscape(num_landscapes=10, resolution=100).fit_transform(dim0int_without_infinity)
    landscapes.append(L)

    L=gd.representations.Landscape(num_landscapes=10, resolution=100).fit_transform(dim1int_without_infinity)
    landscapes.append(L)
    return landscapes

def plot_landscapes(L, dim, sc, state, path):
    land = plt.figure()
    plt.plot(L[0][:100], label = "Landscape 1" )
    plt.plot(L[0][100:200], label = "Landscape 2")
    plt.plot(L[0][200:300], label = "Landscape 3")
    plt.plot(L[0][300:400], label = "Landscape 4")
    plt.plot(L[0][400:500], label = "Landscape 5")
    plt.plot(L[0][500:600], label = "Landscape 6")
    plt.plot(L[0][600:700], label = "Landscape 7")
    plt.plot(L[0][700:800], label = "Landscape 8")
    plt.plot(L[0][800:900], label = "Landscape 9")
    plt.plot(L[0][900:1000], label = "Landscape 10")
    plt.legend()
    if dim == 0:
        plt.title('Average Landscapes ' + state+ ' (dimension 0, '+sc+ ')')
        land.savefig(path+ state + sc +'dim0' + '_pl.jpeg', bbox_inches = 'tight')
    else:
        plt.title('Average Landscapes ' + state+ ' (dimension 1, '+sc+ ')')
        land.savefig(path+ state + sc +'dim1' + '_pl.jpeg', bbox_inches = 'tight')
    plt.close()

def plot_landscapes_year(L, dim, sc, state, path, year):
    land = plt.figure()
    plt.plot(L[0][:100], label = "Landscape 1" )
    plt.plot(L[0][100:200], label = "Landscape 2")
    plt.plot(L[0][200:300], label = "Landscape 3")
    plt.plot(L[0][300:400], label = "Landscape 4")
    plt.plot(L[0][400:500], label = "Landscape 5")
    plt.plot(L[0][500:600], label = "Landscape 6")
    plt.plot(L[0][600:700], label = "Landscape 7")
    plt.plot(L[0][700:800], label = "Landscape 8")
    plt.plot(L[0][800:900], label = "Landscape 9")
    plt.plot(L[0][900:1000], label = "Landscape 10")
    plt.legend()
    if dim == 0:
        filepath = path+ '/' + state + '/'+ sc +str(year)+'dim0' + '_pl.jpeg'
        plt.title('Landscapes ' + state+ ' ' +str(year)+ ' (dimension 0, '+sc+ ')')
        land.savefig(filepath, bbox_inches = 'tight')
    else:
        filepath = path+ '/' + state + '/'+ sc +str(year)+'dim1' + '_pl.jpeg'
        plt.title('Landscapes ' + state+ ' '+str(year)+' (dimension 1, '+sc+ ')')
        land.savefig(filepath, bbox_inches = 'tight')
    plt.close()