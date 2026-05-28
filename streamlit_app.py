import os
import requests
import streamlit as st

st.set_page_config(page_title="AI Fraud Triage Agent", page_icon="🚨", layout="wide")

TRIAGE_API_URL = os.getenv("TRIAGE_API_URL", "http://localhost:8003/triage")
REQUEST_TIMEOUT_SECONDS = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "20"))

st.title("🚨 AI Fraud Triage Agent")
st.caption("Submit a transaction and get a model + graph risk decision.")

with st.sidebar:
    st.header("Connection")
    st.code(TRIAGE_API_URL, language="text")
    st.caption("For Docker, this should usually be http://triage-agent:8003/triage")

with st.form("triage_form"):
    col1, col2 = st.columns(2)
    with col1:
        transaction_id = st.text_input("Transaction ID", value="txn_1001")
        user_id = st.text_input("User ID", value="user_123")
    with col2:
        amount = st.number_input("Amount", min_value=0.0, value=250.0, step=10.0)
        merchant = st.text_input("Merchant", value="Demo Merchant")

    submitted = st.form_submit_button("Run Triage", type="primary")

if submitted:
    payload = {
        "transaction_id": transaction_id.strip(),
        "user_id": user_id.strip(),
        "amount": amount,
        "merchant": merchant.strip(),
    }

    if not payload["transaction_id"] or not payload["user_id"] or not payload["merchant"]:
        st.error("Please fill Transaction ID, User ID, and Merchant.")
        st.stop()

    try:
        with st.spinner("Running AI triage..."):
            response = requests.post(TRIAGE_API_URL, json=payload, timeout=REQUEST_TIMEOUT_SECONDS)
            response.raise_for_status()
            result = response.json()
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the triage API. Check that the backend is running and TRIAGE_API_URL is correct.")
        st.stop()
    except requests.exceptions.Timeout:
        st.error("The triage API took too long to respond. Try again or check backend logs.")
        st.stop()
    except requests.exceptions.HTTPError as exc:
        st.error(f"Triage API returned an error: {exc}")
        st.text(response.text)
        st.stop()
    except Exception as exc:
        st.error(f"Unexpected error: {exc}")
        st.stop()

    decision = result.get("decision", "UNKNOWN")
    if decision == "BLOCK":
        st.error(f"Decision: {decision}")
    elif decision == "REVIEW":
        st.warning(f"Decision: {decision}")
    else:
        st.success(f"Decision: {decision}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Combined Risk", result.get("combined_risk"))
    col2.metric("Model Risk", result.get("risk_score"))
    col3.metric("Graph Risk", result.get("graph_risk"))

    st.subheader("Explanation")
    st.write(result.get("explanation", "No explanation returned."))

    with st.expander("Raw response"):
        st.json(result)
