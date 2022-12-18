import os
import webbrowser
from threading import Thread, Timer
import dash
import dash_bootstrap_components as dbc
from app.src.Dash.components.navbar import Navbar

def open_browser(puerto):
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        cadena = 'http://127.0.0.1:'+str(puerto)+"/"
        try:
            webbrowser.open_new(cadena)
        except:
            print("No se pudo abrir el navegador")

def panelGeneral(puerto):
    Thread(target=ejecutarAplicacion, args=(puerto,), daemon=True).start()
    Timer(1, open_browser(puerto)).start()

def ejecutarAplicacion(puerto):
    #instancio la app dash
    app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

    #creo el navbar
    navbar = Navbar()

    #inicializo el napbar
    app.layout = dbc.Container(
        [navbar, dash.page_container],
        fluid=True,
    )

    #ejecuto la aplicacion
    app.run_server(port=puerto, debug=False, use_reloader=False)