import streamlit as st
import pandas as pd
import json
import os
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from parser import parse_pdf, export_to_pdf

# File paths
CSV_PATH = "parsed_statements.csv"
JSON_PATH = "parsed_statements.json"
PDF_PATH = "parsed_statements.pdf"

# --- Helper to load existing data ---
def load_existing_data():
    if os.path.exists(CSV_PATH):
        return pd.read_csv(CSV_PATH)
    else:
        return pd.DataFrame(columns=["bank", "card_holder", "last_4_digits", "billing_cycle", "payment_due_date", "total_outstanding_balance"])

# --- Helper to save updated data ---
def save_updated_data(df):
    df.to_csv(CSV_PATH, index=False)
    df.to_json(JSON_PATH, orient="records", indent=2)
    export_to_pdf(df.to_dict(orient="records"), PDF_PATH)

# --- Streamlit UI ---
st.set_page_config(page_title="Credit Card Statement Parser", layout="wide")
st.title("Credit Card Statement Parser")

st.markdown(
    """
    Upload your **credit card statement (PDF)** and get structured information like  
    - Bank Name  
    - Card Holder  
    - Last 4 Digits  
    - Billing Cycle  
    - Due Date  
    - Total Outstanding Balance  

    All results will be saved and displayed below.
    """
)

uploaded_file = st.file_uploader("Upload a credit card statement PDF", type=["pdf"])

if uploaded_file:
    st.info(f"Processing `{uploaded_file.name}`...")
    # Save temp file
    tmp_path = f"temp_{uploaded_file.name}"
    with open(tmp_path, "wb") as f:
        f.write(uploaded_file.read())

    # Parse the file
    result = parse_pdf(tmp_path)

    # Load current data
    df = load_existing_data()

    # Add new record
    df = pd.concat([df, pd.DataFrame([result])], ignore_index=True)

    # Save updates
    save_updated_data(df)

    st.success("File parsed successfully and data updated!")
    st.json(result)

    # Remove temp file
    os.remove(tmp_path)

st.subheader("Parsed Statements So Far")

# Display updated table
df = load_existing_data()
st.dataframe(df, use_container_width=True)

# Provide download buttons
if not df.empty:
    col1, col2, col3 = st.columns(3)
    with col1:
        with open(CSV_PATH, "rb") as f:
            st.download_button("⬇ Download CSV", f, file_name="parsed_statements.csv")

    with col2:
        with open(JSON_PATH, "rb") as f:
            st.download_button("⬇ Download JSON", f, file_name="parsed_statements.json")

    with col3:
        with open(PDF_PATH, "rb") as f:
            st.download_button("⬇ Download PDF Report", f, file_name="parsed_statements.pdf")
