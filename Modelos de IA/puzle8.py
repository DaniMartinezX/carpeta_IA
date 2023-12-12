"""

puzle8
representación: cada posición es una cadena de dígitos del 0 al 8 separados por guiones
eje: "0-1-3-4-2-5-7-8-6"

final: "1-2-3-4-5-6-7-8-0"

"""

import pprint
import matplotlib.pyplot as plt
import json
import numpy as np
import math

from Grafo import Grafo

class PuzleN(Grafo):
    def __init__(self, np=8):
        Grafo.__init__(self)
        self.lado = int(math.sqrt(np+1))
    
    def es_solucion(self, nodo_actual):
    # print(f"Procesando nodo: {nodo_actual}")
        if nodo_actual = "1-2-3-4-5-6-7-8-0": return True
        return False

    def calcula_distanciaDst(self, nodo, nodo_destino):
        ###
        ### ????????? Aquí falta
        return 0







    # devuelve una lista de nodos hijo
    def genera_sucesores(self, nodo):
      hijos = []

 #     print(f"genero sucesores de {nodo}")
      # convertir la cadena en una lista
      l = nodo.split("-")
      ind = l.index("0")
      fila = ind // self.lado;  columna = ind % self.lado
      incs = [(-1,0), (1,0), (0,-1), (0,1)]
      for inc in incs:
         f = fila + inc[0]; c = columna + inc[1]
         if f >= 0 and f < self.lado and c >= 0 and c < self.lado:
            #intercambiar
            l[ind] = l[f*self.lado + c];   l[f*self.lado + c] = "0"
            s = "-".join(l)
            hijos.append(s)
            # dejar todo como estaba
            l[f*self.lado + c] = l[ind];   l[ind] = "0"
      return hijos



 
g = PuzleN(8)
final = "1-2-3-4-5-6-7-8-0"
inicial = "2-7-0-4-5-3-8-6-1"

#g = PuzleN(15)
#final = "1-2-3-4-5-6-7-8-9-10-11-12-13-14-15-0"
#inicial = "11-3-0-1-10-12-5-13-7-9-4-8-6-15-2-14" # 1121 pasos y  19200 iters en avaricioso

#g = PuzleN(15)
#final = "1-2-3-4-5-6-7-8-9-10-11-12-13-14-15-0"
#inicial = "14-1-5-4-2-7-6-8-9-10-15-12-13-3-11-0"   # (762 pasos en modo avaricioso), 294 si max_level = 300
#inicial = "0-2-3-4-1-6-7-8-5-10-11-12-9-13-14-15"   # (7 pasos en modo avaricioso)
# g.recorre_grafo("", modo="avaricioso")
# g.recorre_grafo(ini=inicial, end=final, modo="avaricioso")
#g.recorre_grafo(nodo_inicial=inicial, nodo_final=final, modo="profundidad")
ret = g.recorre_grafo(nodo_inicial=inicial, nodo_final=final, modo="avaricioso")
#ret = g.recorre_grafo(nodo_inicial=inicial, nodo_final=final, modo="avaricioso", max_level = 200)

if ret: 
    ruta = g.genera_ruta(final)
    print(f"Encontrada solución en {len(ruta)} pasos:\n{ruta[::-1]}")
else: print("Se exploró sin encontrar solución")