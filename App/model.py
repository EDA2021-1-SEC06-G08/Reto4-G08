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


from DISClib.DataStructures.edge import weight
import datetime
from math import asin, cos, radians, sin, sqrt
from DISClib.ADT import graph as gr
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms import Graphs 
from DISClib.Algorithms.Graphs import scc
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
    Contiene 4 tablas de hash que contiene las informacion del CSV
    Un grafo que contiene la coneccion entre landing_point
    """
    catalog = { 
                'map_landing_points': None,
                'map_countries': None,
                'map_connections': None,
                'capitals': None,
                'graph_landing_points': None
              }
    catalog['map_landing_points'] = mp.newMap(numelements=3200,
                            maptype='PROBING',
                            loadfactor=0.4)
    catalog['map_countries'] = mp.newMap(numelements=650,
                            maptype='PROBING',
                            loadfactor=0.4)
    catalog['map_connections'] = mp.newMap(numelements=1200,
                            maptype='PROBING',
                            loadfactor=0.4)
    catalog['capitals'] = mp.newMap(numelements=650,
                            maptype='PROBING',
                            loadfactor=0.4)
    catalog['graph_landing_points'] = gr.newGraph(datastructure='ADJ_LIST',
                                                  directed=False,
                                                  size=5000)
    return catalog


# ==============================================
# Funciones para agregar informacion al catalogo
# ==============================================


def addMapLanding_points(catalog, element):
    """
    Guarda la informacion del CSV landing_point en tablas de hash 
    que contiene tablas de hash con las ciudades
    """
    # Verificar si no existe el landing_point
    idEsta = mp.contains(catalog['map_landing_points'], element['landing_point_id'])
    # Verifica si es el primer landing_point
    if not idEsta and (mp.size(catalog['map_landing_points']) == 0):
        # Se crea una tabla de hash que contiene como Key una ciudad y como value la informacion del landing point
        cities_map = mp.newMap(numelements=15,
                                        maptype='PROBING',
                                        loadfactor=0.4)
        # Se separa las ciudades del landing_point
        cities = element['name'].split(",")
        # Se itera por cada ciudad para ver si es el pais
        for city in cities:
            CapitalName = city.strip(" ")
            # Se verifica si el pais esta en la tabla de hash de pais
            if mp.contains(catalog['map_countries'], CapitalName):
                # Si no se encuentra la ciudad capital se mete
                if not mp.contains(cities_map, city):
                    countryEntry = mp.get(catalog['map_countries'], CapitalName)
                    country = me.getValue(countryEntry)
                    capital = country['CapitalName']
                    mp.put(cities_map, capital, element)    
            else:
                # Si no se encuentra la ciudad se mete
                if not mp.contains(cities_map, city):
                    mp.put(cities_map, city, element)
        mp.put(catalog['map_landing_points'], element['landing_point_id'], cities_map)
        #Datos a retornar
        print("El primer landing_point cargado es: " + str(element['id']))
        print("El nombre es: " + str(element['name']))
        print("La latitude es: " + str(element['latitude']))
        print("La longitude es: " + str(element['longitude']))
    elif not idEsta:
        # Se crea una tabla de hash que contiene como Key una ciudad y como value la informacion del landing point
        cities_map = mp.newMap(numelements=10,
                                        maptype='PROBING',
                                        loadfactor=0.4)
        # Se separa las ciudades del landing_point
        cities = element['name'].split(",")
        # Se itera por cada ciudad para ver si es el pais
        for city in cities:
            CapitalName = city.strip(" ")
            # Se verifica si el pais esta en la tabla de hash de pais
            if mp.contains(catalog['map_countries'], CapitalName):
                # Si no se encuentra la ciudad capital se mete
                if not mp.contains(cities_map, city):
                    countryEntry = mp.get(catalog['map_countries'], CapitalName)
                    country = me.getValue(countryEntry)
                    capital = country['CapitalName']
                    mp.put(cities_map, capital, element)    
            else:
                # Si no se encuentra la ciudad se mete
                if not mp.contains(cities_map, city):
                    mp.put(cities_map, city, element)
        mp.put(catalog['map_landing_points'], element['landing_point_id'], cities_map)


def addMapCountries(catalog, element):
    """
    Contiene la informacion de Countrie del CSV
    """
    # Verifica si el pais esta en la tabla de hash
    idEsta = mp.contains(catalog['map_countries'], element['CountryName'])
    if not idEsta:
        # Verifica si es el pais no esta vacio
        if element['CountryName'] != '':
            # Mete el pais
            mp.put(catalog['map_countries'], element['CountryName'], element)
            # Mete la capital
            mp.put(catalog['capitals'], element['CapitalName'], element)


def addMapConnections(catalog, element):
    """
    Guarda la informacion de archivo Connections del CSV
    """
    # Verifica que este el landing_point de origen en la tabla de hash
    idEsta = mp.contains(catalog['map_connections'], element['ï»¿origin'])
    if not idEsta:
        # Crear la tabla de hash para el landing_point_destination 
        landing_point_destination_map = mp.newMap(numelements=20,
                                        maptype='PROBING',
                                        loadfactor=0.4)
        # crear la tabla de hash de cables
        landing_point_cable_map = mp.newMap(numelements=10,
                                        maptype='PROBING',
                                        loadfactor=0.4)
        # Se mete la informacion en la tabla de hash
        mp.put(landing_point_cable_map, element['cable_name'], element)
        mp.put(landing_point_destination_map, element['destination'], landing_point_cable_map)                                
        mp.put(catalog['map_connections'], element['ï»¿origin'], landing_point_destination_map)    
    else:
        # Obtener la tabla de hash de origen
        landing_point_origen_mapEntry = mp.get(catalog['map_connections'], element['ï»¿origin'])
        landing_point_origen_map = me.getValue(landing_point_origen_mapEntry)
        # Ver si esta el landing point de destination
        connectionEsta = mp.contains(landing_point_origen_map, element['destination'])
        if not connectionEsta:
            # crear la tabla de hash de cables
            landing_point_cable_map = mp.newMap(numelements=10,
                                            maptype='PROBING',
                                            loadfactor=0.4)
            # Se mete la informacion
            mp.put(landing_point_cable_map, element['cable_name'], element)
            mp.put(landing_point_origen_map, element['destination'], landing_point_cable_map)
            mp.put(catalog['map_connections'], element['ï»¿origin'], landing_point_origen_map)
        else:
            # Obtener la tabla de hash de destination
            landing_point_destination_entry = mp.get(landing_point_origen_map, element['destination'])
            landing_point_destination_map = me.getValue(landing_point_destination_entry)
            # Ver si se encuentra el cable
            cableEsta = mp.contains(landing_point_destination_map, element['cable_name'])
            if not cableEsta:
                # Se mete la informacion                                
                mp.put(landing_point_destination_map, element['cable_name'], element)
                mp.put(landing_point_origen_map, element['destination'], landing_point_destination_map)
                mp.put(catalog['map_connections'], element['ï»¿origin'], landing_point_origen_map)


def AddVertexLanding_PointCiudad(catalog):
    """
    Crea una lista de vertices que tiene la forma 3316-Abidjan
    """
    # Crea una tabla de hash que contiene los vertices
    VertexLanding_point = mp.newMap(numelements=6700,
                                    maptype='PROBING',
                                    loadfactor=0.4)
    # Obtener la lista de landing_points
    landing_point_list = mp.keySet(catalog['map_landing_points'])
    # Iterar sobre la lista de landing_points
    landing_point_iterator = it.newIterator(landing_point_list)
    while it.hasNext(landing_point_iterator):
        landing_point = it.next(landing_point_iterator)
        # Obtener las tablas de hash que tienes las ciudades 
        landing_point_hash_Entry = mp.get(catalog['map_landing_points'], landing_point)
        landing_point_hash = me.getValue(landing_point_hash_Entry)
        # Obtener la lista de ciudades
        cities_list = mp.keySet(landing_point_hash)
        # Iterar sobre la lista de ciudades
        cities_list_iterator = it.newIterator(cities_list)
        while it.hasNext(cities_list_iterator):
            city = it.next(cities_list_iterator)
            # Creo el vertice
            vertex = landing_point + "*" + str(city.strip(" "))
            # Agrego el vertice
            mp.put(VertexLanding_point, vertex, vertex)
    return VertexLanding_point
    

def addVertexCable(catalog, VertexLanding_point):
    """
    A la lista de vertices le agrega a cada vertice el nombre del cable que pasa por ahi 3316-Abidjan-A2frica
    """
    # Crea una tabla de hash de vertices
    vertex_return_nocapital = mp.newMap(numelements=6000,
                              maptype='PROBING',
                              loadfactor=0.4)
    vertex_return_capital = mp.newMap(numelements=6000,
                              maptype='PROBING',
                              loadfactor=0.4)
    # Obtener el origen de cada landing_point en Connections
    origin_list = mp.keySet(catalog['map_connections'])
    # Iterar sobre los origenes
    origin_iterator = it.newIterator(origin_list)
    while it.hasNext(origin_iterator):
        origin = it.next(origin_iterator)
        # Obtener la tabla de hash del origin
        tabla_origin_Entry = mp.get(catalog['map_connections'], origin)
        tabla_origin = me.getValue(tabla_origin_Entry)
        # Obtener la lista de destination
        destination_list = mp.keySet(tabla_origin)
        # Iterar sobre la lista de destination
        destination_iterator = it.newIterator(destination_list)
        while it.hasNext(destination_iterator):
            destination = it.next(destination_iterator)
            # Obtener la tabla de hash del destination
            tabla_destination_Entry = mp.get(tabla_origin, destination)
            tabla_destination = me.getValue(tabla_destination_Entry)
            # Obtener la lista de cables
            cable_list = mp.keySet(tabla_destination)
            # Iterar sobre la lista de cable
            cable_list_iterator = it.newIterator(cable_list)
            while it.hasNext(cable_list_iterator):
                cable = it.next(cable_list_iterator)
                # Obtener los vertices
                VertexLanding_point_list = mp.keySet(VertexLanding_point)
                # Iterar sobre la lista de VertexLanding_point
                VertexLanding_point_iterator = it.newIterator(VertexLanding_point_list)
                while it.hasNext(VertexLanding_point_iterator):
                    vertex = it.next(VertexLanding_point_iterator)
                    # Separar el vertice
                    vertex_separado = vertex.split("*")
                    # Iterar sobre el vertice separado 
                    if (vertex_separado[0] == origin or vertex_separado[0] == destination) and not mp.contains(catalog['capitals'], vertex_separado[1]):
                        vertex = vertex + "*" + cable
                        mp.put(vertex_return_nocapital, vertex, vertex)
                    elif (vertex_separado[0] == origin or vertex_separado[0] == destination) and mp.contains(catalog['capitals'], vertex_separado[1]):
                        vertex = vertex + "*" + cable
                        mp.put(vertex_return_capital, vertex, vertex)
    return vertex_return_nocapital,vertex_return_capital


def AddVertexGrapNoCapital(catalog):
    """
    Agrega los vertex al grafo sin las capitales
    """
    # Obtener la lista de vertex landing_point-ciudad
    VertexLanding_point = AddVertexLanding_PointCiudad(catalog)
    # Obtener el map de vertex
    Vertex_map = addVertexCable(catalog, VertexLanding_point)
    # Obtener la lista de vertex
    Vertex_list = mp.keySet(Vertex_map[0])
    # iterar sobre vertex
    Vertex_iterator = it.newIterator(Vertex_list)
    while it.hasNext(Vertex_iterator):
        vertex = it.next(Vertex_iterator)
        gr.insertVertex(catalog['graph_landing_points'], vertex)


def AddEdgesGrapNoCapital(catalog):
    """
    Agrega el arco entre 2 vertex
    """
    # Obtener la lista de origen
    origin_keys_list= mp.keySet(catalog['map_connections'])
    # Iterar sobre la lista de origen
    origin_keys_iterator = it.newIterator(origin_keys_list)
    while it.hasNext(origin_keys_iterator):
        origin = it.next(origin_keys_iterator)
        # Obtener la tabla de hash de destination
        destination_map_Entry = mp.get(catalog['map_connections'], origin)
        destination_map = me.getValue(destination_map_Entry)
        # Obtener la lista destination
        destination_keys_list = mp.keySet(destination_map)
        # Iterar sobra la lista de destination
        destination_keys_iterator = it.newIterator(destination_keys_list)
        while it.hasNext(destination_keys_iterator):
            destination = it.next(destination_keys_iterator)
            # Obtener la tabla de cables
            cable_map_Entry = mp.get(destination_map, destination)
            cable_map = me.getValue(cable_map_Entry)
            # Obtener la lista de cables
            cable_keys_list = mp.keySet(cable_map)
            # Iterar sobre la lista de cables
            cable_keys_iterator = it.newIterator(cable_keys_list)
            while it.hasNext(cable_keys_iterator):
                cable = it.next(cable_keys_iterator)
                # Obtener los vertex
                vertex_list  = gr.vertices(catalog['graph_landing_points'])
                # Vertex A
                vertexA_list = lt.newList('ARRAY_LIST')
                # Vertex B
                vertexB_list = lt.newList('ARRAY_LIST')
                # iterar sobre la lista de vertex
                vertex_list_iterator = it.newIterator(vertex_list)
                while it.hasNext(vertex_list_iterator):
                    vertex = it.next(vertex_list_iterator)
                    # Separar el vertex
                    vertex_separado = vertex.split("*")
                    # Ver si es origin o destination
                    if vertex_separado[0] == origin and vertex_separado[2] == cable:
                        lt.addLast(vertexA_list, vertex)
                    elif vertex_separado[0] == destination and vertex_separado[2] == cable:
                        lt.addLast(vertexB_list, vertex)
                weight = weightConnection(catalog, origin, destination)
                # Iterar sobre list Vertex A para unir
                vertexA_iterator = it.newIterator(vertexA_list)
                while it.hasNext(vertexA_iterator):
                    vertexA = it.next(vertexA_iterator)
                    # Iterar sobre list Vertex B para unir
                    vertexB_iterator = it.newIterator(vertexB_list)
                    while it.hasNext(vertexB_iterator):
                        vertexB = it.next(vertexB_iterator)
                        gr.addEdge(catalog['graph_landing_points'], vertexA, vertexB, weight)


def weightConnection(catalog, origin, destination):
    """
    Se obtiene el peso entre 2 landing_point
    """
    # Obtener la tabla de origin
    tabla_origin_Entry = mp.get(catalog['map_landing_points'], origin)
    tabla_origin = me.getValue(tabla_origin_Entry)
    # Obtener la tabla de destination
    tabla_destination_Entry = mp.get(catalog['map_landing_points'], destination)
    tabla_destination = me.getValue(tabla_destination_Entry)
    # Obtener el elemento de origin
    values_origin_list = mp.valueSet(tabla_origin)
    # Obtener el elemento de destination
    values_destination_list = mp.valueSet(tabla_destination)
    # Iterar sobra values origin
    values_origin_iterator = it.newIterator(values_origin_list)
    element_origin = it.next(values_origin_iterator)
    # Iterar sobra values destination
    values_destination_iterator = it.newIterator(values_destination_list)
    element_destination = it.next(values_destination_iterator)
    # Obtener la altitud y longitud de origin
    altitud_origin = element_origin['latitude']
    longitud_origin = element_origin['longitude']
    # Obtener la altitud y longitud de destination
    altitud_destination = element_destination['latitude']
    longitud_destination = element_destination['longitude']
    weight = haversine(float(altitud_origin), float(longitud_origin), float(altitud_destination), float(longitud_destination))
    return weight


def addVertexCapital(catalog):
    """
    """
    pass


def grap_Complete(catalog):
    """
    Agrega las funciones de la creacion del grafo
    """
    AddVertexGrapNoCapital(catalog)
    AddEdgesGrapNoCapital(catalog)


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


def req1(catalog, nombre1, nombre2):
    kosaraju = scc.KosarajuSCC(catalog['graph_landing_points'])
    vertices = gr.vertices(catalog['graph_landing_points'])
    vert1 = None
    vert2 = None 
    for vertice in lt.iterator(vertices):
        if vertice.split(sep='*')[1] == nombre1:
            vert1 = vertice
        elif vertice.split(sep='*')[1] == nombre2:
            vert2 = vertice

    for vertice in lt.iterator(vertices):
        if vertice.split(sep='*')[1] == nombre2:
            vert2 = vertice
        elif vertice.split(sep='*')[1] == nombre1:
            vert1 = vertice

    vertice_x = lt.getElement(vertices, 0)
    num_componentes_conectados = scc.sccCount(catalog['graph_landing_points'], kosaraju, vertice_x)
    #mismo_cluster = scc.stronglyConnected(kosaraju, vert1, vert2)
    #if mismo_cluster:
    #    respuesta = 'Los dos landing points están en el mismo clúster'
    #else:
    #    respuesta = 'Los dos landing points no están en el mismo clúster'
    #return num_componentes_conectados, respuesta 

def req2(catalog):
    maxvert = None 
    maxdeg = 0 
    lista_vertices = gr.vertices(catalog['graph_landing_points'])
    for vert in lt.iterator(lista_vertices):
        degree = gr.degree(catalog['graph_landing_points'], vert)
        if (degree > maxdeg):
            maxvert = vert 
            maxdeg = degree
    return maxvert, maxdeg

def req3(catalog, pais_a, pais_b):
    #sacar capital a partir de país 
    entry1 = mp.get(catalog['map_countries'], pais_a)
    vert1 = me.getValue(entry1)['CapitalName']
    entry2 = mp.get(catalog['map_countries'], pais_b)
    vert2 = me.getValue(entry2)['CapitalName']
    grafo = catalog['graph_landing_points']
    lista_ruta = lt.newList()
    vertices = gr.vertices(catalog['graph_landing_points'])

    landing_point_a = None 
    landing_point_b = None 

    for vert in lt.iterator(vertices):
        vertexa = vert.split(sep ='*')
        if vertexa[1] == vert1:
            landing_point_a = vert
        elif vertexa[1] == vert2:
            landing_point_b = vert

    for vert in lt.iterator(vertices):
        vertexb = vert.split(sep ='*')
        if vertexb[1] == vert2:
            landing_point_b = vert
        elif vertexb[1] == vert1:
            landing_point_a = vert
        

    MST = Graphs.dijsktra.Dijkstra(grafo, landing_point_a)
    distancia_total = Graphs.dijsktra.distTo(MST, landing_point_b)
    camino_pila = Graphs.dijsktra.pathTo(MST, landing_point_b)
    iterador = it.newIterator(camino_pila)
    while it.hasNext(iterador):
        ruta = st.pop(camino_pila)
        lt.addLast(lista_ruta, ruta)
    return distancia_total, lista_ruta
    

def req4(catalog):
    grafo = catalog['graph_landing_points']
    vertices_grafo = gr.vertices(grafo)
    vertice1 = lt.getElement(vertices, 0)
    MST = Graphs.dijsktra.Dijkstra(grafo, vertice1)
    vertices_MST = gr.vertices(MST)
    vertice2 = lt.getElement(vertices_MST, (lt.size(vertices_MST)-1))
    num_nodos = gr.numVertices(MST)
    #para hallar costo total hacer un dist to con vertice inicial y final
    distancia_total = Graphs.dijsktra.distTo(MST, vertice2)

    return num_nodos, distancia_total

def req5(catalog, nombre_landing_point):
    grafo = catalog['graph_landing_points']
    #paises = mp.keySet(catalog['map_countries'])
    lista_vertices = gr.vertices(catalog['graph_landing_points']) 
    lista_ciudades_afectadas = lt.newList(datastructure= 'ARRAY_LIST')
    tabla_landing_points = catalog['map_landing_points']
    #llaves_landing_points = mp.keySet(tabla_landing_points)
    lista_numvertice = lt.newList(datastructure= 'ARRAY_LIST')
    lista_paises_afectados = lt.newList(datastructure= 'ARRAY_LIST')
    lista_tablas = lt.newList(datastructure= 'ARRAY_LIST')
    vertice = None 
    for vert in lt.iterator(lista_vertices):
        if nombre_landing_point == vert.split(sep='*')[1]:
            vertice = vert
            paises_afectados = gr.adjacents(grafo, vertice)
            for vertices in lt.iterator(paises_afectados):
                if (int(lt.isPresent(lista_ciudades_afectadas, vertices.split(sep='*')[1]))) == 0:
                    lt.addLast(lista_ciudades_afectadas, vertices.split(sep='*')[1])
                    lt.addLast(lista_numvertice, vertices.split(sep='*')[0])
                    for numvertices in lt.iterator(lista_numvertice):
                        entry1 = mp.get(tabla_landing_points, numvertices)
                        tabla1 = me.getValue(entry1)
                        valores = mp.valueSet(tabla1)
                        values_iterator = it.newIterator(valores)
                        elemento = it.next(values_iterator)
                        ciudades_elemento = elemento['name'].split(sep= ',')
                        for ciudades in lt.iterator(lista_ciudades_afectadas):
                            if ciudades in ciudades_elemento:
                                pais = ciudades_elemento[-1]
                                if (int(lt.isPresent(lista_paises_afectados, pais))) == 0:
                                    lt.addLast(lista_paises_afectados, pais)
                       

    return lt.size(lista_paises_afectados), lista_paises_afectados['elements']


