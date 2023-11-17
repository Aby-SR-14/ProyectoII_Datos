from typing import List
from collections import defaultdict
from dato import Dato

class Compilador:
    def __init__(self):
        self.tablahash_dato = {}
        self.dato_key = []
        self.parametros = []
        self.numero_linea = 0


    def verifica_llave(self,dato):
        for v in self.dato_key:
            if dato.get_identificador() == v:
                return True
        return False

    def es_numero(self,valor):
        if valor[0] == '"':
            return False

        for char in valor:
            if char.isalpha():
                return False

        return True

    def es_funcion(self,valor):
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
                                                if self.valorTipoCorrecto(funcion):
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
                    if not self.valorTipoCorrecto(ele):
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


    def valorTipoCorrecto(self,elemento):
       
        if (elemento.get_tipoDato() == "" and elemento.get_identificador() == "" and elemento.get_valor() == "") or \
            elemento.get_identificador() == "return" or elemento.get_tipoDato() == "void" or \
            (elemento.get_identificador()[0] == 'i' and elemento.get_identificador()[1] == 'f') or \
            (elemento.get_identificador()[0] == 'w' and elemento.get_identificador()[1] == 'h'):
            return True

        if elemento.get_identificador() != "":
            if elemento.get_tipoDato() == "": # no tiene tipo de dato
                if self.verificaLlave(elemento): # existe la llave
                    if self.esNumero(elemento.getValor()): # es número y es acorde
                        key = elemento.get_identificador() # Ej: x=5;
                        ele = self.buscaElementoHash(key)

                        if ele.get_tipoDato() == "int" or ele.get_tipoDato() == "float":
                            elemento.set_tipoDato(ele.getTipoDato())
                            self.hashtableElemento.pop(key)
                            registro = (key, elemento)
                            self.hashtableElemento.append(registro)
                            self.keyElemento.append(ele.getIdentificador())
                            return True
                        else:
                            print(f"Error-- Linea {self.numLinea}: el identificador '{elemento.get_identificador()}' no coincide con el valor de asignación.")
                            return False
                    else: # llave declarada y sin tipo de dato
                        key = elemento.get_identificador # Ej: x=5;
                        ele = self.buscaElementoHash(key)

                        if elemento.get_Valor()[0] == '"' and elemento.getValor()[-1] == '"' and ele.get_tipoDato() == "string":
                            # es cadena y es acorde
                            key = elemento.get_identificador
                            ele = self.buscaElementoHash(key)
                            elemento.set_tipoDato(ele.getTipoDato()) # Ej: cadena = "hola";
                            self.hashtableElemento.pop(key)
                            registro = (key, elemento)
                            self.hashtableElemento.append(registro)
                            self.keyElemento.append(elemento.getIdentificador())
                            return True
                        else:
                            print(f"Error-- Linea {self.numLinea}: el identificador '{elemento.get_identificador()}' no coincide con el valor de asignación.")
                            return False
                else:
                    print(f"Error-- Linea {self.numLinea}: '{elemento.get_identificador()}' no está declarado.")
                    return False
            else: # Tiene tipo de dato
                if self.verifica_llave(elemento): # Si existe
                    print(f"Error-- Linea {self.numLinea}: doble declaración de variable.")
                    return False # doble declaración, mal hecho
                    # int x;
                    # int x; || string x;
                else: # No existe la key
                    if elemento.get_valor() == "": # No tiene valor
                        key = elemento.get_identificador()
                        registro = (key, elemento)
                        self.hashtableElemento.append(registro)
                        self.keyElemento.append(elemento.get_identificador())
                        return True
                    else: # Si tiene valor
                        if self.es_numero(elemento.get_valor()) and (elemento.get_tipoDato() == "int" or elemento.get_tipoDato() == "float"):
                            # es número y es acorde
                            # int x = 5;
                            key = elemento.get_identificador()

                            # ele = buscaElementoHash(key)
                            # elemento.setTipoDato(ele.getTipoDato())

                            self.hashtableElemento.pop(key)
                            registro = (key, elemento)
                            self.hashtableElemento.append(registro)
                            self.keyElemento.append(elemento.get_identificador())
                            return True
                        else:
                            if elemento.get_valor()[0] == '"' and elemento.get_valor()[-1] == '"' and elemento.get_tipoDato() == "string":
                                # declaración y definición correcta
                                key = elemento.get_identificador()
                                ele = self.buscaElementoHash(key)
                                elemento.set_tipoDato(ele.getTipoDato())

                                self.hashtableElemento.pop(key) # Ej: string cadena = "hola";
                                registro = (key, elemento)
                                self.hashtableElemento.append(registro)
                                self.keyElemento.append(elemento.get_identificador())
                                return True
                            else:
                                print(f"Error-- Linea {self.numero_linea}: el identificador '{elemento.get_identificador()}' no coincide con el valor de asignación.")
                                return False
        print(f"Error-- Linea {self.numero_linea}: se esperaba identificador")
        return False


comp=Compilador()
comp.text_reader()