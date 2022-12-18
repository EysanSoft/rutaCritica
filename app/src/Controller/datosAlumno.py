import pandas as pd
from app.src.Controller.exist_materias_per_periodo import ordenPeriodos
from app.src.Controller.globalVariables import CLAVE
from app.src.Services.dbConnect import conexionBd
from app.src.Services.querys import queryDatosAlumno, queryListaMaterias, queryAperturaMaterias
from app.src.Services.relations import getRelations
import networkx as nx

def uniquify(df_columns):
    seen = set()
    for item in df_columns:
        fudge = 1
        newitem = item
        while newitem in seen:
            fudge += 1
            newitem = "{} N.P -> {}".format(item, fudge)
        yield newitem
        seen.add(newitem)

def FindMaxLength(lst):
    maxList = max(lst, key=len)
    maxLength = max(map(len, lst))
    return maxList, maxLength

def listadoMaterias(clave):
    resultado = pd.read_sql(queryListaMaterias(clave),con=conexionBd())
    return resultado

def obtencionDatosAlumno(matricula,clave):
    materiasAlumno = pd.read_sql(queryDatosAlumno(matricula), con=conexionBd())
    if materiasAlumno.empty:
        print("matricula no registrada")
        #mostrarMensajes(ventana,"Error. Matricula no registrada")
    else:
        listaMaterias = materiasAlumno.drop_duplicates(subset='Nombre', keep="last")
        lista_materias_aprobadas = listaMaterias.query("Aprobado == 2")
        lista_materias_reprobadas = listaMaterias.query("Aprobado == 1")
        materiasFaltantes = listadoMaterias(clave)[listadoMaterias(clave)['Nombre'].isin(lista_materias_aprobadas['Nombre']) == False]
        return materiasFaltantes, lista_materias_aprobadas, lista_materias_reprobadas

def findMat(periodo,clave,nombre):
    listadoPeriodos = ordenPeriodos(3, periodo)
    for i in range(len(listadoPeriodos)):
        x = busquedaMateria(listadoPeriodos[i],nombre,clave)
        if x != None:
            dato = {"materia":nombre, "periodo":listadoPeriodos[i],"siguientePeriodo":listadoPeriodos[i+1]}
            break

    return dato

def busquedaMateria(periodo,materia,clave):
    enero_abril = [1, 2, 4, 5, 7, 8, 10]
    mayo_agosto = [2, 3, 5, 6, 8, 9]
    septiembre_diciembre = [1, 3, 4, 6, 7, 9, 10]

    if periodo == "enero-abril":
        resultado = pd.read_sql(queryAperturaMaterias(enero_abril, clave), con=conexionBd())
        return confirmacionMateria(materia,resultado)

    if periodo == "mayo-agosto":
        resultado = pd.read_sql(queryAperturaMaterias(mayo_agosto, clave), con=conexionBd())
        return confirmacionMateria(materia,resultado)

    if periodo == "septiembre-diciembre":
        resultado = pd.read_sql(queryAperturaMaterias(septiembre_diciembre, clave), con=conexionBd())
        return confirmacionMateria(materia,resultado)

def confirmacionMateria(materia,resultado):
    existMateria = materia in resultado['Nombre'].values
    if existMateria:
        return materia
    else:
        return None

def filtrarDataframe(dataframe, aprobado, materiasFaltantes):
    actividades = dataframe['Nombre']
    dicc = pd.DataFrame(getRelations())
    G = nx.from_pandas_edgelist(dicc, source='materia', target='depende', edge_attr=None, create_using=nx.DiGraph())
    listaAprobado = aprobado['Nombre'].values.tolist()

    for i in actividades:
        try:
            ancestors = sorted(list(nx.ancestors(G, i)))
            for j in ancestors:
                if j not in listaAprobado:
                    print("Esta materia no lo puede llevar porque esta seriada " + j)
                    dato = dataframe.loc[dataframe['Nombre'] == i]
                    dataframe = dataframe.drop(dato.index.values[0])
        except:
            print("no tiene anteriores todo ok")

    try:
        if len(materiasFaltantes) == 1:
            print("si puede tomar estadia")
        elif len(materiasFaltantes) > 1:
            dato = dataframe.loc[dataframe['Nombre'] == 'Estadía']
            dataframe = dataframe.drop(dato.index.values[0])
    except:
        print("No esta estadia en el periodo")

    return dataframe

def getSucessorByName(nombre):
    dicc = pd.DataFrame(getRelations())
    G = nx.from_pandas_edgelist(dicc, source='materia', target='depende', edge_attr=None, create_using=nx.DiGraph())
    try:  # estamos evaluando que hay materias que no existen en las relaciones
        desc = nx.descendants(G, nombre)
        sucesores = [path for p in desc for path in nx.all_simple_paths(G, nombre, p)]
        lista = FindMaxLength(sucesores)
        sucesores = lista[0]
        sucesores.pop(0)
        return sucesores
    except:
        print("No aparece en relaciones")
        return None

def dataframeMateriasRelaciones(listado, dt):
    listado_sucesiones = []

    if 1 <= dt <= 4:
        resultadoPeriodo = "mayo-agosto"

    if 5 <= dt <= 8:
        resultadoPeriodo = "septiembre-diciembre"  # va a ser esto

    if 9 <= dt <= 12:
        resultadoPeriodo = "enero-abril"

    listaGuardar = []
    dicc = pd.DataFrame(getRelations())
    G = nx.from_pandas_edgelist(dicc, source='materia', target='depende', edge_attr=None, create_using=nx.DiGraph())
    listadoSucesores = listado['Nombre'].values.tolist()

    for i in range(len(listadoSucesores)):
        try:  # estamos evaluando que hay materias que no existen en las relaciones
            desc = nx.descendants(G, listadoSucesores[i])
            sucesores = [path for p in desc for path in nx.all_simple_paths(G, listadoSucesores[i], p)]
            lista = FindMaxLength(sucesores)
            sucesores = lista[0]
            sucesores.pop(0)
            diccionario = {
                "Nombre": listadoSucesores[i],
                "Sucesores": sucesores
            }
            listaGuardar.append(diccionario)
        except:
            listaGuardar.append({"Nombre": listadoSucesores[i], "Sucesores": []})
            print("No aparece en relaciones")

    df = pd.DataFrame(listaGuardar)
    if df.empty:
        return pd.DataFrame()
    else:
        my_list = [list(a) for a in zip(df['Nombre'], df['Sucesores'])]
        for nombre, sucesiones in my_list:
            x = {"periodos": resultadoPeriodo, "materias": nombre, "sucesiones": sucesiones}
            listado_sucesiones.append(x)
        return devolverData(listado_sucesiones)

def devolverData(diccionario):
    listaDiccionarios = []

    for i in diccionario:
        if i['periodos'] == "enero-abril":
            dc = evaluarLista(i, "mayo-agosto")
        if i['periodos'] == "mayo-agosto":
            dc = evaluarLista(i, "septiembre-diciembre")
        if i['periodos'] == "septiembre-diciembre":
            dc = evaluarLista(i, "enero-abril")

        listaDiccionarios.append(dc)

    df = pd.DataFrame(listaDiccionarios)  # deberia de quedar con none en enero abril en e.o.e
    col = FindMaxLength(df['periodos'].values.tolist())
    x = list(uniquify(col[0]))

    combinada = list(zip(df['periodos'].values.tolist(), df['materias'].values.tolist()))  # en combinada debo cambiarlo

    for i in combinada:
        for j in range(len(x)):
            if x[j] not in i[0]:
                data = {"data": x[j], "posicion": j}
                i[0].insert(data['posicion'], data['data'])
                i[1].insert(data['posicion'], None)

    columnas = FindMaxLength(df['periodos'].values.tolist())

    dataframe = pd.DataFrame(columns=columnas[0],data=df['materias'].values.tolist())
    return dataframe

def evaluarLista(lista, periodo):
    sucesiones = lista['sucesiones']  # obtengo las sucesiones
    filtroNone = []; listaMaterias = []; listaPeriodos = []
    for i in range(len(sucesiones)):
        if i == 0:
            x = findMat(periodo, CLAVE, sucesiones[i])
        else:
            x = findMat(x['siguientePeriodo'], CLAVE, sucesiones[i])
        filtroNone.append(x)

    for i in filtroNone:
        listaMaterias.append(i['materia'])
        listaPeriodos.append(i['periodo'])

    listaMaterias.insert(0, lista['materias'])
    listaPeriodos.insert(0, lista['periodos'])

    x = list(uniquify(listaPeriodos))

    diccionario = {"periodos": x,"materias": listaMaterias}

    return diccionario