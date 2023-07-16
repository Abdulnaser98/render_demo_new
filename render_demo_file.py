import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import panel as pn

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
men_world_cup_transformed_data = pd.read_csv('/Users/abdulnaser/Desktop/render_demo_new/men_world_cup_transformed_data.csv')


df['date'] = pd.to_datetime(df['date'])

# Extract the year from the 'Date' column
df['year'] = df['date'].dt.year

# Get unique values for home_team and away_team
teams = list(set(df['tournament'].unique()))

# Sort the teams list to have 'FIFA World Cup' and 'UEFA Euro' as the first two choices
teams.sort(key=lambda x: (x != 'FIFA World Cup', x != 'UEFA Euro'))

# Create dropdown widget for selecting a team
tournament_dropdown = pn.widgets.Select(name='Select a tournament:', options=teams, sizing_mode='stretch_width')

# Create output widgets for displaying the line chart and the map
output_map_first = pn.pane.Plotly(sizing_mode='stretch_both', height=400)
output_map_second = pn.pane.Plotly(sizing_mode='stretch_both')
output_map_third = pn.pane.Plotly(sizing_mode='stretch_both')

# Create function to update the line chart and the map based on team selection
def update_dashboard(event):
    selected_tournament = event.new
    if selected_tournament:
        # Filter the DataFrame based on selected_team as home_team or away_team
        tournament_data = df[df['tournament'] == selected_tournament]

        # Create an empty DataFrame to store the filtered tournament_data for the map
        filtered_data = pd.DataFrame(columns=['Country','total_times'])

        d = tournament_data.groupby(['tournament','country','year']).size().reset_index()[['tournament','country','year']]

        d = d.groupby(['tournament','country']).size().reset_index()

        d.rename(columns={0: 'count'}, inplace=True)

        # Create the choropleth map
        fig_map = px.choropleth(d, locations="country", locationmode='country names',
                                hover_name="country", color="count",
                                color_continuous_scale='RdBu')

        fig_map.update_layout(title='Hosting Countries(Women)'.format(selected_tournament))
        output_map_first.object = fig_map

        if selected_tournament == 'FIFA World Cup':
            fig = px.choropleth(world_cup_transformed_data, locations="Team", locationmode='country names',
                    color=world_cup_transformed_data['score'], hover_name="Team",
                    title='Color and Score', hover_data=['score'],
                    color_discrete_map=color_legend_world_cup)
            fig.update_layout(title='Countries Best results(Women)'.format(selected_tournament))
            output_map_second.object = fig

            fig2 = px.choropleth(men_world_cup_transformed_data, locations="Team", locationmode='country names',
                    color=men_world_cup_transformed_data['score'], hover_name="Team",
                    title='Countries Best result(Men)', hover_data=['score'],
                    color_discrete_map=color_legend_world_cup_men)
            output_map_third.object = fig2

        if selected_tournament == 'UEFA Euro':
            fig = px.choropleth(UEFA_women_transformed_data, locations="Team", locationmode='country names',
                    color=UEFA_women_transformed_data['score'], hover_name="Team",
                    title='Color and Score', hover_data=['score'],
                    color_discrete_map=color_legend_UEFA)
            fig.update_layout(title='Countries Best results'.format(selected_tournament))
            output_map_second.object = fig




# Call the update_dashboard function when the team selection changes
tournament_dropdown.param.watch(update_dashboard, 'value')

# Create a Panel layout with a vertical structure
dashboard = pn.Column(
    tournament_dropdown,
    pn.Row(
        output_map_second,
        output_map_third,
        sizing_mode='stretch_width',
    ),
    pn.Row(
        output_map_first,
        sizing_mode='stretch_width'
    ),
    sizing_mode='stretch_both',
    css_classes=['dashboard-container'],
    align='start'  # Align the components horizontally
)

# Add custom CSS styles to increase the size of the dashboard
pn.config.raw_css.append('.dashboard-container { width: 1500px; height: 1000px; }')

# Start the Panel app
dashboard.show()
