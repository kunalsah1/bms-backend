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
from textwrap import wrap


def generate_pdf(quotation):
    def draw_wrapped_text(c, text, x, y, max_width, line_height):
        wrapped_lines = wrap(text, width=max_width // 6)  # Adjust width for wrapping
        for i, line in enumerate(wrapped_lines):
            c.drawCentredString(x, y - (i * line_height), line)

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica", 12)

    # Mapped names
    company_name = quotation.company_id.name if quotation.company_id else "Company name not available"
    company_working = quotation.working_id.title if quotation.working_id else "Working not provided"
    company_address = quotation.address_id.address if quotation.address_id else "Address not provided"

    # Business Header
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(colors.red)
    c.drawCentredString(300, 760, f"{company_name}")
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    c.drawCentredString(300, 745, f"{company_working}")
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(300, 730, f"Mob: {quotation.mobile_number}, Email: {quotation.email_id}")
    draw_wrapped_text(c, f"{company_address}", 300, 715, max_width=400, line_height=15)

    # Date
    c.setFont("Helvetica-Bold", 12)
    c.drawRightString(550, 680, f"DATE: {quotation.quotation_date}")

    # Client Information
    c.setFont("Helvetica-Bold", 12)
    c.drawString(30, 680, "To,")
    c.setFont("Helvetica", 12)
    c.drawString(30, 665, f"{quotation.client_name},")
    c.drawString(30, 650, f"{quotation.client_address1},")
    c.drawString(30, 635, f"{quotation.client_address2},")

    # Table Header
    y_position = 600
    c.setFont("Helvetica-Bold", 12)
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
        if y_position < 100:  # If space is low, start a new page
            c.showPage()
            c.setFont("Helvetica", 12)
            y_position = 700  # Reset position on new page

            # Redraw table headers
            c.setFont("Helvetica-Bold", 12)
            c.drawString(30, y_position, "Sr")
            c.drawString(60, y_position, "Description")
            c.drawString(250, y_position, "Rate")
            c.drawString(350, y_position, "Quantity")
            c.drawString(450, y_position, "Amount")
            c.line(30, y_position - 5, 550, y_position - 5)
            y_position -= 20

        c.drawString(30, y_position, str(index))
        c.drawString(60, y_position, material.get("particular", ""))
        c.drawString(250, y_position, str(material.get("rate", "")))  # Rate Column
        quantity_with_unit = f"{material.get('quantity', '')} {material.get('unit', '')}"
        c.drawString(350, y_position, quantity_with_unit)  # Quantity Column
        c.drawString(450, y_position, str(material.get("amount", "")))  # Amount Column
        c.line(30, y_position - 5, 550, y_position - 5)  # Draw row separator
        y_position -= 20

    # Ensure totals fit within the table
    if y_position < 100:
        c.showPage()
        c.setFont("Helvetica", 12)
        y_position = 700  # Reset to new page

        # Redraw table headers
        c.setFont("Helvetica-Bold", 12)
        c.drawString(30, y_position, "Sr")
        c.drawString(60, y_position, "Description")
        c.drawString(250, y_position, "Rate")
        c.drawString(350, y_position, "Quantity")
        c.drawString(450, y_position, "Amount")
        c.line(30, y_position - 5, 550, y_position - 5)
        y_position -= 20

    # Totals inside the table under the "Description" column
    c.setFont("Helvetica-Bold", 12)

    c.drawString(60, y_position, "Total Material:")  # In Description Column
    c.drawString(450, y_position, str(quotation.total_materials))  # In Amount Column
    c.line(30, y_position - 5, 550, y_position - 5)
    y_position -= 20

    c.drawString(60, y_position, "Labour:")  # In Description Column
    c.drawString(450, y_position, str(quotation.total_labour))  # In Amount Column
    c.line(30, y_position - 5, 550, y_position - 5)
    y_position -= 20

    c.drawString(60, y_position, "Total Amount:")  # In Description Column
    c.drawString(450, y_position, str(quotation.total_amount))  # In Amount Column
    c.line(30, y_position - 5, 550, y_position - 5)  # Draw closing line
    y_position -= 20

    # Signature
    c.setFont("Helvetica", 12)
    c.drawString(400, y_position - 50, "Signature........................")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer


class DownloadQuotationPDF(APIView):
    def get(self, request, quotation_id, format=None):
        print("PDF generated successfully")
        quotation = get_object_or_404(Quotation, id=quotation_id)
        pdf_buffer = generate_pdf(quotation)
        pdf_buffer.seek(0)
        return FileResponse(pdf_buffer, as_attachment=True, filename=f"quotation_{quotation_id}.pdf",
                            content_type='application/pdf')
