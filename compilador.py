from typing import List
from collections import defaultdict
from dato import Dato

class Compilador:

    """
        Se inicializa el objeto Compilador.

        Atributos:
        - hashtable_elemento (dict): Diccionario para almacenar elementos por key.
        - key_elemento (list): Lista de llaves de elementos.
        - parametros (list): Lista de parámetros de funciones.
        - num_linea (int): Contador de líneas procesadas.
        """
    def __init__(self):
        self.hashtable_elemento = {}
        self.key_elemento = []
        self.parametros = []
        self.num_linea = 0

    """
        Verifica si un elemento ya está presente en la lista de keys (key_elemento).

        Parámetros:
        - elemento (Dato): El elemento a verificar.

        Retorna:
        - bool: True si el elemento está presente, False de lo contrario.
        """
    def verifica_llave(self, elemento):
        for v in self.key_elemento:
            if elemento.get_identificador() == v:
                return True
        return False

    """
        Verifica si una cadena representa un número. Verificando asi si todos los componentes son digitos

        Parámetros:
        - x (str): La cadena a verificar.

        Retorna:
        - bool: True si la cadena es un número, False de lo contrario.
        """
    def es_numero(self, x):
        if x[0] == '"':
            return False

        for i in range(len(x)):
            if x[i].isalpha():
                return False

        return True

    """
        Verifica si una cadena representa el comienzo de una función.

        Parámetros:
        - x (str): La cadena a verificar.

        Retorna:
        - bool: True si la cadena representa el comienzo de una función, False de lo contrario.
        """
    def es_funcion(self, x):
        if x and x[0] == '(':
            return True
        return False

    """
        Busca un elemento en el diccionario hashtable_elemento por su key.

        Parámetros:
        - key (str): La key del elemento a buscar.

        Retorna:
        - la key y el valor del elemento encontrado, o None si no se encuentra.
        """
    def busca_elemento_hash(self, key):
        for registro in self.hashtable_elemento.items():
            if registro[1].get_identificador() == key:
                return registro

    """
        Verifica si una variable de retorno coincide con la declaración de la función.

        Parámetros:
        - ret (str): La variable de retorno a verificar.
        - nom_funcion (str): El nombre de la función.

        Retorna:
        - bool: True si la variable de retorno coincide con la declaración de la función, False si no es asi.
        """
    def verifica_return(self, ret, nom_funcion):
        bandera_ret = False
        bandera_fun = False

        for key in self.key_elemento:
            if key == ret:
                bandera_ret = True
            if key == nom_funcion:
                bandera_fun = True

        if bandera_fun and bandera_ret:
            if self.hashtable_elemento[ret].get_tipoDato() == self.hashtable_elemento[nom_funcion].get_tipoDato():
                return True

        return False

    """
        Realiza la lectura y análisis del archivo de texto , procesando línea por línea.
        Analiza las palabras en cada línea para identificar elementos como variables, funciones, tipos de datos
        Realiza verificaciones y validaciones, mostrando mensajes de error cuando es necesario.
        Lee el archivo línea por línea, procesando cada línea para identificar y analizar elementos del programa.
        Los elementos pueden ser variables, funciones o errores de sintaxis.
        """
    def text_reader(self):
        nombre_funcion = ""
        palabra = ""
        palabra2 = ""
        linea = ""
        contador = 0
        bandera = 0
        bandera2 = False
        contador_llaves = 0
        compilacion_correcta = 0

        # ------------Datos elemento---------------
        nombre = ""
        tipo = ""
        valor = ""
        tipo_p = ""
        id_p = ""

        with open("codigos.txt") as entrada:
            if entrada:
                while bandera == 0:
                    linea = entrada.readline()  # lee el archivo
                    contador += 1
                    self.num_linea = contador

                    palabras = linea.split()

                    for palabra in palabras:

                        if not palabra:
                            break

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
                                        if nombre[-1] == ';':
                                            nombre = nombre[:-1]  # elimina el ; para crear el objeto
                                        if palabra[-1] == ';':
                                            palabra = palabra[:-1]  # elimina el ; para crear el objeto

                                    if nombre != palabra:
                                        if nombre != "":
                                            if nombre == "return":
                                                if palabra[:-1]:
                                                    palabra = palabra[:-1]
                                                if not self.verifica_return(palabra, nombre_funcion):
                                                    print(
                                                        f"Error-- la variable de retorno no es correcta conforme a la declaracion de la funcion '{nombre_funcion}'\n\n")
                                                    compilacion_correcta += 1

                                            if tipo_p == "":
                                                tipo_p = palabra
                                                if tipo_p and tipo_p[0] == '(':
                                                    tipo_p = tipo_p[1:]

                                            else:
                                                id_p = palabra
                                                if id_p[-1] == ')' or id_p[-1] == ',':
                                                    id_p = id_p[:-1]

                                            valor = palabra
                                            if self.es_funcion(valor):
                                                bandera2 = True

                                            if bandera2:
                                                if id_p != "" and tipo_p != "":
                                                    funcion = Dato("", tipo_p, id_p)
                                                    if self.valor_tipo_correcto(funcion):
                                                        self.parametros.append(funcion)
                                                    else:
                                                        compilacion_correcta += 1
                                                    tipo_p = ""
                                                    id_p = ""

                                            else:
                                                if valor and valor[-1] == ';':
                                                    valor = valor[:-1]
                                                break  # elimina el ; para crear el objeto

                            palabra2 = palabra

                    bandera2 = False
                    palabra = ""
                    palabra2 = ""
                    tipo_p = ""
                    id_p = ""

                    if len(self.parametros) == 0:
                        ele = Dato(valor, tipo, nombre)
                        if not self.valor_tipo_correcto(ele):
                            print("NO compila....\n\n")
                            compilacion_correcta += 1

                    else:
                        funcion = Dato(nombre, tipo, self.parametros)
                        nombre_funcion = nombre
                        self.key_elemento.append(nombre)
                        key = nombre
                        registro = (key, funcion)
                        self.hashtable_elemento[key] = funcion

                        self.parametros.clear()

                    nombre = ""
                    tipo = ""
                    valor = ""

                    if not linea:
                        bandera = 1  # verifica el final del archivo

        if contador_llaves > 0:
            print("Error-- se esperaba '}'")
            compilacion_correcta += 1

        if contador_llaves < 0:
            print("Error-- se esperaba '{'")
            compilacion_correcta += 1

        if compilacion_correcta == 0:
            print("Successful Compilation\n\n")


    """
        Realiza verificaciones específicas para encontrar si son son correctos los tipos de datos y valores en el programa.

        Parámetros:
        - elemento (Dato): El elemento a verificar.

        Retorna:
        - bool: True si el tipo de dato y valor son correctos, False de lo contrario.
       
        La función realiza diversas comprobaciones para garantizar que un elemento (variable o función) tenga un
        tipo de dato y valor coherentes. Verifica si las asignaciones y declaraciones son válidas, y maneja casos
        específicos como la declaración de variables con o sin tipo de dato, asignaciones de variables.

        Si el tipo de dato y valor son correctos, devuelve True. En caso contrario, imprime mensajes de error y devuelve False.

   
        """
    def valor_tipo_correcto(self, elemento):
        if ((elemento.get_tipoDato() == "" and elemento.get_identificador() == "" and elemento.get_valor() == "")
            or elemento.get_identificador() == "return" or elemento.get_tipoDato() == "void"
            or (elemento.get_identificador() and elemento.get_identificador()[0] == 'i' and elemento.get_identificador()[1] == 'f')
            or (elemento.get_identificador() and elemento.get_identificador()[0] == 'w' and elemento.get_identificador()[1] == 'h')
        ):
            return True

        if elemento.get_identificador() != "":
            if elemento.get_tipoDato() == "":  # no tiene tipo de dato
                if self.verifica_llave(elemento):  # existe la llave
                    if self.es_numero(elemento.get_valor()):  # es número y es acorde
                        key = elemento.get_identificador()

                        ele = self.busca_elemento_hash(key)

                        if ele[1].get_tipoDato() == "int" or ele[1].get_tipoDato() == "float":
                            elemento.set_tipoDato(ele[1].get_tipoDato())
                            self.hashtable_elemento.pop(key)
                            self.hashtable_elemento[key] = elemento
                            self.key_elemento.append(ele[1].get_identificador())
                            return True
                        else:
                            print(f"Error-- Linea {self.num_linea}: el identificador '{elemento.get_identificador()}' no coincide con el valor de asignacion.")
                            return False

                    else:  # llave declarada y sin tipo de dato
                        key = elemento.get_identificador()

                        ele = self.busca_elemento_hash(key)

                        if ((elemento.get_valor()[0] == '"' and elemento.get_valor()[-1] == '"') and ele[1].get_tipoDato() == "string"):  # es cadena y es acorde
                            key = elemento.get_identificador()
                            ele = self.busca_elemento_hash(key)
                            elemento.set_tipoDato(ele[1].get_tipoDato())
                            self.hashtable_elemento.pop(key)
                            self.hashtable_elemento[key] = elemento
                            self.key_elemento.append(elemento.get_identificador())
                            return True
                        else:
                            print(f"Error-- Linea {self.num_linea}: el identificador '{elemento.get_identificador()}' no coincide con el valor de asignacion.")
                            return False
                else:
                    print(f"Error-- Linea {self.num_linea}: '{elemento.get_identificador()}' no esta declarado.")
                    return False

            else:  # tiene tipo de dato
                if self.verifica_llave(elemento):  # Si existe
                    print(f"Error-- Linea {self.num_linea}: doble declaracion de variable.")
                    return False  # doble declaración, mal hecho

                else:  # No existe la llave
                    if elemento.get_valor() == "":  # No tiene valor
                        key = elemento.get_identificador()
                        registro = (key, elemento)
                        self.hashtable_elemento[key] = elemento
                        self.key_elemento.append(elemento.get_identificador())
                        return True

                    else:  # Si tiene valor
                        if (self.es_numero(elemento.get_valor()) and (elemento.get_tipoDato() == "int" or elemento.get_tipoDato() == "float")):  # es número y es acorde
                            key = elemento.get_identificador()
                            self.hashtable_elemento.pop(key, None)
                            self.hashtable_elemento[key] = elemento
                            self.key_elemento.append(elemento.get_identificador())
                            return True

                        else:
                            if (
                                (elemento.get_valor()[0] == '"' and elemento.get_valor()[-1] == '"')
                                and elemento.get_tipoDato() == "string"
                            ):  # declaración y definición correcta
                                key = elemento.get_identificador()
                                ele = self.busca_elemento_hash(key)
                                elemento.set_tipoDato(ele.get_tipoDato())
                                self.hashtable_elemento.pop(key)
                                self.hashtable_elemento[key] = elemento
                                self.key_elemento.append(elemento.get_identificador())
                                return True
                            else:
                                print(f"Error-- Linea {self.num_linea}: el identificador '{elemento.get_identificador()}' no coincide con el valor de asignacion.")
                                return False
        print(f"Error-- Linea {self.num_linea}: se esperaba identificador.")
        return False

"""
        se crea la instancia del compilador
        se lee el archivo 
        """
comp=Compilador()
comp.text_reader()