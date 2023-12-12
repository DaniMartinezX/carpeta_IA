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
            barca += 1
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
        else:
            barca -= 1
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
    
    """
        Devuelve la cantidad de elementos de dos listas que no son comunes entre sí.

        Args:
            lista1: La primera lista.
            lista2: La segunda lista.

        Returns:
            La cantidad de elementos diferentes.
        """
    def cantidad_diferentes(self, lista1, lista2):
        lista_diferentes = []

        for i, e in enumerate(lista1):
            for i2, e2 in enumerate(lista2):
                if i == i2:
                    if e != e2:
                        lista_diferentes.append(e2)

        return len(lista_diferentes)
        

        #for i1, elemento1 in enumerate(lista1):
        

    def genera_sucesores(self, nodo):
        hijos = []
        for i in range(128):    # 128 porque son 7 bits
            s = format(i, "07b")    # formato de un string de unos y ceros
            if nodo == "1000100" and s == "0000010":
                print(".....")
            if s[0] == nodo[0]: continue    # Si no se ha movido la barca [INCORRECTO]
            if s[1:4].count("0") > 0 and s[4:].count("0") > s[1:4].count("0"): continue   # Si hay más caníbales en un lado que misioneros [INCORRECTO]
            if s[1:4].count("1") > 0 and s[4:].count("1") > s[1:4].count("1"): continue   # Si hay más caníbales en el otro lado que misioneros [INCORRECTO]
            if s[1:5] == nodo[1:5]: continue    # Si los que saben remar siguen en el mismo sitio de antes [INCORRECTO]
            if self.cantidad_diferentes(list(s), list(nodo)) not in [3,2] : continue # Si no han cambiado de posicion la barca y 2 personas o 1 [INCORRECTO]
            if self.cantidad_diferentes(list(s[5:]), list(nodo[5:])) == 2: continue  #  Si se mueven 2 canibales que no saben remar [INCORRECTO]
            if self.cantidad_diferentes(list(s[1:6]), list(nodo[1:6])) != 0 and s[0] == nodo[0]: continue # Si alguien cambio de orilla y no lo hizo en la misma direccion que el barco [INCORRECTO]
            mal = 0
            for i,v in enumerate(nodo):
                if v != s[i] and s[i] != s[0]: mal = 1
            if mal: continue
            if s[0] != nodo[0] and self.cantidad_diferentes(list(s[1:6]), list(nodo[1:6])) == 0: continue # Si sólo se ha movido la barca [INCORRECTO]
            

            """
            si solo se movio la barca
            si habiendo M en la derecha y  hay más canibales que M en la derecha
            si hay misioneros en la izquierda y hay menos misioneros que canibales en la izda
            si se mueven 2 canibales que no saben remar
            si alguien cambio de orilla y no lo hizo en la misma direccion que el barco
            si cambian más de 2 (además de la barca)
            no se pueden mover uno de los Can NO remadores solo
            """
            
            hijos.append(s)
        print(F"Nodo {nodo} genera {hijos}")
        return hijos


#    def genera_sucesores(self, nodo):
       # hijos = []
       # barca = (int)(nodo[0])
       # M_1 = (int)(nodo[1])
       # M_2 = (int)(nodo[2])
       # M_3 = (int)(nodo[3])
       # C_1 = (int)(nodo[4])
       # c_2 = (int)(nodo[5])
       # c_3 = (int)(nodo[6])
#
       # barca = 1 - barca
       # M_1 = 1 - M_1
       # if self.es_posicion_valida(barca, M_1, M_2, M_3, C_1, c_2, c_3):
       #     hijos.append(f"{barca}{M_1}{M_2}{M_3}{C_1}{c_2}{c_3}")
       # M_1 = 1 - M_1
#
  #
       # M_2 = 1 - M_2
       # if self.es_posicion_valida(barca, M_1, M_2, M_3, C_1, c_2, c_3):
       #     hijos.append(f"{barca}{M_1}{M_2}{M_3}{C_1}{c_2}{c_3}")
       # M_2 = 1 - M_2
#
#
       # M_3 = 1 - M_3
       # if self.es_posicion_valida(barca, M_1, M_2, M_3, C_1, c_2, c_3):
       #     hijos.append(f"{barca}{M_1}{M_2}{M_3}{C_1}{c_2}{c_3}")
       # M_3 = 1 - M_3
#
#
       # C_1 = 1 - C_1
       # if self.es_posicion_valida(barca, M_1, M_2, M_3, C_1, c_2, c_3):
       #     hijos.append(f"{barca}{M_1}{M_2}{M_3}{C_1}{c_2}{c_3}")
#
       # c_2 = 1 - c_2
       # if self.es_posicion_valida(barca, M_1, M_2, M_3, C_1, c_2, c_3):
       #     hijos.append(f"{barca}{M_1}{M_2}{M_3}{C_1}{c_2}{c_3}")
       # c_2 = 1 - c_2
#
       # c_3 = 1 - c_3
       # if self.es_posicion_valida(barca, M_1, M_2, M_3, C_1, c_2, c_3):
       #     hijos.append(f"{barca}{M_1}{M_2}{M_3}{C_1}{c_2}{c_3}")
       # c_3 = 1 - c_3
#
       # return hijos
    
    def es_solucion(self, nodo_actual):
      return nodo_actual == "1111111"
    

try:
    g = canival_misionero()
    g.recorre_grafo(nodo_inicial= "0000000", modo='anchura')
    ruta = g.genera_ruta('1111111')
    print(ruta[::-1])
except Exception as error:
    print(f'Este é o error: {error,}')
