import pandas as pd
from sklearn.calibration import LabelEncoder
from sklearn.preprocessing import OrdinalEncoder

def get_user_interactions_data():
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

def delivery_preferences_data():
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

def recipe_preferences_data():
    recipe_preferences_df = pd.DataFrame({
    'User ID': [1, 2, 3, 4, 5],
    'Preferred Category': ['Salads', 'Meats', 'Seafood', 'Vegan', 'International Dishes'],
    'Most Requested Recipes': ['Quinoa Salad, Caesar Salad', 'BBQ Burger, Teriyaki Chicken',
                               'Grilled Salmon, Shrimp Ceviche', 'Fruit Smoothie, Garbanzo Bowl',
                               'Chicken Curry, Sushi Rolls']
})
    return recipe_preferences_df


# Favorite Recipes Count
favorite_recipes = user_interaction_df['Favorite Recipes'].str.split(', ', expand=True).stack().reset_index(level=1, drop=True).to_frame('Recipe')

# Preferred Delivery Days
preferred_days = delivery_preferences_df['Preferred Delivery Day'].str.split(', ', expand=True).stack().reset_index(level=1, drop=True).to_frame('Day')

# Most Requested Recipes
most_requested_recipes = recipe_preferences_df['Most Requested Recipes'].str.split(', ', expand=True).stack().reset_index(level=1, drop=True).to_frame('Recipe')

# Create copies of the original dataframes for encoding

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

