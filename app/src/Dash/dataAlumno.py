import json
import random

import pandas as pd

from app.src.Controller.criticalPath import getTaskAndDependencie, flatten, calcularRutaCritica
from app.src.Controller.datosAlumno import obtencionDatosAlumno, filtrarDataframe, dataframeMateriasRelaciones
from app.src.Controller.get_materias_per_periodo import obtenerMateriasPeriodoReinscripcion, filtrarMateriasPorPeriodo, obtenerMateriasPeriodoStatusActual
from app.src.Controller.globalVariables import CLAVE

def rutaCriticaTotal(dataframeFiltrado,rutaCriticaTotales):
    listaRutaCriticaTotales = []
    if str(rutaCriticaTotales.get_critical_path()[0]) == "None":  # significa que la ruta critica no es seguido, ejemplo en-ma-ag si no enero y se va a otro periodo
        for i in rutaCriticaTotales.get_critical_path():
            listaRutaCriticaTotales.append(str(i))
        listaRutaCriticaTotales.pop(0)

    if len(listaRutaCriticaTotales) > 0:
        lista = []
        for index, row in dataframeFiltrado.iterrows():
            lista.append(row.to_dict())
        valor = {}
        for i in lista:  # lc
            listaValores = list(i.values())
            result = all(elem in listaValores for elem in listaRutaCriticaTotales)
            if result:
                valor = i
            else:
                print("No, list1 does not contains all elements in list2")
        return valor
    else:
        return None

def relaciones(matricula, mes, bandera): # si es -4 es estatus actual
    if bandera == True: #EstatusActual
        if 1 <= mes <= 4:
            mes = 10
            periodo = "enero-abril"
        elif 5 <= mes <= 8:
            mes = 2
            periodo ="mayo-agosto"
        elif 9 <= mes <= 12:
            mes = 6
            periodo = "septiembre-diciembre"

    if bandera == False:
        if 1 <= mes <= 4:
            periodo = "mayo-agosto"
        elif 5 <= mes <= 8:
            periodo ="septiembre-diciembre"
        elif 9 <= mes <= 12:
            periodo = "enero-abril"

    # obtengo las materias que aprobo reprobo y las que le faltan (las que faltan igual estaran las que reprobo claro esta)
    materiasFaltantes, aprobado, reprobado = obtencionDatosAlumno(matricula, CLAVE)

    # Obtengo la lista de las materias abiertas
    listaMateriasAbiertas = obtenerMateriasPeriodoReinscripcion(mes, CLAVE)

    # estas son las materias que puede tomar en su reinscripcion
    listadoMaterias = filtrarMateriasPorPeriodo(materiasFaltantes,listaMateriasAbiertas)  # aca ya obtengo la reinscripcion

    # quito las materias seriadas
    listadoMateriasReinscripcionFiltrado = filtrarDataframe(listadoMaterias, aprobado, materiasFaltantes)

    # obtengo las relaciones del dataframe
    dataframeFiltrado = dataframeMateriasRelaciones(listadoMateriasReinscripcionFiltrado, mes)
    '''datos = [["A",None,"B","C","D"],["E",None,None,None,None],["F","G",None,None,None],["H",None,"I","N",None]]
    columnas = ["septiembre-diciembre","enero-abril","mayo-agosto","septiembre-diciembre2","enero-abril2"]
    dataframeFiltrado = pd.DataFrame(data=datos, columns=columnas)'''

    if dataframeFiltrado.empty:
        x = {"materiasFaltantes": materiasFaltantes, "materiasAprobadas": aprobado, "materiasReprobadas": reprobado,
             "listadoReinscripcion": listadoMateriasReinscripcionFiltrado,"materiasAbiertas": listaMateriasAbiertas, "periodo": periodo}
        return x

    else:
        # obtengo las tareas y dependencias para la ruta critica
        json_string = dataframeFiltrado.to_json(orient="split", force_ascii=False)
        lista_materias_evaluar = json.loads(json_string)

        if len(lista_materias_evaluar['columns']) == 1:
            rutaCriticaRecomendados = []
            rutaCriticaTotales = None
            listaMaterias = flatten(lista_materias_evaluar['data'])
            materia = random.choice(listaMaterias)
            rutaCriticaRecomendados.append(materia)
            duracion = 15
            duracionPosible = 0
        else:
            tareas_dependencias_totales = getTaskAndDependencie(lista_materias_evaluar, False)
            tareas_dependencias_recomendadas = getTaskAndDependencie(lista_materias_evaluar, True)

            rutaCriticaTotales = calcularRutaCritica(tareas_dependencias_totales['RutaCriticaTotal']['tareas'],
                                                     tareas_dependencias_totales['RutaCriticaTotal']['relaciones'])

            rutaCriticaRecomendados = calcularRutaCritica(
                tareas_dependencias_recomendadas['RutaCriticaRecomendada']['tareas'],
                tareas_dependencias_recomendadas['RutaCriticaRecomendada']['relaciones']).get_critical_path()

            resultado = rutaCriticaTotal(dataframeFiltrado, rutaCriticaTotales)
            if resultado != None:  # le conviene perfectamente agarrar otra materia
                rutaCriticaTotales = resultado
            else:
                rutaCriticaTotales = None

            duracion = calcularRutaCritica(tareas_dependencias_recomendadas['RutaCriticaRecomendada']['tareas'],
                                           tareas_dependencias_recomendadas['RutaCriticaRecomendada'][
                                               'relaciones']).duration

            duracionPosible = calcularRutaCritica(tareas_dependencias_totales['RutaCriticaTotal']['tareas'],
                                                  tareas_dependencias_totales['RutaCriticaTotal'][
                                                      'relaciones']).duration

        x = {"materiasFaltantes": materiasFaltantes, "materiasAprobadas": aprobado, "materiasReprobadas": reprobado,
             "listadoReinscripcion": listadoMateriasReinscripcionFiltrado, "relaciones": dataframeFiltrado,
             "rutaCritica": rutaCriticaRecomendados, "posibleRutaCritica": rutaCriticaTotales,
             "materiasAbiertas": listaMateriasAbiertas, "periodo": periodo, "duracionRuta": duracion,
             "duracionRutaPosible": duracionPosible}

        return x

