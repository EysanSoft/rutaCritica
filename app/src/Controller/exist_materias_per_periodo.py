import pandas as pd

from app.src.Services.dbConnect import conexionBd
from app.src.Services.querys import queryAperturaMaterias


def existMateriasPerPeriodo(periodo,materia,clave):
    enero_abril = [1, 2, 4, 5, 7, 8, 10]
    mayo_agosto = [2, 3, 5, 6, 8, 9]
    septiembre_diciembre = [1, 3, 4, 6, 7, 9, 10]

    if periodo == "enero-abril":
        #print("buscare si existe la materia "+materia+" para este periodo enero abril")
        resultado = pd.read_sql(queryAperturaMaterias(enero_abril, clave), con=conexionBd())
        return evaluarPeriodo(materia,resultado,periodo)

    if periodo == "mayo-agosto":
        #print("buscare si existe la materia "+materia+" para este periodo mayo agosto")
        resultado = pd.read_sql(queryAperturaMaterias(mayo_agosto, clave), con=conexionBd())
        return evaluarPeriodo(materia,resultado,periodo)

    if periodo == "septiembre-diciembre":
        #print("buscare si existe la materia "+materia+" para este periodo septiembre diciembre")
        resultado = pd.read_sql(queryAperturaMaterias(septiembre_diciembre, clave), con=conexionBd())
        return evaluarPeriodo(materia,resultado,periodo)

def evaluarPeriodo(materia,resultado,periodo):
    existMateria = materia in resultado['Nombre'].values
    if existMateria:
        return {"materia":materia,"periodo":periodo}
    else:
        return None


def ordenPeriodos(numIters, periodoActual):
    numPeriodo = 0
    iterActual = 0
    # Nuestra lista resultante.
    listaPeriodos = []
    # Un diccionario de los 3 periodos.
    periodos = {
        1: 'enero-abril',
        2: 'mayo-agosto',
        3: 'septiembre-diciembre',
    }

    if periodoActual == "enero-abril":
        numPeriodo = 1
    if periodoActual == "mayo-agosto":
        numPeriodo = 2
    if periodoActual == "septiembre-diciembre":
        numPeriodo = 3

    while iterActual < numIters:
        iterActual = iterActual + 1
        listaPeriodos.append(periodos[numPeriodo])
        numPeriodo = numPeriodo + 1
        if numPeriodo == 4:
            numPeriodo = 1
    return listaPeriodos