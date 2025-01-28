from dash import Dash, html, dcc, Input, Output
import plotly.graph_objects as go

# Inicializácia aplikácie
app = Dash(__name__) 

# Funkcia na výpočet návratnosti
def vypocitaj_navratnost(percento_vlastnej_spotreby, velkost_baterie):
    # Konštanty
    rocna_vyroba = 10_000  # 10 MWh
    cena_energie = 165  # €/MWh
    cena_virtualnej_baterie = 36  # €/rok
    cena_fyzickej_baterie = 3900  # €

    # Výpočty  
    vlastna_spotreba = percento_vlastnej_spotreby / 100 * rocna_vyroba
    uspora_vlastna = vlastna_spotreba * cena_energie / 1000  # €/rok

    zvysok_energie = rocna_vyroba - vlastna_spotreba
    uspora_virtualna = zvysok_energie * 105 / 1000  # €/rok (rozdiel medzi 165 a 60 €/MWh)
    celkova_uspora = uspora_vlastna + uspora_virtualna - cena_virtualnej_baterie

    # Investície
    investicia = 6100  # € (po dotácii)
    if velkost_baterie > 0:
        investicia += cena_fyzickej_baterie

    # Návratnosť v rokoch
    navratnost = investicia / celkova_uspora
    return navratnost

# Layout aplikácie
app.layout = html.Div([
    html.H1("Návratnosť investície do fotovoltiky"),
    html.Label("Percento vlastnej spotreby:"),
    dcc.Slider(
        id="slider-spotreba",
        min=50,
        max=100,
        step=5,
        value=75,
        marks={i: f"{i}%" for i in range(50, 101, 10)},
    ),
    html.Label("Veľkosť batérie (kWh):"),
    dcc.Slider(
        id="slider-bateria",
        min=0,
        max=15,
        step=5,
        value=0,
        marks={0: "Bez batérie", 5: "5 kWh", 10: "10 kWh", 15: "15 kWh"}
    ),
    dcc.Graph(id="graf-navratnosti")
])

# Callback na aktualizáciu grafu
@app.callback(
    Output("graf-navratnosti", "figure"),
    [Input("slider-spotreba", "value"),
     Input("slider-bateria", "value")]
)
def aktualizuj_graf(percento_vlastnej_spotreby, velkost_baterie):
    navratnost = vypocitaj_navratnost(percento_vlastnej_spotreby, velkost_baterie)

    # Graf
    fig = go.Figure(
        data=[go.Bar(x=["Návratnosť investície"], y=[navratnost], text=[f"{navratnost:.2f} roka"], textposition="auto")]
    )
    fig.update_layout(
        title="Návratnosť investície (v rokoch)",
        yaxis=dict(title="Roky"),
        xaxis=dict(title=""),
        template="plotly_white"
    )
    return fig

# Spustenie servera
if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8000)

