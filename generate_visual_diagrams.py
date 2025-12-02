"""
Generate Visual Diagrams PDF using Graphviz
Creates professional diagrams with actual graphics
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.enums import TA_CENTER
from datetime import datetime
import graphviz
import os

def create_visual_diagrams_pdf():
    """Generate PDF with visual diagrams"""
    
    filename = "OceanLine_Visual_Diagrams.pdf"
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
    elements.append(Paragraph("Visual System Diagrams", heading1_style))
    elements.append(Spacer(1, 0.5*inch))
    
    # Project info
    from reportlab.platypus import Table, TableStyle
    info_data = [
        ['Project:', 'OceanLine Ferry Booking System'],
        ['Student ID:', 'ST7078'],
        ['Name:', 'Hassan Solih'],
        ['Date:', datetime.now().strftime('%B %d, %Y')],
        ['Diagrams:', '6 Visual Diagrams'],
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
    
    # Create diagrams directory
    diagrams_dir = "diagram_images"
    if not os.path.exists(diagrams_dir):
        os.makedirs(diagrams_dir)
    
    # Diagram 1: System Architecture
    elements.append(Paragraph("1. System Architecture Diagram", heading1_style))
    elements.append(Spacer(1, 0.2*inch))
    
    arch_desc = "High-level layered architecture of the OceanLine ferry booking system."
    elements.append(Paragraph(arch_desc, styles['BodyText']))
    elements.append(Spacer(1, 0.2*inch))
    
    arch = graphviz.Digraph('architecture', format='png')
    arch.attr(rankdir='TB', bgcolor='white', fontname='Arial')
    arch.attr('node', shape='box', style='rounded,filled', fillcolor='lightblue', fontname='Arial')
    
    # Layers
    arch.node('client', 'Client Layer\n(Browser)', fillcolor='#e3f2fd')
    arch.node('presentation', 'Presentation Layer\n(Templates/HTML)', fillcolor='#bbdefb')
    arch.node('controller', 'Controller Layer\n(Flask Routes)', fillcolor='#90caf9')
    arch.node('business', 'Business Logic\n(Python Functions)', fillcolor='#64b5f6')
    arch.node('data', 'Data Access Layer\n(SQLAlchemy ORM)', fillcolor='#42a5f5')
    arch.node('database', 'Database Layer\n(MySQL/SQLite)', fillcolor='#2196f3')
    
    arch.edge('client', 'presentation', 'HTTP Request')
    arch.edge('presentation', 'controller', 'Route Call')
    arch.edge('controller', 'business', 'Process')
    arch.edge('business', 'data', 'Query')
    arch.edge('data', 'database', 'SQL')
    arch.edge('database', 'data', 'Result', style='dashed')
    arch.edge('data', 'business', 'Data', style='dashed')
    arch.edge('business', 'controller', 'Response', style='dashed')
    arch.edge('controller', 'presentation', 'Render', style='dashed')
    arch.edge('presentation', 'client', 'HTML', style='dashed')
    
    arch_file = os.path.join(diagrams_dir, 'architecture')
    arch.render(arch_file, cleanup=True)
    elements.append(Image(arch_file + '.png', width=5*inch, height=4*inch))
    elements.append(PageBreak())
    
    # Diagram 2: Database ERD
    elements.append(Paragraph("2. Database Entity Relationship Diagram", heading1_style))
    elements.append(Spacer(1, 0.2*inch))
    
    erd_desc = "Database schema showing tables, relationships, and key fields."
    elements.append(Paragraph(erd_desc, styles['BodyText']))
    elements.append(Spacer(1, 0.2*inch))
    
    erd = graphviz.Digraph('erd', format='png')
    erd.attr(rankdir='LR', bgcolor='white', fontname='Arial')
    erd.attr('node', shape='record', style='filled', fillcolor='lightyellow', fontname='Arial', fontsize='10')
    
    # Tables
    erd.node('users', '{<f0> users|<f1> id (PK)\\l|email (UK)\\l|password_hash\\l|name\\l|phone\\l|created_at\\l}')
    erd.node('bookings', '{<f0> ferry_bookings|<f1> id (PK)\\l|booking_reference (UK)\\l|user_id (FK)\\l|name\\l|email\\l|departure\\l|destination\\l|date\\l|time\\l|seats\\l|selected_seats\\l|total_price\\l|payment_status\\l|is_roundtrip\\l|created_at\\l}')
    erd.node('schedules', '{<f0> schedules|<f1> id (PK)\\l|departure\\l|destination\\l|time\\l|active\\l|created_at\\l}')
    erd.node('daily_schedules', '{<f0> daily_schedules|<f1> id (PK)\\l|departure\\l|destination\\l|date\\l|time\\l|active\\l|created_at\\l}')
    
    # Relationships
    erd.edge('users:f1', 'bookings:f1', label='1:N', color='blue', fontcolor='blue', fontsize='9')
    
    erd_file = os.path.join(diagrams_dir, 'erd')
    erd.render(erd_file, cleanup=True)
    elements.append(Image(erd_file + '.png', width=6*inch, height=4*inch))
    elements.append(PageBreak())
    
    # Diagram 3: User Booking Flow
    elements.append(Paragraph("3. User Booking Process Flow", heading1_style))
    elements.append(Spacer(1, 0.2*inch))
    
    flow_desc = "Complete user journey from homepage to booking confirmation."
    elements.append(Paragraph(flow_desc, styles['BodyText']))
    elements.append(Spacer(1, 0.2*inch))
    
    flow = graphviz.Digraph('user_flow', format='png')
    flow.attr(rankdir='TB', bgcolor='white', fontname='Arial')
    flow.attr('node', shape='box', style='rounded,filled', fillcolor='lightgreen', fontname='Arial', fontsize='10')
    
    flow.node('start', 'Homepage', shape='ellipse', fillcolor='#c8e6c9')
    flow.node('login', 'Login/Register', fillcolor='#a5d6a7')
    flow.node('book', 'Booking Form', fillcolor='#81c784')
    flow.node('seats', 'Select Seats', fillcolor='#66bb6a')
    flow.node('payment', 'Payment', fillcolor='#4caf50')
    flow.node('confirm', 'Confirmation', fillcolor='#43a047')
    flow.node('end', 'View Receipt', shape='ellipse', fillcolor='#388e3c')
    
    flow.edge('start', 'login', 'Click Book Now')
    flow.edge('login', 'book', 'Authenticated')
    flow.edge('book', 'seats', 'Submit Form\n(Route, Date, Time)')
    flow.edge('seats', 'payment', 'Choose Seats')
    flow.edge('payment', 'confirm', 'Upload Proof\n/Bank Transfer')
    flow.edge('confirm', 'end', 'Download PDF')
    
    flow_file = os.path.join(diagrams_dir, 'user_flow')
    flow.render(flow_file, cleanup=True)
    elements.append(Image(flow_file + '.png', width=4.5*inch, height=5*inch))
    elements.append(PageBreak())
    
    # Diagram 4: Admin Dashboard Flow
    elements.append(Paragraph("4. Admin Dashboard Flow", heading1_style))
    elements.append(Spacer(1, 0.2*inch))
    
    admin_desc = "Administrator workflow for system management."
    elements.append(Paragraph(admin_desc, styles['BodyText']))
    elements.append(Spacer(1, 0.2*inch))
    
    admin = graphviz.Digraph('admin_flow', format='png')
    admin.attr(rankdir='TB', bgcolor='white', fontname='Arial')
    admin.attr('node', shape='box', style='rounded,filled', fillcolor='#ffe0b2', fontname='Arial', fontsize='10')
    
    admin.node('login', 'Admin Login', shape='ellipse', fillcolor='#ffcc80')
    admin.node('dashboard', 'Dashboard\n(Stats & Revenue)', fillcolor='#ffb74d')
    admin.node('bookings', 'Manage\nBookings', fillcolor='#ffa726')
    admin.node('schedules', 'Manage\nSchedules', fillcolor='#ff9800')
    admin.node('payments', 'Verify\nPayments', fillcolor='#fb8c00')
    admin.node('reports', 'View\nReports', fillcolor='#f57c00')
    admin.node('settings', 'System\nSettings', fillcolor='#ef6c00')
    
    admin.edge('login', 'dashboard', 'Auth Success')
    admin.edge('dashboard', 'bookings')
    admin.edge('dashboard', 'schedules')
    admin.edge('dashboard', 'payments')
    admin.edge('dashboard', 'reports')
    admin.edge('dashboard', 'settings')
    
    admin_file = os.path.join(diagrams_dir, 'admin_flow')
    admin.render(admin_file, cleanup=True)
    elements.append(Image(admin_file + '.png', width=5*inch, height=4*inch))
    elements.append(PageBreak())
    
    # Diagram 5: API Request Flow
    elements.append(Paragraph("5. API Request-Response Flow", heading1_style))
    elements.append(Spacer(1, 0.2*inch))
    
    api_desc = "AJAX API endpoints for dynamic frontend interactions."
    elements.append(Paragraph(api_desc, styles['BodyText']))
    elements.append(Spacer(1, 0.2*inch))
    
    api = graphviz.Digraph('api_flow', format='png')
    api.attr(rankdir='LR', bgcolor='white', fontname='Arial')
    api.attr('node', shape='box', style='rounded,filled', fontname='Arial', fontsize='10')
    
    # Client side
    api.node('browser', 'Browser\n(JavaScript)', fillcolor='#e1bee7', shape='box3d')
    
    # API endpoints
    api.node('get_price', 'POST /get_price\n(Route → Price)', fillcolor='#ce93d8')
    api.node('get_times', 'POST /get_times\n(Route + Date → Times)', fillcolor='#ba68c8')
    api.node('get_seats', 'POST /get_available_seats\n(Trip → Booked Seats)', fillcolor='#ab47bc')
    api.node('pay', 'POST /pay\n(Generate PDF)', fillcolor='#9c27b0')
    
    # Server side
    api.node('server', 'Flask Server\n(Process & Query)', fillcolor='#8e24aa', shape='cylinder')
    
    api.edge('browser', 'get_price', 'AJAX')
    api.edge('get_price', 'server')
    api.edge('server', 'get_price', 'JSON', style='dashed')
    api.edge('get_price', 'browser', 'Response', style='dashed')
    
    api.edge('browser', 'get_times', 'AJAX')
    api.edge('get_times', 'server')
    
    api.edge('browser', 'get_seats', 'AJAX')
    api.edge('get_seats', 'server')
    
    api.edge('browser', 'pay', 'AJAX')
    api.edge('pay', 'server')
    api.edge('server', 'pay', 'PDF', style='dashed')
    
    api_file = os.path.join(diagrams_dir, 'api_flow')
    api.render(api_file, cleanup=True)
    elements.append(Image(api_file + '.png', width=6*inch, height=3.5*inch))
    elements.append(PageBreak())
    
    # Diagram 6: Deployment Architecture
    elements.append(Paragraph("6. Deployment Architecture", heading1_style))
    elements.append(Spacer(1, 0.2*inch))
    
    deploy_desc = "Production deployment infrastructure."
    elements.append(Paragraph(deploy_desc, styles['BodyText']))
    elements.append(Spacer(1, 0.2*inch))
    
    deploy = graphviz.Digraph('deployment', format='png')
    deploy.attr(rankdir='TB', bgcolor='white', fontname='Arial')
    deploy.attr('node', shape='box', style='filled', fontname='Arial', fontsize='10')
    
    # Internet
    deploy.node('internet', 'Internet\n(Users)', shape='cloud', fillcolor='#b3e5fc')
    
    # Load balancer
    deploy.node('lb', 'Load Balancer\n(nginx/ALB)', fillcolor='#81d4fa')
    
    # App servers
    with deploy.subgraph(name='cluster_0') as c:
        c.attr(label='Application Servers', style='dashed')
        c.node('app1', 'Flask App 1\n(Gunicorn)', fillcolor='#4fc3f7')
        c.node('app2', 'Flask App 2\n(Gunicorn)', fillcolor='#4fc3f7')
        c.node('app3', 'Flask App 3\n(Gunicorn)', fillcolor='#4fc3f7')
    
    # Database
    deploy.node('db_primary', 'MySQL\nPrimary', fillcolor='#29b6f6', shape='cylinder')
    deploy.node('db_replica', 'MySQL\nReplica', fillcolor='#03a9f4', shape='cylinder')
    
    # Cache
    deploy.node('redis', 'Redis\nCache', fillcolor='#039be5', shape='cylinder')
    
    # Storage
    deploy.node('s3', 'S3/Storage\n(Files)', fillcolor='#0288d1', shape='folder')
    
    # Connections
    deploy.edge('internet', 'lb', 'HTTPS')
    deploy.edge('lb', 'app1')
    deploy.edge('lb', 'app2')
    deploy.edge('lb', 'app3')
    
    deploy.edge('app1', 'db_primary', 'Read/Write')
    deploy.edge('app2', 'db_primary', 'Read/Write')
    deploy.edge('app3', 'db_replica', 'Read Only', style='dashed')
    
    deploy.edge('app1', 'redis', 'Cache')
    deploy.edge('app2', 'redis', 'Cache')
    
    deploy.edge('app1', 's3', 'Upload')
    deploy.edge('db_primary', 'db_replica', 'Replication', style='dotted')
    
    deploy_file = os.path.join(diagrams_dir, 'deployment')
    deploy.render(deploy_file, cleanup=True)
    elements.append(Image(deploy_file + '.png', width=6*inch, height=5*inch))
    elements.append(PageBreak())
    
    # Summary
    elements.append(Paragraph("Summary", heading1_style))
    elements.append(Spacer(1, 0.2*inch))
    
    summary_text = """
    The OceanLine Ferry Booking System implements a well-structured, scalable architecture 
    with clear separation of concerns. The visual diagrams illustrate the layered architecture, 
    database relationships, user workflows, admin management, API interactions, and production 
    deployment infrastructure. The system is designed for reliability, maintainability, and 
    future scalability.
    """
    elements.append(Paragraph(summary_text, styles['BodyText']))
    
    elements.append(Spacer(1, 0.5*inch))
    
    # Footer
    footer_data = [
        ['Student:', 'Hassan Solih'],
        ['ID:', 'ST7078'],
        ['Date:', datetime.now().strftime('%B %d, %Y')],
    ]
    
    footer_table = Table(footer_data, colWidths=[1.5*inch, 3*inch])
    footer_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))
    
    elements.append(footer_table)
    
    # Build PDF
    doc.build(elements)
    print(f"✅ Visual diagrams PDF generated successfully: {filename}")
    print(f"   Diagram images saved in: {diagrams_dir}/")
    return filename

if __name__ == "__main__":
    create_visual_diagrams_pdf()
