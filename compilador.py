

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

    def busca_elemento_hash(key):
        for registro in tablahash_dato.items():
            if registro[1].get_identificador() == key:
                return registro[1]

    def verifica_return(ret, nombre_funcion):
        flag_ret = False
        flag_fun = False

        for key in dato_key:
            if key == ret:
                flag_ret = True

            if key == nombre_funcion:
                flag_fun = True

        if flag_fun and flag_ret:
            if hashtable_elemento[ret].get_tipo_dato() == hashtable_elemento[nombre_funcion].get_tipo_dato():
                return True

        return False
