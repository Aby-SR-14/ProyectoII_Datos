Básicamente la tabla hash va a a ser un diccionario que contiene diccionarios dentro. Ejemplo

tabla[nombre]={["Tipo":string,"Valor":Maria]}
tabla[x]={["Tipo":int,"Valor":8]}
tabla[flotante]={["Tipo":float,"Valor":5.5]}

porque a veces se debe de estar recuperando datos porque se le asignan valores nuevos. Ejemplo

int valor = 6
valor = 10      Hay que estar revisando que el tipo coincida con el valor
