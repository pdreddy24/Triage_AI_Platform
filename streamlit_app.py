# streamlit_app.py

import streamlit as st
import requests

st.set_page_config(page_title="AI Fraud Triage Agent", layout="wide")

st.title("🚨 AI Fraud Triage Agent")

API_URL = "http://localhost:8003/triage"

with st.form("triage_form"):
    transaction_id = st.text_input("Transaction ID")
    user_id = st.text_input("User ID")
    amount = st.number_input("Amount", min_value=0.0)
    merchant = st.text_input("Merchant")

    submitted = st.form_submit_button("Run Triage")

if submitted:
    payload = {
        "transaction_id": transaction_id,
        "user_id": user_id,
        "amount": amount,
        "merchant": merchant
    }

    with st.spinner("Running AI Triage..."):
        response = requests.post(API_URL, json=payload)

    if response.status_code == 200:
        result = response.json()

        st.success(f"Decision: {result['decision']}")
        st.metric("Combined Risk", result["combined_risk"])
        st.metric("Model Risk", result["risk_score"])
        st.metric("Graph Risk", result["graph_risk"])

        st.subheader("Explanation")
        st.write(result["explanation"])
    else:
        st.error("Error running triage")