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

# Brand Colors - Modern Professional Palette
BRAND_PRIMARY = colors.HexColor("#1A365D")  # Deep Navy Blue
BRAND_SECONDARY = colors.HexColor("#4A6FA5")  # Medium Blue
BRAND_ACCENT = colors.HexColor("#FF6B6B")  # Accent Red
BRAND_LIGHT = colors.HexColor("#F7FAFC")  # Off-White
BRAND_TEXT = colors.HexColor("#2D3748")  # Dark Gray for Text
BRAND_HIGHLIGHT = colors.HexColor("#EDF2F7")  # Light Gray for Highlights
TABLE_HEADER = colors.HexColor("#2C5282")  # Table Header Blue

class InvoiceDocTemplate(BaseDocTemplate):
    def __init__(self, filename, company_name="Paramount Clothing", **kwargs):
        # Further reduce margins
        super().__init__(filename, pagesize=A4,
                         leftMargin=1.0 * cm, rightMargin=1.0 * cm,  # Reduced margins
                         topMargin=1.2 * cm, bottomMargin=1.2 * cm, **kwargs)  # Reduced margins
        self.company_name = company_name
        self.styles = getSampleStyleSheet()
        self.addPageTemplates([self._create_template()])

    def _create_template(self):
        frame = Frame(
            self.leftMargin, self.bottomMargin + 12 * mm,
            self.width, self.height - 24 * mm, id='content')
        return PageTemplate(id='InvoiceTemplate', frames=frame, onPage=self._add_page_elements)

    def _add_page_elements(self, canvas, doc):
        canvas.saveState()

        # Page Header with gradient
        canvas.setFillColorRGB(0.1, 0.21, 0.36, 1.0)  # Base color of gradient
        canvas.rect(0, doc.height + doc.topMargin - 0.5 * cm, doc.pagesize[0], 0.8 * cm, fill=1, stroke=0)

        # Header line
        canvas.setStrokeColor(BRAND_ACCENT)
        canvas.setLineWidth(2)
        canvas.line(doc.leftMargin, doc.height + doc.topMargin - 0.5 * cm,
                    doc.pagesize[0] - doc.rightMargin, doc.height + doc.topMargin - 0.5 * cm)

        # Footer with gradient and content
        canvas.setStrokeColor(BRAND_SECONDARY)
        canvas.setLineWidth(0.5)
        canvas.line(doc.leftMargin, doc.bottomMargin + 10 * mm,
                    doc.pagesize[0] - doc.rightMargin, doc.bottomMargin + 10 * mm)

        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(BRAND_TEXT)
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

    # Enhanced Styles with ReportLab's built-in fonts
    title_style = ParagraphStyle(
        name='Title',
        fontSize=18,
        alignment=TA_CENTER,
        textColor=BRAND_PRIMARY,
        fontName='Helvetica-Bold',
        spaceAfter=12
    )

    header_style = ParagraphStyle(
        name='Header',
        fontSize=10,
        textColor=BRAND_PRIMARY,
        fontName='Helvetica-Bold',
        leading=14
    )

    normal_style = ParagraphStyle(
        name='Normal',
        fontSize=9,
        alignment=TA_LEFT,
        textColor=BRAND_TEXT,
        fontName='Helvetica'
    )

    elements = []

    # Logo and Company Info in Header
    logo_path = "company_logo.png"
    if os.path.exists(logo_path):
        logo = Image(logo_path)
        logo._restrictSize(2.4 * cm, 2.4 * cm)
    else:
        initials_style = ParagraphStyle(
            name='Initials',
            fontSize=22,
            alignment=TA_CENTER,
            textColor=colors.white,
            fontName='Helvetica-Bold'
        )
        logo = Table(
            [[Paragraph("PC", initials_style)]],
            colWidths=[2.4 * cm],
            rowHeights=[2.4 * cm]
        )
        logo.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), BRAND_SECONDARY),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))

    # Enhanced Invoice Header
    company_name_para = Paragraph(
        f"""<para align=left>
            <font name="Helvetica-Bold" size="14" color="#{BRAND_PRIMARY.hexval()[2:]}">{doc.company_name}</font><br/>
            <font name="Helvetica" size="9" color="#{BRAND_SECONDARY.hexval()[2:]}">Quality Apparel Exporters</font>
        </para>""",
        styles["Normal"]
    )

    invoice_details = Paragraph(
        f"""<para align=right>
            <font name="Helvetica-Bold" size="14" color="#{BRAND_PRIMARY.hexval()[2:]}">TAX INVOICE</font><br/><br/>
            <font name="Helvetica-Bold" size="9" color="#{BRAND_TEXT.hexval()[2:]}">Invoice #:</font> 
            <font name="Helvetica" size="9" color="#{BRAND_TEXT.hexval()[2:]}">PC-0001</font><br/>
            <font name="Helvetica-Bold" size="9" color="#{BRAND_TEXT.hexval()[2:]}">Date:</font> 
            <font name="Helvetica" size="9" color="#{BRAND_TEXT.hexval()[2:]}">{date.today().strftime('%d.%m.%Y')}</font><br/>
            <font name="Helvetica-Bold" size="9" color="#{BRAND_TEXT.hexval()[2:]}">Our Ref:</font> 
            <font name="Helvetica" size="9" color="#{BRAND_TEXT.hexval()[2:]}">PC-0425-PI-01</font><br/>
            <font name="Helvetica-Bold" size="9" color="#{BRAND_TEXT.hexval()[2:]}">Your Ref:</font> 
            <font name="Helvetica" size="9" color="#{BRAND_TEXT.hexval()[2:]}">PO# 20250409</font>
        </para>""",
        styles["Normal"]
    )

    company_info = [[
        logo,
        company_name_para,
        invoice_details
    ]]

    # Create header with balanced column widths
    company_table = Table(company_info, colWidths=[2.7 * cm, 9.0 * cm, 7.0 * cm])
    company_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'LEFT'),
        ('ALIGN', (2, 0), (2, 0), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))

    elements.append(company_table)
    elements.append(Spacer(1, 12))

    # Add horizontal rule for visual separation
    elements.append(HRFlowable(
        width="100%",
        thickness=1,
        color=BRAND_LIGHT,
        spaceBefore=8,
        spaceAfter=12,
        hAlign='CENTER'
    ))

    # Enhanced Contact Info Section
    def create_contact_table(title, data):
        rows = []
        for label, value in data:
            rows.append([
                Paragraph(f"<b>{label}</b>",
                          ParagraphStyle(name='ContactLabel', fontSize=8.5, textColor=BRAND_TEXT,
                                         fontName='Helvetica-Bold')),
                Paragraph(f"{value}",
                          ParagraphStyle(name='ContactValue', fontSize=8.5, textColor=BRAND_TEXT,
                                         fontName='Helvetica'))
            ])

        contact_detail = Table(rows, colWidths=[3.0 * cm, 5.7 * cm])  # Adjusted widths
        contact_detail.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
            ('TOPPADDING', (0, 0), (-1, -1), 1),
        ]))

        # Create header for the section
        header = Table(
            [[Paragraph(f"<b>{title}</b>",
                        ParagraphStyle(name='ContactHeader', fontSize=9, textColor=colors.white,
                                       fontName='Helvetica-Bold'))]],
            colWidths=[8.7 * cm],  # Adjusted width
            rowHeights=[0.6 * cm]  # Reduced height
        )
        header.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), TABLE_HEADER),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ]))

        # Create the complete contact section with header and content
        section = Table(
            [[header], [contact_detail]],
            colWidths=[9.2 * cm]
        )
        section.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 0.5, BRAND_SECONDARY),
            ('LINEBELOW', (0, 0), (-1, 0), 0.5, BRAND_SECONDARY),
        ]))

        return section

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
        ["GSTIN:", ""]
    ]

    bill_to_section = create_contact_table("BILL TO", bill_to_data)
    ship_to_section = create_contact_table("SHIP TO", ship_to_data)

    contact_table = Table(
        [[bill_to_section, Spacer(1, 0), ship_to_section]],
        colWidths=[9.2 * cm, 0.5 * cm, 9.2 * cm]
    )

    # Reduce spacing between sections
    elements.append(Spacer(1, 8))  # Reduced from 12

    # Reduce spacing after horizontal rule
    elements.append(HRFlowable(
        width="100%",
        thickness=1,
        color=BRAND_LIGHT,
        spaceBefore=6,  # Reduced from 8
        spaceAfter=8,   # Reduced from 12
        hAlign='CENTER'
    ))

    # Enhanced Contact Info Section
    def create_contact_table(title, data):
        rows = []
        for label, value in data:
            rows.append([
                Paragraph(f"<b>{label}</b>",
                          ParagraphStyle(name='ContactLabel', fontSize=8.5, textColor=BRAND_TEXT,
                                         fontName='Helvetica-Bold')),
                Paragraph(f"{value}",
                          ParagraphStyle(name='ContactValue', fontSize=8.5, textColor=BRAND_TEXT,
                                         fontName='Helvetica'))
            ])

        contact_detail = Table(rows, colWidths=[3.0 * cm, 5.7 * cm])  # Adjusted widths
        contact_detail.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
            ('TOPPADDING', (0, 0), (-1, -1), 1),
        ]))

        # Create header for the section
        header = Table(
            [[Paragraph(f"<b>{title}</b>",
                        ParagraphStyle(name='ContactHeader', fontSize=9, textColor=colors.white,
                                       fontName='Helvetica-Bold'))]],
            colWidths=[8.7 * cm],  # Adjusted width
            rowHeights=[0.6 * cm]  # Reduced height
        )
        header.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), TABLE_HEADER),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ]))

        # Create the complete contact section with header and content
        section = Table(
            [[header], [contact_detail]],
            colWidths=[9.2 * cm]
        )
        section.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 0.5, BRAND_SECONDARY),
            ('LINEBELOW', (0, 0), (-1, 0), 0.5, BRAND_SECONDARY),
        ]))

        return section

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
        ["GSTIN:", ""]
    ]

    bill_to_section = create_contact_table("BILL TO", bill_to_data)
    ship_to_section = create_contact_table("SHIP TO", ship_to_data)

    contact_table = Table(
        [[bill_to_section, Spacer(1, 0), ship_to_section]],
        colWidths=[9.2 * cm, 0.5 * cm, 9.2 * cm]
    )

    elements.append(contact_table)
    elements.append(Spacer(1, 15))

    # Enhanced Line Items Table
    table_header = ["Sl. No.", "Description", "HSN/SAC", "Qty", "Unit", "Rate", "Amount", "GST%", "GST Amt", "Total"]
    items = [
        ["1", "COTTON SHIRT MATERIAL", "21011190", "65", "MTRS", "54.55", "3,545.75", "7.00", "248.20", "3,793.95"],
        ["2", "COTTON PANT MATERIAL", "19019090", "51", "MTRS", "84.75", "4,322.25", "7.00", "302.56", "4,624.81"],
        ["3", "LINEN SHIRT MATERIAL", "19019090", "52", "MTRS", "98.25", "5,109.00", "7.00", "357.63", "5,466.63"],
        ["4", "LINEN PANT MATERIAL", "09042211", "39", "MTRS", "143.85", "5,610.15", "7.00", "392.71", "6,002.86"],
        ["5", "RAYON SHIRT MATERIAL", "13019013", "75", "MTRS", "43.45", "3,258.75", "7.00", "228.11", "3,486.86"],
        ["6", "RAYON PANT MATERIAL", "22021010", "59", "MTRS", "58.90", "3,475.10", "7.00", "243.26", "3,718.36"]
    ]

    # Create a more visually appealing table with alternating row colors
    table = Table([table_header] + items, repeatRows=1,
                  colWidths=[1.04 * cm, 5 * cm, 1.94 * cm, 1.14 * cm, 1.34 * cm, 1.4 * cm,
                        1.64 * cm, 1.44 * cm, 2.04 * cm, 2.24 * cm])

    # Advanced table styling
    table_style = [
        # Header styling
        ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEADER),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),

        # Data cells alignment
        ('ALIGN', (0, 1), (0, -1), 'CENTER'),  # Serial number centered
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),  # Description left-aligned
        ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),  # All numeric values right-aligned

        # Borders and grid
        ('GRID', (0, 0), (-1, -1), 0.15, colors.lightgrey),
        ('LINEBELOW', (0, 0), (-1, 0), 1, BRAND_SECONDARY),  # Thicker line below header

        # Cell padding
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),

        # Font settings
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
    ]

    # Add alternating row colors
    for i in range(len(items)):
        if i % 2 == 0:
            table_style.append(('BACKGROUND', (0, i + 1), (-1, i + 1), BRAND_HIGHLIGHT))

    table.setStyle(TableStyle(table_style))
    elements.append(table)
    elements.append(Spacer(1, 12))

    # Summary Table with Enhanced Visual Styling
    summary_data = [
        [Paragraph("Sub Total", ParagraphStyle('SubTotal', parent=normal_style, fontName='Helvetica')),

         Paragraph("25,321.00", ParagraphStyle('SubTotalVal', parent=normal_style, fontName='Helvetica'))],
        [Paragraph("GST @ 7%", ParagraphStyle('Tax', parent=normal_style, fontName='Helvetica')),

         Paragraph("1,772.47", ParagraphStyle('TaxVal', parent=normal_style, fontName='Helvetica'))],
        [Paragraph("<b>Total</b>",
                   ParagraphStyle('TotalBold', parent=normal_style, fontName='Helvetica-Bold', fontSize=10)),
         Paragraph("<b>27,093.47</b>",
                   ParagraphStyle('TotalBoldRight', parent=normal_style, fontName='Helvetica-Bold', fontSize=10))]
    ]

    # Create summary table with balanced layout
    summary_table = Table(
        summary_data,
        colWidths=[15.5 * cm, 3.4 * cm]
    )

    # Apply enhanced styling to summary table
    summary_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('BACKGROUND', (0, 0), (1, 0), BRAND_LIGHT),
        ('BACKGROUND', (0, 1), (1, 1), BRAND_LIGHT),
        ('BACKGROUND', (0, 2), (1, 2), BRAND_HIGHLIGHT),
        ('LINEABOVE', (0, 2), (1, 2), 0.5, BRAND_PRIMARY),
        ('LINEBELOW', (0, 2), (1, 2), 0.5, BRAND_PRIMARY),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        # Box around the total row
        ('BOX', (0, 2), (1, 2), 0.5, BRAND_PRIMARY),
    ]))

    elements.append(summary_table)
    elements.append(Spacer(1, 8))

    # Amount in Words Section with Better Styling
    amount_words_para = Paragraph(
        f"""<para><font name="Helvetica-Bold" size="9" color="#{BRAND_PRIMARY.hexval()[2:]}">Amount in Words:</font><br/>
        <font name="Helvetica" size="9" color="#{BRAND_TEXT.hexval()[2:]}">Singapore Dollars Twenty Seven Thousand Ninety Three And Forty Seven Cents Only</font></para>""",
        ParagraphStyle(
            name='Words',
            fontSize=9,
            leading=12,
            textColor=BRAND_TEXT,
            alignment=TA_LEFT
        )
    )

    # Place in a styled box
    amount_words_table = Table(
        [[amount_words_para]],
        colWidths=[19.0 * cm]
    )
    amount_words_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), BRAND_LIGHT),
        ('BOX', (0, 0), (0, 0), 0.5, BRAND_SECONDARY),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(amount_words_table)
    elements.append(Spacer(1, 12))

    # Bank Details Section with Enhanced Visual Appeal
    bank_header = Paragraph(
        f"""<para><font name="Helvetica-Bold" size="10" color="#{BRAND_PRIMARY.hexval()[2:]}">Bank Details</font></para>""",
        ParagraphStyle(
            name='BankHeader',
            fontSize=10,
            textColor=BRAND_PRIMARY,
            alignment=TA_LEFT
        )
    )

    # Create bank details in a more visually appealing table
    bank_data_style = ParagraphStyle(
        name="BankData",
        fontSize=8.5,
        fontName='Helvetica',
        textColor=BRAND_TEXT
    )

    bank_label_style = ParagraphStyle(
        name="BankLabel",
        fontSize=8.5,
        fontName='Helvetica-Bold',
        textColor=BRAND_PRIMARY
    )

    bank_data = [
        [Paragraph("Account Name:", bank_label_style),
         Paragraph("Paramount Clothing", bank_data_style),
         Paragraph("A/C No.:", bank_label_style),
         Paragraph("7678197857", bank_data_style)],
        [Paragraph("Bank Name:", bank_label_style),
         Paragraph("Indian Bank, Pallavaram", bank_data_style),
         Paragraph("SWIFT Code:", bank_label_style),
         Paragraph("IDIBINBBMEP", bank_data_style)],
        [Paragraph("IFS Code:", bank_label_style),
         Paragraph("IDIB000P012", bank_data_style), "", ""]
    ]

    # Create bank details table with modern styling
    bank_table = Table(
        bank_data,
        colWidths=[2.8 * cm, 6.9 * cm, 2.5 * cm, 6.7 * cm]
    )

    bank_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BRAND_LIGHT),
        ('GRID', (0, 0), (-1, -1), 0.15, colors.lightgrey),
        ('BOX', (0, 0), (-1, -1), 0.5, BRAND_SECONDARY),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))

    # Combine bank header and details
    bank_section = Table(
        [[bank_header], [Spacer(1, 5)], [bank_table]],
        colWidths=[19.0 * cm]
    )
    bank_section.setStyle(TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))

    elements.append(bank_section)
    elements.append(Spacer(1, 18))

    # Signature Section with Modern Styling
    signature_text = Paragraph(
        f"""<para>For <b>Paramount Clothing</b><br/><br/>
        <font name="Helvetica-Bold" size="9" color="#{BRAND_PRIMARY.hexval()[2:]}">Authorized Signatory</font></para>""",
        ParagraphStyle(
            name='Sign',
            alignment=TA_RIGHT,
            fontSize=9,
            fontName='Helvetica',
            textColor=BRAND_TEXT
        )
    )

    # Add thank you note
    thank_you_note = Paragraph(
        f"""<para align="center"><font name="Helvetica-Oblique" size="9" color="#{BRAND_SECONDARY.hexval()[2:]}">
        Thank you for your business!</font></para>""",
        ParagraphStyle(
            name='ThankYou',
            alignment=TA_CENTER,
            fontSize=9,
            fontName='Helvetica-Oblique',
            textColor=BRAND_SECONDARY
        )
    )

    # Create signature table
    signature_table = Table(
        [[signature_text, thank_you_note]],
        colWidths=[9.5 * cm, 9.5 * cm]
    )
    signature_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
        ('ALIGN', (1, 0), (1, 0), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
    ]))

    elements.append(signature_table)

    # Build the document
    doc.build(elements)

if __name__ == "__main__":
    create_invoice("paramount_invoice_modern.pdf")