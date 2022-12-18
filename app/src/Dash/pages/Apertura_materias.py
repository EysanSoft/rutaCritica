#Importo las librerias
import dash
from dash import html
from pylocalstorage import LocalStorage
from app.src.Dash.components.materies.createTable import crearTabla
from app.src.Dash.components.reinscription.simbologia import margenSimbologia
from app.src.Dash.dataAlumno import relaciones

dash.register_page(__name__, path="/aperturamaterias")

def tableAperturaMaterias(dataframeApertura,idinput,listaCards):
    tablaDependencias = html.Div([
        crearTabla(dataframeApertura,idinput,listaCards)
    ])

    return {"tablaApertura": tablaDependencias}

#Instancio La Clase Del Alumno
alumno = LocalStorage().getItem("informacionAlumno")

#con esta data puedo hacer la vista
relacionDataframe = relaciones(alumno['matriculaAlumno'],alumno['mes'],False)

lista = ["a1","a2","a3","a4","a5"]

aperturaMaterias = tableAperturaMaterias(relacionDataframe['materiasAbiertas'],"inputApertura",lista)

layout = html.Div(
    id="id",
    style= margenSimbologia(),
    children=[
        html.H5("Apertura De Materias Para El Periodo " + str(relacionDataframe['periodo'])),
        html.Br(),
        html.Br(),
        html.Br(),
        aperturaMaterias['tablaApertura']
    ]
)