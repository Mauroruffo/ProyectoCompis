from estructuras.VarsFuncs import *
from estructuras.Stack import *

txt = " "
cont = 0

def incrementarContador():
    global cont
    cont +=1
    return "%d" %cont

class Nodo():
    pass

class Null(Nodo):
	def __init__(self):
		self.type = 'void'

	def imprimir(self,ident):
		print(ident + "nodo nulo")

	def traducir(self):
		global txt
		id = incrementarContador()
		txt += id+"[label= "+"nodo_nulo"+"]"+"\n\t"

		return id

class program(Nodo):
    def __init__(self, son1, son2, son3, name):
        self.name = name
        self.son1 = son1
        self.son2 = son2
        self.son3 = son3
        Variable(son2, "program")

    def imprimir(self, ident):
        self.son1.imprimir(" " + ident)
        self.son2.imprimir(" " + ident)
        self.son3.imprimir(" " + ident)
        print(ident + "Nodo: " + self.name)

    def traducir(self):
        global txt
        id = incrementarContador()
        son1 = self.son1.traducir()
        son2 = self.son2.traducir()
        son3 = self.son3.traducir()
        txt += id + "[label= " + self.name + "]"+"\n\t"
        txt += id + "->" + son1 + "\n\t"
        txt += id + "->" + son2 + "\n\t"
        txt += id + "->" + son3 + "\n\t"
        return "digraph G {\n\t" + txt + "}"

class vars(Nodo):
    def __init__(self, son1, son2, name):
        self.name = name
        self.son1 = son1
        self.son2 = son2

    def imprimir(self, ident):
        self.son1.imprimir(" " + ident)
        print(ident + "Nodo: " + self.name)

    def traducir(self):
        global txt
        id = incrementarContador()
        son1 = self.son1.traducir()
        txt += id + "[label= " + self.name + "]"+"\n\t"
        txt += id + "->" + son1 + "\n\t"
        return id

class varsid1(Nodo):
    def __init__(self, name):
        self.name = name

    def imprimir(self, ident):
        print(ident + "ID: " + self.name)

    def traducir(self):
        global txt
        id = incrementarContador()
        return id

class varsid2(Nodo):
    def __init__(self, name):
        self.name = name

    def traducir(self):
        global txt
        id = incrementarContador()
        return id

class tipo1(Nodo):
    def __init__(self, name):
        self.name = name

    def traducir(self):
        global txt
        id = incrementarContador()
        return id

class tipo2(Nodo):
    def __init__(self, name):
        self.name = name

    def traducir(self):
        global txt
        id = incrementarContador()
        return id

class bloque(Nodo):
    def __init__(self, son1, name):
        self.name = name
        self.son1 = son1

    def imprimir(self, ident):
        self.son1.imprimir(" " + ident)
        print(ident + "Nodo: " + self.name)
        
    def traducir(self):
        global txt
        id = incrementarContador()
        son1 = self.son1.traducir()
        txt += id + "[label= " + self.name + "]"+"\n\t"
        txt += id + "->" + son1 + "\n\t"
        return id

class estatutoRec1(Nodo):
    def __init__(self, son1, son2, name):
        self.name = name
        self.son1 = son1
        self.son2 = son2

    def imprimir(self, ident):
        self.son1.imprimir(" " + ident)
        self.son2.imprimir(" " + ident)
        print(ident + "Nodo: " + self.name)
        
    def traducir(self):
        global txt
        id = incrementarContador()
        son1 = self.son1.traducir()
        son2 = self.son2.traducir()
        txt += id + "[label= " + self.name + "]"+"\n\t"
        txt += id + "->" + son1 + "\n\t"
        txt += id + "->" + son2 + "\n\t"
        return id

class estatuto1(Nodo):
    def __init__(self, son1, name):
        self.name = name
        self.son1 = son1

    def imprimir(self, ident):
        self.son1.imprimir(" " + ident)
        print(ident + "Nodo: " + self.name)
        
    def traducir(self):
        global txt
        id = incrementarContador()
        son1 = self.son1.traducir()
        txt += id + "[label= " + self.name + "]"+"\n\t"
        txt += id + "->" + son1 + "\n\t"
        return id

class estatuto2(Nodo):
    def __init__(self, son1, name):
        self.name = name
        self.son1 = son1

    def imprimir(self, ident):
        self.son1.imprimir(" " + ident)
        print(ident + "Nodo: " + self.name)
        
    def traducir(self):
        global txt
        id = incrementarContador()
        son1 = self.son1.traducir()
        txt += id + "[label= " + self.name + "]"+"\n\t"
        txt += id + "->" + son1 + "\n\t"
        return id

class estatuto3(Nodo):
    def __init__(self, son1, name):
        self.name = name
        self.son1 = son1

    def imprimir(self, ident):
        self.son1.imprimir(" " + ident)
        print(ident + "Nodo: " + self.name)
        
    def traducir(self):
        global txt
        id = incrementarContador()
        son1 = self.son1.traducir()
        txt += id + "[label= " + self.name + "]"+"\n\t"
        txt += id + "->" + son1 + "\n\t"
        return id

class estatuto4(Nodo):
    def __init__(self, son1, name):
        self.name = name
        self.son1 = son1

    def imprimir(self, ident):
        self.son1.imprimir(" " + ident)
        print(ident + "Nodo: " + self.name)
        
    def traducir(self):
        global txt
        id = incrementarContador()
        son1 = self.son1.traducir()
        txt += id + "[label= " + self.name + "]"+"\n\t"
        txt += id + "->" + son1 + "\n\t"
        return id

class estatuto5(Nodo):
    def __init__(self, son1, name):
        self.name = name
        self.son1 = son1

    def imprimir(self, ident):
        self.son1.imprimir(" " + ident)
        print(ident + "Nodo: " + self.name)
        
    def traducir(self):
        global txt
        id = incrementarContador()
        son1 = self.son1.traducir()
        txt += id + "[label= " + self.name + "]"+"\n\t"
        txt += id + "->" + son1 + "\n\t"
        return id

class asignacion(Nodo):
    def __init__(self, son1, name):
        self.name = name
        self.son1 = son1

    def imprimir(self, ident):
        self.son1.imprimir(" " + ident)
        print(ident + "Nodo: " + self.name)
        
    def traducir(self):
        global txt
        id = incrementarContador()
        son1 = self.son1.traducir()
        txt += id + "[label= " + self.name + "]"+"\n\t"
        txt += id + "->" + son1 + "\n\t"
        return id

class condicion(Nodo):
    def __init__(self, son1, son2, name):
        self.name = name
        self.son1 = son1
        self.son2 = son2

    def imprimir(self, ident):
        self.son1.imprimir(" " + ident)
        self.son2.imprimir(" " + ident)
        print(ident + "Nodo: " + self.name)
        
    def traducir(self):
        global txt
        id = incrementarContador()
        son1 = self.son1.traducir()
        son2 = self.son2.traducir()
        txt += id + "[label= " + self.name + "]"+"\n\t"
        txt += id + "->" + son1 + "\n\t"
        txt += id + "->" + son2 + "\n\t"
        return id

class condicion2(Nodo):
    def __init__(self, son1, son2, name):
        self.name = name
        self.son1 = son1
        self.son2 = son2

    def imprimir(self, ident):
        self.son1.imprimir(" " + ident)
        self.son2.imprimir(" " + ident)
        print(ident + "Nodo: " + self.name)
        
    def traducir(self):
        global txt
        id = incrementarContador()
        son1 = self.son1.traducir()
        son2 = self.son2.traducir()
        txt += id + "[label= " + self.name + "]"+"\n\t"
        txt += id + "->" + son1 + "\n\t"
        txt += id + "->" + son2 + "\n\t"
        return id

class read(Nodo):
    def __init__(self, name):
        self.name = name

    def traducir(self):
        global txt
        id = incrementarContador()
        return id

class while_(Nodo):
    def __init__(self, son1, son2, name):
        self.name = name
        self.son1 = son1
        self.son2 = son2

    def imprimir(self, ident):
        self.son1.imprimir(" " + ident)
        self.son2.imprimir(" " + ident)
        print(ident + "Nodo: " + self.name)
        
    def traducir(self):
        global txt
        id = incrementarContador()
        son1 = self.son1.traducir()
        son2 = self.son2.traducir()
        txt += id + "[label= " + self.name + "]"+"\n\t"
        txt += id + "->" + son1 + "\n\t"
        txt += id + "->" + son2 + "\n\t"
        return id
    
class expresion1(Nodo):
    def __init__(self, son1, son2, name):
        self.name = name
        self.son1 = son1
        self.son2 = son2

    def imprimir(self, ident):
        self.son1.imprimir(" " + ident)
        self.son2.imprimir(" " + ident)
        print(ident + "Nodo: " + self.name)
        
    def traducir(self):
        global txt
        id = incrementarContador()
        son1 = self.son1.traducir()
        son2 = self.son2.traducir()
        txt += id + "[label= " + self.name + "]"+"\n\t"
        txt += id + "->" + son1 + "\n\t"
        txt += id + "->" + son2 + "\n\t"
        return id

class expresion2(Nodo):
    def __init__(self, son1, son2, name):
        self.name = name
        self.son1 = son1
        self.son2 = son2

    def imprimir(self, ident):
        self.son1.imprimir(" " + ident)
        self.son2.imprimir(" " + ident)
        print(ident + "Nodo: " + self.name)
        
    def traducir(self):
        global txt
        id = incrementarContador()
        son1 = self.son1.traducir()
        son2 = self.son2.traducir()
        txt += id + "[label= " + self.name + "]"+"\n\t"
        txt += id + "->" + son1 + "\n\t"
        txt += id + "->" + son2 + "\n\t"
        return id

class expresion3(Nodo):
    def __init__(self, son1, son2, name):
        self.name = name
        self.son1 = son1
        self.son2 = son2

    def imprimir(self, ident):
        self.son1.imprimir(" " + ident)
        self.son2.imprimir(" " + ident)
        print(ident + "Nodo: " + self.name)
        
    def traducir(self):
        global txt
        id = incrementarContador()
        son1 = self.son1.traducir()
        son2 = self.son2.traducir()
        txt += id + "[label= " + self.name + "]"+"\n\t"
        txt += id + "->" + son1 + "\n\t"
        txt += id + "->" + son2 + "\n\t"
        return id

class exp1(Nodo):
    def __init__(self, son1, son2, name):
        self.name = name
        self.son1 = son1
        self.son2 = son2

    def imprimir(self, ident):
        self.son1.imprimir(" " + ident)
        self.son2.imprimir(" " + ident)
        print(ident + "Nodo: " + self.name)
        
    def traducir(self):
        global txt
        id = incrementarContador()
        son1 = self.son1.traducir()
        son2 = self.son2.traducir()
        txt += id + "[label= " + self.name + "]"+"\n\t"
        txt += id + "->" + son1 + "\n\t"
        txt += id + "->" + son2 + "\n\t"
        return id

class exp2(Nodo):
    def __init__(self, son1, son2, name):
        self.name = name
        self.son1 = son1
        self.son2 = son2
        t1 = None
        print("-", son1, son2, t1)

    def imprimir(self, ident):
        self.son1.imprimir(" " + ident)
        self.son2.imprimir(" " + ident)
        print(ident + "Nodo: " + self.name)
        
    def traducir(self):
        global txt
        id = incrementarContador()
        son1 = self.son1.traducir()
        son2 = self.son2.traducir()
        txt += id + "[label= " + self.name + "]"+"\n\t"
        txt += id + "->" + son1 + "\n\t"
        txt += id + "->" + son2 + "\n\t"
        return id

class termino1(Nodo):
    def __init__(self, son1, son2, name):
        self.name = name
        self.son1 = son1
        self.son2 = son2

    def imprimir(self, ident):
        self.son1.imprimir(" " + ident)
        self.son2.imprimir(" " + ident)
        print(ident + "Nodo: " + self.name)
        
    def traducir(self):
        global txt
        id = incrementarContador()
        son1 = self.son1.traducir()
        son2 = self.son2.traducir()
        txt += id + "[label= " + self.name + "]"+"\n\t"
        txt += id + "->" + son1 + "\n\t"
        txt += id + "->" + son2 + "\n\t"
        return id

class exp2(Nodo):
    def __init__(self, son1, son2, name):
        self.name = name
        self.son1 = son1
        self.son2 = son2

    def imprimir(self, ident):
        self.son1.imprimir(" " + ident)
        self.son2.imprimir(" " + ident)
        print(ident + "Nodo: " + self.name)
        
    def traducir(self):
        global txt
        id = incrementarContador()
        son1 = self.son1.traducir()
        son2 = self.son2.traducir()
        txt += id + "[label= " + self.name + "]"+"\n\t"
        txt += id + "->" + son1 + "\n\t"
        txt += id + "->" + son2 + "\n\t"
        return id

class termino2(Nodo):
    def __init__(self, son1, son2, name):
        self.name = name
        self.son1 = son1
        self.son2 = son2

    def imprimir(self, ident):
        self.son1.imprimir(" " + ident)
        self.son2.imprimir(" " + ident)
        print(ident + "Nodo: " + self.name)
        
    def traducir(self):
        global txt
        id = incrementarContador()
        son1 = self.son1.traducir()
        son2 = self.son2.traducir()
        txt += id + "[label= " + self.name + "]"+"\n\t"
        txt += id + "->" + son1 + "\n\t"
        txt += id + "->" + son2 + "\n\t"
        return id

class factor1(Nodo):
    def __init__(self, son1, name):
        self.name = name
        self.son1 = son1

    def imprimir(self, ident):
        self.son1.imprimir(" " + ident)
        print(ident + "Nodo: " + self.name)
        
    def traducir(self):
        global txt
        id = incrementarContador()
        son1 = self.son1.traducir()
        txt += id + "[label= " + self.name + "]"+"\n\t"
        txt += id + "->" + son1 + "\n\t"
        return id

class factor2(Nodo):
    def __init__(self, son1, name):
        self.name = name
        self.son1 = son1

    def imprimir(self, ident):
        self.son1.imprimir(" " + ident)
        print(ident + "Nodo: " + self.name)
        
    def traducir(self):
        global txt
        id = incrementarContador()
        son1 = self.son1.traducir()
        txt += id + "[label= " + self.name + "]"+"\n\t"
        txt += id + "->" + son1 + "\n\t"
        return id

class factor3(Nodo):
    def __init__(self, name):
        self.name = name

    def traducir(self):
        global txt
        id = incrementarContador()
        return id

class factor4(Nodo):
    def __init__(self, son1, name):
        self.name = name
        self.son1 = son1

    def imprimir(self, ident):
        self.son1.imprimir(" " + ident)
        print(ident + "Nodo: " + self.name)
        
    def traducir(self):
        global txt
        id = incrementarContador()
        son1 = self.son1.traducir()
        txt += id + "[label= " + self.name + "]"+"\n\t"
        txt += id + "->" + son1 + "\n\t"
        return id

class varcte1(Nodo):
    def __init__(self, son1, name):
        self.name = name
        self.son1 = son1

    def imprimir(self, ident):
        self.son1.imprimir(" " + ident)
        print(ident + "Nodo: " + self.name)
        
    def traducir(self):
        global txt
        id = incrementarContador()
        son1 = self.son1.traducir()
        txt += id + "[label= " + self.name + "]"+"\n\t"
        txt += id + "->" + son1 + "\n\t"
        return id

class varcte2(Nodo):
    def __init__(self, son1, name):
        self.name = name
        self.son1 = son1

    def imprimir(self, ident):
        self.son1.imprimir(" " + ident)
        print(ident + "Nodo: " + self.name)
        
    def traducir(self):
        global txt
        id = incrementarContador()
        son1 = self.son1.traducir()
        txt += id + "[label= " + self.name + "]"+"\n\t"
        txt += id + "->" + son1 + "\n\t"
        return id

class varcte3(Nodo):
    def __init__(self, son1, name):
        self.name = name
        self.son1 = son1

    def imprimir(self, ident):
        self.son1.imprimir(" " + ident)
        print(ident + "Nodo: " + self.name)
        
    def traducir(self):
        global txt
        id = incrementarContador()
        son1 = self.son1.traducir()
        txt += id + "[label= " + self.name + "]"+"\n\t"
        txt += id + "->" + son1 + "\n\t"
        return id

class write(Nodo):
    def __init__(self, son1, name):
        self.name = name
        self.son1 = son1

    def imprimir(self, ident):
        self.son1.imprimir(" " + ident)
        print(ident + "Nodo: " + self.name)
        
    def traducir(self):
        global txt
        id = incrementarContador()
        son1 = self.son1.traducir()
        txt += id + "[label= " + self.name + "]"+"\n\t"
        txt += id + "->" + son1 + "\n\t"
        return id

class writeInside1(Nodo):
    def __init__(self, son1, son2, son3, name):
        self.name = name
        self.son1 = son1
        self.son2 = son2
        self.son3 = son3

    def imprimir(self, ident):
        self.son1.imprimir(" " + ident)
        self.son2.imprimir(" " + ident)
        self.son3.imprimir(" " + ident)
        print(ident + "Nodo: " + self.name)
        
    def traducir(self):
        global txt
        id = incrementarContador()
        son1 = self.son1.traducir()
        son2 = self.son2.traducir()
        son3 = self.son3.traducir()
        txt += id + "[label= " + self.name + "]"+"\n\t"
        txt += id + "->" + son1 + "\n\t"
        txt += id + "->" + son2 + "\n\t"
        txt += id + "->" + son3 + "\n\t"
        return id

class writeInside2(Nodo):
    def __init__(self, son1, name):
        self.name = name
        self.son1 = son1

    def imprimir(self, ident):
        self.son1.imprimir(" " + ident)
        print(ident + "Nodo: " + self.name)
        
    def traducir(self):
        global txt
        id = incrementarContador()
        son1 = self.son1.traducir()
        txt += id + "[label= " + self.name + "]"+"\n\t"
        txt += id + "->" + son1 + "\n\t"
        return id

class writeInside3(Nodo):
    def __init__(self, son1, name):
        self.name = name
        self.son1 = son1

    def imprimir(self, ident):
        self.son1.imprimir(" " + ident)
        print(ident + "Nodo: " + self.name)
        
    def traducir(self):
        global txt
        id = incrementarContador()
        son1 = self.son1.traducir()
        txt += id + "[label= " + self.name + "]"+"\n\t"
        txt += id + "->" + son1 + "\n\t"
        return id

class more1(Nodo):
    def __init__(self, name):
        self.name = name

    def traducir(self):
        global txt
        id = incrementarContador()
        return id

class string(Nodo):
    def __init__(self, name):
        self.name = name

    def traducir(self):
        global txt
        id = incrementarContador()
        return id

class class_(Nodo):
    def __init__(self, son1, son2, name):
        self.name = name
        self.son1 = son1
        self.son2 = son2

    def imprimir(self, ident):
        self.son1.imprimir(" " + ident)
        self.son2.imprimir(" " + ident)
        print(ident + "Nodo: " + self.name)
        
    def traducir(self):
        global txt
        id = incrementarContador()
        son1 = self.son1.traducir()
        son2 = self.son2.traducir()
        txt += id + "[label= " + self.name + "]"+"\n\t"
        txt += id + "->" + son1 + "\n\t"
        txt += id + "->" + son2 + "\n\t"
        return id

class method(Nodo):
    def __init__(self, son1, son2, name):
        self.name = name
        self.son1 = son1
        self.son2 = son2

    def imprimir(self, ident):
        self.son1.imprimir(" " + ident)
        self.son2.imprimir(" " + ident)
        print(ident + "Nodo: " + self.name)
        
    def traducir(self):
        global txt
        id = incrementarContador()
        son1 = self.son1.traducir()
        son2 = self.son2.traducir()
        txt += id + "[label= " + self.name + "]"+"\n\t"
        txt += id + "->" + son1 + "\n\t"
        txt += id + "->" + son2 + "\n\t"
        return id

class bloquemethod(Nodo):
    def __init__(self, son1, son2, name):
        self.name = name
        self.son1 = son1
        self.son2 = son2

    def imprimir(self, ident):
        self.son1.imprimir(" " + ident)
        print(ident + "Nodo: " + self.name)
        
    def traducir(self):
        global txt
        id = incrementarContador()
        son1 = self.son1.traducir()
        txt += id + "[label= " + self.name + "]"+"\n\t"
        txt += id + "->" + son1 + "\n\t"
        return id

class function(Nodo):
    def __init__(self, son1, son2, name):
        self.name = name
        self.son1 = son1
        self.son2 = son2

class function1(Nodo):
    def __init__(self, son1, son2, name):
        self.name = name
        self.son1 = son1
        self.son2 = son2

class function2(Nodo):
    def __init__(self, son1, son2, name):
        self.name = name
        self.son1 = son1
        self.son2 = son2

class function3(Nodo):
    def __init__(self, son1, son2, name):
        self.name = name
        self.son1 = son1
        self.son2 = son2

class function4(Nodo):
    def __init__(self, son1, son2, name):
        self.name = name
        self.son1 = son1
        self.son2 = son2

class function5(Nodo):
    def __init__(self, son1, son2, name):
        self.name = name
        self.son1 = son1
        self.son2 = son2

class function6(Nodo):
    def __init__(self, son1, son2, name):
        self.name = name
        self.son1 = son1
        self.son2 = son2

class function7(Nodo):
    def __init__(self, son1, son2, name):
        self.name = name
        self.son1 = son1
        self.son2 = son2

class vdim(Nodo):
    def __init__(self, son1, son2, name):
        self.name = name
        self.son1 = son1
        self.son2 = son2

class vdim1(Nodo):
    def __init__(self, son1, son2, name):
        self.name = name
        self.son1 = son1
        self.son2 = son2

class vdim2(Nodo):
    def __init__(self, son1, son2, name):
        self.name = name
        self.son1 = son1
        self.son2 = son2

class vdim3(Nodo):
    def __init__(self, son1, son2, name):
        self.name = name
        self.son1 = son1
        self.son2 = son2

class arrayaccess(Nodo):
    def __init__(self, son1, son2, name):
        self.name = name
        self.son1 = son1
        self.son2 = son2

class arrayaccess1(Nodo):
    def __init__(self, son1, son2, name):
        self.name = name
        self.son1 = son1
        self.son2 = son2

class arrayaccess2(Nodo):
    def __init__(self, son1, son2, name):
        self.name = name
        self.son1 = son1
        self.son2 = son2

class arrayaccess3(Nodo):
    def __init__(self, son1, son2, name):
        self.name = name
        self.son1 = son1
        self.son2 = son2


class ID(Nodo):
    def __init__(self, name):
        self.name = name

    def imprimir(self, ident):
        print(ident + "ID: " + self.name)

    def traducir(self):
        global txt
        id = incrementarContador()
        return id

class Int(Nodo):
    def __init__(self, name):
        self.name = name

    def imprimir(self, ident):
        print(ident + "Int: " + self.name)

    def traducir(self):
        global txt
        id = incrementarContador()
        return id

class Float(Nodo):
    def __init__(self, name):
        self.name = name

    def imprimir(self, ident):
        print(ident + "Int: " + self.name)

    def traducir(self):
        global txt
        id = incrementarContador()
        return id

class Plus(Nodo):
    def __init__(self, name):
        self.name = name

    def imprimir(self, ident):
        print(ident + "Plus: " + self.name)

    def traducir(self):
        global txt
        id = incrementarContador()
        return id

class Minus(Nodo):
    def __init__(self, name):
        self.name = name

    def imprimir(self, ident):
        print(ident + "Plus: " + self.name)

    def traducir(self):
        global txt
        id = incrementarContador()
        return id

class LT(Nodo):
    def __init__(self, name):
        self.name = name

    def imprimir(self, ident):
        print(ident + "Less than: " + self.name)

    def traducir(self):
        global txt
        id = incrementarContador()
        return id

class GT(Nodo):
    def __init__(self, name):
        self.name = name

    def imprimir(self, ident):
        print(ident + "Greater than: " + self.name)

    def traducir(self):
        global txt
        id = incrementarContador()
        return id

class NE(Nodo):
    def __init__(self, name):
        self.name = name

    def imprimir(self, ident):
        print(ident + "Greater than: " + self.name)

    def traducir(self):
        global txt
        id = incrementarContador()
        return id

class Division(Nodo):
    def __init__(self, name):
        self.name = name

    def imprimir(self, ident):
        print(ident + "Division: " + self.name)

    def traducir(self):
        global txt
        id = incrementarContador()
        return id

class Multiplication(Nodo):
    def __init__(self, name):
        self.name = name

    def imprimir(self, ident):
        print(ident + "Greater than: " + self.name)

    def traducir(self):
        global txt
        id = incrementarContador()
        return id

class empty(Nodo):
    pass