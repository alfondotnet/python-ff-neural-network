import neurona
import sys

class Capa:

    def __init__(self, tamaño, tamaño_anterior, posicion):
        
        self.neuronas = list()
        self.posicion = posicion # posicion de la capa en la red
        
        entrada = True if posicion == 0 else False

        for n in range(tamaño):
            self.neuronas.append(neurona.Neurona(tamaño_anterior, n, entrada))


    def calcula(self, entradas):
        # Cada capa recibe una lista de entradas y tiene que devolver
        # Una lista de salidas (una por cada neurona)
        try:
            salida = list()
            if (self.posicion==0): # si es la capa de entrada
                if (len(entradas) != len(self.neuronas)):
                    raise Exception('Capa>Calcula: La longitud de la entrada debe ser igual al numero de neuronas de entrada!')
                    sys.exit(0)
                for indice in range(len(entradas)):
                    salida.append(entradas[indice]) # En la capa de entrada la salida es la propia entrada
                return salida
            # Si no es capa de entrada recibe la capa una lista de entradas y por cada neurona
            # tiene que llamar al calcula de esas entradas
            for n in self.neuronas:
                salida.append(n.calcula(entradas))
            return salida

        except Exception as e:
            print (e)
            
                    
    

    def __str__(self):

        string = "La capa " + str(self.posicion) + " tiene " + str(len(self.neuronas)) + " neuronas:\n"
        
        for n in self.neuronas:

            string += "\t\t " + str(n) + "\n"

        return string
    
