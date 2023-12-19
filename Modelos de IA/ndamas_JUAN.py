import random
from Grafo import Grafo
import numpy as np  

"""
[[4,0], [2, 1], ....]

[4,2,5,2,1,6,7,3] , [3,1,5,5,1,2,7,3]

"""

class ndamas(Grafo):
    errores_poblacion = [10]
    poblacion = []
    tablero = []

    def __init__(self, n):
      self.tablero = np.zeros((n, n), dtype=int)
      pass

    def es_solucion(self, nodo_actual):
        if nodo_actual == 0: return True
        return False

    def gen_elementos2(self, nelem):
        pob = []
        for i in range(nelem):

            # Genero las damas creando una lista con el índice de la fila de cada columna de la matríz donde están
            elementos = self.genera_nelementos(8)
            indice = -1

            # Inicializo la matriz con una matriz de 8,8 de ceros
            jugada = np.zeros((8, 8), dtype=int)

            # Añado una dama en la posición seleccionada
            for l in elementos:
                indice += 1
                jugada[l][indice] = 1
        pob.append(jugada)
        return pob

    # generar nelem individuos al azar
    def genera_nelementos(self, nelem):
      elementos = []
      numero_aleatorio = random.randint(0, nelem-1)
      for i in range(nelem):
         elementos.append(random.randint(0, nelem-1))
      return elementos
    
    # Cuenta la cantidad de 1 que contiene una lista
    def cuantos_unos(self, lista):
      contador = 0
      for i in lista:
        if i == 1:
          contador += 1
      return contador


    def v2(self, jugada):
        num = 8
        nerrores_jugada = 0
        # Compruebo errores
        for x in range(num):
            for y in range(num):
                if jugada[x][y] == 1:
                    unos = 0
                    # Compruebo eje 'x'
                    fila = jugada[x]
                    unos = self.cuantos_unos(fila)
                    if unos > 1:
                        nerrores_jugada += 1
                    
                    # Compruebo eje 'y'
                    columna = []
                    for q in range(8):
                        columna.append(jugada[q][y])
                    unos = self.cuantos_unos(columna)
                    if unos > 1:
                        nerrores_jugada += 1
        
        # Compruebo diagonales
        diagonal = []
        diagonal_inversa = []

        ind_diagonal = -8
        for d in range(15):
            ind_diagonal += 1

            diagonal = jugada.diagonal(ind_diagonal)
            diagonal_inversa = np.fliplr(jugada).diagonal(ind_diagonal)

            unos = self.cuantos_unos(diagonal)
            if unos > 1:
                nerrores_jugada += 1
            # print(f'Diagonal {diagonal}, unos: {unos}')
                unos = self.cuantos_unos(diagonal_inversa)
            if unos > 1:
                nerrores_jugada += 1
        return nerrores_jugada


    # valora cuantos errores tiene la posición
    # 0 es ningún error, cualquier otro valor es positivo
    def valora_errores_posicion(self, num):#pos
      nerrores = 0
      nerrores_jugada = 0
      
      # Creación de jugada
      for i in range(100):
        # Añado errores a errores acomulados
        nerrores += nerrores_jugada
        # Reinicio la variables de los errores de cada jugada
        nerrores_jugada = 0

        # Genero las damas creando una lista con el índice de la fila de cada columna de la matríz donde están
        elementos = self.genera_nelementos(num)
        indice = -1

        # Inicializo la matriz con una matriz de 8,8 de ceros
        jugada = np.zeros((num, num), dtype=int)

        # Añado una dama en la posición seleccionada
        for l in elementos:
          indice += 1
          jugada[l][indice] = 1
        print(jugada)

        # Compruebo errores
        for x in range(num):
          for y in range(num):
            if jugada[x][y] == 1:
              unos = 0
              # Compruebo eje 'x'
              fila = jugada[x]
              unos = self.cuantos_unos(fila)
              if unos > 1:
                nerrores_jugada += 1
                
              # Compruebo eje 'y'
              columna = []
              for q in range(8):
                columna.append(jugada[q][y])
              unos = self.cuantos_unos(columna)
              if unos > 1:
                nerrores_jugada += 1
        
        # Compruebo diagonales
        diagonal = []
        diagonal_inversa = []

        ind_diagonal = -8
        for d in range(15):
          ind_diagonal += 1

          diagonal = jugada.diagonal(ind_diagonal)
          diagonal_inversa = np.fliplr(jugada).diagonal(ind_diagonal)

          unos = self.cuantos_unos(diagonal)
          if unos > 1:
            nerrores_jugada += 1
          # print(f'Diagonal {diagonal}, unos: {unos}')
          unos = self.cuantos_unos(diagonal_inversa)
          if unos > 1:
            nerrores_jugada += 1
          # print(f'Diagonal {diagonal_inversa}, unos: {unos}')
            
        
        print(f'Esta jugada tiene {nerrores_jugada} errores')

        '''
        Si el número de errores de la presente jugada es menor que el 
        último número de errores mínimo que se recogió que se añada la 
        matriz a la población
        '''
        if nerrores_jugada < self.errores_poblacion[len(self.errores_poblacion)-1]:
          self.errores_poblacion.append(nerrores_jugada)
          self.poblacion.append(jugada)

        print(f'{nerrores} errores acomulados')
        print()

      print(f'\nPOBLACION {len(self.poblacion)}:\n{self.poblacion}\nErrores TOP:{self.errores_poblacion}')
      return nerrores


# Generar una población inicial
# durante un número máximo de iteraciones:
#   ordenar la poblacion
#   quedarse con los mejores
#   si alguno es solucion acabar
#   cruzar individuos
#   añadir hijos a la población
    
g = ndamas(8)
g.genera_nelementos(8)
num = g.valora_errores_posicion(8)

g = ndamas(8)
pob = g.gen_elementos2(100)
iter = 0
for iter in range(100):
   pob.sort(key = g.v2)
   # mirar si pob[0] es solucion y break
   pob = pob[:100]
   #generar hijos
   lg = len(pob)/2
   for i in range(lg):
      el1 = pob[2*i]
      el2 = pob[2*i + 1]
      hijo 


