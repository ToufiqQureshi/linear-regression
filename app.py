import streamlit as st
import joblib
import numpy as np

# Model Load karo
model = joblib.load("hotel_price_model.pkl")

# Streamlit App UI
st.title("Hotel Room Price Prediction")

# Feature Input (Adjust karna ho toh yaha add kar sakte ho)
feature_1 = st.number_input("Enter Feature 1:", value=100)
feature_2 = st.number_input("Enter Feature 2:", value=50)

if st.button("Predict Price"):
    # Prediction
    prediction = model.predict(np.array([[feature_1, feature_2]]))
    st.write(f"Predicted Price: ₹ {round(prediction[0], 2)}")
