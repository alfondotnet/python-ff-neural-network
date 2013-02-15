import red
import faux
import fnmatch
import os
import random

# Ejemplo de prueba para la XOR
# Salida de entrenamiento:
#   Encontrada una RED MEJOR con ajuste: 1.9676966821537965
#   Encontrada una RED MEJOR con ajuste: 1.2596858372501274
#   Encontrada una RED MEJOR con ajuste: 0.1553738213748919
#   Paro el script (Ctrl+C


# La neurona que mejor aprende es la que tiene 4 neuronas en la capa oculta

def entrenamiento():
    
    conjunto_entrenamiento = [([0,0],[0]),([0,1],[1]),([1,0],[1]),([1,1],[0])]

    mejor_ajuste = 1000000
    it = 10000
    
    for i in range(it):

        r = red.Red("XOR", [2,int(random.uniform(2,5)),1])
        ##print ("aa")
        r.retroPropagacion(conjunto_entrenamiento, round(random.uniform(0.1,0.25),2), 400, round(random.uniform(0.8,0.9),2),mejor_ajuste)
        
        if r.aj < mejor_ajuste:
            mejor_ajuste = r.aj
            print ("Encontrada una RED MEJOR con ajuste: "+ str(mejor_ajuste))
            r.serializar("red_xor_entrenada") ###### TODO HACER CUANDO NO RECIBA NADA
            
        else:
            print ("Error encontrado: "+ str(r.aj) + " (PEOR)")

            
def comprobar(r, entrada):
 
    hd = r.haciaAdelante(entrada)

    return hd[2]



def main():

    #entrenamiento() ##(esto lo corro primero)
    
    r = red.cargarRed("red_xor_entrenada")

    print (r)
    print (r.ajuste)
    print (comprobar(r, [0,0]))
    print (comprobar(r, [0,1]))
    print (comprobar(r, [1,0]))
    print (comprobar(r, [1,1]))
    
    
    
main()
