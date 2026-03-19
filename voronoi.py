from shapely.ops import polylabel
import shapely as spl
from shapely import Point,Polygon
import matplotlib.pyplot as plt
import numpy as np





def Random_Points_in_Polygon(polygon, number):
    points = []
    minx, miny, maxx, maxy = polygon.bounds
    while len(points) < number:
        pnt = np.random.uniform(minx, maxx), np.random.uniform(miny, maxy)
        if polygon.contains(Point(pnt)):
            points.append(pnt)
    return spl.MultiPoint(points) #selection aléatoire de points

def furthest_distance(poly,p):
    return max([spl.distance(p,i) for i in [Point(coord) for coord in poly.exterior.coords]])
    #le critère de la dichotomie est la moyenne de portées des clusters

def estimation(polygon,dist):
    return int(spl.area(polygon)/(np.pi*dist*dist))

def traitement(pts,polygon,end=False):
    voronoi = spl.voronoi_polygons(pts)
    voronoi_list,voronoi_special,voronoi_temp,fail,ref =[],[],[],[],list(voronoi.geoms)
    for i in ref: #on prend les polygones simples (intersection = unique polygone)
        if polygon.contains(i):
            voronoi_list.append(i)
        else:
            temp = spl.intersection(polygon,i)
            if not temp.is_empty:
                if end:
                    plt.plot(*i.exterior.xy,color="green")
                voronoi_special.append(temp)
    for i in voronoi_special: #on récupère le plus gros polygone de chaque multipolygone 
        if type(i)==spl.MultiPolygon: 
            _,big = max([(spl.area(k),k) for k in i.geoms])
            voronoi_temp.append(big)
            for k in i.geoms:
                if k != big:
                    other = [(voronoi_list[l],l) for l in range(len(voronoi_list)) if k.touches(voronoi_list[l])]
                    if len(other)==0:
                        fail.append(k)
                        continue  
                    for l in range(len(other)):
                        union = spl.unary_union((k,other[l][0]))
                        if type(union)==Polygon:
                            voronoi_list[other[l][1]] = union
                            break
        else: 
            voronoi_temp.append(i)
    voronoi_list+=voronoi_temp
    m=0
    while fail and m<10: #On fusionne les polygones restants
        m+=1
        remaining = []
        for i in fail:
            removed = False
            for j in range(len(voronoi_list)):
                if i.touches(voronoi_list[j]):
                    union = spl.unary_union((voronoi_list[j], i))
                    if type(union) == Polygon:
                        voronoi_list[j] = union
                        removed = True
                        break
            if not removed:
                remaining.append(i)
        fail = remaining
    return voronoi_list


def dichotomie(polygon,debut,fin,objectif,n,nmax,limit,facteur=1.25):
    nb_actuel =int((fin+debut)/2)
    if limit<=0:
        raise ValueError("Recursion infinie")
    points = Random_Points_in_Polygon(polygon,nb_actuel)
    
    for i in range(n):
        voronoi = traitement(points,polygon)   
        coos=[i.centroid if spl.contains (i,i.centroid) else polylabel(i) for i in voronoi]
        points = spl.MultiPoint(coos)
    fd = [furthest_distance(voronoi[j],coos[j]) for j in range(len(voronoi)) if not spl.dwithin(spl.LinearRing(polygon.exterior.coords),voronoi[j],objectif/100)]#on prend une marge pour les erreurs flottants
    if not fd:
        fd = [furthest_distance(voronoi[j], coos[j]) for j in range(len(voronoi))]
    m = sum(fd)/len(fd) #on estime avec les polygons intérieur, ceux de l'exterieur étants déformés
    print("nb_actuel =",nb_actuel,"debut=",debut,"fin=",fin,"m=",m*facteur)
    if debut == nmax or abs(fin-nmax)==1:
        return dichotomie(polygon,nb_actuel,2*nmax,objectif,n,limit-1,2*nmax)
    if (fin==debut) or abs(fin-debut)==1:
        return (m,nb_actuel,voronoi,points)
    if m>objectif:
        return dichotomie(polygon,nb_actuel,fin,objectif,n,limit-1,nmax)
    elif m< objectif:
        return dichotomie(polygon,debut,nb_actuel,objectif,n,limit-1,nmax)
    else :
        return (m,nb_actuel,voronoi,points)
    



