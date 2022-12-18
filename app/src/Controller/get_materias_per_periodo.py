import pandas as pd
from app.src.Services.dbConnect import conexionBd
from app.src.Services.querys import queryAperturaMaterias

def obtenerMateriasPeriodoStatusActual(mes,clave):
    enero_abril = [1, 2, 4, 5, 7, 8, 10]
    mayo_agosto = [2, 3, 5, 6, 8, 9]
    septiembre_diciembre = [1, 3, 4, 6, 7, 9, 10]

    if 1 <= mes  <= 4:
        print("actual enero abril")
        resultado = pd.read_sql(queryAperturaMaterias(enero_abril,clave), con=conexionBd())

    if 5 <= mes <= 8:
        print("actual mayo agosto")
        resultado = pd.read_sql(queryAperturaMaterias(mayo_agosto,clave), con=conexionBd())

    if 9 <= mes <= 12:
        print("actual septiembre diciembre")
        resultado = pd.read_sql(queryAperturaMaterias(septiembre_diciembre,clave), con=conexionBd())

    return resultado

def obtenerMateriasPeriodoReinscripcion(mes,clave):
    enero_abril = [1, 2, 4, 5, 7, 8, 10]
    mayo_agosto = [2, 3, 5, 6, 8, 9]
    septiembre_diciembre = [1, 3, 4, 6, 7, 9, 10]

    if 1 <= mes  <= 4:
        print("reinscripcion mayo agosto")
        resultado = pd.read_sql(queryAperturaMaterias(mayo_agosto,clave), con=conexionBd())

    if 5 <= mes <= 8:
        print("reinscripcion septiembre diciembre")
        resultado = pd.read_sql(queryAperturaMaterias(septiembre_diciembre,clave), con=conexionBd())

    if 9 <= mes <= 12:
        print("reinscripcion enero abril")
        resultado = pd.read_sql(queryAperturaMaterias(enero_abril,clave), con=conexionBd())


    return resultado

def filtrarMateriasPorPeriodo(materiasFaltantes,listaMateriasAbiertas):
    obtencionMateriasReinscripcion = listaMateriasAbiertas[listaMateriasAbiertas['Nombre'].isin(materiasFaltantes['Nombre']) == True]
    return obtencionMateriasReinscripcion
