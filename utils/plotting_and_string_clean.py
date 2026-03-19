import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np

import matplotlib as mpl
import osmnx as ox
from matplotlib.colors import hsv_to_rgb, to_hex, to_rgba
import colour as c
import re
import unicodedata


def clean_file_name(recherche_maps: str, longueur_max: int = 20) -> str:
    """
    Transforme une chaîne de recherche en un nom de fichier valide et propre.
    """
    chaine_sans_accents = unicodedata.normalize('NFKD', recherche_maps)\
                                     .encode('ASCII', 'ignore')\
                                     .decode('utf-8')
    chaine_sans_espaces = chaine_sans_accents.replace(' ', '_')
    nom_propre = re.sub(r'[^\w\-]', '', chaine_sans_espaces)
    nom_final = nom_propre[:longueur_max]
    return nom_final.strip('_')

def plotting(g,pts=[[[],[]]],color =["red","violet"],renvoie=False,interactive = False,titre = None):
    if interactive :
        status = plt.ion()
    else :
        status = plt.ioff()
    with status:
        fig, ax = plt.subplots(figsize=(8,8), facecolor="#111111", frameon=False)
        gdf_edges = ox.graph_to_gdfs(g, nodes=False)["geometry"]
        ax = gdf_edges.plot(ax=ax, color="orange", lw=1, alpha=None, zorder=1)
        gdf_nodes = ox.graph_to_gdfs(g, edges=False, node_geometry=False)[["x", "y"]]
        ax.scatter(
                x=gdf_nodes["x"],
                y=gdf_nodes["y"],
                s=15,
                color="orange",
                alpha=None,
                edgecolor=None,
                zorder=1,
            )
        for i in range(len(pts)):
            ax.scatter(
                    x=pts[i][1],
                    y=pts[i][0],
                    s=15,
                    color=color[i],
                    alpha=None,
                    edgecolor=None,
                    zorder=1,
                )
        if renvoie :
            return ax
        else : 
            plt.title(titre,y=-0.05)
            plt.xticks([])
            plt.yticks([])


def generate_random_color(n,node_color=None):
    min_v=0.7
    max_v=0.8
    min_s = 0.8
    max_s = 1
    if node_color == None: 
        return [to_hex(hsv_to_rgb(np.concatenate([np.random.rand(1),np.random.uniform(min_s,max_s,size=1), np.random.uniform(min_v, max_v, size=1)]))) for i in range(n)]
    return [to_hex(hsv_to_rgb(np.concatenate([np.random.rand(2), np.random.uniform(min_v, max_v, size=1)]))) for i in range(n)]+[to_hex(node_color)]

def generate_linear_color(n,name = None, color1=None,color2=None,node_color = None):
    if name == None:
        color1 = c.Color(color1)
        color2 = c.Color(color2)
        if node_color ==None:
            return list(color1.range_to(color2, n))
        return list(color1.range_to(color2, n))+[node_color]
    cmap = mpl.colormaps[name]
    if node_color==None:
        return list(cmap(np.linspace(0, 1, n)))
    return list(cmap(np.linspace(0, 1, n)))+[np.array(to_rgba(node_color))]
