# Vuleka Invoice Webhook

This is a Python Flask webhook that generates PDF invoices and emails them using Zoho SMTP.

## Example JSON for POST to `/send-invoice`:
{
  "client_name": "Sipho Dlamini",
  "client_email": "sipho@example.com",
  "service_type": "Electrical Wiring",
  "description": "Install electrical wiring for 3-bedroom home",
  "amount": 12000
}
