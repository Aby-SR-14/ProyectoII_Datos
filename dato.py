class Dato:
    """Esta clase representa un elemento en el compilador."""

    """
        Inicializa el objeto Dato.

        cotiene los siguientes parámetros:
        - valor, tipo(str): El valor del elemento.
        - tipoDato, tipo(str): El tipo de dato del elemento.
        - identificador, tipo(str): El identificador del elemento.
        """
    def __init__(self, valor,tipoDato, identificador):
        self.valor = valor
        self.identificador = identificador
        self.tipoDato = tipoDato
        self.parametros = None

    """
        Establece el valor del elemento.
        - valor,tipo (str): El nuevo valor del elemento.
        """
    def set_valor(self, valor):
        
        self.valor = valor
    """
        Obtiene el valor del elemento.
        - retorna valor,tipo (str): El valor del elemento.
        """
    def get_valor(self):
        return self.valor

    """
        Establece el Tipo de Datp del elemento.
        - identificador,tipo (str): El nuevo identificador del elemento.
        """
    def set_identificador(self, identificador):
        self.identificador = identificador

    """
        Obtiene el identificador del elemento.
        - retorna identificador,tipo (str): El identificador del elemento.
        """
    def get_identificador(self):
        return self.identificador
    
    """
        Establece el valor del elemento.
        - tipoDato,tipo (str): El nuevo tipo de dato del elemento.
        """
    def set_tipoDato(self, tipoDato):
        self.tipoDato = tipoDato
    """
        Obtiene el tipo de Dato del elemento.
        - retorna tipoDato,tipo (str): El tipo de dato del elemento.
        """
    def get_tipoDato(self):
        return self.tipoDato
    """
        Establece el parametro del elemento.
        - parametro,tipo (str): El nuevo parametro del elemento.
        """
    def set_parametros(self, parametros):
        self.parametros = parametros
    """
        Obtiene el parrametro del elemento.
        - retorna parametro,tipo (str): El parametro del elemento.
        """
    def get_parametros(self):
        return self.parametros


    def __str__(self):
        resultado = "Tipo de Dato: {}\n".format(self.tipoDato)
        resultado += "Identificador: {}\n".format(self.identificador)
        resultado += "Valor: {}\n".format(self.valor)

        if self.parametros:
            for parametro in self.parametros:
                resultado += parametro.__str__()

        return resultado
