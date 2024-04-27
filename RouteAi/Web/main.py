from dash import Dash, Input, Output, html, dcc, State
import dash_bootstrap_components as dbc
import sqlite3
import base64
from dash.exceptions import PreventUpdate
import logging
import dash


# Initialize the database
def init_db():
    conn = sqlite3.connect('pothole_data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS potholes (
            id INTEGER PRIMARY KEY,
            adresse TEXT,
            postal TEXT,
            type_road TEXT,
            message TEXT,
            image BLOB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def get_navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Client", href="/")),
            dbc.NavItem(dbc.NavLink("Employé", href="/dashboard")),
        ],
        brand="Pothole Reporting",
        brand_href="/",
        color="primary",
        dark=True,
    )
    return navbar

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    get_navbar(),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/dashboard':
        return dashboard_layout()
    else:
        return contact_form()

def contact_form():
    return html.Div([
        html.H1('RoutAi', style={'textAlign': 'center', 'color': 'blue'}),
        dbc.Container([
            dcc.Markdown('# Décrivez nous votre nid de poule!'),
            html.Br(),
            dbc.Card(
                dbc.CardBody([
                    dbc.Form([
                        adresse_input(),
                        postal_input(),
                        type_road_input(),
                        img_input(),
                        message_input()
                    ]),
                    html.Div(id='div-buttons', children=[
                        dbc.Button('Envoyer', color='primary', id='button-submit', n_clicks=0),
                        html.Span(' '),  # This adds spacing between the buttons.
                        dbc.Button('Recommencer', color='secondary', id='button-reset', n_clicks=0),
                    ]),
                ])
            ),
            html.Br()
        ])
    ])


def adresse_input():
    return dbc.Row([
        dbc.Label("Adresse", html_for="example-adresse-row", width=2),
        dbc.Col(dbc.Input(type="text", id="example-adresse-row", placeholder="Donnez l'adresse du nid de poule"), width=10),
    ], className="mb-3")

def postal_input():
    return dbc.Row([
        dbc.Label("Code Postal", html_for="example-code-postal-row", width=2),
        dbc.Col(dbc.Input(type="text", id="example-code-postal-row", placeholder="Donnez le Code Postal du nid de poule"), width=10),
    ], className="mb-3")

def img_input():
    return dbc.Row([
        dbc.Label("Photo du nid de poule", html_for="example-img-row", width=2),
        dbc.Col(dcc.Upload(['Drag and Drop or ', html.A('Select Files')], id="example-img-row", style={
            'width': '100%', 'height': '60px', 'lineHeight': '60px',
            'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
            'textAlign': 'center'
        }, multiple=False, accept=".jpg"), width=10),
    ], className="mb-3")

def type_road_input():
    return dbc.Row([
        dbc.Label("Type de route", html_for="example-type-road-row", width=2),
        dbc.Col(dbc.Select(id="example-type-road-row", options=[
            {"label": "Artère Principale", "value": "Artère Principale"},
            {"label": "Rue Collectrice", "value": "Rue Collectrice"},
            {"label": "Rue Locale", "value": "Rue Locale"}
        ], value="Artère Principale"), width=10),
    ], className="mb-3")

def message_input():
    return dbc.Row([
        dbc.Label("Message", html_for="example-message-row", width=2),
        dbc.Col(dbc.Textarea(id="example-message-row", className="mb-3", placeholder="Enter message", required=True), width=10),
    ], className="mb-3")


@app.callback(
    [Output('example-adresse-row', 'value'),
     Output('example-code-postal-row', 'value'),
     Output('example-type-road-row', 'value'),
     Output('example-message-row', 'value'),
     Output('example-img-row', 'contents')],
    [Input('button-reset', 'n_clicks')]
)
def reset_form(n_clicks):
    if n_clicks > 0:
        # Returning '' will reset the text inputs, 'None' will reset the upload component
        return '', '', 'Artère Principale', '', None
    raise PreventUpdate

@app.callback(
    Output('div-buttons', 'children'),
    [Input("button-submit", 'n_clicks'),
     Input("button-reset", 'n_clicks')],
    [State("example-adresse-row", 'value'),
     State("example-code-postal-row", 'value'),
     State("example-img-row", 'contents'),
     State("example-type-road-row", 'value'),
     State("example-message-row", 'value')]
)
def submit_message(n_clicks_submit, n_clicks_reset, adresse, postal, img_contents, type_road, message):
    ctx = dash.callback_context

    if not ctx.triggered:
        button_id = 'No clicks yet'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == "button-submit" and n_clicks_submit > 0:
        if img_contents:
            # Extract content part of the file upload
            content_type, content_string = img_contents.split(',')
            img_blob = base64.b64decode(content_string)
        else:
            img_blob = None  # Handle case where no image is provided
        
        conn = sqlite3.connect('pothole_data.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO potholes (adresse, postal, type_road, message, image) VALUES (?, ?, ?, ?, ?)
        ''', (adresse, postal, type_road, message, img_blob))
        conn.commit()
        conn.close()
        logging.info(f"Message submitted: {adresse}, {postal}, {type_road}, {message}")
        return [html.P("Message Sent"), dbc.Button('Recommencer', color='secondary', id='button-reset', n_clicks=0)]
    elif button_id == "button-reset" and n_clicks_reset > 0:
        # Logic for reset, which could simply be the same buttons without the "Message Sent" text
        return [dbc.Button('Envoyer', color='primary', id='button-submit', n_clicks=0), html.Span(' '), dbc.Button('Recommencer', color='secondary', id='button-reset', n_clicks=0)]

    # If no button was clicked, return the default layout for buttons
    return [dbc.Button('Envoyer', color='primary', id='button-submit', n_clicks=0), html.Span(' '), dbc.Button('Recommencer', color='secondary', id='button-reset', n_clicks=0)]


def dashboard_layout():
    return html.Div([
        html.H1('Dashboard', style={'textAlign': 'center'}),
        # Add dashboard components here, such as displaying the data
    ])



if __name__ == "__main__":
    app.run_server(debug=True)
