import streamlit as st
import pandas as pd
import numpy as np
from scipy.optimize import linprog

# Define the food items and their nutritional information
food_items = {
    "Rice": {"calories": 200, "protein": 6, "cost": 20},
    "Eggs": {"calories": 70, "protein": 7, "cost": 10},
    "Chicken": {"calories": 200, "protein": 30, "cost": 50},
    "Lentils": {"calories": 150, "protein": 10, "cost": 15},
    "Milk": {"calories": 100, "protein": 8, "cost": 12},
    "Bread": {"calories": 250, "protein": 8, "cost": 10}
}

# Convert food items to a DataFrame for display
food_df = pd.DataFrame.from_dict(food_items, orient='index', columns=['calories', 'protein', 'cost'])

# Streamlit app
st.title("Diet Optimizer")

# User input for dietary requirements
st.sidebar.header("Dietary Requirements")
min_calories = st.sidebar.number_input("Minimum Calories:", min_value=0, value=2000)
min_protein = st.sidebar.number_input("Minimum Protein (g):", min_value=0, value=50)
budget_range = st.sidebar.slider("Budget Range (₹):", 0, 500, (100, 300))

# User input for food selection
st.header("Select Food Items")
selected_foods = st.multiselect("Choose food items:", list(food_items.keys()))

# Filter selected food items
selected_food_items = {k: food_items[k] for k in selected_foods}
selected_food_df = pd.DataFrame.from_dict(selected_food_items, orient='index', columns=['calories', 'protein', 'cost'])

if st.button("Optimize Diet"):
    # Extract data for linear programming
    c = [food_items[food]['cost'] for food in selected_foods]
    A = [[food_items[food]['calories'] for food in selected_foods],
         [food_items[food]['protein'] for food in selected_foods]]
    b = [min_calories, min_protein]
    x_bounds = [(0, None) for _ in selected_foods]

    # Solve the linear programming problem
    result = linprog(c, A_ub=-np.array(A), b_ub=-np.array(b), bounds=x_bounds, method='highs')

    if result.success:
        st.success("Optimal solution found!")
        optimal_solution = result.x
        total_cost = np.dot(optimal_solution, c)

        # Display the optimal solution
        st.write("Optimal Diet Plan:")
        for i, food in enumerate(selected_foods):
            st.write(f"{food}: {optimal_solution[i]:.2f} units")
        st.write(f"Total Cost: ₹{total_cost:.2f}")

        # Display the nutritional information
        st.write("Nutritional Information:")
        calories = np.dot(optimal_solution, [food_items[food]['calories'] for food in selected_foods])
        protein = np.dot(optimal_solution, [food_items[food]['protein'] for food in selected_foods])
        st.write(f"Calories: {calories:.2f}")
        st.write(f"Protein: {protein:.2f} g")
    else:
        st.error("No optimal solution found.")

# Display the selected food items
st.write("Selected Food Items:")
st.dataframe(selected_food_df)
