"""
Parsear_Mreps.py

Este programa formatear el resultado de Mreps para obtener un CSV o TSV 
que contenga el inicio, final, y secuencia de las Short Tandem Repeats
encontradas por el programa. 

Está pendiente agregar la opción de utilizar el programa con argumentos
de la linea de comandos y documentar en ingles. 

    ****************************************************************
    *   Autor: David Saiz Martinez                                 *
    *   Version 1.0                                                *
    *   Fecha: 12/12/2021                                          *
    ****************************************************************
"""
import os
import re
import sys

#Seleccionar el directorio
dir = "./Directorio_archivos_Mreps/"
archivos = os.listdir(dir)

#Procesas los archivos que sean de Mreps
parsear = []
for file in archivos:
    if file.endswith("_mreps.txt") and not file.startswith("._"):
        parsear.append(file)

#Crear directorio de resultados
outdir = os.mkdir('./Directorio_resultados/')
file_type = "csv"

#Seleccionar separador en funcion del tipo de fichero
if file_type.upper() == "TSV":
    sep = "\t"

else:
    sep = ";"

#Obtener resultados
for mreps in parsear:
    #Archivo de salida
    outfile = outdir + mreps[0:-4] + "." + file_type.lower()

    with open (dir + mreps, "r") as f:
        lista_resultados = []
        for line in f:
            if re.match(" *[0-9]", line):
                a = line.split("\t")
                b = a[0].split("->")

                inicio = b[0].strip()
                fin = b[1].strip()[0:-2]
                secuencia = a[-1].replace(" ", "")[0:-2]
                
                lista_resultados.append((inicio,fin,secuencia))

    #Escribir los resultados en el archivo de salida       
    fichiero = open(outfile, "w")
    fichiero.write("Inicio" + sep + "Final" + sep + "Secuencia" + sep + "Base" + "\n")

    for i in lista_resultados:
        fichiero.write(i[0] + sep + i[1] + sep + i[2] + sep + "-" +"\n")

    #Cerrar archivo
    fichiero.close()



