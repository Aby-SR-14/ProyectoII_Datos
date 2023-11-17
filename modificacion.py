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
    def retornar_dato(self, key):
        if key in self.tablahash_dato:
            tipo = self.tablahash_dato[key]["Tipo"]
            valor = self.tablahash_dato[key]["Valor"]
            identificador=key
            dato = Dato(valor,tipo,identificador)
            return dato
        else:
            return None
    def verificar_valor_valido(self, dato, palabra_actual):
        if dato.get_tipoDato() == self.tablahash_dato[dato.get_identificador()]["Tipo"]:
            if self.tablahash_dato[dato.get_identificador()]["Tipo"] == "int":
                try:
                    entero = int(palabra_actual)
                    self.tablahash_dato[dato.get_identificador()]["Valor"]={entero}
                    return 1
                except ValueError:
                    print("ERROR")
                    return -1
            elif self.tablahash_dato[dato.get_identificador()]["Tipo"] == "string":
                    try:
                        if isinstance(palabra_actual,str):
                            dato.set_valor(palabra_actual)
                            self.tablahash_dato[dato.get_identificador()]["Valor"]={palabra_actual}
                            return 1
                    except ValueError:
                        print ("No es un string")
                        return -1
            elif self.tablahash_dato[dato.get_identificador()]["Tipo"] == "float":
                    try:
                            # Intenta convertir la cadena a un número de punto flotante
                        flotante = float(palabra_actual)
                        self.tablahash_dato[dato.get_identificador()]["Valor"]={flotante}
                        return 1
                    except ValueError:
                        print("ERROR FLOAT")
                        return -1
        return -1
    def agregar_dato(self, dato):
        if dato.get_tipoDato() == 'int':
            dato.set_valor(0)
            analisis.tablahash_dato[dato.get_identificador()]={"Tipo":dato.get_tipoDato(), "Valor":dato.get_valor()}
            return 1
        elif dato.get_tipoDato() == "string":
            dato.set_valor("")
            analisis.tablahash_dato[dato.get_identificador()]={"Tipo":dato.get_tipoDato(), "Valor":dato.get_valor()}
            return 1
        elif dato.get_tipoDato() == "float":
            dato.set_valor(0.0)
            analisis.tablahash_dato[dato.get_identificador()]={"Tipo":dato.get_tipoDato(), "Valor":dato.get_valor()}
            return 1
        elif dato.get_tipoDato() == "void" or "while" or "if":
            dato.set_valor("")
            dato.set_parametros("")
            return 1
        return -1

contador = 0
analisis = Analisador()
#analisis.leer_codigo()
valor = False
creando_parametro=False
creando_dato=True
dato=Dato(0,"","")
parametro = Dato(0,"","")
i=0
bandera = True
guardarDato = {}
tipos={"tipo":["int", "string", "float","void"],"cuerpo":["while", "if"]}
with open("numero.txt") as archivo:
            #Lectura por linea
            for linea in archivo:
                #contador de la linea para indicar un error
                contador += 1
                #Split almacena todas las palabras separadas por un espacio, tab o endline
                #La idea es ir recorriendo el vector e ir verificando las variables y funciones
                palabras = linea.split()
                i=0
                #iteramos según la cantidad de palabras almacenadas
                while i in range(len (palabras)):
                    palabra_actual = palabras[i]
                    if analisis.dato_almacenado(palabra_actual) > 0 :
                        #Si es un dato almacenado hay que setear el dato por si se llega a actualizar el valor de la variable
                        if creando_parametro :
                            #No creo que sea necesario pero por si acaso
                            parametro= analisis.retornar_dato(palabra_actual)
                        elif creando_dato:
                            dato= analisis.retornar_dato(palabra_actual)
                            i+=1
                    elif analisis.verificar_dato(palabra_actual) > 0:
                        if creando_parametro:
                            parametro.set_tipoDato(palabra_actual)
                            i=+1                            
                        elif creando_dato:
                            dato.set_tipoDato(palabra_actual)
                            i=+1
                    elif palabra_actual is "=":
                        #Si es = es porque se le asigna un valor a la variable, para eso la bandera
                        i+=1
                        valor = True
                    elif palabra_actual is not "=" and valor is False and analisis.verificar_dato(palabra_actual)< 0 and palabra_actual[0] != '(':
                        #Si no es una asignacion y la bandera de valor es false, es porque es el nombre de la variable o funcion
                        #No siempre se le asigna un valor al dato, como en los parametros
                        #Por lo que es mejor colocarle un valor y guardarlo
                        if creando_parametro:
                            #Si es un único parametro empieza y termina con(), si son varios el nombre(identificador)
                            #termina en , por lo que hay que borrarla, si es ) crear_parametro = false
                            #si es , crear_parametro = true, PERO es un nuevo parametro por lo que hay que eliminar el actual
                            #Para que no hayan errores o se modifique el parametro pasado
                            if palabra_actual [len(palabra_actual)-1] == ')' or ',':
                                palabra_actual = palabra_actual[:-1]
                                parametro.set_identificador(palabra_actual)
                                if(analisis.agregar_dato(parametro)> 0):
                                    i+=1
                        elif creando_dato:
                            dato.set_identificador(palabra_actual)
                            if(analisis.agregar_dato(dato)> 0):
                                i+=1
                        
                        else:
                            print("No se ha agregado el dato a la tabla")
                    elif valor is True and analisis.verificar_dato(palabra_actual)<0:
                        if creando_parametro:
                            if analisis.verificar_valor_valido(parametro, palabra_actual)>0:
                                valor = False
                                i+=1
                        elif creando_dato:
                            if analisis.verificar_valor_valido(dato, palabra_actual)>0:
                                valor = False
                                i+=1
                        else:
                            print("Error en la linea {}, el valor no coincide con el tipo de la variable".format(contador))
                            valor = False
                    #funcion
                    elif palabra_actual[0] =="(":
                    #parametros
                        creando_parametro=True
                        #slicing es para eliminar el primer caracter ya que tiene "(" 
                        palabra_actual = palabra_actual[1:]
                        if analisis.verificar_dato(palabra_actual) > 0:
                            parametro.set_tipoDato(palabra_actual)
                        i+=1
