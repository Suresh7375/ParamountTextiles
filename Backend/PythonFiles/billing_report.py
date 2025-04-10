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
            self.leftMargin, self.bottomMargin + 10 * mm,
            self.width, self.height - 20 * mm, id='content')
        return PageTemplate(id='InvoiceTemplate', frames=frame, onPage=self._add_footer)

    def _add_footer(self, canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(BRAND_PRIMARY)
        canvas.setLineWidth(0.5)
        canvas.line(doc.leftMargin, doc.bottomMargin + 10 * mm,
                    doc.pagesize[0] - doc.rightMargin, doc.bottomMargin + 10 * mm)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(BRAND_SECONDARY)
        canvas.drawString(doc.leftMargin, doc.bottomMargin + 6 * mm,
                          f"{self.company_name} • GST Registered Company")
        canvas.drawCentredString(doc.pagesize[0] / 2, doc.bottomMargin + 6 * mm,
                                 "www.paramountclothing.com")
        canvas.drawRightString(doc.pagesize[0] - doc.rightMargin, doc.bottomMargin + 6 * mm,
                               f"Page {canvas.getPageNumber()}")
        canvas.drawCentredString(doc.pagesize[0] / 2, doc.bottomMargin + 2 * mm,
                                 "Email: info@paramountclothing.com • Phone: +65 9876 5432")
        canvas.restoreState()

def create_invoice(output_path):
    doc = InvoiceDocTemplate(output_path)
    styles = doc.styles

    title_style = ParagraphStyle(name='Title', fontSize=16, alignment=TA_CENTER, textColor=BRAND_PRIMARY)
    header_style = ParagraphStyle(name='Header', fontSize=10, textColor=BRAND_PRIMARY)
    normal_style = ParagraphStyle(name='Normal', fontSize=8, alignment=TA_RIGHT)

    elements = []

    elements.append(Paragraph("TAX INVOICE", title_style))
    elements.append(Spacer(1, 8))

    logo_path = "company_logo.png"
    if os.path.exists(logo_path):
        logo = Image(logo_path)
        logo._restrictSize(2.2 * cm, 2.2 * cm)  # Maintain aspect ratio within given box
    else:
        logo = Spacer(1, 2.2 * cm)

    company_name_para = Paragraph(
        """<para align=left>
            <font name="Helvetica-Bold" size="12" color="#2C3E50">Paramount Clothing</font><br/>
            <font name="Helvetica" size="8" color="#7F8C8D">Quality Apparel Exporters</font>
        </para>""",
        styles["Normal"]
    )

    invoice_details = Paragraph("Invoice #: PC-0001<br/>Date: 09.04.2025<br/>Our Ref: PC-0425-PI-01<br/>Your Ref: PO# 20250409", normal_style)
    company_info = [[
        logo,
        company_name_para,
        invoice_details
    ]]
    company_table = Table(company_info, colWidths=[2.5 * cm, 6.2 * cm, 10.0 * cm])
    company_table.setStyle(TableStyle([
        ('ALIGN', (2, 0), (2, 0), 'RIGHT')
    ]))
    elements.append(company_table)
    elements.append(Spacer(1, 8))

    bill_to_data = [
        ["Name:", "M/S. ABC STORES"],
        ["Address:", "#01-04, BLOCK 219"],
        ["Area:", "PARKLANDS, SERANGOON"],
        ["City:", "SINGAPORE"],
        ["PIN:", "315602"],
        ["GSTIN:", ""]
    ]

    ship_to_data = [
        ["Name:", "M/S. ABC STORES"],
        ["Address:", "#01-04, BLOCK 219"],
        ["Area:", "PARKLANDS, SERANGOON"],
        ["City:", "SINGAPORE"],
        ["PIN:", "315602"],
        ["", ""]
    ]

    bill_to_table = Table(bill_to_data, colWidths=[3.2 * cm, 9.3 * cm])
    ship_to_table = Table(ship_to_data, colWidths=[3.2 * cm, 9.3 * cm])
    for tbl in [bill_to_table, ship_to_table]:
        tbl.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('TOPPADDING', (0, 0), (-1, -1), 1),
        ]))

    contact_table = Table([
        [Paragraph("<b>Bill To</b>", header_style), Paragraph("<b>Ship To</b>", header_style)],
        [bill_to_table, ship_to_table]
    ], colWidths=[9.95 * cm, 9.95 * cm])
    contact_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BRAND_LIGHT),
        ('BOX', (0, 0), (-1, -1), 0.3, colors.grey),
        ('INNERGRID', (0, 0), (-1, -1), 0.2, colors.lightgrey),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
    ]))
    elements.append(contact_table)
    elements.append(Spacer(1, 8))

    table_header = ["Sl. No.", "Description", "HSN/SAC", "Qty", "Unit", "Rate", "Amount", "GST%", "GST Amt", "Total"]
    items = [
        ["1", "COTTON SHIRT MATERIAL", "21011190", "65", "MTRS", "54.55", "3545.75", "7.00", "248.20", "3793.95"],
        ["2", "COTTON PANT MATERIAL", "19019090", "51", "MTRS", "84.75", "4322.25", "7.00", "302.56", "4624.81"],
        ["3", "LINEN SHIRT MATERIAL", "19019090", "52", "MTRS", "98.25", "5109.00", "7.00", "357.63", "5466.63"],
        ["4", "LINEN PANT MATERIAL", "09042211", "39", "MTRS", "143.85", "5610.15", "7.00", "392.71", "6002.86"],
        ["5", "RAYON SHIRT MATERIAL", "13019013", "75", "MTRS", "43.45", "3258.75", "7.00", "228.11", "3486.86"],
        ["6", "RAYON PANT MATERIAL", "22021010", "59", "MTRS", "58.90", "3475.10", "7.00", "243.26", "3718.36"]
    ]

    table = Table([table_header] + items, repeatRows=1,
                  colWidths=[1.2 * cm, 4 * cm, 2.2 * cm, 1.2 * cm, 1.4 * cm, 1.6 * cm, 2.1 * cm, 1.4 * cm, 2.1 * cm, 2.3 * cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BRAND_PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.3, colors.grey),
        ('FONTSIZE', (0, 0), (-1, -1), 7.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3)
    ]))
    elements.append(table)
    elements.append(Spacer(1, 8))

    summary_data = [
        [Paragraph("Sub Total", normal_style), Paragraph("25,321.00", normal_style)],
        [Paragraph("GST @ 7%", normal_style), Paragraph("1,772.47", normal_style)],
        [Paragraph("<b>Total</b>", ParagraphStyle('TotalBold', parent=normal_style, fontName='Helvetica-Bold')),
         Paragraph("<b>27,093.47</b>",
                   ParagraphStyle('TotalBoldRight', parent=normal_style, fontName='Helvetica-Bold'))]
    ]

    summary_table = Table(summary_data, colWidths=[15.0 * cm, 4.1 * cm])
    summary_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('BACKGROUND', (0, -1), (-1, -1), BRAND_LIGHT),
        ('LINEABOVE', (0, -1), (-1, -1), 0.5, colors.grey),
        ('LINEBELOW', (0, -1), (-1, -1), 0.5, colors.grey),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 4)
    ]))
    elements.append(summary_table)

    # elements.append(Spacer(1, 4))
    LEFT_INDENT_CM = 0.3 * cm

    amount_words_para = Paragraph(
        "<b>Amount in Words:</b><br/><font color='#2C3E50'>Singapore Dollars Twenty Seven Thousand Ninety Three And Forty Seven Cents Only</font>",
        ParagraphStyle(
            name='Words',
            fontSize=8,
            leading=10,
            textColor=BRAND_SECONDARY,
            alignment=TA_LEFT
        )
    )
    amount_words_table = Table([[amount_words_para]], colWidths=[19.9 * cm])
    amount_words_table.setStyle(TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), LEFT_INDENT_CM),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    elements.append(Spacer(1, 4))
    elements.append(amount_words_table)

    small_style = ParagraphStyle(name="Small", fontSize=7.5)

    bank_data = [
        [Paragraph("<b>Account Name:</b>", small_style), "Paramount Clothing",
         Paragraph("<b>A/C No.:</b>", small_style), "7678197857"],
        [Paragraph("<b>Bank Name:</b>", small_style), "Indian Bank, Pallavaram",
         Paragraph("<b>SWIFT Code:</b>", small_style), "IDIBINBBMEP"],
        [Paragraph("<b>IFS Code:</b>", small_style), "IDIB000P012", "", ""]
    ]

    bank_table = Table(bank_data, colWidths=[3.2 * cm, 6.5 * cm, 3.2 * cm, 6.5 * cm])
    bank_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.3, colors.lightgrey),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 7.8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))

    bank_header = Paragraph(
        "<b><u>Bank Details</u></b>",
        ParagraphStyle(
            name='BankHeader',
            fontSize=8.5,
            textColor=BRAND_PRIMARY,
            alignment=TA_LEFT
        )
    )
    bank_header_table = Table([[bank_header]], colWidths=[19.9 * cm])
    bank_header_table.setStyle(TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), LEFT_INDENT_CM),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    elements.append(Spacer(1, 6))
    elements.append(bank_header_table)

    # Existing bank table remains as is
    elements.append(bank_table)

    elements.append(Spacer(1, 6))
    elements.append(Paragraph("For Paramount Clothing<br/><br/><br/>Authorized Signatory",
                              ParagraphStyle(name='Sign', alignment=TA_RIGHT, fontSize=8)))
    doc.build(elements)

if __name__ == "__main__":
    create_invoice("paramount_invoice_recreated.pdf")
