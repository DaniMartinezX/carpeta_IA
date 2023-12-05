from Grafo import Grafo
import pprint
import matplotlib.pyplot as plt
import numpy as np

class canival_misionero(Grafo):
    def es_posicion_valida(self,barca, M_1, M_2, M_3, C_1, c_2, c_3):
        misioneros = [M_1, M_2, M_3]
        canivales = [C_1, c_2, c_3]
        num_canivales_0 = 0
        num_canivales_1 = 0
        num_misioneros_0 = 0
        num_misioneros_1 = 0

        if barca == 0:
            
        else:


        for i in canivales:
            if i == 0:
                num_canivales_0 += 1
            else:
                num_canivales_1 += 1

        for j in misioneros:
            if j == 0:
                num_misioneros_0 += 1
            else:
                num_misioneros_1 += 1
        
        if num_canivales_0 > num_misioneros_0: return False
        if num_canivales_1 > num_misioneros_1: return False

        return True
    
    def genera_sucesores(self, nodo):
        hijos = []
        M_1 = (int)(nodo[0])
        M_2 = (int)(nodo[1])
        M_3 = (int)(nodo[2])
        C_1 = (int)(nodo[3])
        c_2 = (int)(nodo[4])
        c_3 = (int)(nodo[5])
        #barca = (int)(nodo[6])

        M_1 = 1 - M_1
        if self.es_posicion_valida(M_1, M_2, M_3, C_1, c_2, c_3):
            hijos.append(f"{M_1}{M_2}{M_3}{C_1}{c_2}{c_3}")

        M_2 = 1 - M_2
        if self.es_posicion_valida(M_1, M_2, M_3, C_1, c_2, c_3):
            hijos.append(f"{M_1}{M_2}{M_3}{C_1}{c_2}{c_3}")

        M_3 = 1 - M_3
        if self.es_posicion_valida(M_1, M_2, M_3, C_1, c_2, c_3):
            hijos.append(f"{M_1}{M_2}{M_3}{C_1}{c_2}{c_3}")

        C_1 = 1 - C_1
        if self.es_posicion_valida(M_1, M_2, M_3, C_1, c_2, c_3):
            hijos.append(f"{M_1}{M_2}{M_3}{C_1}{c_2}{c_3}")

        c_2 = 1 - c_2
        if self.es_posicion_valida(M_1, M_2, M_3, C_1, c_2, c_3):
            hijos.append(f"{M_1}{M_2}{M_3}{C_1}{c_2}{c_3}")
        c_2 = 1 - c_2

        c_3 = 1 - c_3
        if self.es_posicion_valida(M_1, M_2, M_3, C_1, c_2, c_3):
            hijos.append(f"{M_1}{M_2}{M_3}{C_1}{c_2}{c_3}")
        c_3 = 1 - c_3

        return hijos
    
    def es_solucion(self, nodo_actual):
      return nodo_actual == "111111"
    
g = canival_misionero()
g.recorre_grafo(nodo_inicial= "000000", modo='anchura')
ruta = g.genera_ruta('111111')
print(ruta[::-1])