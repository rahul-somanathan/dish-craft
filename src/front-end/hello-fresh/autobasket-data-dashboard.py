
# Create an interactive web-based data dashboard
import dash
import pandas as pd
from dash import dcc, html
import plotly.express as px
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# # Init Data File Path
# data_file_path = '../../../data/generated/hello-fresh/'

# # Import Data
# user_interaction_df = pd.read_parquet(f'{data_file_path}user_interaction_data.parquet')
# delivery_preferences_df = pd.read_parquet(f'{data_file_path}delivery_preferences.parquet')
# recipe_preferences_df = pd.read_parquet(f'{data_file_path}recipe_preferences.parquet')

# merged_data = pd.read_parquet('../../../data/generated/hello-fresh/merged_data.parquet')

# # Filter Data
# favorite_recipes = user_interaction_df['Favorite Recipes'].str.split(', ', expand=True).stack().reset_index(level=1, drop=True).to_frame('Recipe')
# preferred_days = delivery_preferences_df['Preferred Delivery Day'].str.split(', ', expand=True).stack().reset_index(level=1, drop=True).to_frame('Day')
# most_requested_recipes = recipe_preferences_df['Most Requested Recipes'].str.split(', ', expand=True).stack().reset_index(level=1, drop=True).to_frame('Recipe')
# corr = merged_data.corr()


# Load the datasets
user_interaction_df = pd.DataFrame({
    'User ID': [1, 2, 3, 4, 5],
    'Sessions Initiated': [15, 10, 12, 8, 20],
    'Average Time per Session (min)': [12.5, 8.2, 10.6, 15.3, 7.8],
    'Favorite Recipes': ['Quinoa Salad, Spring Pasta', 'BBQ Burger, Margherita Pizza',
                         'Grilled Salmon, Tomato Soup', 'Tofu Tacos, Fruit Smoothie',
                         'Chicken Curry, Mushroom Risotto'],
    'Last Purchase': ['2023-07-10', '2023-07-12', '2023-07-11', '2023-07-09', '2023-07-08']
})

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

recipe_preferences_df = pd.DataFrame({
    'User ID': [1, 2, 3, 4, 5],
    'Preferred Category': ['Salads', 'Meats', 'Seafood', 'Vegan', 'International Dishes'],
    'Most Requested Recipes': ['Quinoa Salad, Caesar Salad', 'BBQ Burger, Teriyaki Chicken',
                               'Grilled Salmon, Shrimp Ceviche', 'Fruit Smoothie, Garbanzo Bowl',
                               'Chicken Curry, Sushi Rolls']
})

# Favorite Recipes Count
favorite_recipes = user_interaction_df['Favorite Recipes'].str.split(', ', expand=True).stack().reset_index(level=1, drop=True).to_frame('Recipe')

# Preferred Delivery Days
preferred_days = delivery_preferences_df['Preferred Delivery Day'].str.split(', ', expand=True).stack().reset_index(level=1, drop=True).to_frame('Day')

# Most Requested Recipes
most_requested_recipes = recipe_preferences_df['Most Requested Recipes'].str.split(', ', expand=True).stack().reset_index(level=1, drop=True).to_frame('Recipe')

# Create copies of the original dataframes for encoding
from sklearn.calibration import LabelEncoder
from sklearn.preprocessing import OrdinalEncoder


encoded_user_interaction_data = user_interaction_df.copy()
encoded_delivery_preferences_data = delivery_preferences_df.copy()
encoded_recipe_preferences_data = recipe_preferences_df.copy()

# Initialize LabelEncoder and OrdinalEncoder
label_encoder = LabelEncoder()
ordinal_encoder = OrdinalEncoder()


# Encode non-ordinal categorical variables in user_interaction_data
encoded_user_interaction_data['Favorite Recipes'] = label_encoder.fit_transform(encoded_user_interaction_data['Favorite Recipes'])


# Encode non-ordinal categorical variables in recipe_preferences_data
encoded_recipe_preferences_data['Preferred Category'] = label_encoder.fit_transform(encoded_recipe_preferences_data['Preferred Category'])


# Encode ordinal categorical variables in delivery_preferences_data
encoded_delivery_preferences_data['Delivery Frequency'] = ordinal_encoder.fit_transform(encoded_delivery_preferences_data[['Delivery Frequency']])
encoded_delivery_preferences_data['Preferred Delivery Day'] = ordinal_encoder.fit_transform(encoded_delivery_preferences_data[['Preferred Delivery Day']])

# Merge encoded dataframes based on 'User ID'
merged_data = pd.merge(encoded_user_interaction_data, encoded_delivery_preferences_data, on='User ID')
merged_data = pd.merge(merged_data, encoded_recipe_preferences_data, on='User ID')

# Convert 'Last Purchase' to numeric (days since a reference date)
merged_data['Last Purchase'] = pd.to_datetime(merged_data['Last Purchase'])
merged_data['Last Purchase'] = (merged_data['Last Purchase'] - merged_data['Last Purchase'].min()).dt.days

# Drop columns 'Most Requested Recipes' and 'Delivery Address'
columns_to_drop = ['Most Requested Recipes', 'Delivery Address']
merged_data = merged_data.drop(columns=columns_to_drop, errors='ignore')

corr = merged_data.corr()


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
                    figure=px.histogram(delivery_preferences_df, x='Delivery Frequency', title='Delivery Frequency Distribution')
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