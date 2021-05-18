"""
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
from DISClib.ADT import list as lt
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
    print("3- Datos interesantes")
    print("4- Identificar los clusteres de comunicacion")
    print("5- Identificar los puntos de conexion criticos de la red")
    print("6- La ruta de menor distancia")
    print("7- Identificar la infraestructura critica de la red")
    print("8- Analisis de fallas")
    print("9- Los mejores canales para transmitir")
    print("10- La mejor ruta para comunicarme")
    print("11- Graficando los grafos")
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

def totalLanding_points(catalog):
    """
    """
    print("\n")
    print("El total de landing_points cargados es: " + str(lt.size(catalog['landing_points'])))

def totalConnections(catalog):
    """
    """
    print("El total de conexiones es: " + str(lt.size(catalog['connections'])))

def totalCountries(catalog):
    """
    """
    print("El total de paises es: " + str(lt.size(catalog['countries'])))

def firstLanding_point(catalog):
    """
    """
    landing_point = lt.firstElement(catalog['landing_points'])
    print("\n")
    print("Los datos del primer landing_point cargado son: ")
    print("El landing_point es: " + str(landing_point['landing_point_id']))
    print("El nombre es: " + str(landing_point['name']))
    print("La altitud es: " + str(landing_point['latitude']))
    print("La longitud es: " + str(landing_point['longitude']))
    print("\n")

def lastCountrie(catalog):
    """
    """
    countrie = lt.lastElement(catalog['countries'])
    print("\n")
    print("Los datos del ultimo pais cargado son: ")
    print("La cantidad de poblacion de " + str(countrie['CountryName']) + " es " + str(countrie['Population']))
    print("La cantidad de usuarios de internet de " + str(countrie['CountryName']) + " es " + str(countrie['Internet users']))
    print("\n")
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
        print("Datos cargados ....")
        print("\n")
    elif int(inputs[0]) == 3:
        print("Cargando información de los archivos ....")
        totalLanding_points(catalog)
        totalConnections(catalog)
        totalCountries(catalog)
        firstLanding_point(catalog)
        lastCountrie(catalog)
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
    elif int(inputs[0]) == 11:
        print("Cargando información de los archivos ....")
    else:
        sys.exit(0)
sys.exit(0)
