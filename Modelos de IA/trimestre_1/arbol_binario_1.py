class Nodo:
  def __init__(self, texto):
    self.si = None
    self.no = None
    self.datos = texto

class ArbolBinario:
  def __init__(self):
    self.root = None  # Puntero al nodo raíz del árbol

  def preguntar(self,nodo):
    if nodo is None or nodo.si is None and nodo.no is None:
      print(nodo.datos)
    else:
      print(nodo.datos)
      respuesta = input()
      if respuesta == "s":
        self.preguntar(nodo.si)
      else:
        self.preguntar(nodo.no)
    

#Preguntas
raiz = Nodo('Tienen aguja?')
# ===========================
r1 = Nodo('Acículas largas o no?')
r10 = Nodo('verticiliadas o no?')
# ===========================
r0 = Nodo('Hojas grandes o no?')
r01 = Nodo('Hojas compuestas o no?')
r011 = Nodo('Hojas palmado-compuestas?')
r010 = Nodo('Hojas duras?')
r0110 = Nodo('Legumbre o no?')
r0101 = Nodo('Bellota o no?')
r0100 = Nodo('Hoja Penninervia o no?')
r01001 = Nodo('Hoja más larga que ancha?')
r01000 = Nodo('Fruto con 2 alas que forman un ángulo?')
r010010 = Nodo('Borde inferior asimétrico?')

# Creación de árbol binario
arbol = ArbolBinario()


# EMPIEZA EL ROOT
raiz.si = r1
raiz.no = r0
# PRINCIPAL SÍ -------------------------
r1.si = Nodo('PINO') 
r1.no = r10 
r10.si = Nodo('CEDRO') 
r10.no = Nodo('ABETO') 

# PRINCIPAL NO -------------------------
r0.si = r01

r0.no = Nodo('CIPRÉS')

r01.si = r011
r01.no = r010

r011.si = Nodo('CASTAÑO DE INDIAS')
r011.no = r0110
r010.si = r0101
r010.no = r0100

r0110.si = Nodo('FALSA ACACIA')
r0110.no = Nodo('FRESNO')
r0101.si = Nodo('ENCINA')
r0101.no = Nodo('MADROÑO')
r0100.si = r01001
r0100.no = r01000

r01001.si = Nodo('SAUCE LLORÓN')
r01001.no = r010010
r01000.si = Nodo('ARCE')
r01000.no = Nodo('PLÁTANO DE SOMBRA')

r010010.si = Nodo('OLMO')
r010010.no = Nodo('CHOPO')

arbol.preguntar(raiz)
