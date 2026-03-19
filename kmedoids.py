import kmedoids as km
import numpy as np
import shapely as spl

def furthest_distance(mat,medoids,classes):
    return sum([max([(mat[medoids[j]][i]) for i in range(len(classes)) if classes[i]==j]) for j in range (len(medoids))])/len(medoids) #critère de dichotomie = moyenne des portées des clusters


def dichotomie(mat,debut,fin,objectif,n,nmax,limit):

    nb_actuel =int((fin+debut)/2)
    if limit<=0:
        raise ValueError("Recursion infinie")
    res = km.fasterpam(mat,nb_actuel, max_iter=n, init='random', random_state=None, n_cpu=-1)
    m= furthest_distance(mat,res.medoids,res.labels)
    if debut == nmax or abs(fin-nmax)==1:
        return dichotomie(mat,nb_actuel,2*nmax,objectif,n,2*nmax,limit-1)
    if (fin==debut) or abs(fin-debut)==1:
        return (m,nb_actuel,res)
    if m>objectif:
        return dichotomie(mat,nb_actuel,fin,objectif,n,nmax,limit-1)
    elif m< objectif:
        return dichotomie(mat,debut,nb_actuel,objectif,n,nmax,limit)
    else :
        return (m,nb_actuel,res)

def estimation(polygon,dist):
    return int(spl.area(polygon)/(np.pi*dist*dist))


