from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import random
import os
from datetime import datetime, timedelta

# Change the details every time you want to generate a new sample PDF
BANK_DETAILS = {
    "bank_name": "Hdfc Bank",                  # Change bank name
    "card_holder": "Punit Jain",               # Change name
    "last_4_digits": "9876",                   # Last 4 digits
    "billing_cycle": "01 Sep 2025 - 30 Sep 2025",
    "payment_due_date": "25 Oct 2025",
    "total_outstanding_balance": "20000.00"    # Amount
}


MERCHANTS = [
    "AMAZON", "FLIPKART", "SWIGGY", "ZOMATO", "BIG BAZAAR",
    "SPENCERS", "PAYTM", "MOBIKWIK", "UBER", "OLA",
    "INDIAN OIL", "HP PETROL", "SPAR HYPERMARKET",
    "CROMA", "RELIANCE DIGITAL", "GROCERY STORE", "PANTALOONS"
]

def generate_transactions():
    """Generate random sample transactions"""
    transactions = [["Date", "Description", "Amount (INR)"]]
    start_date = datetime(2025, 9, 1)
    for _ in range(random.randint(5, 8)):  # 5–8 transactions per PDF
        day = start_date + timedelta(days=random.randint(1, 29))
        merchant = random.choice(MERCHANTS)
        amount = f"{random.uniform(500, 60000):,.2f}"
        transactions.append([day.strftime("%d-%b-%Y"), merchant, amount])
    return transactions

def create_pdf(details, output_dir="data/samples"):
    """Create a single synthetic PDF statement"""
    os.makedirs(output_dir, exist_ok=True)

    # Generate unique filename with timestamp
    timestamp = datetime.now().strftime("%Y_%m_%d_%H%M%S")
    filename = f"{details['bank_name'].replace(' ', '_')}_Statement_{timestamp}.pdf"
    filepath = os.path.join(output_dir, filename)

    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter

    # --- Header ---
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.HexColor("#1a237e"))
    c.drawString(150, height - 80, f"{details['bank_name']} Credit Card Statement")

    # --- Card Info Section ---
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    y = height - 130
    c.drawString(50, y, f"Card Holder: {details['card_holder']}")
    c.drawString(50, y - 20, f"Card Number: XXXX-XXXX-XXXX-{details['last_4_digits']}")
    c.drawString(50, y - 40, f"Statement Period: {details['billing_cycle']}")
    c.drawString(50, y - 60, f"Payment Due Date: {details['payment_due_date']}")
    c.drawString(50, y - 80, f"Total Amount Due: INR {details['total_outstanding_balance']}")

    # --- Transaction Table ---
    transactions = generate_transactions()
    table = Table(transactions, colWidths=[120, 220, 120])

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke)
    ])
    table.setStyle(style)

    y -= 150
    table.wrapOn(c, width, height)
    table.drawOn(c, 50, y - (len(transactions) * 20))

    # --- Footer Disclaimer ---
    c.setFont("Helvetica-Oblique", 9)
    c.setFillColor(colors.gray)
    c.drawString(50, 60, "This is a synthetic sample statement generated for testing and development purposes only.")
    c.drawString(50, 50, "No real account or customer data is used.")

    c.save()
    print(f"Generated: {filepath}")

def main():
    create_pdf(BANK_DETAILS)

if __name__ == "__main__":
    main()
