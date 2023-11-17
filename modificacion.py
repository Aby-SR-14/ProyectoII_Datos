from typing import List
from collections import defaultdict
from dato import Dato
class Analisador:
    def __init__(self):
        self.tablahash_dato = {}
        self.tipos={"tipo":["int", "string", "float","void"],"cuerpo":["while", "if"]}
        self.numero_linea=0

    def es_numero(self,valor):
        if valor.isdigit():
            return int(valor)
        else: return 0
    
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
            dato.set_tipoDato(palabra_actual)
            return 1
        elif palabra_actual in self.tipos["cuerpo"]:
            print ("cuerpo")
            dato.set_tipoDato(palabra_actual)   
            return 2 
        else: return -1 
    def dato_almacenado (self, key):
        if key in self.tablahash_dato:
            return 1
        else:
            return 0
    def editar_valor(self, key, valor):
        if self.dato_almacenado(key) >0:
            self.tablahash_dato[key]={valor}
            return 1
        else:
            return -1



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
                if palabra_actual in analisis.tablahash_dato :
                    print("Es un dato guardado")
                    i+=1
                elif analisis.verificar_dato(palabra_actual) > 0:
                    dato.set_tipoDato(palabra_actual)
                    i=+1
                elif palabra_actual is "=":
                     i+=1
                     valor = True
                elif palabra_actual is not "=" and valor is False:
                    #Si no es una asignacion y la bandera de valor es false, es porque es el nombre de la variable o funcion
                    #No siempre se le asigna un valor al dato, como en los parametros
                    #Por lo que es mejor colocarle un valor y guardarlo
                    dato.set_identificador(palabra_actual)
                    if dato.get_tipoDato() == 'int':
                        dato.set_valor(0)
                        analisis.tablahash_dato[dato.identificador]:{dato.get_valor}
                        i+=1
                    elif dato.get_tipoDato() == "string":
                        dato.set_valor("")
                        analisis.tablahash_dato[dato.identificador]:{dato.get_valor}
                        i+=1
                    elif dato.get_tipoDato() == "float":
                        dato.set_valor(0.0)
                        analisis.tablahash_dato[dato.identificador]:{dato.get_valor}
                        i+=1
                    elif dato.get_tipoDato() == "void" or "while" or "if":
                        dato.set_valor("")
                        dato.set_parametros("")
                        i+=1       
                elif valor is True:
                    if dato.get_tipoDato() == 'int':
                        try:
                            entero = int(palabra_actual)
                            dato.set_valor(entero)
                            i+=1
                        except ValueError:
                            print("ERROR")
                    elif dato.get_tipoDato() == "string":
                        try:
                            if isinstance(palabra_actual,str):
                                dato.set_valor(palabra_actual)
                                i+=1
                        except ValueError:
                            print ("No es un string")
                    elif dato.get_tipoDato() == "float":
                        try:
                        # Intenta convertir la cadena a un número de punto flotante
                            flotante = float(palabra_actual)
                            dato.set_valor(palabra_actual)
                            i+=1
                        except ValueError:
                            print("ERROR FLOAT")

                    