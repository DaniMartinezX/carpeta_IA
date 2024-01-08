"""
Aplicación que presenta el grafo de las provincias españolas y muestre
la ruta más breve de León a A Coruña.
"""
import json
import pprint
import numpy as np
import matplotlib.pyplot as plt

import time

filename = 'gprovincias.json'

class ErrNodoGrafo(Exception):
  def __init__(self, message='nodo no existe en el grafo'):
    super().__init__(message)

class Grafo:
    def __init__(self):
        self.nodos = {}
        self.abiertos = []
        self.cerrados = []

    # AÑADE nodo nuevo al grafo
    def add_node(self, nodo, **kargs):
        if nodo in self.nodos: raise ErrNodoGrafo(message= "El nodo ya existe")
        self.nodos[nodo] = {'edges': {}}
        for k,v in kargs.items():
            self.nodos[nodo][k] = v

    # BORRA nodo en el grafo
    def remove_node(self, nodo):
        if nodo not in self.nodos: raise ErrNodoGrafo
        # desconectarme de todos los nodos con los que tengo aristas
        for n in self.nodos[nodo]["edges"]:
            self.nodos[n]["edges"].pop(nodo)
        # Finalmente se borra el nodo
        self.nodos.pop(nodo)

    # AÑADE ATRIBUTOS nuevos a un nodo
    def set_node_attributes(self, nodo, **kargs):
        for k,v in kargs.items():
            self.nodos[nodo][k] = v

    # MUESTRA ATRIBUTOS de un nodo (devuelve valor), si no hay nada devuelve 'None'
    def get_node_attribute(self, nodo, attribute, default=None):
        ret = self.nodos[nodo].get(attribute, default)
        return ret
    
    # AÑADE ARISTA nueva entre 2 nodos
    def add_edge(self, nodo1, nodo2, **kargs):
        if nodo1 not in self.nodos or nodo2 not in self.nodos: raise ErrNodoGrafo
        self.nodos[nodo1]["edges"][nodo2] = kargs
        self.nodos[nodo2]["edges"][nodo1] = kargs

    # BORRA ARISTA del grafo
    def remove_edge(self, nodo1, nodo2):
        if nodo1 not in self.nodos or nodo2 not in self.nodos: raise ErrNodoGrafo
        self.nodos[nodo1]["edges"].pop(nodo2, None)
        self.nodos[nodo2]["edges"].pop(nodo1, None)


    # AÑADE ATRIBUTOS A UNA ARISTA
    def set_edge_attributes(self, nodo1, nodo2, **kargs):
        for k,v in kargs.items():
            self.nodos[nodo1]["edges"][nodo2][k] = v

    # MUESTRA ATRIBUTOS DE UNA ARISTA
    def get_edge_attribute(self, nodo1, nodo2, attribute, default=None):
        ret = self.nodos[nodo1]["edges"][nodo2].get(attribute, default)
        return ret

    # Retorna lista con los nodos conectados
    def adj(self, nodo):
        adyacentes = [n for n in self.nodos[nodo]["edges"]]
        return adyacentes
    
    def dibuja(self):
        fig, ax = plt.subplots()
        for n in self.nodos:
            x = self.get_node_attribute(n, "x", 0)
            y = self.get_node_attribute(n, "y", 0)
            ax.scatter(x, y, s=300)
            ax.text(x,y, n)
            plt.text(x,y-0.2, str(self.get_node_attribute(n, "distanciaOrg", 0)))
            for l in self.nodos[n].get('edges', None):  # Por si no tiene nodos asociados que devuelva None
                ax.plot([self.get_node_attribute(n, "x", 0), 
                self.get_node_attribute(l, "x", 0)],
                [self.get_node_attribute(n, "y", 0),
                self.get_node_attribute(l, "y", 0)])

    def dibuja_ruta(self, ruta):
        for i, n in enumerate(ruta):
            if i == 0: continue
            x1 = self.get_node_attribute(ruta[i-1], "x")
            y1 = self.get_node_attribute(ruta[i-1], "y")
            x2 = self.get_node_attribute(ruta[i], "x")
            y2 = self.get_node_attribute(ruta[i], "y")
            plt.plot([x1,x2], [y1,y2], color='k', linewidth=3)

    def pop_abiertos(self, modo, f_astar):
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
            # Escoger de todos los abiertos el que tenga menos
            # valor de distanciaDst %%%%
            idx_min = 0
            for i, n in enumerate(self.abiertos):
                if self.get_node_attribute(n, "distanciaDst") < self.get_node_attribute(self.abiertos[idx_min], "distanciaDst"):
                    idx_min = i
            ret = self.abiertos.pop(idx_min)
        elif modo == "A*":
            # Dorg*f + Ddst*(1-f)
            idx_min = 0
            for i, n in enumerate(self.abiertos):
                if (self.get_node_attribute(n, "distanciaOrg") * f_astar) + (self.get_node_attribute(n, "distanciaDst") * (1-f_astar)) < \
                   (self.get_node_attribute(self.abiertos[idx_min], "distanciaOrg") * f_astar) + (self.get_node_attribute(self.abiertos[idx_min], "distanciaDst") * (1-f_astar)):
                    idx_min = i
                    # 1ª Vez A*
#                if (self.get_node_attribute(n, "distanciaOrg") + self.get_node_attribute(n, "distanciaDst"))/2 < \
#                   (self.get_node_attribute(self.abiertos[idx_min], "distanciaOrg") + self.get_node_attribute(self.abiertos[idx_min], "distanciaDst"))/2:
                    
            
            ret = self.abiertos.pop(idx_min)
            # Escoger la media, es el algoritmo más utilizado.
            #     
#            nodo_men_dist = self.abiertos[0]
#            for i,n in enumerate(self.abiertos):
#                dist_estimada = (self.get_node_attribute(n, "distanciaDst") + self.get_node_attribute(n, "distanciaOrg")) / 2
#                if dist_estimada < self.get_node_attribute(nodo_men_dist, 'distancia_media'):
#                    nodo_men_dist = n
#                ret = self.abiertos.pop(n)
            # media = list(map(lambda x: (self.get_node_attribute(x, 'distanciaDst', 0) + self.get_node_attribute(x, 'distanciaOrg', 0))/2,self.abiertos))
            # print(f'La media es {media}')
            # ret = self.abiertos.pop(self.abiertos.index(self.abiertos[media.index(min(media))]))
        return ret
    
    # si el nodo es una solución del problema devuelve TRUE
    def es_solucion(self, nodo_actual):
        print(f"Procesando nodo: {nodo_actual}")
        return False

    # devuelve una lista con todos los nodos conectados al nodo actual
    def genera_sucesores(self, nodo_actual):
        return self.adj(nodo_actual)

    # devuelve una lista con los hijos, decidiendo que hacer si ya están en abiertos o cerrados
    def procesa_repetidos(self, hijos_iniciales):
        # print(f"procesa_repetidos: {hijos_iniciales}")
        hijos = [h for h in hijos_iniciales if h not in self.abiertos and h not in self.cerrados]
        return hijos
    


    # hacer recorridos del grafo en profundidad, anchura, ....
    def recorre_grafo(self, nodo_inicial = None, nodo_destino = None, modo="anchura", factor_astar = 0.1):
        

        self.abiertos = []
        self.cerrados = []

        # si no se proporciona inicial escojo el primero que se creó
        if nodo_inicial is None: nodo_inicial = list(self.nodos.keys())[0]



        # INICIALIZAR la distanciaOrg de los nodos aquí
        for n in self.nodos:
            self.set_node_attributes(n, distanciaOrg = np.inf)
            self.set_node_attributes(n, antecesor=None)
            self.set_node_attributes(n, distanciaDst=np.inf)
        self.set_node_attributes(nodo_inicial, distanciaDst = self.calcula_distanciaDst(nodo_inicial, nodo_destino))
        self.set_node_attributes(nodo_inicial, distanciaOrg = 0)


        # Poner en nodo inicial distancia a destino

        # metemos en abiertos el nodo inicial
        self.abiertos.append(nodo_inicial)

        while len(self.abiertos) > 0: # mientras en abiertos existan nodos
            # quitar un nodo
            actual = self.pop_abiertos(modo, factor_astar)

            # mirar si es una solución
            # si tal break
            if self.es_solucion(actual):
                break

            # actual a cerrado
            self.cerrados.append(actual)

            # generar sucesores
            hijos = self.genera_sucesores(actual)

            # si estamos en modo dijkstra
            # para cada hijo,
            # Si (distanciaOrg de actual + coste hacia el hijo )   <    distanciaOrg del hijo
            #       distanciaOrg del hijo = (distanciaOrg de actual + coste hacia el hijo )

            for h in hijos:
                if self.nodos[actual]['distanciaOrg'] + self.nodos[actual]['edges'][h]['weight'] < self.nodos[h]['distanciaOrg']:            
                    self.nodos[h]['distanciaOrg'] = self.nodos[actual]['distanciaOrg'] + self.nodos[actual]['edges'][h]['weight']
                    self.nodos[h]['antecesor'] = actual
                    pprint.pprint(actual)

                if nodo_destino:
                    d_destino = self.calcula_distanciaDst(h, nodo_destino)
                    # Actualizar en hijo distancia
                    self.set_node_attributes(h, distanciaDst=d_destino)
                

            # que hacer con los repetidos
            hijos = self.procesa_repetidos(hijos)

            for h in hijos:
                self.abiertos.append(h)
            
            

    
    

    def calcula_distanciaDst(self, destino, origen):
        # Retorna una heurística de la distancia
        ret = 0
        x_origen = self.get_node_attribute(origen,"x")
        y_origen = self.get_node_attribute(origen,"y")
        x_destino = self.get_node_attribute(destino,"x")
        y_destino = self.get_node_attribute(destino,"y")

        # Cálculo de la hipotenusa con la fórmula de Pitágoras
        # Lo multiplicamos por 111 ya que en este caso la escala hace referencia a esa distancia
        # Y así tenemos la distancia exacta.
        ret = np.sqrt(((x_origen * x_destino)**2) + (((y_origen * y_destino)**2))) * 111
        return ret

    def genera_ruta(self, inicio, puntero='antecesor'):
        l = []
        nodo = inicio
        while nodo is not None and nodo not in l:
            l.append(nodo)
            nodo = self.get_node_attribute(nodo, puntero)
        
        puntero_nuevo = 'distanciaOrg'
        print(f'La distancia que hay hasta el destino es de {self.get_node_attribute(inicio, puntero_nuevo)} Kms')
        return l

    def calcula_media(self, destino, origen):
        ret = 0
        ret1 = self.get_node_attribute(origen, 'distanciaOrg')
        ret2 = self.get_node_attributes(destino, 'distanciaDst')

        ret = (ret1 + ret2) / 2
        print(f'La media es de {ret} Kms')
        return ret

    

g = Grafo()

def save_grafo(g):
    with open('Modelos de IA\gprovincias.json', 'w') as f:
        json.dump(g.nodos, f, indent="\t")

def load_grafo(g):
    with open("Modelos de IA\gprovincias.json") as f:
        # Cargar su contenido y crear un diccionario
        p = json.load(f)

        g.nodos = p

    # Lo de arriba resume lo de abajo
#    for key in list(p.keys()):
#        nodo = p[key]
#        g.add_node(key,edges=nodo.get('edges',None),x=nodo["x"],y=nodo["y"])
    


load_grafo(g)
inicio, final = [0.0,0.0]

inicio = time.time()
g.recorre_grafo(nodo_inicial='A Coruña', nodo_destino="Cádiz", modo='A*')
final = time.time()

print(f'\nTiempo de ejecución = {final-inicio}\n')


g.dibuja()
ruta = g.genera_ruta("Cádiz")
print(ruta[::-1])
g.dibuja_ruta(ruta)
plt.show()

# Mejoras para el algoritmo A*
# 1) incluir un factor f en recorre_grafico el cal supondrá una operacion aponderada para que el
#    algoritmo tire más a Dijstra(distanciaOrg) o a Avaricioso(distanciaDst): Dorg*f + Ddst*(1-f)
# 2) Suponer un coste máximo que le pasamos a la función recorre_grafico (coste_max=....)
# 3) Que no supere un nvl máximo de nodos para que llegue a destino (nivel_max=....). Al generar un hijo su nvl es el del padre + 1.