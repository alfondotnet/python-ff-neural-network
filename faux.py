import red
import fnmatch
import os

proporcion = 1000

# Funciones auxiliares que se usan en más de un sitio

def obtenerConjunto(fichero):

    f = open(fichero,"rb")

    pixels_string = str(f.read()).strip("'") # Quitamos unas comillitas
    pixels_string = pixels_string.replace("\\n","") # Quitamos los \n
    pixels_string = pixels_string[12:len(pixels_string)-1] # Quitamos el header 
    pixels = pixels_string.split(" ") # Hallamos la lista de pixeles

    for i in range(len(pixels)):
        pixels[i] = int(pixels[i]) / int(proporcion) # Esto lo hacemos para evitar que redondee
        # demasiado nuestra función pre-sigmoide que evitaba el math range error
    
    return pixels

def comprobar(nombre, foto, tipo, clasificaciones, humano=True):
    
    r = red.cargarRed("redes/"+tipo+"/"+nombre)
    entradas = obtenerConjunto("test/"+tipo+"/"+foto)
   
    hd = r.haciaAdelante(entradas)

    # Debug
    #f = open("redes/"+tipo+"/"+foto+".txt", "w")
    #f.write(str(hd))
    #f.flush()
    #f.close()
    
    #r.guardarDatos("redes/"+tipo+"/red_posturas_datos.txt")
    
    
    if humano == True:
        return clasificar(hd[-1], clasificaciones)
    else:
        return hd[-1]


def clasific_regexp(tipo):
    
    if tipo == "posturas":
        return ["*-arriba-*","*-frente-*","*-abajo-*"]
    elif tipo == "gestos":
        return ["*frente*sonriendo*","*frente*serio*","*frente*lengua*'"]
    elif tipo == "ojos":
        return ["*frente*abiertos*","*frente*cerrados*","*frente*gafas*"]
    elif tipo == "personas":
        return ["fon*frente*","papa*frente*","mama*frente*"]
    
def clasificaciones(tipo):
    
    if tipo == "posturas":
        return ["arriba","frente","abajo"]
    elif tipo == "gestos":
        return ["sonriendo","serio","lengua"]
    elif tipo == "ojos":
        return ["abiertos","cerrados","gafas"]
    elif tipo == "personas":
        return ["fon","papa","mama"]   


def conjunto(tipo):
    
    conjunto_entrenamiento = list()

    clasificaciones_regexp = clasific_regexp(tipo)
        
    # FRENTE: [0,1,0]
    for f in os.listdir('fotos'):
        if fnmatch.fnmatch(f, clasificaciones_regexp[0]):
            pix = obtenerConjunto("fotos/"+f)
            conjunto_entrenamiento.append((pix,[1,0,0]))

    # ARRIBA: [1,0,0]
    for f in os.listdir('fotos'):
        if fnmatch.fnmatch(f, clasificaciones_regexp[1]):
            pix = obtenerConjunto("fotos/"+f)
            conjunto_entrenamiento.append((pix,[0,1,0]))

    # ABAJO: [0,0,1]
    for f in os.listdir('fotos'):
        if fnmatch.fnmatch(f, clasificaciones_regexp[2]):
            pix = obtenerConjunto("fotos/"+f)
            conjunto_entrenamiento.append((pix,[0,0,1]))
            
    return conjunto_entrenamiento


def obtenerMejorRed(tipo):
    mejor_acierto = 0
    for f in os.listdir('redes/'+tipo):
        # Para cada red f
        aciertos = 0
        num_test = 0
        for m in os.listdir('test/'+tipo):
            clasificacion = comprobar(f, m, tipo, clasificaciones(tipo), True)
            if fnmatch.fnmatch(m, "*"+clasificacion+"*"):
                aciertos += 1
            num_test += 1
        if aciertos > mejor_acierto:
            mejor_acierto = aciertos
            mejor_red = f
            
    return (mejor_red,str(mejor_acierto) + "/" + str(num_test))

def clasificar(lista, clasificaciones):

    return clasificaciones[lista.index(max(lista))]



    

