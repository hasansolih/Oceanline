"""
Generate Data Flow Diagram (DFD) PDF
Creates Level 0 and Level 1 DFDs for OceanLine Ferry Booking System
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Circle, Polygon
from datetime import datetime

def create_dfd_pdf():
    """Generate Data Flow Diagram PDF"""
    
    filename = "OceanLine_Data_Flow_Diagram.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4,
                          rightMargin=50, leftMargin=50,
                          topMargin=50, bottomMargin=50)
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#0d6efd'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#0d6efd'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#495057'),
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )
    
    # Title Page
    elements.append(Spacer(1, 1*inch))
    elements.append(Paragraph("OceanLine Ferry Service", title_style))
    elements.append(Paragraph("Data Flow Diagram (DFD)", heading1_style))
    elements.append(Spacer(1, 0.5*inch))
    
    # Project info
    info_data = [
        ['Project:', 'OceanLine Ferry Booking System'],
        ['Student ID:', 'ST7078'],
        ['Name:', 'Hassan Solih'],
        ['Date:', datetime.now().strftime('%B %d, %Y')],
        ['Document:', 'Context & Level 1 DFD'],
    ]
    
    info_table = Table(info_data, colWidths=[1.5*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#495057')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    elements.append(info_table)
    elements.append(PageBreak())
    
    # DFD Legend
    elements.append(Paragraph("DFD Symbol Legend", heading1_style))
    elements.append(Spacer(1, 0.2*inch))
    
    legend_drawing = Drawing(500, 200)
    
    # External Entity (Rectangle)
    legend_drawing.add(Rect(20, 150, 100, 40, fillColor=colors.HexColor('#ffe0b2'), 
                           strokeColor=colors.black, strokeWidth=2))
    legend_drawing.add(String(70, 165, 'External Entity',
                             fontSize=10, fontName='Helvetica-Bold', textAnchor='middle'))
    legend_drawing.add(String(200, 170, 'External user or system',
                             fontSize=9, fontName='Helvetica', textAnchor='start'))
    
    # Process (Circle)
    legend_drawing.add(Circle(70, 100, 30, fillColor=colors.HexColor('#bbdefb'), 
                             strokeColor=colors.black, strokeWidth=2))
    legend_drawing.add(String(70, 95, 'Process',
                             fontSize=9, fontName='Helvetica-Bold', textAnchor='middle'))
    legend_drawing.add(String(200, 100, 'System process/function',
                             fontSize=9, fontName='Helvetica', textAnchor='start'))
    
    # Data Store (Double line)
    legend_drawing.add(Line(20, 50, 120, 50, strokeColor=colors.black, strokeWidth=2))
    legend_drawing.add(Line(20, 40, 120, 40, strokeColor=colors.black, strokeWidth=2))
    legend_drawing.add(String(70, 30, 'Data Store',
                             fontSize=9, fontName='Helvetica-Bold', textAnchor='middle'))
    legend_drawing.add(String(200, 45, 'Database or file storage',
                             fontSize=9, fontName='Helvetica', textAnchor='start'))
    
    # Data Flow (Arrow)
    legend_drawing.add(Line(20, 10, 120, 10, strokeColor=colors.black, strokeWidth=2))
    legend_drawing.add(Polygon([115, 10, 120, 13, 120, 7],
                              fillColor=colors.black, strokeColor=colors.black))
    legend_drawing.add(String(200, 10, 'Data flow direction',
                             fontSize=9, fontName='Helvetica', textAnchor='start'))
    
    elements.append(legend_drawing)
    elements.append(PageBreak())
    
    # Context Diagram (Level 0)
    elements.append(Paragraph("Context Diagram (Level 0 DFD)", heading1_style))
    elements.append(Spacer(1, 0.2*inch))
    
    context_desc = "High-level view showing the OceanLine system and its external entities."
    elements.append(Paragraph(context_desc, styles['BodyText']))
    elements.append(Spacer(1, 0.3*inch))
    
    context_drawing = Drawing(500, 400)
    
    # Central System (Circle)
    context_drawing.add(Circle(250, 200, 60, fillColor=colors.HexColor('#bbdefb'), 
                               strokeColor=colors.black, strokeWidth=3))
    context_drawing.add(String(250, 205, 'OceanLine',
                              fontSize=12, fontName='Helvetica-Bold', textAnchor='middle'))
    context_drawing.add(String(250, 190, 'Ferry Booking',
                              fontSize=11, fontName='Helvetica-Bold', textAnchor='middle'))
    context_drawing.add(String(250, 175, 'System',
                              fontSize=11, fontName='Helvetica-Bold', textAnchor='middle'))
    
    # External Entities
    # Customer
    context_drawing.add(Rect(50, 330, 100, 50, fillColor=colors.HexColor('#ffe0b2'), 
                            strokeColor=colors.black, strokeWidth=2))
    context_drawing.add(String(100, 350, 'Customer',
                              fontSize=11, fontName='Helvetica-Bold', textAnchor='middle'))
    
    # Admin
    context_drawing.add(Rect(350, 330, 100, 50, fillColor=colors.HexColor('#ffe0b2'), 
                            strokeColor=colors.black, strokeWidth=2))
    context_drawing.add(String(400, 350, 'Administrator',
                              fontSize=11, fontName='Helvetica-Bold', textAnchor='middle'))
    
    # Bank/Payment
    context_drawing.add(Rect(350, 70, 100, 50, fillColor=colors.HexColor('#ffe0b2'), 
                            strokeColor=colors.black, strokeWidth=2))
    context_drawing.add(String(400, 90, 'Bank/Payment',
                              fontSize=11, fontName='Helvetica-Bold', textAnchor='middle'))
    
    # Email System
    context_drawing.add(Rect(50, 70, 100, 50, fillColor=colors.HexColor('#ffe0b2'), 
                            strokeColor=colors.black, strokeWidth=2))
    context_drawing.add(String(100, 90, 'Email System',
                              fontSize=11, fontName='Helvetica-Bold', textAnchor='middle'))
    
    # Data Flows - Customer
    # Customer -> System: Booking Request
    context_drawing.add(Line(150, 340, 210, 250, strokeColor=colors.blue, strokeWidth=2))
    context_drawing.add(Polygon([205, 245, 210, 250, 206, 253],
                               fillColor=colors.blue, strokeColor=colors.blue))
    context_drawing.add(String(175, 300, 'Booking Request',
                              fontSize=8, fontName='Helvetica', textAnchor='middle', fillColor=colors.blue))
    
    # System -> Customer: Confirmation
    context_drawing.add(Line(210, 230, 150, 350, strokeColor=colors.green, strokeWidth=2, strokeDashArray=[3, 2]))
    context_drawing.add(Polygon([155, 350, 150, 350, 153, 345],
                               fillColor=colors.green, strokeColor=colors.green))
    context_drawing.add(String(170, 280, 'Confirmation',
                              fontSize=8, fontName='Helvetica', textAnchor='middle', fillColor=colors.green))
    
    # Admin -> System: Manage
    context_drawing.add(Line(350, 340, 290, 250, strokeColor=colors.blue, strokeWidth=2))
    context_drawing.add(Polygon([295, 253, 290, 250, 294, 246],
                               fillColor=colors.blue, strokeColor=colors.blue))
    context_drawing.add(String(325, 300, 'Management',
                              fontSize=8, fontName='Helvetica', textAnchor='middle', fillColor=colors.blue))
    
    # System -> Admin: Reports
    context_drawing.add(Line(290, 230, 350, 350, strokeColor=colors.green, strokeWidth=2, strokeDashArray=[3, 2]))
    context_drawing.add(Polygon([345, 350, 350, 350, 347, 345],
                               fillColor=colors.green, strokeColor=colors.green))
    context_drawing.add(String(330, 280, 'Reports',
                              fontSize=8, fontName='Helvetica', textAnchor='middle', fillColor=colors.green))
    
    # System -> Bank: Payment Info
    context_drawing.add(Line(290, 170, 350, 100, strokeColor=colors.blue, strokeWidth=2))
    context_drawing.add(Polygon([345, 100, 350, 100, 347, 105],
                               fillColor=colors.blue, strokeColor=colors.blue))
    context_drawing.add(String(325, 140, 'Payment Info',
                              fontSize=8, fontName='Helvetica', textAnchor='middle', fillColor=colors.blue))
    
    # Bank -> System: Payment Status
    context_drawing.add(Line(350, 90, 290, 180, strokeColor=colors.green, strokeWidth=2, strokeDashArray=[3, 2]))
    context_drawing.add(Polygon([295, 180, 290, 180, 293, 175],
                               fillColor=colors.green, strokeColor=colors.green))
    context_drawing.add(String(330, 120, 'Status',
                              fontSize=8, fontName='Helvetica', textAnchor='middle', fillColor=colors.green))
    
    # System -> Email: Notifications
    context_drawing.add(Line(210, 170, 150, 100, strokeColor=colors.blue, strokeWidth=2))
    context_drawing.add(Polygon([155, 100, 150, 100, 153, 105],
                               fillColor=colors.blue, strokeColor=colors.blue))
    context_drawing.add(String(175, 140, 'Notifications',
                              fontSize=8, fontName='Helvetica', textAnchor='middle', fillColor=colors.blue))
    
    elements.append(context_drawing)
    elements.append(PageBreak())
    
    # Level 1 DFD
    elements.append(Paragraph("Level 1 Data Flow Diagram", heading1_style))
    elements.append(Spacer(1, 0.2*inch))
    
    level1_desc = "Detailed view of internal processes within the OceanLine Ferry Booking System."
    elements.append(Paragraph(level1_desc, styles['BodyText']))
    elements.append(Spacer(1, 0.3*inch))
    
    level1_drawing = Drawing(520, 650)
    
    # External Entities
    # Customer
    level1_drawing.add(Rect(10, 550, 90, 40, fillColor=colors.HexColor('#ffe0b2'), 
                           strokeColor=colors.black, strokeWidth=2))
    level1_drawing.add(String(55, 565, 'Customer',
                             fontSize=10, fontName='Helvetica-Bold', textAnchor='middle'))
    
    # Admin
    level1_drawing.add(Rect(420, 550, 90, 40, fillColor=colors.HexColor('#ffe0b2'), 
                           strokeColor=colors.black, strokeWidth=2))
    level1_drawing.add(String(465, 565, 'Admin',
                             fontSize=10, fontName='Helvetica-Bold', textAnchor='middle'))
    
    # Processes (Circles with numbers)
    processes = [
        (1, "User\nAuthentication", 120, 500, colors.HexColor('#e3f2fd')),
        (2, "Booking\nManagement", 260, 500, colors.HexColor('#bbdefb')),
        (3, "Seat\nSelection", 400, 500, colors.HexColor('#90caf9')),
        (4, "Payment\nProcessing", 260, 380, colors.HexColor('#64b5f6')),
        (5, "Schedule\nManagement", 120, 260, colors.HexColor('#42a5f5')),
        (6, "Report\nGeneration", 400, 260, colors.HexColor('#2196f3')),
        (7, "System\nConfiguration", 260, 140, colors.HexColor('#1976d2')),
    ]
    
    for num, name, x, y, color in processes:
        level1_drawing.add(Circle(x, y, 35, fillColor=color, 
                                 strokeColor=colors.black, strokeWidth=2))
        level1_drawing.add(String(x, y + 15, str(num),
                                 fontSize=11, fontName='Helvetica-Bold', textAnchor='middle'))
        lines = name.split('\n')
        level1_drawing.add(String(x, y - 5, lines[0],
                                 fontSize=8, fontName='Helvetica', textAnchor='middle'))
        if len(lines) > 1:
            level1_drawing.add(String(x, y - 15, lines[1],
                                     fontSize=8, fontName='Helvetica', textAnchor='middle'))
    
    # Data Stores
    datastores = [
        ("D1", "Users DB", 120, 380),
        ("D2", "Bookings DB", 260, 620),
        ("D3", "Schedules DB", 400, 380),
        ("D4", "Config Store", 400, 140),
    ]
    
    for ds_id, ds_name, x, y in datastores:
        # Double line for data store
        level1_drawing.add(Line(x - 50, y, x + 50, y, strokeColor=colors.black, strokeWidth=2))
        level1_drawing.add(Line(x - 50, y - 10, x + 50, y - 10, strokeColor=colors.black, strokeWidth=2))
        level1_drawing.add(String(x - 45, y - 5, ds_id,
                                 fontSize=8, fontName='Helvetica-Bold', textAnchor='start'))
        level1_drawing.add(String(x, y - 5, ds_name,
                                 fontSize=8, fontName='Helvetica', textAnchor='middle'))
    
    # Data Flows (simplified key flows)
    flows = [
        # Customer -> P1
        (55, 550, 100, 530, "Login", colors.blue),
        # P1 -> D1
        (120, 465, 120, 390, "User Data", colors.green),
        # P1 -> P2
        (155, 500, 225, 500, "Auth Token", colors.blue),
        # P2 -> D2
        (260, 535, 260, 610, "Booking", colors.green),
        # P2 -> P3
        (295, 500, 365, 500, "Seat Info", colors.blue),
        # P3 -> D3
        (400, 465, 400, 390, "Availability", colors.green),
        # P3 -> P4
        (380, 470, 280, 410, "Selection", colors.blue),
        # P4 -> D2
        (240, 410, 240, 610, "Payment", colors.green),
        # Admin -> P5
        (465, 550, 450, 530, "Manage", colors.blue),
        # P5 -> D3
        (155, 280, 350, 340, "Schedule", colors.green),
        # Admin -> P6
        (445, 550, 420, 530, "Request", colors.blue),
        # P6 -> D2
        (380, 280, 280, 610, "Data", colors.green),
        # P7 -> D4
        (295, 150, 350, 150, "Config", colors.green),
    ]
    
    for x1, y1, x2, y2, label, color in flows:
        level1_drawing.add(Line(x1, y1, x2, y2, strokeColor=color, strokeWidth=1.5))
        # Arrow head
        dx = x2 - x1
        dy = y2 - y1
        import math
        angle = math.atan2(dy, dx)
        level1_drawing.add(Polygon([
            x2 - 5*math.cos(angle - 0.3), y2 - 5*math.sin(angle - 0.3),
            x2, y2,
            x2 - 5*math.cos(angle + 0.3), y2 - 5*math.sin(angle + 0.3)
        ], fillColor=color, strokeColor=color))
    
    elements.append(level1_drawing)
    elements.append(PageBreak())
    
    # Process Descriptions
    elements.append(Paragraph("Process Descriptions", heading1_style))
    elements.append(Spacer(1, 0.2*inch))
    
    process_desc = [
        ['Process', 'Description', 'Inputs', 'Outputs'],
        ['P1: User Authentication', 'Validates user credentials and manages sessions', 
         'Login credentials', 'Auth token, User session'],
        ['P2: Booking Management', 'Handles ferry booking creation and modification', 
         'Booking details, User info', 'Booking record, Confirmation'],
        ['P3: Seat Selection', 'Manages seat availability and selection', 
         'Trip details, Seat choices', 'Seat assignment, Availability status'],
        ['P4: Payment Processing', 'Processes payments and generates receipts', 
         'Payment proof, Booking data', 'Payment status, Receipt PDF'],
        ['P5: Schedule Management', 'Creates and updates ferry schedules', 
         'Route info, Time slots', 'Schedule records'],
        ['P6: Report Generation', 'Creates analytics and reports for admin', 
         'Date range, Filter criteria', 'PDF reports, Analytics data'],
        ['P7: System Configuration', 'Manages system settings and parameters', 
         'Configuration changes', 'Updated settings'],
    ]
    
    process_table = Table(process_desc, colWidths=[1.4*inch, 2*inch, 1.3*inch, 1.3*inch])
    process_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0d6efd')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
    
    elements.append(process_table)
    elements.append(PageBreak())
    
    # Data Store Descriptions
    elements.append(Paragraph("Data Store Descriptions", heading1_style))
    elements.append(Spacer(1, 0.2*inch))
    
    datastore_desc = [
        ['Data Store', 'Description', 'Contents'],
        ['D1: Users Database', 
         'Stores user account information and authentication data',
         'User ID, Email, Password hash, Name, Phone, Created date'],
        ['D2: Bookings Database', 
         'Contains all ferry booking records and payment status',
         'Booking ID, Reference number, User ID, Route, Date, Time, Seats, Price, Payment status'],
        ['D3: Schedules Database', 
         'Maintains ferry schedule information',
         'Schedule ID, Departure, Destination, Time, Active status, Date'],
        ['D4: Configuration Store', 
         'System settings and configuration parameters',
         'Ferry capacity, Route prices, System preferences'],
    ]
    
    ds_table = Table(datastore_desc, colWidths=[1.6*inch, 2.2*inch, 2.2*inch])
    ds_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#28a745')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
    ]))
    
    elements.append(ds_table)
    elements.append(Spacer(1, 0.5*inch))
    
    # Summary
    elements.append(Paragraph("Summary", heading1_style))
    elements.append(Spacer(1, 0.2*inch))
    
    summary_text = """
    The Data Flow Diagrams illustrate how data moves through the OceanLine Ferry Booking System:
    
    <br/><br/>
    <b>Context Diagram (Level 0):</b><br/>
    Shows the system boundary and interactions with external entities (Customer, Administrator, 
    Bank/Payment, Email System).
    
    <br/><br/>
    <b>Level 1 DFD:</b><br/>
    Breaks down the system into 7 core processes: User Authentication, Booking Management, 
    Seat Selection, Payment Processing, Schedule Management, Report Generation, and System 
    Configuration. Each process interacts with relevant data stores (Users, Bookings, Schedules, 
    Configuration).
    
    <br/><br/>
    <b>Data Stores:</b><br/>
    Four main data stores persist critical system information: user accounts, booking records, 
    ferry schedules, and system configuration settings.
    """
    
    elements.append(Paragraph(summary_text, styles['BodyText']))
    
    elements.append(Spacer(1, 0.5*inch))
    
    # Footer
    footer_data = [
        ['Student:', 'Hassan Solih'],
        ['ID:', 'ST7078'],
        ['Project:', 'OceanLine Ferry Booking System'],
        ['Date:', datetime.now().strftime('%B %d, %Y')],
    ]
    
    footer_table = Table(footer_data, colWidths=[1.5*inch, 3*inch])
    footer_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    
    elements.append(footer_table)
    
    # Build PDF
    doc.build(elements)
    print(f"✅ Data Flow Diagram PDF generated successfully: {filename}")
    return filename

if __name__ == "__main__":
    create_dfd_pdf()
