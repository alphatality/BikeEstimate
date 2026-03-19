import osmnx as ox
import networkx as nx
from pathlib import Path
import igraph as ig
from shapely import to_geojson,from_geojson
import numpy as np
import time as t
import os


def get_data(place,crs="EPSG:2154"):
    print("getting data ...")
    graph = ox.graph_from_place(place, network_type="walk", simplify=False, retain_all=False, truncate_by_edge=False, which_result=None, buffer_dist=None)
    poly = ox.project_gdf(ox.geocode_to_gdf(place),to_crs=crs).unary_union
    data = (graph,poly)
    print("got data")
    return data

def save_data(g,poly,name,generate=True,folder_name = os.getcwd()+r"\data"):
    print("saving data...")
    filepath = Path(os.path.join(folder_name, r"polygon_"+name+r".geojson"))
    print("treating data")
    h = to_simple_graph(g)
    g_plot=nx.MultiGraph(g)
    print("data treated")
    filepath.write_text(to_geojson(poly))
    print("nombre de noeuds :",g_plot.number_of_nodes())
    print("nombre d'arètes :",g_plot.number_of_edges())
    ox.save_graphml(g_plot,os.path.join(folder_name, r"graph_"+name +r"_geom.graphml"))
    nx.write_graphml(h,os.path.join(folder_name, r"graph_"+name+r"_simple.graphml"))
    if generate:
        print("calculating distance...")
        h = ig.Graph.Load(os.path.join(folder_name, r"graph_"+name+r"_simple.graphml"),format='graphml')
        t1 = t.process_time()
        mat = h.distances(weights="length")
        print("durée de calcul :",t.process_time()-t1)
        np.save(os.path.join(folder_name, r"matrice_"+name+r".npy"),mat)
        print("distance calculated")
    print("data saved")

def treat_graph(g,crs="EPSG:2154"):
    h = ox.project_graph(g,to_crs=crs)
    h = ox.consolidate_intersections(h, tolerance=10, rebuild_graph=True, dead_ends=False, reconnect_edges=True)
    h = ox.simplify_graph(h)
    h = ox.get_digraph(h,weight="length")
    return h.to_undirected()


def to_simple_graph(g):
    h = nx.Graph()
    dico = {int(i):int(i) for i in g.nodes()}
    nx.set_node_attributes(g,dico,"commun_id")
    for i in g.nodes():
        h.add_node(int(i), x= g.nodes[i]['x'],y=g.nodes[i]['y'],commun_id = g.nodes[i]["commun_id"])
    
    att = nx.get_edge_attributes(g,"length")
    for i in g.edges():
        h.add_edge(i[0],i[1],length = att[i])
    return h

def load_data(name,plot = False, igraph = False,polygone = False, matrix=False,folder_name = os.getcwd()+r"\data"):
    if polygone:
        filepath = Path(os.path.join(folder_name, r"polygon_"+name+r".geojson"))
        poly = from_geojson(filepath.read_text())
    else :
        poly = None
    if (igraph):
        h = ig.Graph.Load(os.path.join(folder_name, r"graph_"+name+r"_simple.graphml"),format='graphml')
    else :
        h = None
    if plot:
        g = ox.load_graphml(os.path.join(folder_name, r"graph_"+name +r"_geom.graphml"))
    else:
        g = None
    if matrix:
        mat =np.load(os.path.join(folder_name, r"matrice_"+name+r".npy"))
    else :
        mat = None
    res = (g,h,poly,mat)
    temp =[i for i in res if i is not None]
    return temp
