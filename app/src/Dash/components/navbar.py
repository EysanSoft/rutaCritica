import dash
import dash_bootstrap_components as dbc

def Navbar():
    navbar = dbc.NavbarSimple(
        dbc.DropdownMenu(
            [
                dbc.DropdownMenuItem(page["name"], href=page["path"])
                for page in dash.page_registry.values()
                if page["module"] != "pages.not_found_404"
            ],
            nav=True,
            label="Despliega Aca",
        ),
        brand="Universidad Politecnica De Chiapas",
        brand_href="https://google.com",
        color="dark",
        dark=True,
        className="mb-2",
    )

    return navbar