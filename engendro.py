import os
import faux
import red
import random

# Vale, digamos que este es el "frontend" del trabajo, lo único que el usuario va a usar
# Hay varias opciones
# Entrenar
#    Se entrena una red neurona del tipo que se le diga
# Comprobar
#    Aquí se enfrenta una determinada red con una batería de pruebas independiente del conjunto
#    de entrenamiento
#    Hay una opción (T) que saca qué red de las del tipo especificado es la mejor de todas
#    Entendiendose la mejor como la que más fotos de test acierta
# Seguir entrenando
#    Esto empieza a buscar redes pero solo guarda aquellas que superen la una cota dada
#    por el error cuadrático de la red que se le especifique al programa

# Iba a hacer una función que abriera N hijos entrenadores en paralelo, aunque
# Me ha resultado más fácil dada también la fecha que es (día antes de la entrega)
# Guardar cada red con el nombre de su error y abrir varias terminales, por lo que linux
# se encarga del resto.

def entrenamiento(iteraciones, it_retropro, tipo, dos_capas_ocultas, red_entrenada=False, verbose=False):
    

    conjunto_entrenamiento = faux.conjunto(tipo)


    if red_entrenada != False: # Si hay una entrenada entrenamos a mejor

        r = red.cargarRed("redes/"+tipo+"/"+ red_entrenada)
        mejor_ajuste = r.aj

    else:
        
        r = red.Red(tipo, [690,2,3]) # Bogus networkz
        mejor_ajuste = 1000000  
    

    print ("**************************************************************")
    print ("@@               Entrenamiento de "+tipo+"                  @@")
    print ("**************************************************************")
    
    print ("Va a comenzar el entrenamiento de la red ["+ r.nombre + "] \nComenzando con cota: "+ str(mejor_ajuste) + "...")
    print ("Numero de fotos para el entrenamiento: "+ str(len(conjunto_entrenamiento)))
    print ("Numero de iteraciones: "+ str(iteraciones))
    print ("Pulsa ENTER para comenzar el entrenamiento")
    input()
    
    for _ in range(iteraciones):

        neuronas_oculta = int(random.uniform(2,6))
        neuronas_oculta2 = int(random.uniform(4,6))
        if dos_capas_ocultas == True:
            r = red.Red(tipo, [690,neuronas_oculta,neuronas_oculta2,3])
        else:
            r = red.Red(tipo, [690,neuronas_oculta,3])  
              
        factor_aprendizaje = round(random.uniform(0.1,0.25),2)
        momentum = round(random.uniform(0.8,0.9),2)
        
        if (verbose):
            print ("++ Haciendo RP con FA: "+ str(factor_aprendizaje) + ", MOM: "+ str(momentum) + ", NOC: "+ str(neuronas_oculta) + "," + str(neuronas_oculta2))
        
        r = r.retroPropagacion(conjunto_entrenamiento, factor_aprendizaje, int(it_retropro), momentum, mejor_ajuste)

        if (verbose):
            print ("++ Error encontrado "+ str(r.aj))
        
        if r.aj < mejor_ajuste:
            mejor_ajuste = r.aj
            print ("+++++ Encontrada una RED MEJOR con ajuste: "+ str(mejor_ajuste))
            r.serializar("redes/"+tipo+"/"+ str(mejor_ajuste)) 
    

def main():

    print('''                                                                                  
  ___ _ __   __ _  ___ _ __   __| |_ __ ___  
 / _ \ '_ \ / _` |/ _ \ '_ \ / _` | '__/ _ \ 
|  __/ | | | (_| |  __/ | | | (_| | | | (_) |
 \___|_| |_|\__, |\___|_| |_|\__,_|_|  \___/ 
            |___/         By Alfonso Perez                   
 ''')

    print('''
    Que deseas hacer? 
    1) Entrenar
    2) Comprobar
    3) Seguir entrenando''')
    opcion = input(":")
    print ("\n")

    tipos = ["posturas","personas","ojos","gestos"]
    opciones = ["entrenar","comprobar","seguir entrenando"]
    
    print("Qué tipo de red quieres "+opciones[int(opcion)-1]+"?")
    
    i = 0
    for t in tipos:
        print ("("+str(i)+") "+ t)
        i += 1
    
    indice = input(":")
    tipo = tipos[int(indice)]

    if opcion == "1" or opcion == "3":
        
        print("Cuantas iteraciones en cada entorno quieres hacer? ej: 30")
        it_ret = input (":")
        
        print("Cuantas capas ocultas quieres probar? (Soportado 1/2)")
        capas_ocultas = input(":")
        
        if capas_ocultas == "2":
            dos_capas_ocultas = True
        else:
            dos_capas_ocultas = False
        
        if opcion == "1":
            entrenamiento(50, it_ret, tipo, dos_capas_ocultas, False, True)    

        if opcion == "3":
            
            print("Introduce el indice de la red que quieres seguir entrenando")
            
            nombres = list()
            i = 0
            for f in os.listdir('redes/'+tipo):
                print ("("+ str(i) + ") "+ f)
                nombres.append(f)
                i += 1
            indice = input(":")
            nombre = nombres[int(indice)]
            
            entrenamiento(50, it_ret, tipo, dos_capas_ocultas, nombre, True)    

    elif opcion == "2":
        
        # Aquí comprobamos en el directorio de test
        
        
        print("Introduce el indice de la red que quieres comprobar")
        
        nombres = list()
        i = 0
        for f in os.listdir('redes/'+tipo):
            print ("("+ str(i) + ") "+ f)
            nombres.append(f)
            i += 1
            
        print ("(T) Todas! (Decidme cual es mejor)")    
             
        indice = input(":")
        
        if indice == "T":
            # Aquí tenemos que iterar y decir cual es mejor
            
            print ("La mejor red del tipo "+ tipo + " es: "+ faux.obtenerMejorRed(tipo)[0] + " con "+ str(faux.obtenerMejorRed(tipo)[1]) + " aciertos")
                
        else:
            nombre = nombres[int(indice)]
            
            print("Quieres sacar la salida en Humano?")
    
            humano_input = input("(s/n): ")
    
            if(humano_input == "s"):
                humano = True
            else:
                humano = False
    
            redd = red.cargarRed("redes/"+tipo+"/"+nombre)
            
            print("\nAjuste de la red: "+ str(redd.aj) + "\n")
    
            for f in os.listdir('test/'+tipo):
                print ("La foto "+ str(f) + " mira: " + str(faux.comprobar(nombre, f, tipo, faux.clasificaciones(tipo), humano)))
     
        
main()