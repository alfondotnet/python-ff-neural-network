import capa
import sys 
import pickle
import os
import faux
import fnmatch

# [21 Enero 2013] Inicio del trabajo ==========
# Bueno, después de leerme documentación al respecto
# Voy a empezar a hacer la implementación.
# Voy a intentar hacer la estructura lo más general posible para luego 
# poder modificarla bien
# RED: 
#    Tendrá:
#    Un nombre: Para __str__    
#    Una lista de tamaños de capas, por ejemplo [3,2,2] es una red con 3 capas, 3 neuronas de entrada
#    2 de salida y 2 en la capa oculta


# [23 Enero 2013]
# En teoría está listo, tengo que probar con un algoritmo de internet a ver si el mío aprende más o menos igual a ver si está bien.
# Problemas solucionados:
# Pues he tenido varios, uno de ellos es que no actualizaba correctamente los pesos ya que como considero el primer elemento de la
# lista de pesos el peso "umbral" pues me hice un lío con los índices y actualizaba el peso que no era, gracias al debugger de IDLE
# lo tengo mucho más claro y actualiza de forma correcta.
# TODO: Implementar momemtum ya que para el xor no me aprende nada bien, le pregunte lo que le pregunte me saca respuestas cercanas al
# 0.5

# [24 Enero 2013]
# Bueno, despues de pasarme toda la noche probando cosas, he hecho:

# - Un script en bash para que te haga una foto de la webcam y la ponga en una carpeta siguiendo recomendaciones del sistema
# de ficheros del profesor
# - He corregido el math range error: (Esto pasaba porque si los primeros pesos eran todos del mismo signo, y las entradas
# eran grandecitas (máx 255), llegaba un numero demasiado grande a la función sigmoide y petaba
# por lo que he considerado 0.9999999999999999 y 0.0000000000000000 cuando el numero es mayor o menor que 700
# y ya no da el fallo.

# - He programado el momentum, que hace que mejore mucho el rendimiento de mi prueba en XOR

# - Un fuzzer de parámetros, que lo que hace básicamente es:
# Escoge aleatoriamente un número de neuronas en la capa oculta, un factor de aprendizaje, momentum, y num. de iteraciones
# y luego va quedándose con la red que tenga el mejor "ajuste". Este ajuste lo que hace es mirar las diferencias en valor
# absoluto de las respuestas sobre la batería de pruebas del conjunto de entrenamiento con respecto a las salidas esperadas.
# por lo que la red que tenga menor "ajuste" es la "mejor" o la que "mejor" se ajusta.

# Estre criterio para la XOR me ha dado muy buenos resultados, una red con 0.01 de ajuste me saca 0.90 y pico para [1,0] y [0,1]
# y 0.0 y pico para [1,1] y [0,0]. Y para las caras la verdad que también. Queda en el TODO como evitar el sobre ajuste, aunque
# eso la verdad que son consideraciones que haré cuando tenga un conjunto de entrenamiento rico (bastantes más fotos de las que
# tengo ahora).

# 
REDONDEAR = 8

class Red:

    def __init__(self, nombre, tam_capas):

        self.nombre = nombre
        self.capas = list()
        self.aj = 10000
        
        tam_ant = 1
        posicion = 0
        for c in tam_capas:
            self.capas.append(capa.Capa(c, tam_ant, posicion))
            posicion += 1
            tam_ant = tam_capas[posicion-1]

    def haciaAdelante(self, entrada):
        ''' La red recibe una entrada de n valores (siendo n el numero de neuronas de entrada)
            y devuelve una lista de salidas de capa (cada salida de capa es una lista de salidas de neurona) '''

        try:
            if(len(entrada) != len(self.capas[0].neuronas)):
                raise Exception('Red>HaciaAdelante: El numero de entradas no coincide con de neuronas de entrada')
                sys.exit(0)
            
            indice_capa = 0
            salida = list()
            ret = list()
            
            while (indice_capa < len(self.capas)): # Iteramos hacia alante por capas
                salida = self.capas[indice_capa].calcula(entrada) # Cada capa calcula una salida que es una lista con las salidas de cada neurona
                entrada = salida
                ret.append(salida)
                indice_capa += 1
            return ret


        except Exception as e:
            print (e)


    def haciaAtras(self, salidas, salidas_esperadas, factor_aprendizaje, alfa):
        '''Ahora esta funcion recibe la salida que ha dado la funcion haciaAdelante y va hacia atras
            actualizando los pesos.
           Recibe también la lista de salidas esperadas para cada neurona de salida 0...n '''


        indice_capa = len(self.capas)-1 # Empezamos en la capa de salida

        erroresi = list() # Es una lista de errores de los nodos de la capa "siguiente"
        erroresj = list() # Es una lsita de errores de los nodos de la capa "actual"

        while indice_capa >= 0:
            
            # Vamos hacia atrás por capas
            
            if indice_capa == len(self.capas)-1: # CAPA DE SALIDA
                        # Aquí se entra sólo en la primera iteración (en la última capa)
                        # Llenamos la lista Erroresi con los errores de las neuronas de salida
                for indice_neurona in range(len(self.capas[indice_capa].neuronas)): # Hacia abajo por neuronas

                    salida_neurona = salidas[indice_capa][indice_neurona] # aj
                    error_neurona = salida_neurona * (1 - salida_neurona) * (salidas_esperadas[indice_neurona] - salida_neurona)

                    erroresi.append(error_neurona)

            else:

                # Aquí entramos en todas las demás capas

                # AQUI SE PEGARIA LO DE LOS PESOS UMBRALES
                # Es decir al principio de cada capa se actualizan todos los pesos umbrales
                # de la capa siguiente
                 
                for i in range(len(self.capas[indice_capa+1].neuronas)): # Aquí los umbrales de cada neurona en la capa proxima
                        incremento = factor_aprendizaje * -1 * erroresi[i] + alfa * (self.capas[indice_capa+1].neuronas[i].incrementos[0]) # <---- REVISAR
                        self.capas[indice_capa+1].neuronas[i].pesos[0] += incremento
                        self.capas[indice_capa+1].neuronas[i].incrementos[0] = incremento
           
                        
                for j in range(len(self.capas[indice_capa].neuronas)):
                    # Aquí iteramos sobre las neuronas de la capa ACTUAL
                                
                    aj = salidas[indice_capa][j] # aj, salida de esa neurona (se calculó en el haciaAdelante)
                    sumatorio = 0 # SUMATORIO Wji Error i

                    for i in range(len(self.capas[indice_capa+1].neuronas)): # Para el Sumatorio de los pesos

                        # Aquí iteramos sobre las neuronas de la capa POSTERIOR (ACTUAL+1)
                        # Para construir el sumatorio de los errores y los pesos multiplicadaos
                        # Hay que acceder en cada neurona[i] a su peso j+1
                        # Ya que en todas las neuronas el peso[0] lo considero el umbral
                                        
                        sumatorio += self.capas[indice_capa+1].neuronas[i].pesos[j+1] * erroresi[i] 

                        # Ahora en cada iteración sobre las neuronas de la capa ACTUAL
                        # Voy construyendo la lista de errores j
                                        
                    erroresj.append(aj * (1 - aj) * sumatorio)

                    # Ahora lo que nos queda es actualizar los pesos, ya que tenemos construido la lista de los
                    # errores de la capa actual y la próxima
                    
                    # Actualizamos primero los pesos umbrales (lo hago aparte pues no consideré el valor -1
                    # como parte de la lista de entradas (salidas de capa) al principio)
                    ########################## REVISAR SI EL MOMENTUM DE AQUI ESTA BIEN METIDO --- [11 Feb 2013] -> No esta bien j+1 => 0

                    # HAY QUE SACAR LO DE ABAJO Y METERLO ARRIBA
                    # SACADO [12 Feb 2013]
                        
                    # Ahora para actualizar todos los pesos que van desde la capa actual a la próxima
                    # Hay que acceder a las neuronas de la capa próxima e ir actualizando sus pesos
                    # Pues recuerdo que considero los pesos como entrantes a las neuronas

                    # El incremento que hay abajo se lo sumo pues estoy considerando momemtum a día de hoy (24 enero 2013)
                    
                    for i in range(len(self.capas[indice_capa+1].neuronas)): 
                        # Aquí todos los pesos ji 
                        incremento = factor_aprendizaje * aj * erroresi[i] + alfa * (self.capas[indice_capa+1].neuronas[i].incrementos[j+1])
                        self.capas[indice_capa+1].neuronas[i].pesos[j+1] += incremento
                        self.capas[indice_capa+1].neuronas[i].incrementos[j+1] = incremento


                erroresi = erroresj # Ahora como voy hacia atrás mi lista de errores ACTUAL pasa a ser la PROXIMA en la siguiente iteración
                erroresj = list() # Creo una nueva lista de erroresj que llenaré en la siguiente iteración

                
            indice_capa -= 1

    # Devuelvo el ajuste en el método de retroPropagacion
    
    def retroPropagacion(self, conjunto_entrenamiento, factor_aprendizaje, max_iteraciones, momentum, mejor_ajuste):
        # Aquí nos entra un mejor_ajuste
        # Que es el menor error cuadrático que se ha encontrado hasta la fecha, y un max_iteraciones, que se considera
        # el número máximo de iteraciones permitidas sin haber encontrado algo mejor (algo con menor error cuadrático)
        
        
        iteraciones_fallidas = 0
        mejor_red = self

        mejor_error = mejor_ajuste
        
        while(True):
            
            
            for i in range(len(conjunto_entrenamiento)):
                adelante = self.haciaAdelante(conjunto_entrenamiento[i][0])
                self.haciaAtras(adelante, conjunto_entrenamiento[i][1], factor_aprendizaje, momentum)

            # A partir de aquí la red está relativamente entrenada con respecto al conjunto de entrenamiento
            # Ahora medimos su error cuadrático

            errorc = self.ajuste(conjunto_entrenamiento)
            self.aj = errorc


            # Se muestra ya que no ralentiza demasiado
            
            print ("Error "+ str(errorc))
            print ("Iteraciones fallidas "+ str(iteraciones_fallidas) + "/" + str(max_iteraciones))
            print ("Mejor error: "+ str(mejor_error))
            
            
            if(errorc < mejor_error):
                mejor_error = errorc
                mejor_red = self # cargo la mejor red en la variable
                iteraciones_fallidas = 0
            else:
                iteraciones_fallidas += 1
                
            # Condiciones de parada de todas formas
            
            
            if(errorc < 0.05):  # Cota de error
                return mejor_red

            if(iteraciones_fallidas > max_iteraciones): # Si se pega n iteraciones sin superar el error
                return mejor_red


    def reglaDelta(self, conjunto_entrenamiento, num_iteraciones, factor_aprendizaje):
        ''' Comprobamos que la red es un perceptron '''

        try:

            if len(self.capas) > 2 or len(self.capas[1].neuronas) > 1:
                raise Exception('RED > REGLADELTA: Para entrenar con regla delta la red ha de ser un perceptrón')

        
            for _ in range(num_iteraciones):
                for i in range(len(conjunto_entrenamiento)):
                    salidas = self.haciaAdelante(conjunto_entrenamiento[i][0])
                    # Primero actualizamos el umbral
                    self.capas[1].neuronas[0].pesos[0] += factor_aprendizaje * ( conjunto_entrenamiento[i][1][0] - salidas[1][0] ) * salidas[1][0] * ( 1 - salidas[1][0] ) * -1
                    # Ahora el resto
                    for indice_peso in range(len(self.capas[1].neuronas[0].pesos)-1): # Solo hay una neurona de salida
                        self.capas[1].neuronas[0].pesos[indice_peso+1] += factor_aprendizaje * ( conjunto_entrenamiento[i][1][0] - salidas[1][0] ) * salidas[1][0] * ( 1 - salidas[1][0] ) * salidas[0][indice_peso]             
                    
        except Exception as e:
            print(e)
            
    # Error cuadrático
    # Dado un conjunto de entrenamiento, calcula el error cuadrático de la red
    
    def ajuste(self, conjunto_entrenamiento):

        errores = 0

        for c in conjunto_entrenamiento:
            salidas = self.haciaAdelante(c[0])
            for indice_salida in range(len(salidas[len(self.capas)-1])):
                errores += ((salidas[len(self.capas)-1][indice_salida] - c[1][indice_salida])**2)/2

        return errores
    
        
        

    # Esta es una función de debug que guarda los pesos a un fichero para
    # facilitar la legibilidad
    
    def guardarDatos(self, fichero):
        
        st = str(self)
        f = open(fichero, 'w')
        f.write(st)
        f.flush()
        f.close()

    def serializar(self, fichero):
        with open(fichero, 'wb') as f:

            pickle.dump(self, f)


    def __str__(self):

        string = "La red "+ self.nombre + " tiene " + str(len(self.capas)) + " capas:\n"

        for c in self.capas:
            string += "\t "+ str(c) + "\n"

        return string

# Funcion que des-serializa una red a partir de un fichero

def cargarRed(fichero):
        
        with open(fichero, 'rb') as f:
                red = pickle.load(f)
        return red

