from Grafo import Grafo
import pprint
import matplotlib.pyplot as plt
import numpy as np


class Plov(Grafo):
  def es_posicion_valida(self, pastor, lobo, oveja, verdura):
    if lobo == oveja    and pastor != oveja: return False
    if verdura == oveja and pastor != oveja: return False
    return True


  def genera_sucesores(self, nodo):
    hijos = []
    pastor = (int)(nodo[0])
    lobo = (int)(nodo[1])
    oveja = (int)(nodo[2])
    verdura = (int)(nodo[3])

    pastor = 1 - pastor
    if self.es_posicion_valida(pastor, lobo, oveja, verdura):
      hijos.append(f"{pastor}{lobo}{oveja}{verdura}")

    lobo = 1-lobo
    if self.es_posicion_valida(pastor, lobo, oveja, verdura):
      hijos.append(f"{pastor}{lobo}{oveja}{verdura}")
    lobo = 1-lobo

    oveja = 1-oveja
    if self.es_posicion_valida(pastor, lobo, oveja, verdura):
      hijos.append(f"{pastor}{lobo}{oveja}{verdura}")
    oveja = 1-oveja

    verdura = 1-verdura
    if self.es_posicion_valida(pastor, lobo, oveja, verdura):
      hijos.append(f"{pastor}{lobo}{oveja}{verdura}")
    verdura = 1-verdura

    return hijos


  def es_solucion(self, nodo_actual):
      return nodo_actual == "1111"
  

g = Plov()
g.recorre_grafo(nodo_inicial= "0000", modo="anchura")
ruta = g.genera_ruta('1111')
print(ruta[::-1])