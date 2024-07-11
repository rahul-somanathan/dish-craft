# Import Libraries
import requests
import streamlit as st

# Define CSS style for scrollable divs
scrollable_style = """
    <style>
        .scrollable {
            max-height: 250px;
            overflow-y: auto;
            border: 1px solid #ddd;
            padding: 10px;
            border-radius: 5px;
        }
    </style>
"""

# Function to fetch available users
def get_available_users():
    response = requests.get('http://backend:8000/available_users')
    return response.json().get("user_ids", [])

# Function to fetch user data
def get_user_data(user_id):
    response = requests.get(f'http://backend:8000/recommend/{user_id}')
    return response.json()

# Main function
def main():
    # Add title and description
    st.title("DishCraft™ by AutoBasket")
    st.write("Unlock a world of culinary delights tailored just for you!")
    
    # Fetch available users
    available_users = get_available_users()
    
    # Show user selection dropdown
    user_id = st.selectbox("Select User ID", available_users)
    
    # If no users available, show message and return
    if not available_users:
        st.warning("No available users.")
        return
    
    # Button to trigger data fetching
    if st.button("Submit"):
        user_data = get_user_data(user_id)
        
        # Check for errors
        if "Error" in user_data:
            st.error("Error fetching data from the server.")
            return
        
        # Display past rated recipes
        with st.expander("Recipes Rated by User"):
            past_rated_recipes = user_data.get("past_rated_recipes", [])
            if past_rated_recipes:
                for recipe in past_rated_recipes:
                    st.write(f"- {recipe}")
            else:
                st.write("No past rated recipes.")
        
        # Display recommended recipes
        with st.expander("Recommended Recipes"):
            recommended_recipes = user_data.get("recommended_recipes", [])
            if recommended_recipes:
                for recipe in recommended_recipes:
                    st.write(f"- {recipe}")
            else:
                st.write("No recommended recipes.")

# Run the app
if __name__ == "__main__":
    # Add CSS styling
    st.markdown(scrollable_style, unsafe_allow_html=True)
    main()
