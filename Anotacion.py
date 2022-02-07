"""
Anotacion.py

Este programa permite anotar las regiones de homopolymeros o STR con el
formato obtendi por los programas Parseas_Mreps y Parsear_Scope y el 
fichero de notación de Virclust. 

Está pendiente agregar la opción de utilizar el programa con argumentos
de la linea de comandos y documentar en ingles. 

    ****************************************************************
    *   Autor: David Saiz Martinez                                 *
    *   Version 1.0                                                *
    *   Fecha: 23/01/2021                                          *
    ****************************************************************
"""
import os

#Directorios
dir_anot = "./VirClust/"
dir_in = "./Directorio_resultados_repeticiones/"
directorio = os.listdir(dir_anot)

#Selecionar solo los archivos de anotacion
Annot_file = []
for archivo in directorio:
    if archivo.endswith("virclust_.tsv") and not archivo.startswith("._"):
        Annot_file.append(archivo)

#Opiciones resultados
outdir = "./Anotados/"
file_type = "csv"

#Seleccionar separador en funcion del tipo de fichero
if file_type.upper() == "TSV":
    sep = "\t"

else:
    sep = ";"

#Resultados
for fago in Annot_file:
    #Obtener la informacion de anotacion
    anot_file = dir_anot + fago
    inicios = []
    finales = []
    prot_names = []
    prot_anot = []
    prot_class =[]
    with open (anot_file, "r") as f:
        for line in f:
            a = line.split("\t")
            prot_id= a[7]
            if prot_id not in prot_names:

                #Inicios y finales
                inicios.append(int(a[2]))
                finales.append(int(a[3]))

                #Nombre de la proteina y su anotacion
                prot_names.append(a[7]) #Protein id
                prot_anot.append(a[28]) #Tipo de proteina
                prot_class.append(a[29]) #Categoria funcional

    #Fichero de resultados)
    salida = open(outdir + fago[0:-4] + "." + file_type, "w")

    resumen_file = dir_in + fago[0:-4] + "." + file_type
    with open (resumen_file, "r") as f2:
        cabecera = f2.readline()
        salida.write(cabecera[0:-1] + sep + "Protein_id" + sep + "PHROGS_annot" + sep + "PHROGS_functional_category" + sep +"CrossGen" + sep + "PHROGS_annot2" + sep + "PHROGS_functional_category2" + sep +  "PHROGS_annot3" + sep + "PHROGS_functional_category3" +"\n")
        for line in f2:
            b = line.split(sep)
            start = int(b[0])
            end = int(b[1])

            for i, menor in enumerate(inicios):
                #Si el final de la repeticion acaba antes del primer gen o el principio de la repeticion enpieza después del ultimo gen, es terminal
                if end < inicios[0] or start > finales[-1]:  
                    salida.write(line[0:-1] + sep + "Terminal" + sep + "Terminal" +"\n")
                    break
                
                else:
                    try:
                        #Si la repeticion empieza dentro de un gen 
                        if start >= inicios[i] and start < inicios[i+1]:
                            #Si acaba en ese mismo gen, se clasifica como tal
                            if end <= finales[i]:
                                salida.write(line[0:-1] + sep + prot_names[i] + sep + prot_anot[i] + sep + prot_class[i] +"\n")
                            #Si empieza despues del final del gen y acaba antes que del inicio del siguiente
                            elif start > finales[i] and end < inicios[i+1]:
                                salida.write(line[0:-1] + sep + " " + sep + "Intergenico" + sep + "Intergenico"+"\n")

                            else:
                                try:
                                    #Si empieza en un gen pero acaba fuera, se considera parte de ese gen
                                    if end <= inicios[i+1]:
                                        salida.write(line[0:-1] + sep +prot_names[i] + sep + prot_anot[i] + sep + prot_class[i] + sep +"OUT" +"\n")
                                    
                                    #Si acaba dentro del siguiente gen se consideran ambos genes
                                    elif end <= finales[i+1]:
                                        salida.write(line[0:-1] + sep + prot_names[i] + sep + prot_anot[i] + sep + prot_class[i] + sep +" " + sep + prot_anot[i+1] + sep + prot_class[i+1]+"\n")
                                    
                                    #Si acaba dentro del siguiente gen se consideran ambos genes. En este caso acaba fuera del gen. 
                                    elif end <= inicios[i+2]:
                                        salida.write(line[0:-1] + sep + prot_names[i] + sep +prot_anot[i] + sep + prot_class[i] + sep +"OUT" + sep + prot_anot[i+1] + sep + prot_class[i+1]+"\n")

                                    #Si llega a un tercer gen (cosa dificil por la longitud de las secuencias), se consideran los 3 genes
                                    elif end <= finales[i+2]:
                                        salida.write(line[0:-1] + sep + prot_names[i] + sep + prot_anot[i] + sep + prot_class[i] + sep +"OUT" + sep + prot_anot[i+1] + sep + prot_class[i+1] + sep + prot_anot[i+2] + sep + prot_class[i+2]+"\n")

                                    #Cubre en caso de que no se haya contenplado alguna posibilidad (no debería aparecer en el resultado)
                                    else:
                                        salida.write(line[0:-1] + sep + " "[i] + sep + "NO-ANOTADO" + sep + "NO-ANOTADO"+"\n")

                                except:
                                    #Cubre en caso de sucecer un error con esa repeticion (no debería aparecer en el resultado)
                                    salida.write(line[0:-1] + sep + "NO-ANOTADO" + sep + "NO-ANOTADO"+"\n")  
                                    pass

                    except:
                        #Cuenta los terminales que se intentan comparar con el ultimo +1 elemento de la lista y producen out of range
                        salida.write(line[0:-1] + sep + " " + sep + "Terminal" + sep + "Terminal"+"\n")
    

