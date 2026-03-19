import os
from collections import deque
import heapq

def recherche_noeud_plus_proche(g,seed,dist,recherche,visited,tolerance=0):
    q=[]
    visite = set()
    heapq.heappush(q,(0.,seed)) #on initialise
    while q:
        d,noeud_courant = heapq.heappop(q)
        visite.add(noeud_courant)
        y = g.incident(noeud_courant)
        for voisin in y: #djikstra borné à d mètres
            if g.es[voisin].target == noeud_courant:
                x = g.es[voisin].source
            else: 
                x = g.es[voisin].target
            if (d+g.es[voisin]['length']) <= dist:
                if x not in visite:
                    heapq.heappush(q,((d+g.es[voisin]["length"],x)))
                    visite.add(x)
                    visited.add(x)
                    if x in recherche:
                        recherche.remove(x) # On supprime les noeuds trop proches
            elif (d+g.es[voisin]['length']) >= dist+tolerance:
                continue
            else:
                if x not in visite:
                    visite.add(x)
                    heapq.heappush(q,((d+g.es[voisin]["length"],x)))
                    if x in recherche :
                        return x #dès qu'on en trouve un on le renvoie
    return -1


def chercher_noeuds_proches(g, seed, distance_max,visited=None,resultats= None,plot =None):
    if visited is None:
        visited = set()
    if resultats is None:
        resultats = set()
    q=[]
    visite =set()
    heapq.heappush(q,(0.,seed))
    #on part du point initial
    while q:

        d,noeud_courant = heapq.heappop(q)
        #on prend un noeud et sa distance à la seed
        visite.add(noeud_courant)
        visited.add(noeud_courant)
        #on le marque comme visité
        y = g.incident(noeud_courant)
        #on prend les noeuds incidents
        for voisin in y: #djikstra borné sur chaque sommet
            if g.es[voisin].target == noeud_courant:
                x = g.es[voisin].source
            else: 
                x = g.es[voisin].target
            if (d+g.es[voisin]['length']) <= distance_max:
                if x not in visite:
                    if x in resultats :
                        resultats.discard(x)
                        #discard evite erreur si plus dedans 
                    heapq.heappush(q,((d+g.es[voisin]["length"],x)))
            else:
                if x not in visite and x not in visited:
                    resultats.add(x)                  
    return resultats,visite





def indice(g,seed):
    return g.vs.select(commun_id_eq =seed)[0].index





def approx (g,seed,dist,tolerance=0.):
    final = [] #initialisation des noeuds à chercher
    seed_id = indice(g,seed)
    temp,visite = chercher_noeuds_proches(g,seed_id,dist) #temp = noeud à bonne distance, visite= noeud visité lors de la recherche
    init = deque(temp) #on les traite dans l'ordre  
    a_visite = set() #set des noeuds à visiter à la prochaine itération
    j=0
    while init:
        i = init.popleft() #on prends le premier élément
        #on vérifie qu'il ne soit pas trop proche d'un noeud déja pris et que ce ne soit pas non plus le premier, qui est déjà dedans
        #print(i)
        x = recherche_noeud_plus_proche(g,i,dist,init,visite,tolerance) 
        # on cherche un noeud à la bonne distance dans ceux que l'on est entrain de traité. A défaut on a -1 et on traite le prochain de la file 
        if not i in final:
            final.append(i)
        #on ajoute le noeud traité dans résultat
        chercher_noeuds_proches(g,i,dist,visite,a_visite)
        #on ajoute les visités lors de la recherches des noeuds suivants
        #on ajoute les noeuds suivants
        if x ==-1 :
            #si x =-1 alors on a pas trouvé de point donc soit c'est vide soit c'est trop loin
            if init:
                #si init est pas vide on a juste pas trouvé de noeud, donc on continue
                continue
            else:
                #sinon on réinitialise init avec les noeuds suivants
                init = deque(a_visite)
                a_visite.clear()
                #on vide a_visite
                j+=1
                continue
        init.remove(x)
        init.appendleft(x)
    return final







