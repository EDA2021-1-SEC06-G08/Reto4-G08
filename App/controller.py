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
    loadLanding_points(catalog)
    loadCountries(catalog)
    loadConnections(catalog)

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