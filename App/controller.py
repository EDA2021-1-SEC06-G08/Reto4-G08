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
 """

import config as cf
import model
import csv
import time
import tracemalloc


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""
# =====================================
# Inicialización del Catálogo de libros
# =====================================

def initCatalog():
    """
    """
    catalog = model.newCatalog()
    return catalog

# ================================
# Funciones para la carga de datos
# ================================

def loadData(catalog):
    """
    """

    loadCountries(catalog)
    loadLanding_points(catalog)
    loadConnections(catalog)
    model.grap_Complete(catalog)
    
def loadLanding_points(catalog):
    """
    """
    file = cf.data_dir + 'landing_points.csv'
    input_file = csv.DictReader(open(file))
    for element in input_file:
        model.addMapLanding_points(catalog, element)

def loadCountries(catalog):
    """
    """
    file = cf.data_dir + 'countries.csv'
    input_file = csv.DictReader(open(file))
    for element in input_file:
        model.addMapCountries(catalog, element)
        
def loadConnections(catalog):
    """
    """
    file = cf.data_dir + 'connections.csv'
    input_file = csv.DictReader(open(file))
    for element in input_file:
        model.addMapConnections(catalog, element)
        #print(element)

#requerimientos 
def req1(catalog,nombre1, nombre2):
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    respuesta = model.req1(catalog, nombre1, nombre2)
   
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return respuesta, delta_time, delta_memory

def req2(catalog):
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    respuesta = model.req2(catalog)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return respuesta, delta_time, delta_memory

def req3(catalog, pais_a, pais_b):
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    respuesta = model.req3(catalog, pais_a, pais_b)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)


    return respuesta, delta_time, delta_memory


def req4(catalog):
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    respuesta = model.req4(catalog)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)


    return respuesta, delta_time, delta_memory

def req5(catalog, nombre_landing_point):
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    respuesta = model.req5(catalog, nombre_landing_point)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return respuesta, delta_time, delta_memory




def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(start_memory, stop_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory