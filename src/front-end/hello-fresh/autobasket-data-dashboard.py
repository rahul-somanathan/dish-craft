
# Create an interactive web-based data dashboard
import dash
import pandas as pd
from dash import dcc, html
import plotly.express as px
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from sklearn.calibration import LabelEncoder
from sklearn.preprocessing import OrdinalEncoder

global user_interaction_df 
global delivery_preferences_df 
global recipe_preferences_df 
global merged_data 
global corr 
global favorite_recipes
global preferred_days 
global most_requested_recipes 

# Function to load user interaction data
def load_user_interaction_data():
    user_interaction_df = pd.DataFrame({
        'User ID': [1, 2, 3, 4, 5],
        'Sessions Initiated': [15, 10, 12, 8, 20],
        'Average Time per Session (min)': [12.5, 8.2, 10.6, 15.3, 7.8],
        'Favorite Recipes': ['Quinoa Salad, Spring Pasta', 'BBQ Burger, Margherita Pizza',
                             'Grilled Salmon, Tomato Soup', 'Tofu Tacos, Fruit Smoothie',
                             'Chicken Curry, Mushroom Risotto'],
        'Last Purchase': ['2023-07-10', '2023-07-12', '2023-07-11', '2023-07-09', '2023-07-08']
    })
    return user_interaction_df

# Function to preprocess user interaction data
def preprocess_user_interaction_data(user_interaction_df):
    label_encoder = LabelEncoder()

    encoded_user_interaction_data = user_interaction_df.copy()

    encoded_user_interaction_data['Favorite Recipes'] = label_encoder.fit_transform(encoded_user_interaction_data['Favorite Recipes'])
    encoded_user_interaction_data['Last Purchase'] = pd.to_datetime(encoded_user_interaction_data['Last Purchase'])
    encoded_user_interaction_data['Last Purchase'] = (encoded_user_interaction_data['Last Purchase'] - encoded_user_interaction_data['Last Purchase'].min()).dt.days
    
    return encoded_user_interaction_data

# Function to load delivery preferences data
def load_delivery_preferences_data():
    delivery_preferences_df = pd.DataFrame({
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
    return delivery_preferences_df

# Function to preprocess delivery preferences data
def preprocess_delivery_preferences_data(delivery_preferences_df):
    ordinal_encoder = OrdinalEncoder()

    encoded_delivery_preferences_data = delivery_preferences_df.copy()

    encoded_delivery_preferences_data['Delivery Frequency'] = ordinal_encoder.fit_transform(encoded_delivery_preferences_data[['Delivery Frequency']])
    encoded_delivery_preferences_data['Preferred Delivery Day'] = ordinal_encoder.fit_transform(encoded_delivery_preferences_data[['Preferred Delivery Day']])
   
    return encoded_delivery_preferences_data

# Function to load recipe preferences data
def load_recipe_preferences_data():
    recipe_preferences_df = pd.DataFrame({
        'User ID': [1, 2, 3, 4, 5],
        'Preferred Category': ['Salads', 'Meats', 'Seafood', 'Vegan', 'International Dishes'],
        'Most Requested Recipes': ['Quinoa Salad, Caesar Salad', 'BBQ Burger, Teriyaki Chicken',
                                   'Grilled Salmon, Shrimp Ceviche', 'Fruit Smoothie, Garbanzo Bowl',
                                   'Chicken Curry, Sushi Rolls']
    })
    return recipe_preferences_df

# Function to preprocess recipe preferences data
def preprocess_recipe_preferences_data(recipe_preferences_df):
    label_encoder = LabelEncoder()
    
    encoded_recipe_preferences_data = recipe_preferences_df.copy()

    encoded_recipe_preferences_data['Preferred Category'] = label_encoder.fit_transform(encoded_recipe_preferences_data['Preferred Category'])
    
    return encoded_recipe_preferences_data

def get_favorite_recipes(user_interaction_df):
    # Favorite Recipes Count
    favorite_recipes = user_interaction_df['Favorite Recipes'].str.split(', ', expand=True).stack().reset_index(level=1, drop=True).to_frame('Recipe')
    return favorite_recipes

def get_prefered_days(delivery_preferences_df):
    # Preferred Delivery Days
    preferred_days = delivery_preferences_df['Preferred Delivery Day'].str.split(', ', expand=True).stack().reset_index(level=1, drop=True).to_frame('Day')
    return preferred_days

def get_most_requested_recipes(recipe_preferences_df):
    # Most Requested Recipes
    most_requested_recipes = recipe_preferences_df['Most Requested Recipes'].str.split(', ', expand=True).stack().reset_index(level=1, drop=True).to_frame('Recipe')
    return most_requested_recipes

def get_merged_data(encoded_user_interaction_data, encoded_delivery_preferences_data, encoded_recipe_preferences_data):
    # Merge encoded dataframes based on 'User ID'
    merged_data = pd.merge(encoded_user_interaction_data, encoded_delivery_preferences_data, on='User ID')
    merged_data = pd.merge(merged_data, encoded_recipe_preferences_data, on='User ID')

    # Convert 'Last Purchase' to numeric (days since a reference date)
    merged_data['Last Purchase'] = pd.to_datetime(merged_data['Last Purchase'])
    merged_data['Last Purchase'] = (merged_data['Last Purchase'] - merged_data['Last Purchase'].min()).dt.days

    # Drop columns 'Most Requested Recipes' and 'Delivery Address'
    columns_to_drop = ['Most Requested Recipes', 'Delivery Address']
    merged_data = merged_data.drop(columns=columns_to_drop, errors='ignore')

    return merged_data

def get_merged_data_corr(merged_data):
    return merged_data.corr()

def init_data():
    user_interaction_df = load_user_interaction_data()
    delivery_preferences_df = load_delivery_preferences_data()
    recipe_preferences_df = load_recipe_preferences_data()

    favorite_recipes = get_favorite_recipes(user_interaction_df)
    most_requested_recipes = get_most_requested_recipes(recipe_preferences_df)
    preferred_days = get_prefered_days(delivery_preferences_df)
    
    encoded_user_interaction_data = preprocess_user_interaction_data(user_interaction_df)
    encoded_delivery_preferences_data = preprocess_delivery_preferences_data(delivery_preferences_df)
    encoded_recipe_preferences_data = preprocess_recipe_preferences_data(recipe_preferences_df)

    merged_data = get_merged_data(encoded_user_interaction_data, encoded_delivery_preferences_data, encoded_recipe_preferences_data)
    corr = get_merged_data_corr(merged_data)

init_data()

# Initialize the Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout using Bootstrap components for better styling and responsiveness
app.layout = dbc.Container([
    html.H1("AutoBasket Data Dashboard", className="my-4 text-center"),  # Adjust margin and alignment
    
    dcc.Tabs(id='tabs', children=[
        dcc.Tab(label='User Interaction Data', children=[
            dbc.Row([
                dbc.Col(dcc.Graph(
                    id='sessions-vs-time',
                    figure=px.scatter(user_interaction_df, x='Sessions Initiated', y='Average Time per Session (min)', color='User ID')
                ), md=6),  # Adjust column size for responsiveness
                
                dbc.Col(dcc.Graph(
                    id='favorite-recipes-count',
                    figure=px.bar(favorite_recipes['Recipe'].value_counts().reset_index(), x='count', y='Recipe', labels={'index': 'Recipe', 'Recipe': 'Count'}, title='Favorite Recipes Count')
                ), md=6),
            ]),
        ]),
        
        dcc.Tab(label='Delivery Preferences', children=[
            dbc.Row([
                dbc.Col(dcc.Graph(
                    id='delivery-frequency-distribution',
                    figure=px.chistogram(delivery_preferences_df, x='Delivery Frequency', title='Delivery Frequency Distribution')
                ), md=6),
                
                dbc.Col(dcc.Graph(
                    id='preferred-delivery-days',
                    figure=px.bar(preferred_days['Day'].value_counts().reset_index(), x='count', y='Day', labels={'index': 'Day', 'Day': 'Count'}, title='Preferred Delivery Days')
                ), md=6),
            ]),
        ]),
        
        dcc.Tab(label='Recipe Preferences', children=[
            dbc.Row([
                dbc.Col(dcc.Graph(
                    id='most-requested-recipes',
                    figure=px.bar(most_requested_recipes['Recipe'].value_counts().reset_index(), x='count', y='Recipe', labels={'index': 'Recipe', 'Recipe': 'Count'}, title='Most Requested Recipes')
                ), md=6),
                
                dbc.Col(dcc.Graph(
                    id='preferred-category-distribution',
                    figure=px.histogram(recipe_preferences_df, x='Preferred Category', title='Preferred Category Distribution')
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
                    figure=px.imshow(corr, text_auto=True, title='Correlation Matrix')
                ), md=6),
            ]),
        ]),
    ]),
], fluid=True)  # Use fluid container for full-width layout

if __name__ == '__main__':
    
    app.run_server(debug=True)
