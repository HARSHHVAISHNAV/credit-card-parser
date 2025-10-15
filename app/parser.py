import pdfplumber
import pytesseract
from pdf2image import convert_from_path
import re
import pandas as pd
import os
import json
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

# Bank-specific patterns
BANK_PATTERNS = {
    "HDFC Bank": {
        "card_holder": r"Card Holder\s*[:\-]?\s*([A-Za-z ]+?)(?=\s*Card Number)",
        "last_4_digits": r"Card Number\s*[:\-]?\s*(?:XXXX-XXXX-XXXX-)?(\d{4})",
        "billing_cycle": r"(?:Statement Period|Billing Cycle)\s*[:\-]?\s*(\d{1,2}\s\w+\s\d{4})",
        "payment_due_date": r"Payment Due Date\s*[:\-]?\s*(\d{1,2}\s\w+\s\d{4})",
        "total_outstanding_balance": r"Total Amount Due\s*[:\-]?\s*(?:INR|₹)?\s*([\d,]+\.\d{2})"
    },
    "ICICI Bank": {
        "card_holder": r"Card Holder\s*[:\-]?\s*([A-Za-z ]+?)(?=\s*Card Number)",
        "last_4_digits": r"Card Number\s*[:\-]?\s*(?:XXXX-XXXX-XXXX-)?(\d{4})",
        "billing_cycle": r"(?:Statement Period|Billing Cycle)\s*[:\-]?\s*(\d{1,2}\s\w+\s\d{4})",
        "payment_due_date": r"Payment Due Date\s*[:\-]?\s*(\d{1,2}\s\w+\s\d{4})",
        "total_outstanding_balance": r"Total Amount Due\s*[:\-]?\s*(?:INR|₹)?\s*([\d,]+\.\d{2})"
    },
    "SBI Card": {
        "card_holder": r"Card Holder\s*[:\-]?\s*([A-Za-z ]+?)(?=\s*Card Number)",
        "last_4_digits": r"Card Number\s*[:\-]?\s*(?:XXXX-XXXX-XXXX-)?(\d{4})",
        "billing_cycle": r"(?:Statement Period|Billing Cycle)\s*[:\-]?\s*(\d{1,2}\s\w+\s\d{4})",
        "payment_due_date": r"Payment Due Date\s*[:\-]?\s*(\d{1,2}\s\w+\s\d{4})",
        "total_outstanding_balance": r"Total Amount Due\s*[:\-]?\s*(?:INR|₹)?\s*([\d,]+\.\d{2})"
    },
    "Axis Bank": {
        "card_holder": r"Card Holder\s*[:\-]?\s*([A-Za-z ]+?)(?=\s*Card Number)",
        "last_4_digits": r"Card Number\s*[:\-]?\s*(?:XXXX-XXXX-XXXX-)?(\d{4})",
        "billing_cycle": r"(?:Statement Period|Billing Cycle)\s*[:\-]?\s*(\d{1,2}\s\w+\s\d{4})",
        "payment_due_date": r"Payment Due Date\s*[:\-]?\s*(\d{1,2}\s\w+\s\d{4})",
        "total_outstanding_balance": r"Total Amount Due\s*[:\-]?\s*(?:INR|₹)?\s*([\d,]+\.\d{2})"
    },
    "Canara Bank": {
        "card_holder": r"Card Holder\s*[:\-]?\s*([A-Za-z ]+?)(?=\s*Card Number)",
        "last_4_digits": r"Card Number\s*[:\-]?\s*(?:XXXX-XXXX-XXXX-)?(\d{4})",
        "billing_cycle": r"(?:Statement Period|Billing Cycle)\s*[:\-]?\s*(\d{1,2}\s\w+\s\d{4})",
        "payment_due_date": r"Payment Due Date\s*[:\-]?\s*(\d{1,2}\s\w+\s\d{4})",
        "total_outstanding_balance": r"Total Amount Due\s*[:\-]?\s*(?:INR|₹)?\s*([\d,]+\.\d{2})"
    }
}

# Extract text from PDF with OCR fallback
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print(f" Error reading {pdf_path}: {e}")

    # If no text → use OCR
    # if not text.strip():
    #     print(f" Using OCR fallback for {os.path.basename(pdf_path)}")
    #     pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    #     images = convert_from_path(pdf_path,dpi=300, poppler_path=r"C:\poppler\poppler-25.07.0\Library\bin")
    #     for img in images:
    #         text += pytesseract.image_to_string(img) + "\n"

    text = re.sub(r"\s+", " ", text).strip()

    return text  
        


# Parse individual PDF
def parse_pdf(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    result = {
        "bank": None,
        "card_holder": None,
        "last_4_digits": None,
        "billing_cycle": None,
        "payment_due_date": None,
        "total_outstanding_balance": None
    }

    # Detect bank
    for bank in BANK_PATTERNS.keys():
        if re.search(bank, text, re.IGNORECASE):
            result["bank"] = bank
            patterns = BANK_PATTERNS[bank]
            break
    else:
        result["bank"] = "Unknown"
        print(f"Could not detect bank in {os.path.basename(pdf_path)}")
        return result

    # Extract fields
    for field, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            result[field] = match.group(1).strip()

    return result


# PDF Export Function
def export_to_pdf(data, out_pdf="parsed_statements.pdf"):
    c = canvas.Canvas(out_pdf, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.HexColor("#1a237e"))
    c.drawString(160, height - 70, "Credit Card Statement Parsing Report")

    c.setFont("Helvetica", 11)
    c.setFillColor(colors.black)
    y = height - 120

    table_data = [["Bank", "Card Holder", "Last 4 Digits", "Billing Cycle", "Due Date", "Total Due"]]
    for d in data:
        table_data.append([
            d.get("bank", ""),
            d.get("card_holder", ""),
            d.get("last_4_digits", ""),
            d.get("billing_cycle", ""),
            d.get("payment_due_date", ""),
            d.get("total_outstanding_balance", "")
        ])

    table = Table(table_data, colWidths=[90, 110, 70, 110, 90, 90])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 11),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
    ]))
    table.wrapOn(c, width, height)
    table.drawOn(c, 40, y - len(table_data) * 20)

    c.setFont("Helvetica-Oblique", 9)
    c.setFillColor(colors.gray)
    c.drawString(50, 50, "Generated automatically by Credit Card Statement Parser.")
    c.save()
    print(f"PDF summary saved as {out_pdf}")


# Process all PDFs in a folder
def process_all_pdfs(folder="data/samples", out_csv="parsed_statements.csv", out_json="parsed_statements.json"):
    parsed_data = []

    for file in os.listdir(folder):
        if file.lower().endswith(".pdf"):
            pdf_path = os.path.join(folder, file)
            print(f"Parsing: {file}")
            data = parse_pdf(pdf_path)
            parsed_data.append(data)

    # Save as CSV + JSON
    df = pd.DataFrame(parsed_data)
    df.to_csv(out_csv, index=False)
    df.to_json(out_json, orient="records", indent=2)
    print(f"\nDone! Parsed data saved to:\n  - {out_csv}\n  - {out_json}")

    # Export summary to PDF
    export_to_pdf(parsed_data)


#   Run directly
if __name__ == "__main__":
    folder = "data/samples"
    process_all_pdfs(folder)
