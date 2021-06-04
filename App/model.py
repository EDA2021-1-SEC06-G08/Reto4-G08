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
from DISClib.DataStructures import linkedlistiterator as it
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms import Graphs 
from DISClib.ADT import stack as st 
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
        print("La latitude es: " + str(element['latitude']))
        print("La longitude es: " + str(element['longitude']))
    elif not idEsta:
        mp.put(catalog['map_landing_points'], element['landing_point_id'], element)
    
def addMapCountries(catalog, element):
    """
    """
    idEsta = mp.contains(catalog['map_countries'], element['CountryName'])
    if not idEsta:
        mp.put(catalog['map_countries'], element['CountryName'], element)

def addMapConnections(catalog, element):
    """
    """
    idEsta = mp.contains(catalog['map_connections'], element['ï»¿origin'])
    if not idEsta:
        landing_point_map = mp.newMap(numelements=80,
                                        maptype='PROBING',
                                        loadfactor=0.4)
        elementos = lt.newList('ARRAY_LIST')
        lt.addLast(elementos, element)
        mp.put(landing_point_map, element['destination'], elementos)                                
        mp.put(catalog['map_connections'], element['ï»¿origin'], landing_point_map)
    else:
        connection_entry = mp.get(catalog['map_connections'], element['ï»¿origin'])
        landing_point_map = me.getValue(connection_entry)
        connectionEsta = mp.contains(landing_point_map, element['destination'])
        if not connectionEsta:
            landing_point_map = mp.newMap(numelements=80,
                                        maptype='PROBING',
                                        loadfactor=0.4)
            elementos = lt.newList('ARRAY_LIST')
            lt.addLast(elementos, element)
            mp.put(landing_point_map, element['destination'], elementos)                                
            mp.put(catalog['map_connections'], element['ï»¿origin'], landing_point_map)
        else:
            mapEntry = mp.get(landing_point_map, element['destination'])
            lista = me.getValue(mapEntry)
            lt.addLast(lista, element)
            mp.put(landing_point_map, element['destination'], lista)
            mp.put(catalog['map_connections'], element['ï»¿origin'], landing_point_map)

def AddVertexGrap(catalog):
    """
    """
    landing_point_list = mp.valueSet(catalog['map_landing_points'])
    iterator = it.newIterator(landing_point_list)
    while it.hasNext(iterator):
        landing_point = it.next(iterator)
        ciudades = landing_point['name'].split(",")
        i = 0
        """mapEntry = mp.get(catalog['map_countries'], ciudades[-1])
        countri = me.getValue(mapEntry)
        city = countri['CapitalName']
        name = city[1:]
        name = landing_point['landing_point_id'] + "-" + name
        if not gr.containsVertex(catalog['graph_landing_points'], name):
            gr.insertVertex(catalog['graph_landing_points'], name)"""
        while i < (len(ciudades)-1):
            name = landing_point['landing_point_id']
            city = ciudades[i]
            city = city[0:]
            name = name + "-" + str(city)
            if not gr.containsVertex(catalog['graph_landing_points'], name):
                gr.insertVertex(catalog['graph_landing_points'], name)
            i += 1

def AddEdgesGrap(catalog):
    """
    """
    landings_points_values_map = mp.valueSet(catalog['map_connections'])
    iterator = it.newIterator(landings_points_values_map)
    while it.hasNext(iterator):
        tabla_hash = it.next(iterator)
        connections = mp.valueSet(tabla_hash)
        iterador = it.newIterator(connections)
        while it.hasNext(iterador):
            landing_point_list = it.next(iterador)
            iterabor = it.newIterator(landing_point_list)
            while it.hasNext(iterabor):
                landing_point = it.next(iterabor)
                origin = landing_point['origin']
                destination = landing_point['destination']
                if mp.contains(catalog['map_landing_points'], origin) and mp.contains(catalog['map_landing_points'], destination):
                    landing_point_origin_Entry = mp.get(catalog['map_landing_points'], origin)
                    landing_point_info_origin = me.getValue(landing_point_origin_Entry)
                    latitude_origin = landing_point_info_origin['latitude']
                    longitude_origin = landing_point_info_origin['longitude']
                    landing_point_info_destination_Entry = mp.get(catalog['map_landing_points'], destination)
                    landing_point_info_destination = me.getValue(landing_point_info_destination_Entry)
                    latitude_destination = landing_point_info_destination['latitude']
                    longitude_destination = landing_point_info_destination['longitude']
                    distance_km = haversine(float(latitude_origin), float(longitude_origin), float(latitude_destination), float(longitude_destination))
                    vertexA = lt.newList('ARRAY_LIST')
                    vertexB = lt.newList('ARRAY_LIST')
                    list_vertex = gr.vertices(catalog['graph_landing_points'])
                    iteracor = it.newIterator(list_vertex)
                    while it.hasNext(iteracor):
                        vertex = it.next(iteracor)
                        vertex_separado = vertex.split("-")
                        for number in vertex_separado:
                            if origin == number:
                                lt.addLast(vertexA, vertex)
                            elif destination == number:
                                lt.addLast(vertexB, vertex)
                    vertex_Aiterator = it.newIterator(vertexA)
                    while it.hasNext(vertex_Aiterator):
                        vertexA_connector = it.next(vertex_Aiterator)
                        vertex_Biterator = it.newIterator(vertexB)
                        while it.hasNext(vertex_Biterator):
                            vertexB_connector = it.next(vertex_Biterator)
                            gr.addEdge(catalog['graph_landing_points'], vertexA_connector, vertexB_connector, distance_km)






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

#req 3 
"""def max_interconexión(catalog):
    graph = catalog['graph_landing_points']"""
    


# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

def req2(catalog):
    lista_vertices = gr.vertices(catalog['graph_landing_points'])
    tamaño =lt.size(lista_vertices)
    respuesta = lt.newList()
    grados = lt.newList()
    #sacamos el grado para cada uno de los vertices 
    iterador = it.newIterator(lista_vertices)
    while it.hasNext(iterador):
        vertice = it.next(iterador)
        grado = gr.degree(catalog['graph_landing_points'], vertice)
        if grado != 0:
           lt.addLast(respuesta, ((vertice['name'], vertice['id']), grado))
    return respuesta 

def req3(catalog, pais_a, pais_b):
    lista_ruta = lt.newList()
    grafo = catalog['graph_landing_points']
    MST = Graphs.dijsktra.Dijkstra(grafo, pais_a)
    distancia_total = Graphs.dijsktra.distTo(MST, pais_b)
    camino_pila = Graphs.dijsktra.pathTo(MST, pais_b)
    sacar_el_primero = st.pop(camino_pila)
    iterador = it.newIterator(camino_pila)
    while it.hasNext(iterador):
        ruta = st.pop(camino_pila)
        lt.addLast(lista_ruta, ruta)
    return (lista_ruta, distancia_total)
    

def req4(catalog):
    grafo = catalog['graph_landing_points']
    vertices_grafo = gr.vertices(grafo)
    vertice1 = lt.getElement(vertices, 0)
    MST = Graphs.dijsktra.Dijkstra(grafo, vertice1)
    vertices_MST = gr.vertices(MST)
    vertice2 = lt.getElement(vertices, (lt.size(vertices_MST)-1))
    num_nodos = gr.numVertices(MST)
    #para hallar costo total hacer un dist to con vertice inicial y final
    distancia_total = Graphs.dijsktra.distTo(MST, vertice2)

    return num_nodos, distancia_total


def req5(catalog, landing_point):
    adyacentes =  gr.adjacents(catalog['graph_landing_points'], landing_point)
    #relacionar adyacentes con paises 
