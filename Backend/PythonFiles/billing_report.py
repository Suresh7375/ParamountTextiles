import os
from datetime import date
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer,
    Table, TableStyle, HRFlowable, Image
)
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT

# Brand Colors
BRAND_PRIMARY = colors.HexColor("#2C3E50")
BRAND_SECONDARY = colors.HexColor("#7F8C8D")
BRAND_LIGHT = colors.HexColor("#ECF0F1")

class InvoiceDocTemplate(BaseDocTemplate):
    def __init__(self, filename, company_name="Paramount Clothing", **kwargs):
        super().__init__(filename, pagesize=A4, **kwargs)
        self.company_name = company_name
        self.styles = getSampleStyleSheet()
        self.addPageTemplates([self._create_template()])

    def _create_template(self):
        frame = Frame(
            self.leftMargin, self.bottomMargin + 20 * mm,
            self.width, self.height - 30 * mm, id='content')
        return PageTemplate(id='InvoiceTemplate', frames=frame, onPage=self._add_footer)

    def _add_footer(self, canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(BRAND_PRIMARY)
        canvas.setLineWidth(0.5)
        canvas.line(doc.leftMargin, doc.bottomMargin + 15 * mm,
                    doc.pagesize[0] - doc.rightMargin, doc.bottomMargin + 15 * mm)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(BRAND_SECONDARY)
        canvas.drawString(doc.leftMargin, doc.bottomMargin + 10 * mm,
                          f"{self.company_name} • GST Registered Company")
        canvas.drawCentredString(doc.pagesize[0] / 2, doc.bottomMargin + 10 * mm,
                                 "www.paramountclothing.com")
        canvas.drawRightString(doc.pagesize[0] - doc.rightMargin, doc.bottomMargin + 10 * mm,
                               f"Page {canvas.getPageNumber()}")
        canvas.drawCentredString(doc.pagesize[0] / 2, doc.bottomMargin + 5 * mm,
                                 "Email: info@paramountclothing.com • Phone: +65 9876 5432")
        canvas.restoreState()

def create_invoice(output_path):
    doc = InvoiceDocTemplate(output_path)
    styles = doc.styles

    title_style = ParagraphStyle(name='Title', fontSize=16, alignment=TA_CENTER, textColor=BRAND_PRIMARY)
    header_style = ParagraphStyle(name='Header', fontSize=12, textColor=BRAND_PRIMARY)
    normal_style = ParagraphStyle(name='Normal', fontSize=10)

    elements = []

    elements.append(Paragraph("TAX INVOICE", title_style))
    elements.append(Spacer(1, 12))

    logo_path = "company_logo.png"  # Ensure this file exists in your directory
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=2.5 * cm, height=2.5 * cm)
    else:
        logo = Spacer(1, 2.5 * cm)

    company_info = [
        [logo, Paragraph("<b>Paramount Clothing</b>", header_style),
         Paragraph("Invoice #: PC-0001<br/>Date: 09.04.2025<br/>Our Ref: PC-0425-PI-01<br/>Your Ref: PO# 20250409", normal_style)]
    ]
    company_table = Table(company_info, colWidths=[2.8 * cm, 6.2 * cm, 6.5 * cm])
    elements.append(company_table)
    elements.append(Spacer(1, 12))

    customer_info = [
        [Paragraph("<b>Bill To</b><br/>M/S. ABC STORES<br/>#01-04, BLOCK 219<br/>PARKLANDS<br/>SERANGOON<br/>SINGAPORE<br/>PIN: 315602<br/>GSTIN:", normal_style),
         Paragraph("<b>Ship To</b><br/>M/S. ABC STORES<br/>#01-04, BLOCK 219<br/>PARKLANDS<br/>SERANGOON<br/>SINGAPORE<br/>PIN: 315602", normal_style)]
    ]
    customer_table = Table(customer_info, colWidths=[9 * cm, 7 * cm])
    elements.append(customer_table)
    elements.append(Spacer(1, 12))

    table_header = ["Sl. No.", "Description", "HSN/SAC", "Qty", "Unit", "Rate", "Amount", "GST%", "GST Amt", "Total"]
    items = [
        ["1", "COTTON SHIRT MATERIAL", "21011190", "65", "MTRS", "54.55", "3545.75", "7.00", "248.20", "3793.95"],
        ["2", "COTTON PANT MATERIAL", "19019090", "51", "MTRS", "84.75", "4322.25", "7.00", "302.56", "4624.81"],
        ["3", "LINEN SHIRT MATERIAL", "19019090", "52", "MTRS", "98.25", "5109.00", "7.00", "357.63", "5466.63"],
        ["4", "LINEN PANT MATERIAL", "09042211", "39", "MTRS", "143.85", "5610.15", "7.00", "392.71", "6002.86"],
        ["5", "RAYON SHIRT MATERIAL", "13019013", "75", "MTRS", "43.45", "3258.75", "7.00", "228.11", "3486.86"],
        ["6", "RAYON PANT MATERIAL", "22021010", "59", "MTRS", "58.90", "3475.10", "7.00", "243.26", "3718.36"]
    ]

    full_table = [table_header] + items
    table = Table(full_table, repeatRows=1, colWidths=[1 * cm, 3.5 * cm, 2 * cm, 1.2 * cm, 1.5 * cm, 1.8 * cm, 2.2 * cm, 1.5 * cm, 2.2 * cm, 2.2 * cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BRAND_PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.3, colors.grey),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4)
    ]))
    elements.append(table)
    elements.append(Spacer(1, 12))

    summary_table = Table([
        ["Sub Total", "25,321.00"],
        ["GST 7%", "1,772.47"],
        ["Total", "27,093.47"]
    ], colWidths=[12 * cm, 4 * cm])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BRAND_LIGHT),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Amount In Words: <b>Singapore Dollars Twenty Seven Thousand Ninety Three And Forty Seven Cents Only</b>", normal_style))
    elements.append(Spacer(1, 12))

    bank_details = [
        ["Account Name:", "Paramount Clothing"],
        ["A/C No.:", "7678197857"],
        ["IFS Code:", "IDIB000P012"],
        ["Bank Name:", "Indian Bank, Pallavaram"],
        ["SWIFT Code:", "IDIBINBBMEP"]
    ]
    bank_table = Table(bank_details, colWidths=[5 * cm, 10 * cm])
    bank_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(Paragraph("<b>Bank Details:</b>", header_style))
    elements.append(bank_table)
    elements.append(Spacer(1, 24))

    elements.append(Paragraph("<b>For Paramount Clothing</b><br/><br/><br/>Authorized Signatory", ParagraphStyle(name='Sign', alignment=TA_RIGHT)))

    doc.build(elements)

if __name__ == "__main__":
    create_invoice("paramount_invoice_recreated.pdf")

