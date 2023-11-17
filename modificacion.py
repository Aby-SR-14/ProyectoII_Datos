from typing import List
from collections import defaultdict
from dato import Dato
class Analisador:
    def __init__(self):
        self.tablahash_dato = {}
        self.tipos={"tipo":["int", "string", "float","void"],"cuerpo":["while", "if"]}
        self.numero_linea=0
    
    def leer_codigo(self):
        with open("numero.txt") as archivo:
            contenido = archivo.read()
            palabras = contenido.split()
            for i in range(len (palabras)):
                palabra_actual = palabras[i]
                if palabra_actual in self.tipo[palabra_actual]:
                    self.tipo[palabra_actual]
                    self.tipo[palabra_actual] = palabras[i+1]

        print("Diccionario de datos recolectados", self.tablahash_dato)
                    
    def verificar_dato(self, palabra_actual):
        if palabra_actual in self.tipos["tipo"]:
            print("tipo de dato")
            return 1
        elif palabra_actual in self.tipos["cuerpo"]:
            print ("cuerpo")  
            return 2 
        else: return -1 
    def dato_almacenado (self, key):
        if key in self.tablahash_dato:
            return 1
        else:
            return 0
    def retornar_valor(self, key, dato):
        if key in self.tablahash_dato:
            dato.set_tipo(self.tablahash_dato[key]["Tipo"])
            dato.set_valor(self.tablahash_dato[key]["Valor"])
            dato.set_identificador(key)
            return dato
        else:
            return None
    def verificar_valor_valido(self, dato, palabra_actual):
        if dato.get_tipoDato() == self.tablahash_dato[dato.get_identificador()]["Tipo"]:
            if self.tablahash_dato[dato.get_identificador()]["Tipo"] == "int":
                try:
                    entero = int(palabra_actual)
                    self.tablahash_dato[dato.get_identificador()]["Tipo"]={entero}
                    return 1
                except ValueError:
                    print("ERROR")
                    return -1
            elif self.tablahash_dato[dato.get_identificador()]["Tipo"] == "string":
                    try:
                        if isinstance(palabra_actual,str):
                            dato.set_valor(palabra_actual)
                            self.tablahash_dato[dato.get_identificador()]["Tipo"]={palabra_actual}
                            return 1
                    except ValueError:
                        print ("No es un string")
                        return -1
            elif self.tablahash_dato[dato.get_identificador()]["Tipo"] == "float":
                    try:
                            # Intenta convertir la cadena a un número de punto flotante
                        flotante = float(palabra_actual)
                        self.tablahash_dato[dato.get_identificador()]["Tipo"]={flotante}
                        return 1
                    except ValueError:
                        print("ERROR FLOAT")
                        return -1
        return -1

contador = 0
analisis = Analisador()
#analisis.leer_codigo()
valor = False
dato=Dato(0,"","")
i=0
bandera = True
guardarDato = {}
tipos={"tipo":["int", "string", "float","void"],"cuerpo":["while", "if"]}
with open("numero.txt") as archivo:
            contenido = archivo.read()
            #Split almacena todas las palabras separadas por un espacio, tab o endline
            #La idea es ir recorriendo el vector e ir verificando las variables y funciones
            palabras = contenido.split()
            #iteramos según la cantidad de palabras almacenadas
            while i in range(len (palabras)):
                palabra_actual = palabras[i]
                if analisis.dato_almacenado(palabra_actual) > 0 :
                    #Si es un dato almacenado hay que setear el dato por si se llega a actualizar el valor de la variable
                    dato.set_identificador(palabra_actual)
                    dato= dato(analisis.retornar_valor(palabra_actual) )
                    i+=1
                elif analisis.verificar_dato(palabra_actual) > 0:
                    dato.set_tipoDato(palabra_actual)
                    i=+1
                elif palabra_actual is "=":
                     #Si es = es porque se le asigna un valor a la variable, para eso la bandera
                     i+=1
                     valor = True
                elif palabra_actual is not "=" and valor is False:
                    #Si no es una asignacion y la bandera de valor es false, es porque es el nombre de la variable o funcion
                    #No siempre se le asigna un valor al dato, como en los parametros
                    #Por lo que es mejor colocarle un valor y guardarlo
                    dato.set_identificador(palabra_actual)
                    if dato.get_tipoDato() == 'int':
                        dato.set_valor(0)
                        analisis.tablahash_dato[dato.get_identificador()]={"Tipo":dato.get_tipoDato(), "Valor":dato.get_valor()}
                        i+=1
                    elif dato.get_tipoDato() == "string":
                        dato.set_valor("")
                        analisis.tablahash_dato[dato.get_identificador()]={"Tipo":dato.get_tipoDato(), "Valor":dato.get_valor()}
                        i+=1
                    elif dato.get_tipoDato() == "float":
                        dato.set_valor(0.0)
                        analisis.tablahash_dato[dato.get_identificador()]={"Tipo":dato.get_tipoDato(), "Valor":dato.get_valor()}
                        i+=1
                    elif dato.get_tipoDato() == "void" or "while" or "if":
                        dato.set_valor("")
                        dato.set_parametros("")
                        i+=1       
                elif valor is True and analisis.verificar_dato(palabra_actual)<0:
                    if analisis.verificar_valor_valido(dato, palabra_actual)>0:
                        valor = false
                        i+=1
                    else:
                        print("Error en la linea {}, el valor no coincide con el tipo de la variable".format(contador))

                    