import pandas as pd
import dash_html_components as html
import dash_table

def diccionarioSimbologia(df):
    listaColores = ['#008000','#CDCDCD', 'yellow', 'red'] #rojo #CC6666 verde #008000 gris #cdcdcd
    dataframe = pd.DataFrame({
        "estadoSimbologia":df.columns,
        "colorSimbologia":listaColores,
    })
    return dataframe

def creacionDataframeSimbologia():
    df = pd.DataFrame(
        columns=['Materias Aprobadas', 'Materias Faltantes', 'Materias Reprobadas', "Ruta Critica"],
        data=[['', '', '','']]
    )
    return df

def colorSimbologia(simbologia):
    styles2 = [{'if': {'filter_query': '{' + val + '} is blank', 'column_id': val},
                'backgroundColor': background_color, 'color': 'white'} for val, background_color
               in zip(simbologia['estadoSimbologia'].tolist(), simbologia['colorSimbologia'].tolist())
               ]

    return styles2

def margenSimbologia():
    CONTENT_STYLE = {
        "margin-left": "3rem",
        "margin-right": "3rem",
        "padding": "3rem 3rem",
    }
    return CONTENT_STYLE

def tablaSimbologia(dataframe,simbologia):
    return html.Div([dash_table.DataTable(
                id='tablaGeneral',
                columns=[{'name': i, 'id': i} for i in dataframe.columns],
                data=dataframe.to_dict('records'),
                style_header={
                    'backgroundColor': 'rgb(30, 30, 30)',
                    'color': 'white'
                },
                style_table={'overflowX': 'auto'},
                style_cell={
                    'font-family': 'cursive',
                    'font-size': '12px',
                    'text-align': 'center',
                    'color': 'black',
                },
                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                },
                style_data_conditional=colorSimbologia(simbologia),#creacionSimbologia(df),
                fill_width=False
            )])