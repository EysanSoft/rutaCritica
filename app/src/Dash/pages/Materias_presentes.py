#Importo las librerias
import dash
from dash import html
from pylocalstorage import LocalStorage

from app.src.Dash.components.materies.createTable import crearTabla
from app.src.Dash.components.reinscription.simbologia import margenSimbologia
from app.src.Dash.dataAlumno import relaciones

dash.register_page(__name__, path="/materiaspresentes")

def tableMateriasPresentes(dataframePresentes,idinput,listaCards):
    tablaDependencias = html.Div([
        crearTabla(dataframePresentes, idinput, listaCards)
    ])

    return {"tablaPresente": tablaDependencias}

#Instancio La Clase Del Alumno
alumno = LocalStorage().getItem("informacionAlumno")

#con esta data puedo hacer la vista
relacionDataframe = relaciones(alumno['matriculaAlumno'],alumno['mes'],True)

lista = ["p1","p2","p3","p4","p5"]

materiasPresentes = tableMateriasPresentes(relacionDataframe['materiasAbiertas'],"inputPresentes",lista)

layout = html.Div(
    id="id",
    style=margenSimbologia(),
    children=[
        html.H5("Materias Presentes Para El Periodo " + str(relacionDataframe['periodo'])),
        html.Br(),
        html.Br(),
        html.Br(),
        materiasPresentes['tablaPresente']
    ]
)