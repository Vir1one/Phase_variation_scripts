"""
Parsear_SCOPE.py

Este programa permite formatear el resultado de SCOPE++ para obtener un CSV o TSV 
que contenga el inicio, final, la secuencia y el tipo de base de homopolímero
en base a los resultados del programa SCOPE++. 

Está pendiente agregar la opción de utilizar el programa con argumentos
de la linea de comandos y documentar en ingles. 

    ****************************************************************
    *   Autor: David Saiz Martinez                                 *
    *   Version 1.0                                                *
    *   Fecha: 15/12/2021                                          *
    ****************************************************************
"""
import os
import re


#Seleccionar el directorio
dir = "./Directorio_archivos_SCOPE/"
archivos = os.listdir(dir)
sams_dir = "./SAMS/"

#Procesas los archivos que sean de SCOPE
parsear = []
for file in archivos:
    if file.endswith(".poly") and not file.startswith("._"):
        parsear.append(file)

#Crear directorio de resultados
outdir = os.mkdir('./Directorio_resultados/')
file_type = "csv"

#Seleccionar separador en funcion del tipo de fichero
if file_type.upper() == "TSV":
    sep = "\t"

else:
    sep = ";"

#Resultados
for resultado in parsear:
    print("Procesando:", resultado)
    nombre = resultado[0:-5] #Eliminar la extension

    #Tipos de archivos. El fichero SAM y archivo de SCOPE han de tener el mismo nombre
    Scope_file = dir + resultado
    Sam_file = sams_dir + nombre + ".sam"
    output_file = outdir + nombre + "." + file_type

    with open (Scope_file, "r") as f:
        # Abir SAM
        sam = open(Sam_file, "r")
        contenido = sam.read()

        #Abrir output
        outdir = open (output_file, "w")
        outdir.write("Inicio" + sep + "Fin" + sep +  "secuencia" + sep + "Base" + "\n")
        
        for line in f:
            try:
                if line.startswith("@"):
                    a = line.split("(")

                    #Informacion de la read
                    read_info = a[0]
                    read = read_info.split(" ")[0][1:]
                    #print(read)
                    sentido = read_info.split(" ")[1][0] #Forward o revers (1 o 2)

                    #Informacion de los homopolymeros
                    datos = a[1].split(",")
                    base = datos[0][-1]
                    m = re.search("[0-9]+", datos[1])
                    inicio = int(m.group(0))
                    #print(1, m.group(0))

                    m2 = re.search("[0-9]+", datos[2])
                    fin = int(m2.group(0))
                    #print(base, inicio)

                    #Busqueda de la read en el fichero SAM
                    patron = read+ ".+"
                    z = re.finditer(patron, contenido)

                    for num, match in enumerate(z):
                        if num == int(sentido) - 1: #Si es forward es la primera ocurrencia, si es revers la segunda
                            info_sam = match.group().split("\t")
                            break

                    posicion_genoma = int(info_sam[3]) #Lugar de mapeo de la read
                    
                #Evitar que busque en las lineas que no toca
                elif not re.search("[\+H]",line.upper()):
                    secuencia = line[int(inicio)-1:int(fin)] #Extrer la secuencia de homopolimeros
                    outdir.write(str(inicio+posicion_genoma) + sep + str(fin+posicion_genoma) + sep + secuencia + sep + base + "\n")

            except:
                print("Error en read:", line)

                



