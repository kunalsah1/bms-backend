from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from django.shortcuts import get_object_or_404
from ..models import Quotation
from rest_framework import status


def generate_pdf(quotation):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica", 12)
    # mapped names
    company_name = quotation.company_id.name if quotation.company_id else "Company name not available"
    company_working = quotation.working_id.title if quotation.working_id else "Working not provided"
    company_address = quotation.address_id.address if quotation.address_id else "address not provided"


    # Business Header
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(colors.red)
    c.drawCentredString(300, 760, f"{company_name}")
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    c.drawCentredString(300, 745, f"{company_working}")
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(300, 730, f"Mob: {quotation.mobile_number}, Email: {quotation.email_id}")
    c.drawCentredString(300, 715, f"{company_address}")
    # c.drawCentredString(300, 720, "Mumbai - 400102")

    # Date
    c.setFont("Helvetica-Bold", 12)
    c.drawRightString(550, 700, f"DATE: {quotation.quotation_date}")

    # Client Information
    c.setFont("Helvetica-Bold", 12)
    c.drawString(30, 680, "To,")
    c.setFont("Helvetica", 12)
    c.drawString(30, 665, f"{quotation.client_name},")
    c.drawString(30, 650, f"{quotation.client_address1},")
    c.drawString(30, 635, f"{quotation.client_address2},")

    # Table Header

    y_position = 600
    c.setFont("Helvetica-Bold", 12)  # Set font before drawing the text
    c.drawCentredString(300, 620, f"{quotation.bill_or_quotation.title()}:")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(30, y_position, "Sr")
    c.drawString(60, y_position, "Description")
    c.drawString(250, y_position, "Rate")
    c.drawString(350, y_position, "Quantity")
    c.drawString(450, y_position, "Amount")
    c.line(30, y_position - 5, 550, y_position - 5)

    c.setFont("Helvetica", 12)
    y_position -= 20

    # Adding Material Data
    for index, material in enumerate(quotation.materials, start=1):
        c.drawString(30, y_position, str(index))
        c.drawString(60, y_position, material.get("particular", ""))
        c.drawString(250, y_position, str(material.get("rate", "")))
        quantity_with_unit = f"{material.get('quantity', '')} {material.get('unit', '')}"
        c.drawString(350, y_position, quantity_with_unit)
        c.drawString(450, y_position, str(material.get("amount", "")))
        c.line(30, y_position - 5, 550, y_position - 5)
        y_position -= 20

    # Totals
    c.setFont("Helvetica-Bold", 12)
    c.drawString(350, y_position - 20, f"Total Material: {quotation.total_materials}")
    c.drawString(350, y_position - 40, f"Labour: {quotation.total_labour}")
    c.drawString(350, y_position - 60, f"Total Amount: {quotation.total_amount}")

    # Signature
    c.setFont("Helvetica", 12)
    c.drawString(400, y_position - 100, "Signature........................")
    # c.line(400, y_position - 105, 550, y_position - 105)

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer


class DownloadQuotationPDF(APIView):
    def get(self, request, quotation_id, format=None):
        # Debugging step
        print("PDF generated successfully")

        quotation = get_object_or_404(Quotation, id=quotation_id)
        pdf_buffer = generate_pdf(quotation)
        pdf_buffer.seek(0)
        return FileResponse(pdf_buffer, as_attachment=True, filename=f"quotation_{quotation_id}.pdf",
                            content_type='application/pdf')
