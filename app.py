import os
from flask import Flask, request
from flask_mail import Mail, Message
from fpdf import FPDF
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv(".env")

app.config.update(
    MAIL_SERVER=os.getenv("SMTP_HOST"),
    MAIL_PORT=int(os.getenv("SMTP_PORT")),
    MAIL_USERNAME=os.getenv("SMTP_USER"),
    MAIL_PASSWORD=os.getenv("SMTP_PASS"),
    MAIL_USE_TLS=False,
    MAIL_USE_SSL=True
)

mail = Mail(app)

@app.route("/send-invoice", methods=["POST"])
def send_invoice():
    data = request.get_json()
    client_name = data.get("client_name")
    client_email = data.get("client_email")
    service = data.get("service_type")
    description = data.get("description")
    amount = float(data.get("amount", 0))
    vat = amount * 0.15
    total = amount + vat

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="INVOICE", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"To: {client_name}", ln=True)
    pdf.cell(200, 10, txt=f"Service: {service}", ln=True)
    pdf.multi_cell(0, 10, txt=f"Description: {description}")
    pdf.cell(200, 10, txt=f"Subtotal: R {amount:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"VAT (15%): R {vat:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Total: R {total:.2f}", ln=True)

    pdf_path = f"invoice_{client_name.replace(' ', '_')}.pdf"
    pdf.output(pdf_path)

    subject = os.getenv("EMAIL_SUBJECT", "Invoice from Vuleka Construction")
    body = os.getenv("EMAIL_BODY", "Hello {{client_name}}, your invoice is attached.").replace("{{client_name}}", client_name)

    msg = Message(subject, sender=os.getenv("SMTP_USER"), recipients=[client_email])
    msg.body = body
    with open(pdf_path, 'rb') as f:
        msg.attach(pdf_path, 'application/pdf', f.read())

    mail.send(msg)
    os.remove(pdf_path)

    return {"status": "success", "message": "Invoice sent to client."}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
