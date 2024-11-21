import streamlit as st
import numpy as np
from scipy.optimize import linprog

# Food Data: calories, protein, and cost per unit
food_items = {
    "Rice": {"calories": 200, "protein": 6, "cost": 20},
    "Eggs": {"calories": 70, "protein": 7, "cost": 10},
    "Chicken": {"calories": 250, "protein": 30, "cost": 50},
    "Apple": {"calories": 80, "protein": 0, "cost": 15}
}

# Streamlit UI for user inputs
st.title("Diet Optimization App")

calories_needed = st.number_input("Enter your daily caloric requirement:", min_value=100, value=1500)
protein_needed = st.number_input("Enter your daily protein requirement:", min_value=10, value=50)
budget_min = st.number_input("Enter your minimum budget (₹):", min_value=0, value=100)
budget_max = st.number_input("Enter your maximum budget (₹):", min_value=0, value=500)

# Select food items
selected_foods = st.multiselect("Select food items", options=list(food_items.keys()))

# Prepare the LP input data
c = [food_items[item]["cost"] for item in selected_foods]  # Cost vector (objective function)
A = [
    [-food_items[item]["calories"] for item in selected_foods],  # Calories constraint
    [-food_items[item]["protein"] for item in selected_foods]   # Protein constraint
]
b = [-calories_needed, -protein_needed]  # Right-hand side of the constraints

# Bounds: each food item can be purchased from 0 to an upper bound based on budget
bounds = [(0, budget_max / food_items[item]["cost"]) for item in selected_foods]

# Solve the LP problem
if st.button("Solve"):
    result = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

    if result.success:
        st.subheader("Optimal Solutions")
        # Display the top 3 solutions
        solutions = result.x
        total_cost = sum(solutions[i] * c[i] for i in range(len(solutions)))

        st.write(f"Total cost: ₹{total_cost:.2f}")
        st.write("Food quantities selected (in units):")
        for i, item in enumerate(selected_foods):
            st.write(f"{item}: {solutions[i]:.2f} units")
    else:
        st.error("No solution found. Try adjusting your requirements or budget.")
