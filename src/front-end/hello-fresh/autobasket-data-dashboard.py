
# Create an interactive web-based data dashboard
import dash
import pandas as pd
from dash import dcc, html
import plotly.express as px
import plotly.graph_objs as go
from dash.dependencies import Input, Output

# Init Data File Path
data_file_path = '../../../data/generated/hello-fresh/'

# Import Data
user_interaction_df = pd.read_parquet(f'{data_file_path}user_interaction_data.parquet')
delivery_preferences_df = pd.read_parquet(f'{data_file_path}delivery_preferences.parquet')
recipe_preferences_df = pd.read_parquet(f'{data_file_path}recipe_preferences.parquet')

merged_data = pd.read_parquet('../../../data/generated/hello-fresh/merged_data.parquet')

# Filter Data
favorite_recipes = user_interaction_df['Favorite Recipes'].str.split(', ', expand=True).stack().reset_index(level=1, drop=True).to_frame('Recipe')
preferred_days = delivery_preferences_df['Preferred Delivery Day'].str.split(', ', expand=True).stack().reset_index(level=1, drop=True).to_frame('Day')
most_requested_recipes = recipe_preferences_df['Most Requested Recipes'].str.split(', ', expand=True).stack().reset_index(level=1, drop=True).to_frame('Recipe')
corr = merged_data.corr()

# Create a Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("AutoBasket Data Dashboard"),
    dcc.Tabs(id='tabs', children=[
        dcc.Tab(label='User Interaction Data', children=[
            dcc.Graph(
                id='sessions-vs-time',
                figure=px.scatter(user_interaction_df, x='Sessions Initiated', y='Average Time per Session (min)', color='User ID')
            ),
            dcc.Graph(
                id='favorite-recipes-count',
                figure=px.bar(favorite_recipes['Recipe'].value_counts().reset_index(), x='index', y='Recipe', labels={'index': 'Recipe', 'Recipe': 'Count'}, title='Favorite Recipes Count')
            )
        ]),
        dcc.Tab(label='Delivery Preferences', children=[
            dcc.Graph(
                id='delivery-frequency-distribution',
                figure=px.histogram(delivery_preferences_df, x='Delivery Frequency', title='Delivery Frequency Distribution')
            ),
            dcc.Graph(
                id='preferred-delivery-days',
                figure=px.bar(preferred_days['Day'].value_counts().reset_index(), x='index', y='Day', labels={'index': 'Day', 'Day': 'Count'}, title='Preferred Delivery Days')
            )
        ]),
        dcc.Tab(label='Recipe Preferences', children=[
            dcc.Graph(
                id='most-requested-recipes',
                figure=px.bar(most_requested_recipes['Recipe'].value_counts().reset_index(), x='index', y='Recipe', labels={'index': 'Recipe', 'Recipe': 'Count'}, title='Most Requested Recipes')
            ),
            dcc.Graph(
                id='preferred-category-distribution',
                figure=px.histogram(recipe_preferences_df, x='Preferred Category', title='Preferred Category Distribution')
            )
        ]),
        dcc.Tab(label='Combined Data', children=[
            dcc.Graph(
                id='user-interaction-vs-delivery',
                figure=px.scatter(merged_data, x='Sessions Initiated', y='Average Time per Session (min)', color='Delivery Frequency', size='Preferred Category', title='User Interaction vs Delivery Preferences')
            ),
            dcc.Graph(
                id='correlation-matrix',
                figure=px.imshow(corr, text_auto=True, title='Correlation Matrix')
            )
        ])
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)