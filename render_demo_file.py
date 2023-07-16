import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html

color_legend_world_cup = {
    'Champion': 'blue',
    'Finalist': 'lightblue',
    'Semifinals': 'green',
    'Quarterfinals': 'lightgreen',
    '2nd Round': 'orange',
    '1nd Round': 'yellow'
}

color_legend_UEFA = {
    'Champion': 'blue',
    'Finalist': 'lightblue',
    'Semifinals': 'green',
    'Quarterfinals': 'lightgreen',
    'Group stage': 'orange',
}

color_legend_world_cup_men = {
    'Champion': 'blue',
    'Finalist': 'lightblue',
    'Semifinals': 'green',
    'Quarterfinals': 'lightgreen',
    '2nd Round': 'orange',
    '1nd Round': 'yellow'
}

df = pd.read_csv('/Users/abdulnaser/Desktop/render_demo_new/results.csv')  # Replace 'results.csv' with the actual file path or DataFrame name
UEFA_women_transformed_data = pd.read_csv('/Users/abdulnaser/Desktop/render_demo_new/UEFA_women_transformed_data.csv')
world_cup_transformed_data = pd.read_csv('/Users/abdulnaser/Desktop/render_demo_new/world_cup_transformed_data.csv')


df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year

teams = list(set(df['tournament'].unique()))
teams.sort(key=lambda x: (x != 'FIFA World Cup', x != 'UEFA Euro'))


app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        dcc.Dropdown(
            id='tournament-dropdown',
            options=[{'label': team, 'value': team} for team in teams],
            value=None,
            placeholder='Select a tournament'
        ),
        dcc.Graph(id='map-first')
    ]
)



@app.callback(
    dash.dependencies.Output('map-first', 'figure'),
    [dash.dependencies.Input('tournament-dropdown', 'value')]
)
def update_map_first(selected_tournament):
        tournament_data = df[df['tournament'] == selected_tournament]

        filtered_data = pd.DataFrame(columns=['Country', 'total_times'])

        d = tournament_data.groupby(['tournament', 'country', 'year']).size().reset_index()[['tournament', 'country', 'year']]
        d = d.groupby(['tournament', 'country']).size().reset_index()
        d.rename(columns={0: 'count'}, inplace=True)

        fig_map = px.choropleth(d, locations="country", locationmode='country names',
                                hover_name="country", color="count",
                                color_continuous_scale='RdBu')

        fig_map.update_layout(title='Hosting Countries(Women)'.format(selected_tournament))
        return fig_map


if __name__ == '__main__':
    app.run_server(debug=True)

