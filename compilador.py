from typing import List
from collections import defaultdict
from dato import Dato
"""
II Proyecto Programado: Analizador semántico
Elias Campos Artavia
Dilanna Cordoba Campos
Abigail Salas Ramírez
"""

class Compilador:

    """
        Se inicializa el objeto Compilador.

        Atributos:
        - tabla_hash_dato (dict): Diccionario para almacenar datos por key.
        - key_dato (list): Lista de llaves de datos.
        - parametros (list): Lista de parámetros de funciones.
        - num_linea (int): Contador de líneas procesadas.
        """
    def __init__(self):
        self.tabla_hash_dato = {}
        self.key_dato = []
        self.parametros = []
        self.num_linea = 0

    """
        Verifica si un dato ya está presente en la lista de keys (key_dato).

        Parámetros:
        - dato (Dato): El dato a verificar.

        Retorna:
        - bool: True si el dato está presente, False de lo contrario.
        """
    def verifica_llave(self, dato):
        for v in self.key_dato:
            if dato.get_key() == v:
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
        Busca un dato en el diccionario tabla_hash_dato por su key.

        Parámetros:
        - key (str): La key del dato a buscar.

        Retorna:
        - la key y el valor del dato encontrado, o None si no se encuentra.
        """
    def buscar_dato_tablaHash(self, key):
        for dato in self.tabla_hash_dato.items():
            if dato[1].get_key() == key:
                return dato

    """
        Verifica si una variable de retorno coincide con la declaración de la función.

        Parámetros:
        - ret (str): La variable de retorno a verificar.
        - nom_funcion (str): El nombre de la función.

        Retorna:
        - bool: True si la variable de retorno coincide con la declaración de la función, False si no es asi.
        """
    def verifica_return(self, retorno, nom_funcion):
        validacion_return = False
        validacion_funcion = False

        for key in self.key_dato:
            if key == retorno:
                validacion_return = True
            if key == nom_funcion:
                validacion_funcion = True

        if validacion_funcion and validacion_return:
            if self.tabla_hash_dato[retorno].get_tipoDato() == self.tabla_hash_dato[nom_funcion].get_tipoDato():
                return True

        return False

    """
        Realiza la lectura y análisis del archivo de texto , procesando línea por línea.
        Analiza las palabras en cada línea para identificar datos como variables, funciones, tipos de datos
        Realiza verificaciones y validaciones, mostrando mensajes de error cuando es necesario.
        Lee el archivo línea por línea, procesando cada línea para identificar y analizar datos del programa.
        Los datos pueden ser variables, funciones o errores de sintaxis.
        """
    def text_reader(self):
        nombre_funcion = ""
        palabra = ""
        palabra_aux = ""
        linea = ""
        contador = 0
        validacion = 0
        validacion_aux = False
        contador_llaves = 0
        compilacion_correcta = 0

        
        nombre = ""
        tipo = ""
        valor = ""
        tipo_palabra = ""
        key_palabra = ""
 
        """
        El archivo codigoCorrecto.txt o codigoIncorrecto.txt, se leeran línea por línea, por medio del read line
        y se separan todas las palabras que se encuentran en la linea por medio del .split
        También se eliminará los caracteres que no se toman para la validación, como lo son 
        los "()" y el ";" 
        Se cuenta con dos archivos .txt, en donde el mismo nombre menciona la funcionalidad 
        al abrirlo con el analizador semántico
        "codigoCorrecto.txt"    y   "codigoIncorrecto.txt"
        """
        with open("codigoIncorrecto.txt") as entrada:
            if entrada:
                while validacion == 0:
                    linea = entrada.readline()
                    contador += 1
                    self.num_linea = contador

                    palabras = linea.split()

                    for palabra in palabras:

                        if not palabra:
                            break

                        if palabra != palabra_aux:
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
                                            nombre = nombre[:-1]
                                        if palabra[-1] == ';':
                                            palabra = palabra[:-1]

                                    if nombre != palabra:
                                        if nombre != "":
                                            if nombre == "return":
                                                if palabra[:-1]:
                                                    palabra = palabra[:-1]
                                                if not self.verifica_return(palabra, nombre_funcion):
                                                    print(
                                                        f"Error-- Linea {self.num_linea}: valor de retorno no coincide con la declaración de la funcion'{nombre_funcion}'\n\n")
                                                    compilacion_correcta += 1

                                            if tipo_palabra == "":
                                                tipo_palabra = palabra
                                                if tipo_palabra and tipo_palabra[0] == '(':
                                                    tipo_palabra = tipo_palabra[1:]

                                            else:
                                                key_palabra = palabra
                                                if key_palabra[-1] == ')' or key_palabra[-1] == ',':
                                                    key_palabra = key_palabra[:-1]

                                            valor = palabra
                                            if self.es_funcion(valor):
                                                validacion_aux = True

                                            if validacion_aux:
                                                if key_palabra != "" and tipo_palabra != "":
                                                    funcion = Dato("", tipo_palabra, key_palabra)
                                                    if self.valor_tipo_correcto(funcion):
                                                        self.parametros.append(funcion)
                                                    else:
                                                        compilacion_correcta += 1
                                                    tipo_palabra = ""
                                                    key_palabra = ""

                                            else:
                                                if valor and valor[-1] == ';':
                                                    valor = valor[:-1]
                                                break

                            palabra_aux = palabra

                    validacion_aux = False
                    palabra = ""
                    palabra_aux = ""
                    tipo_palabra = ""
                    key_palabra = ""

                    if len(self.parametros) == 0:
                        elemento = Dato(valor, tipo, nombre)
                        if not self.valor_tipo_correcto(elemento):
                            print("COMPILACION INTERRUMPIDA....\n\n")
                            compilacion_correcta += 1

                    else:
                        funcion = Dato(nombre, tipo, self.parametros)
                        nombre_funcion = nombre
                        self.key_dato.append(nombre)
                        key = nombre
                        self.tabla_hash_dato[key] = funcion

                        self.parametros.clear()

                    nombre = ""
                    tipo = ""
                    valor = ""

                    if not linea:
                        validacion = 1  # verifica el final del archivo

        if contador_llaves > 0:
            print("Error-- Linea " +str(self.num_linea)+": se esperaba '}' ")
            compilacion_correcta += 1

        if contador_llaves < 0:
            print("Error-- Linea " + str(self.num_linea) +": se esperaba '{' ")
            compilacion_correcta += 1

        if compilacion_correcta == 0:
            print("Successful Compilation\n\n")


    """
        Realiza verificaciones específicas para encontrar si son son correctos los tipos de datos y valores en el programa.

        Parámetros:
        - dato (Dato): El dato a verificar.

        Retorna:
        - bool: True si el tipo de dato y valor son correctos, False de lo contrario.
       
        La función realiza diversas comprobaciones para garantizar que un dato (variable o función) tenga un
        tipo de dato y valor coherentes. Verifica si las asignaciones y declaraciones son válidas, y maneja casos
        específicos como la declaración de variables con o sin tipo de dato, asignaciones de variables.

        Si el tipo de dato y valor son correctos, devuelve True. En caso contrario, imprime mensajes de error y devuelve False.

   
        """
    def valor_tipo_correcto(self, dato):
        if ((dato.get_tipoDato() == "" and dato.get_key() == "" and dato.get_valor() == "")
            or dato.get_key() == "return" or dato.get_tipoDato() == "void"
            or (dato.get_key() and dato.get_key()[0] == 'i' and dato.get_key()[1] == 'f')
            or (dato.get_key() and dato.get_key()[0] == 'w' and dato.get_key()[1] == 'h')
        ):
            return True

        if dato.get_key() != "":
            if dato.get_tipoDato() == "":  # no tiene tipo de dato
                if self.verifica_llave(dato):  # existe la llave
                    if self.es_numero(dato.get_valor()):  # es número y es acorde
                        key = dato.get_key()

                        elemento = self.buscar_dato_tablaHash(key)

                        if elemento[1].get_tipoDato() == "int" or elemento[1].get_tipoDato() == "float":
                            dato.set_tipoDato(elemento[1].get_tipoDato())
                            self.tabla_hash_dato.pop(key)
                            self.tabla_hash_dato[key] = dato
                            self.key_dato.append(elemento[1].get_key())
                            return True
                        else:
                            print(f"Error-- Linea {self.num_linea}: el identificador '{dato.get_key()}' no coincide con el valor de asignacion.")
                            return False

                    else:  # llave declarada y sin tipo de dato
                        key = dato.get_key()

                        elemento = self.buscar_dato_tablaHash(key)

                        if ((dato.get_valor()[0] == '"' and dato.get_valor()[-1] == '"') and elemento[1].get_tipoDato() == "string"):  # es cadena y es acorde
                            key = dato.get_key()
                            elemento = self.buscar_dato_tablaHash(key)
                            dato.set_tipoDato(elemento[1].get_tipoDato())
                            self.tabla_hash_dato.pop(key)
                            self.tabla_hash_dato[key] = dato
                            self.key_dato.append(dato.get_key())
                            return True
                        else:
                            print(f"Error-- Linea {self.num_linea}: el identificador '{dato.get_key()}' no coincide con el valor de asignacion.")
                            return False
                else:
                    print(f"Error-- Linea {self.num_linea}: '{dato.get_key()}' no esta declarado.")
                    return False

            else:  # tiene tipo de dato
                if self.verifica_llave(dato):  # Si existe
                    print(f"Error-- Linea {self.num_linea}: doble declaracion de variable.")
                    return False  # doble declaración, mal hecho

                else:  # No existe la llave
                    if dato.get_valor() == "":  # No tiene valor
                        key = dato.get_key()
                        self.tabla_hash_dato[key] = dato
                        self.key_dato.append(dato.get_key())
                        return True

                    else:  # Si tiene valor
                        if (self.es_numero(dato.get_valor()) and (dato.get_tipoDato() == "int" or dato.get_tipoDato() == "float")):  # es número y es acorde
                            key = dato.get_key()
                            self.tabla_hash_dato.pop(key, None)
                            self.tabla_hash_dato[key] = dato
                            self.key_dato.append(dato.get_key())
                            return True

                        else:
                            if (
                                (dato.get_valor()[0] == '"' and dato.get_valor()[-1] == '"')
                                and dato.get_tipoDato() == "string"
                            ):  # declaración y definición correcta
                                key = dato.get_key()
                                elemento = self.buscar_dato_tablaHash(key)
                                dato.set_tipoDato(elemento.get_tipoDato())
                                self.tabla_hash_dato.pop(key)
                                self.tabla_hash_dato[key] = dato
                                self.key_dato.append(dato.get_key())
                                return True
                            else:
                                print(f"Error-- Linea {self.num_linea}: el identificador '{dato.get_key()}' no coincide con el valor de asignacion.")
                                return False
        print(f"Error-- Linea {self.num_linea}: se esperaba identificador.")
        return False

    """
        se crea la instancia del compilador
        se lee el archivo 
        """
comp=Compilador()
comp.text_reader()