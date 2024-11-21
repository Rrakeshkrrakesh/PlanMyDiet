import streamlit as st
import pandas as pd
import numpy as np
from scipy.optimize import linprog

# Define the food items and their nutritional information
food_items = {
    "Rice": {"calories": 360, "protein": 7.5, "cost": 50, "unit": "kg"},
    "Bread": {"calories": 265, "protein": 9.4, "cost": 23, "unit": "packet"},
    "Egg": {"calories": 70, "protein": 6.3, "cost": 8, "unit": "piece"},
    "Milk": {"calories": 67, "protein": 3.3, "cost": 62, "unit": "litre"},
    "Lentil": {"calories": 353, "protein": 25.8, "cost": 140, "unit": "kg"},
    "Chicken": {"calories": 239, "protein": 27, "cost": 220, "unit": "kg"},
    "Paneer": {"calories": 265, "protein": 18.3, "cost": 350, "unit": "kg"}
}

# Convert food items to a DataFrame for display
food_df = pd.DataFrame.from_dict(food_items, orient='index', columns=['calories', 'protein', 'cost', 'unit'])

# Streamlit app
st.title("Diet Optimizer")

# User input for dietary requirements
st.sidebar.header("Dietary Requirements")
min_calories = st.sidebar.number_input("Minimum Calories:", min_value=0, value=2000)
min_protein = st.sidebar.number_input("Minimum Protein (g):", min_value=0, value=50)
budget_range = st.sidebar.slider("Budget Range (₹):", 0, 5500, (100, 3000))

# User input for food selection
st.header("Select Food Items")
selected_foods = st.multiselect("Choose food items:", list(food_items.keys()))

# Filter selected food items
selected_food_items = {k: food_items[k] for k in selected_foods}
selected_food_df = pd.DataFrame.from_dict(selected_food_items, orient='index', columns=['calories', 'protein', 'cost', 'unit'])

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
            st.write(f"{food}: {optimal_solution[i]:.2f} {food_items[food]['unit']}")
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
