import random
from Grafo import Grafo
import pprint

"""
[[4,0], [2, 1], ....]

[4,2,5,2,1,6,7,3] , [3,1,5,5,1,2,7,3]

"""

class ndamas(Grafo):
    # self.poblacion = []
    def __init__(self, n):
      pass

    def crear_tablero(self):
        tablero = []
        l1n = ['n',' ','n',' ','n',' ','n',' ']
        l2n = [' ','n',' ','n',' ','n',' ','n']
        l_vacia = [' ',' ',' ',' ',' ',' ',' ',' ']
        l1b = ['b',' ','b',' ','b',' ','b',' ']
        l2b = [' ','b',' ','b',' ','b',' ','b']

        tablero.append(l1n)
        tablero.append(l2n)
        tablero.append(l1n)
        tablero.append(l_vacia)
        tablero.append(l_vacia)
        tablero.append(l1b)
        tablero.append(l2b)
        tablero.append(l1b)

        return tablero

    # generar nelem individuos al azar
    def genera_nelementos(self, nelem):
      
      return elementos

    # valora cuantos errores tiene la posición
    # 0 es ningún error, cualquier otro valor es positivo
    def valora_errores_posicion(self, pos):
      nerrores = 0

      return nerrores


# Generar una población inicial
# durante un número máximo de iteraciones:
#   ordenar la poblacion
#   quedarse con los mejores
#   si alguno es solucion acabar
#   cruzar individuos
#   añadir hijos a la población
    
g = ndamas(2)
tablero = g.crear_tablero()
pprint.pprint(tablero)