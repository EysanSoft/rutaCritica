import dash_bootstrap_components as dbc
import dash_table
from dash import html
from dash.dash_table.Format import Format

from app.src.Dash.components.reinscription.relationDependencias import colorsAlumno


def mostrarPosibleRuta(dataframeTabla,rutacritica,idinput):
    contenedorTabla = dash_table.DataTable(
        id=idinput,
        data=dataframeTabla.to_dict("records"),
        #columns=[{"name": i, "id": i} for i in dataframeTabla.columns],
        columns=[
            {
                'name': i,
                'id': i,
                'type': 'numeric',
                'format': Format(
                    nully='N/A'
                )
            } for i in dataframeTabla.columns
        ],
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
        style_data_conditional=colorsAlumno(dataframeTabla, rutacritica),
        fill_width=True
    )

    return contenedorTabla