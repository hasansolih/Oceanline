"""
Generate Enhanced Visual Diagrams PDF using PIL/Pillow
Creates professional diagrams with box-and-arrow graphics
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Table, TableStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Circle, Polygon
from reportlab.graphics import renderPDF
from datetime import datetime
import os

def create_enhanced_diagrams_pdf():
    """Generate PDF with enhanced visual diagrams using reportlab graphics"""
    
    filename = "OceanLine_Enhanced_Diagrams.pdf"
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
    
    # Title Page
    elements.append(Spacer(1, 1*inch))
    elements.append(Paragraph("OceanLine Ferry Service", title_style))
    elements.append(Paragraph("Enhanced System Diagrams", heading1_style))
    elements.append(Spacer(1, 0.5*inch))
    
    # Project info
    info_data = [
        ['Project:', 'OceanLine Ferry Booking System'],
        ['Student ID:', 'ST7078'],
        ['Name:', 'Hassan Solih'],
        ['Date:', datetime.now().strftime('%B %d, %Y')],
        ['Diagrams:', '6 Professional Visual Diagrams'],
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
    
    # Diagram 1: System Architecture Layers
    elements.append(Paragraph("1. System Architecture - Layered Design", heading1_style))
    elements.append(Spacer(1, 0.2*inch))
    
    arch_desc = "The OceanLine system follows a classic layered architecture pattern with clear separation of concerns."
    elements.append(Paragraph(arch_desc, styles['BodyText']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Create architecture diagram
    arch_drawing = Drawing(400, 400)
    
    # Layers (top to bottom)
    layers = [
        ("Client Layer", "Browser - HTML/CSS/JavaScript", colors.HexColor('#e3f2fd')),
        ("Presentation Layer", "Jinja2 Templates", colors.HexColor('#bbdefb')),
        ("Controller Layer", "Flask Routes & Views", colors.HexColor('#90caf9')),
        ("Business Logic", "Python Functions", colors.HexColor('#64b5f6')),
        ("Data Access Layer", "SQLAlchemy ORM", colors.HexColor('#42a5f5')),
        ("Database Layer", "MySQL / SQLite", colors.HexColor('#2196f3'))
    ]
    
    y_start = 380
    box_height = 50
    box_width = 300
    x_offset = 50
    
    for i, (title, subtitle, color) in enumerate(layers):
        y = y_start - (i * (box_height + 10))
        
        # Draw box
        arch_drawing.add(Rect(x_offset, y, box_width, box_height, 
                             fillColor=color, strokeColor=colors.black, strokeWidth=2))
        
        # Add title
        arch_drawing.add(String(x_offset + box_width/2, y + box_height - 15, title,
                               fontSize=12, fontName='Helvetica-Bold', textAnchor='middle'))
        
        # Add subtitle
        arch_drawing.add(String(x_offset + box_width/2, y + 15, subtitle,
                               fontSize=10, fontName='Helvetica', textAnchor='middle'))
        
        # Draw arrow to next layer
        if i < len(layers) - 1:
            arrow_x = x_offset + box_width/2
            arrow_start_y = y
            arrow_end_y = y - 10
            
            arch_drawing.add(Line(arrow_x, arrow_start_y, arrow_x, arrow_end_y,
                                strokeColor=colors.black, strokeWidth=2))
            
            # Arrow head
            arch_drawing.add(Polygon([arrow_x-5, arrow_end_y, 
                                    arrow_x+5, arrow_end_y,
                                    arrow_x, arrow_end_y-5],
                                   fillColor=colors.black, strokeColor=colors.black))
    
    elements.append(arch_drawing)
    elements.append(PageBreak())
    
    # Diagram 2: Database Schema
    elements.append(Paragraph("2. Database Entity Relationship Model", heading1_style))
    elements.append(Spacer(1, 0.2*inch))
    
    db_desc = "The database consists of four main tables with clear relationships and constraints."
    elements.append(Paragraph(db_desc, styles['BodyText']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Database tables diagram
    db_drawing = Drawing(500, 350)
    
    # Helper function to draw table
    def draw_table_box(drawing, x, y, title, fields, width=140, color=colors.HexColor('#fff9c4')):
        height = 30 + (len(fields) * 15)
        
        # Title box
        drawing.add(Rect(x, y + height - 30, width, 30, 
                        fillColor=colors.HexColor('#fdd835'), strokeColor=colors.black, strokeWidth=2))
        drawing.add(String(x + width/2, y + height - 15, title,
                          fontSize=11, fontName='Helvetica-Bold', textAnchor='middle'))
        
        # Fields box
        drawing.add(Rect(x, y, width, height - 30, 
                        fillColor=color, strokeColor=colors.black, strokeWidth=2))
        
        # Draw fields
        for i, field in enumerate(fields):
            drawing.add(String(x + 5, y + height - 45 - (i * 15), field,
                             fontSize=8, fontName='Helvetica', textAnchor='start'))
        
        return height
    
    # Users table
    users_fields = ['id (PK)', 'email (UNIQUE)', 'password_hash', 'name', 'phone', 'created_at']
    draw_table_box(db_drawing, 20, 180, 'users', users_fields)
    
    # Bookings table
    bookings_fields = ['id (PK)', 'booking_reference (UK)', 'user_id (FK)', 'name', 
                       'departure', 'destination', 'date', 'time', 'seats', 
                       'selected_seats', 'total_price', 'payment_status']
    booking_height = draw_table_box(db_drawing, 200, 150, 'ferry_bookings', bookings_fields, width=160)
    
    # Schedules table
    schedules_fields = ['id (PK)', 'departure', 'destination', 'time', 'active', 'created_at']
    draw_table_box(db_drawing, 20, 20, 'schedules', schedules_fields)
    
    # Daily schedules table
    daily_fields = ['id (PK)', 'departure', 'destination', 'date', 'time', 'active']
    draw_table_box(db_drawing, 200, 20, 'daily_schedules', daily_fields, width=160)
    
    # Relationship arrow (users -> bookings)
    db_drawing.add(Line(160, 240, 200, 240, strokeColor=colors.blue, strokeWidth=2))
    db_drawing.add(String(180, 245, '1:N', fontSize=9, fontName='Helvetica-Bold', 
                         textAnchor='middle', fillColor=colors.blue))
    
    elements.append(db_drawing)
    elements.append(PageBreak())
    
    # Diagram 3: User Booking Flow
    elements.append(Paragraph("3. User Booking Process Workflow", heading1_style))
    elements.append(Spacer(1, 0.2*inch))
    
    flow_desc = "Step-by-step user journey from homepage to booking confirmation with payment."
    elements.append(Paragraph(flow_desc, styles['BodyText']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Booking flow diagram
    flow_drawing = Drawing(400, 500)
    
    # Helper for flow boxes
    def draw_flow_step(drawing, x, y, text, color=colors.HexColor('#a5d6a7'), width=200, height=50):
        drawing.add(Rect(x, y, width, height, 
                        fillColor=color, strokeColor=colors.black, 
                        strokeWidth=2, rx=10, ry=10))
        
        # Split text into lines if needed
        lines = text.split('\n')
        start_y = y + height/2 + (len(lines) * 5)
        for line in lines:
            drawing.add(String(x + width/2, start_y, line,
                             fontSize=10, fontName='Helvetica-Bold', textAnchor='middle'))
            start_y -= 12
    
    # Flow steps
    steps = [
        ("Homepage\nLanding Page", colors.HexColor('#c8e6c9')),
        ("Login / Register\nAuthentication", colors.HexColor('#a5d6a7')),
        ("Booking Form\nRoute, Date, Passengers", colors.HexColor('#81c784')),
        ("Select Seats\nChoose Seat Numbers", colors.HexColor('#66bb6a')),
        ("Payment\nUpload Proof/Bank Details", colors.HexColor('#4caf50')),
        ("Confirmation\nBooking Reference", colors.HexColor('#43a047')),
        ("Receipt PDF\nDownload/Print", colors.HexColor('#388e3c'))
    ]
    
    x = 100
    y_start = 470
    step_gap = 65
    
    for i, (step_text, color) in enumerate(steps):
        y = y_start - (i * step_gap)
        draw_flow_step(flow_drawing, x, y, step_text, color)
        
        # Draw arrow to next step
        if i < len(steps) - 1:
            arrow_x = x + 100
            arrow_start_y = y
            arrow_end_y = y - 15
            
            flow_drawing.add(Line(arrow_x, arrow_start_y, arrow_x, arrow_end_y,
                                strokeColor=colors.black, strokeWidth=2))
            
            # Arrow head
            flow_drawing.add(Polygon([arrow_x-4, arrow_end_y, 
                                    arrow_x+4, arrow_end_y,
                                    arrow_x, arrow_end_y-6],
                                   fillColor=colors.black, strokeColor=colors.black))
    
    elements.append(flow_drawing)
    elements.append(PageBreak())
    
    # Diagram 4: Admin Dashboard Features
    elements.append(Paragraph("4. Admin Dashboard Management System", heading1_style))
    elements.append(Spacer(1, 0.2*inch))
    
    admin_desc = "Centralized admin interface for comprehensive system management and monitoring."
    elements.append(Paragraph(admin_desc, styles['BodyText']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Admin dashboard diagram
    admin_drawing = Drawing(500, 350)
    
    # Central dashboard circle
    admin_drawing.add(Circle(250, 175, 50, 
                            fillColor=colors.HexColor('#ffb74d'), 
                            strokeColor=colors.black, strokeWidth=3))
    admin_drawing.add(String(250, 175, 'Admin',
                           fontSize=14, fontName='Helvetica-Bold', textAnchor='middle'))
    admin_drawing.add(String(250, 160, 'Dashboard',
                           fontSize=12, fontName='Helvetica-Bold', textAnchor='middle'))
    
    # Surrounding feature boxes
    features = [
        ("Bookings\nManagement", 250, 280, colors.HexColor('#ffa726')),
        ("Schedule\nManagement", 380, 220, colors.HexColor('#ff9800')),
        ("Payment\nVerification", 380, 130, colors.HexColor('#fb8c00')),
        ("Reports &\nAnalytics", 250, 70, colors.HexColor('#f57c00')),
        ("System\nSettings", 120, 130, colors.HexColor('#ef6c00')),
        ("User\nManagement", 120, 220, colors.HexColor('#e65100'))
    ]
    
    for feature_text, x, y, color in features:
        # Feature box
        admin_drawing.add(Rect(x - 40, y - 20, 80, 40,
                              fillColor=color, strokeColor=colors.black, 
                              strokeWidth=2, rx=5, ry=5))
        
        lines = feature_text.split('\n')
        admin_drawing.add(String(x, y + 5, lines[0],
                                fontSize=9, fontName='Helvetica-Bold', textAnchor='middle'))
        admin_drawing.add(String(x, y - 8, lines[1],
                                fontSize=9, fontName='Helvetica', textAnchor='middle'))
        
        # Line to center
        admin_drawing.add(Line(x, y, 250, 175, 
                             strokeColor=colors.HexColor('#333333'), strokeWidth=1.5))
    
    elements.append(admin_drawing)
    elements.append(PageBreak())
    
    # Diagram 5: API Endpoints
    elements.append(Paragraph("5. AJAX API Endpoints Architecture", heading1_style))
    elements.append(Spacer(1, 0.2*inch))
    
    api_desc = "RESTful API endpoints for dynamic client-server communication and real-time data exchange."
    elements.append(Paragraph(api_desc, styles['BodyText']))
    elements.append(Spacer(1, 0.3*inch))
    
    # API table
    api_data = [
        ['Endpoint', 'Method', 'Purpose', 'Response'],
        ['/get_price', 'POST', 'Calculate route price', 'JSON: {price: float}'],
        ['/get_times', 'POST', 'Get available times', 'JSON: {times: []}'],
        ['/get_available_seats', 'POST', 'Get booked seats', 'JSON: {booked: []}'],
        ['/pay', 'POST', 'Generate receipt PDF', 'PDF File'],
        ['/admin/update-payment', 'POST', 'Update payment status', 'JSON: {success: bool}'],
    ]
    
    api_table = Table(api_data, colWidths=[1.5*inch, 0.8*inch, 1.8*inch, 1.7*inch])
    api_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0d6efd')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    elements.append(api_table)
    elements.append(Spacer(1, 0.4*inch))
    
    # API flow diagram
    api_drawing = Drawing(450, 200)
    
    # Browser box
    api_drawing.add(Rect(20, 80, 100, 60, fillColor=colors.HexColor('#e1bee7'), 
                        strokeColor=colors.black, strokeWidth=2))
    api_drawing.add(String(70, 115, 'Browser',
                          fontSize=12, fontName='Helvetica-Bold', textAnchor='middle'))
    api_drawing.add(String(70, 95, 'JavaScript',
                          fontSize=10, fontName='Helvetica', textAnchor='middle'))
    
    # Flask server box
    api_drawing.add(Rect(330, 80, 100, 60, fillColor=colors.HexColor('#9c27b0'), 
                        strokeColor=colors.black, strokeWidth=2))
    api_drawing.add(String(380, 115, 'Flask Server',
                          fontSize=12, fontName='Helvetica-Bold', textAnchor='middle', fillColor=colors.white))
    api_drawing.add(String(380, 95, 'Python/SQLAlchemy',
                          fontSize=9, fontName='Helvetica', textAnchor='middle', fillColor=colors.white))
    
    # Request arrow
    api_drawing.add(Line(120, 125, 330, 125, strokeColor=colors.green, strokeWidth=2))
    api_drawing.add(String(225, 135, 'AJAX POST Request',
                          fontSize=10, fontName='Helvetica-Bold', textAnchor='middle', fillColor=colors.green))
    api_drawing.add(Polygon([325, 125, 330, 128, 330, 122],
                           fillColor=colors.green, strokeColor=colors.green))
    
    # Response arrow
    api_drawing.add(Line(330, 95, 120, 95, strokeColor=colors.blue, strokeWidth=2, strokeDashArray=[4, 2]))
    api_drawing.add(String(225, 85, 'JSON Response',
                          fontSize=10, fontName='Helvetica-Bold', textAnchor='middle', fillColor=colors.blue))
    api_drawing.add(Polygon([125, 95, 120, 98, 120, 92],
                           fillColor=colors.blue, strokeColor=colors.blue))
    
    elements.append(api_drawing)
    elements.append(PageBreak())
    
    # Diagram 6: Technology Stack
    elements.append(Paragraph("6. Technology Stack Overview", heading1_style))
    elements.append(Spacer(1, 0.2*inch))
    
    tech_desc = "Complete technology stack used in the OceanLine Ferry Booking System."
    elements.append(Paragraph(tech_desc, styles['BodyText']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Technology stack table
    tech_data = [
        ['Layer', 'Technology', 'Version', 'Purpose'],
        ['Frontend', 'HTML5/CSS3', '-', 'Structure & Styling'],
        ['', 'Bootstrap', '5.3', 'Responsive Design'],
        ['', 'JavaScript', 'ES6', 'Client Interactions'],
        ['', 'Chart.js', '4.4.0', 'Data Visualization'],
        ['Backend', 'Python', '3.14', 'Core Language'],
        ['', 'Flask', '3.1.2', 'Web Framework'],
        ['', 'Flask-Login', '0.6.3', 'Authentication'],
        ['', 'Flask-WTF', '1.2.2', 'CSRF Protection'],
        ['Database', 'SQLAlchemy', '2.0.44', 'ORM'],
        ['', 'MySQL', '8.0', 'Production DB'],
        ['', 'SQLite', '3', 'Development DB'],
        ['Utilities', 'ReportLab', '4.4.5', 'PDF Generation'],
        ['', 'Werkzeug', '3.1.3', 'Security Utils'],
        ['', 'Pillow', '11.0.0', 'Image Processing'],
    ]
    
    tech_table = Table(tech_data, colWidths=[1.2*inch, 1.5*inch, 0.8*inch, 2.3*inch])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#28a745')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('SPAN', (0, 1), (0, 4)),  # Frontend span
        ('SPAN', (0, 5), (0, 8)),  # Backend span
        ('SPAN', (0, 9), (0, 11)), # Database span
        ('SPAN', (0, 12), (0, 14)), # Utilities span
        ('BACKGROUND', (0, 1), (0, 4), colors.HexColor('#e3f2fd')),
        ('BACKGROUND', (0, 5), (0, 8), colors.HexColor('#fff3e0')),
        ('BACKGROUND', (0, 9), (0, 11), colors.HexColor('#f3e5f5')),
        ('BACKGROUND', (0, 12), (0, 14), colors.HexColor('#e8f5e9')),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('VALIGN', (0, 1), (0, -1), 'TOP'),
    ]))
    
    elements.append(tech_table)
    elements.append(PageBreak())
    
    # Summary Page
    elements.append(Paragraph("Documentation Summary", heading1_style))
    elements.append(Spacer(1, 0.3*inch))
    
    summary_text = """
    The OceanLine Ferry Booking System is a comprehensive web application built with modern 
    technologies and following best practices in software architecture. The system implements:
    
    <br/><br/>
    <b>Architecture Highlights:</b><br/>
    • Layered MVC architecture for separation of concerns<br/>
    • RESTful API design for AJAX interactions<br/>
    • Secure authentication and authorization<br/>
    • Responsive frontend with Bootstrap 5.3<br/>
    • Database-agnostic ORM with SQLAlchemy<br/>
    
    <br/>
    <b>Key Features:</b><br/>
    • Real-time seat availability checking<br/>
    • Dynamic price calculation<br/>
    • Automated PDF receipt generation<br/>
    • Admin dashboard with analytics<br/>
    • Payment verification system<br/>
    • Comprehensive reporting<br/>
    
    <br/>
    <b>Security Features:</b><br/>
    • CSRF protection on all forms<br/>
    • Password hashing with Werkzeug<br/>
    • Session-based authentication<br/>
    • Role-based access control<br/>
    
    <br/>
    The system is designed for scalability, maintainability, and future enhancements. 
    All diagrams in this document illustrate the professional architecture and implementation 
    of the OceanLine Ferry Booking System.
    """
    
    elements.append(Paragraph(summary_text, styles['BodyText']))
    
    elements.append(Spacer(1, 0.8*inch))
    
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
    print(f"✅ Enhanced visual diagrams PDF generated successfully: {filename}")
    return filename

if __name__ == "__main__":
    create_enhanced_diagrams_pdf()
