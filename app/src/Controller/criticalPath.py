import pandas as pd
from criticalpath import Node
from app.src.Services.dbConnect import conexionBd

def calcularRutaCritica(tareas,dependencias):
    p = Node('proyecto')

    # Cargar al proyecto las tareas y sus duraciones
    for i in tareas:
        p.add(Node(i[0], duration=i[1]["duracion"]))

    # Cargar al proyecto sus dependencias (secuencias)
    for j in dependencias:
        p.link(j[0], j[1])

    # Actualizar el proyecto:
    p.update_all()
    return p

def getMaterias():
    materias = pd.read_sql('select Nombre from d_materia where planestudiosid=28',con=conexionBd()).values.flatten().tolist()
    return materias

def listarSecuencia(lista):
    listaResultante = []
    iter = 0
    while iter < (len(lista) - 1):
        listaAuxEnPares = (lista[iter], lista[iter + 1])
        listaResultante.append(listaAuxEnPares)
        iter = iter + 1
    return listaResultante

def flatten(lista):
    return [item for sublist in lista for item in sublist]

def getTaskAndDependencie(listaMateriasEvaluar,bandera):
    if bandera == True:  # listaRecomendada
        for i in listaMateriasEvaluar['data']:  # calculo redes provramacion analisis
            if i[1] == None:
                i.clear()
        listaFiltrada = list(filter(None, listaMateriasEvaluar['data']))
        listaRecomendada = getDependencias(listaFiltrada)  # habra alguna
        return {"RutaCriticaRecomendada": listaRecomendada}
    else:
        listaTotal = getDependencias(listaMateriasEvaluar['data'])  # habra alguna
        return {"RutaCriticaTotal": listaTotal}

def getDependencias(lista):
    listaCritica = []

    for i in lista:  # listaFiltrada:#listaMateriasEvaluar['data']:
        listaCritica.append(listarSecuencia(i))
    dependencias = flatten(listaCritica)

    dataframe = pd.DataFrame(dependencias, columns=['from', 'to'])
    listaValores = dataframe.values.flatten()
    listaTiempos = list(dict.fromkeys(listaValores))

    tareas = []

    for i in listaTiempos:
        if i == None:
            duracion = 0
        else:
            duracion = 15
        task = (i, {'duracion': duracion})
        tareas.append(task)

    return {"relaciones": dependencias, "tareas": tareas}