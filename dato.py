class Dato:
    def __init__(self, valor,tipoDato, identificador):
        self.valor = valor
        self.identificador = identificador
        self.tipoDato = tipoDato
        self.parametros = None

    def set_valor(self, valor):
        self.valor = valor

    def get_valor(self):
        return self.valor

    def set_identificador(self, identificador):
        self.identificador = identificador

    def get_identificador(self):
        return self.identificador
    
    def set_tipoDato(self, tipoDato):
        self.tipoDato = tipoDato

    def get_tipoDato(self):
        return self.tipoDato

    def set_parametros(self, parametros):
        self.parametros = parametros

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
