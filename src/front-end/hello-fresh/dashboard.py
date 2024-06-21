import pandas as pd
from dash import Dash, html, dcc, Input, Output, Patch, clientside_callback, callback
import plotly.express as px
import dash_bootstrap_components as dbc
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder
from dash.dependencies import Input, Output
from dash_bootstrap_templates import load_figure_template
import plotly.io as pio

# Load user interaction data
def load_user_interaction_data():
    return pd.DataFrame({
        'User ID': [1, 2, 3, 4, 5],
        'Sessions Initiated': [15, 10, 12, 8, 20],
        'Average Time per Session (min)': [12.5, 8.2, 10.6, 15.3, 7.8],
        'Favorite Recipes': ['Quinoa Salad, Spring Pasta', 'BBQ Burger, Margherita Pizza',
                             'Grilled Salmon, Tomato Soup', 'Tofu Tacos, Fruit Smoothie',
                             'Chicken Curry, Mushroom Risotto'],
        'Last Purchase': ['2023-07-10', '2023-07-12', '2023-07-11', '2023-07-09', '2023-07-08']
    })

# Preprocess user interaction data
def preprocess_user_interaction_data(user_interaction_df):
    label_encoder = LabelEncoder()
    encoded_user_interaction_data = user_interaction_df.copy()

    encoded_user_interaction_data['Favorite Recipes'] = label_encoder.fit_transform(encoded_user_interaction_data['Favorite Recipes'])
    encoded_user_interaction_data['Last Purchase'] = pd.to_datetime(encoded_user_interaction_data['Last Purchase'])
    encoded_user_interaction_data['Last Purchase'] = (encoded_user_interaction_data['Last Purchase'] - encoded_user_interaction_data['Last Purchase'].min()).dt.days
    
    return encoded_user_interaction_data

# Load delivery preferences data
def load_delivery_preferences_data():
    return pd.DataFrame({
        'User ID': [1, 2, 3, 4, 5],
        'Delivery Address': ['123 Main St, Toronto', '456 Maple Ave, Vancouver',
                             '789 Pine Rd, Montreal', '101 Oak St, Calgary',
                             '222 Elm St, Ottawa'],
        'Delivery Frequency': ['2 times per week', '3 times per week', '1 time per week',
                               '2 times per week', '4 times per week'],
        'Preferred Delivery Day': ['Tuesday and Friday', 'Monday, Wednesday, Friday',
                                   'Thursday', 'Wednesday and Saturday',
                                   'Monday, Tuesday, Thursday, Saturday']
    })

# Preprocess delivery preferences data
def preprocess_delivery_preferences_data(delivery_preferences_df):
    ordinal_encoder = OrdinalEncoder()
    encoded_delivery_preferences_data = delivery_preferences_df.copy()

    encoded_delivery_preferences_data['Delivery Frequency'] = ordinal_encoder.fit_transform(encoded_delivery_preferences_data[['Delivery Frequency']])
    encoded_delivery_preferences_data['Preferred Delivery Day'] = ordinal_encoder.fit_transform(encoded_delivery_preferences_data[['Preferred Delivery Day']])
   
    return encoded_delivery_preferences_data

# Load recipe preferences data
def load_recipe_preferences_data():
    return pd.DataFrame({
        'User ID': [1, 2, 3, 4, 5],
        'Preferred Category': ['Salads', 'Meats', 'Seafood', 'Vegan', 'International Dishes'],
        'Most Requested Recipes': ['Quinoa Salad, Caesar Salad', 'BBQ Burger, Teriyaki Chicken',
                                   'Grilled Salmon, Shrimp Ceviche', 'Fruit Smoothie, Garbanzo Bowl',
                                   'Chicken Curry, Sushi Rolls']
    })

# Preprocess recipe preferences data
def preprocess_recipe_preferences_data(recipe_preferences_df):
    label_encoder = LabelEncoder()
    encoded_recipe_preferences_data = recipe_preferences_df.copy()

    encoded_recipe_preferences_data['Preferred Category'] = label_encoder.fit_transform(encoded_recipe_preferences_data['Preferred Category'])
    
    return encoded_recipe_preferences_data

# Extract favorite recipes
def get_favorite_recipes(user_interaction_df):
    favorite_recipes = user_interaction_df['Favorite Recipes'].str.split(', ').explode().reset_index(drop=True)
    return favorite_recipes

# Extract preferred delivery days
def get_preferred_delivery_days(delivery_preferences_df):
    preferred_delivery_days = delivery_preferences_df['Preferred Delivery Day'].str.split(', ').explode().reset_index(drop=True)
    return preferred_delivery_days

# Extract most requested recipes
def get_most_requested_recipes(recipe_preferences_df):
    most_requested_recipes = recipe_preferences_df['Most Requested Recipes'].str.split(', ').explode().reset_index(drop=True)
    return most_requested_recipes

# Merge all processed data
def merge_data(user_interaction_df, delivery_preferences_df, recipe_preferences_df):
    merged_data = pd.merge(user_interaction_df, delivery_preferences_df, on='User ID')
    merged_data = pd.merge(merged_data, recipe_preferences_df, on='User ID')

    merged_data['Last Purchase'] = pd.to_datetime(merged_data['Last Purchase'])
    merged_data['Last Purchase'] = (merged_data['Last Purchase'] - merged_data['Last Purchase'].min()).dt.days

    merged_data.drop(columns=['Most Requested Recipes', 'Delivery Address'], inplace=True, errors='ignore')

    return merged_data

# Initialize Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY, dbc.icons.FONT_AWESOME], suppress_callback_exceptions=True)
app.title = "AutoBasket Data Dashboard"

# adds  templates to plotly.io
load_figure_template(["minty", "minty_dark"])

# Initialize data
user_interaction_df = load_user_interaction_data()
encoded_user_interaction_df = preprocess_user_interaction_data(user_interaction_df)

delivery_preferences_df = load_delivery_preferences_data()
encoded_delivery_preferences_df = preprocess_delivery_preferences_data(delivery_preferences_df)

recipe_preferences_df = load_recipe_preferences_data()
encoded_recipe_preferences_df = preprocess_recipe_preferences_data(recipe_preferences_df)

merged_data = merge_data(encoded_user_interaction_df, encoded_delivery_preferences_df, encoded_recipe_preferences_df)

color_mode_switch =  html.Span(
    [
        dbc.Label(className="fa fa-moon", html_for="color-mode-switch"),
        dbc.Switch( id="color-mode-switch", value=False, className="d-inline-block ms-1", persistence=True),
        dbc.Label(className="fa fa-sun", html_for="color-mode-switch"),
    ]
)

# Define layout
app.layout = dbc.Container([
    html.H1("AutoBasket Data Dashboard", className="my-4 text-center"),
    
    dcc.Tabs(id='tabs', children=[
        dcc.Tab(label='User Interaction Data', children=[
            dbc.Row([
                dbc.Col(dcc.Graph(
                    id='sessions-vs-time',
                    figure=px.scatter(encoded_user_interaction_df, x='Sessions Initiated', y='Average Time per Session (min)', color='User ID')
                ), md=6),
                
                dbc.Col(dcc.Graph(
                    id='favorite-recipes-count',
                    figure=px.bar(get_favorite_recipes(user_interaction_df).value_counts().reset_index(), x='Favorite Recipes', y='count', labels={'index': 'Recipe', 'Favorite Recipes': 'Count'}, title='Favorite Recipes Count')
                ), md=6),
            ]),
        ]),
        
        dcc.Tab(label='Delivery Preferences', children=[
            dbc.Row([
                dbc.Col(dcc.Graph(
                    id='delivery-frequency-distribution',
                    figure=px.histogram(encoded_delivery_preferences_df, x='Delivery Frequency', title='Delivery Frequency Distribution')
                ), md=6),
                
                dbc.Col(dcc.Graph(
                    id='preferred-delivery-days',
                    figure=px.bar(get_preferred_delivery_days(delivery_preferences_df).value_counts().reset_index(), x='Preferred Delivery Day', y='count', labels={'index': 'Day', 'Preferred Delivery Day': 'Count'}, title='Preferred Delivery Days')
                ), md=6),
            ]),
        ]),
        
        dcc.Tab(label='Recipe Preferences', children=[
            dbc.Row([
                dbc.Col(dcc.Graph(
                    id='most-requested-recipes',
                    figure=px.bar(get_most_requested_recipes(recipe_preferences_df).value_counts().reset_index(), x='Most Requested Recipes', y='count', labels={'index': 'Recipe', 'Most Requested Recipes': 'Count'}, title='Most Requested Recipes')
                ), md=6),
                
                dbc.Col(dcc.Graph(
                    id='preferred-category-distribution',
                    figure=px.histogram(encoded_recipe_preferences_df, x='Preferred Category', title='Preferred Category Distribution')
                ), md=6),
            ]),
        ]),
        
        dcc.Tab(label='Combined Data', children=[
            dbc.Row([
                dbc.Col(dcc.Graph(
                    id='user-interaction-vs-delivery',
                    figure=px.scatter(merged_data, x='Sessions Initiated', y='Average Time per Session (min)', color='Delivery Frequency', size='Preferred Category', title='User Interaction vs Delivery Preferences')
                ), md=6),
                
                dbc.Col(dcc.Graph(
                    id='correlation-matrix',
                    figure=px.imshow(merged_data.corr(), text_auto=True, title='Correlation Matrix')
                ), md=6),
            ]),
        ]),
    ]),
], fluid=True)

@callback(
    Output("graph", "figure"),
    Input("color-mode-switch", "value"),
)

def update_figure_template(switch_on):
    # When using Patch() to update the figure template, you must use the figure template dict
    # from plotly.io  and not just the template name
    template = pio.templates["minty"] if switch_on else pio.templates["minty_dark"]

    patched_figure = Patch()
    patched_figure["layout"]["template"] = template
    return patched_figure

clientside_callback(
    """
    (switchOn) => {
       document.documentElement.setAttribute('data-bs-theme', switchOn ? 'light' : 'dark');  
       return window.dash_clientside.no_update
    }
    """,
    Output("color-mode-switch", "id"),
    Input("color-mode-switch", "value"),
)

if __name__ == '__main__':
    app.run_server(debug=True)
