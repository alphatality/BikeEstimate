import shapely as spl


def moyenne(cluster,mat,pts):
    maxs = [max([(mat[pts[i]][j]) for j in cluster[i]]) for i in range(len(cluster))]
    return sum(maxs)/len(maxs),maxs #moyenne des maximums(portée des clusters)

def correct_dist(pts,mat,cluster,dist_min,dist_max):
    dedans = sum([sum([1 for j in cluster[i] if (mat[pts[i]][j])>=dist_min and (mat[pts[i]][j])<=dist_max]) for i in range(len(cluster))])
    return dedans/len(mat) #Proportion de la zone desservie


def ecart_type(moy,maxs):
    return (sum([(maxs[i]-moy)**2 for i in range(len(maxs))])/len(maxs))**(1/2)#écart moyen à la moyenne : homogénéinité des clusters

def moy_poly(polys):
    maxs = [max([spl.distance(spl.Point(j),polys[i].centroid) for j in polys[i].exterior.coords]) for i in range(len(polys))]
    return sum(maxs)/len(maxs),maxs #moyenne des maximums(portée des clusters)

def ecart_type_poly(moy,maxs) :
    return sum([(maxs[i]-moy)**2 for i in range(len(maxs))])/len(maxs) 
    #Proportion de la zone desservie

    
def correct_dist_poly(polys,poly_ref,dist):
    ref = poly_ref.area
    surface = sum([spl.intersection(i,spl.buffer(i.centroid,dist,quad_segs=10)).area for i in polys])
    return surface/ref
    #écart moyen à la moyenne : homogénéinité des clusters

def cluster (g,pts,distance):
    classes =[min([(distance[i][pts[j]],j) for j in range(len(pts))]) for i in range(len(distance))]
    res =[[] for i in range(len(pts))]
    for i in range(len(classes)):
        _,j=classes[i]
        res[j].append(g.vs[i].index)
    return res
    #extrait les clusters