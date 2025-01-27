from dash import Dash, html

# Inicializácia aplikácie
app = Dash(__name__)

# Nastavenie vzhľadu aplikácie
app.layout = html.Div([
    html.H1("Vitaj na mojej prvej Dash aplikácii!"),
    html.P("Toto je základný text.")
])

# Spustenie servera
if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8000)

