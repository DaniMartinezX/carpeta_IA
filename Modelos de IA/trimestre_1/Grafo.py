import pprint
import matplotlib.pyplot as plt
import json
import numpy as np

class ErrNodoGrafo(Exception):
  def __init__(self, message='nodo no existe en el grafo'):
    super().__init__(message)

class GrafoBase:
  def __init__(self):
    self.nodos = {}

  def add_node(self, nodo, **kargs):
    if nodo in self.nodos: raise ErrNodoGrafo(message="Nodo Ya Existe!!")
    self.nodos[nodo] = {"edges":{}}
    for k,v in kargs.items():
      self.nodos[nodo][k] = v

  def remove_node(self, nodo):
    if nodo not in self.nodos: raise ErrNodoGrafo
    # desconectarme de todos los nodos con los que tengo aristas
    for n in self.nodos[nodo]["edges"]:
      self.nodos[n]["edges"].pop(nodo)
    self.nodos.pop(nodo)

  def set_node_attributes(self, nodo, **kargs):
    for k,v in kargs.items():
      self.nodos[nodo][k] = v

  def get_node_attribute(self, nodo, attribute, default=None):
    ret = self.nodos[nodo].get(attribute, default)
    return ret

  def add_edge(self, nodo1, nodo2, **kargs):
    if nodo1 not in self.nodos or nodo2 not in self.nodos: raise ErrNodoGrafo
    self.nodos[nodo1]["edges"][nodo2] = kargs
    self.nodos[nodo2]["edges"][nodo1] = kargs

  def remove_edge(self, nodo1, nodo2):
    if nodo1 not in self.nodos or nodo2 not in self.nodos: raise ErrNodoGrafo
    self.nodos[nodo1]["edges"].pop(nodo2, None)
    self.nodos[nodo2]["edges"].pop(nodo1, None)

  def set_edge_attributes(self, nodo1, nodo2, **kargs):
    for k,v in kargs.items():
      self.nodos[nodo1]["edges"][nodo2][k] = v

  def get_edge_attribute(self, nodo1, nodo2, attribute, default=None):
    ret = self.nodos[nodo1]["edges"][nodo2].get(attribute, default)
    return ret

  # returna una lista con los nodos conectados
  def adj(self, nodo):
    adyacentes = [n for n in self.nodos[nodo]["edges"]]
    return adyacentes


  def save_grafo(self, filename):
      with open(filename, 'w') as f:
          json.dump(self.nodos, f, indent="\t")

  def load_grafo(self, filename):
      with open(filename) as f:
          # Cargar su contenido y crear un diccionario
          self.nodos = json.load(f)

  def dibuja(self):
    fig = plt.figure(figsize=(20,10))

  # para cada nodo, dibuja un circulo en la posicion Xn, Yn
    for n in self.nodos:
      Xn = self.get_node_attribute(n, "x", 0)
      Yn = self.get_node_attribute(n, "y", 0)
      plt.scatter(Xn, Yn, s=300)
      plt.text(Xn,Yn, n)
      # plt.text(Xn,Yn-0.2, str(self.get_node_attribute(n, "distanciaOrg", 0)))

      # para cada arista
      for arista in self.nodos[n]["edges"]:
        # mira la posicion del nodo destino Xd, Yd
        Xd = self.get_node_attribute(arista, "x", 0)
        Yd = self.get_node_attribute(arista, "y", 0)
        plt.plot([Xn, Xd], [Yn, Yd], color="b", linewidth=0.5)
        # Escribe el weight en la mitad de camino entre los dos nodos
        plt.text((Xn+Xd)/2, (Yn+Yd)/2, self.get_edge_attribute(n, arista, "weight", 0), alpha=0.5)

  def dibuja_ruta(self, ruta):
    for i, n in enumerate(ruta):
      if i == 0: continue
      x1 = self.get_node_attribute(ruta[i-1], "x")
      y1 = self.get_node_attribute(ruta[i-1], "y")
      x2 = self.get_node_attribute(ruta[i], "x")
      y2 = self.get_node_attribute(ruta[i], "y")
      plt.plot([x1, x2], [y1, y2], color="k", linewidth=3)



class Grafo(GrafoBase):
  def __init__(self):
    super().__init__()
    self.abiertos = []
    self.cerrados = []

 # quita y devuelve un nodo de abiertos,
  # si modo = profundidad devuelve el último en entrar LIFO
  # si modo = anchura devuelve el primero en entrar (FIFO)
  # .....
  def pop_abiertos(self, modo):
    ret = None
    if modo == "profundidad":
      ret = self.abiertos.pop()
    elif modo == "anchura":
      ret = self.abiertos.pop(0)
    elif modo == "dijkstra":
      # escoger de todos los de abiertos el que tenga menor
      # valor de distanciaOrg
      idx_min = 0
      for i, n in enumerate(self.abiertos):
        if self.get_node_attribute(n, "distanciaOrg") < self.get_node_attribute(self.abiertos[idx_min], "distanciaOrg"):
          idx_min = i
      ret = self.abiertos.pop(idx_min)
    elif modo == "avaricioso":
      # escoger de todos los de abiertos el que tenga menor
      # valor de distanciaDst %%%%%
      idx_min = 0
      for i, n in enumerate(self.abiertos):
          if self.get_node_attribute(n, "distanciaDst") < self.get_node_attribute(self.abiertos[idx_min], "distanciaDst"):
              idx_min = i
      ret = self.abiertos.pop(idx_min)
      pass
    elif modo == "A*":
      # escoger la media
      # 
      pass
    return ret

  # si el nodo es una solución del problema devuelve TRUE
  def es_solucion(self, nodo_actual):
    # print(f"Procesando nodo: {nodo_actual}")
    return False

  # devuelve una lista con todos los nodos conectados al nodo actual
  def genera_sucesores(self, nodo_actual):
    return self.adj(nodo_actual)

  # devuelve una lista con los hijos, decidiendo que hacer si ya están en abiertos o cerrados
  def procesa_repetidos(self, hijos_iniciales):
    # print(f"procesa_repetidos: {hijos_iniciales}")
    hijos = [h for h in hijos_iniciales if h not in self.abiertos and h not in self.cerrados]
    return hijos

# ***************************************************************
# ***************************************************************

  # hacer recorridos del grafo en profundidad, anchura, dijkstra ....
  def recorre_grafo(self, nodo_inicial = None, nodo_destino = None, modo="anchura"):
    self.abiertos = []
    self.cerrados = []

    # si no se proporciona inicial escojo el primero que se creó
    if nodo_inicial is None: nodo_inicial = list(self.nodos.keys())[0]
    if nodo_inicial not in self.nodos:
        self.add_node(nodo_inicial, distanciaOrg = 0,  distanciaDst = np.inf)

        

# poner en todos los nodos un atributo distanciaOrg = inf
# excepto en el inicial que es 0
    for n in self.nodos:
      self.set_node_attributes(n, distanciaOrg=np.inf)
      self.set_node_attributes(n, antecesor=None)
    self.set_node_attributes(nodo_inicial, distanciaOrg=0)

    #%%%% poner en nodo_inicial distancia a destino

    # metemos en abiertos el nodo inicial
    self.abiertos.append(nodo_inicial)

    while len(self.abiertos) > 0: # mientras en abiertos existan nodos
      # quitar un nodo
      actual = self.pop_abiertos(modo)

      # mirar si es una solución
      # si tal break
      if self.es_solucion(actual):
        break

      # actual a cerrado
      self.cerrados.append(actual)

      # generar sucesores
      hijos = self.genera_sucesores(actual)


      # para cada hijo,
      # Si (distanciaOrg de actual + coste hacia el hijo )   <    distanciaOrg del hijo
      #       distanciaOrg del hijo = (distanciaOrg de actual + coste hacia el hijo )
      d_actual = self.get_node_attribute(actual, "distanciaOrg", 0)
      for hijo in hijos:
        if hijo not in self.nodos:
            self.add_node(hijo, distanciaOrg = d_actual+1,  distanciaDst = np.inf)
            self.set_node_attributes(hijo, antecesor=actual)
        self.add_edge(actual, hijo, weight=1)
        
        c_hijo = self.get_edge_attribute(actual, hijo, "weight", 0)
        d_hijo = self.get_node_attribute(hijo, "distanciaOrg", 0)
        if (c_hijo + d_actual) < d_hijo:
          self.set_node_attributes(hijo, distanciaOrg=(c_hijo+d_actual))
          self.set_node_attributes(hijo, antecesor=actual)
      # calcular la distancia a destino de cada hijo y anotarla en él
        if nodo_destino:
          d_destino = self.calcula_distanciaDst(hijo, nodo_destino)
          # actualizar en hijo esta distancia
          self.set_node_attributes(hijo, distanciaDst=d_destino)

      # que hacer con los repetidos
      hijos = self.procesa_repetidos(hijos)


      # insertar los hijos en abiertos
      for hijo in hijos:
        self.abiertos.append(hijo)

  def calcula_distanciaDst(self, destino, origen):
    # retorna una heurística de la distancia...
    ret = 0
    return ret

  def genera_ruta(self, inicio, puntero="antecesor"):
    l = []
    nodo = inicio
    while nodo is not None and nodo not in l:
      l.append(nodo)
      nodo = self.get_node_attribute(nodo, puntero)
    return l

