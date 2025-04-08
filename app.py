from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

themes = [
    "Automation", "Robotics", "Safety", "Materials & Sustainability", "Pre-fabrication",
    "Software & AI Tools", "Foreign Labor & Underrepresented Groups", "Advanced BIM",
    "Age Demographics", "Gender Inclusion", "Workforce Integration", "Training & Adaptation"
]

options = [
    {'label': 'Scenario 1 (a)', 'value': 'a'},
    {'label': 'Scenario 2 (b)', 'value': 'b'},
    {'label': 'Scenario 3 (c)', 'value': 'c'}
]

def layout_row(theme):
    return dbc.Row([
        dbc.Col(html.Div(theme), width=4),
        dbc.Col(dcc.Dropdown(id=f"current-{theme}", options=options, placeholder="Current State"), width=3),
        dbc.Col(dcc.Dropdown(id=f"desired-{theme}", options=options, placeholder="Desired State"), width=3),
        dbc.Col(html.Div(id=f"gap-{theme}"), width=2)
    ], className='mb-2')

app.layout = html.Div([
    html.H2("Scenario Readiness Self-Assessment Tool"),
    html.Hr(),
    html.Div([layout_row(theme) for theme in themes]),
    html.Br(),
    dbc.Button("Calculate Summary", id="calc-btn", color="primary"),
    html.Div(id="summary-output", className='mt-4')
])

@app.callback(
    Output("summary-output", "children"),
    [Input("calc-btn", "n_clicks")],
    [State(f"current-{theme}", "value") for theme in themes] +
    [State(f"desired-{theme}", "value") for theme in themes]
)
def calculate_summary(n_clicks, *values):
    if not n_clicks:
        return ""
    current_values = values[:len(themes)]
    desired_values = values[len(themes):]
    scenario_match = {"a": 0, "b": 0, "c": 0}
    total_gap = 0

    for cur, des in zip(current_values, desired_values):
        if not cur or not des:
            continue
        scenario_match[cur] += 1
        gap = abs(ord(cur) - ord(des))
        total_gap += gap

    best_fit = max(scenario_match, key=scenario_match.get)
    label_map = {
        "a": "Scenario 1: Technological Utopia",
        "b": "Scenario 2: Tech-Workforce Equilibrium",
        "c": "Scenario 3: Conservative Advancement"
    }

    return html.Div([
        html.H5("Assessment Summary:"),
        html.P(f"Your most aligned scenario based on current state: {label_map[best_fit]}"),
        html.P(f"Total Gap Score: {total_gap}"),
        html.P("Use these insights to inform your future workforce strategy.")
    ])

if __name__ == '__main__':
    app.run_server(debug=True)
