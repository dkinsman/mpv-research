import sys
import matplotlib.pyplot as plt
import numpy as np
import math

infinity = float('inf')

def fromDionysusText(filename):
    # read text files that are generated by D Morozov's Dionysus code.
    input = open(filename)

    res = []
    for line in input.readlines():
        if line.strip().startswith('#'):
            continue
        
        dim, birth, death = line.strip().split()
        
        dim = int(dim)
        birth = float(birth)
        death = float(death)
        # need the sqrt here because the Dionysus alpha shape code gives squared distances
        res.append((math.sqrt(birth), math.sqrt(death), dim))

    input.close()
    return tuple(res)


#def fromTextFile(filename):
#    fp = open(filename)
#    result = fromDionysusText(fp)
#    fp.close()
#    return result

def rescalePairs(pairs,a):
    # rescale the birth and death values by a factor a
    res = [ (b*a, d*a, dim) for b, d, dim in pairs ]
    return tuple(res)


def save_data(data,filename):
    import pickle
    fp = open(filename,"w")
    pickle.dump(data,fp)
    fp.close()


def load_data(filename):
    import pickle
    fp = open(filename,"r")
    data = pickle.load(fp)
    fp.close()
    return data



def homologyRank(pairs,dim,bvals,dvals,threshold=0.0):
    # pairs is a tuple holding (birth, death, dimension) information for persistence (obtained by reading in from a file).
    # dim is the dimension you want to work with
    # bvals, dvals are lists of real numbers to evaluate the rank function on.
    # threshold is the minimum persistence for pairs in the diagram.
    
    # The homology rank function at (b,d) counts the number of cycles of dimension dim that satisfy  (birth <= b) and ( death > d )
    
    # This python function returns the "cumulative histogram discretization" of the homology rank function.

    countKeys = [(bv,dv) for bv in bvals for dv in dvals if dv >= bv ]
    count = { ck: 0 for ck in countKeys }
    for birth, death, d in pairs:
        if d == dim and death-birth > threshold:
            for (bv,dv) in countKeys:
                if (bv >= birth and dv < death):
                    count[(bv,dv)] += 1
    return count

def rescaleRank(rankFunc,a):
    return {key: a*rankFunc[key] for key in rankFunc}


def linCombRank(rankFuncList,scalarList):
    # compute a linear combination of some number of rank functions
    # these rank functions must all be evaluated at the same (b,d) points.
    return {key: sum(rankFuncList[i][key]*scalarList[i] for i in range(len(scalarList))) for key in rankFuncList[0]}


def meanRank(rankFuncList):
    # compute the pointwise mean value of the rank functions
    length_list = len(rankFuncList)
    sumRank = {key: sum(rankFuncList[i][key] for i in range(length_list)) for key in rankFuncList[0]}
    return {key: (1.0/length_list)*sumRank[key] for key in sumRank}

    #scalars = [ 1.0/length_list for i in range(length_list)]
    #return linCombRank(rankFuncList,scalars)

def centeredRanks(rankFuncList):
    meanRankFunc=meanRank(rankFuncList)
    return [linCombRank([r,meanRankFunc],[1,-1]) for r in rankFuncList]

def centeredRanksFaster(rankFuncList,meanRankFunc):
    return [linCombRank([r,meanRankFunc],[1,-1]) for r in rankFuncList]

def varRank(centeredRankList):
    # compute pointwise variance of (centered) rank fuctions
    return {key: (1.0/len(centeredRankList))*sum(c[key]**2 for c in centeredRankList) for key in centeredRankList[0]}


def generateWeights(keys, box_length=1.0, A=1):
    # calculate weights for use in computing the dot product between two rank functions
    # keys contains the (birth, death) pairs at which the rank functions are evaluated.
    # this weight function assumes the birth and death values are equally spaced.
    #
    # multiply the weights by the "box area" to get a dot-product that approximates an integral.
    box_area=box_length*box_length  
    weights={(b,d): box_area*math.exp(A*(b-d)) for (b,d) in keys }
    
    birth_keys=[b for (b,d) in keys]
    max_death = max([d for (b,d) in keys])
    
    weights.update({(b,max_death): box_area*math.exp(b-max_death)/(1-math.exp(-box_length)) for b in birth_keys})
    # This formula is from the sum of weights of all the boxes that would lie above and including (b, max_death)
    # We are assuming here that the value of the rank function is constant in this line of boxes.
    # The formula uses the geometric series
    #   sum(box_area*exp(b-max_death-kl))= box_area*exp(b-max_death)*sum(exp(-l)^k)
    # over k from 0 to infty. 
    return weights


def dotProduct(rankf,rankg,weightFunction):
    # the rankf, rankg are two rank function dictionaries that must have the same keys
    # weights is a dictionary with the same keys also.
    
    return sum( rankf[key]*rankg[key]*weightFunction[key] for key in rankf )



def create_dot_product_matrix(set_rank_functions, weightFunction):
    #We want to create the dot product matrix for the set of centered rank functions {f1, f2, ... fN}
    #Theoretically this matrix is XX^T where X is the data matrix with each row a different rank
    #function and each column the (b,d) locations
    # XX^T is an inner product with weights.
    N = len(set_rank_functions)
    a = np.zeros((N,N))
    for i in range(N):
        a[i,i] = dotProduct(set_rank_functions[i], set_rank_functions[i], weightFunction)
        for j in range(i):
            a[i,j]=dotProduct(set_rank_functions[i], set_rank_functions[j], weightFunction)
            a[j,i] = a[i,j]
    return a


def faster_create_dot_product(set_rank_functions, weightFunction):
    # VR attempt to speed up dot product computation
    #
    N = len(set_rank_functions)
    keys = set_rank_functions[0].keys()
    weighted_rank_functions = []
    for i in range(N):
        weighted_rank_functions.append({k: set_rank_functions[i][k]*weightFunction[k] for k in keys })

    a = np.zeros((N,N))
    for i in range(N):
        a[i,i] = sum( set_rank_functions[i][k]*weighted_rank_functions[i][k] for k in keys )
        for j in range(i):
            a[i,j] = sum( set_rank_functions[i][k]*weighted_rank_functions[j][k] for k in keys )
            a[j,i] = a[i,j]
    return a



def find_princ_comp(dot_product_matrix, centered_rank_functions, number_pc):
    # PCA uses the non-zero eigenvalues and eigenvectors of (X^T X).
    # Here X is the matrix where each row is a sample function. 
    # We know XX^T which is input as dot_product_matrix here - given each pair of functions we know their dot product.
    # Eigenvectors and eigenvalues of the two are related as follows. Suppose l is an eigenvalue of XX^T with eigenvector w. Then l is also an eigenvalue of X^TX with eigenvector X^Tw.

    #print dot_product_matrix
    
    eig_values, eig_vectors=np.linalg.eigh(dot_product_matrix)
    ascend_sort_index = np.argsort(eig_values)
    descend_sort_index = ascend_sort_index[::-1]
    eig_values_sorted = eig_values[descend_sort_index]
    
    #print eig_values_sorted
    eig_vectors_sorted = eig_vectors[:,descend_sort_index]
    # print eig_vectors_sorted
    set_princ_comp=[] 
    #print eig_values_sorted
   
    # shorthand eig_vectors_sorted[i,k]=Vec[i,k], center_rank_functions[i]=f_i 
    #(v_k=)unscaled_pc_comp[k]=sum_i Vec[i,k] f[i] 
    # so |v_k|^2 = sum_{i,j} Vec[i,k]Vec[j,k] f_i dot f_j = sum_{i,j} Vec[i,k]Vec[j,k] dot_prod_matrix[i,j]
    number_functions=len(centered_rank_functions)
    for k in range(number_pc):
        # print eig_vectors_sorted[:,k].T
        length_squared=0
        for j in range(number_functions):
            length_squared+=sum(eig_vectors_sorted[i,k]*eig_vectors_sorted[j,k]*dot_product_matrix[i,j] for i in range(number_functions))
        # print "length squared is "
        # print length_squared
        v=linCombRank(centered_rank_functions,eig_vectors_sorted[:,k].T)
        set_princ_comp.append(rescaleRank(v, 1.0/math.sqrt(length_squared)))
    # for i in range(num_pc):
#             v=linCombRank(centered_rank_functions,eig_vectors_sorted[:,i].T)
#
# length=(sum(eig_vectors_sorted[i,j]* eig_vectors_sorted[i,j])
    
    return (eig_values_sorted, set_princ_comp)

def variationExplained(eig_values_sorted):
    total = sum(eig_values_sorted)
    return [ (1.0/total) * sum(eig_values_sorted[0:i+1]) for i in range(len(eig_values_sorted)) ]


def pcScoreArray(centeredRankList,princCompList,weightFunction):
    # compute weighted dot products of rank functions with principal component eigenvectors.
    # D is the number of dimensions we're projecting onto.
    
    N = len(centeredRankList)
    D = len(princCompList)
    a = np.zeros((N,D))  # each row is a rank function, can be transposed later if necessary.
    for i in range(N):
        for j in range(D):
            a[i,j] = dotProduct(centeredRankList[i], princCompList[j], weightFunction)
    return a

def find_pca_eigenvalues(dot_product_matrix):
    # find only the eigenvalues of the PCA matrix.

    eig_values = np.linalg.eigvalsh(dot_product_matrix)
    ascend_sort_index = np.argsort(eig_values)
    descend_sort_index = ascend_sort_index[::-1]
    eig_values_sorted = eig_values[descend_sort_index]

    return eig_values_sorted


def euler(pairs,bvals,dvals,threshold=0.0):
    # This python function returns the "persistent euler characteristic"
    # defined as euler(b,d) = homologyRank_0(b,d) - homologyRank_1(b,d) + homologyRank_2(b,d)
    
    # pairs is a tuple holding (birth, death, dimension) information for persistence (obtained by reading in from a file).
    # bvals, dvals are lists of real numbers to evaluate the euler function on.
    # threshold is the minimum persistence for pairs in the diagram.
    
    # The euler function at (b,d) counts the alternating sum of cycles by dimension with (birth <= b) and ( death > d )
    
    countKeys = [(bv,dv) for bv in bvals for dv in dvals if dv >= bv ]
    count = { ck: 0 for ck in countKeys }
    for birth, death, dim in pairs:
        for (bv,dv) in countKeys:
            if (bv >= birth and dv < death):
                count[(bv,dv)] += math.pow(-1,dim)
    return count




def plot_rank(bvals,dvals,rankFunc,cont=0,**kwargs):
    # bvals, dvals are the birth and death values used in the keys for the rankFunc
    # rankFunc is a dictionary of {(b,d) : number } form
    
    x_bin_length = bvals[1] - bvals[0]
    x_offset = x_bin_length/2.0
    y_bin_length = dvals[1] - dvals[0]
    y_offset = y_bin_length/2.0
    
    x = np.arange(bvals[0]-x_offset,bvals[-1]+x_bin_length,x_bin_length)
    y = np.arange(dvals[0]-y_offset,dvals[-1]+y_bin_length,y_bin_length)
    
    c = np.zeros((len(bvals),len(dvals)))
    for i in range(len(bvals)):
        for j in range(len(dvals)):
            if dvals[j] >= bvals[i]:
                c[i,j] = rankFunc[(bvals[i],dvals[j])]

    fig = plt.figure()
    ax  = plt.subplot(111)
    pc = ax.pcolormesh(x,y,c.T,**kwargs)
    ax.set_xlim(x[0],x[-1])
    ax.set_ylim(y[0],y[-1])
    plt.colorbar(pc)
    if cont:
        cs = ax.contour(bvals,dvals,c.T,cont,colors='grey',alpha=0.7,linewidth=0.5)
    plt.draw()
    return pc


def new_plot_rank(rankFunc,**kwargs):
    # rankFunc is a dictionary of {(birth,death) : number } form
    
    births = set([b for (b,d) in rankFunc.keys()])
    deaths = set([d for (b,d) in rankFunc.keys()])
    
    bvals = list(births)
    dvals = list(deaths)
    bvals.sort()
    dvals.sort()
    
    x_bin_length = bvals[1] - bvals[0]
    x_offset = x_bin_length/2.0
    y_bin_length = dvals[1] - dvals[0]
    y_offset = y_bin_length/2.0
    
    x = np.arange(bvals[0]-x_offset,bvals[-1]+x_bin_length,x_bin_length)
    y = np.arange(dvals[0]-y_offset,dvals[-1]+y_bin_length,y_bin_length)
    
    c = np.zeros((len(bvals),len(dvals)))
    for i in range(len(bvals)):
        for j in range(len(dvals)):
            if dvals[j] >= bvals[i]:
                c[i,j] = rankFunc[(bvals[i],dvals[j])]
    
    fig = plt.figure()
    ax  = plt.subplot(111)
    pc = ax.pcolormesh(x,y,c.T,**kwargs)
    ax.set_xlim(x[0],x[-1])
    ax.set_ylim(y[0],y[-1])
    plt.colorbar(pc)
    plt.draw()
    return pc



if __name__ == '__main__':

# SEE homology_rank_bead.py for more recent code to process bead packing data

# set up for the bead_pack data

    threshold = 0.0
    dim = 1
   
    bvals = np.arange(0,1,0.001)
    # if dim == 1:
    #     bvals = np.arange(0.0,1,0.001)
    # elif dim ==0:
    #     bvals = np.arange(0.0,0.1,0.0001)
    # if dim == 2:
  #       bvals = np.arange(0.055,0.085,0.0001)
  #   elif dim ==1:
  #       bvals = np.arange(0.045,0.080,0.0001)
    dvals = bvals
    rankFuncs = []
    box_length=bvals[1]-bvals[0]

    # for ss in range(2013, 2022):
    infile = './raw/mi_persistence.txt'
    pairs = fromDionysusText(infile)
    rankFuncs.append(homologyRank(pairs,dim,bvals,dvals,threshold))
    print(rankFuncs)
    print ("Processed data")

    # for ss in range(23):
    #     infile = file_prefix+cryst_subsets[ss]+cryst_file_suffix
    #     pairs = fromDionysusText(infile)
    #     rankFuncs.append(homologyRank(pairs,dim,bvals,dvals,threshold))

    # print ("Processed partial cryst bead packs")

    # save_data(rankFuncs,'rankFunctionList_1D.pkl')

    mnRankFunc = meanRank(rankFuncs)
    pcmn = plot_rank(bvals,dvals,mnRankFunc)
    #plt.show()
    plt.savefig("mean_rank_function_1D_test.png")
    #plt.close()

    centeredList = centeredRanks(rankFuncs)
    print(len(centeredList))
    weightFunc = generateWeights(rankFuncs[0].keys(), box_length)
    
    print ("weightFunction generated")
    dot_prod_matrix = create_dot_product_matrix(centeredList, weightFunc)
    
    print ("dot product matrix generated")
    print(dot_prod_matrix)

    (all_eig_vals, some_princ_comps) = find_princ_comp(dot_prod_matrix, centeredList, 4)

    print (variationExplained(all_eig_vals))

    print (pcScoreArray(centeredList,some_princ_comps,weightFunc))

    pcpc = plot_rank(bvals,dvals,some_princ_comps[0])
    #plt.show()
    plt.savefig("first_principal_comp_1D_test.png")
    #plt.close()



