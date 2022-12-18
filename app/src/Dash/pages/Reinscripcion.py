#Importo las librerias
import dash
import pandas as pd
from dash import html
from pylocalstorage import LocalStorage
from app.src.Controller.globalVariables import CLAVE
from app.src.Dash.components.posibleRuta.table import mostrarPosibleRuta
from app.src.Dash.components.reinscription.planEstudios import crearTabla, creacionDataFrame
from app.src.Dash.components.reinscription.relationDependencias import reinscripcionTable
from app.src.Dash.components.reinscription.simbologia import creacionDataframeSimbologia, diccionarioSimbologia, tablaSimbologia, margenSimbologia
from app.src.Dash.dataAlumno import relaciones

dash.register_page(__name__, path="/")

def simbolo_table(dataframeSimbologia,simbologia):
    tablaSimbolo = html.Div([
        html.H5("Simbologia Utilizada"),
        html.Br(),
        tablaSimbologia(dataframeSimbologia, simbologia),
        html.Br(),
        html.Br()
    ])

    return {"tablaSimbologia":tablaSimbolo}

def plan_table(matricula,dataframeTabla,aprobado,reprobado,materiasFaltantes, idinput, listaCards):
    planEstudios = html.Div([
        html.H5('Plan De Estudios Del Alumno Con Matricula ' + str(matricula)),
        html.Br(),
        html.Br(),
        crearTabla(dataframeTabla, aprobado, reprobado, materiasFaltantes, idinput, listaCards),
        html.Br(),
        html.Br()
    ])

    return {"planEstudios":planEstudios}

def dependencies_table(matricula,dataframeReinscripcion,rutaCritica,idinput,listCards,duracion):
    tablaDependencias = html.Div([
        html.H5('Ruta Critica Del Alumno Con Matricula ' + str(matricula)+" Con Una Duracion De "+str(duracion)+ " Semanas"),
        html.Br(),
        html.Br(),
        reinscripcionTable(dataframeReinscripcion, rutaCritica, idinput, listCards),
    ])

    return {"tablaDependencias":tablaDependencias}

def posibleRutaCritica(ruta_critica,idinput,relaciones):
    if ruta_critica != None:
        rutaCritica = list(ruta_critica.values())
        dataframe = pd.DataFrame([ruta_critica])
        tablaPosibleRutaCritica = html.Div([
            html.Br(),
            html.Br(),
            html.H5("Asi Mismo Se Sugiere Que Tome La Siguiente Ruta Critica Con Una Duracion De "+str(relaciones['duracionRutaPosible'])+" Semanas"),
            html.Br(),
            html.Br(),
            mostrarPosibleRuta(dataframe,rutaCritica,idinput)
        ])
    else:
        tablaPosibleRutaCritica = html.Div()

    return {"posibleRutaCritica":tablaPosibleRutaCritica}

#Instancio La Clase Del Alumno
alumno = LocalStorage().getItem("informacionAlumno")

#con esta data puedo hacer la vista
relacionDataframe = relaciones(alumno['matriculaAlumno'],alumno['mes'],False)

#datosTabla
dataframeSimbologia = creacionDataframeSimbologia()
simbologia = diccionarioSimbologia(dataframeSimbologia)
dataframeTabla = creacionDataFrame(CLAVE)

#obtengo los widgets
widgetSimbologia = simbolo_table(dataframeSimbologia,simbologia)

#listaCards
lista = ["11","12","13","14","15"]
lista2 = ["16","17","18","19","20"]

widgetPlanEstudios = plan_table(alumno['matriculaAlumno'],dataframeTabla,
relacionDataframe['materiasAprobadas'],relacionDataframe['materiasReprobadas'],relacionDataframe['materiasFaltantes'],"inputhome", lista)

if len(relacionDataframe) == 6:
    layout = html.Div(
        id="id",
        style=margenSimbologia(),
        children=[
            html.H5("Reinscripcion Para El Periodo " + str(relacionDataframe['periodo']) + " Del Alumno Con Matricula " + str(alumno['matriculaAlumno'])),
            html.Br(),
            html.Br(),
            html.Br(),
            widgetSimbologia['tablaSimbologia'],
            widgetPlanEstudios['planEstudios'],
            html.H5("No Puede Tomar Ninguna Materia Debido A Que Para El Periodo "+str(relacionDataframe['periodo']+" No Abren Las Asignaturas Que Tiene Pendiente"))
        ]
    )

else:
    widgetDependenciasTable = dependencies_table(alumno['matriculaAlumno'],relacionDataframe['relaciones'],relacionDataframe['rutaCritica'],
    "inputhome2",lista2,relacionDataframe['duracionRuta'])

    widgetPosibleRutaCritica = posibleRutaCritica(relacionDataframe['posibleRutaCritica'],"posibleReinscripcion", relacionDataframe)

    layout = html.Div(
        id="id",
        style=margenSimbologia(),
        children=[
            html.H5("Reinscripcion Para El Periodo "+str(relacionDataframe['periodo'])+" Del Alumno Con Matricula "+str(alumno['matriculaAlumno'])),
            html.Br(),
            html.Br(),
            html.Br(),
            widgetSimbologia['tablaSimbologia'],
            widgetPlanEstudios['planEstudios'],
            widgetDependenciasTable['tablaDependencias'],
            widgetPosibleRutaCritica['posibleRutaCritica']
        ]
    )