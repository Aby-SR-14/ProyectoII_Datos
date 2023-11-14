

from typing import List
from collections import defaultdict
from dato import Dato

class Compilador:
    def __init__(self):
        self.tablahash_dato = {}
        self.dato_key = []
        self.parametros = []
        self.numero_linea = 0


    def verifica_llave(dato, dato_key):
        for v in dato_key:
            if dato.get_identificador() == v:
                return True
        return False

    def es_numero(valor):
        if valor[0] == '"':
            return False

        for char in valor:
            if char.isalpha():
                return False

        return True

    def es_funcion(valor):
        if valor[0] == '(':
            return True

        return False

    def busca_elemento_hash(self, key):
        for registro in self.tablahash_dato.items():
            if registro[1].get_identificador() == key:
                return registro[1]

    def verifica_return(self, ret, nombre_funcion):
        flag_ret = False
        flag_fun = False

        for key in self.dato_key:
            if key == ret:
                flag_ret = True

            if key == nombre_funcion:
                flag_fun = True

        if flag_fun and flag_ret:
            if self.tablahash_dato[ret].get_tipo_dato() == self.tablahash_dato[nombre_funcion].get_tipo_dato():
                return True

        return False
    
    def text_reader(self):
        nombre_funcion = ""
        palabra = ""
        palabra2 = ""
        contador = 0
        bandera = 0 
        bandera2 = False
        contador_llaves = 0
        compilacion_correcta = 0



        nombre = ""
        tipo = ""
        valor = ""
        tipo_p = ""
        id_p = ""

        with open("codigos.txt") as entrada:
            while bandera == 0:
                linea = entrada.readline()
                contador += 1
                numero_linea = contador

                if not linea:
                    break  

                palabras = linea.split()

                for palabra in palabras:
                    if palabra != palabra2:
                        if palabra == "{":
                            contador_llaves += 1
                        if palabra == "}":
                            contador_llaves -= 1

                        if palabra != "=":
                            if palabra in ["int", "void", "float", "string"] and tipo == "":
                                tipo = palabra
                            else:
                                if nombre == "" and palabra[0].isalpha():
                                    nombre = palabra
                                    if nombre[-1] == ";":
                                        nombre = nombre[:-1] 

                                    if palabra[-1] == ";":
                                        palabra = palabra[:-1] 

                                if nombre != palabra:
                                    if nombre != "":
                                        if nombre == "return":
                                            palabra = palabra[:-1]
                                            if not Dato.verifica_return(palabra, nombre_funcion):
                                                print(
                                                    f"Error-- la variable de retorno no es correcta conforme a la declaracion de la funcion '{nombre_funcion}'"
                                                )
                                                compilacion_correcta += 1

                                        if tipo_p == "":
                                            tipo_p = palabra
                                            if tipo_p[0] == "(":
                                                tipo_p = tipo_p[1:]

                                        else:
                                            id_p = palabra
                                            if id_p[-1] == ")" or id_p[-1] == ",":
                                                id_p = id_p[:-1]

                                        valor = palabra
                                        if self.es_funcion(valor):
                                            bandera2 = True

                                        if bandera2:
                                            if id_p != "" and tipo_p != "":
                                                funcion = Dato(tipo_p, id_p, "")
                                                if self.valor_tipo_correcto(funcion):
                                                    self.parametros.append(funcion)
                                                else:
                                                    compilacion_correcta += 1
                                                tipo_p = ""
                                                id_p = ""

                                        else:
                                            if valor[-1] == ";":
                                                valor = valor[:-1]
                                            break

                                    palabra2 = palabra
                                    bandera2 = False
                                    palabra = ""
                                    palabra2 = ""
                                    tipo_p = ""
                                    id_p = ""

                if not self.parametros:
                    ele = Dato(tipo, nombre, valor)
                    if not self.valor_tipo_correcto(ele):
                        print("NO compila....")
                        compilacion_correcta += 1

                else:
                    funcion = Dato(tipo, nombre, self.parametros.copy())
                    nombre_funcion = nombre
                    self.dato_key.append(nombre)
                    key = nombre
                    registro = {key: funcion}
                    self.tablahash_dato.update(registro)
                    self.parametros.clear()

                nombre = ""
                tipo = ""
                valor = ""

        if contador_llaves > 0:
            print("Error-- se esperaba '}'")

        if contador_llaves < 0:
            print("Error-- se esperaba '{'")

        if compilacion_correcta == 0:
            print("Compilacion exitosa")
