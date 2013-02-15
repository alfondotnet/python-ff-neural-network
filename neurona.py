import random
import math
import sys

# 21 Ene 2013
# En la neurona guardare una lista de "n" pesos de entrada
# En la capa 0 (entrada), los pesos de entrada valen 1


MIN = -0.5
MAX = 0.5


class Neurona:

    def __init__(self, n, posicion, entrada=False, nombre=""):

        self.pesos = list()
        self.incrementos = list() # Es una lista con los incrementos anteriores (uno por cada peso)
        self.nombre = nombre # El nombre en caso de que sea de salida.
        self.posicion = posicion # La posicion que ocupa la neurona en la capa

        # Añadimos el peso imaginario solo a las capas que no son la de entrada
        if entrada == False:
            self.pesos.append(random.uniform(MIN,MAX))
            self.incrementos.append(0)

        for _ in range(n):
            if entrada:
                self.pesos.append(1.0) # HE CONSIDERADO QUE LAS NEURONAS DE ENTRADA TIENEN PESO 1
            else:
                self.pesos.append(random.uniform(MIN,MAX))
                self.incrementos.append(0)


    def calcula(self, entrada):
        
        ''' Aqui llega una lista de valores de entrada 
        --- El valor i-esimo se corresponde con el peso
        --- i-esimo que tiene almacenado la neurona en cuestion    
        '''

        try:
            
            if(len(entrada) != len(self.pesos)-1):
                raise Exception('Neurona>Calcula:El numero de entradas tiene que ser NUM_PESOS - 1')
                sys.exit(0)
            
            ini = 0

            ini += -1 * self.pesos[0] # sumamos primero el imaginario y pasamos a sumar el resto de entradas

            for e in range(len(entrada)):
                ini += entrada[e] * self.pesos[e+1]  # La entrada 0 es el peso 1 pues el peso 0 es de la imaginaria

            # Hacemos esto para evitar el math range error
            
            if (ini > 700):
                return 0.999
            elif(ini < -700):
                return 0.1
            else:
                return self.activacion(ini)            
            

        except Exception as e:
            print (e)
    

        
        return False

    def activacion(self, x):

        return 1 / (1 + math.exp(x*-1))

    

    def __str__(self):

        string = self.nombre + " -> " + str(self.pesos)

        return string

        
