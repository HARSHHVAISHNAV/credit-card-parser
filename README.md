# Credit Card Statement Parser

A Python-based tool that extracts key information from **credit card statements** (PDFs) such as:

- Bank Name  
- Card Holder  
- Last 4 Digits  
- Billing Cycle  
- Payment Due Date  
- Total Outstanding Balance  

Built using **Python**, **pdfplumber**, **ReportLab**, and **Streamlit**.

---

## Project Structure
```bash
credit-card-parser/
│
├── app/
│ ├── parser.py # Extracts info from PDF statements
│ └── ui/
│ └── streamlit_app.py # Streamlit interface for uploads & viewing
│
├── data/
│ └── samples/ # Contains sample generated PDFs
│
├── generate_one_pdf.py # Creates a new random credit card statement
├── requirements.txt # Python dependencies
├── README.md # Documentation
└── .gitignore # Ignore unnecessary files

yaml
Copy code

---

## Features

- Parse statements from **HDFC, ICICI, SBI, Axis, and Canara Bank**
- Smart regex-based field extraction
- Automatic CSV / JSON / PDF summary generation
- Streamlit UI for uploading and viewing parsed data
- Synthetic PDF generator for testing

---

## How to Run Locally
```bash
1.Clone the repository

git clone https://github.com/<your-username>/credit-card-parser.git
cd credit-card-parser


2.Create a virtual environment
python -m venv venv
venv\Scripts\activate   # (on Windows)
# or
source venv/bin/activate   # (on Mac/Linux)

3. Install dependencies
pip install -r requirements.txt

4. Generate test PDFs
python generate_one_pdf.py

5. Run the Streamlit app
streamlit run app/ui/streamlit_app.py


Then open http://localhost:8501
 in your browser


Author

Harsh Vaishnav
Computer Engineering Student
Connect on LinkedIn
 ((https://www.linkedin.com/in/harsh-vaishnav-a8b46b230/))