﻿"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 """

import config as cf
import sys
import controller
from DISClib.ADT import graph as gr
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import linkedlistiterator as it
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.DataStructures import mapentry as me
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

# ====  
# Menu
# ====

def printMenu():
    print("Bienvenido")
    print("1- Cargar el catálogo")
    print("2- Cargar la data del catalogo")
    print("3- Identificar los clusteres de comunicacion")
    print("4- Identificar los puntos de conexion criticos de la red")
    print("5- La ruta de menor distancia")
    print("6- Identificar la infraestructura critica de la red")
    print("7- Analisis de fallas")
    print("8- Los mejores canales para transmitir")
    print("9- La mejor ruta para comunicarme")
    print("10- Graficando los grafos")
    print("0- Para salir del menu")

# ===========================
# Implementacion del catalogo
# ===========================

def initCatalog():
    """
    """
    return controller.initCatalog()

# ==============
# Carga de datos
# ==============

def loadData(catalog):
    """
    """
    controller.loadData(catalog)

# ==================
# Datos interesantes
# ==================

def total_landing_point(catalog):
    """
    """
    print("El total de landing points es: " + str(mp.size(catalog['map_landing_points'])))

def total_connections(catalog):
    """
    """
    total = 0
    lista_map = mp.valueSet(catalog['map_connections'])
    iterator = it.newIterator(lista_map)
    while it.hasNext(iterator):
        mapa = it.next(iterator)
        connections = mp.valueSet(mapa)
        iterador = it.newIterator(connections)
        while it.hasNext(iterador):
            element = it.next(iterador)
            total += 1
    print("El total de connections es: " + str(total))

def total_countries(catalog):
    """
    """
    print("El total de paises es: " + str(mp.size(catalog['map_countries'])))

def last_country(catalog):
    """
    """
    list_countries = mp.valueSet(catalog['map_countries'])
    last_element = lt.lastElement(list_countries)
    print("El nombre del ultimo pais: " + str(last_element['CountryName']))
    print("La cantidad de poblacion es: " + str(last_element['Population']))
    print("La cantidad de usuario con interent es: " + str(last_element['Internet users']))

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    print("\n")
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Inicializando....")
        catalog = initCatalog()
        print("\n")
    elif int(inputs[0]) == 2:
        print("Cargando información de los archivos ....")
        loadData(catalog)
        total_landing_point(catalog)
        total_countries(catalog)
        last_country(catalog)
        total_connections(catalog)
        #print(catalog['graph_landing_points'])
        print("Datos cargados ....")
        print("\n")
    elif int(inputs[0]) == 3:
        print("Cargando información de los archivos ....")
    elif int(inputs[0]) == 4:
        print("Cargando información de los archivos ....")
    elif int(inputs[0]) == 5:
        print("Cargando información de los archivos ....")
    elif int(inputs[0]) == 6:
        print("Cargando información de los archivos ....")
    elif int(inputs[0]) == 7:
        print("Cargando información de los archivos ....")
    elif int(inputs[0]) == 8:
        print("Cargando información de los archivos ....")
    elif int(inputs[0]) == 9:
        print("Cargando información de los archivos ....")
    elif int(inputs[0]) == 10:
        print("Cargando información de los archivos ....")
    else:
        sys.exit(0)
sys.exit(0)
