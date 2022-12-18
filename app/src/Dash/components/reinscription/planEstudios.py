import networkx as nx
import dash_bootstrap_components as dbc
import pandas as pd
from dash import html, dash_table, callback, dcc, Dash
from dash.dependencies import Input, Output
from app.src.Controller.datosAlumno import listadoMaterias
from app.src.Controller.globalVariables import CLAVE
from app.src.Services.relations import getRelations

def creacionDataFrame(clave):
    lista = listadoMaterias(clave)
    periodo1 = lista[lista['Periodo'] == 1]['Nombre'].tolist()
    periodo2 = lista[lista['Periodo'] == 2]['Nombre'].tolist()
    periodo3 = lista[lista['Periodo'] == 3]['Nombre'].tolist()
    periodo4 = lista[lista['Periodo'] == 4]['Nombre'].tolist()
    periodo5 = lista[lista['Periodo'] == 5]['Nombre'].tolist()
    periodo6 = lista[lista['Periodo'] == 6]['Nombre'].tolist()
    periodo7 = lista[lista['Periodo'] == 7]['Nombre'].tolist()
    periodo8 = lista[lista['Periodo'] == 8]['Nombre'].tolist()
    periodo9 = lista[lista['Periodo'] == 9]['Nombre'].tolist()

    dataframe = pd.DataFrame(
        {
            "Cuatrimestre 1": periodo1,
            "< - >":[None,None,None,None,None,None,None],
            "Cuatrimestre 2": periodo2,
            "< - > ": [None, None, None, None, None, None, None],
            "Cuatrimestre 3": periodo3,
            "< - >  ": [None, None, None, None, None, None, None],
            "Cuatrimestre 4": periodo4,
            "< - >   ": [None, None, None, None, None, None, None],
            "Cuatrimestre 5": periodo5,
            "< - >    ": [None, None, None, None, None, None, None],
            "Cuatrimestre 6": periodo6,
            "< - >     ": [None, None, None, None, None, None, None],
            "Cuatrimestre 7": periodo7,
            "< - >      ": [None, None, None, None, None, None, None],
            "Cuatrimestre 8": periodo8,
            "< - >       ": [None, None, None, None, None, None, None],
            "Cuatrimestre 9": periodo9,
            "< - >        ": [None, None, None, None, None, None, None],
            "Cuatrimestre 10": ["Estadía",None,None,None,None,None,None],
        },
    )

    '''dataframe = pd.DataFrame(
        {
            "Cuatrimestre 1": periodo1,
            "Cuatrimestre 2": periodo2,
            "Cuatrimestre 3": periodo3,
            "Cuatrimestre 4": periodo4,
            "Cuatrimestre 5": periodo5,
            "Cuatrimestre 6": periodo6,
            "Cuatrimestre 7": periodo7,
            "Cuatrimestre 8": periodo8,
            "Cuatrimestre 9": periodo9,
            "Cuatrimestre 10": ["Estadía", None, None, None, None, None, None],
        },
    )'''


    return dataframe

def colorsAlumno(dataframe,materiasAprobadas,materiasReprobadas,materiasFaltantes):
    dataframeAprobado = definicionColor(materiasAprobadas,"green")
    dataframeReprobado = definicionColor(materiasReprobadas,"yellow")
    dataframeFaltantes = definicionColor(materiasFaltantes,"gray")

    styles = (
        [
            {
                'if': {
                    'column_id': x,
                    'filter_query': '{' + x + '}' + f' eq "{val}"'
                },
                'backgroundColor': background_color,
                'color': 'white'
            }
            for val, background_color
            in zip(dataframeAprobado['Nombre'].tolist(), dataframeAprobado['Color'].tolist()) for x in dataframe.columns.tolist()
        ] +
        [
            {
                'if': {
                    'column_id': x,
                    'filter_query': '{' + x + '}' + f' eq "{val}"'
                },
                'backgroundColor': background_color,
                'color': 'white'
            }
            for val, background_color
            in zip(dataframeFaltantes['Nombre'].tolist(), dataframeFaltantes['Color'].tolist()) for x in dataframe.columns.tolist()
        ] +
        [
            {
                'if': {
                    'column_id': x,
                    'filter_query': '{' + x + '}' + f' eq "{val}"'
                },
                'backgroundColor': background_color,
                'color': 'red'
            }
            for val, background_color
            in zip(dataframeReprobado['Nombre'].tolist(), dataframeReprobado['Color'].tolist()) for x in dataframe.columns.tolist()
        ]
    )

    return styles

def crearTabla(dataframeTabla,aprobado,reprobado,materiasFaltantes,idinput,listaCards):
    contenedorTabla = dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dash_table.DataTable(
                                id=idinput,
                                columns=[{"name": i, "id": i} for i in dataframeTabla.columns],
                                data=dataframeTabla.to_dict("records"),
                                style_header={
                                    'backgroundColor': 'rgb(30, 30, 30)',
                                    'color': 'white'
                                },
                                style_table={'overflowX': 'auto'},
                                style_cell={
                                    'font-family': 'cursive',
                                    'font-size': '12px',
                                    'text-align': 'center',
                                    'color': 'black'
                                },
                                style_data={
                                    'whiteSpace': 'normal',
                                    'height': 'auto',
                                    'color': 'black',
                                },
                                style_data_conditional=colorsAlumno(dataframeTabla, aprobado, reprobado, materiasFaltantes),
                                fill_width=True
                            )
                        ]
                    )
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        "Titulo", className="card-title", id=listaCards[0]
                                    ),
                                    html.P(
                                        "Objetivo",
                                        className="card-text",
                                        id=listaCards[1],
                                    ),
                                    html.P(
                                        "Horas A La Semana",
                                        className="card-text",
                                        id=listaCards[2],
                                    ),
                                    html.P(
                                        "Total De Horas",
                                        className="card-text",
                                        id=listaCards[3],
                                    ),
                                    html.P(
                                        "Seriacion",
                                        className="card-text",
                                        id=listaCards[4],
                                    ),
                                ]
                            )
                        )
                    ),
                ],
                className="mb-4",
            ),
        ]
    )

    cardInfo(dataframeTabla,idinput,listaCards)

    return contenedorTabla

def cardInfo(dataframe,idinput,listaCards): #el app es para el callback y el dataframe para obtener la columna
    lista = listadoMaterias(CLAVE)
    card_content = "Materia: "
    card_content2 = "Objetivo: "
    card_content3 = "Horas A La Semana:"
    card_content4 = "Total De Horas:"
    card_content5 = ""

    @callback(Output(listaCards[0], "children"), Input(idinput, "active_cell"))
    def update_card(slct_rows_names):
        if slct_rows_names:
            col = dataframe[slct_rows_names["column_id"]]
            val = col[slct_rows_names["row"]]
            return "Materia: " + str(val)
        return card_content

    @callback(Output(listaCards[1], "children"), Input(idinput, "active_cell"))
    def update_card(slct_rows_names):
        if slct_rows_names:
            col = dataframe[slct_rows_names["column_id"]]
            val = col[slct_rows_names["row"]]
            if val != None:
                Objetivo = lista[lista['Nombre'] == val]['Objetivo'].values[0]
                return "Objetivo: " + str(Objetivo)
        return card_content2

    @callback(Output(listaCards[2], "children"), Input(idinput, "active_cell"))
    def update_card(slct_rows_names):
        if slct_rows_names:
            col = dataframe[slct_rows_names["column_id"]]
            val = col[slct_rows_names["row"]]
            if val != None:
                horasSemana = lista[lista['Nombre'] == val]['HorasSemana'].values[0]
                return "Horas A La Semana: " + str(horasSemana)
        return card_content3

    @callback(Output(listaCards[3], "children"), Input(idinput, "active_cell"))
    def update_card(slct_rows_names):
        if slct_rows_names:
            col = dataframe[slct_rows_names["column_id"]]
            val = col[slct_rows_names["row"]]
            if val != None:
                totalHoras = lista[lista['Nombre'] == val]['TotalHoras'].values[0]
                return "Total De Horas: " + str(totalHoras)
        return card_content4

    @callback(Output(listaCards[4], "children"), Input(idinput, "active_cell"))
    def update_card(slct_rows_names):
        if slct_rows_names:
            col = dataframe[slct_rows_names["column_id"]]
            val = col[slct_rows_names["row"]]
            if val != None:
                seriado = lista[lista['Nombre'] == val]['TipoPrerequisito'].values[0]
                if seriado == "NO" or seriado == "":
                    return "La Materia No Esta Seriada"
                else:
                    if seriado != "PC":
                        dicc = pd.DataFrame(getRelations())
                        G = nx.from_pandas_edgelist(dicc, source='materia', target='depende', edge_attr=None,create_using=nx.DiGraph())
                        try:
                            antecesores = sorted(list(nx.ancestors(G, val)))  ##todos los anteriores
                        except:
                            return "La Materia No Esta Seriada"
                        return "La Materia Esta Seriada Con Las Siguientes Materias " + str(antecesores)
                    else:
                        return "Para Hacer La Estadia Necesitas Tener Liberado Las Materias"
        return card_content5

def definicionColor(tipoEstado,color):
    colorDefinicion = []

    for i in range(len(tipoEstado)):
        colorDefinicion.append(color)

    diccionario = {"Nombre": tipoEstado['Nombre'], "Color": colorDefinicion}
    dataframe = pd.DataFrame(diccionario)
    return dataframe