import os
from utils.stats import *
from utils.plotting_and_string_clean import *
from utils.get_graph import *
from glouton_igraph import *
from kmedoids import *
from voronoi import *
from optimisation_lineaire import *
import pulp

folder_name = DATA_DIR = Path(__file__).resolve().parent / "data"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)


city = "Strasbourg"
file_name = clean_file_name(city)
crs = "EPSG:2154"
generate = True #choisis si on calcule tout le matrice de distance ou si on utilise celle déjà calculée
dist = 400 #distance acceptable à marcher
marge = 200 #marge acceptable sur la distance habituelle (pour la méthode gloutonnes)
facteur = 1.25 #facteur de surestimation de la distance pour les méthodes spatiales
spatial_dist = dist/facteur
nb_iteration_kmedoids = 500
nb_iteration_voronoi = 500
solver = pulp.CPLEX_CMD(path=r'C:\Program Files\IBM\ILOG\CPLEX_Studio2211\cplex\bin\x64_win64\cplex.exe')

def main(methode = "glouton",regenerate = True):
    if regenerate:
        data = get_data(city,crs)
        save_data(treat_graph(data[0],crs),data[1],file_name,generate=generate)
    match methode:
        case "glouton":
            g_plot,h,polygon,mat=load_data(file_name, plot = True,igraph=True,polygone=True,matrix=True)
            seed_xy = polylabel(polygon)
            seed_x = seed_xy.x
            seed_y = seed_xy.y
            seed = ox.nearest_nodes(nx.MultiDiGraph(g_plot),seed_x,seed_y)
            t2 = t.process_time()
            resultat = approx(h,seed,dist,marge)
            print("durée de calcul processeur:",(t.process_time()-t2))
            clusters= cluster(h,resultat,mat)
            moy,maxs = moyenne(clusters,mat,resultat)
            print("nombre de noeuds :",g_plot.number_of_nodes())
            print("nombre d'arètes :",g_plot.number_of_edges())
            print("moy =", moy)
            print("ecart-type =", ecart_type(moy,maxs))
            print("dans l'intervalle:",correct_dist(resultat,mat,clusters,0,400))
            print("nombre de stations :",len(clusters))
        case "kmedoids":
            g_plot,h,polygon,mat = load_data("paris",plot=True,igraph=True,polygone=True,matrix=True)
            t2 = t.process_time()
            m,nb_station,res = dichotomie(mat,0, estimation(polygon,dist/facteur)*4, dist,nb_iteration_kmedoids,estimation(polygon,dist/facteur))
            print("durée processeur",t.process_time()-t2)
            medoids=res.medoids
            label =res.labels
            clusters =[[i for i in range(len(label)) if label[i]==j] for j in range(len(medoids))]
            print("nombre de noeuds :",g_plot.number_of_nodes())
            print("nombre d'arètes :",g_plot.number_of_edges())
            moy,maxs = moyenne(clusters,mat,medoids)
            print("moyenne :",moy)
            print("ecart-type :",ecart_type(moy,maxs))
            print("distance correcte:",correct_dist(medoids,mat,clusters,0,dist+100))
            print("nombre de station :",len(medoids))
        case "voronoi":
            polygon = load_data(file_name,polygone=True)[0]
            t2 = t.process_time()
            distance_max,nb_station,voronoi_list,voronoi_center = dichotomie(polygon,0,estimation(polygon,dist)*4,dist,nb_iteration_voronoi,estimation(polygon,dist)*4,facteur)
            print("durée de calcul processeur:",(t.process_time()-t2))
            voronoi_int = [voronoi_list[j] for j in range(len(voronoi_list)) if not spl.dwithin(spl.LinearRing(polygon.exterior.coords),voronoi_list[j],dist/100)]

            voronoi_center = [i.centroid for i in voronoi_list]
            moy,maxs = moy_poly(voronoi_int)
            print("distance moyenne",moy*facteur)
            print("ecart-type",ecart_type_poly(moy,maxs))
            print("à bonne distance =",correct_dist_poly(voronoi_list,polygon,dist))
            print("Il y a",nb_station,"station, distantes d'au plus",distance_max)
        case "exact":
            g_plot,h,polygon,mat = load_data(file_name,plot=True,igraph=True,polygone=True,matrix=True)
            problem,x,y = def_problem(mat,dist)
            t2 = t.process_time()
            problem.solve(solver = solver)

            print("durée processeur:",t.process_time()-t2)
            print("nombre de noeuds :",g_plot.number_of_nodes())
            print("nombre d'arètes :",g_plot.number_of_edges())
            print("Status:", pulp.LpStatus[problem.status])
            print("Number of stations placed:", pulp.value(problem.objective))
            stations = [i for i in range(len(x)) if x[i].varValue > 0.5]
            clusters = cluster(h,stations,mat)
            moy,maxs = moyenne(clusters,mat,stations)
            print("moyenne :",moy)
            print("ecart-type :",ecart_type(moy,maxs))
            print("distance correcte:",correct_dist(stations,mat,clusters,0,dist))


main("kmedoids",regenerate=False)