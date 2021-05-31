"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import datetime
from math import asin, cos, radians, sin, sqrt

from DISClib.ADT import graph as gr
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.DataStructures import mapentry as me

import config as cf

assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""
# ==================
# API del TAD libros
# ==================

def newCatalog():
    """
    """
    catalog = { 
                'map_landing_points': None,
                'map_countries': None,
                'map_connections': None,
                'graph_landing_points': None
              }

    catalog['map_landing_points'] = mp.newMap(numelements=3500,
                            maptype='PROBING',
                            loadfactor=0.4)
    catalog['map_countries'] = mp.newMap(numelements=650,
                            maptype='PROBING',
                            loadfactor=0.4)
    catalog['map_connections'] = mp.newMap(numelements=9000,
                            maptype='PROBING',
                            loadfactor=0.4)
    catalog['graph_landing_points'] = gr.newGraph(datastructure='ADJ_LIST',
                                                  directed=False,
                                                  size=19500)

    return catalog

# ==============================================
# Funciones para agregar informacion al catalogo
# ==============================================

def addMapLanding_points(catalog, element):
    """
    """
    idEsta = mp.contains(catalog['map_landing_points'], element['landing_point_id'])
    if not idEsta and (mp.size(catalog['map_landing_points']) == 0):
        mp.put(catalog['map_landing_points'], element['landing_point_id'], element)
        print("El primer landing_point cargado es: " + str(element['id']))
        print("El nombre es: " + str(element['name']))
        print("La altituld es: " + str(element['latitude']))
        print("La longutid es: " + str(element['longitude']))
    elif not idEsta:
        mp.put(catalog['map_landing_points'], element['landing_point_id'], element)
    
def addMapCountries(catalog, element):
    """
    """
    idEsta = mp.contains(catalog['map_countries'],element['CountryName'])
    if not idEsta:
        mp.put(catalog['map_countries'],element['CountryName'], element)

def addMapConnections(catalog, element):
    """
    """
    idEsta = mp.contains(catalog['map_connections'], element['\ufefforigin'])
    if not idEsta:
        landing_point_map = mp.newMap(numelements=80,
                                        maptype='PROBING',
                                        loadfactor=0.4)
        mp.put(landing_point_map, str(element['\ufefforigin']) + '-' + str(element['destination']), element)                                
        mp.put(catalog['map_connections'], element['\ufefforigin'], landing_point_map)
    else:
        connection_entry = mp.get(catalog['map_connections'], element['\ufefforigin'])
        landing_point_map = me.getValue(connection_entry)
        connectionEsta = mp.contains(landing_point_map, str(element['\ufefforigin']) + '-' + str(element['destination']))
        if not connectionEsta:
            mp.put(landing_point_map, str(element['\ufefforigin']) + '-' + str(element['destination']), element)
            mp.put(catalog['map_connections'], element['\ufefforigin'], landing_point_map)

def addLanding_point_graph(catalog, element):
    """
    """
    name_vertex_origen = formatVertex_origin(element)
    name_vertex_destinantion = formatVertex_destination(element)
    if not gr.containsVertex(catalog['graph_landing_points'], name_vertex):
        gr.insertVertex(catalog['graph_landing_points'], name_vertex)


# ================
# Funciones Helper
# ================

def cleanServiceDistance(lastservice, service):
    """
    En caso de que el archivo tenga un espacio en la
    distancia, se reemplaza con cero.
    """
    if service['Distance'] == '':
        service['Distance'] = 0
    if lastservice['Distance'] == '':
        lastservice['Distance'] = 0

def formatVertex_origin(landing_point):
    """
    Se formatea el nombrer del vertice con el id de la estación
    seguido de la ruta.
    """
    name = landing_point['origin'] + '-'
    name = name + landing_point['cable_id']
    return name

def formatVertex_destination(landing_point):
    """
    """
    name = landing_point['destination'] + '-'
    name = name + landing_point['cable_id']
    return name

def haversine(lat1, lon1, lat2, lon2):
    """
    """
    r = 6372.8
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
    c = 2*asin(sqrt(a))
      
    distance = r * c

    return distance

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
